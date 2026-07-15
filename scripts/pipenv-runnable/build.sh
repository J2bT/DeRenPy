#!/usr/bin/env bash
set -e

case "$1" in
    package)
        pipenv requirements > requirements.txt
        python -m build
        ;;

    executable)
        echo "Not implemented!"
        exit 1
        ;;

    *)
        echo "Usage: pipenv run build {package|executable}"
        exit 1
        ;;
esac
