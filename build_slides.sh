#!/usr/bin/env bash

set -euo pipefail


usage() {
	cat <<'EOF'
Usage: ./build_slides.sh FOLDER

Build every .djot deck recursively below FOLDER as PDF, PPTX, and ODP.

For one deck or a selected destination, use deck_tools.py build instead.
EOF
}


if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
	usage
	exit 0
fi

if [[ "$#" -ne 1 ]]; then
	usage >&2
	exit 2
fi

repo_root="$(git rev-parse --show-toplevel)"
source "$repo_root/source_me.sh"
exec python3 "$repo_root/deck_tools.py" build --format all "$1"
