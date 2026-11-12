#!/usr/bin/env bash

~/nsh/junk-drawer/stage-files.sh && git stash && git pull && git stash pop && echo "" && git status
