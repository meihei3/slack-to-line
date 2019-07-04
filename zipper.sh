#!/usr/bin/env bash

zip -r upload.zip . -x '*.git*' '*.idea*' '*__pycache__*' '*.iml'\
 'requirements.txt' 'README.md' '.gitignore' '*.zip' '*zipper.sh'\
 'packages/*.dist-info*' 'packages/bin' '.python-version' 't.py'