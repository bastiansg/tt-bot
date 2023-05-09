#!/bin/env sh

# reinstall local packages with no deps & edition mode
pip install --break-system-packages --no-deps -e /src/tt_bot

jupyter-lab --ip=0.0.0.0 --allow-root --no-browser
