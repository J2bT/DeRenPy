#!/usr/bin/env bash

pushd .. > /dev/null

pipenv requirements > requirements.txt
pipenv run python -m build

# shellcheck disable=SC2164
popd > /dev/null
