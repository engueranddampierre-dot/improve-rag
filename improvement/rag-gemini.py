import sys, os
import json
from pathlib import Path
import requests

def charger_rag(rag: str):
	"""Importe retrieve_maude_context depuis le RAG choisi (--rag), ou None.
	Valeurs : rag-system (defaut), maude-rag-hybrid, maude-rag-sections, none."""
	if rag in (None, 'none'):
		return None
	rag = rag.removeprefix('../')
	sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', rag))
	from rag.builder_code import retrieve_maude_context
	return retrieve_maude_context

# initialise dans __main__ selon --rag ; par defaut le baseline, comme avant
retrieve_maude_context = None

# Schema for the answer
MAIN_SCHEMA = {
	'type': 'object',
	'properties': {
		'comment': {
			'type': 'string',
			'description': 'The model reply except for the modified code'
		},
		'code': {
			'type': 'string',
			'description': 'The modified code (a multiline string)'
		},
	},
	'required': ['comment', 'code']
}

class Gemini:
	"""Connector to the Gemini API"""

	# URL for the REST API of the Google AI
	API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'

	# Response schema
	SCHEMA = {
		'responseMimeType': 'application/json',
		'responseJsonSchema': MAIN_SCHEMA,
	}

	def __init__(self, model: str):
		self.session = requests.Session()
		self.model = model
		self.session.headers.update({'x-goog-api-key': os.environ['GEMINI_API_KEY']})

	def optimize(self, code: str, lang: str):
		
		base = f'Please, simplify and improve the efficiency of the following {lang} code while preserving the semantics. Keep the original function signatures, but change the implementation as needed.'
    
		if lang == 'Maude' and retrieve_maude_context:
			context = retrieve_maude_context(code)
			# imported rag from builder_code.py (selon --rag)
			rag_block = f'\n\nThe following excerpts from the Maude manual document the constructs used. Use them as the authoritative reference for Maude syntax. Do NOT introduce notation that does not appear in these excerpts or the original code.\n\nMAUDE MANUAL EXCERPTS:\n{context}'
		else:
			rag_block = ""

		message = f'{base}{rag_block}\n```\n{code}\n```\n'

		# Ask the API
		answer = self.session.post(self.API_URL.format(model=self.model), json={'contents': [{'parts': [{'text': message}]}], 'generationConfig': self.SCHEMA})

		if answer.status_code == 200:
			x = json.loads(answer.json()['candidates'][0]['content']['parts'][0]['text'])
			print(x)
			return x

		else:
			raise ValueError(f'API error: {answer.content}')

class Gemma:
	"""Connector to the Gemma API"""

	# URL for the REST API of the Google AI
	API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'

	def __init__(self, model: str):
		self.session = requests.Session()
		self.model = model
		self.session.headers.update({'x-goog-api-key': os.environ['GEMINI_API_KEY']})

	def _separate_code(self, text: str):
		"""Separate code from explanation"""

		buckets = ([], [])
		current = 0

		# Collect lines
		for line in text.split('\n'):
			if line.startswith('```'):
				current = 1 - current
			else:
				buckets[current].append(line)

		# Join lines
		return {'comment': '\n'.join(buckets[0]), 'code': '\n'.join(buckets[1])}

	def optimize(self, code: str, lang: str, raw=False):
	
		base = f'Please, simplify and improve the efficiency of the following {lang} code while preserving the semantics. Keep the original function signatures, but change the implementation as needed.'
		if lang == 'Maude' and retrieve_maude_context:
			context = retrieve_maude_context(code)
			rag_block = f'\n\nThe following excerpts from the Maude manual document the constructs used. Use them as the authoritative reference for Maude syntax. Do NOT introduce notation that does not appear in these excerpts or the original code.\n\nMAUDE MANUAL EXCERPTS:\n{context}'
		else:
			rag_block = ""
		message = f'{base}{rag_block}\n```\n{code}\n```\n'

		# Ask the API
		answer = self.session.post(self.API_URL.format(model=self.model),
		                           json={'contents': [{'parts': [{'text': message}]}]})

		if answer.status_code == 200:
			parts = answer.json()['candidates'][0]['content']['parts']
			text = next(p['text'] for p in reversed(parts) if not p.get('thought'))

			return text if raw else self._separate_code(text)

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


def line_comment(suffix: str):
	"""Start of line comment"""

	match suffix:
		case '.maude':
			return '***\t'

		case '.py':
			return '#\t'

		case _:
			return '//\t'


def get_model_handler(name: str):
	"""Get the model handler"""

	if name.startswith('gemini'):
		return Gemini
	elif name.startswith('gemma'):
		return Gemma
	elif name.startswith('devstral'):
		return Ollama


def write_response(response, out, source, model):
	"""Write the response to the given output file"""

	# Inicio de comentario
	comment_mark = line_comment(source.suffix)

	out.write(f'{comment_mark.rstrip()}\n{comment_mark}<comment from="{model}">\n')

	for line in response['comment'].split('\n'):
		out.write(f'{comment_mark}{line}'.rstrip() + '\n')

	out.write(f'{comment_mark}</comment>\n{comment_mark.rstrip()}\n\n')

	out.write(response['code'])


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description='Interface to LLM')
	parser.add_argument('input', help='Input file', type=Path)
	parser.add_argument('-o', help='Output JSON file', type=Path)
	parser.add_argument('--model', '-m', help='Model to use', default='gemini-3-flash-preview')
	parser.add_argument('--rag', help='RAG backend: rag-system, maude-rag-hybrid, maude-rag-sections or none',
	                    default='rag-system')

	args = parser.parse_args()

	# Selectionne le RAG demande (les trois exposent retrieve_maude_context)
	retrieve_maude_context = charger_rag(args.rag)

	# Get the handler class for the model
	model_handler = get_model_handler(args.model)

	if model_handler is None:
		print(f'Unknown model {args.model}.')
		sys.exit(1)

	model = model_handler(args.model)

	# Recognizes the programming language
	if lang := language(args.input.suffix):
		response = model.optimize(args.input.read_text(), lang)

		# Output file
		output = args.o

		if output is None:
			output = args.input.with_stem(f'{args.input.stem}-gemini')

		elif output.is_dir():
			output = output / args.input.name

		# Write to the output file
		with open(output, 'w') as out:
			write_response(response, out, args.input, args.model)

	else:
		print(f'Unsupported language or extension {lang}.')
