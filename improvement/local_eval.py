"""Client de l'evaluateur etendu maude_eval_rw.py (sous-processus isole).
Nouveau fichier : repair.py continue d'utiliser maude_eval.py sans changement.
Retourne en plus les temps de reduction par terme (pour best_of.py)."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
EVAL_TIMEOUT = 60


def evaluer_rw(code, termes, timeout=EVAL_TIMEOUT):
    """-> (loaded, results, times, stderr_chargement)"""
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "candidate.maude"
        src.write_text(code)
        tj = Path(tmp) / "termes.json"
        tj.write_text(json.dumps(termes))

        try:
            proc = subprocess.run(
                (sys.executable, str(HERE / "maude_eval_rw.py"), str(src), str(tj)),
                capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return False, {}, {}, "timeout : la reduction ne termine pas"

        stderr_load, _, _ = proc.stderr.partition("===TERMES===")
        stderr_load = stderr_load.strip()

        if proc.returncode != 0:
            return False, {}, {}, stderr_load or f"processus Maude en echec ({proc.returncode})"
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError:
            return False, {}, {}, stderr_load or "sortie illisible"

        if not data["loaded"] or "Warning" in stderr_load or "Error" in stderr_load:
            return False, data.get("results", {}), data.get("times", {}), stderr_load

        return True, data["results"], data.get("times", {}), stderr_load
