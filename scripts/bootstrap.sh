#!/usr/bin/env bash
set -euo pipefail
if [[ "$(uname -s)" != "Linux" ]]; then
  echo 'LogicaSophia bootstrap currently targets Linux.' >&2
  exit 1
fi
python3 -m venv .venv
.venv/bin/python -m pip install -e .
echo 'Installed. Use: source .venv/bin/activate && logicasophia inventory'
