#!/usr/bin/env bash
set -e

if ! [[ $(which pytest) ]]; then
    pip install pytest
fi

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
cd "$ROOT_DIR"

pytest --doctest-modules pycats
