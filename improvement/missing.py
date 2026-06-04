#
# Complete the missing translations
#

from pathlib import Path
import subprocess
import sys
import time

# Root of the original source code
ORIGINAL_ROOT = Path('tests/original')
# Source of the model translations
MODEL_ROOT = Path('tests/gemini-3-flash')
# Model
MODEL = 'gemini-3-flash-preview'
# Delay between requests
DELAY = 30
# Limit by the quota
QUOTA = 20

# Remaining quota
remaining = QUOTA

for file in ORIGINAL_ROOT.rglob('*'):
	# Ignore directories and JSON files
	if not file.is_file() or file.suffix == '.json':
		continue

	# Model translation path
	model_file = MODEL_ROOT / file.relative_to(ORIGINAL_ROOT)

	# Generate it only if not already there
	if not model_file.exists():
		print('⏵', model_file)
		subprocess.run((sys.executable, 'improve.py', file, '-o', model_file.parent, '-m', MODEL))

		remaining -= 1

		if remaining == 0:
			print('Stopped because the quota has been reached.')
			break

		time.sleep(DELAY)
