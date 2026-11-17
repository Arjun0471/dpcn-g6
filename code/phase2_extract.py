"""Re-read citing works (with authorships) from the cache; save compact table."""
import json, glob, pickle, sys
sys.path.insert(0, '.')
import group6_pipeline as gp
S = pickle.load(open('phase2_state.pkl', 'rb'))
corpus = set(S['papers'])
rows = {}
for f in glob.glob('cache/*.json'):
    d = json.load(open(f))
    for w in d.get('results', []) or []:
        if 'referenced_works' not in w or 'primary_location' in w or 'authorships' not in w:
            continue
        wid = gp.short(w['id'])
        if wid in corpus or wid in rows:
            continue
        refs = {gp.short(r) for r in w.get('referenced_works') or []} & corpus
        if not refs:
            continue
        auths = []
        for a in w['authorships']:
            aid = gp.short((a.get('author') or {}).get('id'))
            insts = [(gp.short(i.get('id')), i.get('display_name'), i.get('country_code'), i.get('type')) for i in a.get('institutions') or []]
            auths.append((aid, (a.get('author') or {}).get('display_name'), insts))
        rows[wid] = {'year': w.get('publication_year'), 'refs': refs, 'auths': auths, 'n_refs_total': len(w.get('referenced_works') or [])}
print(len(rows))
pickle.dump(rows, open('phase2_citing.pkl', 'wb'))
