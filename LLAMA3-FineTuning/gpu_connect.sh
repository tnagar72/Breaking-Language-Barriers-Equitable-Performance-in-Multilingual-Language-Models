#!/bin/bash
set -exuo pipefail

qrsh -q "gpu@@lucy_$1" -l gpu=1