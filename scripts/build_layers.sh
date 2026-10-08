#!/usr/bin/env bash
set -euo pipefail

rm -rf layer/pillow/python layer/reportlab/python
mkdir -p layer/pillow/python layer/reportlab/python

python3 -m pip install --upgrade --target layer/pillow/python Pillow
python3 -m pip install --upgrade --target layer/reportlab/python reportlab

echo "Lambda layers built under layer/"
