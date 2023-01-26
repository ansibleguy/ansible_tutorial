#!/bin/bash

set -e

# allows you to run the script from any directory as it changes into the directory one level up
cd "$(dirname "$0")/.."

echo ''
echo 'LINTING Ansible'
echo ''
ansible-lint -c .ansible-lint.yml

echo ''
echo 'LINTING Yaml'
echo ''
yamllint .

echo ''
echo 'LINTING Python'
echo ''

pylint --recursive=y .
