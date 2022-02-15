#!/usr/bin/bash

poetry config repositories.destrepo "${REPO_URL}"

poetry publish \
    --build \
    --repository="destrepo" \
    --username="__token__" \
    --password="${PYPI_TOKEN}"
