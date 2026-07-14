#!/usr/bin/env bash

pushd .. > /dev/null

export PIPENV_VENV_IN_PROJECT=1
pipenv sync --dev

# shellcheck disable=SC2164
popd > /dev/null
