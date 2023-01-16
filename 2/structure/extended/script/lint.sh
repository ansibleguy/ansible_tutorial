#!/bin/bash

set -e

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

pylint --recursive=y
