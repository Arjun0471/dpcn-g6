#!/usr/bin/env python3
"""
DPCN Phase II analysis - Group 6 (IIT Bhubaneswar, IIT Indore, IIT Mandi), 2016-2026.

Runs after group6_pipeline.py (which writes phase2_state.pkl) and phase2_extract.py (phase2_citing.pkl).
Everything is computed offline from the cached OpenAlex responses, scimagojr.csv and faculty_list.csv,
plus citer_meta.json / citer_years.json (OpenAlex output counts of the top 60 citing institutions).

Scope rules (from the Phase II directions):
  * Publication statistics use ALL institute papers, students' papers included.
  * Faculty statistics and faculty networks use only listed faculty (faculty_list.csv). Several OpenAlex
    profiles with the same name at the same institute are merged into one listed person.
  * "Impact factor" = SCImago "Citations / Doc. (2 years)": citations in year Y to items of Y-1 and Y-2,
    divided by those items. Same formula as the Clarivate JIF, computed on Scopus data (JCR is not open).

Outputs: out/phase2/*.csv and out/phase2/phase2_data.json (the dashboard reads the JSON).
"""
import json
import pickle
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import networkx as nx
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import group6_pipeline as gp  # noqa: E402

OUT = HERE / "out" / "phase2"
OUT.mkdir(parents=True, exist_ok=True)
YEARS = list(range(2016, 2027))
INST = {k: v["name"] for k, v in gp.INSTITUTIONS.items()}
OURS = set(INST)
MEGA = 10            # "papers with 10-100 authors" threshold from the directions
HYPER = 100          # OpenAlex lists at most 100 authors per work in list results: 100 means "100 or more"

# private (self-financed / deemed-private) universities among the top-60 citing institutions; all others in
# that list are central/state government institutions, government labs (CSIR, DAE, MoES) or public universities
PRIVATE = {"I876193797": "VIT", "I85461943": "Saveetha", "I145286018": "SRM IST", "I164861460": "Manipal (MAHE)",
           "I191972202": "Amity", "I81556334": "Amrita", "I110360157": "Lovely Professional Univ.",
           "I101407740": "Chandigarh Univ.", "I74319210": "Chitkara", "I74796645": "BITS Pilani",
           "I875944469": "KL (Koneru Lakshmaiah)", "I67357951": "KIIT", "I60054993": "Graphic Era",
           "I193073490": "Siksha O Anusandhan", "I106826634": "Jain Univ.", "I162030827": "Thapar",
           "I5847235": "UPES", "I82571370": "GLA Univ."}


def log(*a):
    print(*a, flush=True)


def load():
    S = pickle.load(open(HERE / "phase2_state.pkl", "rb"))
    C = pickle.load(open(HERE / "phase2_citing.pkl", "rb"))
    return S, C


def scimago_if():
    df = pd.read_csv(HERE / "scimagojr.csv", sep=";", dtype=str, on_bad_lines="skip")
    col = "Citations / Doc. (2years)"
    by_issn, by_title = {}, {}
    for _, r in df.iterrows():
        try:
            v = float(str(r[col]).replace(",", "."))
        except ValueError:
            continue
        for issn in str(r.get("Issn", "")).split(","):
            issn = issn.strip().upper()
            if len(issn) == 8:
                by_issn.setdefault(issn, v)
        by_title.setdefault(gp.norm_title(r.get("Title")), v)
    return by_issn, by_title


def main():
    S, C = load()
    P = S["papers"]                        # all institute papers (journal + conference), students included
    fac = S["faculty"]                     # set of (author_id, inst_id) profiles matched to the list
    names = S["names"]
    dept = S["dept"]
    ainfo = S["author_info"]
    by_issn, by_title = scimago_if()

    # ---------------- listed people (merge same-name profiles at one institute)
    fl = pd.read_csv(HERE / "faculty_list.csv", dtype=str).fillna("")
    list_name = {}
    for _, r in fl.iterrows():
        iid = gp.INST_BY_NAME.get(r["institution"].strip())
        list_name[(" ".join(gp.norm_name(r["name"])), iid)] = r["name"].strip()
    person_of = {}                         # (aid, iid) -> person key "inst|normalised name"
    for aid, iid in fac:
        k = (" ".join(gp.norm_name(names[aid])), iid)
        person_of[(aid, iid)] = f"{iid}|{k[0]}"
    persons = defaultdict(lambda: {"profiles": set()})
    for (aid, iid), pk in person_of.items():
        k = (pk.split("|", 1)[1], iid)
        persons[pk].update(name=list_name.get(k, names[aid]), iid=iid)
        persons[pk]["profiles"].add(aid)
    log(f"{len(persons)} listed faculty (from {len(fac)} OpenAlex profiles)")

    # ---------------- paper table (all papers)
    prow = {}
    for pid, p in P.items():
        auths = p["authorships"]
        n_auth = p.get("n_authors_full") or len(auths)   # true count, also for 100+ author papers
        insts_all = {}
        countries = set()
        for a in auths:
            for i in a.get("institutions") or []:
                if i.get("id"):
                    insts_all[gp.short(i["id"])] = (i.get("display_name"), i.get("country_code"), i.get("type"))
                if i.get("country_code"):
                    countries.add(i["country_code"])
        issn = p["issn"].replace("-", "").upper() if p["issn"] else ""
        jif = None
        if p["type"] == "journal":
            jif = by_issn.get(issn)
            if jif is None:
                jif = by_title.get(gp.norm_title(p["venue"]))
        prow[pid] = {
            "id": pid, "title": p["title"], "year": p["year"], "type": p["type"], "venue": p["venue"],
            "doi": p["doi"], "citations": p["citations"], "quartile": p["quartile"], "if": jif,
            "n_authors": n_auth, "field": p["field"], "our_insts": sorted({i for i in insts_all if i in OURS}),
            "partners": {k: v for k, v in insts_all.items() if k not in OURS},
            "intl": any(c != "IN" for c in countries),
        }

    # faculty authors per paper (person level)
    paper_people = defaultdict(set)
    for pid, aid, nm, iid, _ in S["author_rows"]:
        if (aid, iid) in person_of:
            paper_people[pid].add(person_of[(aid, iid)])
    for pid in prow:
        prow[pid]["faculty"] = sorted(paper_people.get(pid, ()))

    # ---------------- 1. institutional overview (all papers; faculty counts from the list)
    def author_class(n):
        return "<10" if n < MEGA else ("10-99" if n < HYPER else "100+")

    overview, trend = [], []
    for iid, nm in list(INST.items()) + [("ALL", "Group 6 (all three)")]:
        ps = [r for r in prow.values() if iid == "ALL" or iid in r["our_insts"]]
        js = [r for r in ps if r["type"] == "journal"]
        q1 = [r for r in js if r["quartile"] == "Q1"]
        cls = Counter(author_class(r["n_authors"]) for r in ps)
        nfac = sum(1 for k, v in persons.items() if iid == "ALL" or v["iid"] == iid)
        listed = int((fl["institution"] == nm).sum()) if iid != "ALL" else len(fl)
        overview.append({
            "institution": nm, "listed_faculty": listed, "faculty_with_papers": nfac,
            "publications": len(ps), "with_faculty_author": sum(1 for r in ps if r["faculty"]),
            "journal": len(js), "conference": len(ps) - len(js),
            "q1": len(q1), "q1_if_gt5": sum(1 for r in q1 if (r["if"] or 0) > 5),
            "q1_if_gt10": sum(1 for r in q1 if (r["if"] or 0) > 10),
            "authors_lt10": cls["<10"], "authors_ge10": cls["10-99"] + cls["100+"], "authors_ge100": cls["100+"],
            "citations": sum(r["citations"] for r in ps),
            "international_share": round(sum(r["intl"] for r in ps) / max(1, len(ps)), 3),
        })
        for y in YEARS:
            py = [r for r in ps if r["year"] == y]
            partners = set()
            ind = set()
            for r in py:
                for k, (n_, cc, t) in r["partners"].items():
                    partners.add(k)
                    if cc == "IN":
                        ind.add(k)
            trend.append({"institution": nm, "year": y, "publications": len(py),
                          "journal": sum(1 for r in py if r["type"] == "journal"),
                          "conference": sum(1 for r in py if r["type"] == "conference"),
                          "q1": sum(1 for r in py if r["quartile"] == "Q1"),
                          "authors_ge10": sum(1 for r in py if r["n_authors"] >= MEGA),
                          "collab_institutions": len(partners), "collab_indian": len(ind),
                          "collab_foreign": len(partners) - len(ind),
                          "international_papers": sum(r["intl"] for r in py)})
    pd.DataFrame(overview).to_csv(OUT / "institution_overview.csv", index=False)
    pd.DataFrame(trend).to_csv(OUT / "yearly_trend.csv", index=False)

    # ---------------- 2. faculty and departments (listed people)
    # co-authorship among listed faculty: person-level graph, one edge weight per joint paper
    FG = nx.Graph()
    FG.add_nodes_from(persons)
    yearly_edges = defaultdict(list)
    for pid, ppl in paper_people.items():
        if prow[pid]["n_authors"] >= HYPER:
            continue      # 100+ author consortium papers (ALICE, Belle II, ...) are not treated as collaboration links
        ppl = sorted(ppl)
        for a, b in combinations(ppl, 2):
            w = FG[a][b]["weight"] + 1 if FG.has_edge(a, b) else 1
            FG.add_edge(a, b, weight=w)
            yearly_edges[prow[pid]["year"]].append((a, b))
    deg = dict(FG.degree())
    k = None if len(FG) <= 2500 else 600
    btw = nx.betweenness_centrality(FG, k=k, seed=42)
    comms = nx.community.louvain_communities(FG, weight="weight", seed=42)
    comms = sorted(comms, key=len, reverse=True)
    comm_of = {n: i for i, c in enumerate(comms) for n in c}
    modularity = nx.community.modularity(FG, comms, weight="weight")

    fac_rows = []
    person_papers = defaultdict(set)
    for pid, ppl in paper_people.items():
        for pk in ppl:
            person_papers[pk].add(pid)
    for pk, v in persons.items():
        ps = [prow[x] for x in person_papers[pk]]
        cits = sorted((r["citations"] for r in ps), reverse=True)
        h_win = sum(1 for i, c in enumerate(cits, 1) if c >= i)
        mega = [r for r in ps if r["n_authors"] >= MEGA]
        coauthors = set()
        partner_insts = set()
        for r in ps:
            partner_insts |= set(r["partners"])
            coauthors |= {gp.short((a.get("author") or {}).get("id")) for a in P[r["id"]]["authorships"]}
        coauthors -= v["profiles"]
        prof = [ainfo.get(a, {}) for a in v["profiles"]]
        life_c = max((x.get("cited_by_count") or 0 for x in prof), default=0)
        life_h = max(((x.get("summary_stats") or {}).get("h_index") or 0 for x in prof), default=0)
        depts = Counter(dept.get((a, v["iid"]), "Unknown") for a in v["profiles"])
        venues = Counter(r["venue"] for r in ps if r["type"] == "journal" and r["venue"])
        mega_c = sum(r["citations"] for r in mega)
        tot_c = sum(cits)
        flags = []
        if life_c >= 100_000:
            flags.append("lifetime citations >= 1 lakh")
        if tot_c and mega_c / tot_c >= 0.5:
            flags.append(f">= 50% of citations from {MEGA}+ author papers")
        if any(r["n_authors"] >= HYPER for r in ps):
            flags.append("has 100+ author papers")
        fac_rows.append({
            "person": pk, "name": v["name"], "institution": INST[v["iid"]],
            "department": depts.most_common(1)[0][0], "openalex_profiles": len(v["profiles"]),
            "papers": len(ps), "q1_papers": sum(1 for r in ps if r["quartile"] == "Q1"),
            "q1_if_gt5": sum(1 for r in ps if r["quartile"] == "Q1" and (r["if"] or 0) > 5),
            "citations": tot_c, "h_index_2016_2026": h_win,
            "h_index_lifetime": life_h, "citations_lifetime": life_c,
            "papers_10plus_authors": len(mega), "citations_from_10plus": mega_c,
            "citations_excl_10plus": tot_c - mega_c,
            "share_citations_10plus": round(mega_c / tot_c, 3) if tot_c else 0,
            "coauthors": len(coauthors), "faculty_coauthors": deg.get(pk, 0),
            "partner_institutions": len(partner_insts),
            "betweenness": round(btw.get(pk, 0), 5), "community": comm_of.get(pk, -1),
            "top_journal": venues.most_common(1)[0][0] if venues else "",
            "flags": "; ".join(flags),
        })
    fdf = pd.DataFrame(fac_rows).sort_values("papers", ascending=False)
    fdf.drop(columns=["person"]).to_csv(OUT / "faculty_comparison.csv", index=False)

    # top publications by journal impact factor (IF, then citations as tie-break)
    def top_by_if(ps, n):
        ps = [r for r in ps if r["if"] is not None]
        return sorted(ps, key=lambda r: (-r["if"], -r["citations"]))[:n]

    def pub_out(r):
        return {"title": r["title"], "journal": r["venue"], "year": r["year"], "if": round(r["if"], 2),
                "quartile": r["quartile"], "citations": r["citations"], "doi": r["doi"],
                "n_authors": r["n_authors"], "faculty": [persons[x]["name"] for x in r["faculty"]][:6],
                "fk": r["faculty"][:6]}

    top30 = {nm: [pub_out(r) for r in top_by_if([x for x in prow.values() if iid in x["our_insts"]], 30)]
             for iid, nm in INST.items()}
    top30["Group 6 (all three)"] = [pub_out(r) for r in top_by_if(list(prow.values()), 30)]
    pd.DataFrame([dict(scope=k, rank=i + 1, **{kk: vv for kk, vv in r.items() if kk != "faculty"},
                       faculty="; ".join(r["faculty"])) for k, v in top30.items() for i, r in enumerate(v)]
                 ).to_csv(OUT / "top30_publications_by_IF.csv", index=False)

    freq_j = {}
    for iid, nm in list(INST.items()) + [("ALL", "Group 6 (all three)")]:
        c = Counter(r["venue"] for r in prow.values() if r["type"] == "journal" and (iid == "ALL" or iid in r["our_insts"]))
        ifs = {r["venue"]: r["if"] for r in prow.values() if r["type"] == "journal"}
        q = {r["venue"]: r["quartile"] for r in prow.values() if r["type"] == "journal"}
        freq_j[nm] = [{"journal": j, "papers": n, "if": round(ifs.get(j) or 0, 2) if ifs.get(j) else None,
                       "quartile": q.get(j, "")} for j, n in c.most_common(20)]
    pd.DataFrame([dict(scope=k, **r) for k, v in freq_j.items() for r in v]).to_csv(OUT / "frequent_journals.csv", index=False)

    per_fac_top10 = {}
    rows10 = []
    for pk, v in persons.items():
        best = top_by_if([prow[x] for x in person_papers[pk]], 10)
        if best:
            per_fac_top10[pk] = [pub_out(r) for r in best]
            for i, r in enumerate(best):
                rows10.append({"name": v["name"], "institution": INST[v["iid"]], "rank": i + 1, "title": r["title"],
                               "journal": r["venue"], "if": round(r["if"], 2), "quartile": r["quartile"],
                               "year": r["year"], "citations": r["citations"], "doi": r["doi"]})
    pd.DataFrame(rows10).to_csv(OUT / "faculty_top10_by_IF.csv", index=False)

    dep_rows = []
    for (inst, dp), g in fdf.groupby(["institution", "department"]):
        pids = set().union(*[person_papers[p] for p in g["person"]])
        ps = [prow[x] for x in pids]
        js = [r for r in ps if r["type"] == "journal"]
        dep_rows.append({"institution": inst, "department": dp, "faculty": len(g), "papers": len(ps),
                         "q1_share": round(sum(r["quartile"] == "Q1" for r in js) / max(1, len(js)), 3),
                         "citations": sum(r["citations"] for r in ps),
                         "median_papers_per_faculty": float(g["papers"].median()),
                         "median_h_2016_2026": float(g["h_index_2016_2026"].median())})
    ddf = pd.DataFrame(dep_rows).sort_values(["institution", "papers"], ascending=[True, False])
    ddf.to_csv(OUT / "department_comparison.csv", index=False)

    # ---------------- 3. networks
    # 3a co-authorship (faculty only) - picture: largest components, highest degree first
    viz = []
    for c in sorted(nx.connected_components(FG), key=len, reverse=True):
        if len(c) < 3 or len(viz) >= 320:
            break
        viz += sorted(c, key=lambda n: -deg[n])[:320 - len(viz)]
    vs = set(viz)
    coauth = {"nodes": [{"id": n, "label": persons[n]["name"], "inst": INST[persons[n]["iid"]],
                         "community": comm_of[n], "degree": deg[n], "btw": round(btw[n], 5),
                         "papers": len(person_papers[n])} for n in viz],
              "edges": [{"s": a, "t": b, "w": d["weight"]} for a, b, d in FG.edges(data=True) if a in vs and b in vs],
              "n": FG.number_of_nodes(), "m": FG.number_of_edges(),
              "isolated": sum(1 for n in FG if deg[n] == 0), "communities": len([c for c in comms if len(c) > 1]),
              "modularity": round(modularity, 3),
              "largest_component": len(max(nx.connected_components(FG), key=len))}

    # 3b institutional network: institutions on Group 6 papers; edge = papers on which both appear.
    # Built twice: all papers, and without 100+ author consortium papers (which add hundreds of foreign partners).
    inst_meta = {}
    for r in prow.values():
        for k_ in r["our_insts"]:
            inst_meta[k_] = (INST[k_], "IN", "group6")
        for k_, (n_, cc, t) in r["partners"].items():
            inst_meta[k_] = (n_, cc, t)

    def itype(n):
        nm_, cc, t = inst_meta.get(n, ("", "", ""))
        if n in OURS:
            return "Group 6"
        if cc != "IN":
            return "Foreign"
        return "Indian (" + gp.cluster_of(nm_) + ")"

    def build_instnet(exclude_hyper):
        IG = nx.Graph()
        country = Counter()
        for r in prow.values():
            if exclude_hyper and r["n_authors"] >= HYPER:
                continue
            ins = set(r["our_insts"]) | set(r["partners"])
            for a, b in combinations(sorted(ins), 2):
                if a in OURS or b in OURS:          # ego network of the three IITs (partner-partner links omitted)
                    IG.add_edge(a, b, weight=IG[a][b]["weight"] + 1 if IG.has_edge(a, b) else 1)
            for cc in {v[1] for v in r["partners"].values() if v[1] and v[1] != "IN"}:
                country[cc] += 1
        strength = {n: sum(d["weight"] for _, _, d in IG.edges(n, data=True)) for n in IG}
        ranked = sorted((n for n in IG if n not in OURS), key=lambda n: -strength[n])
        keep = set(ranked[:90]) | OURS
        kinds = Counter(itype(n) for n in IG if n not in OURS)
        net = {"nodes": [{"id": n, "label": inst_meta[n][0], "country": inst_meta[n][1], "kind": itype(n),
                          "papers": strength[n]} for n in keep if n in inst_meta],
               "edges": [{"s": a, "t": b, "w": d["weight"]} for a, b, d in IG.edges(data=True) if a in keep and b in keep],
               "n_partners": IG.number_of_nodes() - len(OURS & set(IG)),
               "n_indian": sum(1 for n in IG if n not in OURS and inst_meta[n][1] == "IN"),
               "n_countries": len({inst_meta[n][1] for n in IG if n not in OURS}),
               "top_countries": country.most_common(15),
               "kinds": kinds.most_common(),
               "top_partners": [{"institution": inst_meta[n][0], "country": inst_meta[n][1], "kind": itype(n),
                                 "shared_papers": strength[n]} for n in ranked[:25]]}
        return net, ranked, strength

    instnet, ranked_x, strength_x = build_instnet(True)
    instnet_all, ranked_a, strength_a = build_instnet(False)
    pd.DataFrame([{"institution": inst_meta[n][0], "country": inst_meta[n][1], "kind": itype(n),
                   "shared_papers_excl_100plus_author_papers": strength_x.get(n, 0),
                   "shared_papers_all": strength_a[n], "openalex_id": n} for n in ranked_a]
                 ).to_csv(OUT / "institutional_network_partners.csv", index=False)

    # 3c temporal analysis: faculty co-authorship and collaboration by year
    temporal = []
    cum = nx.Graph()
    for y in YEARS:
        Gy = nx.Graph()
        Gy.add_edges_from(yearly_edges.get(y, []))
        cum.add_edges_from(yearly_edges.get(y, []))
        act = {pk for pid, ppl in paper_people.items() if prow[pid]["year"] == y for pk in ppl}
        Gy.add_nodes_from(act)
        lc = max((len(c) for c in nx.connected_components(Gy)), default=0)
        cross = sum(1 for a, b in Gy.edges() if persons[a]["iid"] != persons[b]["iid"])
        temporal.append({"year": y, "active_faculty": len(act), "coauthor_links": Gy.number_of_edges(),
                         "avg_degree": round(2 * Gy.number_of_edges() / max(1, len(act)), 2),
                         "largest_component_share": round(lc / max(1, len(act)), 3),
                         "cross_institute_links": cross, "cumulative_links": cum.number_of_edges(),
                         "density": round(nx.density(Gy), 5) if len(Gy) > 1 else 0})
    pd.DataFrame(temporal).to_csv(OUT / "temporal_network.csv", index=False)

    # 3d citation network (within the corpus; all papers)
    CG = nx.DiGraph()
    CG.add_nodes_from(prow)
    for pid, p in P.items():
        for r in p["refs"]:
            if r in prow and r != pid:
                CG.add_edge(pid, r)
    pr = nx.pagerank(CG, alpha=0.85)
    indeg = dict(CG.in_degree())
    cit_year = Counter()
    for u, v in CG.edges():
        cit_year[prow[u]["year"]] += 1
    cross_inst = sum(1 for u, v in CG.edges() if not set(prow[u]["our_insts"]) & set(prow[v]["our_insts"]))
    citnet = {"nodes": CG.number_of_nodes(), "edges": CG.number_of_edges(), "cross_institute_edges": cross_inst,
              "pagerank_top": [{"title": prow[n]["title"], "year": prow[n]["year"], "pagerank": round(pr[n], 6),
                                "in_degree": indeg[n], "citations": prow[n]["citations"],
                                "institutions": ", ".join(INST[i] for i in prow[n]["our_insts"])}
                               for n, _ in sorted(pr.items(), key=lambda x: -x[1])[:15]],
              "in_degree_hist": {str(k_): v for k_, v in sorted(Counter(min(d, 30) for d in indeg.values()).items())},
              "edges_by_year": [cit_year.get(y, 0) for y in YEARS]}

    # ---------------- 4. notes: who cites Group 6, and large-collaboration papers
    meta = json.load(open(HERE / "citer_meta.json"))
    yout = json.load(open(HERE / "citer_years.json"))
    g6_people = {a for _, a, _, _, _ in S["author_rows"]}          # anyone who published from a Group 6 IIT
    paper_auth = {pid: {gp.short((a.get("author") or {}).get("id")) for a in p["authorships"]} for pid, p in P.items()}
    st = defaultdict(Counter)
    yr = defaultdict(Counter)
    top_auth = defaultdict(Counter)
    for cid, c in C.items():
        aids = {a for a, _, _ in c["auths"]}
        alum = bool(aids & g6_people)
        selfc = any(aids & paper_auth[r] for r in c["refs"])
        seen = set()
        for aid, nm, ins in c["auths"]:
            for iid, *_ in ins:
                if iid in meta:
                    top_auth[iid][aid] += len(c["refs"])
                    if iid not in seen:
                        seen.add(iid)
                        s = st[iid]
                        s["papers"] += 1
                        s["cites"] += len(c["refs"])
                        s["alum"] += alum
                        s["self"] += selfc
                        yr[iid][c["year"]] += 1
    citers = []
    for iid, m in meta.items():
        s = st[iid]
        o1 = sum(yout[iid][str(y)] for y in (2018, 2019))
        o2 = sum(yout[iid][str(y)] for y in (2024, 2025))
        c1 = sum(yr[iid][y] for y in (2018, 2019))
        c2 = sum(yr[iid][y] for y in (2024, 2025))
        ta = top_auth[iid]
        citers.append({
            "institution": m["n"], "ownership": "Private" if iid in PRIVATE else "Government / public",
            "openalex_type": m["t"], "citing_papers": s["papers"], "citations_to_group6": s["cites"],
            "own_output_2016_2026": m["w"],
            "citing_papers_per_1000_own_papers": round(1000 * s["papers"] / m["w"], 1),
            "rate_2018_19": round(1000 * c1 / o1, 1) if o1 else None,
            "rate_2024_25": round(1000 * c2 / o2, 1) if o2 else None,
            "own_output_growth": round(o2 / o1, 1) if o1 else None,
            "citing_growth": round(c2 / c1, 1) if c1 else None,
            "group6_refs_per_citing_paper": round(s["cites"] / max(1, s["papers"]), 2),
            "share_by_former_group6_authors": round(s["alum"] / max(1, s["papers"]), 3),
            "share_author_self_citation": round(s["self"] / max(1, s["papers"]), 3),
            "share_from_top10_citing_authors": round(sum(v for _, v in ta.most_common(10)) / max(1, sum(ta.values())), 3),
            "yearly_citing_papers": [yr[iid].get(y, 0) for y in YEARS],
            "yearly_output": [yout[iid][str(y)] for y in YEARS],
        })
    cdf = pd.DataFrame(citers).sort_values("citations_to_group6", ascending=False)
    cdf.drop(columns=["yearly_citing_papers", "yearly_output"]).to_csv(OUT / "citing_institutions_analysis.csv", index=False)
    grp = cdf.groupby("ownership")[["citing_papers_per_1000_own_papers", "rate_2018_19", "rate_2024_25",
                                    "own_output_growth", "citing_growth", "group6_refs_per_citing_paper",
                                    "share_by_former_group6_authors", "share_author_self_citation"]].median().round(3)
    grp.to_csv(OUT / "citing_institutions_private_vs_government.csv")

    big = sorted((r for r in prow.values() if r["n_authors"] >= MEGA), key=lambda r: -r["citations"])
    pd.DataFrame([{"title": r["title"], "year": r["year"], "journal": r["venue"],
                   "authors": "100+" if r["n_authors"] >= HYPER else r["n_authors"], "citations": r["citations"],
                   "doi": r["doi"], "institutions": ", ".join(INST[i] for i in r["our_insts"]),
                   "group6_faculty": "; ".join(persons[x]["name"] for x in r["faculty"])} for r in big]
                 ).to_csv(OUT / "flagged_10plus_author_papers.csv", index=False)
    flagged_fac = fdf[fdf["flags"] != ""].sort_values("citations_lifetime", ascending=False)
    flagged_fac.drop(columns=["person"]).to_csv(OUT / "flagged_faculty.csv", index=False)
    big_share = {nm: {"papers": sum(1 for r in big if iid in r["our_insts"]),
                      "citations": sum(r["citations"] for r in big if iid in r["our_insts"]),
                      "all_citations": sum(r["citations"] for r in prow.values() if iid in r["our_insts"])}
                 for iid, nm in INST.items()}

    # ---------------- Phase I panels, recomputed on the same scope (all institute papers)
    ext = pd.read_csv(HERE / "out" / "supplementary" / "indian_connections_extended.csv") \
        if (HERE / "out" / "supplementary" / "indian_connections_extended.csv").exists() else pd.DataFrame()
    jac = {(r.your_inst, r.partner_inst): r.topic_jaccard for r in ext.itertuples()} if len(ext) else {}
    ref_ind = S["ref_indian"]
    scopes = list(INST.items()) + [("ALL", "Group 6 (all three)")]
    own_sets = {iid: ({iid} if iid != "ALL" else set(OURS)) for iid, _ in scopes}

    def in_scope(r, iid):
        return iid == "ALL" or iid in r["our_insts"]

    # collaboration type, team size and field vs citation impact.
    # "citation index" = a paper's citations / mean citations of all Group 6 papers of the same year,
    # so 1.0 is the Group 6 average and papers of different ages can be compared.
    year_mean = {y: (sum(r["citations"] for r in prow.values() if r["year"] == y) /
                     max(1, sum(1 for r in prow.values() if r["year"] == y))) for y in YEARS}
    KINDS = ["Single institute", "With other Indian institutions", "International"]
    SIZES = [("1", 1, 1), ("2–3", 2, 3), ("4–5", 4, 5), ("6–9", 6, 9), ("10–99", 10, 99), ("100+", 100, 10 ** 9)]
    for r in prow.values():
        r["kind"] = "International" if r["intl"] else ("With other Indian institutions" if r["partners"] else "Single institute")
        r["rel"] = r["citations"] / year_mean[r["year"]] if year_mean[r["year"]] else 0.0

    def grp_stats(rs):
        js_ = [r for r in rs if r["type"] == "journal"]
        return {"papers": len(rs), "cites_per_paper": round(sum(r["citations"] for r in rs) / max(1, len(rs)), 2),
                "citation_index": round(sum(r["rel"] for r in rs) / max(1, len(rs)), 3),
                "q1_share": round(sum(1 for r in js_ if r["quartile"] == "Q1") / max(1, len(js_)), 3)}

    def impact_block(ps):
        small = [r for r in ps if r["n_authors"] < MEGA]
        fl = []
        for fname, cnt in Counter(r["field"] for r in ps).most_common(10):
            rs = [r for r in ps if r["field"] == fname]
            a, b = sum(1 for r in rs if r["year"] == YEARS[0]), sum(1 for r in rs if r["year"] == YEARS[-2])
            fl.append({"field": fname, **grp_stats(rs), "share": round(cnt / len(ps), 3),
                       "international_share": round(sum(r["intl"] for r in rs) / len(rs), 3),
                       "growth": round(b / a, 1) if a >= 10 else None})
        return {
            "kinds": [{"kind": k, **grp_stats([r for r in small if r["kind"] == k])} for k in KINDS],
            "sizes": [{"size": lab, **grp_stats([r for r in ps if lo <= r["n_authors"] <= hi])} for lab, lo, hi in SIZES],
            "mix": {k: [round(sum(1 for r in ps if r["year"] == y and r["kind"] == k) /
                              max(1, sum(1 for r in ps if r["year"] == y)), 4) for y in YEARS] for k in KINDS},
            "venue": {t: grp_stats([r for r in ps if r["type"] == t]) for t in ("journal", "conference")},
            "quartile": {q: grp_stats([r for r in ps if r["type"] == "journal" and r["quartile"] == q]) for q in ("Q1", "Q2", "Q3", "Q4")},
            "fields": fl,
        }

    detail = {}
    for iid, nm in scopes:
        mine = own_sets[iid]
        ps = [r for r in prow.values() if in_scope(r, iid)]
        js = [r for r in ps if r["type"] == "journal"]
        cs = [r for r in ps if r["type"] == "conference"]
        qc = Counter(r["quartile"] or "Unranked" for r in js)
        cc_ = Counter(r["quartile"] or "Unranked" for r in cs)
        fields = Counter(r["field"] for r in ps)
        top_cited = sorted(ps, key=lambda r: -r["citations"])[:10]
        # citation flow with other Indian institutions
        in_year, out_year = Counter(), Counter()
        inflow, outflow = Counter(), Counter()
        for r in ps:
            for ref in P[r["id"]]["refs"]:
                tgt = P[ref]["indian"] if ref in P else (ref_ind.get(ref) or {}).get("insts")
                if not tgt:
                    continue
                others = {k: v for k, v in tgt.items() if k not in mine}
                if others:
                    out_year[r["year"]] += 1
                    for v in others.values():
                        outflow[v] += 1
        ids = {r["id"] for r in ps}
        for c in C.values():
            hit = c["refs"] & ids
            if not hit:
                continue
            insts = {i: n for _, _, ins in c["auths"] for i, n, cc, t in ins if cc == "IN" and i not in mine}
            if insts:
                in_year[c["year"]] += len(hit)
                for v in insts.values():
                    inflow[v] += len(hit)
        for u, v in CG.edges():                      # citations between Group 6 papers of different institutes
            if v in ids:
                others = {k: n for k, n in P[u]["indian"].items() if k not in mine}
                if others and (iid != "ALL"):
                    in_year[prow[u]["year"]] += 1
                    for n in others.values():
                        inflow[n] += 1
        tin, tout = sum(in_year.values()), sum(out_year.values())
        # Indian co-authorship partners
        part = defaultdict(lambda: [0, 0])
        for r in ps:
            for k, n in P[r["id"]]["indian"].items():
                if k not in mine:
                    part[n][0] += 1
                    part[n][1] += r["citations"]
        partners = []
        for n, (sp, tc) in sorted(part.items(), key=lambda x: -x[1][0])[:40]:
            cl = gp.cluster_of(n)
            j = jac.get((nm, n))
            partners.append({"partner_inst": n, "shared_papers": sp, "total_citations": tc, "partner_cluster": cl,
                             "cross_cluster": f"IIT <-> {cl}" if cl != "IIT" else "",
                             "citations_received_from_partner": inflow.get(n, 0),
                             "citations_given_to_partner": outflow.get(n, 0),
                             "topic_jaccard": None if j is None or j != j else round(float(j), 3)})
        detail[nm] = {
            "papers": len(ps), "journal_papers": len(js), "conference_papers": len(cs),
            "citations": sum(r["citations"] for r in ps),
            "trend_journal": [sum(1 for r in js if r["year"] == y) for y in YEARS],
            "trend_conference": [sum(1 for r in cs if r["year"] == y) for y in YEARS],
            "quartiles": {k: qc.get(k, 0) for k in ["Q1", "Q2", "Q3", "Q4", "Unranked"]},
            "core": {k: cc_.get(k, 0) for k in ["A*", "A", "B", "C", "Unranked"]},
            "fields": [{"name": n, "papers": c} for n, c in fields.most_common(12)],
            "most_cited": [{"title": r["title"], "journal": r["venue"], "year": r["year"], "citations": r["citations"],
                            "doi": r["doi"], "n_authors": r["n_authors"]} for r in top_cited],
            "flow": {"in": [in_year.get(y, 0) for y in YEARS], "out": [out_year.get(y, 0) for y in YEARS],
                     "in_total": tin, "out_total": tout, "impact_ratio": round(tin / tout, 3) if tout else None,
                     "top_citing": [{"name": n, "citations": c} for n, c in inflow.most_common(10)]},
            "partners": partners, "n_partners": len(part),
            "impact": impact_block(ps),
        }

    # citation network picture: most influential papers plus the papers citing them
    ranked = [n for n, _ in sorted(pr.items(), key=lambda x: -x[1])]
    picked, seen = [], set()
    for seed in ranked:
        if len(picked) >= 300:
            break
        if CG.in_degree(seed) == 0 or seed in seen:
            continue
        for n in [seed] + sorted(CG.predecessors(seed), key=lambda n: -pr[n])[:12]:
            if n not in seen and len(picked) < 300:
                seen.add(n)
                picked.append(n)
    citviz = {"nodes": [{"id": n, "label": prow[n]["title"][:90],
                         "inst": INST[prow[n]["our_insts"][0]] if prow[n]["our_insts"] else "",
                         "multi": len(prow[n]["our_insts"]) > 1, "year": prow[n]["year"], "pr": pr[n],
                         "indeg": indeg[n], "cites": prow[n]["citations"], "doi": prow[n]["doi"]} for n in picked],
              "edges": [{"s": u, "t": v} for u, v in CG.edges() if u in seen and v in seen]}

    # verification statistics
    orcid = Counter()
    for pid, aid, nm, iid, _ in S["author_rows"]:
        if (aid, iid) in fac:
            for a in P[pid]["authorships"]:
                if gp.short((a.get("author") or {}).get("id")) == aid:
                    orcid[bool((a.get("author") or {}).get("orcid"))] += 1
    verify = {"listed": len(fl), "matched_people": len(persons), "profiles": len(fac),
              "multi_profile_people": sum(1 for v in persons.values() if len(v["profiles"]) > 1),
              "faculty_authorships_with_orcid": round(orcid[True] / max(1, sum(orcid.values())), 3),
              "papers_all": len(prow), "papers_with_faculty": sum(1 for r in prow.values() if r["faculty"]),
              "journal_if_coverage": round(sum(1 for r in prow.values() if r["type"] == "journal" and r["if"] is not None)
                                           / max(1, sum(1 for r in prow.values() if r["type"] == "journal")), 3)}

    # every paper of every listed faculty member, for the dashboard's author pages
    fac_keys = list(fdf["person"])
    fac_ix = {k: i for i, k in enumerate(fac_keys)}
    pids_all = sorted(set().union(*person_papers.values()), key=lambda x: (-prow[x]["year"], -prow[x]["citations"]))
    pix = {x: i for i, x in enumerate(pids_all)}
    TCODE = {"journal": "j", "conference": "c"}
    papers_out = []
    for x in pids_all:
        r = prow[x]
        papers_out.append([r["title"], r["year"], r["venue"] or "", TCODE.get(r["type"], "o"),
                           (r["doi"] or "").replace("https://doi.org/", ""), r["citations"], r["quartile"] or "",
                           round(r["if"], 2) if r["if"] is not None else None, r["n_authors"],
                           sorted(fac_ix[k] for k in r["faculty"])])
    author_papers = {k: sorted(pix[x] for x in person_papers[k]) for k in fac_keys if person_papers[k]}

    data = {"meta": {"years": YEARS, "mega": MEGA, "generated": pd.Timestamp.today().strftime("%Y-%m-%d"),
                     "verify": verify},
            "overview": overview, "trend": trend,
            "faculty": fdf.drop(columns=["person"]).assign(key=fdf["person"]).to_dict("records"),
            "departments": ddf.to_dict("records"), "top30": top30, "freq_journals": freq_j,
            "coauth": coauth, "instnet": instnet, "instnet_all": instnet_all, "temporal": temporal,
            "citnet": citnet, "detail": detail, "citviz": citviz, "citers": cdf.to_dict("records"),
            "citers_summary": grp.reset_index().to_dict("records"),
            "big_papers": [{"title": r["title"], "year": r["year"], "journal": r["venue"],
                            "authors": "100+" if r["n_authors"] >= HYPER else r["n_authors"],
                            "citations": r["citations"], "doi": r["doi"],
                            "faculty": [persons[x]["name"] for x in r["faculty"]][:4],
                            "fk": r["faculty"][:4]} for r in big[:60]],
            "big_share": big_share,
            "flagged_faculty": flagged_fac.drop(columns=["person"]).assign(key=flagged_fac["person"]).to_dict("records"),
            "papers": papers_out, "author_papers": author_papers}
    imp_rows = []
    for nm_, dv in detail.items():
        im_ = dv["impact"]
        for k_ in im_["kinds"]:
            imp_rows.append({"scope": nm_, "group_by": "collaboration type (<10 authors)", "group": k_["kind"], **{x: k_[x] for x in ("papers", "cites_per_paper", "citation_index", "q1_share")}})
        for k_ in im_["sizes"]:
            imp_rows.append({"scope": nm_, "group_by": "number of authors", "group": k_["size"], **{x: k_[x] for x in ("papers", "cites_per_paper", "citation_index", "q1_share")}})
        for t_ in ("journal", "conference"):
            imp_rows.append({"scope": nm_, "group_by": "venue type", "group": t_, **im_["venue"][t_]})
        for q_ in ("Q1", "Q2", "Q3", "Q4"):
            imp_rows.append({"scope": nm_, "group_by": "journal quartile", "group": q_, **im_["quartile"][q_]})
        for f_ in im_["fields"]:
            imp_rows.append({"scope": nm_, "group_by": "field", "group": f_["field"], **{x: f_[x] for x in ("papers", "cites_per_paper", "citation_index", "q1_share")},
                             "international_share": f_["international_share"], "growth_2016_2025": f_["growth"]})
    pd.DataFrame(imp_rows).to_csv(OUT / "collaboration_impact.csv", index=False)
    from insights import make_insights
    data["insights"] = make_insights(data)
    (OUT / "phase2_data.json").write_text(json.dumps(data, default=lambda o: None if o != o else str(o)))
    tpl = (HERE / "phase2_template.html").read_text(encoding="utf-8") if (HERE / "phase2_template.html").exists() else None
    if tpl:
        (HERE / "out" / "group6_dashboard.html").write_text(
            tpl.replace("__PHASE2_DATA__", json.dumps(data, default=lambda o: None if o != o else str(o)).replace("</", "<\\/")),
            encoding="utf-8")
    log("overview:", pd.DataFrame(overview).to_string())
    log("verify:", verify)
    log("co-authorship:", {k: v for k, v in coauth.items() if k not in ("nodes", "edges")})
    log("institutional:", {k: v for k, v in instnet.items() if k not in ("nodes", "edges", "top_countries")})
    log("citation:", {k: citnet[k] for k in ("nodes", "edges", "cross_institute_edges")})
    log("private vs govt:\n", grp.to_string())
    log("flagged faculty:", len(flagged_fac), "| 10+ author papers:", len(big))


if __name__ == "__main__":
    main()
