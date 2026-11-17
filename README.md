# Group 6: IIT Cluster (IIT Bhubaneswar · IIT Indore · IIT Mandi)

DPCN Research Mapping Project, 2016–2026 · Team: Arjun Dingankar, Soham Acharya, Sumit Kumar

**Dashboard:** https://arjun0471.github.io/dpcn-g6/
**Report:** [Key_Observations.pdf](Key_Observations.pdf) (4 pages; editable copy: Key_Observations.docx)

## What is in this submission
| Path | Contents |
|---|---|
| `index.html` | The analysis dashboard (the page served at the link above). Open it in a browser with internet access. |
| `Key_Observations.pdf` | Key observations report: basic statistics and network analysis, with interpretation. |
| `data/` | Main dataset, exactly as the instruction note specifies: `group6_data.csv`, `citation_network.csv`, `authorship_network.csv`, `indian_connections.csv`. |
| `data/inputs/` | Inputs: `faculty_list.csv`, SCImago journal ranks (`scimagojr.csv`), CORE conference ranks (`core_ranks.csv`), full author lists of 100+ author papers, and the output counts of the top citing institutions. |
| `data/analysis/` | Tables behind the dashboard and the report: institution overview, yearly trend, faculty and department comparison, top 30 by IF, each faculty member's top 10 by IF, frequent journals, institutional partners, temporal network, collaboration impact, citing institutions, flagged faculty and papers, and `dashboard_data.json`. |
| `data/supplementary/` | Extended versions of the four main CSVs (OpenAlex IDs, departments, flags) and per-paper / per-author network metrics. |
| `code/` | The pipeline: `group6_pipeline.py` → `phase2_extract.py` → `phase2.py` (uses `insights.py` and `phase2_template.html`) → `make_report.py`. |
| `SOURCES.md`, `DECISIONS.md` | Every source used, and how authors were verified, identical names handled and the data processed. |

The raw OpenAlex API responses (about 4,300 cached files) are not included because of their size; the pipeline downloads them again.

**Two scopes are used.** The main CSVs and the Phase I numbers below cover papers with at least one listed faculty author (17,317 papers). The overview statistics in the dashboard and the report cover every paper with a Group 6 affiliation, students' papers included (21,344 papers), as the Phase II directions ask. Figures such as the Q1 share therefore differ slightly between the two scopes.

## Run it (roughly 5–10 min the first time with 8 parallel requests; `--workers 4` if you see many 429s)
1. Put the files from `code/` and `data/inputs/` in one folder.
2. `pip install requests pandas networkx`
3. Get a free OpenAlex API key (openalex.org → sign up → API key). Without a key the daily budget is ~1,000 calls; a full run needs ~3,000.
   - macOS/Linux: `export OPENALEX_API_KEY=yourkey`
   - Windows (PowerShell): `$env:OPENALEX_API_KEY="yourkey"`
4. `python group6_pipeline.py`

Every response is cached in `cache/`. If the run stops (budget, Wi-Fi), just run it again and it continues.
To rebuild outputs after editing inputs without using the API: `python group6_pipeline.py --offline`

## Recommended extra inputs (same folder, then re-run)
| File | Why | Where |
|---|---|---|
| `faculty_list.csv` (`name,institution,department`) | Optional override. Without it, faculty are identified from authorship roles (see method notes), which gives 232 / 345 / 233 people for Bhubaneswar / Indore / Mandi. | Copy from the three institute websites. `institution` must be exactly `IIT Bhubaneswar`, `IIT Indore` or `IIT Mandi`. |
| `scimagojr.csv` | Journal quartiles (Q1–Q4). Already included. Scimago blocks scripted downloads, so if you ever need a fresh copy, download it by hand. | scimagojr.com → Journal Rankings → "Download data" |
| `core_ranks.csv` | CORE A*/A/B/C for conference papers. Also auto-downloaded if possible. | portal.core.edu.au/conf-ranks → Export |

## Outputs (`out/`) — exactly as the instruction note specifies
| File | Columns |
|---|---|
| `group6_data.csv` | group, institution, author, title, year, type, journal_name, issn, doi, citations, quartile, coauthor_institutes, cites_indian_inst, cited_by_indian_inst |
| `citation_network.csv` | source_doi, target_doi, source_inst, target_inst, year |
| `authorship_network.csv` | author_a, author_b, paper_doi, inst_a, inst_b, year |
| `indian_connections.csv` | your_inst, partner_inst, shared_papers, total_citations |
| `group6_dashboard.html` | interactive dashboard (all required panels incl. citation + co-authorship graphs); open in a browser with internet |

`out/supplementary/` holds working files that are not part of the required submission: extended versions of the four CSVs (with OpenAlex IDs, department, cross-institute flags, partner cluster, citation in/out flow and topic Jaccard), paper_metrics.csv (in-degree, PageRank), author_metrics.csv (degree, betweenness, Louvain community), faculty_summary.csv, department_summary.csv and the dashboard's data.

## Results of the run (faculty_list.csv)
- Faculty = only the people in faculty_list.csv: 1,512 names (Bhubaneswar 249 · Indore 858 · Mandi 405), all found in OpenAlex, matched to 1,881 author profiles (common names such as "Rajesh Kumar" match several profiles).
- Phase I files include only papers with at least one listed faculty author: 17,317 papers from 2016–2026 (33,044 paper × faculty rows). Per institute: Bhubaneswar 4,019 · Indore 8,549 · Mandi 4,805 (papers shared by two institutes count for each).
- Q1 share of journal papers: Bhubaneswar 56.4% · Indore 59.3% · Mandi 57.7%.
- 222,392 citation edges (DOI to DOI, 2016–2026), 42,069 of them between Group 6 papers. 65,469 co-authorship edges. 1,435 institute–partner pairs.
- Faculty co-authorship network (Phase I, every paper): 1,721 connected faculty, 69 Louvain communities (modularity 0.9).
- Phase II statistics use all 21,344 institute papers (students' papers included); see the dashboard and Key_Observations.pdf.

## Phase II and the dashboard
After the pipeline, run:
```
python phase2_extract.py   # citing papers with their authors, from the cache
python phase2.py           # Phase II metrics -> out/phase2/*.csv, and the dashboard out/group6_dashboard.html
python make_report.py      # report/Key_Observations.html with its figures (print to PDF)
```
In this submission `out/group6_dashboard.html` is `index.html`, `out/*.csv` is `data/`, `out/phase2/` is `data/analysis/` and `out/supplementary/` is `data/supplementary/`.
`out/group6_dashboard.html` is the single dashboard for the whole project. It covers every Phase I panel and the Phase II directions. An institute selector at the top (All three / Bhubaneswar / Indore / Mandi) drives the institution-level panels. Tabs:
1. **Overview:** institution summary and Q1 with IF > 5 / > 10; author-count classes; yearly trends; collaborating institutions per year. Below that, the per-institute detail: publication trend, quartile distribution, top 5 journals, CORE ranks, research areas, most-cited top 10; then collaboration and citation impact (collaboration type, team size, collaboration mix by year, research fields).
2. **Faculty & departments:** productivity vs connectedness; most productive and most connected; h-index distribution; faculty list by department; sortable faculty comparison; top 30 papers by IF; most frequent journals; each person's top 10 by IF; concentration of output (Lorenz curve, Gini); department comparison. Clicking any faculty name opens that person's full paper list; the search box at the top finds a faculty member by name.
3. **Networks:** co-authorship (faculty only), institutional, temporal analysis, and the citation network (graph, PageRank, in-degree distribution).
4. **Indian connectivity:** citation in-flow and out-flow, impact ratio, year-wise flow, top 10 citing institutes, partner ranking with cross-cluster flags and topic Jaccard.
5. **Notes:** institutions that cite Group 6 a lot (private vs government), and large-collaboration flags.
6. **Data & sources.**

Our findings are in Key_Observations.pdf and in the "Key findings" boxes on each tab; method decisions are in DECISIONS.md §4. The pipeline alone also writes a simpler `group6_dashboard.html`; running `phase2.py` replaces it with the full one.

## Method notes
- Source: OpenAlex works with an author affiliated to one of the three ROR IDs, 2016–2026. Kept: journal articles/reviews/letters and conference papers (OpenAlex type `conference-paper`, plus book-series proceedings). Excluded: preprints, repositories (Zenodo, arXiv), book chapters in edited books, errata, editorials.
  ROR: Bhubaneswar 04gx72j20 · Indore 01hhf7w52 · Mandi 05r9r2f34.
- `group6_data.csv` holds faculty publications only (papers with at least one listed faculty author): one row per paper × Group 6 faculty author. A paper with three faculty authors appears three times, once per author. The brief's "Fetch all faculty publications" is read as papers where the faculty member is listed with the assigned institute's affiliation.
- The network files are scoped to the same faculty publications. citation_network.csv keeps only edges with a DOI on both ends and a year in 2016–2026; the few others are in supplementary/. Edges in all three directions are included: between Group 6 papers, Group 6 citing other Indian institutes (out-flow), and other Indian institutes citing Group 6 (in-flow). year = year of the citing paper.
- authorship_network.csv nodes are Group 6 faculty and their co-authors at other Indian institutions (the inter-institute connections). Students and foreign co-authors are excluded, and papers without a DOI are left out. inst_a ≠ inst_b marks a cross-institution edge.
- indian_connections.csv: shared_papers = Group 6 faculty papers co-authored with the partner institution; total_citations = sum of OpenAlex citations of those shared papers.
- TRUE/FALSE flags are written in capitals, as in the brief.
- `cites_indian_inst` = the paper cites a work with an author at another Indian institution; `cited_by_indian_inst` = it is cited by one. "Another" is relative to the row's own institution, so IIT Indore ↔ IIT Mandi counts.
- Citation network metrics (in-degree, PageRank) use only the Group 6 corpus. In-/out-flow edges to other Indian institutes are in the CSV only.
- Authorship metrics use faculty of the three institutes only. For papers with more than 50 authors (e.g. CERN collaborations), only pairs among Group 6 authors are kept, so 1,000-author papers don't create half a million edges.
- Betweenness is exact up to 2,000 faculty; above that it is estimated from 500 sampled nodes (seed 42).
- Louvain uses edge weight = number of joint papers, seed 42.
- Topic Jaccard = overlap of each institution's top-30 OpenAlex subfields (2016–26), computed for every partner institution.
- Citation impact ratio = in-flow edges / out-flow edges.
- Faculty (no faculty list): an author counts as faculty of an institute if, in 2016–2026, they have ≥ 5 papers there, are last or corresponding author on ≥ 3 of them, and published there in ≥ 3 different years. PhD students mostly appear as first or middle authors, so this filters them out (the plain ≥ 5 papers rule gave 2,232 people). Some postdocs and faculty who have since left the institute may still pass the rule.
- Departments are parsed from affiliation strings ("Department of …", "School of …", "Discipline of …"). Each person gets the department they used in their latest 3 active years, because departments were renamed over time (e.g. IIT Mandi's School of Engineering split into Mechanical & Materials / Computing & Electrical / Civil & Environmental). Spelling variants are mapped to each institute's official department or school names, home departments take priority over research centres, and the old IIT Mandi "Basic Sciences" / "Engineering" labels are assigned by the person's main research field.
- OpenAlex's author disambiguation is used as-is. Common names (e.g. several "Rajesh Kumar" profiles at IIT Indore) stay separate profiles, and a profile is never merged with another by name.
- Lifetime h-index comes from OpenAlex author profiles (very high values such as ~120 come from large physics collaborations like ALICE at CERN).
- CORE ranks match only ~10% of conference papers. Most venues (e.g. IEEE regional conferences, Materials Today: Proceedings) are not in the CORE list, which only covers computing conferences.
