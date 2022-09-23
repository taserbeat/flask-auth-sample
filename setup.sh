#!/bin/bash

readonly SCRIPT_EXECUTED_DIR=$(pwd)

readonly SCRIPT_DIR=$(
    cd $(dirname $0)
    pwd
)

cd "${SCRIPT_DIR}"

if [ -e ./.venv/ ]; then
    rm -r ./.venv/
fi

export PIPENV_VENV_IN_PROJECT=true

if [ -e ./Pipfile.lock ]; then
    echo "Pipfile.lock is found."
    echo "Running 'pipenv sync --dev'"
    pipenv sync --dev
elif [ -e ./Pipfile ]; then
    echo "Pipfile is found."
    echo "Running 'pipenv install --dev'"
    pipenv install --dev
else
    echo "Pipfile/Pipfile.lock are not found."
    echo "Try to create pipenv project by manual."
    cd "${SCRIPT_EXECUTED_DIR}"
    exit 1
fi

cd ${SCRIPT_EXECUTED_DIR}
