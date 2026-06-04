#
# Prueba con la API de Gemini
#

import os
import json
from pathlib import Path

import requests

# Root of test files
TEST_ROOT = Path('tests/original')
# Root of test inputs
INPUT_ROOT = Path('inputs')

# Schema for the model answer
ANSWER_SCHEMA = {
	'type': 'object',
	'properties': {
		'comment': {
			'type': 'string',
			'description': 'The model reply except for the generated tests',
		},
		'tests': {
			'type': 'array',
			'description': 'Each element is a test case',
			'items': {
				'type': 'string',
				'description': 'A self-contained function-call expression in the language that invokes a function of the source code'
			}
		},
	},
	'required': ['comment', 'tests']
}


class Gemini:
	"""Connector to the Gemini API"""

	# URL for the REST API of the Gemini 3 Flash Preview model
	API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent'

	# Response schema
	SCHEMA = {
		'responseMimeType': 'application/json',
		'responseJsonSchema': ANSWER_SCHEMA,
	}

	def __init__(self):
		self.session = requests.Session()
		self.session.headers.update({'x-goog-api-key': os.environ['GEMINI_API_KEY']})

	def optimize(self, code: str, lang: str):
		"""Optimize a given code fragment"""

		# Prompt
		message = f'Please, give me a set of tests (only inputs) with high coverage for the following {lang} code.\n```\n{code}\n```\n'

		# Ask the API
		answer = self.session.post(self.API_URL, json={'contents': [{'parts': [{'text': message}]}], 'generationConfig': self.SCHEMA})

		if answer.status_code == 200:
			return json.loads(answer.json()['candidates'][0]['content']['parts'][0]['text'])

		else:
			raise ValueError(f'API error: {answer.content}')


class Ollama:
	"""Connector to Ollama"""

	# URL for the REST API
	API_URL = 'http://localhost:11434/api/chat'

	def __init__(self, model: str):
		self.session = requests.Session()
		self.model = model

	def optimize(self, code: str, lang: str, raw=False):
		"""Optimize a given code fragment"""

		# Prompt
		message = f'Please, give me a set of tests (only inputs) with high coverage for the following {lang} code.\n```\n{code}\n```\n'

		# Ask the API
		answer = self.session.post(
			self.API_URL,
			json={
				'model': self.model,
				'messages': [{'role': 'user', 'content': message}],
				'stream': False,
				'format': ANSWER_SCHEMA,
			},
		)

		if answer.status_code == 200:
			return json.loads(answer.json()['message']['content'])

		else:
			raise ValueError(f'API error: {answer.content}')


def language(suffix: str):
	"""Language for a given suffix"""

	match suffix:
		case '.cc' | '.cpp' | '.cxx':
			return 'C++'

		case '.py':
			return 'Python'

		case '.rs':
			return 'Rust'

		case '.maude':
			return 'Maude'

		case '.dfy':
			return 'Dafny'


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description='Interface to LLM for generating tests')
	parser.add_argument('input', help='Input file', type=Path)
	parser.add_argument('--model', '-m', help='Model to use', default='gemini-3-flash')
	parser.add_argument('-o', help='Output JSON file', type=Path)

	args = parser.parse_args()

	model = Gemini() if args.model == 'gemini-3-flash' else Ollama(args.model)

	# Recognizes the programming language
	if lang := language(args.input.suffix):
		response = model.optimize(args.input.read_text(), lang)

		# Output file
		output = args.o

		if not output:
			# Place the output where expected for generated test cases
			if args.input.is_relative_to(TEST_ROOT):
				output = INPUT_ROOT / args.model / args.input.relative_to(TEST_ROOT).with_suffix('.json')
				output.parent.mkdir(parents=True, exist_ok=True)
			else:
				output = Path('testcase.json')

		with open(output, 'w') as jsf:
			json.dump(response, jsf)

	else:
		print(f'Unsupported language or extension {lang}.')
