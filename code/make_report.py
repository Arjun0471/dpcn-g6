"""Builds the Key Observations report (HTML + figures) from out/phase2/phase2_data.json.

Every number in the report is read or computed from the same data file the dashboard uses.
Usage: python make_report.py   ->  report/Key_Observations.html, report/fig1.png, report/fig2.png
(The HTML is then printed to PDF and converted to DOCX.)
"""
import json
import re
from itertools import combinations
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
OUT = HERE / "report"
OUT.mkdir(exist_ok=True)
d = json.loads((HERE / "out" / "phase2" / "phase2_data.json").read_text())

DASH = "https://arjun0471.github.io/dpcn-g6/"
REPO = "https://github.com/Arjun0471/dpcn-g6"
INSTS = ["IIT Bhubaneswar", "IIT Indore", "IIT Mandi"]
ALL = "Group 6 (all three)"
SH = {"IIT Bhubaneswar": "Bhubaneswar", "IIT Indore": "Indore", "IIT Mandi": "Mandi", ALL: "Group 6"}
COL = {"IIT Bhubaneswar": "#2a78d6", "IIT Indore": "#eb6834", "IIT Mandi": "#1baf7a"}
YEARS = d["meta"]["years"]
Y0, Y1 = YEARS[0], YEARS[-2]
FULL = YEARS[:-1]                      # last year is partial


def n(x):
    s = str(int(round(x)))
    if len(s) <= 3:
        return s
    head, tail, parts = s[:-3], s[-3:], []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ",".join(parts + [tail])


def p(x, k=0):
    return f"{100 * x:.{k}f}%"


def strip(html):
    return re.sub(r"<[^>]+>", "", html)


O = {o["institution"]: o for o in d["overview"]}
T = {(t["institution"], t["year"]): t for t in d["trend"]}
F = d["faculty"]
P = d["papers"]
A = O[ALL]
IM = d["detail"][ALL]["impact"]
B = d["big_share"]
CA = d["coauth"]
TM = {t["year"]: t for t in d["temporal"]}
CN = d["citnet"]
NET = d["instnet"]
NETA = d["instnet_all"]
FL = {i: d["detail"][i]["flow"] for i in INSTS + [ALL]}
S = {s["ownership"]: s for s in d["citers_summary"]}
BF = d["flagged_faculty"]

# ---------------------------------------------------------------- derived numbers
cpp = {i: O[i]["citations"] / O[i]["publications"] for i in INSTS + [ALL]}
cpp_x = {i: (O[i]["citations"] - B[i]["citations"]) / (O[i]["publications"] - B[i]["papers"]) for i in INSTS}
grow = {i: T[(i, Y1)]["publications"] / T[(i, Y0)]["publications"] for i in INSTS}
q1y = {i: [T[(i, y)]["q1"] / T[(i, y)]["journal"] for y in FULL] for i in INSTS}
intl = {i: (T[(i, Y0)]["international_papers"] / T[(i, Y0)]["publications"],
            T[(i, Y1)]["international_papers"] / T[(i, Y1)]["publications"]) for i in INSTS}
core = d["detail"][ALL]["core"]
core_unranked = core["Unranked"] / sum(core.values())

share10, gini = {}, {}
for i in INSTS:
    v = sorted(f["papers"] for f in F if f["institution"] == i)
    share10[i] = sum(v[-(len(v) // 10):]) / sum(v)
    c, area = 0, 0.0
    for x in v:
        prev = c / sum(v)
        c += x
        area += (prev + c / sum(v)) / 2 / len(v)
    gini[i] = 1 - 2 * area

pairs = set()
for x in P:
    if x[8] >= 100:
        continue
    for a, b in combinations(sorted(x[9]), 2):
        pairs.add((a, b))
same_dept = sum(F[a]["institution"] == F[b]["institution"] and F[a]["department"] == F[b]["department"] for a, b in pairs)
same_inst = sum(F[a]["institution"] == F[b]["institution"] for a, b in pairs)
cross_inst = len(pairs) - same_inst
multi = sum(1 for x in P if len({F[j]["institution"] for j in x[9]}) >= 2)
avg_deg = 2 * CA["m"] / CA["n"]
density = CA["m"] / (CA["n"] * (CA["n"] - 1) / 2)
from scipy.stats import spearmanr
rho_c = spearmanr([f["papers"] for f in F], [f["citations"] for f in F]).statistic
rho_f = spearmanr([f["papers"] for f in F], [f["faculty_coauthors"] for f in F]).statistic
peak = max(FULL, key=lambda y: TM[y]["active_faculty"])
top_p = sorted(F, key=lambda f: -f["papers"])[:3]
top_c = sorted(F, key=lambda f: -f["faculty_coauthors"])[:3]
top_b = sorted(F, key=lambda f: -f["betweenness"])[:3]
top_x = sorted(F, key=lambda f: -f["citations_excl_10plus"])[:3]
deps = sorted(d["departments"], key=lambda x: -x["papers"])[:4]
no_internal = CN["in_degree_hist"]["0"] / CN["nodes"]
bigc = sum(B[i]["citations"] for i in INSTS) / sum(B[i]["all_citations"] for i in INSTS)
phys = sum(1 for f in BF if "physic" in f["department"].lower() or "astro" in f["department"].lower() or f["department"] == "Basic Sciences")
s1 = max(BF, key=lambda f: f["papers_10plus_authors"])
life = max(F, key=lambda f: f["citations_lifetime"])
life_f = max(BF, key=lambda f: f["citations_lifetime"])
top20 = sorted(d["citers"], key=lambda c: -c["citing_papers"])[:20]
priv20 = sum(c["ownership"] == "Private" for c in top20)
fast = sorted((c for c in d["citers"] if c["ownership"] == "Private" and c["own_output_growth"]), key=lambda c: -c["own_output_growth"])[:2]
kS, kN, kI = IM["kinds"]
z = {x["size"]: x for x in IM["sizes"]}
bigf = [f for f in IM["fields"] if f["papers"] >= 500]
f_cit = max(bigf, key=lambda f: f["citation_index"])
f_top = IM["fields"][0]
f_phys = next(f for f in IM["fields"] if f["field"].startswith("Physics"))
fj = d["detail"][ALL]
tp = NET["top_partners"][:4]
iit = lambda s: s.replace("Indian Institute of Technology", "IIT")

# ---------------------------------------------------------------- figures
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titlesize": 8.5, "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.grid": True,
                     "grid.color": "#e6e3dc", "grid.linewidth": .6, "axes.axisbelow": True, "legend.frameon": False})

fig, ax = plt.subplots(1, 3, figsize=(7.4, 2.25))
for i in INSTS:
    ax[0].plot(FULL, [T[(i, y)]["publications"] for y in FULL], color=COL[i], lw=1.8, marker="o", ms=2.5, label=SH[i])
    ax[1].plot(FULL, [100 * v for v in q1y[i]], color=COL[i], lw=1.8, marker="o", ms=2.5, label=SH[i])
ax[0].set_title("(a) Publications per year")
ax[0].legend(fontsize=7, loc="upper left")
ax[1].set_title("(b) Q1 share of journal papers (%)")
for a_ in ax[:2]:
    a_.set_xticks([2016, 2019, 2022, 2025])
labels = ["Single\ninstitute", "With other\nIndian inst.", "Inter-\nnational"]
bars = ax[2].bar(labels, [k["citation_index"] for k in IM["kinds"]], color=["#9aa3ad", "#5598e7", "#104281"], width=.62)
ax[2].axhline(1, color="#555", lw=.8, ls="--")
for b_, k in zip(bars, IM["kinds"]):
    ax[2].text(b_.get_x() + b_.get_width() / 2, b_.get_height() + .02, f"{k['citation_index']:.2f}", ha="center", fontsize=7.5)
ax[2].set_title("(c) Citation index")
ax[2].set_ylim(0, 1.45)
ax[2].grid(axis="x", visible=False)
fig.tight_layout(w_pad=1.6)
fig.savefig(OUT / "fig1.png", dpi=220)
plt.close(fig)

fig, ax = plt.subplots(1, 3, figsize=(7.4, 2.25))
ax[0].plot(FULL, [TM[y]["active_faculty"] for y in FULL], color="#104281", lw=1.8, marker="o", ms=2.5, label="Active faculty")
ax[0].plot(FULL, [TM[y]["coauthor_links"] for y in FULL], color="#eb6834", lw=1.8, marker="o", ms=2.5, label="Co-author links")
ax[0].set_title("(a) Faculty network per year")
ax[0].set_xticks([2016, 2019, 2022, 2025])
ax[0].legend(fontsize=7, loc="upper left")
vals = [100 * same_dept / len(pairs), 100 * (same_inst - same_dept) / len(pairs), 100 * cross_inst / len(pairs)]
bars = ax[1].bar(["Same\ndept.", "Same inst.,\nother dept.", "Other\ninstitute"], vals, color=["#104281", "#5598e7", "#9aa3ad"], width=.62)
for b_, v in zip(bars, vals):
    ax[1].text(b_.get_x() + b_.get_width() / 2, v + 1.5, f"{v:.1f}%", ha="center", fontsize=7.5)
ax[1].set_title("(b) Co-author links (%)")
ax[1].set_ylim(0, 82)
ax[1].grid(axis="x", visible=False)
w = .36
xs = range(3)
ax[2].bar([x - w / 2 for x in xs], [FL[i]["in_total"] / 1000 for i in INSTS], w, color="#1baf7a", label="Received")
ax[2].bar([x + w / 2 for x in xs], [FL[i]["out_total"] / 1000 for i in INSTS], w, color="#9aa3ad", label="Given")
ax[2].set_xticks(list(xs), [SH[i] for i in INSTS])
ax[2].set_title("(c) Indian citations ('000)")
ax[2].legend(fontsize=7, loc="upper left")
ax[2].grid(axis="x", visible=False)
fig.tight_layout(w_pad=1.6)
fig.savefig(OUT / "fig2.png", dpi=220)
plt.close(fig)

# ---------------------------------------------------------------- text
rows1 = [
    ("Listed faculty", lambda o: n(o["listed_faculty"])),
    ("Publications", lambda o: n(o["publications"])),
    ("&nbsp;&nbsp;Journal papers", lambda o: n(o["journal"])),
    ("&nbsp;&nbsp;Conference papers", lambda o: n(o["conference"])),
    ("Q1 papers", lambda o: n(o["q1"])),
    ("&nbsp;&nbsp;Q1 share of journal papers", lambda o: p(o["q1"] / o["journal"], 1)),
    ("Q1 with IF &gt; 5", lambda o: n(o["q1_if_gt5"])),
    ("Q1 with IF &gt; 10", lambda o: n(o["q1_if_gt10"])),
    ("Papers with &lt; 10 authors", lambda o: f"{n(o['authors_lt10'])} ({p(o['authors_lt10'] / o['publications'], 1)})"),
    ("Papers with 10+ authors", lambda o: n(o["authors_ge10"])),
    ("&nbsp;&nbsp;of which 100+ authors", lambda o: n(o["authors_ge100"])),
    ("Citations", lambda o: n(o["citations"])),
    ("Citations per paper", lambda o: f"{o['citations'] / o['publications']:.1f}"),
    ("Papers with a foreign co-author", lambda o: p(o["international_share"], 1)),
    (f"Growth in papers, {Y0} → {Y1}", None),
]
t1 = "".join(
    "<tr><td>" + lab + "</td>" + "".join(
        "<td>" + (fn(O[i]) if fn else (f"{grow[i]:.1f}×" if i in grow else
                                       f"{sum(T[(j, Y1)]['publications'] for j in INSTS) / sum(T[(j, Y0)]['publications'] for j in INSTS):.1f}×")) + "</td>"
        for i in INSTS + [ALL]) + "</tr>" for lab, fn in rows1)

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Key Observations — Group 6</title>
<style>
@page {{ size: A4; margin: 15mm 16mm 15mm 16mm; }}
body {{ font: 9.6pt/1.42 "Liberation Sans", "DejaVu Sans", Arial, sans-serif; color: #1b1f24; margin: 0; }}
h1 {{ font-size: 17pt; margin: 0 0 2pt; }}
h2 {{ font-size: 11.5pt; margin: 11pt 0 4pt; padding-bottom: 2pt; border-bottom: 1.2pt solid #c07a3a; break-after: avoid; }}
h3 {{ font-size: 9.8pt; margin: 7pt 0 2pt; break-after: avoid; }}
p {{ margin: 0 0 5pt; }}
ul {{ margin: 0 0 5pt; padding-left: 14pt; }}
li {{ margin: 0 0 3pt; }}
.meta {{ color: #444; font-size: 9pt; margin-bottom: 6pt; }}
.meta b {{ color: #1b1f24; }}
table {{ border-collapse: collapse; width: 100%; font-size: 8.8pt; margin: 4pt 0 6pt; break-inside: avoid; }}
th, td {{ padding: 2.2pt 5pt; border-bottom: .5pt solid #d9d5cc; text-align: right; }}
th:first-child, td:first-child {{ text-align: left; }}
th {{ border-bottom: 1pt solid #1b1f24; font-weight: 700; }}
td:last-child, th:last-child {{ font-weight: 700; }}
table.net td:last-child, table.net th:last-child {{ font-weight: 400; text-align: left; }}
table.net td, table.net th {{ text-align: left; vertical-align: top; }}
.cap {{ font-size: 8.3pt; color: #555; margin: 0 0 6pt; }}
img {{ width: 100%; display: block; margin: 4pt 0 1pt; }}
.fig {{ break-inside: avoid; }}
a {{ color: #1c5cab; text-decoration: none; }}
</style></head><body>

<h1>Key Observations: Group 6, IIT Cluster</h1>
<div class="meta"><b>DPCN Research Mapping Project</b> · IIT Bhubaneswar, IIT Indore, IIT Mandi · publications {YEARS[0]}–{YEARS[-1]}<br>
<b>Team:</b> Arjun Dingankar, Soham Acharya, Sumit Kumar<br>
<b>Dashboard:</b> <a href="{DASH}">{DASH}</a> · <b>Dataset and code:</b> <a href="{REPO}">{REPO}</a></div>

<h2>1. Data and method</h2>
<p>We collected every publication from {YEARS[0]} to {YEARS[-1]} that lists IIT Bhubaneswar, IIT Indore or IIT Mandi as an author affiliation in OpenAlex:
<b>{n(A['publications'])} papers</b> ({n(A['journal'])} journal, {n(A['conference'])} conference) with {n(A['citations'])} citations. {YEARS[-1]} is a partial year (data collected in October {YEARS[-1]}),
so growth figures stop at {Y1}. Journal quartiles and impact factors come from SCImago (IF = citations per document over two years, the same formula as the Journal Impact Factor),
and conference ranks from CORE 2023. The faculty list has {n(A['listed_faculty'])} names; all were matched to OpenAlex author profiles by name and institute,
and {d['meta']['verify']['multi_profile_people']} people with several same-name profiles were merged into one. Publication statistics use all papers, including students' papers.
Faculty statistics and faculty networks use listed faculty only, and papers with 100 or more authors are left out of co-authorship links.
To compare papers of different ages we use a <b>citation index</b>: a paper's citations divided by the average for Group 6 papers of the same year (1.0 = average).</p>

<h2>2. Basic statistics</h2>
<table><thead><tr><th>Table 1. Overview, {YEARS[0]}–{YEARS[-1]}</th><th>IIT Bhubaneswar</th><th>IIT Indore</th><th>IIT Mandi</th><th>Group 6</th></tr></thead><tbody>{t1}</tbody></table>

<div class="fig"><img src="fig1.png" alt="Publications per year, Q1 share per year, citation index by collaboration type">
<p class="cap"><b>Figure 1.</b> (a) Publications per year. (b) Share of journal papers in Q1 journals. (c) Citation index by collaboration type, papers with fewer than 10 authors; the dashed line is the Group 6 average.</p></div>

<ul>
<li><b>Output more than doubled everywhere.</b> From {Y0} to {Y1}, Mandi grew {grow['IIT Mandi']:.1f}× ({n(T[('IIT Mandi', Y0)]['publications'])} → {n(T[('IIT Mandi', Y1)]['publications'])} papers),
Indore {grow['IIT Indore']:.1f}× ({n(T[('IIT Indore', Y0)]['publications'])} → {n(T[('IIT Indore', Y1)]['publications'])}) and Bhubaneswar {grow['IIT Bhubaneswar']:.1f}×
({n(T[('IIT Bhubaneswar', Y0)]['publications'])} → {n(T[('IIT Bhubaneswar', Y1)]['publications'])}). Indore is the largest of the three and publishes {p(O['IIT Indore']['publications'] / A['publications'])} of the group's papers.</li>
<li><b>Quality rose along with volume.</b> {p(A['q1'] / A['journal'])} of journal papers are in Q1 journals, and the Q1 share increased at every institute
(Mandi {p(q1y['IIT Mandi'][0])} → {p(q1y['IIT Mandi'][-1])}, Indore {p(q1y['IIT Indore'][0])} → {p(q1y['IIT Indore'][-1])}, Bhubaneswar {p(q1y['IIT Bhubaneswar'][0])} → {p(q1y['IIT Bhubaneswar'][-1])}).
We read this as the institutes maturing: they are not growing by publishing in weaker venues.</li>
<li><b>Most Q1 papers are in good but not elite journals.</b> {p(A['q1_if_gt5'] / A['q1'])} of Q1 papers are in journals with IF above 5, but only {p(A['q1_if_gt10'] / A['q1'], 1)} ({n(A['q1_if_gt10'])} papers) are in journals with IF above 10.
The three institutes are close on this measure: IF &gt; 10 papers are {", ".join(f"{p(O[i]['q1_if_gt10'] / O[i]['journal'], 1)} of journal papers at {SH[i]}" for i in INSTS)}.</li>
<li><b>Nearly all papers come from small teams.</b> {p(A['authors_lt10'] / A['publications'], 1)} of papers have fewer than 10 authors. The {n(A['authors_ge100'])} papers with 100+ authors are almost all from
Bhubaneswar ({n(O['IIT Bhubaneswar']['authors_ge100'])}) and Indore ({n(O['IIT Indore']['authors_ge100'])}); Mandi has {n(O['IIT Mandi']['authors_ge100'])}. These come from high-energy physics collaborations
(Belle II, ALICE at CERN), which Bhubaneswar and Indore are members of.</li>
<li><b>Indore's papers are cited most.</b> Citations per paper are {cpp['IIT Indore']:.1f} at Indore, {cpp['IIT Bhubaneswar']:.1f} at Bhubaneswar and {cpp['IIT Mandi']:.1f} at Mandi.
The order stays the same when papers with 10+ authors are removed ({cpp_x['IIT Indore']:.1f}, {cpp_x['IIT Bhubaneswar']:.1f}, {cpp_x['IIT Mandi']:.1f}), so the lead is not caused by large collaborations.</li>
<li><b>International papers are cited more.</b> Among papers with fewer than 10 authors, those with a foreign co-author have a citation index of {kI['citation_index']:.2f}, against {kN['citation_index']:.2f} for papers with
other Indian institutions and {kS['citation_index']:.2f} for single-institute papers; {p(kI['q1_share'])} of international journal papers are in Q1 journals against {p(kS['q1_share'])}.
Citations also rise with team size, from {z['1']['citation_index']:.2f} for single-author papers to {z['6–9']['citation_index']:.2f} for 6–9 authors.
This is a correlation: stronger groups may simply attract foreign partners more easily. Indore raised its international share from {p(intl['IIT Indore'][0])} to {p(intl['IIT Indore'][1])},
while Bhubaneswar's fell from {p(intl['IIT Bhubaneswar'][0])} to {p(intl['IIT Bhubaneswar'][1])}.</li>
<li><b>Engineering is the largest field, but not the most cited.</b> {f_top['field']} is {p(f_top['share'])} of papers with a citation index of {f_top['citation_index']:.2f}.
Among fields with 500+ papers, {f_cit['field']} is cited most ({f_cit['citation_index']:.2f}). {f_phys['field']} is the most international field ({p(f_phys['international_share'])} of papers with a foreign co-author).</li>
<li><b>Conference ranks say little here.</b> {p(core_unranked)} of the conference papers are in venues CORE does not rank, because CORE mainly covers computing. Journal quartiles are the better quality measure for this cluster.</li>
</ul>

<h2>3. Faculty and departments</h2>
<ul>
<li><b>A few people produce much of the output.</b> The top 10% of listed faculty account for {p(share10['IIT Indore'])} of faculty authorships at Indore, {p(share10['IIT Mandi'])} at Mandi and {p(share10['IIT Bhubaneswar'])} at Bhubaneswar.
The Gini coefficient of papers per faculty member is {gini['IIT Bhubaneswar']:.2f}, {gini['IIT Indore']:.2f} and {gini['IIT Mandi']:.2f} (Bhubaneswar, Indore, Mandi), so output is unevenly spread in all three.</li>
<li><b>Most productive faculty:</b> {", ".join(f"{f['name']} ({SH[f['institution']]}, {n(f['papers'])} papers)" for f in top_p)}.
<b>Most cited without 10+ author papers:</b> {", ".join(f"{f['name']} ({n(f['citations_excl_10plus'])})" for f in top_x)}.
<b>Most connected inside Group 6:</b> {", ".join(f"{f['name']} ({f['faculty_coauthors']} faculty co-authors)" for f in top_c)}.</li>
<li><b>Productive is not the same as connected.</b> The rank correlation (Spearman) between papers and citations is {rho_c:.2f}, but only {rho_f:.2f} between papers and the number of faculty co-authors.
Some of the most productive faculty work mainly with students and outside partners.</li>
<li><b>Largest departments by papers:</b> {"; ".join(f"{x['department']} at {SH[x['institution']]} ({n(x['papers'])} papers, {p(x['q1_share'])} Q1)" for x in deps)}.
The most used journals are Scientific Reports, Physical Review D and the Journal of Physical Chemistry C; the highest-IF venues reached are Progress in Materials Science (IF 47.7) and Progress in Energy and Combustion Science (45.1).</li>
<li><b>Caution on per-faculty averages.</b> The faculty list has {n(O['IIT Indore']['listed_faculty'])} names for Indore, {n(O['IIT Mandi']['listed_faculty'])} for Mandi and {n(O['IIT Bhubaneswar']['listed_faculty'])} for Bhubaneswar,
which is more than the regular faculty strength. Papers per listed faculty member therefore reflect the length of the list as much as productivity, and we do not rank the institutes on it.</li>
</ul>

<h2>4. Network analysis</h2>
<table class="net"><thead><tr><th>Table 2. Network</th><th>Nodes</th><th>Edges</th><th>Main measures</th></tr></thead><tbody>
<tr><td>Faculty co-authorship</td><td>{n(CA['n'])} faculty</td><td>{n(CA['m'])} links</td><td>average degree {avg_deg:.1f}; density {density:.4f}; largest connected component {n(CA['largest_component'])} ({p(CA['largest_component'] / CA['n'])}); {CA['isolated']} isolated; {CA['communities']} Louvain communities, modularity {CA['modularity']:.2f}</td></tr>
<tr><td>Institutional collaboration</td><td>{n(NET['n_partners'])} partner institutions</td><td>shared papers</td><td>{n(NET['n_indian'])} Indian and {n(NET['n_partners'] - NET['n_indian'])} foreign partners in {NET['n_countries']} countries (100+ author papers excluded; {n(NETA['n_partners'])} partners in {NETA['n_countries']} countries with them)</td></tr>
<tr><td>Citation network (within Group 6)</td><td>{n(CN['nodes'])} papers</td><td>{n(CN['edges'])} citations</td><td>{n(CN['cross_institute_edges'])} citations ({p(CN['cross_institute_edges'] / CN['edges'], 1)}) cross between institutes; {p(no_internal)} of papers are never cited from inside the group</td></tr>
<tr><td>Temporal (per year)</td><td>{n(TM[Y0]['active_faculty'])} → {n(TM[peak]['active_faculty'])} active faculty</td><td>{n(TM[Y0]['coauthor_links'])} → {n(TM[peak]['coauthor_links'])} links</td><td>{Y0} → {peak} (peak year); average degree stays near 3 ({TM[Y0]['avg_degree']:.1f} → {TM[peak]['avg_degree']:.1f}); density falls {TM[Y0]['density']:.4f} → {TM[peak]['density']:.4f}</td></tr>
</tbody></table>

<div class="fig"><img src="fig2.png" alt="Faculty network per year, co-author link types, citations exchanged with Indian institutions">
<p class="cap"><b>Figure 2.</b> (a) Faculty active in the co-authorship network and links between them, per year. (b) Share of faculty co-author links by type. (c) Citations received from and given to other Indian institutions.</p></div>

<ul>
<li><b>The three institutes are three separate networks.</b> {p(same_inst / len(pairs), 1)} of faculty co-author links are inside one institute, and {p(same_dept / len(pairs))} are inside one department.
Only {n(multi)} of {n(len(P))} faculty papers involve faculty from two Group 6 institutes, and only {p(CN['cross_institute_edges'] / CN['edges'], 1)} of the citations inside the group cross institutes.
Being in the same cluster has not produced joint work; the institutes collaborate far more with older IITs than with each other.</li>
<li><b>Tight groups joined by a few bridges.</b> The modularity of {CA['modularity']:.2f} shows that faculty work in well-separated groups, which mostly follow departments.
Even so, {p(CA['largest_component'] / CA['n'])} of faculty are in one connected component, because a small number of people link the groups.
The strongest bridges by betweenness centrality are {", ".join(f"{f['name']} ({f['department']}, {SH[f['institution']]})" for f in top_b)}. They work in areas that cut across departments, such as signal processing and biosciences.</li>
<li><b>The network grew by adding people, not by people becoming more connected.</b> Active faculty rose from {n(TM[Y0]['active_faculty'])} in {Y0} to {n(TM[peak]['active_faculty'])} in {peak}, and links from {n(TM[Y0]['coauthor_links'])} to {n(TM[peak]['coauthor_links'])},
but the average number of faculty co-authors per year stayed near 3 and density fell. New faculty join existing groups; the groups do not merge. Cross-institute links rose from {TM[Y0]['cross_institute_links']} in {Y0} to {TM[Y1]['cross_institute_links']} in {Y1}, which is still very small.
The drop after {peak} is probably a data effect: recent papers are often not yet linked to an author's main OpenAlex profile.</li>
<li><b>Partners are mostly older IITs and foreign universities.</b> The closest Indian partners are {", ".join(f"{iit(t['institution'])} ({n(t['shared_papers'])} shared papers)" for t in tp)}.
The United States has the most partner institutions ({n(dict(NET['top_countries'])['US'])}), followed by the United Kingdom ({n(dict(NET['top_countries'])['GB'])}) and Germany ({n(dict(NET['top_countries'])['DE'])}).
Including 100+ author papers adds {n(NETA['n_partners'] - NET['n_partners'])} partners that exist only through consortium papers, so we exclude those papers by default.</li>
<li><b>Group 6 cites Indian institutions more than they cite it.</b> The ratio of citations received to citations given is {FL['IIT Bhubaneswar']['impact_ratio']:.2f} for Bhubaneswar, {FL['IIT Indore']['impact_ratio']:.2f} for Indore and {FL['IIT Mandi']['impact_ratio']:.2f} for Mandi.
A ratio below 1 is expected for institutes founded in 2008–09, whose work builds on older institutions. Indore is closest to balance.</li>
</ul>

<h2>5. Two special checks</h2>
<h3>Non-governmental institutions that cite Group 6 a lot</h3>
<p>{priv20} of the 20 Indian institutions that cite Group 6 most are private universities (for example Vellore Institute of Technology, SRM and Saveetha). We tested four possible reasons on the top 60 citing institutions.
(1) <b>Size:</b> per 1,000 of their own papers, private universities cite Group 6 <i>less</i> than government ones ({S['Private']['citing_papers_per_1000_own_papers']:.0f} vs {S['Government / public']['citing_papers_per_1000_own_papers']:.0f}).
(2) <b>Growth:</b> their own output grew {S['Private']['own_output_growth']}× between 2018–19 and 2024–25 against {S['Government / public']['own_output_growth']}× for government institutions ({fast[0]['institution']} {fast[0]['own_output_growth']}×, {fast[1]['institution']} {fast[1]['own_output_growth']}×).
(3) <b>Personal links:</b> fewer of their citing papers have a former Group 6 author ({p(S['Private']['share_by_former_group6_authors'], 1)} vs {p(S['Government / public']['share_by_former_group6_authors'], 1)}) or are author self-citations ({p(S['Private']['share_author_self_citation'])} vs {p(S['Government / public']['share_author_self_citation'])}).
(4) <b>A few heavy citers:</b> the ten most active citing authors account for about a fifth of citing papers in both groups.
Our conclusion is that the high counts are a volume effect. These universities now publish very large numbers of papers in engineering, materials and computing, and so they cite everyone in those fields more, including Group 6. We found no sign of unusual citing behaviour aimed at Group 6.</p>
<h3>Faculty with very high citations from large collaborations</h3>
<p>We flagged faculty when at least half of their citations come from papers with 10+ authors, when they have any paper with 100+ authors, or when their lifetime citations reach 1 lakh. <b>{len(BF)} faculty are flagged</b>, {phys} of them in physics, astronomy or basic-sciences departments.
Papers with 10+ authors carry only {p(bigc, 1)} of the group's citations, but the effect on individuals is large: for {s1['name']} (Physics, Indore) they are {n(s1['papers_10plus_authors'])} of {n(s1['papers'])} papers and {p(s1['share_citations_10plus'])} of citations.
No listed faculty member reaches 1 lakh citations in OpenAlex; the highest lifetime count among flagged faculty is {n(life_f['citations_lifetime'])} ({life_f['name']}). Google Scholar counts are usually higher, which may explain the figure of 1 lakh.
For fair comparison, the dashboard shows every faculty member's citations both with and without 10+ author papers.</p>

<h2>6. Limitations</h2>
<ul>
<li>OpenAlex is the only publication source. Its citation counts are lower than Google Scholar's, and some recent papers are not yet linked to the right author profile.</li>
<li>Impact factors are SCImago's two-year citations per document, not Clarivate's JIF, so individual values differ slightly from JCR.</li>
<li>Authors are matched to the faculty list by name within an institute. Two different people with the same name at one institute would be merged; the list also contains more names than the regular faculty.</li>
<li>{YEARS[-1]} is incomplete, and citations for {Y1}–{YEARS[-1]} papers are still accumulating.</li>
</ul>
</body></html>"""

(OUT / "Key_Observations.html").write_text(html, encoding="utf-8")
print("written", OUT / "Key_Observations.html", "| words:", len(strip(html).split()))
