#!/usr/bin/env python
"""
Extract the builds used in Github CI, so that we can run them locally
"""

import os
import sys
from pathlib import Path
import yaml

# Auto-detect repository root
script_dir = Path(__file__).parent.absolute()
REPO_ROOT = None

# Walk up the directory tree to find repository root
current_dir = script_dir
while current_dir != current_dir.parent:
    if (current_dir / 'platformio.ini').exists() and (current_dir / '.git').exists():
        REPO_ROOT = current_dir
        break
    current_dir = current_dir.parent

if REPO_ROOT is None:
    print("ERROR: Could not detect repository root or not in a Marlin repository", file=sys.stderr)
    print("This script must be run from within the CR6Community-Marlin repository", file=sys.stderr)
    sys.exit(1)

# Change to repository root for consistent path handling
os.chdir(REPO_ROOT)

workflow_file = REPO_ROOT / '.github' / 'workflows' / 'test-builds.yml'
if not workflow_file.exists():
    print(f"ERROR: Workflow file not found: {workflow_file}", file=sys.stderr)
    sys.exit(1)

with open(workflow_file, encoding='utf-8') as f:
    github_configuration = yaml.safe_load(f)
test_platforms = github_configuration\
	['jobs']['test_builds']['strategy']['matrix']['test-platform']
print(' '.join(test_platforms))
