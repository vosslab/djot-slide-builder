# source_me.sh - shell environment for running this repo's Python.
# Usage: source source_me.sh && python3 ...
# This is a bash script sourced into your shell, not run directly.

# Require bash: the checks below and the repo's tab-indented shell style are
# bash-specific. Fail loudly rather than misbehave under another shell.
set | grep -q '^BASH_VERSION=' || echo "use bash for your shell"
set | grep -q '^BASH_VERSION=' || exit 1

# Source ~/.bashrc FIRST, before any repo-specific environment extension below.
# ~/.bashrc applies local shell setup (PATH, etc.) and resets some variables --
# it clears PYTHONPATH (verified). Anything that sets PYTHONPATH must run after
# this line, or ~/.bashrc would wipe it.
source ~/.bashrc

# Make Cargo-installed optional source validators, including Jotdown, available
# to repository commands when the conventional per-user Cargo bin directory exists.
CARGO_BIN="$HOME/.cargo/bin"
if [[ -d "$CARGO_BIN" ]]; then
	export PATH="$CARGO_BIN:$PATH"
fi
unset CARGO_BIN

# Python runtime defaults: unbuffered stdout/stderr, and no .pyc/__pycache__
# files written on import.
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Make repository packages available to Python commands after sourcing this environment.
REPO_ROOT="$(git rev-parse --show-toplevel)"
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"
unset REPO_ROOT
