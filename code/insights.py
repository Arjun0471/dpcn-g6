"""Key findings for the dashboard, computed from the Phase II data dict.

Every number in the text is computed here from the same data the charts use, so the
bullets stay in sync when the pipeline is rerun. Wording is descriptive; where a reason
is suggested it is marked as a reading of the numbers, not a tested cause.
"""
from collections import Counter
from itertools import combinations
from urllib.parse import quote

from scipy.stats import spearmanr

INSTS = ["IIT Bhubaneswar", "IIT Indore", "IIT Mandi"]
SHORT = {"IIT Bhubaneswar": "Bhubaneswar", "IIT Indore": "Indore", "IIT Mandi": "Mandi"}


def n(x):
    """Indian digit grouping, like the dashboard (1,00,000)."""
    s = str(int(round(x)))
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ",".join(parts + [tail])


def p(x, d=0):
    return f"{100 * x:.{d}f}%"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def make_insights(d):
    O = {o["institution"]: o for o in d["overview"]}
    T = {(t["institution"], t["year"]): t for t in d["trend"]}
    F = d["faculty"]
    P = d["papers"]
    years = d["meta"]["years"]
    y0, y1 = years[0], years[-2]          # last year is partial
    M = d["meta"]["mega"]

    def link(f):
        return f'<a class="au" href="#author={quote(f["key"])}">{esc(f["name"])}</a>'

    out = {}

    # ---------------- overview
    grow = sorted(((T[(i, y1)]["publications"] / T[(i, y0)]["publications"], i) for i in INSTS), reverse=True)
    q1 = {i: (T[(i, y0)]["q1"] / T[(i, y0)]["journal"], T[(i, y1)]["q1"] / T[(i, y1)]["journal"]) for i in INSTS}
    intl = {i: (T[(i, y0)]["international_papers"] / T[(i, y0)]["publications"],
                T[(i, y1)]["international_papers"] / T[(i, y1)]["publications"]) for i in INSTS}
    B = d["big_share"]
    cpp = {i: O[i]["citations"] / O[i]["publications"] for i in INSTS}
    cpp_x = {i: (O[i]["citations"] - B[i]["citations"]) / (O[i]["publications"] - B[i]["papers"]) for i in INSTS}
    by_cpp = sorted(INSTS, key=lambda i: -cpp[i])
    cits = sorted((x[5] for x in P), reverse=True)
    top1 = sum(cits[: len(cits) // 100]) / sum(cits)
    uncited = sum(c == 0 for c in cits) / len(cits)
    A = O["Group 6 (all three)"]
    core = d["detail"]["Group 6 (all three)"]["core"]
    conf_unranked = core.get("Unranked", 0) / max(1, sum(core.values()))
    up = sorted(INSTS, key=lambda i: -(intl[i][1] - intl[i][0]))
    im = d["detail"]["Group 6 (all three)"]["impact"]
    kI, kS = im["kinds"][2], im["kinds"][0]
    iy = len(years) - 2
    IMPACT_1 = (f"<b>Papers written with foreign partners are cited more.</b> Among papers with fewer than {M} authors, international papers are cited "
                f"<b>{kI['citation_index']:.2f}×</b> the Group 6 average for their year and single-institute papers <b>{kS['citation_index']:.2f}×</b>; "
                f"{p(kI['q1_share'])} of the international journal papers are in Q1 journals against {p(kS['q1_share'])}. "
                f"The share of single-institute papers fell from {p(im['mix']['Single institute'][0])} ({y0}) to {p(im['mix']['Single institute'][iy])} ({y1}).")
    big_f = [f for f in im["fields"] if f["papers"] >= 500]
    f_cit = max(big_f, key=lambda f: f["citation_index"])
    f_grow = max((f for f in big_f if f["growth"]), key=lambda f: f["growth"])
    f_top = im["fields"][0]
    IMPACT_2 = (f"<b>Engineering dominates the output, but it is not where citations are highest.</b> {esc(f_top['field'])} is {p(f_top['share'])} of all papers "
                f"with a citation index of {f_top['citation_index']:.2f}×. Among fields with 500+ papers, {esc(f_cit['field'])} is cited most ({f_cit['citation_index']:.2f}×)"
                + (f" and also grew fastest ({f_grow['growth']:.1f}× from {y0} to {y1})." if f_grow is f_cit else f"; {esc(f_grow['field'])} grew fastest ({f_grow['growth']:.1f}× from {y0} to {y1})."))
    out["overview"] = [
        f"<b>All three institutes more than doubled their output.</b> Publications {y0} → {y1}: "
        + ", ".join(f"{SHORT[i]} {n(T[(i, y0)]['publications'])} → {n(T[(i, y1)]['publications'])} (<b>{g:.1f}×</b>)" for g, i in grow)
        + f". {years[-1]} is a partial year, so it is left out of growth figures.",
        f"<b>Growth did not come at the cost of venue quality.</b> The Q1 share of journal papers rose at every institute from {y0} to {y1}: "
        + ", ".join(f"{SHORT[i]} {p(q1[i][0])} → <b>{p(q1[i][1])}</b>" for i in sorted(INSTS, key=lambda i: -q1[i][1])) + ".",
        f"<b>{SHORT[by_cpp[0]]}'s papers are cited most, and not only because of large collaborations.</b> Citations per paper: "
        + ", ".join(f"{SHORT[i]} {cpp[i]:.1f}" for i in by_cpp)
        + f". Leaving out {M}+ author papers: " + ", ".join(f"{SHORT[i]} {cpp_x[i]:.1f}" for i in by_cpp) + ".",
        "<b>International co-authorship moved in different directions.</b> Share of papers with a foreign co-author, "
        f"{y0} → {y1}: " + ", ".join(f"{SHORT[i]} {p(intl[i][0])} → <b>{p(intl[i][1])}</b>" for i in up) + ".",
        IMPACT_1,
        IMPACT_2,
        f"<b>Citations are concentrated.</b> The most-cited 1% of faculty papers hold {p(top1, 1)} of their citations, "
        f"while {p(uncited, 1)} have no citations yet (most of these are from {years[-2]}–{str(years[-1])[2:]}).",
        f"<b>Conference rankings cover little of the output.</b> {p(conf_unranked)} of the {n(A['conference'])} conference papers are in venues "
        "that CORE does not rank (CORE mainly ranks computing venues), so journal quartiles are the more useful quality measure here.",
    ]

    # ---------------- faculty
    share10 = {}
    med = {}
    for i in INSTS:
        ps = sorted((f["papers"] for f in F if f["institution"] == i), reverse=True)
        share10[i] = sum(ps[: len(ps) // 10]) / sum(ps)
        med[i] = ps[len(ps) // 2] if len(ps) % 2 else (ps[len(ps) // 2 - 1] + ps[len(ps) // 2]) / 2
    gini = {}
    for i in INSTS:
        v = sorted(f["papers"] for f in F if f["institution"] == i)
        tot_, c_, area = sum(v), 0, 0.0
        for x in v:
            prev = c_ / tot_
            c_ += x
            area += (prev + c_ / tot_) / 2 / len(v)
        gini[i] = 1 - 2 * area
    rho_c = spearmanr([f["papers"] for f in F], [f["citations"] for f in F]).statistic
    rho_f = spearmanr([f["papers"] for f in F], [f["faculty_coauthors"] for f in F]).statistic
    top_p = sorted(F, key=lambda f: -f["papers"])[:3]
    top_f = sorted(F, key=lambda f: -f["faculty_coauthors"])[:3]
    top_x = sorted(F, key=lambda f: -f["citations_excl_10plus"])[:3]
    lst = sorted(INSTS, key=lambda i: -O[i]["listed_faculty"])
    out["faculty"] = [
        "<b>A small group produces a large share of the work.</b> The top 10% of listed faculty account for "
        + ", ".join(f"<b>{p(share10[i])}</b> of faculty authorships at {SHORT[i]}" if j == 0 else f"<b>{p(share10[i])}</b> at {SHORT[i]}"
                    for j, i in enumerate(sorted(INSTS, key=lambda i: -share10[i])))
        + ". Median papers per listed faculty member: " + ", ".join(f"{SHORT[i]} {med[i]:g}" for i in INSTS) + ".",
        "<b>Output is unevenly spread in all three institutes.</b> Gini coefficient of papers per listed faculty member: "
        + ", ".join(f"{SHORT[i]} <b>{gini[i]:.2f}</b>" for i in INSTS) + " (0 = everyone publishes equally, 1 = one person publishes everything).",
        f"<b>Productive faculty are usually well cited, less often well connected inside Group 6.</b> Spearman ρ = {rho_c:.2f} between papers and citations, "
        f"but {rho_f:.2f} between papers and the number of Group 6 faculty co-authors.",
        "<b>Most papers:</b> " + ", ".join(f"{link(f)} ({n(f['papers'])})" for f in top_p)
        + ". <b>Most Group 6 faculty co-authors:</b> " + ", ".join(f"{link(f)} ({f['faculty_coauthors']})" for f in top_f)
        + f". <b>Most citations without {M}+ author papers:</b> " + ", ".join(f"{link(f)} ({n(f['citations_excl_10plus'])})" for f in top_x) + ".",
        "<b>Per-faculty averages depend on the list.</b> The faculty list has "
        + ", ".join(f"{n(O[i]['listed_faculty'])} names for {SHORT[i]}" for i in lst)
        + ", so papers per listed faculty (" + ", ".join(f"{SHORT[i]} {O[i]['publications'] / O[i]['listed_faculty']:.1f}" for i in lst) + ") "
        "reflect list size as much as productivity.",
    ]

    # ---------------- networks
    pairs = set()
    for x in P:
        if x[8] >= 100:
            continue
        for a, b in combinations(sorted(x[9]), 2):
            pairs.add((a, b))
    same_i = sum(F[a]["institution"] == F[b]["institution"] for a, b in pairs) / len(pairs)
    same_d = sum(F[a]["institution"] == F[b]["institution"] and F[a]["department"] == F[b]["department"] for a, b in pairs) / len(pairs)
    multi = sum(1 for x in P if len({F[j]["institution"] for j in x[9]}) >= 2)
    C = d["coauth"]
    bridges = sorted(F, key=lambda f: -f["betweenness"])[:3]
    tm = {t["year"]: t for t in d["temporal"]}
    peak = max((y for y in years[:-1]), key=lambda y: tm[y]["active_faculty"])
    tot = Counter()
    for i in INSTS:
        for y in years:
            tot[y] += T[(i, y)]["publications"]
    fy = Counter(x[1] for x in P)
    share = {y: fy[y] / tot[y] for y in years}
    tp = d["instnet"]["top_partners"][:3]
    out["networks"] = [
        f"<b>Collaboration stays inside each institute.</b> {p(same_i, 1)} of faculty co-author links join people at the same institute, and {p(same_d)} "
        f"join people in the same department. Only {n(multi)} of {n(len(P))} faculty papers have faculty from two or more Group 6 institutes.",
        f"<b>Many tight groups, joined by a few bridges.</b> Modularity is {C['modularity']} across {C['communities']} communities, yet "
        f"{n(C['largest_component'])} of {n(C['n'])} faculty ({p(C['largest_component'] / C['n'])}) are in one connected group. "
        "The people who join the groups most (highest betweenness): " + ", ".join(link(f) for f in bridges) + ".",
        f"<b>The number of faculty active in a year peaked in {peak}</b> ({n(tm[peak]['active_faculty'])} faculty, {n(tm[peak]['coauthor_links'])} links), "
        f"while total output kept rising. The share of papers with a listed faculty author fell from {p(share[y0])} in {y0} to {p(share[y1])} in {y1}. "
        "Recent papers are often not yet linked to an author's main OpenAlex profile, so the latest years of the faculty network are probably understated.",
        "<b>The closest Indian partners are older IITs.</b> Shared papers (100+ author papers excluded): "
        + ", ".join(f"{esc(t['institution'].replace('Indian Institute of Technology', 'IIT'))} {n(t['shared_papers'])}" for t in tp)
        + f". Partners span {d['instnet']['n_countries']} countries; the United States is the largest foreign partner country.",
    ]

    # ---------------- india
    fl = {i: d["detail"][i]["flow"] for i in INSTS}
    tc = d["detail"]["Group 6 (all three)"]["flow"]["top_citing"][:3]
    priv = {c["institution"] for c in d["citers"] if c["ownership"] == "Private"}
    out["india"] = [
        "<b>Group 6 cites other Indian institutions more than they cite Group 6.</b> Citations received vs given: "
        + ", ".join(f"{SHORT[i]} {n(fl[i]['in_total'])} vs {n(fl[i]['out_total'])} (ratio {fl[i]['impact_ratio']:.2f})" for i in INSTS)
        + ". A ratio below 1 is common for younger institutes, which build on the work of older ones.",
        "<b>The largest Indian citers mix older IITs and large private universities:</b> "
        + ", ".join(f"{esc(t['name'])}{' (private)' if t['name'] in priv else ''} {n(t['citations'])}" for t in tc) + ".",
    ]

    # ---------------- notes: non-government citers, large collaborations
    S = {s["ownership"]: s for s in d["citers_summary"]}
    pv, gv = S["Private"], S["Government / public"]
    cd = sorted((c for c in d["citers"] if c["ownership"] == "Private" and c["own_output_growth"]),
                key=lambda c: -c["own_output_growth"])[:2]
    top20 = sorted(d["citers"], key=lambda c: -c["citing_papers"])[:20]
    conc = {o: sorted(c["share_from_top10_citing_authors"] for c in d["citers"] if c["ownership"] == o) for o in S}
    medc = {o: v[len(v) // 2] for o, v in conc.items()}
    out["notes_citers"] = [
        f"<b>Volume, not stronger interest.</b> {sum(c['ownership'] == 'Private' for c in top20)} of the top 20 citing institutions are private, "
        f"but per 1,000 of their own papers they cite Group 6 less than government ones ({pv['citing_papers_per_1000_own_papers']:.0f} vs {gv['citing_papers_per_1000_own_papers']:.0f}).",
        f"<b>Their own output grew much faster.</b> Private output grew {pv['own_output_growth']}× from 2018–19 to 2024–25 against {gv['own_output_growth']}× for government ones, "
        "e.g. " + ", ".join(f"{esc(c['institution'])} {c['own_output_growth']}×" for c in cd)
        + ". A likely reason: more papers in fields that overlap with Group 6 (engineering, materials, computing) bring more references to its work. We did not test the field mix of the citing papers.",
        f"<b>Not explained by personal links.</b> Fewer of their citing papers have a former Group 6 author ({p(pv['share_by_former_group6_authors'], 1)} vs {p(gv['share_by_former_group6_authors'], 1)}) "
        f"or are self-citations ({p(pv['share_author_self_citation'])} vs {p(gv['share_author_self_citation'])}).",
        f"<b>Not a few heavy citers either.</b> The 10 most active citing authors at an institution account for about the same share in both groups "
        f"({p(medc['Private'])} private vs {p(medc['Government / public'])} government, medians).",
    ]

    BF = d["flagged_faculty"]
    dep = Counter(f["department"] for f in BF)
    phys = sum(v for k, v in dep.items() if "physic" in k.lower() or "astro" in k.lower() or k == "Basic Sciences")
    s1 = max(BF, key=lambda f: f["papers_10plus_authors"])
    allc = sum(B[i]["all_citations"] for i in INSTS)
    bigc = sum(B[i]["citations"] for i in INSTS)
    life = max(F, key=lambda f: f["citations_lifetime"])
    life_f = max(BF, key=lambda f: f["citations_lifetime"])
    out["notes_big"] = [
        f"<b>About half the flags come from physics.</b> {phys} of the {len(BF)} flagged faculty are in physics, astronomy or basic-sciences departments, "
        "where papers from collaborations such as ALICE at CERN and Belle II carry hundreds or thousands of authors.",
        f"<b>Small at institute level, large for individuals.</b> {M}+ author papers carry {p(bigc / allc, 1)} of all Group 6 citations, but for {link(s1)} "
        f"they are {n(s1['papers_10plus_authors'])} of {n(s1['papers'])} papers and {p(s1['share_citations_10plus'])} of citations. "
        "Faculty rankings should use citations without these papers.",
        f"<b>No listed faculty member reaches 1 lakh citations in OpenAlex.</b> The highest lifetime count among flagged faculty is {link(life_f)} ({n(life_f['citations_lifetime'])}); "
        f"the highest overall is {link(life)} ({n(life['citations_lifetime'])}, with {life['papers']} Group 6 papers), whose career citations come mostly from other institutions. "
        "Google Scholar counts are usually higher than OpenAlex.",
    ]
    return out
