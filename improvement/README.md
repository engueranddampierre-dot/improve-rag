# Improvement of generated code by AI models

## LAUNCHING :
Create a venv from improve-rag/improvement, install requirements.txt from rag-system, start docker from qdrant
If you already have the venv, activate it 'source .venv/bin/activate' then start qdrant

The structure of this directory is as follows:

* `improve.py` is used to obtain optimized code from a supported language model (namely, `gemini-*`, `gemma-*`, and `devstral-small-2`, although it can be easily extended for others). The `GEMINI_API_KEY` environment variable should be defined to use the Google AI API.
* `check.py` is used to check whether a translated program compiles (`compile` subcommand), test whether it is equivalent (`diff`), and benchmark it (`bench`).
* `make_test.py` is used to generate test inputs for the given file with the supported models. `GEMINI_API_KEY` should be defined as well.
* `missing.py` and `missing_inputs.py` are used to generate the missing translations of the code in `tests/original`, or the missing inputs in `inputs/<model>`.

## Compile-and-repair loop

* `repair.py` runs a generate -> lint -> compile -> diff-test -> repair loop: the candidate is checked locally (linter + the `maude` Python package) and the diagnostic is fed back to the model, up to `--max-iters` times. Motivated by the rag-gemini-2.5-flash results: 4/19 failures were parse errors and 2/19 were semantic bugs, all detectable locally before accepting an answer.
  * `--rag ../rag-system | ../maude-rag-hybrid | ../maude-rag-sections | none` selects the retrieval backend (also useful to compare RAGs *inside* the loop).
  * `--example` adds the most similar program from `tests/original` as a few-shot exemplar.
  * `-m scripted:file.json` replays canned responses (offline testing).
* `linter.py` encodes the failure taxonomy observed in `tests/rag-gemini-2.5-flash` (`when` guards, non-ASCII punctuation, `--` comments, `=` inside `if_then_else_fi`, non-linear LHS patterns, undeclared variables) and auto-fixes the safe cases (Unicode punctuation).
* `maude_eval.py` is the isolated subprocess used by `repair.py` to load a module and reduce test terms.

Example:

```bash
python repair.py tests/original/maudec/maude/pow.maude -m gemini-2.5-flash --rag ../rag-system --trace trace-pow.json
```

Known issue found while building this: `inputs/spec/maudec/maude/collatz.toml` references `rlapp_Nat`/`arlapp_Nat`, which are not defined anywhere -- even the original module cannot parse those terms, so the diff stage of `check.py` can never test collatz. `repair.py` detects and skips such terms with a warning (and the new `maude_eval_rw.py` below now implements the convention).

## Comparison tooling (new files, nothing above was modified)

* `run_matrix.py` orchestrates the full comparison: files × configurations (RAG × model × with/without loop), aggregates traces into `results-matrix.json` and prints a summary table. `matrix-example.json` is a ready-to-edit config. The special model `echo` returns the original unchanged (no API call) — smoke-tests the whole pipeline for free.
* `best_of.py` is the alternative strategy to the repair loop: N candidates, each verified locally (linter + load + differential tests + properties), the fastest correct one wins (per-term reduction timings). Compare `repair.py` vs `best_of.py` at equal token budget.
* `props.py` + `inputs/props/maudec/maude/*.toml`: metamorphic property tests — algebraic identities checked inside the candidate under random substitutions (e.g. `first(h(F1,B1,F2,B2)) == F1`, `f(X,M+N) == f(X,M)*f(X,N)`, `gcd(A,B) == gcd(B,A)`). The real free-tuples non-linear-pattern bug violates `first_h` immediately, while 25 random points on a single expression could miss it.
* `maude_eval_rw.py` / `local_eval.py`: extended evaluator implementing the `rlapp_<Sort>` / `arlapp_<Sort>` convention sketched by `collatz.toml`, plus per-term timings. `arlapp` = sorted set of all one-step rewrite successors (`search =>1`) — **use this one in specs**: it is formulation-independent (verified: original collatz and an `if_then_else_fi` variant agree on all tested `arlapp` terms, while `rlapp`, i.e. `rewrite(1)`, is position-sensitive and may differ between equivalent programs). `repair.py` still uses the plain `maude_eval.py`; switching it to the extended evaluator is a one-line change left deliberately untouched.
