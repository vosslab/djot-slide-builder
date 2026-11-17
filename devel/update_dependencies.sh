#!/usr/bin/env bash
# This file is vendored. Local changes can and will be overwritten by propagation.

# Refresh and validate one project locally; retain changes on failure.
set -uo pipefail
if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
	printf '%s\n' 'Usage: update_dependencies.sh [--package-json PATH]'
	exit 0
fi
case "$#:${1:-}" in
	0:|2:--package-json|2:-p) ;;
	*) echo "ERROR: use update_dependencies.sh [--package-json PATH]" >&2; exit 2 ;;
esac
repo_root="$(git rev-parse --show-toplevel)" || exit 1
cd "$repo_root" || exit 1
[ ! -f source_me.sh ] || source source_me.sh
if ! python3 -c 'import sys; raise SystemExit(sys.version_info < (3, 10))'; then
	echo "ERROR: configured Python must be 3.10 or newer." >&2
	exit 1
fi
failed=0
stage() {
	local label="$1"
	shift
	echo "==> $label"
	if "$@"; then
		echo "PASS: $label"
		return 0
	fi
	echo "FAIL: $label" >&2
	failed=1
	return 1
}
has_script() {
	node -e 'const d = require("./package.json"); process.exit(d.scripts && d.scripts[process.argv[1]] ? 0 : 1)' "$1"
}
if ! manifest="$(python3 devel/sync_typescript_package_pins.py --select-only "$@")"; then
	echo "FAIL: package manifest selection failed." >&2
	exit 1
fi
package_dir="$(dirname "$manifest")"
cd "$package_dir" || exit 1
echo "package manifest: $manifest"
workspace_root="$package_dir"
while [ "$workspace_root" != "$repo_root" ]; do
	workspace_root="$(dirname "$workspace_root")"
	if node -e 'const fs = require("fs"); const p = process.argv[1]; process.exit(fs.existsSync(p) && JSON.parse(fs.readFileSync(p)).workspaces ? 0 : 1)' "$workspace_root/package.json"; then
		echo "ERROR: select the npm workspace root and use its declared workspace checks." >&2
		exit 1
	fi
done
checker="$repo_root/devel/check_typescript_package_policy.py"
ready=1
stage "refresh direct dependencies and overrides" python3 \
	"$repo_root/devel/sync_typescript_package_pins.py" --package-json "$manifest" --apply || ready=0
if [ "$ready" -eq 1 ]; then
	stage "check package manifest policy" python3 "$checker" "$manifest" || ready=0
fi
if [ "$ready" -eq 1 ]; then
	stage "install refreshed dependency tree" npm install --strict-peer-deps || ready=0
fi
if [ "$ready" -eq 1 ]; then
	stage "check resolved dependency tree" python3 "$checker" --check-resolved-freshness "$manifest"
	audit_file="$(mktemp "${TMPDIR:-/tmp}/npm-audit.XXXXXX")" || exit 1
	trap 'rm -f "$audit_file"' EXIT
	audit_status=0
	npm audit --json >"$audit_file" || audit_status=$?
	stage "audit resolved dependency tree" python3 "$checker" --audit-json "$audit_file" || audit_status=1
	if [ "$audit_status" -ne 0 ]; then
		failed=1
		cat "$audit_file" >&2
	fi
	if [ -x ./check_codebase.sh ]; then
		stage "codebase checks" ./check_codebase.sh
	elif has_script check; then
		stage "project checks" npm run check
	else
		stage "typecheck" npm run typecheck
		stage "tests" npm test
	fi
	if [ -f ./build_github_pages.sh ]; then
		stage "production build" bash ./build_github_pages.sh
	elif has_script build; then
		stage "production build" npm run build
	else
		echo "SKIP: no production build is declared."
	fi
	stage "clean lockfile install" npm ci --no-audit
else
	echo "SKIP: later stages require a refreshed, installed dependency tree." >&2
fi
if [ "$failed" -ne 0 ]; then
	echo "INCOMPLETE: dependency maintenance failed; keep the updated files and repair forward." >&2
	exit 1
fi
echo "PASS: dependency maintenance completed for $manifest"
