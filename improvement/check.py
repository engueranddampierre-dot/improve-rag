#
# Check that given program run
#

from collections import namedtuple
import json
import multiprocessing as mp
from multiprocessing.connection import wait
import os
from pathlib import Path
import random
import re
import shutil
import signal
import statistics
import subprocess
import sys
import tempfile
import tomllib
import time
from typing import TextIO


class ValidationResult:
	"""Result of a validation test"""

	BUILD_ERROR = 0
	RUN_ERROR = 1
	FAILED = 2
	OK = 3

	def __init__(self, status = 3, msg=None):
		self.status = status
		self.msg = msg

	def __repr__(self):
		return f'ValidationResult({self.status!r}, {self.msg!r})'

	@property
	def ok(self):
		return self.status == self.OK

	@classmethod
	def from_run(cls, proc: subprocess.CompletedProcess):
		"""Generate a result from a process output"""

		if proc.returncode < 0:
			return cls(cls.RUN_ERROR, f'terminated with signal {signal.Signals(-proc.returncode).name}: {proc.stdout.decode()}')

		if proc.returncode > 0:
			return cls(cls.FAILED, proc.stdout.decode())

		return cls(cls.OK)

	@classmethod
	def from_compiler_run(cls, proc: subprocess.CompletedProcess):
		"""Generate a result from a process output"""

		if proc.returncode != 0:
			return cls(cls.BUILD_ERROR, proc.stdout.decode())

		return cls(cls.OK)


class CppDriver:
	"""Compiler connector for C++"""

	CXX = os.environ.get('CXX', 'c++')
	LANG = 'cpp'

	@classmethod
	def available(cls):
		"""Check whether the compiler is available"""

		return shutil.which(cls.CXX) is not None

	def build(self, source, root, tests=False):
		"""Build the given source just to check validity"""

		# Generate an executable or only an object file
		build_type = '-oa.out' if tests else '-c'

		ret = subprocess.run((self.CXX, '-std=c++20', '-fdiagnostics-color=always', build_type, source),
		                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=root)

		return ValidationResult.from_compiler_run(ret)

	def _wrap_namespace(self, source: Path, dest: TextIO, name: str, extra: dict):
		"""Wrap source in a namespace name into dest"""

		includes, body = [], []

		with source.open() as fin:
			# Separate includes from the main content
			for line in fin:
				if line.lstrip().startswith('#'):
					includes.append(line)
				else:
					body.append(line)

		# Write includes
		for line in includes:
			dest.write(line)

		# Write body in a namespace
		dest.write(f'\nnamespace {name} {{\n')


		for line in body:
			dest.write(line)

		# Include additional code after the original one
		if include := extra.get('include'):
			dest.write(include)

		dest.write('\n}\n')

	def translate_input(self, data):
		"""Convert input data for test case generation"""

		match data:
			case bool():
				return 'true' if data else 'false'

			case list():
				args = tuple(self.translate_input(arg) for arg in data)
				return f'{{{", ".join(args)}}}'

		return str(data)

	def diff_test(self, apath, bpath, tests, extra, root, timeout=None):
		"""Compile a program for doing differential testing"""

		# Deal with each version separately
		source = root / 'main.cpp'

		with source.open('w') as out:
			if global_include := extra.get('global_include'):
				out.write(global_include)

			for version, path in (('a', apath), ('b', bpath)):
				# Wrap the corresponding sources in a namespace
				self._wrap_namespace(path, out, version, extra)


			# Code to fix the combination of both implementations
			if diff_fix := extra.get('diff_fix'):
				out.write(diff_fix)

			# Main function that run the tests
			out.write('\n#include <iostream>\n\nint main() {\n')

			for test in tests:
				safe_expr = test.expr.replace('\n', '').replace('"', r'\"')
				out.write(f'if ([](){{ using namespace a; return {test.expr}; }}() != [](){{ using namespace b; return {test.expr}; }}()) {{\n'
					  f'\tstd::cout << "Test {test.name} failed with {safe_expr}.\\n";\n\treturn 1;\n'
					  '}\n')

			out.write('\n\treturn 0;\n}\n')

		# Try to compile it
		# print(os.getpid())
		# input()
		result = self.build(source, root, tests=True)

		if not result.ok:
			return result

		# Run the program itself
		ret = subprocess.run(('./a.out',), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
		                     cwd=root, timeout=timeout)
		return ValidationResult.from_run(ret)

	def benchmark(self, path, tests, extra, root):
		"""Compile a program for running the benchmarks"""

		source = root / 'main.cpp'

		with source.open('w') as out:
			# Include additional code for the tests
			if global_include := extra.get('global_include'):
				out.write(global_include)

			out.write(path.read_text())

			# Include additional code for the tests
			if include := extra.get('include'):
				out.write(include)

			# Main function that run the tests
			out.write('\n#include <iostream>\n\nint main() {\n')

			for test in tests:
				out.write(f'{test.expr};\n')

			out.write('\n\treturn 0;\n}\n')

		# Try to compile it
		result = self.build(source, root, tests=True)

		if not result.ok:
			return False, result

		return True, (root / 'a.out',)


class RustDriver:
	"""Compiler connector for Rust"""

	LANG = 'rust'
	DECL_REGEX = re.compile(r'(?:fn [^\(]+\()|(?:enum [^\s]+ {)')
	DECL_TEXT = 'pub {}'

	@staticmethod
	def available():
		"""Check whether the Rust compiler is available"""

		return shutil.which('rustc') is not None

	def build(self, source, root, tests=False):
		"""Build the given source just to check validity"""

		build_type = '--test' if tests else '--crate-type=lib'
		ret = subprocess.run(('rustc', '--color=always', build_type, source),
		                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=root)

		return ValidationResult.from_compiler_run(ret)

	def _wrap_namespace(self, source: Path, dest: TextIO, name: str):
		"""Wrap source in a namespace name into dest"""

		with source.open() as fin:
			# Separate includes from the main content
			dest.write(f'mod {name} {{\n')
			for line in fin:
				dest.write(self.DECL_REGEX.sub(lambda v: self.DECL_TEXT.format(v.group(0)), line))

			dest.write('}')

		dest.write('\n')

	def translate_input(self, data):
		"""Convert input data for test generation"""

		match data:
			case bool():
				return 'true' if data else 'false'

			case list():
				args = tuple(self.translate_input(arg) for arg in data)
				return f'&vec![{", ".join(args)}]'

		return str(data)

	def diff_test(self, apath, bpath, tests, extra, root, timeout=None):
		"""Compile a program for doing differential testing"""

		source = root / 'main.rs'

		with source.open('w') as out:
			for version, path in (('a', apath), ('b', bpath)):
				# Wrap the corresponding sources in a namespace
				self._wrap_namespace(path, out, version)

			# Module with the tests
			out.write('#[cfg(test)]\nmod tests {\n\n')

			for test in tests:
				out.write(f'\t#[test]\n\tfn test_{test.name}() {{\n\t\tassert_eq!(')
				out.write(f'format!("{{:?}}", {{use a::*; {test.expr}}}), '
				          f'format!("{{:?}}", {{use b::*; {test.expr}}}), "{test.expr}");\n}}\n')

			out.write('\n}\n')

		# Try to compile it
		ret = subprocess.run(('rustc', '--color=always', '--test', source),
		                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=root)

		if ret.returncode != 0:
			return ValidationResult.from_compiler_run(ret)

		# Run the program itself
		ret = subprocess.run(('./main',), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
		                     cwd=root, timeout=timeout)
		return ValidationResult.from_run(ret)

	def benchmark(self, path, tests, extra, root):
		"""Prepare a given file of benchmarks"""

		source = root / 'main.rs'

		with source.open('w') as out:
			out.write(path.read_text())

			# Main function that run the tests
			out.write('\nfn main() {\n')

			for test in tests:
				out.write(f'{test.expr};\n')

			out.write('\n}\n')

		# Try to compile it
		result = self.build(source, root, tests=True)

		if not result.ok:
			return False, result

		return True, (root / 'main',)


class PythonDriver:
	"""Compiler connector for Python"""

	LANG = 'py'

	TEST_BODY = '''\
	def test_{name}(self):
		def lhs():
			import a
			return eval("{expr}", a.__dict__)
		def rhs():
			import b
			return eval("{expr}", b.__dict__)
		return self.assertEqual(repr(lhs()), repr(rhs()))

'''

	@staticmethod
	def available():
		return shutil.which('python') is not None

	def build(self, source, root, tests=False):
		output = subprocess.PIPE
		# Copy file to avoid writing the output outside the root
		shutil.copy(source, root)
		ret = subprocess.run(('python', '-m', 'py_compile', source.name), stdout=output, stderr=output, cwd=root)

		return ValidationResult.from_compiler_run(ret)

	@staticmethod
	def translate_input(input):
		"""Translate input for test case generation"""

		return repr(input)

	def diff_test(self, apath, bpath, tests, extra, root, timeout=None):

		source = root / 'main.py'

		# Copy the versions
		shutil.copy(apath, root / 'a.py')
		shutil.copy(bpath, root / 'b.py')

		# Generate the test to compare them
		with source.open('w') as out:
			out.write('import a\nimport b\nimport unittest\n')

			out.write(f'class TestSuite(unittest.TestCase):\n')
			for test in tests:
				out.write(self.TEST_BODY.format(name=test.name, expr=test.expr))

			out.write('import sys\nsys.setrecursionlimit(100000)\nunittest.main()')

		# Run the program itself
		ret = subprocess.run((sys.executable, source), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
		                     cwd=root, timeout=timeout)
		return ValidationResult.from_run(ret)

	def benchmark(self, path, tests, extra, root):
		"""Prepare a given file of benchmarks"""

		source = root / 'main.py'

		with source.open('w') as out:
			out.write(path.read_text())

			# Main function that run the tests
			for test in tests:
				out.write(f'{test}\n')

		return True, (sys.executable, source)


class MaudeRunner:
	"""Class to run Maude code in a separate process"""

	def __init__(self, path):
		self.path = path
		child_pipe, self.parent_pipe = mp.Pipe()
		self.proc = mp.Process(target=self._eval_main, args=(str(path.absolute()), child_pipe))

	def start(self):
		self.proc.start()

	@staticmethod
	def _eval_main(fname, pipe):
		"""Main function to evaluate output"""

		import maude
		maude.init()
		maude.load(fname)
		m = maude.getCurrentModule()

		if m is None:
			pipe.send(None)
			return

		try:
			while term := pipe.recv():
				t = m.parseTerm(term)
				if t is None:
					pipe.send(None)
					return
				else:
					t.reduce()
					pipe.send(t.prettyPrint(0))

		except EOFError:
			pass

	def send(self, term):
		self.parent_pipe.send(term)

	def recv(self, timeout=None):
		ready = wait((self.parent_pipe, self.proc.sentinel), timeout=timeout)

		if not ready:
			return False, f'timed out for {self.path}'

		if self.proc.sentinel in ready:
			return False, f'process failed with exit code {self.proc.exitcode} for {self.path}'

		try:
			return True, self.parent_pipe.recv()

		except EOFError:
			return False, f'no answer recieved for {self.path}'


class MaudeDriver:
	"""Compiler connector for Maude"""

	LANG = 'maude'

	@staticmethod
	def available():
		"""Check whether Maude is available"""

		return shutil.which('maude') is not None

	def build(self, source, root, tests=False):
		output = subprocess.PIPE
		ret = subprocess.run(('maude', source.absolute()), input=b'\nquit\n', stdout=output, stderr=output, cwd=root)

		if ret.returncode != 0 or b'Warning: ' in ret.stderr:
			return ValidationResult(ValidationResult.BUILD_ERROR, ret.stderr.decode())

		return ValidationResult()

	def translate_input(self, data):
		"""Convert input data for test case generation"""

		match data:
			case bool():
				return 'true' if data else 'false'

			case list():
				args = tuple(self.translate_input(arg) for arg in data)
				return ' '.join(args)

		return str(data)

	def diff_test(self, apath, bpath, tests, extra, root, timeout=None):

		# TODO: take timeout into account

		# We do the evaluation here because merging Maude file is more complex
		runners = (MaudeRunner(apath), MaudeRunner(bpath))

		for runner in runners:
			runner.start()

		# What to do
		output = ValidationResult()
		exit = False

		for test in tests:
			# Send the term to be reduced by the other processes
			for runner in runners:
				runner.send(test.expr)

			# Wait for the answer
			answers = [None, None]

			for k, runner in enumerate(runners):
				ok, answers[k] = runner.recv(timeout=timeout)

				if not ok:
					output = ValidationResult(ValidationResult.RUN_ERROR, answers[k])
					exit = True
					break

				if answers[k] is None:
					output = ValidationResult(ValidationResult.BUILD_ERROR, 'parsing error (most likely)')
					exit = True
					break

			if exit: break

			if answers[0] != answers[1]:
				output = ValidationResult(ValidationResult.FAILED, f'failed test case "{test.name}" ("{test.expr}") with outputs "{answers[0]}" and "{answers[1]}"')
				exit = True
				break

		if not exit:
			for runner in runners:
				runner.send(None)

		return output

	def benchmark(self, path, tests, extra, root):
		"""Prepare a given file of benchmarks"""

		source = root / 'main.maude'

		with source.open('w') as out:
			out.write(path.read_text())

			# Main function that run the tests
			for test in tests:
				out.write(f'red {test} .\n')

			out.write('\nquit\n')

		return True, ('maude', source)


class BenchmarkResult:
	"""Result of a benchmark"""

	def __init__(self, times: list[float], memories: list[int]):
		self.times = times
		self.memories = memories

		self.time_mean = statistics.mean(times)
		self.memory_mean = statistics.mean(memories)

	def dump(self):
		return {
			'raw_time': self.times,
			'raw_memory': self.memories,
			'time': self.time_mean,
			'memory': self.memory_mean,
		}


class BenchExec:
	"""Benchmarker with benchexec"""

	def benchmark(self, args, root, repeats=10):
		"""Benchmark a given command"""

		time = []
		memory = []

		for _ in range(repeats):
			# Run using BenchExec's runexec
			ret = subprocess.run(('runexec', '--read-only-dir=/', *args),
					     stdout=subprocess.PIPE,
					     stderr=subprocess.PIPE, cwd=root)

			if ret.returncode != 0:
				print(f'❌ Failed to run {args[0]}: {ret.stderr.decode()}')
				return None, None

			data = dict(line.split('=') for line in ret.stdout.decode().split('\n') if line.strip())

			time.append(float(data['cputime'][:-1]))
			memory.append(int(data['memory'][:-1]))

		return BenchmarkResult(time, memory)


# Associates file extensions with drivers

COMPILERS = {
	'.rs': RustDriver(),
	'.py': PythonDriver(),
	'.cpp': CppDriver(),
	'.maude': MaudeDriver(),
}

# Remove unsupported compilers
COMPILERS = {ext: comp for ext, comp in COMPILERS.items() if comp.available()}


def get_benchmarker(name: str):
	"""Get a benchmarking method"""

	match name:
		case 'benchexec':
			return BenchExec()


def check_compile(args):
	"""Check whether the given files compile"""

	count, total = 0, 0
	results = {}

	# Use a temporary directory not to mesh files up
	with tempfile.TemporaryDirectory() as tmpdir:
		# Process each supported file (by a compiler) from the input
		for file in args.input:
			if (handler := COMPILERS.get(file.suffix)):
				result = handler.build(file.absolute(), tmpdir)
				print('✅' if result.ok else '❌', file)

				# Count how many files compile
				if result.ok:
					count += 1

				# Show error output, in that case
				elif args.v:
					print(result.msg)

				results[str(file)] = result.ok
				total += 1

	print(f'{count}/{total} files compile')

	# Save the results for later
	with open(args.o, 'w') as out:
		json.dump(results, out)

# Type of test inputs
TestInput = namedtuple('TestInput', ('expr', 'name'))

def make_tests(spec, driver):
	"""Make tests for a given specification"""

	tests = []

	# Global example cases given as a string
	for k, example in enumerate(spec.get('examples', ())):
		tests.append(TestInput(example, f'example_{k}'))

	for fn, data in spec.items():
		# extra has special meaning
		if fn == 'extra':
			continue

		# Include the example in the cases
		for k, example in enumerate(data.get('examples', ())):
			args = ', '.join(map(driver.translate_input, example))
			tests.append(TestInput(f'{fn}({args})', f'{fn}_example_{k}'))

		if signature := data.get('signature'):
			# Number of tests to generate
			count = data.get('count', 25)

			for k in range(count):
				case = []

				for ty in signature:
					# The general form is {type: ty} but we admit simply ty
					if isinstance(ty, str):
						ty = {'type': ty}

					match ty['type']:
						case 'nat':
							case.append(random.randint(ty.get('min', 0), ty.get('max', 2 ** 31)))

						case 'int':
							case.append(random.randint(ty.get('min', - 2 ** 30), ty.get('max', 2 ** 30)))

						case 'bool':
							case.append(random.choice([True, False]))

						case 'float':
							case.append(random.uniform(ty.get('min', -1e6), ty.get('max', 1e6)))

						case _:
							raise ValueError(f'unknown signature type: {ty["type"]}')

				args = ', '.join(map(driver.translate_input, case))
				tests.append(TestInput(f'{fn}({args})', f'{fn}_random_{k}'))

	return tests


def get_tests(args):
	"""Get the tests to be evaluated"""

	tests_root = Path('tests')
	original_name = 'original'
	inputs_root = Path('inputs/spec')

	# Group inputs regardless of its model
	groups = {}

	for file in args.input:
		if not file.is_relative_to(tests_root):
			print(f'⚠️ Skipping file outside the test root {file}')
			continue

		if file.is_dir():
			print(f'⚠️ Skipping directory {file.name}')
			continue

		model_path = file.parents[-3]

		# Silently ignore the original files
		if model_path.name == original_name:
			continue

		groups.setdefault(file.relative_to(model_path), {})[model_path.name] = file

	for name, files in groups.items():
		# Load test specification
		test_spec = inputs_root / name.with_suffix('.toml')

		# Find a suitable compiler
		if (handler := COMPILERS.get(name.suffix)) is None:
			print(f'⚠️ Skipping unknown file extension {name.name}')
			continue

		# Read tests from the specification (random and manual)
		if test_spec.is_file():
			with test_spec.open('rb') as tomlin:
				spec = tomllib.load(tomlin)

			# Make tests for the specification
			tests = make_tests(spec, handler)
			extra = spec.get('extra', {})

		else:
			tests = []
			extra = {}

		# Collect test from the AI models
		for subdir in inputs_root.parent.iterdir():
			if not subdir.is_dir() or subdir.name == 'spec':
				continue

			# Check whether there are cases generated by this model
			ai_cases = subdir / name.with_suffix('.json')

			if ai_cases.is_file():
				with open(ai_cases) as cin:
					ai_data = json.load(cin)

				for k, ai_test in enumerate(ai_data.get('tests', ())):
					tests.append(TestInput(ai_test, f'aitest_{k}'))

		if not tests:
			print(f'⚠️ Skipping file without test specified {name}')
			continue

		# Original file
		original = tests_root / original_name / name

		files['original'] = original

		yield name, files, handler, tests, extra


def diff_test(args):
	"""Apply differential testing on a test case"""

	count, total = 0, 0
	results = {}

	# Limit testing to files that compile
	ffilter = None

	if args.filter:
		with open(args.filter) as jin:
			ffilter = {k for k, v in json.load(jin).items() if v}

	ICONS = {
		ValidationResult.OK: '✅',
		ValidationResult.FAILED: '❌',
		ValidationResult.RUN_ERROR: '💥',
		ValidationResult.BUILD_ERROR: '😞',
	}

	for name, files, handler, tests, extra in get_tests(args):
		original = files['original']

		print(f'{name} ({len(tests)} cases)')

		for model, modified in files.items():
			# We do not check with ourselves
			if model == 'original' or (ffilter is not None and str(modified) not in ffilter):
				continue

			# Use differential testing with the original file
			with tempfile.TemporaryDirectory() as tmpdir:
				print(f'  {model}', end='', flush=True)

				try:
					start = time.perf_counter()
					result = handler.diff_test(original, modified, tests, extra, Path(tmpdir), timeout=args.timeout)
					end = time.perf_counter()

					print(f'\r  {ICONS[result.status]} {model} \x1b[33m{end - start:.4}\x1b[0m')

				except subprocess.TimeoutExpired:
					print(f'\r  ⏰ {model}')
					result = ValidationResult(ValidationResult.FAILED, 'timed out')

			if result.ok:
				count += 1
			elif args.v:
				print(' ', result.msg)

			results.setdefault(str(name), {})[model] = dict(ok=result.ok, status=result.status, msg=result.msg)

			total += 1

	print(f'{count}/{total} tests passed')

	# Save the results
	with open(args.o, 'w') as out:
		json.dump(results, out)


def benchmark(args):
	"""Benchmark tests"""

	results = {}
	benchmarker = get_benchmarker(args.tool)

	# Limit testing to files that are equivalent
	ffilter = {}

	if args.filter:
		with open(args.filter) as jin:
			ffilter = {k: {v for v, info in vs.items() if info['ok']} for k, vs in json.load(jin).items()}

	for name, files, handler, tests, extra in get_tests(args):
		data = {}

		# Check the filter (first part)
		if not (name_filter := ffilter.get(str(name))):
			print(f'⚠️ Skipping {name} because there are no equivalent translations')
			continue

		print(name)

		# Benchmark the original file
		for model, file in files.items():
			# Check the filter (model)
			if model != 'original' and model not in name_filter:
				continue

			with tempfile.TemporaryDirectory(dir='.') as tmpdir:
				ok, msg = handler.benchmark(file, tests, extra, Path(tmpdir))

				if not ok:
					if args.v:
						print(f'❌ Failed to compile {file}: {msg.msg}')
					else:
						print(f'❌ Failed to compile {file}.')

					continue

				result = benchmarker.benchmark(msg, tmpdir, repeats=args.repeats)

				if result is None:
					continue

				data[model] = result

		if len(data) <= 1 or 'original' not in data:
			print(f'⚠️ Skipping {name} by incomplete benchmark')
			continue

		odata = data['original']
		results[str(name)] = {'original': odata.dump()}

		for model, mdata in data.items():
			if model == 'original':
				continue

			speedup = odata.time_mean / mdata.time_mean
			memoryred = odata.memory_mean / mdata.memory_mean

			print(f' {model}')
			print(f'  Time    | {odata.time_mean:20} | {mdata.time_mean:20} | {speedup:20}')
			print(f'  Memory  | {odata.memory_mean:20} | {mdata.memory_mean:20} | {memoryred:20}')

			results[str(name)][model] = mdata.dump() | {'speedup': speedup, 'memorydown': memoryred}

	with open(args.o, 'w') as out:
		json.dump(results, out)


def main():
	import argparse

	parser = argparse.ArgumentParser(description='Check modified programs')
	parser.add_argument('-v', help='Enable verbose output', action='store_true')
	parser.set_defaults(cb=None)
	subp = parser.add_subparsers()

	# Check whether the given files compile
	tmp = subp.add_parser('compile', help='Check whether the given programs compile')
	tmp.add_argument('input', help='Programs to check', nargs='+', type=Path)
	tmp.add_argument('-o', help='Path for the JSON output', type=Path, default=Path('results-compile.json'))
	tmp.set_defaults(cb=check_compile)

	tmp = subp.add_parser('diff', help='Apply differential testing')
	tmp.add_argument('input', help='Examples to check', nargs='+', type=Path)
	tmp.add_argument('--filter', '-f', help='Only use file a successful compilation as indicated by the given JSON file', type=Path)
	tmp.add_argument('--timeout', '-t', help='Timeout for each single execution (of all tests, in seconds)', type=int, default=240)
	tmp.add_argument('-o', help='Path for the JSON output', type=Path, default=Path('results-diff.json'))
	tmp.set_defaults(cb=diff_test)

	tmp = subp.add_parser('bench', help='Benchmark modified implementations')
	tmp.add_argument('input', help='Examples to check', nargs='+', type=Path)
	tmp.add_argument('--filter', '-f', help='Only use file a successful equivalence testing as indicated by the given JSON file', type=Path)
	tmp.add_argument('--repeats', '-r', help='How many times the execution is repeated', type=int, default=3)
	tmp.add_argument('--timeout', '-t', help='Timeout for each single execution (of all tests, in seconds)', type=int, default=240)
	tmp.add_argument('-o', help='Path for the JSON output', type=Path, default=Path('results-bench.json'))
	tmp.add_argument('--tool', help='Tool to measure resources', choices=('benchexec',), default='benchexec')
	tmp.set_defaults(cb=benchmark)

	args = parser.parse_args()

	if args.cb:
		args.cb(args)


if __name__ == '__main__':
	main()
