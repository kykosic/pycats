#!/usr/bin/env bash
set -e

if ! [[ $(which flake8) ]]; then
    pip install flake8
fi

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
cd "$ROOT_DIR"

flake8 --exclude test_* pycats
