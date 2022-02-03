#!/usr/bin/bash

poetry install $(test "$NO_DEV" = "true" && echo "--no-dev")
