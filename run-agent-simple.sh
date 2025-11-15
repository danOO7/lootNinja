#!/bin/bash
cd "$(dirname "$0")/agent" || exit 1
source .venv/bin/activate
cd src
python -m main_simple
