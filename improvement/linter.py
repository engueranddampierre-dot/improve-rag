"""Micro-linter Maude pour code genere par LLM.

Chaque regle vient d'un echec REEL observe dans tests/rag-gemini-2.5-flash :
- repeated.maude       : guard `when` emprunte a Haskell/SML
- simple-list.maude    : apostrophe typographique U+2019, commentaires `--`
- collatz.maude        : `=` au lieu de `==` dans un terme if_then_else_fi
- free-tuples.maude    : pattern non-lineaire involontaire (variable repetee)

Deux usages :
- diagnostics clairs a injecter dans le prompt de reparation (les messages
  du parseur Maude sont souvent laconiques : "parsing error")
- autofix des substitutions sures (ponctuation Unicode -> ASCII)
"""
import re
import unicodedata

FATAL = "fatal"      # ne compilera pas
WARN  = "warning"    # legal mais suspect dans du code genere


# --- Substitutions Unicode sures (copie depuis PDF/traitement de texte) ---
UNICODE_FIXES = {
    "’": "'",   # '
    "‘": "'",   # '
    "“": '"',   # "
    "”": '"',   # "
    "–": "-",   # –
    "—": "-",   # —
    " ": " ",   # espace insecable
    "…": "...",
}


def autofix(code):
    """Applique les corrections deterministes. Retourne (code, corrections)."""
    fixes = []
    for bad, good in UNICODE_FIXES.items():
        if bad in code:
            fixes.append(f"caractere Unicode {unicodedata.name(bad, hex(ord(bad)))} remplace par {good!r}")
            code = code.replace(bad, good)
    return code, fixes


def _sans_commentaires(ligne):
    """Tronque une ligne a partir d'un commentaire *** ou ---."""
    for marque in ("***", "---"):
        pos = ligne.find(marque)
        if pos != -1:
            ligne = ligne[:pos]
    return ligne


def _variables_declarees(code):
    """Variables declarees par var/vars (+ inline X:Sort)."""
    declarees = set()
    for m in re.finditer(r'^\s*vars?\s+(.+?)\s*:\s*\S+\s*\.', code, re.MULTILINE):
        declarees.update(m.group(1).split())
    declarees.update(re.findall(r'\b([A-Za-z][\w\'-]*):(?=[A-Za-z])', code))
    return declarees


def lint(code):
    """Retourne une liste de dicts {severity, line, msg}."""
    issues = []
    lignes = code.split("\n")

    def add(sev, num, msg):
        issues.append({"severity": sev, "line": num, "msg": msg})

    for num, brute in enumerate(lignes, 1):
        ligne = _sans_commentaires(brute)

        # 1. Caracteres non-ASCII hors commentaires
        for ch in ligne:
            if ord(ch) > 127:
                nom = unicodedata.name(ch, hex(ord(ch)))
                add(FATAL, num,
                    f"caractere non-ASCII {ch!r} ({nom}) — Maude ne le parsera pas ; "
                    f"probablement une apostrophe/un tiret typographique a remplacer")
                break

        # 2. Guard `when` (n'existe pas en Maude)
        if re.search(r'\bwhen\b', ligne):
            add(FATAL, num,
                "mot-cle `when` : n'existe pas en Maude (guard emprunte a Haskell/SML) ; "
                "utiliser une equation conditionnelle `ceq ... if ...`")

        # 3. Commentaires `--` (Maude accepte `***` et `---` uniquement)
        if re.search(r'(^|\s)--(?!-)(\s|$)', brute):
            add(FATAL, num,
                "commentaire `--` : Maude n'accepte que `***` ou `---`")

        # 4. `=` simple dans un terme if_then_else_fi (il faut `==`)
        m = re.search(r'\bif\b(.*?)\bthen\b', ligne)
        if m and re.search(r'(?<![=<>~/\\])=(?![=/])', m.group(1)):
            add(FATAL, num,
                "`=` dans un terme if_then_else_fi : `=` n'est pas un operateur Bool ; "
                "utiliser `==` (l'egalite `cond = val` n'est legale que dans les "
                "conditions de ceq/crl, pas dans un terme)")

    # 5. Patterns non-lineaires dans les membres gauches d'equations
    declarees = _variables_declarees(code)
    for num, brute in enumerate(lignes, 1):
        ligne = _sans_commentaires(brute)
        m = re.match(r'\s*(?:eq|ceq)\s+(.*?)\s=(?!=)\s', ligne)
        if not m:
            continue
        lhs = m.group(1)
        tokens = re.findall(r"[A-Za-z][\w'-]*", lhs)
        for v in declarees:
            if tokens.count(v) > 1:
                add(WARN, num,
                    f"pattern non-lineaire : la variable {v} apparait "
                    f"{tokens.count(v)} fois dans le membre gauche — legal en Maude "
                    f"(exige l'egalite des sous-termes) mais souvent involontaire "
                    f"dans du code genere ; verifier que c'est voulu")

    # 6. Identifiants suspects non declares dans les equations
    #    (heuristique : token style variable, utilise dans eq/rl, ni declare
    #    ni operateur/sorte connu — le parseur le signalera de toute facon,
    #    mais ce message est plus clair que le sien)
    ops = set(re.findall(r'^\s*ops?\s+(.+?)\s*:', code, re.MULTILINE))
    ops_tokens = set()
    for o in ops:
        ops_tokens.update(re.findall(r"[A-Za-z][\w'-]*", o))
    sortes = set()
    for m in re.finditer(r'^\s*sorts?\s+(.+?)\s*\.', code, re.MULTILINE):
        sortes.update(m.group(1).split())
    MOTS_CLES = {'eq', 'ceq', 'rl', 'crl', 'mb', 'cmb', 'if', 'then', 'else',
                 'fi', 'and', 'or', 'not', 'true', 'false', 'owise', 'otherwise',
                 'is', 'sort', 'sorts', 'op', 'ops', 'var', 'vars', 'subsort',
                 'subsorts', 'protecting', 'including', 'extending', 'rem',
                 'quo', 'gcd', 'lcm', 'min', 'max', 'sd', 'abs', 'ctor',
                 'assoc', 'comm', 'id', 'prec', 'gather', 'endfm', 'endm'}
    for num, brute in enumerate(lignes, 1):
        ligne = _sans_commentaires(brute)
        if not re.match(r'\s*(?:c?eq|c?rl)\b', ligne):
            continue
        for tok in set(re.findall(r"\b[A-Z][\w'-]*\b", ligne)):
            if tok in declarees or tok in ops_tokens or tok in sortes:
                continue
            if tok.lower() in MOTS_CLES or tok in ('Bool', 'Nat', 'Int', 'Float', 'String', 'Qid'):
                continue
            add(WARN, num,
                f"identifiant {tok} utilise dans une equation/regle sans etre "
                f"declare (ni var, ni op, ni sort) — si c'est une variable, "
                f"la declarer ou ecrire {tok}:Sorte")

    return issues


def format_issues(issues):
    """Formatage pour le prompt de reparation."""
    return "\n".join(
        f"- ligne {i['line']} [{i['severity']}] : {i['msg']}" for i in issues
    )


def fatals(issues):
    return [i for i in issues if i["severity"] == FATAL]


if __name__ == "__main__":
    import sys
    from pathlib import Path
    code = Path(sys.argv[1]).read_text()
    code, fixes = autofix(code)
    for f in fixes:
        print(f"[autofix] {f}")
    issues = lint(code)
    print(format_issues(issues) if issues else "aucun probleme detecte")
