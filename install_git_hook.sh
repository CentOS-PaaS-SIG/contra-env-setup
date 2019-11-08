#!/usr/bin/env bash

# Copyright Red Hat, Inc

###
#
# Please ensure that you list any hooks you're installing in the echo
# statement below and indicate what function it provides.
#
##

echo """
This will install the following git hooks:
- pre-commit: This hook will automatically regenerate documentation
"""
find .git/hooks -type l -exec rm {} \; && find .githooks -type f -exec ln -sf ../../{} .git/hooks/ \;