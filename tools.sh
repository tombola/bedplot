#!/bin/bash

# This file sort of outlines cli workflow

# Using uv run will 'sync' the environment automatically
alias dj="uv run django-admin"
alias start="open http://bedplot.local:8000 && dj runserver"
# examples
# dj runserver && open http://bedplot.local:8000/
# dj migrate
# dj makemigrations
# dj createsuperuser