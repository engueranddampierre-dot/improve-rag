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
INPUTS_ROOT = Path('inputs/gemini-3-flash')
# Model
MODEL = 'gemini-3-flash'
# Delay between requests
DELAY = 30
# Limit the generation at most the given number of times
QUOTA = 20

# Remaining quota
remaining = QUOTA

for file in ORIGINAL_ROOT.rglob('*'):
	# Ignore directories and JSON files
	if not file.is_file() or file.suffix == '.json':
		continue

	# Generated inputs path translation path
	input_file = INPUTS_ROOT / file.relative_to(ORIGINAL_ROOT).with_suffix('.json')

	# Generate it only if not already there
	if not input_file.exists():
		print('⏵', input_file)
		subprocess.run((sys.executable, 'make_test.py', file, '-m', MODEL))

		# Check if we have reached the quota
		remaining -= 1

		if remaining == 0:
			print('Stopped because the quota has been reached')
			break

		time.sleep(DELAY)
