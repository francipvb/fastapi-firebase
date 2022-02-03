#!/usr/bin/bash

poetry config repositories.destrepo "${REPO_URL}"
poetry config pypi-token.destrepo "${PYPI_TOKEN}"

poetry publish \
    --build \
    --repository "destrepo"
