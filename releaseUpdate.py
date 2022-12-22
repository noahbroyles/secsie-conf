#!/usr/bin/env python3

import subprocess

# Remove the old build directories, if any
subprocess.call(['rm', '-fr', 'build/', 'dist/'])

# Run setup.py
subprocess.call(['python3', 'setup.py', 'sdist', 'bdist_wheel'])

# Use Twine to upload the output to PyPi
subprocess.call(['twine', 'upload', 'dist/*'])
