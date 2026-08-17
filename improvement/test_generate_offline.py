"""Test hors ligne de generate.py (zero appel API, zero token).
Usage : python test_generate_offline.py   (depuis improvement/, venv actif)

Scenario : spec pow -> candidat 1 faux (le vrai pow casse de
rag-gemini-2.5-flash) -> candidat 2 correct (l'original). Verifie que la
boucle rejette puis accepte, que la reference n'est jamais montree au
modele, et que le connecteur EdenAI extrait bien les blocs de code.
"""
import json
import sys
from pathlib import Path

import generate
import repair

HERE = Path(__file__).parent
ORIG = HERE / 'tests/original/maudec/maude'


def sans_commentaires(p):
    return '\n'.join(l for l in p.read_text().split('\n')
                     if not l.startswith('***')).strip() + '\n'


def main():
    # --- 1. boucle de generation scriptee sur pow ---
    casse = sans_commentaires(HERE / 'tests/rag-gemini-2.5-flash/maudec/maude/pow.maude')
    correct = (ORIG / 'pow.maude').read_text()
    rp = Path('/tmp/gen-pow.json')
    rp.write_text(json.dumps([{'comment': 'try1', 'code': casse},
                              {'comment': 'try2', 'code': correct}]))

    conn = repair.Scripted(str(rp))
    orig_get = repair.get_connector
    repair.get_connector = lambda name: conn
    generate.get_connector = lambda name: conn
    try:
        code, comment, trace = generate.gen_loop(
            HERE / 'specs/maudec/maude/pow.txt', 'ignore', 'none',
            max_iters=3, seed=0)
    finally:
        repair.get_connector = orig_get
        generate.get_connector = orig_get

    assert trace['final'] == 'ok', trace
    assert trace['iterations'][0]['ok'] is False
    assert trace['iterations'][1]['ok'] is True
    print('1. boucle generation OK (rejet iter 1, accepte iter 2)')

    # --- 2. la reference n'apparait dans AUCUN prompt ---
    for msg in conn.calls:
        assert 'eq f(X, s N) = X * f(X, N)' not in msg, "la reference a fuite dans le prompt !"
    assert 'SPECIFICATION' in conn.calls[0] and 'f(2, 3)' in conn.calls[0]
    print('2. reference jamais montree au modele, spec et termes presents')

    # --- 3. connecteur EdenAI : extraction des blocs de code ---
    rep = repair.EdenAI._separate_code(
        "Here is the program:\n```maude\nfmod M is\nendfm\n```\nDone.")
    assert 'fmod M is' in rep['code'] and 'Here is' in rep['comment']
    rep2 = repair.EdenAI._separate_code("no code block at all")
    assert rep2['code'].strip() == ''
    print('3. extraction EdenAI OK (avec et sans bloc ```)')

    # --- 4. routage des connecteurs ---
    import os
    os.environ.setdefault('EDENAI_API_KEY', 'test-key')
    c = repair.get_connector('edenai:deepseek/deepseek-v4-flash')
    assert isinstance(c, repair.EdenAI) and c.model == 'deepseek/deepseek-v4-flash'
    print('4. routage edenai: OK')

    print('\nTOUT EST OK')


if __name__ == '__main__':
    main()
