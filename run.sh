#!/bin/bash
# runs without ssl cert

FLASK_APP=up.py python -m flask run --host 0.0.0.0
