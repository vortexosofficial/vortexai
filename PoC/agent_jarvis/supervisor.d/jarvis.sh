#!/bin/bash

set -eux

CURRENT_SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_ROOT_DIR=$( dirname -- "${CURRENT_SCRIPT_DIR}" )
cd "${PROJECT_ROOT_DIR}"

echo "${PROJECT_ROOT_DIR}"

# https://stackoverflow.com/questions/61915607/commandnotfounderror-your-shell-has-not-been-properly-configured-to-use-conda
source /root/miniconda3/etc/profile.d/conda.sh

conda activate jarvis
exec python -m jarvis.main
