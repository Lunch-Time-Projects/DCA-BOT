#!/usr/bin/env bash

# Remove existing build folder
echo "Remove existing build folder..."
if [ -d build ]; then
  rm -rf build
fi

# Recreate build directory
echo "Recreate build directory..."
mkdir -p build/function/ build/layer/

# Copy source files
echo "Copy source files..."
cp -r src/ build/function/

# Activate virtualenv
echo "Activate virtualenv..."
python3 -m venv env
. env/bin/activate

# Pack python libraries
echo "Pack python libraries..."
pip3 install -r src/requirements.txt -t build/layer/python

# Remove pycache in build directory
# https://stackoverflow.com/questions/28991015/python3-project-remove-pycache-folders-and-pyc-files
echo "Remove pycache in build directory..."
find build -type f | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm

echo "Done!"