#!/usr/bin/env bash

set -e
set -x

python -m pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=70 -q "$@"
