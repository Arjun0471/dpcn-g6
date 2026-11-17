# DECISIONS — Group 6 (IIT Bhubaneswar · IIT Indore · IIT Mandi)

This file explains how we verified authors, how we handled identical names, and how the data was processed. All steps are in `group6_pipeline.py`. Running it again with the cached responses in `cache/` (`python group6_pipeline.py --offline`) reproduces every output exactly.

---

## 1. How did we verify the authors mentioned in the papers?

We used three checks, applied in this order.

**Check 1: the author was at the institute on that paper.**
An author is linked to IIT Bhubaneswar, Indore or Mandi only if OpenAlex lists that institute in that author's affiliation on that specific paper. OpenAlex links affiliations to the institute's ROR ID; the IDs are listed in SOURCES.md. We did not use an author's "current institution", because that can be wrong for people who moved. For example, a professor who joined IIT Mandi in 2020 counts only for papers where they list IIT Mandi, not for their earlier papers from another institute.

**Check 2: the author is on our faculty list.**
Only people in `faculty_list.csv` count as faculty. Each OpenAlex author on a paper is compared with the list as follows:
- Both names are normalised: lower-case, titles removed (Dr, Prof, Mr, Ms, Mrs), punctuation and hyphens turned into spaces. For example, "Prof. Sumit Sinha‐Ray" becomes "sumit sinha ray".
- The match has to be on the **full name, within the same institute**.
- The code also has a fallback match on surname + first initial, but it is only allowed when exactly one listed person and exactly one OpenAlex profile share that key. In the final run it was never needed: all 1,512 listed names matched on the full name.

The match result for every listed person is in `out/supplementary/faculty_coverage.csv`: whether they were found, how they were matched, how many OpenAlex profiles matched, and how many 2016–2026 papers they have.

**Check 3: only papers with a listed faculty author are kept.**
A paper is in `group6_data.csv` only if at least one author passed Checks 1 and 2. Of 21,344 institute papers, 17,317 qualified. Each row is one paper × one listed faculty author. Students and outside co-authors are never rows; they appear only as context, e.g. in `coauthor_institutes`.

**Cross-checks we ran on top of these:**
- **Author roles.** We compared the list with a rule based on authorship roles: at least 5 papers at the institute, at least 3 as last or corresponding author, and active in at least 3 years. 252 people who meet the rule are not on the list, for example Aditi Halder (IIT Mandi) and Bhargav Vaidya (IIT Indore). Their papers are excluded because the list defines faculty.
- **Department.** Each faculty member's department was compared with the departments written in their paper affiliations, and mapped to each institute's official department / school names (see §3, step 6).
- **Spot checks.** We checked a few names by hand. For example, Rajesh Kumar (IIT Indore) is affiliated with Physics on his papers, consistent with the list.

**What we could not verify:** we could not confirm the list against official institute web pages. IIT Indore has no central faculty list, IRINS blocks automated access, and the IIT Bhubaneswar faculty page did not load (see SOURCES.md §3).

---

## 2. How did we handle authors with identical names?

**Identity comes from OpenAlex author IDs, not names.**
OpenAlex assigns each author an ID using ORCID, co-authors, affiliations and research topics. Two different people with the same name normally get different IDs. Paper counts, h-index and network nodes are all computed per OpenAlex author ID.

**Same name, different institutes: never merged.**
Matching against the list is done within each institute. A "Rajesh Kumar" at IIT Indore is never matched to a "Rajesh Kumar" at IIT Mandi or anywhere else.

**Same name, same institute: all matching profiles go to the listed person.**
The faculty list gives only a name, institute and department, so it cannot tell two same-named profiles apart. When several OpenAlex profiles at one institute have exactly the listed name, all of them are attributed to that listed person.
- This affected **184 of 1,512 listed names**, which matched **553 profiles** in total: Bhubaneswar 21 names, Indore 100, Mandi 63.
- The largest cases are common names: Rajesh Kumar (Indore, 17 profiles), Pradeep Kumar (Mandi, 14), Rajeev Kumar (Mandi, 10), Ankur Kumar (Mandi, 9), Mukesh Kumar and Nagendra Kumar (Indore, 8 each).
- Usually these extra profiles are the same person split by OpenAlex. Sometimes they are a different person with the same name, e.g. a PhD student who is not on the list. We could not separate those cases automatically, so the faculty-level counts for these 182 names may be overstated.

**Other safeguards:**
- **Surname + initial matching** (e.g. "R. Kumar") is only used when it is unambiguous on both sides, so abbreviated names cannot cause false merges. It was not needed in the final run.
- **No double counting of papers.** Paper totals, citations, trends and quartile shares count each paper once (by its OpenAlex work ID), even when several listed faculty co-wrote it.
- **People who moved between the three IITs** keep a separate row per institute. 9 profiles appear at two of the three IITs.
- **The faculty table is one row per profile.** `faculty_summary.csv` has 1,881 rows for the 1,512 listed people, because of the multi-profile names above. In the report, faculty counts are taken from the list (249 / 858 / 405), not from profiles.

---

## 3. Data processing pipeline

```
OpenAlex API ──► 1 Fetch papers ──► 2 Filter venues ──► 3 Rank (SCImago / CORE)
                                                               │
faculty_list.csv ──► 4 Match authors ──► 5 Keep faculty papers ┘
                                                │
          6 Departments ◄───────────────────────┤
          7 Citation links (OpenAlex cites / cited_by) ──► citation_network.csv
          8 Co-authorship pairs ──► authorship_network.csv
          9 Indian partner aggregation ──► indian_connections.csv
         10 Metrics (PageRank, centrality, Louvain) ──► dashboard + report
```

**Step 1: Fetch papers (OpenAlex).**
- **Query:** all works 2016–2026 with an author affiliated to each institute's OpenAlex/ROR ID, in two passes:
  - articles, reviews, letters and book chapters;
  - OpenAlex's separate `conference-paper` type. This one was added after we found that conference papers were being missed.
- **Result:** 23,682 unique works.
- **Caching:** every API response is saved in `cache/`, so the run can be resumed and repeated without new API calls.
- **Papers with 100+ authors:** OpenAlex search results list at most 100 authors per paper. For the 310 papers above that limit (CERN ALICE, Belle II and similar), the full author list was fetched paper by paper (`full_authors.json`). This restored 1,691 Group 6 author entries that the cut-off had hidden; without it, physicists such as Raghunath Sahoo would have been missing from about 170 of their papers.

**Step 2: Keep only journal and conference papers.**
- **Journal:** the source type is `journal`.
- **Conference:** the work type is `conference-paper`, or the source is a conference / proceedings series.
- **Dropped:** preprints and repositories (arXiv, Zenodo, Figshare), chapters in edited books, errata and editorials.
- **Result:** 21,344 papers with at least one IIT-affiliated author.

**Step 3: Add ranks.**
- **Journals:** the SCImago best quartile, matched by ISSN and then by title. 95% of journal papers received a quartile.
- **Conferences:** the CORE2023 rank, matched by title or acronym. Only about 9% matched, because CORE covers only computing conferences; see SOURCES.md.

**Step 4: Match authors to the faculty list.** As described in §1 and §2.

**Step 5: Keep faculty publications.**
- **Rule:** keep papers with at least one listed faculty author.
- **Result:** 17,317 papers, giving 33,044 paper × faculty rows.
- **Institute assignment:** a paper belongs to the institute(s) of its listed faculty authors (Bhubaneswar 4,019, Indore 8,549, Mandi 4,805; papers shared between institutes count for each).

**Step 6: Assign departments.**
- **Source:** the department given in `faculty_list.csv`, or, if blank, the department named in the person's paper affiliations ("Department of …", "School of …", "Discipline of …").
- **Which affiliation wins:** affiliations from the person's latest 3 active years take priority, because departments were renamed over the decade. A home department takes priority over a research centre.
- **Naming:** spelling variants are mapped to each institute's official department / school names (e.g. "Earth" → Earth, Ocean and Climate Sciences; "Metallurgical …" and "Metallurgy …" → one department).

**Step 7: Build the citation network.**
- **Edges inside the corpus:** for each paper we read `referenced_works`. Any reference to another Group 6 paper is an internal edge (42,069 edges).
- **Out-flow:** OpenAlex's `cited_by` filter combined with `institutions.country_code:IN` finds the referenced papers that have an author at an Indian institution. A reference counts as out-flow when that Indian institution is not the citing paper's own institute.
- **In-flow:** the `cites` filter with the same country filter finds Indian papers that cite Group 6 papers.
- **Output:** `citation_network.csv` keeps edges with a DOI on both ends and a citing year of 2016–2026 (222,392 edges). `year` is the year of the citing paper.
- **Row flags:** a paper's `cites_indian_inst` / `cited_by_indian_inst` is TRUE when it cites, or is cited by, a paper from another Indian institution. "Another" is relative to the row's own institute, so IIT Indore ↔ IIT Mandi counts.

**Step 8: Build the co-authorship network.**
- **Pairs:** for every paper (with a DOI), all pairs of authors where both are either listed faculty or authors at another Indian institution. Students and foreign co-authors are excluded.
- **Big collaborations:** papers with more than 50 authors (e.g. CERN collaborations) contribute only pairs between listed faculty.
- **Cross-institution edges:** `inst_a ≠ inst_b`.
- **Result:** 65,469 edges in `authorship_network.csv`.

**Step 9: Aggregate Indian connections.**
- **Grouping:** for each institute and each Indian partner institution.
  - `shared_papers`: Group 6 faculty papers co-authored with that partner.
  - `total_citations`: the sum of OpenAlex citations of those papers.
- **Result:** 1,435 institute–partner pairs with 863 partner institutions.
- **Extras for the report:** partner cluster (IIT, NIT, CSIR, DAE …), citations exchanged with each partner, and topic Jaccard similarity (overlap of each institution's top-30 OpenAlex research subfields). These are in `supplementary/indian_connections_extended.csv`.

**Step 10: Compute metrics and build outputs.**
- **Citation network, papers inside Group 6 only:**
  - PageRank (damping 0.85);
  - in-degree, both cluster-wide and within each institute.
- **Co-authorship network, listed faculty only:**
  - degree centrality;
  - betweenness centrality (exact, or sampled from 500 nodes above 2,000 nodes; seed 42);
  - Louvain communities weighted by number of joint papers (seed 42): 69 communities, modularity 0.90.
- **Institute statistics:** papers per year, Q1 fraction, top 5 journals, top 10 cited papers, research fields (OpenAlex primary topic), h-index distribution (OpenAlex lifetime h-index per profile), and Indian citation in-flow / out-flow and impact ratio.
- **Outputs:** the four required CSVs in `out/` with exactly the columns in the instruction note, plus `group6_dashboard.html`. Extended versions and metric tables are in `out/supplementary/`.

**Checks before submission.**
- **Automated:** exact column names and order, years 2016–2026 only, all three institutes present, `type` is only journal/conference, ISSN only on journals, DOIs as URLs, TRUE/FALSE flags, and every author row is a listed faculty member.
- **Manual:** the dashboard was rendered and inspected.

---

## 4. Phase II decisions

Phase II (`phase2.py`, `out/phase2/`) follows the additional directions. Phase I and Phase II share one dashboard, `out/group6_dashboard.html`. Its institution-level panels (trend, quartiles, top journals, CORE, research areas, most-cited, h-index, Indian connectivity) are computed on all institute papers, the same scope as the other publication statistics. The main choices:

**Students' papers in statistics, not in faculty networks.**
Publication statistics (counts, Q1, impact factor, author-count classes, yearly trends, collaborating institutions) use all 21,344 papers with a Group 6 affiliation, including papers by students only. Faculty comparisons and the faculty co-authorship network use listed faculty only.

**Impact factor.**
Clarivate's Journal Impact Factor (JCR) is not openly available. We use SCImago's "Citations / Doc. (2 years)": citations in year Y to a journal's items from Y−1 and Y−2, divided by those items. It is the same formula as the JIF, but computed on Scopus data, so values are usually somewhat higher than the official JIF (e.g. Scientific Reports 5.0 here). 95% of journal papers have a value. "IF > 5" and "IF > 10" use this number. Top-30 lists are ranked by IF, with ties broken by citations.

**One person, several profiles.**
Faculty-level numbers merge all OpenAlex profiles matched to one listed name at one institute into one person (see §2). A person's h-index (2016–26) is recomputed from the merged papers; the lifetime h-index and lifetime citations are taken from their largest profile, so they are not inflated by adding profiles together.

**Author-count classes.**
"< 10" and "10 or more" authors, as asked; 100+ is shown separately. Author counts use the full author list (see Step 1).

**Co-authorship network excludes 100+ author papers.**
Appearing together on a 1,000-author consortium paper is not a collaboration between two people, so those 310 papers do not create faculty–faculty links in the Phase II network. They still count in publication statistics, and they remain in the Phase I `authorship_network.csv`, because the instruction note asks for pairs from every paper.

**Institutional network.**
Nodes are institutions on Group 6 papers. Edges join each Group 6 institute to each partner institution and are weighted by shared papers; links between two partners are left out to keep the picture readable. The dashboard shows two versions: without 100+ author papers (the default, since consortium papers add about 190 foreign partners that only appear there) and with all papers.

**Temporal analysis.**
Each year's network contains the listed faculty who published that year and the co-author links from that year's papers. Yearly figures: active faculty, links, average co-authors, share in the largest connected group, and cross-institute links.

**Note A: institutions that cite Group 6 a lot.**
- **Which institutions:** the top 60 Indian citing institutions by citations to Group 6.
- **Ownership:** classified by hand as private (deemed or self-financed universities: VIT, SRM, Saveetha, Manipal, Amity, Amrita, LPU, Chandigarh University, Chitkara, BITS Pilani, KL, KIIT, Graphic Era, SOA, Jain, Thapar, UPES, GLA) or government/public (central and state institutions, government labs). OpenAlex does not record ownership.
- **Normalisation:** each institution's own output (all its 2016–2026 papers, and per year) was taken from OpenAlex. Citing is then compared per 1,000 own papers and as growth from 2018–19 to 2024–25.
- **Other indicators:**
  - **Former Group 6 authors:** the share of citing papers with an author who has published from a Group 6 IIT.
  - **Author self-citation:** an author citing their own Group 6 paper.
  - **Group 6 references per citing paper.**
  - **Concentration:** the share coming from the 10 most active citing authors.
- **Conclusion:** private universities cite Group 6 less per paper they publish; their high totals follow from how fast their own output grew. Former Group 6 authors, self-citation and a few heavy citers do not explain it. See Key_Observations.pdf §5.

**Note B: large collaborations.**
Every paper with 10 or more authors is flagged (`flagged_10plus_author_papers.csv`). A faculty member is flagged if:
- at least 50% of their 2016–26 citations come from 10+ author papers, or
- they have any 100+ author paper, or
- their lifetime citations are 1 lakh or more.

No one reaches 1 lakh in OpenAlex (the highest is 77,055); Google Scholar counts are usually higher. The faculty table shows citations with and without 10+ author papers side by side.

**Citation index (collaboration and impact).**
Older papers have had more time to collect citations, so raw citations per paper cannot compare groups of papers with different age mixes. The citation index of a paper is its citations divided by the mean citations of all Group 6 papers published in the same year; 1.0 is the Group 6 average. It is averaged over:
- collaboration type: single institute, with other Indian institutions, international (any author affiliation outside India). Papers with 10+ authors are left out of this comparison so that consortium papers do not drive it;
- number of authors (1, 2–3, 4–5, 6–9, 10–99, 100+);
- venue type, journal quartile and OpenAlex field.

Output: `data/analysis/collaboration_impact.csv`. The index describes association, not cause.

**Concentration of faculty output.**
The Lorenz curve and Gini coefficient are computed per institute on papers per listed faculty member (2016–26).

**Checks on Phase II numbers.**
Key numbers were recomputed by separate code from the raw data, and all checks passed:
- publications, Q1 and Q1 with IF > 10 per institute;
- 10+ author counts;
- the Saveetha rate and growth factors;
- the private vs government medians;
- Raghunath Sahoo's paper counts;
- the co-authorship link count;
- the top-30 ordering and the flag rule.
