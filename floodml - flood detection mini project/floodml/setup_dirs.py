#!/usr/bin/env python3
import os
import sys

dirs = ['data/archive', 'data/input', 'data/processed']

for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f'OK: {d}')

print('\nAll directories created successfully!')
