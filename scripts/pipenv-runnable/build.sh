#!/usr/bin/env bash
set -e

case "$1" in
    package)
        pipenv requirements > requirements.txt
        python -m build
        ;;

    *)
        echo "Usage: $0 package"
        exit 1
        ;;
esac
