#!/usr/bin/env bash

find . -type f -name "*-2026_Conflict*"

~/nsh/junk-drawer/stage-files.sh && git stash && git pull && git stash pop && echo "" && git status
