#!/bin/bash -e
cd "$(dirname "$0")"
virtualenv temp_env -q -p python3
source temp_env/bin/activate
echo "locking production requirements ..."
pip install --upgrade -q -r production-to-freeze.txt
pip freeze > production.txt
echo "locking develop requirements ..."
pip install --upgrade -q -r develop-to-freeze.txt
pip freeze > develop.txt
echo "cleaning up..."
deactivate
rm -rf temp_env