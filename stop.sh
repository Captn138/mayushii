#!/usr/bin/bash

set -e

tmux kill-session -a || true
if [[ -d ~/venv ]]; then rm -r ~/venv; fi
if [[ -d ~/bot ]]; then rm -r ~/bot; fi
rm start.sh stop.sh
