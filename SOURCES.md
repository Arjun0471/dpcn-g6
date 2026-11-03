# SOURCES — Group 6 (IIT Cluster: IIT Bhubaneswar · IIT Indore · IIT Mandi)

Every number in the dataset, network files, dashboard and report comes from the sources below. Data was collected on 19–21 October 2026.

## 1. Primary data source

| Source | What we took from it | How it was accessed |
|---|---|---|
| **OpenAlex** — https://openalex.org (API: https://api.openalex.org) | All publications 2016–2026, titles, years, DOIs, venues (journal / conference), ISSNs, citation counts, author lists with per-paper affiliations, `referenced_works` (who cites whom), research fields/topics, author h-index (`summary_stats`) | REST API with a free API key, 4,322 cached responses. Endpoints: `/works` (filters `institutions.id`, `publication_year`, `type`, `cites`, `cited_by`, `institutions.country_code`, `group_by=primary_topic.subfield.id`) and `/authors` |
| OpenAlex documentation — https://developers.openalex.org/api-reference/authentication, https://help.openalex.org/api/filtering/ | API limits (100 results/page, 100 OR-values/filter), filter syntax | Read |

### Institution identifiers (ROR + OpenAlex)

| Institution | ROR ID | OpenAlex ID |
|---|---|---|
| IIT Bhubaneswar | https://ror.org/04gx72j20 | I99729588 |
| IIT Indore | https://ror.org/01hhf7w52 | I64295750 |
| IIT Mandi | https://ror.org/05r9r2f34 | I9579091 |

ROR registry: https://ror.org. IDs were verified against the OpenAlex institutions endpoint.

Additional OpenAlex data used in Phase II:
- **Full author lists** of the 310 papers with 100+ authors, from the single-work endpoint (`/works/{id}`), because list results show at most 100 authors. File: `full_authors.json`.
- **Author profiles** of the restored authors (`/authors`).
- **Total output** of the top 60 Indian citing institutions, overall and per year 2016–2026 (`/works?filter=institutions.id:…&group_by=publication_year`). Files: `citer_meta.json`, `citer_years.json`.

## 2. Ranking sources

| Source | Used for | Version |
|---|---|---|
| **SCImago Journal & Country Rank** — https://www.scimagojr.com/journalrank.php | Journal quartile (Q1–Q4, "SJR Best Quartile"), matched by ISSN, then by journal title | Full export downloaded 19 Oct 2026 (32,193 journals; 2025 edition), file `scimagojr.csv` |
| **SCImago "Citations / Doc. (2 years)"** (same file) | Impact factor used in Phase II (Journal Impact Factor formula on Scopus data; Clarivate JCR is not openly available) | 2025 edition |
| **CORE Conference Portal** — https://portal.core.edu.au/conf-ranks/ | Conference rank (A*, A, B, C), matched by conference title / acronym | CORE2023 export (955 conferences, 759 with A*–C), file `core_ranks.csv` |

## 3. Faculty list

| Source | Used for |
|---|---|
| `faculty_list.csv` — compiled and supplied by our group (1,512 names: Bhubaneswar 249, Indore 858, Mandi 405) | Defines who counts as faculty. Only papers with at least one listed person are included |

Institute websites we tried for official faculty lists. None could be used, so no data was taken from them:
- https://www.iiti.ac.in and https://facultyaffairs.iiti.ac.in — no central faculty list; faculty are listed separately on each department's site.
- https://iiti.irins.org (IRINS) — protected by a Cloudflare bot check, so it could not be read automatically.
- https://old.iitbbs.ac.in/faculty-members.php — page did not load.

## 4. Software

Python 3 with pandas (data), NetworkX (PageRank, degree/betweenness centrality, Louvain communities), requests (API). Dashboard: Chart.js 4.4.1 and Cytoscape.js 3.28.1 (loaded from cdnjs.cloudflare.com). Code: `group6_pipeline.py`.

## 5. Publication venues in the dataset

The papers in `group6_data.csv` (17,317 papers) appeared in **2,744 journals** and **533 conference / proceedings venues**. All of them are listed below with the number of Group 6 papers each. The venue name, ISSN and paper metadata come from OpenAlex; quartiles from SCImago; conference ranks from CORE. Phase II publication statistics also include students' papers (21,344 papers); their venues are in `out/phase2/frequent_journals.csv` and the dashboard.

Contents: [5.1 Journals](#51-journals-2744) · [5.2 Conferences](#52-conferences--proceedings-533) · [6. Indian partner institutions](#6-indian-partner-institutions-863)

### 5.1 Journals (2,744)

| # | Journal | ISSN | Scimago quartile | Papers |
|---|---|---|---|---|
| 1 | Scientific Reports | 2045-2322 | Q1 | 165 |
| 2 | Physical review. D/Physical review. D. | 2470-0010 | Q1 | 151 |
| 3 | The Journal of Physical Chemistry C | 1932-7447 | Q1 | 125 |
| 4 | Journal of Alloys and Compounds | 0925-8388 | Q1 | 104 |
| 5 | IEEE Access | 2169-3536 | Q1 | 103 |
| 6 | Physical review. B./Physical review. B | 2469-9950 | Q1 | 101 |
| 7 | ChemistrySelect | 2365-6549 | Q3 | 97 |
| 8 | Materials Today Proceedings | 2214-7853 | — | 97 |
| 9 | ACS Applied Materials & Interfaces | 1944-8244 | Q1 | 94 |
| 10 | ACS Applied Nano Materials | 2574-0970 | Q1 | 89 |
| 11 | IEEE Sensors Journal | 1530-437X | Q1 | 87 |
| 12 | RSC Advances | 2046-2069 | Q1 | 80 |
| 13 | Ceramics International | 0272-8842 | Q1 | 74 |
| 14 | Journal of Materials Engineering and Performance | 1059-9495 | Q2 | 74 |
| 15 | Journal of High Energy Physics | 1029-8479 | Q2 | 73 |
| 16 | Dalton Transactions | 1477-9226 | Q2 | 72 |
| 17 | Journal of Materials Science Materials in Electronics | 0957-4522 | Q2 | 72 |
| 18 | Monthly Notices of the Royal Astronomical Society | 0035-8711 | Q1 | 69 |
| 19 | Nanoscale | 2040-3364 | Q1 | 66 |
| 20 | IEEE Transactions on Electron Devices | 0018-9383 | Q1 | 64 |
| 21 | Journal of Applied Physics | 0021-8979 | Q2 | 64 |
| 22 | Journal of Materials Chemistry C | 2050-7526 | Q1 | 64 |
| 23 | New Journal of Chemistry | 0398-9836 | Q2 | 64 |
| 24 | ACS Omega | 2470-1343 | Q1 | 62 |
| 25 | Journal of Biomolecular Structure and Dynamics | 0739-1102 | Q2 | 61 |
| 26 | Journal of Materials Chemistry A | 2050-7488 | Q1 | 61 |
| 27 | Physical Review C | 0556-2813 | Q1 | 59 |
| 28 | ACS Applied Energy Materials | 2574-0962 | Q1 | 58 |
| 29 | IEEE Sensors Letters | 2475-1472 | Q2 | 56 |
| 30 | Materials Today Communications | 2352-4928 | Q1 | 56 |
| 31 | Physics of Fluids | 1070-6631 | Q1 | 56 |
| 32 | IEEE Transactions on Vehicular Technology | 0018-9545 | Q1 | 55 |
| 33 | Inorganic Chemistry | 0020-1669 | Q1 | 55 |
| 34 | Applied Surface Science | 0169-4332 | Q1 | 54 |
| 35 | Physical Chemistry Chemical Physics | 1463-9076 | Q2 | 54 |
| 36 | Chemistry - An Asian Journal | 1861-471X | Q2 | 53 |
| 37 | Journal of Physics D Applied Physics | 0022-3727 | Q1 | 53 |
| 38 | Biomedical Signal Processing and Control | 1746-8094 | Q1 | 52 |
| 39 | Journal of Physics Condensed Matter | 0953-8984 | Q2 | 51 |
| 40 | The Journal of Organic Chemistry | 0022-3263 | Q2 | 50 |
| 41 | Physical Review Letters | 0031-9007 | Q1 | 49 |
| 42 | IEEE Communications Letters | 1089-7798 | Q1 | 47 |
| 43 | Langmuir | 0743-7463 | Q1 | 46 |
| 44 | The European Physical Journal C | 1434-6044 | Q1 | 46 |
| 45 | The Journal of Physical Chemistry Letters | 1948-7185 | Q1 | 46 |
| 46 | Transactions of the Indian Institute of Metals | 0972-2815 | Q2 | 46 |
| 47 | Journal of Energy Storage | 2352-152X | Q1 | 45 |
| 48 | Construction and Building Materials | 0950-0618 | Q1 | 44 |
| 49 | Journal of Hazardous Toxic and Radioactive Waste | 2153-5493 | Q2 | 43 |
| 50 | Environmental Science and Pollution Research | 0944-1344 | Q1 | 42 |
| 51 | IEEE Transactions on Instrumentation and Measurement | 0018-9456 | Q1 | 42 |
| 52 | International Journal of Hydrogen Energy | 0360-3199 | Q1 | 42 |
| 53 | ACS Applied Electronic Materials | 2637-6113 | Q1 | 41 |
| 54 | Small | 1613-6810 | Q1 | 40 |
| 55 | Materials Letters | 0167-577X | Q2 | 39 |
| 56 | Chemical Communications | 1359-7345 | Q1 | 38 |
| 57 | Materials Research Express | 2053-1591 | Q2 | 38 |
| 58 | Expert Systems with Applications | 0957-4174 | Q1 | 37 |
| 59 | Materials Chemistry and Physics | 0254-0584 | Q1 | 37 |
| 60 | Natural Hazards | 0921-030X | Q1 | 37 |
| 61 | Applied Physics Letters | 0003-6951 | Q1 | 36 |
| 62 | Materials Advances | 2633-5409 | Q1 | 35 |
| 63 | Physica Scripta | 0031-8949 | Q2 | 35 |
| 64 | Theoretical and Applied Climatology | 0066-6424 | Q2 | 35 |
| 65 | Applied Thermal Engineering | 1359-4311 | Q1 | 34 |
| 66 | Chemistry - A European Journal | 0947-6539 | Q1 | 34 |
| 67 | Journal of Magnetism and Magnetic Materials | 0304-8853 | Q2 | 34 |
| 68 | Applied Physics A | 0947-8396 | Q2 | 33 |
| 69 | International Journal of Biological Macromolecules | 0141-8130 | Q1 | 33 |
| 70 | Journal of Electronic Materials | 0361-5235 | Q2 | 33 |
| 71 | Structures | 2352-0124 | Q1 | 33 |
| 72 | IEEE Wireless Communications Letters | 2162-2337 | Q1 | 32 |
| 73 | Electrochimica Acta | 0013-4686 | Q1 | 31 |
| 74 | Nanotechnology | 0957-4484 | Q2 | 31 |
| 75 | ACS Applied Bio Materials | 2576-6422 | Q1 | 30 |
| 76 | Applied Soft Computing | 1568-4946 | Q1 | 30 |
| 77 | ChemCatChem | 1867-3880 | Q1 | 30 |
| 78 | Indian geotechnical journal | 0046-8983 | Q3 | 29 |
| 79 | The Science of The Total Environment | 0048-9697 | Q1 | 29 |
| 80 | Journal of Astrophysics and Astronomy | 0250-6335 | Q2 | 28 |
| 81 | Physical review. E | 2470-0045 | Q2 | 28 |
| 82 | International Journal of Heat and Mass Transfer | 0017-9310 | Q1 | 27 |
| 83 | Journal of Materials Research and Technology | 2214-0697 | Q1 | 27 |
| 84 | Mathematical Methods in the Applied Sciences | 0170-4214 | Q2 | 27 |
| 85 | Physica A Statistical Mechanics and its Applications | 0378-4371 | Q2 | 27 |
| 86 | Pure and Applied Geophysics | 0033-4533 | Q2 | 27 |
| 87 | Sadhana | 0256-2499 | Q2 | 27 |
| 88 | The European Physical Journal A | 1434-6001 | Q1 | 27 |
| 89 | Circuits Systems and Signal Processing | 0278-081X | Q3 | 26 |
| 90 | Journal of Organometallic Chemistry | 0022-328X | Q3 | 26 |
| 91 | Materials Science and Engineering A | 0921-5093 | Q1 | 26 |
| 92 | Measurement | 0263-2241 | Q1 | 26 |
| 93 | Mechanics of Advanced Materials and Structures | 1537-6494 | Q1 | 26 |
| 94 | Optical Materials | 0925-3467 | Q1 | 26 |
| 95 | Organic & Biomolecular Chemistry | 1477-0520 | Q2 | 26 |
| 96 | Physics Letters B | 0370-2693 | Q1 | 26 |
| 97 | IEEE Systems Journal | 1932-8184 | Q1 | 25 |
| 98 | Journal of Materials Science | 0022-2461 | Q1 | 25 |
| 99 | Journal of environmental chemical engineering | 2213-2929 | Q1 | 25 |
| 100 | Materialia | 2589-1529 | Q2 | 25 |
| 101 | Multimedia Tools and Applications | 1380-7501 | Q1 | 25 |
| 102 | Surfaces and Interfaces | 2468-0230 | Q1 | 25 |
| 103 | The Journal of Physical Chemistry B | 1520-5207 | Q1 | 25 |
| 104 | IEEE Transactions on Consumer Electronics | 0098-3063 | Q1 | 24 |
| 105 | Polymer Composites | 0272-8397 | Q1 | 24 |
| 106 | Sensors and Actuators B Chemical | 0925-4005 | Q1 | 24 |
| 107 | Solar Energy | 0038-092X | Q1 | 24 |
| 108 | The International Journal of Advanced Manufacturing Technology | 0268-3768 | Q1 | 24 |
| 109 | Advances in Space Research | 0273-1177 | Q1 | 23 |
| 110 | Catalysis Science & Technology | 2044-4753 | Q2 | 23 |
| 111 | Energy Technology | 2194-4288 | Q2 | 23 |
| 112 | International Journal of Climatology | 0899-8418 | Q1 | 23 |
| 113 | Journal of Environmental Management | 0301-4797 | Q1 | 23 |
| 114 | Journal of Materials Chemistry B | 2050-750X | Q1 | 23 |
| 115 | Advanced Functional Materials | 1616-301X | Q1 | 22 |
| 116 | Asian Journal of Organic Chemistry | 2193-5807 | Q3 | 22 |
| 117 | Atmospheric Research | 0169-8095 | Q1 | 22 |
| 118 | Chaos Solitons & Fractals | 0960-0779 | Q1 | 22 |
| 119 | Energy & Fuels | 0887-0624 | Q1 | 22 |
| 120 | Journal of Cleaner Production | 0959-6526 | Q1 | 22 |
| 121 | Journal of Hydrology | 0022-1694 | Q1 | 22 |
| 122 | Chaos An Interdisciplinary Journal of Nonlinear Science | 1054-1500 | Q1 | 21 |
| 123 | Chemical Engineering Journal | 1385-8947 | Q1 | 21 |
| 124 | IEEE Consumer Electronics Magazine | 2162-2248 | Q1 | 21 |
| 125 | Materials and Manufacturing Processes | 1042-6914 | Q1 | 21 |
| 126 | Neural Networks | 0893-6080 | Q1 | 21 |
| 127 | Nuclear Instruments and Methods in Physics Research Section A Accelerators Spectrometers Detectors and Associated Equipment | 0168-9002 | Q2 | 21 |
| 128 | Semiconductor Science and Technology | 0268-1242 | Q3 | 21 |
| 129 | Sensors and Actuators A Physical | 0924-4247 | Q1 | 21 |
| 130 | Silicon | 1876-990X | Q2 | 21 |
| 131 | AIP Advances | 2158-3226 | Q3 | 20 |
| 132 | Computers in Biology and Medicine | 0010-4825 | Q1 | 20 |
| 133 | IEEE Photonics Technology Letters | 1041-1135 | Q2 | 20 |
| 134 | Journal of Building Engineering | 2352-7102 | Q1 | 20 |
| 135 | Journal of Manufacturing Processes | 1526-6125 | Q1 | 20 |
| 136 | Journal of Molecular Liquids | 0167-7322 | Q1 | 20 |
| 137 | Journal of the American Ceramic Society | 0002-7820 | Q2 | 20 |
| 138 | Materials Chemistry Frontiers | 2052-1537 | Q1 | 20 |
| 139 | Neural Computing and Applications | 0941-0643 | Q1 | 20 |
| 140 | Neurocomputing | 0925-2312 | Q1 | 20 |
| 141 | Pattern Recognition Letters | 0167-8655 | Q1 | 20 |
| 142 | Chemical Science | 2041-6520 | Q1 | 19 |
| 143 | Electric Power Systems Research | 0378-7796 | Q1 | 19 |
| 144 | Engineering Applications of Artificial Intelligence | 0952-1976 | Q1 | 19 |
| 145 | Heliyon | 2405-8440 | Q1 | 19 |
| 146 | Journal of Molecular Structure | 0022-2860 | Q2 | 19 |
| 147 | Journal of subatomic particles and cosmology. | 3050-4805 | — | 19 |
| 148 | Materials | 1996-1944 | Q2 | 19 |
| 149 | Sustainable Energy & Fuels | 2398-4902 | Q2 | 19 |
| 150 | The Astrophysical Journal | 0004-637X | Q1 | 19 |
| 151 | The European Physical Journal Plus | 2190-5444 | Q2 | 19 |
| 152 | ACS Materials Letters | 2639-4979 | Q1 | 18 |
| 153 | ACS Sustainable Chemistry & Engineering | 2168-0485 | Q1 | 18 |
| 154 | Chemistry of Materials | 0897-4756 | Q1 | 18 |
| 155 | Engineering Research Express | 2631-8695 | Q2 | 18 |
| 156 | Fuel | 0016-2361 | Q1 | 18 |
| 157 | IEEE Internet of Things Journal | 2327-4662 | Q1 | 18 |
| 158 | IEEE Journal of Biomedical and Health Informatics | 2168-2194 | Q1 | 18 |
| 159 | IEEE Transactions on Communications | 0090-6778 | Q1 | 18 |
| 160 | IEEE Transactions on Very Large Scale Integration (VLSI) Systems | 1063-8210 | Q1 | 18 |
| 161 | Journal of Cosmology and Astroparticle Physics | 1475-7508 | Q2 | 18 |
| 162 | Journal of Lightwave Technology | 0733-8724 | Q1 | 18 |
| 163 | ACS Applied Optical Materials | 2771-9855 | Q2 | 17 |
| 164 | ChemNanoMat | 2199-692X | Q2 | 17 |
| 165 | Chemosphere | 0045-6535 | Q1 | 17 |
| 166 | European Journal of Organic Chemistry | 1099-0690 | Q2 | 17 |
| 167 | IEEE Transactions on Nanotechnology | 1536-125X | Q2 | 17 |
| 168 | IFAC-PapersOnLine | 2405-8963 | — | 17 |
| 169 | Innovative Infrastructure Solutions | 2364-4176 | Q2 | 17 |
| 170 | Journal of Materials in Civil Engineering | 0899-1561 | Q1 | 17 |
| 171 | Journal of Power Sources | 0378-7753 | Q1 | 17 |
| 172 | Meteorology and Atmospheric Physics | 0177-7971 | Q3 | 17 |
| 173 | Nature Communications | 2041-1723 | Q1 | 17 |
| 174 | Proceedings of the Institution of Mechanical Engineers Part C Journal of Mechanical Engineering Science | 0263-7154 | Q2 | 17 |
| 175 | Proceedings of the Institution of Mechanical Engineers Part H Journal of Engineering in Medicine | 0954-4119 | Q2 | 17 |
| 176 | Scripta Materialia | 1359-6462 | Q1 | 17 |
| 177 | The Philosophical Magazine A Journal of Theoretical Experimental and Applied Physics | 1478-6433 | Q3 | 17 |
| 178 | Thin-Walled Structures | 0263-8231 | Q1 | 17 |
| 179 | Acta Mechanica | 0001-5970 | Q1 | 16 |
| 180 | Applied Optics | 0003-6935 | Q2 | 16 |
| 181 | Applied Organometallic Chemistry | 0268-2605 | Q2 | 16 |
| 182 | Experimental Heat Transfer | 0891-6152 | Q2 | 16 |
| 183 | IEEE Transactions on Circuits and Systems I Regular Papers | 1549-8328 | Q1 | 16 |
| 184 | IEEE Transactions on Industry Applications | 0093-9994 | Q1 | 16 |
| 185 | Journal of Earth System Science | 0253-4126 | Q2 | 16 |
| 186 | Journal of Instrumentation | 1748-0221 | Q3 | 16 |
| 187 | Journal of Photochemistry and Photobiology A Chemistry | 1010-6030 | Q1 | 16 |
| 188 | Journal of Vibration Engineering & Technologies | 2321-3558 | Q1 | 16 |
| 189 | Journal of the American Chemical Society | 0002-7863 | Q1 | 16 |
| 190 | Journal of the Indian Society of Remote Sensing | 0255-660X | Q2 | 16 |
| 191 | Materials Science and Engineering B | 0921-5107 | Q1 | 16 |
| 192 | Ocean Engineering | 0029-8018 | Q1 | 16 |
| 193 | Physics Letters A | 0375-9601 | Q2 | 16 |
| 194 | Proceedings of the Institution of Mechanical Engineers Part E Journal of Process Mechanical Engineering | 0954-4089 | Q2 | 16 |
| 195 | Thermal Science and Engineering Progress | 2451-9049 | Q1 | 16 |
| 196 | Wireless Personal Communications | 0929-6212 | Q2 | 16 |
| 197 | Advances in Materials and Processing Technologies | 2374-068X | Q2 | 15 |
| 198 | Applied Intelligence | 0924-669X | Q2 | 15 |
| 199 | Biomass Conversion and Biorefinery | 2190-6815 | Q2 | 15 |
| 200 | CIRP journal of manufacturing science and technology | 1755-5817 | Q1 | 15 |
| 201 | Composite Structures | 0263-8223 | Q1 | 15 |
| 202 | Computers & Electrical Engineering | 0045-7906 | Q1 | 15 |
| 203 | CrystEngComm | 1466-8033 | Q2 | 15 |
| 204 | Environmental Monitoring and Assessment | 0167-6369 | Q2 | 15 |
| 205 | Europhysics Letters (EPL) | 0295-5075 | Q2 | 15 |
| 206 | IEEE Transactions on Circuits & Systems II Express Briefs | 1549-7747 | Q1 | 15 |
| 207 | IET Generation Transmission & Distribution | 1751-8687 | Q2 | 15 |
| 208 | International Journal of Thermal Sciences | 1290-0729 | Q1 | 15 |
| 209 | ACS Applied Engineering Materials | 2771-9545 | — | 14 |
| 210 | Advanced Engineering Materials | 1438-1656 | Q2 | 14 |
| 211 | Angewandte Chemie | 0044-8249 | — | 14 |
| 212 | Angewandte Chemie International Edition | 1433-7851 | Q1 | 14 |
| 213 | Arabian Journal for Science and Engineering | 1319-8025 | Q1 | 14 |
| 214 | Bioresource Technology | 0960-8524 | Q1 | 14 |
| 215 | Chemical Physics Letters | 0009-2614 | Q2 | 14 |
| 216 | Computational Materials Science | 0927-0256 | Q1 | 14 |
| 217 | Digital Signal Processing | 1051-2004 | Q2 | 14 |
| 218 | European Journal of Inorganic Chemistry | 1099-0682 | Q3 | 14 |
| 219 | IEEE Embedded Systems Letters | 1943-0663 | Q2 | 14 |
| 220 | IEEE Transactions on Industrial Electronics | 0278-0046 | Q1 | 14 |
| 221 | Inorganica Chimica Acta | 0020-1693 | Q2 | 14 |
| 222 | Journal of Public Affairs | 1472-3891 | Q2 | 14 |
| 223 | Journal of materials research/Pratt's guide to venture capital sources | 0884-1616 | Q2 | 14 |
| 224 | Metallurgical and Materials Transactions A | 1073-5623 | Q1 | 14 |
| 225 | Pattern Recognition | 0031-3203 | Q1 | 14 |
| 226 | Process Safety and Environmental Protection | 0263-8762 | Q2 | 14 |
| 227 | Separation and Purification Technology | 1383-5866 | Q1 | 14 |
| 228 | The Analyst | 0003-2654 | Q2 | 14 |
| 229 | The Journal of Chemical Physics | 0021-9606 | Q1 | 14 |
| 230 | physica status solidi (a) | 0031-8965 | Q2 | 14 |
| 231 | ACS Biomaterials Science & Engineering | 2373-9878 | Q1 | 13 |
| 232 | ACS Catalysis | 2155-5435 | Q1 | 13 |
| 233 | AEU - International Journal of Electronics and Communications | 1434-8411 | Q2 | 13 |
| 234 | ASME Journal of Heat and Mass Transfer | 0022-1481 | Q2 | 13 |
| 235 | Arabian Journal of Geosciences | 1866-7511 | — | 13 |
| 236 | Carbon | 0008-6223 | Q1 | 13 |
| 237 | Crystal Growth & Design | 1528-7483 | Q2 | 13 |
| 238 | Electrical Engineering | 0003-9039 | Q2 | 13 |
| 239 | Engineering Structures | 0141-0296 | Q1 | 13 |
| 240 | Environmental Research | 0013-9351 | Q1 | 13 |
| 241 | IEEE Antennas and Wireless Propagation Letters | 1536-1225 | Q1 | 13 |
| 242 | IEEE Journal of Emerging and Selected Topics in Industrial Electronics | 2687-9735 | Q1 | 13 |
| 243 | Inorganic Chemistry Communications | 1387-7003 | Q1 | 13 |
| 244 | Journal of Physics and Chemistry of Solids | 0022-3697 | Q1 | 13 |
| 245 | Journal of Tribology | 0742-4787 | Q2 | 13 |
| 246 | Linear and Multilinear Algebra | 0308-1087 | Q1 | 13 |
| 247 | Materials Science in Semiconductor Processing | 1369-8001 | Q1 | 13 |
| 248 | Microelectronics Reliability | 0026-2714 | Q2 | 13 |
| 249 | Proceedings of the Institution of Mechanical Engineers Part L Journal of Materials Design and Applications | 1464-4207 | Q2 | 13 |
| 250 | Quarterly Journal of the Royal Meteorological Society | 0035-9009 | Q1 | 13 |
| 251 | SN Applied Sciences | 2523-3963 | — | 13 |
| 252 | Soil Dynamics and Earthquake Engineering | 0267-7261 | Q1 | 13 |
| 253 | Surface and Coatings Technology | 0257-8972 | Q1 | 13 |
| 254 | Tetrahedron Letters | 0040-4039 | Q3 | 13 |
| 255 | ACS Chemical Neuroscience | 1948-7193 | Q1 | 12 |
| 256 | Advanced Materials Interfaces | 2196-7350 | Q1 | 12 |
| 257 | Advanced Theory and Simulations | 2513-0390 | Q1 | 12 |
| 258 | Bioresource Technology Reports | 2589-014X | Q1 | 12 |
| 259 | Climate Dynamics | 0930-7575 | Q1 | 12 |
| 260 | Coordination Chemistry Reviews | 0010-8545 | Q1 | 12 |
| 261 | Engineering Failure Analysis | 1350-6307 | Q1 | 12 |
| 262 | Environmental Earth Sciences | 1866-6280 | Q1 | 12 |
| 263 | European Journal of Mechanics - A/Solids | 0997-7538 | Q1 | 12 |
| 264 | Global Challenges | 2056-6646 | Q1 | 12 |
| 265 | IEEE Open Journal of the Communications Society | 2644-125X | Q1 | 12 |
| 266 | IEEE Transactions on Aerospace and Electronic Systems | 0018-9251 | Q1 | 12 |
| 267 | IEEE Transactions on Cognitive Communications and Networking | 2332-7731 | Q1 | 12 |
| 268 | IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems | 0278-0070 | Q1 | 12 |
| 269 | IEEE Transactions on Smart Grid | 1949-3053 | Q1 | 12 |
| 270 | Integrated ferroelectrics | 1026-7530 | Q4 | 12 |
| 271 | International Journal of Communication Systems | 1074-5351 | Q2 | 12 |
| 272 | International Journal of Electrical Power & Energy Systems | 0142-0615 | Q1 | 12 |
| 273 | International Journal of Mechanical Sciences | 0020-7403 | Q1 | 12 |
| 274 | International Journal of Mechanics and Materials in Design | 1569-1713 | Q1 | 12 |
| 275 | Journal of Biological Chemistry | 0021-9258 | Q1 | 12 |
| 276 | Materials Research Bulletin | 0025-5408 | Q1 | 12 |
| 277 | Mechanical Systems and Signal Processing | 0888-3270 | Q1 | 12 |
| 278 | Mechanics Based Design of Structures and Machines | 0360-1218 | Q2 | 12 |
| 279 | Metals and Materials International | 1225-9438 | Q1 | 12 |
| 280 | Optics & Laser Technology | 0030-3992 | Q1 | 12 |
| 281 | Physical Review A | 0556-2791 | Q1 | 12 |
| 282 | Solar Physics | 0038-0938 | Q2 | 12 |
| 283 | Sustainable Energy Technologies and Assessments | 2213-1388 | Q1 | 12 |
| 284 | Tribology International | 0301-679X | Q1 | 12 |
| 285 | Virology | 0042-6822 | Q2 | 12 |
| 286 | Advanced Sustainable Systems | 2366-7486 | Q1 | 11 |
| 287 | Advanced Synthesis & Catalysis | 1615-4150 | Q1 | 11 |
| 288 | Archives of Civil and Mechanical Engineering | 1644-9665 | Q1 | 11 |
| 289 | ChemPhysChem | 1439-4235 | Q2 | 11 |
| 290 | Defence Science Journal | 0011-748X | Q2 | 11 |
| 291 | Engineering Fracture Mechanics | 0013-7944 | Q1 | 11 |
| 292 | IEEE Electron Device Letters | 0741-3106 | Q1 | 11 |
| 293 | IEEE Transactions on Fuzzy Systems | 1063-6706 | Q1 | 11 |
| 294 | IET Communications | 1751-8628 | Q2 | 11 |
| 295 | International Journal of Geomechanics | 1532-3641 | Q1 | 11 |
| 296 | Journal of Cellular Biochemistry | 0730-2312 | Q2 | 11 |
| 297 | Journal of Chemical Sciences | 0253-4134 | Q3 | 11 |
| 298 | Journal of Computational Science | 1877-7503 | Q1 | 11 |
| 299 | Journal of Nanoscience and Nanotechnology | 1533-4880 | — | 11 |
| 300 | Journal of the Brazilian Society of Mechanical Sciences and Engineering | 1678-5878 | Q2 | 11 |
| 301 | Materials Characterization | 1044-5803 | Q1 | 11 |
| 302 | Molecular Neurobiology | 0893-7648 | Q1 | 11 |
| 303 | Nature | 0028-0836 | Q1 | 11 |
| 304 | Nonlinear Dynamics | 0924-090X | Q1 | 11 |
| 305 | Optics Communications | 0030-4018 | Q2 | 11 |
| 306 | Physics Education | 0031-9120 | Q2 | 11 |
| 307 | Progress in Additive Manufacturing | 2363-9512 | Q1 | 11 |
| 308 | Renewable Energy | 0960-1481 | Q1 | 11 |
| 309 | Road Materials and Pavement Design | 1468-0629 | Q1 | 11 |
| 310 | SN Computer Science | 2661-8907 | Q2 | 11 |
| 311 | Sensors | 1424-8220 | Q1 | 11 |
| 312 | Vacuum | 0042-207X | Q1 | 11 |
| 313 | Water Air & Soil Pollution | 0049-6979 | Q2 | 11 |
| 314 | 3 Biotech | 2190-572X | Q1 | 10 |
| 315 | ACS Applied Polymer Materials | 2637-6105 | Q1 | 10 |
| 316 | Acta Geophysica | 0001-5725 | Q2 | 10 |
| 317 | Applied Mathematics and Computation | 0096-3003 | Q1 | 10 |
| 318 | Asian Journal of Control | 1561-8625 | Q2 | 10 |
| 319 | Atmosphere | 2073-4433 | Q2 | 10 |
| 320 | ChemPhotoChem | 2367-0932 | Q2 | 10 |
| 321 | Dynamics of Atmospheres and Oceans | 0377-0265 | Q2 | 10 |
| 322 | Energies | 1996-1073 | Q1 | 10 |
| 323 | IEEE Transactions on Emerging Topics in Computational Intelligence | 2471-285X | Q1 | 10 |
| 324 | IEEE Transactions on Geoscience and Remote Sensing | 0196-2892 | Q1 | 10 |
| 325 | IEEE Transactions on Industrial Informatics | 1551-3203 | Q1 | 10 |
| 326 | International Communications in Heat and Mass Transfer | 0735-1933 | Q1 | 10 |
| 327 | International Journal of Emerging Electric Power Systems | 1553-779X | Q3 | 10 |
| 328 | International Journal of Pavement Engineering | 1029-8436 | Q1 | 10 |
| 329 | JOM | 0148-6608 | Q2 | 10 |
| 330 | Journal of Natural Fibers | 1544-046X | Q2 | 10 |
| 331 | Journal of Water Process Engineering | 2214-7144 | Q1 | 10 |
| 332 | Linear Algebra and its Applications | 0024-3795 | Q1 | 10 |
| 333 | MAUSAM | 0252-9416 | Q3 | 10 |
| 334 | Manufacturing Letters | 2213-8463 | Q2 | 10 |
| 335 | Microwave and Optical Technology Letters | 0895-2477 | Q3 | 10 |
| 336 | Molecular Catalysis | 2468-8231 | Q2 | 10 |
| 337 | Nanoscale Advances | 2516-0230 | Q1 | 10 |
| 338 | Optics Letters | 0146-9592 | Q1 | 10 |
| 339 | PLoS ONE | 1932-6203 | Q1 | 10 |
| 340 | Palaeogeography Palaeoclimatology Palaeoecology | 0031-0182 | Q1 | 10 |
| 341 | Physica B Condensed Matter | 0921-4526 | Q2 | 10 |
| 342 | Physica E Low-dimensional Systems and Nanostructures | 1386-9477 | Q2 | 10 |
| 343 | Polyhedron | 0277-5387 | Q3 | 10 |
| 344 | Soft Computing | 1432-7643 | Q2 | 10 |
| 345 | Soft Matter | 1744-683X | Q2 | 10 |
| 346 | Superlattices and Microstructures | 0749-6036 | — | 10 |
| 347 | The Visual Computer | 0178-2789 | Q2 | 10 |
| 348 | Bulletin of Materials Science | 0250-4707 | Q3 | 9 |
| 349 | ChemPlusChem | 2192-6506 | Q2 | 9 |
| 350 | Current Science | 0011-3891 | Q3 | 9 |
| 351 | Energy Advances | 2753-1457 | Q1 | 9 |
| 352 | Frontiers in Psychology | 1664-1078 | Q1 | 9 |
| 353 | IEEE Transactions on Computational Social Systems | 2329-924X | Q1 | 9 |
| 354 | Industrial & Engineering Chemistry Research | 0888-5885 | Q1 | 9 |
| 355 | Information Sciences | 0020-0255 | Q1 | 9 |
| 356 | Integration | 0167-9260 | Q2 | 9 |
| 357 | International Journal of Advances in Engineering Sciences and Applied Mathematics | 0975-0770 | — | 9 |
| 358 | International Journal of Applied Mechanics | 1758-8251 | Q2 | 9 |
| 359 | International Journal of Environmental Science and Technology | 1735-1472 | Q1 | 9 |
| 360 | International Journal of Pressure Vessels and Piping | 0308-0161 | Q1 | 9 |
| 361 | International Journal of Systems Assurance Engineering and Management | 0975-6809 | Q2 | 9 |
| 362 | International Journal of Systems Science | 0020-7721 | Q1 | 9 |
| 363 | Journal of Colloid and Interface Science | 0021-9797 | Q1 | 9 |
| 364 | Journal of Drug Delivery Science and Technology | 1773-2247 | Q2 | 9 |
| 365 | Journal of Environmental Engineering | 0733-9372 | Q2 | 9 |
| 366 | Journal of Intelligent Material Systems and Structures | 1045-389X | Q2 | 9 |
| 367 | Journal of Materials Processing Technology | 0924-0136 | Q1 | 9 |
| 368 | Journal of Mathematical Analysis and Applications | 0022-247X | Q1 | 9 |
| 369 | Journal of the Australian Ceramic Society | 0004-881X | Q3 | 9 |
| 370 | Manufacturing Technology Today (MTT) | 0972-7396 | — | 9 |
| 371 | Metallography Microstructure and Analysis | 2192-9262 | Q2 | 9 |
| 372 | New Journal of Physics | 1367-2630 | Q1 | 9 |
| 373 | Optik | 0030-4026 | Q2 | 9 |
| 374 | Organic Letters | 1523-7052 | Q1 | 9 |
| 375 | Physical Communication | 1874-4907 | Q2 | 9 |
| 376 | Renewable and Sustainable Energy Reviews | 1364-0321 | Q1 | 9 |
| 377 | SAR and QSAR in environmental research | 1026-776X | Q3 | 9 |
| 378 | The European Physical Journal B | 1434-6028 | Q3 | 9 |
| 379 | The Journal of Physical Chemistry A | 1089-5639 | Q2 | 9 |
| 380 | Transactions of Indian National Academy of Engineering | 2662-5415 | — | 9 |
| 381 | The international archives of the photogrammetry, remote sensing and spatial information sciences/International archives of the photogrammetry, remote sensing and spatial information sciences | 1682-1750 | — | 9 |
| 382 | Advanced Optical Materials | 2195-1071 | Q1 | 8 |
| 383 | Advances in High Energy Physics | 1687-7357 | Q3 | 8 |
| 384 | Analytical Chemistry | 0003-2700 | Q1 | 8 |
| 385 | Biochemical and Biophysical Research Communications | 0006-291X | Q2 | 8 |
| 386 | CSI Transactions on ICT | 2277-9078 | — | 8 |
| 387 | Chemical Physics | 0301-0104 | Q2 | 8 |
| 388 | Composites Part B Engineering | 1359-8368 | Q1 | 8 |
| 389 | Electronics Letters | 0013-5194 | Q3 | 8 |
| 390 | Energy Reports | 2352-4847 | Q1 | 8 |
| 391 | Environment Development and Sustainability | 1387-585X | Q1 | 8 |
| 392 | Frontiers in Earth Science | 2296-6463 | Q2 | 8 |
| 393 | Frontiers in Microbiology | 1664-302X | Q1 | 8 |
| 394 | Future Generation Computer Systems | 0167-739X | Q1 | 8 |
| 395 | Green Chemistry | 1463-9262 | Q1 | 8 |
| 396 | Heat Transfer | 2688-4534 | Q2 | 8 |
| 397 | IEEE Transactions on Artificial Intelligence | 2691-4581 | Q1 | 8 |
| 398 | IEEE Transactions on Cognitive and Developmental Systems | 2379-8920 | Q1 | 8 |
| 399 | IEEE Transactions on Device and Materials Reliability | 1530-4388 | Q2 | 8 |
| 400 | IETE Technical Review | 0256-4602 | Q2 | 8 |
| 401 | Information Fusion | 1566-2535 | Q1 | 8 |
| 402 | Intermetallics | 0966-9795 | Q1 | 8 |
| 403 | International Journal of Applied Ceramic Technology | 1546-542X | Q2 | 8 |
| 404 | Japanese Journal of Applied Physics | 0021-4922 | Q3 | 8 |
| 405 | Journal of Ambient Intelligence and Humanized Computing | 1868-5137 | Q2 | 8 |
| 406 | Journal of Electronic Imaging | 1017-9909 | Q3 | 8 |
| 407 | Journal of Glaciology | 0022-1430 | Q1 | 8 |
| 408 | Journal of Hydrologic Engineering | 1084-0699 | Q2 | 8 |
| 409 | Journal of Industrial and Engineering Chemistry | 1226-086X | Q1 | 8 |
| 410 | Journal of The Electrochemical Society | 0013-4651 | Q1 | 8 |
| 411 | Materials Horizons | 2051-6347 | Q1 | 8 |
| 412 | Materials Science and Technology | 0267-0836 | Q2 | 8 |
| 413 | Modeling Earth Systems and Environment | 2363-6203 | Q1 | 8 |
| 414 | Next Materials | 2949-8228 | Q1 | 8 |
| 415 | Nonautonomous Dynamical Systems | 2353-0626 | Q3 | 8 |
| 416 | Optical and Quantum Electronics | 0306-8919 | — | 8 |
| 417 | Organometallics | 0276-7333 | Q2 | 8 |
| 418 | Physics and Chemistry of the Earth Parts A/B/C | 1474-7065 | Q1 | 8 |
| 419 | Polymer | 0032-3861 | Q1 | 8 |
| 420 | Proceedings of the Human Factors and Ergonomics Society Annual Meeting | 0163-5182 | — | 8 |
| 421 | Qualitative Theory of Dynamical Systems | 1575-5460 | Q1 | 8 |
| 422 | Results in Engineering | 2590-1230 | Q1 | 8 |
| 423 | Signal Image and Video Processing | 1863-1703 | Q2 | 8 |
| 424 | Solar Energy Materials and Solar Cells | 0927-0248 | Q1 | 8 |
| 425 | Sustainability | 2071-1050 | Q1 | 8 |
| 426 | Theoretical and Applied Fracture Mechanics | 0167-8442 | Q1 | 8 |
| 427 | Water | 2073-4441 | Q1 | 8 |
| 428 | Water Resources Research | 0043-1397 | Q1 | 8 |
| 429 | Water Science & Technology | 0273-1223 | Q2 | 8 |
| 430 | physica status solidi (RRL) - Rapid Research Letters | 1862-6254 | Q2 | 8 |
| 431 | Advanced Materials Technologies | 2365-709X | Q1 | 7 |
| 432 | Alexandria Engineering Journal | 1110-0168 | Q1 | 7 |
| 433 | Annals of Operations Research | 0254-5330 | Q1 | 7 |
| 434 | Applied Acoustics | 0003-682X | Q1 | 7 |
| 435 | Applied Mathematical Modelling | 0307-904X | Q1 | 7 |
| 436 | Archives of Biochemistry and Biophysics | 0003-9861 | Q1 | 7 |
| 437 | Asia-Pacific Journal of Regional Science | 2509-7946 | Q2 | 7 |
| 438 | Biomaterials Science | 2047-4830 | Q1 | 7 |
| 439 | Bulletin of the Australian Mathematical Society | 0004-9727 | Q2 | 7 |
| 440 | Cleaner Engineering and Technology | 2666-7908 | Q1 | 7 |
| 441 | Composites Part C Open Access | 2666-6820 | Q1 | 7 |
| 442 | Computer Networks | 1389-1286 | Q1 | 7 |
| 443 | Crystals | 2073-4352 | Q2 | 7 |
| 444 | Diamond and Related Materials | 0925-9635 | Q1 | 7 |
| 445 | Earth Systems and Environment | 2509-9426 | Q1 | 7 |
| 446 | Electronics | 2079-9292 | Q2 | 7 |
| 447 | Environmental Pollution | 0269-7491 | Q1 | 7 |
| 448 | Ferroelectrics | 0015-0193 | Q4 | 7 |
| 449 | Frontiers in Immunology | 1664-3224 | Q1 | 7 |
| 450 | Global and Planetary Change | 0921-8181 | Q1 | 7 |
| 451 | IEEE Geoscience and Remote Sensing Letters | 1545-598X | Q1 | 7 |
| 452 | IEEE Journal of Emerging and Selected Topics in Power Electronics | 2168-6777 | Q1 | 7 |
| 453 | IEEE Transactions on Green Communications and Networking | 2473-2400 | Q1 | 7 |
| 454 | IEEE Transactions on Intelligent Transportation Systems | 1524-9050 | Q1 | 7 |
| 455 | IEEE Transactions on Network and Service Management | 1932-4537 | Q1 | 7 |
| 456 | IEEE photonics journal | 1943-0647 | Q2 | 7 |
| 457 | International Immunopharmacology | 1567-5769 | Q1 | 7 |
| 458 | International Journal of Computational Methods | 0219-8762 | Q2 | 7 |
| 459 | International Journal of Structural Stability and Dynamics | 0219-4554 | Q1 | 7 |
| 460 | JACS Au | 2691-3704 | Q1 | 7 |
| 461 | Journal of Applied Biomedicine | 0208-5216 | Q1 | 7 |
| 462 | Journal of Composite Materials | 0021-9983 | Q2 | 7 |
| 463 | Journal of Non-Crystalline Solids | 0022-3093 | Q2 | 7 |
| 464 | Journal of Optics | 0150-536X | Q2 | 7 |
| 465 | Journal of Physics B Atomic Molecular and Optical Physics | 0953-4075 | Q2 | 7 |
| 466 | Journal of Solid State Chemistry | 0022-4596 | Q2 | 7 |
| 467 | Journal of Sustainable Cement-Based Materials | 2165-0373 | Q1 | 7 |
| 468 | Journal of the European Ceramic Society | 0955-2219 | Q1 | 7 |
| 469 | Journal of the Optical Society of America B | 0740-3224 | Q2 | 7 |
| 470 | Knowledge-Based Systems | 0950-7051 | Q1 | 7 |
| 471 | Landslides | 1612-510X | Q1 | 7 |
| 472 | Mechanics of Materials | 0167-6636 | Q1 | 7 |
| 473 | Microporous and Mesoporous Materials | 1387-1811 | Q1 | 7 |
| 474 | Nano Letters | 1530-6984 | Q1 | 7 |
| 475 | Numerical Algorithms | 1017-1398 | Q1 | 7 |
| 476 | Plasmonics | 1557-1955 | Q2 | 7 |
| 477 | Pramana | 0304-4289 | Q3 | 7 |
| 478 | Proceedings of the Institution of Mechanical Engineers Part B Journal of Engineering Manufacture | 0954-4054 | Q2 | 7 |
| 479 | Proceedings of the International Astronomical Union | 1743-9213 | Q4 | 7 |
| 480 | Review of Scientific Instruments | 0034-6748 | Q2 | 7 |
| 481 | Small Methods | 2366-9608 | Q1 | 7 |
| 482 | Smart Materials and Structures | 0964-1726 | Q2 | 7 |
| 483 | Solid State Communications | 0038-1098 | Q2 | 7 |
| 484 | Spectrochimica Acta Part A Molecular and Biomolecular Spectroscopy | 1386-1425 | Q1 | 7 |
| 485 | Symmetry | 2073-8994 | Q2 | 7 |
| 486 | The Journal of Analysis | 0971-3611 | Q2 | 7 |
| 487 | The Journal of Supercomputing | 0920-8542 | Q2 | 7 |
| 488 | Transactions on Emerging Telecommunications Technologies | 2161-3915 | Q2 | 7 |
| 489 | Wear | 0043-1648 | Q1 | 7 |
| 490 | ACM Computing Surveys | 0360-0300 | Q1 | 6 |
| 491 | ACS Nano | 1936-0851 | Q1 | 6 |
| 492 | ACS Sensors | 2379-3694 | Q1 | 6 |
| 493 | Analog Integrated Circuits and Signal Processing | 0925-1030 | Q3 | 6 |
| 494 | Astronomy and Astrophysics | 0004-6361 | Q1 | 6 |
| 495 | Atmospheric Environment | 1352-2310 | Q1 | 6 |
| 496 | Biosensors and Bioelectronics | 0956-5663 | Q1 | 6 |
| 497 | Bulletin of Engineering Geology and the Environment | 0074-1612 | Q1 | 6 |
| 498 | ChemInform | 0009-2975 | — | 6 |
| 499 | ChemSusChem | 1864-5631 | Q1 | 6 |
| 500 | Chemical Engineering and Processing - Process Intensification | 0255-2701 | Q1 | 6 |
| 501 | Chinese Journal of Physics | 0577-9073 | Q2 | 6 |
| 502 | Communication in Statistics- Theory and Methods | 0361-0926 | Q3 | 6 |
| 503 | Computational Biology and Chemistry | 1476-9271 | Q2 | 6 |
| 504 | Computational Urban Science | 2730-6852 | Q1 | 6 |
| 505 | Computer Methods and Programs in Biomedicine | 0169-2607 | Q1 | 6 |
| 506 | Computers & Security | 0167-4048 | Q1 | 6 |
| 507 | Computers and Electronics in Agriculture | 0168-1699 | Q1 | 6 |
| 508 | Desalination | 0011-9164 | Q1 | 6 |
| 509 | Discover Sustainability | 2662-9984 | Q1 | 6 |
| 510 | Discrete Mathematics | 0012-365X | Q1 | 6 |
| 511 | Dyes and Pigments | 0143-7208 | Q2 | 6 |
| 512 | Environmental Geochemistry and Health | 0269-4042 | Q1 | 6 |
| 513 | Environmental Quality Management | 1088-1913 | Q3 | 6 |
| 514 | Environmental Technology | 0959-3330 | Q2 | 6 |
| 515 | Environmental Technology & Innovation | 2352-1864 | Q1 | 6 |
| 516 | Frontiers in Molecular Biosciences | 2296-889X | Q1 | 6 |
| 517 | IEEE Transactions on Automation Science and Engineering | 1545-5955 | Q1 | 6 |
| 518 | IEEE Transactions on Biometrics Behavior and Identity Science | 2637-6407 | Q1 | 6 |
| 519 | IEEE Transactions on Emerging Topics in Computing | 2168-6750 | Q1 | 6 |
| 520 | IEEE Transactions on Transportation Electrification | 2332-7782 | Q1 | 6 |
| 521 | IETE Journal of Research | 0377-2063 | Q3 | 6 |
| 522 | Image and Vision Computing | 0262-8856 | Q1 | 6 |
| 523 | Indian Journal of Physics | 0019-5480 | Q3 | 6 |
| 524 | International Journal of Energy Research | 0363-907X | Q1 | 6 |
| 525 | International Journal of Geosynthetics and Ground Engineering | 2199-9260 | Q2 | 6 |
| 526 | International Journal of Molecular Sciences | 1422-0067 | Q1 | 6 |
| 527 | International Journal of Multiphase Flow | 0301-9322 | Q1 | 6 |
| 528 | International Journal of Precision Engineering and Manufacturing | 1229-8557 | Q2 | 6 |
| 529 | International Journal of Refractory Metals and Hard Materials | 0263-4368 | Q1 | 6 |
| 530 | Journal of Earthquake Engineering | 1363-2469 | Q1 | 6 |
| 531 | Journal of Geophysical Research Space Physics | 2169-9380 | Q1 | 6 |
| 532 | Journal of Geotechnical and Geoenvironmental Engineering | 1090-0241 | Q1 | 6 |
| 533 | Journal of High Energy Astrophysics | 2214-4048 | Q1 | 6 |
| 534 | Journal of Information Security and Applications | 2214-2126 | Q1 | 6 |
| 535 | Journal of Laser Applications | 1042-346X | Q2 | 6 |
| 536 | Journal of Magnesium and Alloys | 2213-9567 | Q1 | 6 |
| 537 | Journal of Mechanics in Medicine and Biology | 0219-5194 | Q4 | 6 |
| 538 | Journal of Physics G Nuclear and Particle Physics | 0954-3899 | Q1 | 6 |
| 539 | Journal of Raman Spectroscopy | 0377-0486 | Q3 | 6 |
| 540 | Journal of Rock Mechanics and Geotechnical Engineering | 1674-7755 | Q1 | 6 |
| 541 | Journal of Solid State Electrochemistry | 1432-8488 | Q2 | 6 |
| 542 | Journal of Thermal Analysis and Calorimetry | 1388-6150 | Q2 | 6 |
| 543 | Journal of Thermal Science and Engineering Applications | 1948-5085 | Q2 | 6 |
| 544 | Journal of the Franklin Institute | 0016-0032 | Q1 | 6 |
| 545 | Journal of the Indian Chemical Society | 0019-4522 | Q2 | 6 |
| 546 | Macromolecular Chemistry and Physics | 1022-1352 | Q2 | 6 |
| 547 | Materials Today Chemistry | 2468-5194 | Q1 | 6 |
| 548 | Mathematics | 2227-7390 | Q2 | 6 |
| 549 | Mathematics and Mechanics of Solids | 1081-2865 | Q2 | 6 |
| 550 | Medical & Biological Engineering & Computing | 0140-0118 | Q2 | 6 |
| 551 | Microelectronic Engineering | 0167-9317 | Q2 | 6 |
| 552 | Micromachines | 2072-666X | Q2 | 6 |
| 553 | Molecular Systems Design & Engineering | 2058-9689 | Q1 | 6 |
| 554 | Monthly Notices of the Royal Astronomical Society Letters | 1745-3925 | Q1 | 6 |
| 555 | Nano Express | 2632-959X | Q2 | 6 |
| 556 | Next research. | 3050-4759 | — | 6 |
| 557 | Numerical Heat Transfer Part A Applications | 1040-7782 | Q2 | 6 |
| 558 | Organic Chemistry Frontiers | 2052-4110 | Q1 | 6 |
| 559 | Organic Electronics | 1566-1199 | Q2 | 6 |
| 560 | Pattern Analysis and Applications | 1433-7541 | Q2 | 6 |
| 561 | Physical Review Materials | 2475-9953 | Q1 | 6 |
| 562 | Remote Sensing | 2072-4292 | Q1 | 6 |
| 563 | Solid State Sciences | 1293-2558 | Q2 | 6 |
| 564 | Springer tracts in electrical and electronics engineering | 2731-4200 | — | 6 |
| 565 | Synthetic Metals | 0379-6779 | Q1 | 6 |
| 566 | The Journal of the Acoustical Society of America | 0001-4966 | Q1 | 6 |
| 567 | Water Environment Research | 0043-1303 | Q2 | 6 |
| 568 | e-Prime - Advances in Electrical Engineering Electronics and Energy | 2772-6711 | Q1 | 6 |
| 569 | ACM Transactions on Multimedia Computing Communications and Applications | 1551-6857 | Q1 | 5 |
| 570 | ACS ES&T Engineering | 2690-0645 | Q1 | 5 |
| 571 | ACS Energy Letters | 2380-8195 | Q1 | 5 |
| 572 | ACS Infectious Diseases | 2373-8227 | Q1 | 5 |
| 573 | ACS Photonics | 2330-4022 | Q1 | 5 |
| 574 | APL Electronic Devices | 2995-8423 | — | 5 |
| 575 | Ad Hoc Networks | 1570-8705 | Q1 | 5 |
| 576 | Advanced Science | 2198-3844 | Q1 | 5 |
| 577 | Advances in Cancer Biology - Metastasis | 2667-3940 | Q3 | 5 |
| 578 | Aerosol and Air Quality Research | 1680-8584 | Q2 | 5 |
| 579 | Aerospace Science and Technology | 1270-9638 | Q1 | 5 |
| 580 | Algal Research | 2211-9264 | Q1 | 5 |
| 581 | Applied Energy | 0306-2619 | Q1 | 5 |
| 582 | Applied Sciences | 2076-3417 | Q2 | 5 |
| 583 | Archive of Applied Mechanics | 0939-1533 | Q2 | 5 |
| 584 | Archives of Computational Methods in Engineering | 1134-3060 | Q1 | 5 |
| 585 | Archives of Microbiology | 0003-9276 | Q2 | 5 |
| 586 | BMC Public Health | 1471-2458 | Q1 | 5 |
| 587 | Batteries & Supercaps | 2566-6223 | Q1 | 5 |
| 588 | Biodegradation | 0923-9820 | Q1 | 5 |
| 589 | Biomacromolecules | 1525-7797 | Q1 | 5 |
| 590 | Biomass and Bioenergy | 0961-9534 | Q1 | 5 |
| 591 | Biosensors | 2079-6374 | Q1 | 5 |
| 592 | CATENA | 0341-8162 | Q1 | 5 |
| 593 | Case Studies in Construction Materials | 2214-5095 | Q1 | 5 |
| 594 | Chemical Physics Impact | 2667-0224 | Q1 | 5 |
| 595 | Cognitive Computation | 1866-9956 | Q1 | 5 |
| 596 | Colloids and Surfaces A Physicochemical and Engineering Aspects | 0927-7757 | Q1 | 5 |
| 597 | Communications Earth & Environment | 2662-4435 | Q1 | 5 |
| 598 | Communications in Statistics - Simulation and Computation | 0361-0918 | Q2 | 5 |
| 599 | Computational and Theoretical Chemistry | 2210-271X | Q2 | 5 |
| 600 | Computers & Fluids | 0045-7930 | Q1 | 5 |
| 601 | Discrete and Continuous Dynamical Systems - S | 1937-1179 | Q2 | 5 |
| 602 | Displays | 0141-9382 | Q2 | 5 |
| 603 | ECS Journal of Solid State Science and Technology | 2162-8769 | Q3 | 5 |
| 604 | Electric Power Components and Systems | 1532-5008 | Q2 | 5 |
| 605 | Energy | 0360-5442 | Q1 | 5 |
| 606 | Energy Conversion and Economics | 2634-1581 | — | 5 |
| 607 | Energy RESEARCH LETTERS | 2652-6433 | Q2 | 5 |
| 608 | Entropy | 1099-4300 | Q2 | 5 |
| 609 | Estuarine Coastal and Shelf Science | 0272-7714 | Q1 | 5 |
| 610 | Fibers and Polymers | 1229-9197 | Q2 | 5 |
| 611 | Filomat | 0354-5180 | Q2 | 5 |
| 612 | Frontiers in Pharmacology | 1663-9812 | Q1 | 5 |
| 613 | Future Medicinal Chemistry | 1756-8919 | Q3 | 5 |
| 614 | Gene | 0378-1119 | Q2 | 5 |
| 615 | Geomatics Natural Hazards and Risk | 1947-5705 | Q1 | 5 |
| 616 | Healthcare Technology Letters | 2053-3713 | Q3 | 5 |
| 617 | Humanities and Social Sciences Communications | 2055-1045 | Q1 | 5 |
| 618 | Hydrological Processes | 0885-6087 | Q1 | 5 |
| 619 | Hydrological Sciences Journal | 0262-6667 | Q1 | 5 |
| 620 | IEEE Design and Test | 2168-2356 | Q2 | 5 |
| 621 | IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing | 1939-1404 | Q1 | 5 |
| 622 | IEEE Signal Processing Letters | 1070-9908 | Q1 | 5 |
| 623 | IEEE Transactions on Components Packaging and Manufacturing Technology | 2156-3950 | Q1 | 5 |
| 624 | IEEE Transactions on Dependable and Secure Computing | 1545-5971 | Q1 | 5 |
| 625 | IEEE Transactions on Magnetics | 0018-9464 | Q2 | 5 |
| 626 | IEEE Transactions on Neural Networks and Learning Systems | 2162-237X | Q1 | 5 |
| 627 | IEEE Transactions on Power Electronics | 0885-8993 | Q1 | 5 |
| 628 | IEEE Transactions on Power Systems | 0885-8950 | Q1 | 5 |
| 629 | IEEE Transactions on Sustainable Energy | 1949-3029 | Q1 | 5 |
| 630 | IET Biometrics | 2047-4938 | Q2 | 5 |
| 631 | IET Energy Systems Integration | 2516-8401 | Q2 | 5 |
| 632 | Indian Journal of Pure and Applied Mathematics | 0019-5588 | Q3 | 5 |
| 633 | Inorganic Chemistry Frontiers | 2052-1545 | Q1 | 5 |
| 634 | International Biodeterioration & Biodegradation | 0964-8305 | Q2 | 5 |
| 635 | International Journal of Disaster Risk Reduction | 2212-4209 | Q1 | 5 |
| 636 | International Journal of Hydromechatronics | 2515-0464 | Q1 | 5 |
| 637 | International Journal of Modern Physics E | 0218-3013 | Q2 | 5 |
| 638 | International Journal of Non-Linear Mechanics | 0020-7462 | Q1 | 5 |
| 639 | International Journal of Refrigeration | 0140-7007 | Q1 | 5 |
| 640 | International Journal of Remote Sensing | 0143-1161 | Q2 | 5 |
| 641 | International Journal of Solids and Structures | 0020-7683 | Q1 | 5 |
| 642 | International Journal of Steel Structures | 1598-2351 | Q3 | 5 |
| 643 | International Transactions on Electrical Energy Systems | 2050-7038 | Q2 | 5 |
| 644 | Journal of Alloys and Metallurgical Systems | 2949-9178 | Q1 | 5 |
| 645 | Journal of Applied Polymer Science | 0021-8995 | Q2 | 5 |
| 646 | Journal of Atmospheric and Solar-Terrestrial Physics | 1364-6826 | Q2 | 5 |
| 647 | Journal of CO2 Utilization | 2212-9820 | Q1 | 5 |
| 648 | Journal of Catalysis | 0021-9517 | Q1 | 5 |
| 649 | Journal of Chemical Information and Modeling | 1549-9596 | Q1 | 5 |
| 650 | Journal of Civil Structural Health Monitoring | 2190-5452 | Q1 | 5 |
| 651 | Journal of Computing and Information Science in Engineering | 1530-9827 | Q1 | 5 |
| 652 | Journal of Electroanalytical Chemistry | 1572-6657 | Q2 | 5 |
| 653 | Journal of Intelligent Manufacturing | 0956-5515 | Q1 | 5 |
| 654 | Journal of Manufacturing Science and Engineering | 1087-1357 | Q1 | 5 |
| 655 | Journal of Material Cycles and Waste Management | 1438-4957 | Q1 | 5 |
| 656 | Journal of Micromanufacturing | 2516-5984 | Q2 | 5 |
| 657 | Journal of Thermal Spray Technology | 1059-9630 | Q1 | 5 |
| 658 | Journal of the Mechanical Behavior of Materials | 0334-8938 | Q2 | 5 |
| 659 | Letters of the IEEE Computer Society | 2573-9689 | — | 5 |
| 660 | Life Sciences | 0024-3205 | Q1 | 5 |
| 661 | Lubricants | 2075-4442 | Q2 | 5 |
| 662 | MAPAN | 0970-3950 | Q3 | 5 |
| 663 | Marine Pollution Bulletin | 0025-326X | Q1 | 5 |
| 664 | Materials Science and Engineering C | 0928-4931 | — | 5 |
| 665 | Mathematics and Computers in Simulation | 0378-4754 | Q1 | 5 |
| 666 | Mechanism and Machine Theory | 0094-114X | Q1 | 5 |
| 667 | Meteorological Applications | 1350-4827 | Q2 | 5 |
| 668 | Micro & Nano Letters | 1750-0443 | Q2 | 5 |
| 669 | Microelectronics Journal | 1879-2391 | Q2 | 5 |
| 670 | Microprocessors and Microsystems | 0141-9331 | Q2 | 5 |
| 671 | Millennial Asia | 0976-3996 | Q1 | 5 |
| 672 | Molecular Diversity | 1381-1991 | Q2 | 5 |
| 673 | Molecular Immunology | 0161-5890 | Q2 | 5 |
| 674 | Molecular Therapy — Nucleic Acids | 2162-2531 | Q1 | 5 |
| 675 | Molecules | 1420-3049 | Q1 | 5 |
| 676 | Nano-Structures & Nano-Objects | 2352-507X | Q1 | 5 |
| 677 | Natural hazards and earth system sciences | 1561-8633 | Q1 | 5 |
| 678 | Optical Fiber Technology | 1068-5200 | Q2 | 5 |
| 679 | Results in Control and Optimization | 2666-7207 | Q1 | 5 |
| 680 | Solar RRL | 2367-198X | Q1 | 5 |
| 681 | Stochastic Environmental Research and Risk Assessment | 1436-3240 | Q1 | 5 |
| 682 | Structural Concrete | 1464-4177 | Q1 | 5 |
| 683 | Tetrahedron | 0040-4020 | Q3 | 5 |
| 684 | The Chemical Record | 1527-8999 | Q1 | 5 |
| 685 | The European Physical Journal Special Topics | 1951-6355 | Q2 | 5 |
| 686 | Transactions of the IMF | 0020-2967 | Q3 | 5 |
| 687 | Transportation in Developing Economies | 2199-9287 | — | 5 |
| 688 | Urban Climate | 2212-0955 | Q1 | 5 |
| 689 | physica status solidi (b) | 0370-1972 | Q3 | 5 |
| 690 | ACM Transactions on Computing for Healthcare | 2637-8051 | Q1 | 4 |
| 691 | ACM Transactions on Design Automation of Electronic Systems | 1084-4309 | Q2 | 4 |
| 692 | ACM Transactions on Embedded Computing Systems | 1539-9087 | Q2 | 4 |
| 693 | ACM Transactions on Internet Technology | 1533-5399 | Q1 | 4 |
| 694 | ACS Physical Chemistry Au | 2694-2445 | Q1 | 4 |
| 695 | AKCE International Journal of Graphs and Combinatorics | 0972-8600 | Q3 | 4 |
| 696 | AQUA - Water Infrastructure Ecosystems and Society | 0003-7214 | Q2 | 4 |
| 697 | Advanced Electronic Materials | 2199-160X | Q1 | 4 |
| 698 | Advanced Powder Technology | 0921-8831 | Q2 | 4 |
| 699 | Applied Catalysis B: Environmental | 0926-3373 | Q1 | 4 |
| 700 | Applied Microbiology and Biotechnology | 0175-7598 | Q1 | 4 |
| 701 | Applied Physics B | 0721-7269 | Q2 | 4 |
| 702 | Asian Journal of Chemistry | 0970-7077 | Q4 | 4 |
| 703 | Bioorganic Chemistry | 0045-2068 | Q1 | 4 |
| 704 | Biosensors and Bioelectronics X | 2590-1370 | Q2 | 4 |
| 705 | Bulletin des Sciences Mathématiques | 0007-4497 | Q1 | 4 |
| 706 | Canadian Journal of Chemistry | 0008-4042 | Q3 | 4 |
| 707 | Catalysis Today | 0920-5861 | Q1 | 4 |
| 708 | ChemElectroChem | 2196-0216 | Q2 | 4 |
| 709 | Chemistry & Biodiversity | 1612-1872 | Q2 | 4 |
| 710 | Classical and Quantum Gravity | 0264-9381 | Q1 | 4 |
| 711 | Cluster Computing | 1386-7857 | Q1 | 4 |
| 712 | Complex Variables and Elliptic Equations | 1747-6933 | Q2 | 4 |
| 713 | Complexity | 1076-2787 | Q2 | 4 |
| 714 | Computational Methods and Function Theory | 1617-9447 | Q2 | 4 |
| 715 | Computers & Mathematics with Applications | 0898-1221 | Q1 | 4 |
| 716 | Computers & Structures | 0045-7949 | Q1 | 4 |
| 717 | Current Applied Physics | 1567-1739 | Q2 | 4 |
| 718 | Differential Equations and Dynamical Systems | 0971-3514 | Q3 | 4 |
| 719 | Earth-Science Reviews | 0012-8252 | Q1 | 4 |
| 720 | Electronic Journal of Differential Equations | 1072-6691 | Q3 | 4 |
| 721 | Energy Conversion and Management | 0196-8904 | Q1 | 4 |
| 722 | Engineering Geology | 0013-7952 | Q1 | 4 |
| 723 | Enhanced heat transfer/Journal of enhanced heat transfer | 1026-5511 | Q3 | 4 |
| 724 | Environmental Processes | 2198-7491 | Q1 | 4 |
| 725 | Environmental Progress & Sustainable Energy | 1944-7442 | Q2 | 4 |
| 726 | Environmental Research Climate | 2752-5295 | Q1 | 4 |
| 727 | Environmental Research Letters | 1748-9326 | Q1 | 4 |
| 728 | Environmental Science & Technology | 0013-936X | Q1 | 4 |
| 729 | Environmental Science Advances | 2754-7000 | Q1 | 4 |
| 730 | Environmental Science Water Research & Technology | 2053-1400 | Q1 | 4 |
| 731 | Experimental Thermal and Fluid Science | 0894-1777 | Q1 | 4 |
| 732 | Expert Review of Vaccines | 1476-0584 | Q1 | 4 |
| 733 | FEBS Journal | 1742-464X | Q1 | 4 |
| 734 | Fractals | 0218-348X | Q1 | 4 |
| 735 | Frontiers in Cellular and Infection Microbiology | 2235-2988 | Q1 | 4 |
| 736 | Frontiers in Environmental Science | 2296-665X | Q1 | 4 |
| 737 | Frontiers in Physics | 2296-424X | Q2 | 4 |
| 738 | Frontiers of Structural and Civil Engineering | 2095-2430 | Q1 | 4 |
| 739 | Geological Journal | 0072-1050 | Q2 | 4 |
| 740 | Groundwater for Sustainable Development | 2352-801X | Q1 | 4 |
| 741 | Heat and Mass Transfer | 0947-7411 | Q2 | 4 |
| 742 | IEEE Journal of Quantum Electronics | 0018-9197 | Q2 | 4 |
| 743 | IEEE Letters on Electromagnetic Compatibility Practice and Applications | 2637-6423 | — | 4 |
| 744 | IEEE Transactions on Antennas and Propagation | 0018-926X | Q1 | 4 |
| 745 | IEEE Transactions on Computational Biology and Bioinformatics | 1545-5963 | Q2 | 4 |
| 746 | IEEE Transactions on Dielectrics and Electrical Insulation | 1070-9878 | Q1 | 4 |
| 747 | IEEE Transactions on Engineering Management | 0018-9391 | Q1 | 4 |
| 748 | IEEE Transactions on Human-Machine Systems | 2168-2291 | Q1 | 4 |
| 749 | IEEE Transactions on Information Forensics and Security | 1556-6013 | Q1 | 4 |
| 750 | IEEE Transactions on Molecular Biological and Multi-Scale Communications | 2332-7804 | Q2 | 4 |
| 751 | IEEE Transactions on Power Delivery | 0885-8977 | Q1 | 4 |
| 752 | IEEE Transactions on Wireless Communications | 1536-1276 | Q1 | 4 |
| 753 | IET Computers & Digital Techniques | 1751-8601 | Q4 | 4 |
| 754 | IET Image Processing | 1751-9659 | Q2 | 4 |
| 755 | IET Signal Processing | 1751-9675 | Q3 | 4 |
| 756 | IT Professional | 1520-9202 | Q2 | 4 |
| 757 | In Silico Research in Biomedicine | 3050-7871 | — | 4 |
| 758 | Inflammation Research | 1023-3830 | Q1 | 4 |
| 759 | Inorganics | 2304-6740 | Q2 | 4 |
| 760 | International Journal of Computer Mathematics | 0020-7160 | Q2 | 4 |
| 761 | International Journal of Materials Research (formerly Zeitschrift fuer Metallkunde) | 0044-3093 | Q3 | 4 |
| 762 | International Journal of Modelling Identification and Control | 1746-6172 | Q4 | 4 |
| 763 | International Journal of Modern Physics B | 0217-9792 | Q3 | 4 |
| 764 | International Journal of Numerical Modelling Electronic Networks Devices and Fields | 0894-3370 | Q3 | 4 |
| 765 | International Journal of RF and Microwave Computer-Aided Engineering | 1096-4290 | Q3 | 4 |
| 766 | Investigative Ophthalmology & Visual Science | 0146-0404 | Q1 | 4 |
| 767 | Journal of Applied Phycology | 0921-8971 | Q2 | 4 |
| 768 | Journal of Computational Electronics | 1569-8025 | Q3 | 4 |
| 769 | Journal of Computational and Applied Mathematics | 0377-0427 | Q1 | 4 |
| 770 | Journal of Control and Decision | 2330-7706 | Q2 | 4 |
| 771 | Journal of Coordination Chemistry | 0095-8972 | Q3 | 4 |
| 772 | Journal of Electromagnetic Waves and Applications | 0920-5071 | Q3 | 4 |
| 773 | Journal of Energy and Environmental Sustainability | 2455-2259 | — | 4 |
| 774 | Journal of Engineering Research | 2307-1877 | Q2 | 4 |
| 775 | Journal of Food Measurement & Characterization | 2193-4126 | Q2 | 4 |
| 776 | Journal of Geophysical Research Oceans | 2169-9275 | Q1 | 4 |
| 777 | Journal of Hazardous Materials | 0304-3894 | Q1 | 4 |
| 778 | Journal of Inorganic and Organometallic Polymers and Materials | 1053-0495 | Q2 | 4 |
| 779 | Journal of Luminescence | 0022-2313 | Q2 | 4 |
| 780 | Journal of Marine Systems | 0924-7963 | Q1 | 4 |
| 781 | Journal of Mechanical Science and Technology | 1738-494X | Q2 | 4 |
| 782 | Journal of Medical Systems | 0148-5598 | Q1 | 4 |
| 783 | Journal of Micromechanics and Microengineering | 0960-1317 | Q2 | 4 |
| 784 | Journal of Nanoparticle Research | 1388-0764 | Q2 | 4 |
| 785 | Journal of Orthopaedics | 0972-978X | Q2 | 4 |
| 786 | Journal of Photochemistry and Photobiology B Biology | 1011-1344 | Q1 | 4 |
| 787 | Journal of Pipeline Systems Engineering and Practice | 1949-1190 | Q2 | 4 |
| 788 | Journal of Polymer Research | 1022-9760 | Q2 | 4 |
| 789 | Journal of Public Health | 0943-1853 | Q2 | 4 |
| 790 | Journal of Reinforced Plastics and Composites | 0731-6844 | Q2 | 4 |
| 791 | Journal of Sandwich Structures & Materials | 1099-6362 | Q2 | 4 |
| 792 | Journal of Sound and Vibration | 0022-460X | Q1 | 4 |
| 793 | Journal of Testing and Evaluation | 0090-3973 | Q3 | 4 |
| 794 | Journal of The Institution of Engineers (India) Series C | 2250-0545 | Q3 | 4 |
| 795 | Journal of Thermophysics and Heat Transfer | 0887-8722 | Q3 | 4 |
| 796 | Journal of Vacuum Science & Technology B Nanotechnology and Microelectronics Materials Processing Measurement and Phenomena | 2166-2746 | Q3 | 4 |
| 797 | Journal of Vibration and Control | 1077-5463 | Q2 | 4 |
| 798 | Journal of Web Engineering | 1540-9589 | Q3 | 4 |
| 799 | Journal of the Geological Society of India | 0016-7622 | Q3 | 4 |
| 800 | Journal of the mechanical behavior of biomedical materials/Journal of mechanical behavior of biomedical materials | 1751-6161 | Q1 | 4 |
| 801 | Materials & Design | 0264-1275 | Q1 | 4 |
| 802 | Materials Technology | 1066-7857 | Q2 | 4 |
| 803 | Materials Today Energy | 2468-6069 | Q1 | 4 |
| 804 | Measurement Science and Technology | 0957-0233 | Q2 | 4 |
| 805 | Mediterranean Journal of Mathematics | 1660-5446 | Q1 | 4 |
| 806 | Methodology And Computing In Applied Probability | 1387-5841 | Q2 | 4 |
| 807 | Microbial Pathogenesis | 0882-4010 | Q2 | 4 |
| 808 | Microchemical Journal | 0026-265X | Q2 | 4 |
| 809 | Mining Metallurgy & Exploration | 2524-3462 | Q2 | 4 |
| 810 | Nano Energy | 2211-2855 | Q1 | 4 |
| 811 | Nuclear Physics A | 0375-9474 | Q2 | 4 |
| 812 | Optical Engineering | 0091-3286 | Q3 | 4 |
| 813 | PLANT PHYSIOLOGY | 0032-0889 | Q1 | 4 |
| 814 | PeerJ Computer Science | 2376-5992 | Q2 | 4 |
| 815 | Photonics | 2304-6732 | Q2 | 4 |
| 816 | Physical Review Applied | 2331-7019 | Q1 | 4 |
| 817 | Physical Review Research | 2643-1564 | Q1 | 4 |
| 818 | Physics | 2624-8174 | Q2 | 4 |
| 819 | Polymer Chemistry | 1759-9954 | Q1 | 4 |
| 820 | Polymers | 2073-4360 | Q1 | 4 |
| 821 | Procedia Technology | 2212-0173 | — | 4 |
| 822 | Proceedings of the National Academy of Sciences India Section A Physical Sciences | 0369-8203 | Q3 | 4 |
| 823 | Proceedings of the Royal Society A Mathematical Physical and Engineering Sciences | 1364-5021 | Q1 | 4 |
| 824 | Process Biochemistry | 0032-9592 | Q2 | 4 |
| 825 | Progress in Solid State Chemistry | 0079-6786 | Q1 | 4 |
| 826 | Remote Sensing Applications Society and Environment | 2352-9385 | Q1 | 4 |
| 827 | Resources Conservation and Recycling | 0921-3449 | Q1 | 4 |
| 828 | Science | 0036-8075 | Q1 | 4 |
| 829 | Signal Processing | 0165-1684 | Q1 | 4 |
| 830 | Signal Processing Image Communication | 0923-5965 | Q2 | 4 |
| 831 | Soil Use and Management | 0266-0032 | Q1 | 4 |
| 832 | Solid-State Electronics | 0038-1101 | Q3 | 4 |
| 833 | Structural Health Monitoring | 1475-9217 | Q1 | 4 |
| 834 | Swarm and Evolutionary Computation | 2210-6502 | Q1 | 4 |
| 835 | Synlett | 0936-5214 | Q3 | 4 |
| 836 | Technological Forecasting and Social Change | 0040-1625 | Q1 | 4 |
| 837 | Telecommunication Systems | 1018-4864 | Q2 | 4 |
| 838 | The Astrophysical Journal Supplement Series | 0067-0049 | Q1 | 4 |
| 839 | Thermochimica Acta | 0040-6031 | Q2 | 4 |
| 840 | Transportation Research Record Journal of the Transportation Research Board | 0361-1981 | Q2 | 4 |
| 841 | Vaccines | 2076-393X | Q1 | 4 |
| 842 | Waste Management & Research The Journal for a Sustainable Circular Economy | 0734-242X | Q1 | 4 |
| 843 | e-Journal of Nondestructive Testing | 1435-4934 | — | 4 |
| 844 | iScience | 2589-0042 | Q1 | 4 |
| 845 | The cryosphere | 1994-0416 | Q1 | 4 |
| 846 | ACM Transactions on Asian and Low-Resource Language Information Processing | 2375-4699 | Q2 | 3 |
| 847 | ACS Pharmacology & Translational Science | 2575-9108 | Q2 | 3 |
| 848 | ASCE-ASME Journal of Risk and Uncertainty in Engineering Systems Part A Civil Engineering | 2376-7642 | Q2 | 3 |
| 849 | Acoustical Physics | 1063-7710 | Q3 | 3 |
| 850 | Acta Applicandae Mathematicae | 0167-8019 | Q2 | 3 |
| 851 | Acta Crystallographica Section A Foundations and Advances | 2053-2733 | Q2 | 3 |
| 852 | Acta Geotechnica | 1861-1125 | Q1 | 3 |
| 853 | Acta Materialia | 1359-6454 | Q1 | 3 |
| 854 | Advanced Biology | 2701-0198 | Q1 | 3 |
| 855 | Advanced Materials | 0935-9648 | Q1 | 3 |
| 856 | Advanced Quantum Technologies | 2511-9044 | Q1 | 3 |
| 857 | Advanced Therapeutics | 2366-3987 | Q2 | 3 |
| 858 | Advances in Difference Equations | 1687-1839 | — | 3 |
| 859 | Agricultural Water Management | 0378-3774 | Q1 | 3 |
| 860 | Analysis and Mathematical Physics | 1664-235X | Q1 | 3 |
| 861 | Analytica Chimica Acta | 0003-2670 | Q1 | 3 |
| 862 | Analytical Methods | 1759-9660 | Q2 | 3 |
| 863 | Annales Fennici Mathematici | 2737-0690 | Q1 | 3 |
| 864 | Applied Physics Reviews | 1931-9401 | Q1 | 3 |
| 865 | Applied Water Science | 2190-5487 | Q1 | 3 |
| 866 | Asia-Pacific Financial Markets | 1380-2011 | Q2 | 3 |
| 867 | Asian Journal of Technology Innovation | 1976-1597 | Q2 | 3 |
| 868 | Atmospheric Pollution Research | 1309-1042 | Q1 | 3 |
| 869 | Atomization and Sprays | 1044-5110 | Q3 | 3 |
| 870 | Atoms | 2218-2004 | Q3 | 3 |
| 871 | Beilstein Journal of Nanotechnology | 2190-4286 | Q2 | 3 |
| 872 | Beilstein Journal of Organic Chemistry | 1860-5397 | Q2 | 3 |
| 873 | BioEnergy Research | 1939-1234 | Q1 | 3 |
| 874 | Biochimica et Biophysica Acta (BBA) - Reviews on Cancer | 0304-419X | Q1 | 3 |
| 875 | Biomaterials Advances | 2772-9508 | Q1 | 3 |
| 876 | Biomedical Physics & Engineering Express | 2057-1976 | Q3 | 3 |
| 877 | Bulletin of Earthquake Engineering | 1570-761X | Q1 | 3 |
| 878 | Bulletin of the American Meteorological Society | 0003-0007 | Q1 | 3 |
| 879 | Bulletin of the Malaysian Mathematical Sciences Society | 0126-6705 | Q2 | 3 |
| 880 | CLEAN - Soil Air Water | 1863-0650 | Q3 | 3 |
| 881 | Canadian Geotechnical Journal | 0008-3674 | Q1 | 3 |
| 882 | Canadian Mathematical Bulletin | 0008-4395 | Q2 | 3 |
| 883 | Carbohydrate Polymers | 0144-8617 | Q1 | 3 |
| 884 | Case Studies in Thermal Engineering | 2214-157X | Q1 | 3 |
| 885 | Catalysis Communications | 1566-7367 | Q2 | 3 |
| 886 | Catalysis Letters | 1011-372X | Q2 | 3 |
| 887 | Catalysts | 2073-4344 | Q2 | 3 |
| 888 | Cellular Physiology and Biochemistry | 1015-8987 | Q3 | 3 |
| 889 | Cellular and Molecular Life Sciences | 1420-682X | Q1 | 3 |
| 890 | Cellulose | 0969-0239 | Q1 | 3 |
| 891 | ChemBioChem | 1439-4227 | Q1 | 3 |
| 892 | ChemMedChem | 1860-7179 | Q1 | 3 |
| 893 | Chemical & Biomedical Imaging | 2832-3637 | Q1 | 3 |
| 894 | Chemical Biology & Drug Design | 1747-0277 | Q2 | 3 |
| 895 | Clean Technologies and Environmental Policy | 1618-954X | Q1 | 3 |
| 896 | Cogent Engineering | 2331-1916 | Q2 | 3 |
| 897 | Communications in Nonlinear Science and Numerical Simulation | 1007-5704 | Q1 | 3 |
| 898 | Composites Communications | 2452-2139 | Q1 | 3 |
| 899 | Composites Part A Applied Science and Manufacturing | 1359-835X | Q1 | 3 |
| 900 | Comptes Rendus Mathématique | 1631-073X | Q2 | 3 |
| 901 | Computational and Mathematical Biophysics | 2544-7297 | Q3 | 3 |
| 902 | Computer Communications | 0140-3664 | Q1 | 3 |
| 903 | Computer Speech & Language | 0885-2308 | Q2 | 3 |
| 904 | Computers & Industrial Engineering | 0360-8352 | Q1 | 3 |
| 905 | Computing | 0010-485X | Q2 | 3 |
| 906 | Concurrency and Computation Practice and Experience | 1532-0626 | Q2 | 3 |
| 907 | Corrosion Science | 0010-938X | Q1 | 3 |
| 908 | Current Cancer Drug Targets | 1568-0096 | Q2 | 3 |
| 909 | Current Protocols | 2691-1299 | Q1 | 3 |
| 910 | Current Research in Structural Biology | 2665-928X | Q2 | 3 |
| 911 | Earth Science Informatics | 1865-0473 | Q1 | 3 |
| 912 | Earth and Space Science | 2333-5084 | Q1 | 3 |
| 913 | Ecology Economy and Society–the INSEE Journal | 2581-6101 | Q2 | 3 |
| 914 | Economics of Innovation and New Technology | 1043-8599 | Q1 | 3 |
| 915 | Electrocatalysis | 1868-2529 | Q3 | 3 |
| 916 | Electromagnetics | 0272-6343 | Q3 | 3 |
| 917 | Emergent Materials | 2522-5731 | Q2 | 3 |
| 918 | Engineering Science and Technology an International Journal | 2215-0986 | Q1 | 3 |
| 919 | Engineering With Computers | 0177-0667 | Q1 | 3 |
| 920 | Environmental Challenges | 2667-0100 | Q1 | 3 |
| 921 | Environmental Science Nano | 2051-8153 | Q1 | 3 |
| 922 | Environmental Science Processes & Impacts | 2050-7887 | Q1 | 3 |
| 923 | European Journal of Environmental and Civil engineering | 1964-8189 | Q2 | 3 |
| 924 | European Journal of Mechanics - B/Fluids | 0997-7546 | Q2 | 3 |
| 925 | European Polymer Journal | 0014-3057 | Q1 | 3 |
| 926 | Evolution equations and control theory | 2163-2472 | Q1 | 3 |
| 927 | Experimental Astronomy | 0922-6435 | Q2 | 3 |
| 928 | Expert Review of Proteomics | 1478-9450 | Q2 | 3 |
| 929 | Ferroelectrics Letters Section | 0731-5171 | Q4 | 3 |
| 930 | FlatChem | 2452-2627 | Q1 | 3 |
| 931 | Food Analytical Methods | 1936-9751 | Q2 | 3 |
| 932 | Forces in Mechanics | 2666-3597 | Q2 | 3 |
| 933 | Frequenz | 0016-1136 | Q3 | 3 |
| 934 | Frontiers in Marine Science | 2296-7745 | Q1 | 3 |
| 935 | Frontiers in Public Health | 2296-2565 | Q1 | 3 |
| 936 | Frontiers in Signal Processing | 2673-8198 | Q2 | 3 |
| 937 | Frontiers in Water | 2624-9375 | Q1 | 3 |
| 938 | Functional Materials Letters | 1793-6047 | Q4 | 3 |
| 939 | Future Journal of Pharmaceutical Sciences | 2314-7245 | — | 3 |
| 940 | Future Virology | 1746-0794 | Q3 | 3 |
| 941 | Geophysical Research Letters | 0094-8276 | Q1 | 3 |
| 942 | Georisk Assessment and Management of Risk for Engineered Systems and Geohazards | 1749-9518 | Q1 | 3 |
| 943 | Geotechnical and Geological Engineering | 0960-3182 | Q1 | 3 |
| 944 | Heat Transfer Engineering | 0145-7632 | Q2 | 3 |
| 945 | IEEE Control Systems Letters | 2475-1456 | Q1 | 3 |
| 946 | IEEE Journal of the Electron Devices Society | 2168-6734 | Q2 | 3 |
| 947 | IEEE Transactions on Biomedical Engineering | 0018-9294 | Q1 | 3 |
| 948 | IEEE Transactions on Energy Conversion | 0885-8969 | Q1 | 3 |
| 949 | IEEE Transactions on Information Theory | 0018-9448 | Q1 | 3 |
| 950 | IEEE Transactions on Multimedia | 1520-9210 | Q1 | 3 |
| 951 | IEEE Transactions on NanoBioscience | 1536-1241 | Q2 | 3 |
| 952 | IEEE/CAA Journal of Automatica Sinica | 2329-9266 | Q1 | 3 |
| 953 | IET Circuits Devices & Systems | 1751-858X | Q3 | 3 |
| 954 | IET Nanodielectrics | 2514-3255 | Q1 | 3 |
| 955 | IET Networks | 2047-4954 | Q2 | 3 |
| 956 | IET Optoelectronics | 1751-8768 | Q2 | 3 |
| 957 | IET Quantum Communication | 2632-8925 | Q2 | 3 |
| 958 | IET Renewable Power Generation | 1752-1416 | Q2 | 3 |
| 959 | IFAC Journal of Systems and Control | 2468-6018 | Q2 | 3 |
| 960 | IMA Journal of Mathematical Control and Information | 0265-0754 | Q3 | 3 |
| 961 | ISA Transactions | 0019-0578 | Q1 | 3 |
| 962 | Icarus | 0019-1035 | Q1 | 3 |
| 963 | Industrial Crops and Products | 0926-6690 | Q1 | 3 |
| 964 | Industrial Lubrication and Tribology | 0036-8792 | Q3 | 3 |
| 965 | Infection Genetics and Evolution | 1567-1348 | Q1 | 3 |
| 966 | Information Processing & Management | 0020-0271 | Q1 | 3 |
| 967 | Information Processing Letters | 0020-0190 | Q3 | 3 |
| 968 | International Journal for Computational Methods in Engineering Science and Mechanics | 1550-2287 | Q2 | 3 |
| 969 | International Journal of Adhesion and Adhesives | 0143-7496 | Q2 | 3 |
| 970 | International Journal of Applied Glass Science | 2041-1286 | Q2 | 3 |
| 971 | International Journal of Applied and Computational Mathematics | 2199-5796 | Q3 | 3 |
| 972 | International Journal of Bifurcation and Chaos | 0218-1274 | Q1 | 3 |
| 973 | International Journal of Engineering Science | 0020-7225 | Q1 | 3 |
| 974 | International Journal of Environment and Waste Management | 1478-9868 | Q4 | 3 |
| 975 | International Journal of Fracture | 0020-7268 | Q1 | 3 |
| 976 | International Journal of General Systems | 0308-1079 | Q2 | 3 |
| 977 | International Journal of Imaging Systems and Technology | 0899-9457 | Q2 | 3 |
| 978 | International Journal of Impact Engineering | 0734-743X | Q1 | 3 |
| 979 | International Journal of Information Technology | 2511-2104 | Q1 | 3 |
| 980 | International Journal of Modelling and Simulation | 0228-6203 | Q2 | 3 |
| 981 | International Journal of Nonlinear Sciences and Numerical Simulation | 1565-1339 | Q2 | 3 |
| 982 | International Journal of Pavement Research and Technology | 1996-6814 | Q2 | 3 |
| 983 | International Journal of Plasticity | 0749-6419 | Q1 | 3 |
| 984 | International Journal of Power Electronics | 1756-638X | Q4 | 3 |
| 985 | International Journal of Theoretical Physics | 0020-7748 | Q3 | 3 |
| 986 | International Journal of Thermofluids | 2666-2027 | Q1 | 3 |
| 987 | International Journal of Transportation Science and Technology | 2046-0430 | Q1 | 3 |
| 988 | Internet Technology Letters | 2476-1508 | Q3 | 3 |
| 989 | Iranian Journal of Science and Technology Transactions of Civil Engineering | 2228-6160 | Q2 | 3 |
| 990 | Journal of Alloys and Compounds Communications | 2950-2845 | Q1 | 3 |
| 991 | Journal of Bio- and Tribo-Corrosion | 2198-4220 | Q2 | 3 |
| 992 | Journal of Biomedical Materials Research Part B Applied Biomaterials | 1552-4973 | Q2 | 3 |
| 993 | Journal of Circuits Systems and Computers | 0218-1266 | Q3 | 3 |
| 994 | Journal of Clinical and Experimental Hepatology | 0973-6883 | Q2 | 3 |
| 995 | Journal of Cluster Science | 1040-7278 | Q2 | 3 |
| 996 | Journal of Coatings Technology and Research | 1547-0091 | Q2 | 3 |
| 997 | Journal of Computational Chemistry | 0192-8651 | Q1 | 3 |
| 998 | Journal of Computational Physics | 0021-9991 | Q1 | 3 |
| 999 | Journal of Computing in Civil Engineering | 0887-3801 | Q1 | 3 |
| 1000 | Journal of Engineering Materials and Technology | 0094-4289 | Q2 | 3 |
| 1001 | Journal of Failure Analysis and Prevention | 1547-7029 | Q3 | 3 |
| 1002 | Journal of Fluorescence | 1053-0509 | Q2 | 3 |
| 1003 | Journal of Inorganic Biochemistry | 0162-0134 | Q2 | 3 |
| 1004 | Journal of King Saud University - Science | 1018-3647 | Q1 | 3 |
| 1005 | Journal of Mountain Science | 1672-6316 | Q2 | 3 |
| 1006 | Journal of Nonlinear Optical Physics & Materials | 0218-1991 | Q3 | 3 |
| 1007 | Journal of Optical Communications and Networking | 1943-0620 | Q1 | 3 |
| 1008 | Journal of Performance of Constructed Facilities | 0887-3828 | Q2 | 3 |
| 1009 | Journal of Pressure Vessel Technology | 0094-9930 | Q3 | 3 |
| 1010 | Journal of Proteins and Proteomics | 0975-8151 | — | 3 |
| 1011 | Journal of Statistical Computation and Simulation | 0094-9655 | Q2 | 3 |
| 1012 | Journal of Statistical Mechanics Theory and Experiment | 1742-5468 | Q3 | 3 |
| 1013 | Journal of Superconductivity and Novel Magnetism | 1557-1939 | Q3 | 3 |
| 1014 | Journal of Sustainable Metallurgy | 2199-3823 | Q1 | 3 |
| 1015 | Journal of Thermoplastic Composite Materials | 0892-7057 | Q2 | 3 |
| 1016 | Journal of Transportation Engineering Part B Pavements | 2573-5438 | Q2 | 3 |
| 1017 | Journal of Vacuum Science & Technology A Vacuum Surfaces and Films | 0734-2101 | Q2 | 3 |
| 1018 | Journal of Water and Climate Change | 2040-2244 | Q1 | 3 |
| 1019 | Journal of dynamic decision making | 2365-8037 | — | 3 |
| 1020 | Journal of structural design and construction practice. | 2996-5136 | Q1 | 3 |
| 1021 | Journal of the Indian Institute of Science | 0019-4964 | Q2 | 3 |
| 1022 | Journal of the Mechanics and Physics of Solids | 0022-5096 | Q1 | 3 |
| 1023 | Journal of the Palaeontological Society of India | 0552-9360 | Q4 | 3 |
| 1024 | Journal of the Taiwan Institute of Chemical Engineers | 1876-1070 | Q1 | 3 |
| 1025 | Machine Vision and Applications | 0932-8092 | Q2 | 3 |
| 1026 | Marine Georesources and Geotechnology | 1064-119X | Q2 | 3 |
| 1027 | Marine Micropaleontology | 0377-8398 | Q2 | 3 |
| 1028 | Materials Performance and Characterization | 2165-3992 | Q3 | 3 |
| 1029 | Materials Research Innovations | 1432-8917 | Q3 | 3 |
| 1030 | Materials Science for Energy Technologies | 2589-2991 | Q1 | 3 |
| 1031 | Materials Today | 1369-7021 | Q1 | 3 |
| 1032 | Mathematica Slovaca | 0139-9918 | Q2 | 3 |
| 1033 | Medical Engineering & Physics | 1350-4533 | Q3 | 3 |
| 1034 | Medical Hypotheses | 0306-9877 | Q3 | 3 |
| 1035 | Memories - Materials Devices Circuits and Systems | 2773-0646 | Q2 | 3 |
| 1036 | Metals | 2075-4701 | Q2 | 3 |
| 1037 | Microsystem Technologies | 0946-7076 | Q3 | 3 |
| 1038 | Mineral Processing and Extractive Metallurgy Transactions of the Institutions of Mining and Metallurgy | 2572-6641 | Q3 | 3 |
| 1039 | Modelling and Simulation in Materials Science and Engineering | 0965-0393 | Q2 | 3 |
| 1040 | Modern Physics Letters A | 0217-7323 | Q3 | 3 |
| 1041 | Molecular Biology Reports | 0301-4851 | Q2 | 3 |
| 1042 | Nanomaterials | 2079-4991 | Q1 | 3 |
| 1043 | Natural Hazards Review | 1527-6988 | Q1 | 3 |
| 1044 | Noise & Vibration Worldwide | 0957-4565 | Q3 | 3 |
| 1045 | Nonlinear Analysis Hybrid Systems | 1751-570X | Q1 | 3 |
| 1046 | Ocean Dynamics | 0012-0308 | Q2 | 3 |
| 1047 | Optics and Lasers in Engineering | 0143-8166 | Q1 | 3 |
| 1048 | Oxford Open Materials Science | 2633-6979 | Q2 | 3 |
| 1049 | PLoS Pathogens | 1553-7366 | Q1 | 3 |
| 1050 | Pathogens | 2076-0817 | Q1 | 3 |
| 1051 | Peer-to-Peer Networking and Applications | 1936-6442 | Q2 | 3 |
| 1052 | Pharmaceutical Research | 0724-8741 | Q1 | 3 |
| 1053 | Photodiagnosis and Photodynamic Therapy | 1572-1000 | Q2 | 3 |
| 1054 | Photonic Network Communications | 1387-974X | Q3 | 3 |
| 1055 | Physical Review X | 2160-3308 | Q1 | 3 |
| 1056 | Physics Reports | 0370-1573 | Q1 | 3 |
| 1057 | Plant Phenomics | 2097-0374 | Q1 | 3 |
| 1058 | Powder Technology | 0032-5910 | Q1 | 3 |
| 1059 | Probiotics and Antimicrobial Proteins | 1867-1306 | Q2 | 3 |
| 1060 | Proceedings of the Indian National Science Academy | 2454-9983 | Q2 | 3 |
| 1061 | Proceedings of the Institution of Mechanical Engineers Part J Journal of Engineering Tribology | 1350-6501 | Q2 | 3 |
| 1062 | Proteins Structure Function and Bioinformatics | 0887-3585 | Q2 | 3 |
| 1063 | Quaternary Science Reviews | 0277-3791 | Q1 | 3 |
| 1064 | RSC Sustainability | 2753-8125 | Q1 | 3 |
| 1065 | Rapid Prototyping Journal | 1355-2546 | Q1 | 3 |
| 1066 | Reaction Chemistry & Engineering | 2058-9883 | Q2 | 3 |
| 1067 | Regional Studies in Marine Science | 2352-4855 | Q1 | 3 |
| 1068 | Results in Optics | 2666-9501 | Q2 | 3 |
| 1069 | Results in Surfaces and Interfaces | 2666-8459 | Q1 | 3 |
| 1070 | Revista de la Real Academia de Ciencias Exactas Físicas y Naturales Serie A Matemáticas | 1578-7303 | Q1 | 3 |
| 1071 | Robotics and Autonomous Systems | 0921-8890 | Q1 | 3 |
| 1072 | Royal Society Open Science | 2054-5703 | Q1 | 3 |
| 1073 | SN Business & Economics | 2662-9399 | Q3 | 3 |
| 1074 | Separation Science and Technology | 0149-6395 | Q2 | 3 |
| 1075 | Speech Communication | 0167-6393 | Q1 | 3 |
| 1076 | Surface Engineering | 0267-0844 | Q1 | 3 |
| 1077 | Sustainable Cities and Society | 2210-6707 | Q1 | 3 |
| 1078 | Sustainable Development | 0968-0802 | Q1 | 3 |
| 1079 | Sustainable Energy Grids and Networks | 2352-4677 | Q1 | 3 |
| 1080 | Synthesis | 0039-7881 | Q2 | 3 |
| 1081 | Synthetic Communications | 0039-7911 | Q3 | 3 |
| 1082 | Systems Microbiology and Biomanufacturing | 2662-7655 | Q2 | 3 |
| 1083 | Technology Analysis and Strategic Management | 0953-7325 | Q2 | 3 |
| 1084 | Technology in Society | 0160-791X | Q1 | 3 |
| 1085 | The Indian Economic Journal | 0019-4662 | Q3 | 3 |
| 1086 | The Journal of Strain Analysis for Engineering Design | 0022-4758 | Q3 | 3 |
| 1087 | The Physics Teacher | 0031-921X | Q2 | 3 |
| 1088 | The Singapore Economic Review | 0217-5908 | Q3 | 3 |
| 1089 | Thin Solid Films | 0040-6090 | Q2 | 3 |
| 1090 | Transport in Porous Media | 0169-3913 | Q2 | 3 |
| 1091 | Tribology Transactions | 1040-2004 | Q2 | 3 |
| 1092 | Waves in Random and Complex Media | 1745-5030 | — | 3 |
| 1093 | World Journal of Microbiology and Biotechnology | 0959-3993 | Q1 | 3 |
| 1094 | npj Climate and Atmospheric Science | 2397-3722 | Q1 | 3 |
| 1095 | 3D Printing and Additive Manufacturing | 2329-7662 | Q2 | 2 |
| 1096 | ACM Transactions on Internet of Things | 2577-6207 | Q1 | 2 |
| 1097 | ACM Transactions on Sensor Networks | 1550-4859 | Q1 | 2 |
| 1098 | ACS Chemical Biology | 1554-8929 | Q1 | 2 |
| 1099 | ACS Food Science & Technology | 2692-1944 | Q2 | 2 |
| 1100 | ACS Materials Au | 2694-2461 | Q1 | 2 |
| 1101 | ACS Sustainable Resource Management | 2837-1445 | Q2 | 2 |
| 1102 | AIAA Journal | 0001-1452 | Q1 | 2 |
| 1103 | AIMS Mathematics | 2473-6988 | Q2 | 2 |
| 1104 | APL Materials | 2166-532X | Q1 | 2 |
| 1105 | Acoustics Australia | 0814-6039 | Q2 | 2 |
| 1106 | Acta Metallurgica Sinica (English Letters) | 1006-7191 | Q1 | 2 |
| 1107 | Advanced Engineering Informatics | 1474-0346 | Q1 | 2 |
| 1108 | Advanced Healthcare Materials | 2192-2640 | Q1 | 2 |
| 1109 | Advanced Materials Proceedings | 2002-441X | — | 2 |
| 1110 | American Journal of Engineering and Applied Sciences | 1941-7020 | — | 2 |
| 1111 | American Journal of Mathematical and Management Sciences | 0196-6324 | Q3 | 2 |
| 1112 | Annales Geophysicae | 0992-7689 | Q2 | 2 |
| 1113 | Annals of Physics | 0003-4916 | Q2 | 2 |
| 1114 | Annals of Surgical Oncology | 1068-9265 | Q1 | 2 |
| 1115 | Anti-Cancer Agents in Medicinal Chemistry | 1568-0118 | Q3 | 2 |
| 1116 | Antiviral Research | 0166-3542 | Q1 | 2 |
| 1117 | Applied Geomatics | 1866-928X | Q2 | 2 |
| 1118 | Applied Materials Today | 2352-9407 | Q1 | 2 |
| 1119 | Applied Mathematics and Mechanics | 0253-4827 | Q1 | 2 |
| 1120 | Applied Nanoscience | 2190-5509 | Q2 | 2 |
| 1121 | Applied Network Science | 2364-8228 | Q2 | 2 |
| 1122 | Applied Ocean Research | 0141-1187 | Q1 | 2 |
| 1123 | Applied Spectroscopy | 0003-7028 | Q2 | 2 |
| 1124 | Arab Journal of Basic and Applied Sciences | 2576-5299 | Q2 | 2 |
| 1125 | Architecture Structures and Construction | 2730-9886 | Q1 | 2 |
| 1126 | Archives of Foundry Engineering | 1897-3310 | Q3 | 2 |
| 1127 | Archives of Virology | 0003-9012 | Q2 | 2 |
| 1128 | Arctic Antarctic and Alpine Research | 1523-0430 | Q2 | 2 |
| 1129 | Artificial Intelligence Review | 0269-2821 | Q1 | 2 |
| 1130 | Artificial Intelligence in Medicine | 0933-3657 | Q1 | 2 |
| 1131 | Astrophysics and Space Science | 0004-640X | Q2 | 2 |
| 1132 | BMC Cancer | 1471-2407 | Q2 | 2 |
| 1133 | BMC Microbiology | 1471-2180 | Q1 | 2 |
| 1134 | Battery energy | 2768-1688 | Q1 | 2 |
| 1135 | Benchmarking An International Journal | 1463-5771 | Q1 | 2 |
| 1136 | BioMetals | 0966-0844 | Q1 | 2 |
| 1137 | Biochemical Pharmacology | 0006-2952 | Q1 | 2 |
| 1138 | Biochemistry | 0006-2960 | Q2 | 2 |
| 1139 | Biochimica et Biophysica Acta (BBA) - Biomembranes | 0005-2736 | Q2 | 2 |
| 1140 | Biochimie | 0037-9042 | Q1 | 2 |
| 1141 | Bioconjugate Chemistry | 1043-1802 | Q1 | 2 |
| 1142 | Bioinformation | 0973-2063 | — | 2 |
| 1143 | Biomedical Chromatography | 0269-3879 | Q3 | 2 |
| 1144 | Biomedical Materials | 1748-6041 | Q2 | 2 |
| 1145 | Biomedical materials for multi-functional applications | 2731-9695 | — | 2 |
| 1146 | Bioorganic & Medicinal Chemistry | 0968-0896 | Q2 | 2 |
| 1147 | Biophysical Journal | 0006-3495 | Q1 | 2 |
| 1148 | Bioremediation Journal | 1088-9868 | Q3 | 2 |
| 1149 | Bioscience Reports | 0144-8463 | Q1 | 2 |
| 1150 | Biosystems Engineering | 1537-5110 | Q1 | 2 |
| 1151 | Biotechnology for Sustainable Materials | 2948-2348 | — | 2 |
| 1152 | Building Acoustics | 1351-010X | Q2 | 2 |
| 1153 | Business Strategy and the Environment | 0964-4733 | Q1 | 2 |
| 1154 | Canadian Journal of Biotechnology | 2560-8304 | — | 2 |
| 1155 | Canadian Journal of Electrical and Computer Engineering | 0840-8688 | Q2 | 2 |
| 1156 | Carbohydrate Research | 0008-6215 | Q2 | 2 |
| 1157 | Carbon Trends | 2667-0569 | Q2 | 2 |
| 1158 | Carbon letters | 1976-4251 | Q1 | 2 |
| 1159 | Catalysis Reviews | 0161-4940 | Q1 | 2 |
| 1160 | Cells | 2073-4409 | Q1 | 2 |
| 1161 | Cement and Concrete Composites | 0958-9465 | Q1 | 2 |
| 1162 | Chemical Engineering & Technology | 0930-7516 | Q2 | 2 |
| 1163 | Chemistry Africa | 2522-5758 | Q3 | 2 |
| 1164 | Chemometrics and Intelligent Laboratory Systems | 0169-7439 | Q2 | 2 |
| 1165 | Clinica Chimica Acta | 0009-8981 | Q1 | 2 |
| 1166 | Coatings | 2079-6412 | Q2 | 2 |
| 1167 | Cognitive Systems Research | 1389-0417 | Q2 | 2 |
| 1168 | Colloids and Interface Science Communications | 2215-0382 | Q1 | 2 |
| 1169 | Colloids and Surfaces B Biointerfaces | 0927-7765 | Q1 | 2 |
| 1170 | Combustion Science and Technology | 0010-2202 | Q2 | 2 |
| 1171 | Combustion and Flame | 0010-2180 | Q1 | 2 |
| 1172 | Communications Chemistry | 2399-3669 | Q1 | 2 |
| 1173 | Communications Materials | 2662-4443 | Q1 | 2 |
| 1174 | Communications in Computational Physics | 1815-2406 | Q1 | 2 |
| 1175 | Competitiveness Review An International Business Journal incorporating Journal of Global Competitiveness | 1059-5422 | Q1 | 2 |
| 1176 | Complex Analysis and Operator Theory | 1661-8254 | Q2 | 2 |
| 1177 | Computational and Applied Mathematics | 0101-8205 | Q2 | 2 |
| 1178 | Computer Methods in Biomechanics & Biomedical Engineering | 1025-5842 | Q3 | 2 |
| 1179 | Computer Physics Communications | 0010-4655 | Q1 | 2 |
| 1180 | Computers & Operations Research | 0305-0548 | Q1 | 2 |
| 1181 | Corrosion Reviews | 0334-6005 | Q2 | 2 |
| 1182 | Cureus | 2168-8184 | — | 2 |
| 1183 | Current Microbiology | 0343-8651 | Q2 | 2 |
| 1184 | Current Opinion in Biomedical Engineering | 2468-4511 | Q2 | 2 |
| 1185 | Current Opinion in Environmental Sustainability | 1877-3435 | Q1 | 2 |
| 1186 | Current Protocols in Chemical Biology | 2160-4762 | — | 2 |
| 1187 | Current Research in Microbial Sciences | 2666-5174 | Q1 | 2 |
| 1188 | Database | 1758-0463 | Q1 | 2 |
| 1189 | Deep Sea Research Part II Topical Studies in Oceanography | 0967-0645 | Q1 | 2 |
| 1190 | Development in Practice | 0961-4524 | Q2 | 2 |
| 1191 | Diagnostics | 2075-4418 | Q2 | 2 |
| 1192 | Discover Applied Sciences | 3004-9261 | Q2 | 2 |
| 1193 | Discover Artificial Intelligence | 2731-0809 | Q1 | 2 |
| 1194 | Discover Materials | 2730-7727 | Q1 | 2 |
| 1195 | Discrete Applied Mathematics | 0166-218X | Q2 | 2 |
| 1196 | Discrete and Continuous Dynamical Systems - B | 1531-3492 | Q1 | 2 |
| 1197 | Distributed Ledger Technologies Research and Practice | 2769-6480 | Q2 | 2 |
| 1198 | Drugs in R&D | 1174-5886 | Q2 | 2 |
| 1199 | EES solar. | 3033-4063 | — | 2 |
| 1200 | Earth Surface Processes and Landforms | 0197-9337 | Q1 | 2 |
| 1201 | Earthquake Engineering and Engineering Vibration | 1671-3664 | Q1 | 2 |
| 1202 | Earthquake Spectra | 1944-8201 | Q1 | 2 |
| 1203 | Ecological Engineering | 0925-8574 | Q1 | 2 |
| 1204 | Ecological Indicators | 1470-160X | Q1 | 2 |
| 1205 | Economy and Society | 0308-5147 | Q1 | 2 |
| 1206 | Energy & Environmental Science | 1754-5692 | Q1 | 2 |
| 1207 | Energy Ecology and Environment | 2363-7692 | Q2 | 2 |
| 1208 | Energy Economics | 0140-9883 | Q1 | 2 |
| 1209 | Energy Policy | 0301-4215 | Q1 | 2 |
| 1210 | Energy Storage | 2578-4862 | Q2 | 2 |
| 1211 | Energy Systems | 1868-3967 | Q2 | 2 |
| 1212 | Energy and Buildings | 0378-7788 | Q1 | 2 |
| 1213 | Engineering Reports | 2577-8196 | Q2 | 2 |
| 1214 | Environmental Chemistry Letters | 1610-3653 | Q1 | 2 |
| 1215 | Environmental Sustainability | 2523-8922 | Q1 | 2 |
| 1216 | Environmental and Sustainability Indicators | 2665-9727 | Q1 | 2 |
| 1217 | European Transport/Trasporti Europei | 1825-3997 | Q2 | 2 |
| 1218 | Evolving Earth | 2950-1172 | — | 2 |
| 1219 | Experiments in Fluids | 0723-4864 | Q1 | 2 |
| 1220 | Expert Systems | 0266-4720 | Q2 | 2 |
| 1221 | Extreme Mechanics Letters | 2352-4316 | Q1 | 2 |
| 1222 | FEBS Letters | 0014-5793 | Q1 | 2 |
| 1223 | Fermentation | 2311-5637 | Q1 | 2 |
| 1224 | Finite Elements in Analysis and Design | 0168-874X | Q1 | 2 |
| 1225 | Folia Microbiologica | 0015-5632 | Q2 | 2 |
| 1226 | Food Chemistry Advances | 2772-753X | Q1 | 2 |
| 1227 | Foot and Ankle Surgery | 1268-7731 | Q1 | 2 |
| 1228 | Forensic Science International Reports | 2665-9107 | Q3 | 2 |
| 1229 | Formal Methods in System Design | 0925-9856 | Q3 | 2 |
| 1230 | Fractional Calculus and Applied Analysis | 1311-0454 | Q1 | 2 |
| 1231 | Franklin Open | 2773-1863 | Q2 | 2 |
| 1232 | Frontiers in Big Data | 2624-909X | Q2 | 2 |
| 1233 | Frontiers in Bioengineering and Biotechnology | 2296-4185 | Q1 | 2 |
| 1234 | Frontiers in Cardiovascular Medicine | 2297-055X | Q1 | 2 |
| 1235 | Frontiers in Cell and Developmental Biology | 2296-634X | Q1 | 2 |
| 1236 | Frontiers in Climate | 2624-9553 | Q1 | 2 |
| 1237 | Frontiers in Forests and Global Change | 2624-893X | Q1 | 2 |
| 1238 | Frontiers in Human Neuroscience | 1662-5161 | Q1 | 2 |
| 1239 | Frontiers in Materials | 2296-8016 | Q2 | 2 |
| 1240 | Frontiers in Medical Technology | 2673-3129 | Q1 | 2 |
| 1241 | Frontiers in Molecular Neuroscience | 1662-5099 | Q2 | 2 |
| 1242 | Frontiers in Physiology | 1664-042X | Q2 | 2 |
| 1243 | Frontiers in Robotics and AI | 2296-9144 | Q2 | 2 |
| 1244 | Frontiers in Thermal Engineering | 2813-0456 | — | 2 |
| 1245 | Fusion Engineering and Design | 0920-3796 | Q2 | 2 |
| 1246 | GIScience and geo-environmental modelling | 2730-7506 | — | 2 |
| 1247 | Gels | 2310-2861 | Q1 | 2 |
| 1248 | Gene Reports | 2452-0144 | Q4 | 2 |
| 1249 | Genes & Diseases | 2352-3042 | Q1 | 2 |
| 1250 | Geocarto International | 1010-6049 | Q1 | 2 |
| 1251 | Geomechanics and Geoengineering | 1748-6025 | Q2 | 2 |
| 1252 | Geomechanics for Energy and the Environment | 2352-3808 | Q1 | 2 |
| 1253 | Geomicrobiology Journal | 0149-0451 | Q2 | 2 |
| 1254 | Geomorphology | 0169-555X | Q1 | 2 |
| 1255 | Geoscience Frontiers | 1674-9871 | Q1 | 2 |
| 1256 | Geosciences | 2076-3263 | Q2 | 2 |
| 1257 | Geosciences Journal | 1226-4806 | Q2 | 2 |
| 1258 | Géotechnique | 0016-8505 | Q1 | 2 |
| 1259 | Géotechnique Letters | 2045-2543 | Q1 | 2 |
| 1260 | Hacettepe Journal of Mathematics and Statistics | 1303-5010 | Q2 | 2 |
| 1261 | Human Factors The Journal of the Human Factors and Ergonomics Society | 0018-7208 | Q1 | 2 |
| 1262 | IEEE Internet of Things Magazine | 2576-3180 | Q1 | 2 |
| 1263 | IEEE Journal on Emerging and Selected Topics in Circuits and Systems | 2156-3357 | Q1 | 2 |
| 1264 | IEEE Journal on Flexible Electronics | 2768-167X | Q2 | 2 |
| 1265 | IEEE Open Journal of Circuits and Systems | 2644-1225 | Q2 | 2 |
| 1266 | IEEE Reviews in Biomedical Engineering | 1937-3333 | Q1 | 2 |
| 1267 | IEEE Transactions on Affective Computing | 1949-3045 | Q1 | 2 |
| 1268 | IEEE Transactions on Circuits and Systems for Video Technology | 1051-8215 | Q1 | 2 |
| 1269 | IEEE Transactions on Computers | 0018-9340 | Q1 | 2 |
| 1270 | IEEE Transactions on Control Systems Technology | 1063-6536 | Q1 | 2 |
| 1271 | IEEE Transactions on Cybernetics | 2168-2267 | Q1 | 2 |
| 1272 | IEEE Transactions on Image Processing | 1057-7149 | Q1 | 2 |
| 1273 | IEEE Transactions on Network Science and Engineering | 2327-4697 | Q1 | 2 |
| 1274 | IEEE Transactions on Neural Systems and Rehabilitation Engineering | 1534-4320 | Q1 | 2 |
| 1275 | IEEE Transactions on Plasma Science | 0093-3813 | Q2 | 2 |
| 1276 | IEEE Transactions on Semiconductor Manufacturing | 0894-6507 | Q2 | 2 |
| 1277 | IEEE Transactions on Services Computing | 1939-1374 | Q1 | 2 |
| 1278 | IET Collaborative Intelligent Manufacturing | 2516-8398 | Q2 | 2 |
| 1279 | IET Electrical Systems in Transportation | 2042-9738 | Q2 | 2 |
| 1280 | IET Power Electronics | 1755-4535 | Q2 | 2 |
| 1281 | IET Science Measurement & Technology | 1751-8822 | Q2 | 2 |
| 1282 | INAE Letters | 2366-326X | — | 2 |
| 1283 | INTERNATIONAL JOURNAL OF NEXT-GENERATION COMPUTING | 0976-5034 | — | 2 |
| 1284 | ISPRS Journal of Photogrammetry and Remote Sensing | 0924-2716 | Q1 | 2 |
| 1285 | Indian Journal of Public Health | 0019-557X | Q3 | 2 |
| 1286 | Inflammopharmacology | 0925-4692 | Q1 | 2 |
| 1287 | Infrared Physics & Technology | 1350-4495 | Q2 | 2 |
| 1288 | International Journal of Adaptive Control and Signal Processing | 0890-6327 | Q2 | 2 |
| 1289 | International Journal of Antimicrobial Agents | 0924-8579 | Q1 | 2 |
| 1290 | International Journal of Biomathematics | 1793-5245 | Q2 | 2 |
| 1291 | International Journal of Circuit Theory and Applications | 0098-9886 | Q3 | 2 |
| 1292 | International Journal of Computational Materials Science and Engineering | 2047-6841 | Q3 | 2 |
| 1293 | International Journal of Computational Vision and Robotics | 1752-9131 | Q4 | 2 |
| 1294 | International Journal of Computer Information Systems and Industrial Management Applications | 2150-7988 | Q3 | 2 |
| 1295 | International Journal of Control | 0020-7179 | Q2 | 2 |
| 1296 | International Journal of Damage Mechanics | 1056-7895 | Q1 | 2 |
| 1297 | International Journal of Geotechnical Engineering | 1938-6362 | Q2 | 2 |
| 1298 | International Journal of Green Energy | 1543-5075 | Q2 | 2 |
| 1299 | International Journal of Heat and Fluid Flow | 0142-727X | Q1 | 2 |
| 1300 | International Journal of Intelligent Machines and Robotics | 2398-7510 | — | 2 |
| 1301 | International Journal of Intelligent Transportation Systems Research | 1348-8503 | Q2 | 2 |
| 1302 | International Journal of Internet Marketing and Advertising | 1477-5212 | Q3 | 2 |
| 1303 | International Journal of Internet Technology and Secured Transactions | 1748-569X | Q4 | 2 |
| 1304 | International Journal of Machine Learning and Cybernetics | 1868-8071 | Q2 | 2 |
| 1305 | International Journal of Mathematics in Operational Research | 1757-5850 | Q3 | 2 |
| 1306 | International Journal of Microwave and Wireless Technologies | 1759-0787 | Q3 | 2 |
| 1307 | International Journal of Nonlinear Dynamics and Control | 2050-6902 | — | 2 |
| 1308 | International Journal of Peptide Research and Therapeutics | 1573-3149 | Q2 | 2 |
| 1309 | International Journal of Pharmaceutics | 0378-5173 | Q1 | 2 |
| 1310 | International Journal of Phytoremediation | 1522-6514 | Q2 | 2 |
| 1311 | International Journal of Power and Energy Conversion | 1757-1154 | Q3 | 2 |
| 1312 | International Journal of Precision Engineering and Manufacturing-Green Technology | 2198-0810 | Q1 | 2 |
| 1313 | International Journal of Sustainable Agricultural Management and Informatics | 2054-5819 | Q2 | 2 |
| 1314 | International Journal on Cyber Situational Awareness | 2057-2182 | — | 2 |
| 1315 | International Journal on Document Analysis and Recognition (IJDAR) | 1433-2825 | Q2 | 2 |
| 1316 | International Journal on Interactive Design and Manufacturing (IJIDeM) | 1955-2505 | Q2 | 2 |
| 1317 | International Reviews of Immunology | 0883-0185 | Q1 | 2 |
| 1318 | Ionics | 0947-7047 | Q2 | 2 |
| 1319 | Iranian Journal of Science and Technology Transactions of Mechanical Engineering | 2228-6187 | Q2 | 2 |
| 1320 | JCIS Open | 2666-934X | Q1 | 2 |
| 1321 | Journal Of Big Data | 2196-1115 | Q1 | 2 |
| 1322 | Journal of Adhesion Science and Technology | 0169-4243 | Q2 | 2 |
| 1323 | Journal of Advanced Dielectrics | 2010-135X | Q2 | 2 |
| 1324 | Journal of Aerospace Engineering | 0893-1321 | Q2 | 2 |
| 1325 | Journal of Agribusiness in Developing and Emerging Economies | 2044-0839 | Q1 | 2 |
| 1326 | Journal of Applied Mechanics | 0021-8936 | Q2 | 2 |
| 1327 | Journal of Applied Meteorology and Climatology | 1558-8424 | Q2 | 2 |
| 1328 | Journal of Asian Architecture and Building Engineering | 1346-7581 | Q1 | 2 |
| 1329 | Journal of Ayurveda and Integrative Medicine | 0975-9476 | Q2 | 2 |
| 1330 | Journal of Biomechanical Engineering | 0148-0731 | Q3 | 2 |
| 1331 | Journal of Biophotonics | 1864-063X | Q2 | 2 |
| 1332 | Journal of Bridge Engineering | 1084-0702 | Q1 | 2 |
| 1333 | Journal of Cellular Plastics | 0021-955X | Q2 | 2 |
| 1334 | Journal of Chemical Education | 0021-9584 | Q2 | 2 |
| 1335 | Journal of Climate | 0894-8755 | Q1 | 2 |
| 1336 | Journal of Controlled Release | 0168-3659 | Q1 | 2 |
| 1337 | Journal of Cryptographic Engineering | 2190-8508 | Q3 | 2 |
| 1338 | Journal of Crystal Growth | 0022-0248 | Q2 | 2 |
| 1339 | Journal of Electroceramics | 1385-3449 | Q3 | 2 |
| 1340 | Journal of Electronic Packaging | 1043-7398 | Q2 | 2 |
| 1341 | Journal of Electronic Testing | 0923-8174 | Q3 | 2 |
| 1342 | Journal of Engineering Science and Technology Review | 1791-2377 | Q4 | 2 |
| 1343 | Journal of Geophysical Research Atmospheres | 0148-0227 | Q1 | 2 |
| 1344 | Journal of Hardware and Systems Security | 2509-3428 | — | 2 |
| 1345 | Journal of Hazardous Materials Plastics | 3051-0600 | — | 2 |
| 1346 | Journal of Hepatology | 0168-8278 | Q1 | 2 |
| 1347 | Journal of Heterocyclic Chemistry | 0022-152X | Q3 | 2 |
| 1348 | Journal of Hydrology Regional Studies | 2214-5818 | Q1 | 2 |
| 1349 | Journal of Hydrometeorology | 1525-7541 | Q1 | 2 |
| 1350 | Journal of Imaging | 2313-433X | Q2 | 2 |
| 1351 | Journal of Intelligent & Robotic Systems | 0921-0296 | Q1 | 2 |
| 1352 | Journal of Inverse and Ill-Posed Problems | 0928-0219 | Q3 | 2 |
| 1353 | Journal of Macromolecular Science Part A | 1060-1325 | Q3 | 2 |
| 1354 | Journal of Manufacturing Systems | 0278-6125 | Q1 | 2 |
| 1355 | Journal of Micromechanics and Molecular Physics | 2424-9130 | Q4 | 2 |
| 1356 | Journal of Molecular Graphics and Modelling | 1093-3263 | Q2 | 2 |
| 1357 | Journal of Network and Computer Applications | 1084-8045 | Q1 | 2 |
| 1358 | Journal of Network and Systems Management | 1064-7570 | Q1 | 2 |
| 1359 | Journal of NeuroVirology | 1355-0284 | Q3 | 2 |
| 1360 | Journal of Oilseeds Research | 0970-2776 | — | 2 |
| 1361 | Journal of Peptide Science | 1075-2617 | Q2 | 2 |
| 1362 | Journal of Pharmacology and Experimental Therapeutics | 0022-3565 | Q2 | 2 |
| 1363 | Journal of Physics Communications | 2399-6528 | Q2 | 2 |
| 1364 | Journal of Physics Materials | 2515-7639 | Q1 | 2 |
| 1365 | Journal of Policy Modeling | 0161-8938 | Q2 | 2 |
| 1366 | Journal of Porphyrins and Phthalocyanines | 1088-4246 | Q3 | 2 |
| 1367 | Journal of Probability and Statistics | 1687-952X | — | 2 |
| 1368 | Journal of Proteomics | 1874-3919 | Q2 | 2 |
| 1369 | Journal of Quantitative Economics | 0971-1554 | Q3 | 2 |
| 1370 | Journal of Science Advanced Materials and Devices | 2468-2179 | Q1 | 2 |
| 1371 | Journal of Semiconductors | 1674-4926 | Q1 | 2 |
| 1372 | Journal of Solar Energy Engineering | 0199-6231 | Q2 | 2 |
| 1373 | Journal of Space Weather and Space Climate | 2115-7251 | Q2 | 2 |
| 1374 | Journal of Structural Biology | 1047-8477 | Q2 | 2 |
| 1375 | Journal of Structural Engineering | 0733-9445 | Q1 | 2 |
| 1376 | Journal of Systems Architecture | 1383-7621 | Q1 | 2 |
| 1377 | Journal of Transportation Engineering Part A Systems | 2473-2893 | Q2 | 2 |
| 1378 | Journal of Visual Communication and Image Representation | 1047-3203 | Q1 | 2 |
| 1379 | Journal of Wind Engineering and Industrial Aerodynamics | 0167-6105 | Q1 | 2 |
| 1380 | Journal of medical imaging | 2329-4302 | Q2 | 2 |
| 1381 | Journal of the Asia Pacific Economy | 1354-7860 | Q2 | 2 |
| 1382 | Journal of the Korean Ceramic Society | 1229-7801 | Q2 | 2 |
| 1383 | Knowledge and Information Systems | 0219-1377 | Q1 | 2 |
| 1384 | Land | 2073-445X | Q1 | 2 |
| 1385 | Land Degradation and Development | 1085-3278 | Q1 | 2 |
| 1386 | Laser Physics | 1054-660X | Q3 | 2 |
| 1387 | Letters on Materials | 2218-5046 | Q3 | 2 |
| 1388 | Life Cycle Reliability and Safety Engineering | 2520-1352 | Q3 | 2 |
| 1389 | Luminescence | 1522-7235 | Q3 | 2 |
| 1390 | Machine Learning | 0885-6125 | Q1 | 2 |
| 1391 | Machines | 2075-1702 | Q2 | 2 |
| 1392 | Macromolecular Symposia | 1022-1360 | Q3 | 2 |
| 1393 | Magazine of Concrete Research | 0024-9831 | Q2 | 2 |
| 1394 | Magnetic Resonance Imaging | 0730-725X | Q2 | 2 |
| 1395 | Management of Environmental Quality An International Journal | 1477-7835 | Q1 | 2 |
| 1396 | Manufacturing Review | 2265-4224 | Q2 | 2 |
| 1397 | Margin The Journal of Applied Economic Research | 0025-2921 | Q3 | 2 |
| 1398 | Marine Structures | 0951-8339 | Q1 | 2 |
| 1399 | Materials Today Electronics | 2772-9494 | Q1 | 2 |
| 1400 | Materials Today Physics | 2542-5293 | Q1 | 2 |
| 1401 | Materials Today Sustainability | 2589-2347 | Q1 | 2 |
| 1402 | Materials for Renewable and Sustainable Energy | 2194-1459 | Q1 | 2 |
| 1403 | Mathematical Problems in Engineering | 1024-123X | Q3 | 2 |
| 1404 | Mathematical and Computational Applications | 1300-686X | Q2 | 2 |
| 1405 | Measurement Sensors | 2665-9174 | Q1 | 2 |
| 1406 | Mechanics of Composite Materials | 0032-390X | Q3 | 2 |
| 1407 | Mechatronics | 0957-4158 | Q1 | 2 |
| 1408 | Media Culture & Society | 0163-4437 | Q1 | 2 |
| 1409 | Metabolic Engineering | 1096-7176 | Q1 | 2 |
| 1410 | Metabolites | 2218-1989 | Q2 | 2 |
| 1411 | Metallurgical and Materials Transactions B | 1073-5615 | Q2 | 2 |
| 1412 | Microbiological Research | 0944-5013 | Q1 | 2 |
| 1413 | Microchimica Acta | 0026-3672 | Q2 | 2 |
| 1414 | Microscopy and Microanalysis | 1431-9276 | Q3 | 2 |
| 1415 | Mineral Processing and Extractive Metallurgy Review | 0882-7508 | Q1 | 2 |
| 1416 | Mobile Networks and Applications | 1383-469X | Q2 | 2 |
| 1417 | Monatshefte für Mathematik | 0026-9255 | Q2 | 2 |
| 1418 | Nano Micro Mechanics Review | 3082-8058 | — | 2 |
| 1419 | Nano Research | 1998-0000 | Q1 | 2 |
| 1420 | Nanomedicine | 1743-5889 | Q1 | 2 |
| 1421 | Nanomedicine Nanotechnology Biology and Medicine | 1549-9634 | Q1 | 2 |
| 1422 | Nature Astronomy | 2397-3366 | Q1 | 2 |
| 1423 | Nature Mental Health | 2731-6076 | Q1 | 2 |
| 1424 | Nature Physics | 1745-2473 | Q1 | 2 |
| 1425 | Next Energy | 2949-821X | Q1 | 2 |
| 1426 | Nondestructive Testing And Evaluation | 1058-9759 | Q2 | 2 |
| 1427 | Nonlinear Analysis Modelling and Control | 1392-5113 | Q2 | 2 |
| 1428 | Nuclear Physics B | 0550-3213 | Q2 | 2 |
| 1429 | Numerical Mathematics Theory Methods and Applications | 1004-8979 | Q1 | 2 |
| 1430 | OPSEARCH | 0030-3887 | Q2 | 2 |
| 1431 | Oceans | 2673-1924 | Q2 | 2 |
| 1432 | Optimal Control Applications and Methods | 0143-2087 | Q2 | 2 |
| 1433 | Oral Diseases | 1354-523X | Q1 | 2 |
| 1434 | Parasite Immunology | 0141-9838 | Q2 | 2 |
| 1435 | Pathogens and Disease | 2049-632X | Q2 | 2 |
| 1436 | PeerJ | 2167-8359 | Q1 | 2 |
| 1437 | Phase Transitions | 0141-1594 | Q3 | 2 |
| 1438 | Physical Sciences Reviews | 2365-6581 | Q3 | 2 |
| 1439 | Polymer Bulletin | 0170-0839 | Q2 | 2 |
| 1440 | Polymer International | 0959-8103 | Q2 | 2 |
| 1441 | Polymers and Polymer Composites | 0967-3911 | Q2 | 2 |
| 1442 | Power Research | 0973-0338 | — | 2 |
| 1443 | Practice Periodical on Structural Design and Construction | 1084-0680 | — | 2 |
| 1444 | Precision Engineering | 0141-6359 | Q1 | 2 |
| 1445 | Procedia CIRP | 2212-8271 | — | 2 |
| 1446 | Proceedings of the Edinburgh Mathematical Society | 0013-0915 | Q2 | 2 |
| 1447 | Proceedings of the Institution of Civil Engineers - Structures and Buildings | 0965-0911 | Q3 | 2 |
| 1448 | Progress in Energy and Combustion Science | 0360-1285 | Q1 | 2 |
| 1449 | Progress in Engineering Science | 2950-4252 | Q2 | 2 |
| 1450 | Progress in Materials Science | 0079-6425 | Q1 | 2 |
| 1451 | Protein Expression and Purification | 1046-5928 | Q3 | 2 |
| 1452 | Protein Science | 0961-8368 | Q1 | 2 |
| 1453 | Publications of the Astronomical Society of Australia | 1323-3580 | Q1 | 2 |
| 1454 | Quaternary International | 1040-6182 | Q2 | 2 |
| 1455 | RSC Applied Polymers | 2755-371X | Q1 | 2 |
| 1456 | RSC Mechanochemistry | 2976-8683 | Q2 | 2 |
| 1457 | RSC Medicinal Chemistry | 2632-8682 | Q1 | 2 |
| 1458 | Radiation Physics and Chemistry | 0969-806X | Q2 | 2 |
| 1459 | Radiation effects and defects in solids | 1026-549X | Q3 | 2 |
| 1460 | Reliability Engineering & System Safety | 0951-8320 | Q1 | 2 |
| 1461 | Rendiconti del Circolo Matematico di Palermo Series 2 | 0009-725X | Q2 | 2 |
| 1462 | Research Policy | 0048-7333 | Q1 | 2 |
| 1463 | Research in Economics | 0035-5054 | Q3 | 2 |
| 1464 | Resonance | 0971-8044 | Q3 | 2 |
| 1465 | Results in Chemistry | 2211-7156 | Q2 | 2 |
| 1466 | Results in Earth Sciences | 2211-7148 | — | 2 |
| 1467 | Results in Materials | 2590-048X | Q2 | 2 |
| 1468 | Results in Mathematics | 0378-6218 | Q1 | 2 |
| 1469 | Review of Development Economics | 1363-6669 | Q1 | 2 |
| 1470 | Revista de Fomento Social | 0370-0046 | Q2 | 2 |
| 1471 | SN Comprehensive Clinical Medicine | 2523-8973 | Q4 | 2 |
| 1472 | SciPost Physics Proceedings | 2666-4003 | — | 2 |
| 1473 | Science Advances | 2375-2548 | Q1 | 2 |
| 1474 | Security and Privacy | 2475-6725 | — | 2 |
| 1475 | Seminars in Cancer Biology | 1044-579X | Q1 | 2 |
| 1476 | Sensors International | 2666-3511 | Q1 | 2 |
| 1477 | Shape Memory and Superelasticity | 2199-384X | Q2 | 2 |
| 1478 | Ships and Offshore Structures | 1744-5302 | Q2 | 2 |
| 1479 | Solid State Ionics | 0167-2738 | Q2 | 2 |
| 1480 | Spatial Information Research | 2366-3286 | Q2 | 2 |
| 1481 | Statistics & Probability Letters | 0167-7152 | Q3 | 2 |
| 1482 | Stochastics | 1744-2508 | Q2 | 2 |
| 1483 | Surface Review and Letters | 0218-625X | Q3 | 2 |
| 1484 | Talanta | 0039-9140 | Q1 | 2 |
| 1485 | The Astronomical Journal | 0004-6256 | Q1 | 2 |
| 1486 | The Astrophysical Journal Letters | 2041-8205 | Q1 | 2 |
| 1487 | The European Physical Journal Applied Physics | 1286-0042 | Q4 | 2 |
| 1488 | The Japan Society of Applied Physics |  | — | 2 |
| 1489 | The Journal of Difference Equations and Applications | 1023-6198 | Q3 | 2 |
| 1490 | The Journal of Engineering | 2051-3305 | Q3 | 2 |
| 1491 | The Journal of Object Technology | 1660-1769 | Q4 | 2 |
| 1492 | The Open Civil Engineering Journal | 1874-1495 | Q4 | 2 |
| 1493 | Tourism Recreation Research | 0250-8281 | Q1 | 2 |
| 1494 | Transactions of Nonferrous Metals Society of China | 1003-6326 | Q1 | 2 |
| 1495 | Transboundary and Emerging Diseases | 1865-1674 | Q1 | 2 |
| 1496 | Transnational Corporation Review | 1918-6444 | Q2 | 2 |
| 1497 | Transportation research procedia | 2352-1457 | — | 2 |
| 1498 | Ultrasonics | 0041-624X | Q1 | 2 |
| 1499 | Ultrasonics Sonochemistry | 1350-4177 | Q1 | 2 |
| 1500 | Utilities Policy | 0957-1787 | Q1 | 2 |
| 1501 | Veterinary Vaccine | 2772-5359 | — | 2 |
| 1502 | Virulence | 2150-5594 | Q1 | 2 |
| 1503 | VirusDisease | 2347-3517 | Q3 | 2 |
| 1504 | Waste and Biomass Valorization | 1877-2641 | Q2 | 2 |
| 1505 | Water Conservation Science and Engineering | 2364-5687 | Q2 | 2 |
| 1506 | Water Economics and Policy | 2382-624X | Q2 | 2 |
| 1507 | Water Resources Management | 0920-4741 | Q1 | 2 |
| 1508 | Water Science & Technology Water Supply | 1606-9749 | Q2 | 2 |
| 1509 | Water Security | 2468-3124 | Q1 | 2 |
| 1510 | Welding in the World | 0043-2288 | Q1 | 2 |
| 1511 | Wiley Interdisciplinary Reviews Data Mining and Knowledge Discovery | 1942-4787 | Q1 | 2 |
| 1512 | Wireless Networks | 1022-0038 | Q2 | 2 |
| 1513 | World Development Sustainability | 2772-655X | Q1 | 2 |
| 1514 | ZAMM ‐ Journal of Applied Mathematics and Mechanics / Zeitschrift für Angewandte Mathematik und Mechanik | 0044-2267 | Q2 | 2 |
| 1515 | Zeitschrift für angewandte Mathematik und Physik | 0044-2275 | Q1 | 2 |
| 1516 | npj 2D Materials and Applications | 2397-7132 | Q1 | 2 |
| 1517 | npj natural hazards. | 2948-2100 | — | 2 |
| 1518 | 100th American Meteorological Society Annual Meeting |  | — | 1 |
| 1519 | 2D Materials | 2053-1583 | Q1 | 1 |
| 1520 | 3D Printing in Medicine | 2365-6271 | Q2 | 1 |
| 1521 | 4OR | 1614-2411 | Q1 | 1 |
| 1522 | AAPS PharmSciTech | 1530-9932 | Q1 | 1 |
| 1523 | ACM Journal on Autonomous Transportation Systems | 2833-0528 | — | 1 |
| 1524 | ACM Transactions on Intelligent Systems and Technology | 2157-6904 | Q1 | 1 |
| 1525 | ACM Transactions on Reconfigurable Technology and Systems | 1936-7406 | Q2 | 1 |
| 1526 | ACM Transactions on Spatial Algorithms and Systems | 2374-0353 | Q2 | 1 |
| 1527 | ACS Agricultural Science & Technology | 2692-1952 | Q1 | 1 |
| 1528 | ACS Central Science | 2374-7943 | Q1 | 1 |
| 1529 | ACS Combinatorial Science | 2156-8944 | — | 1 |
| 1530 | ACS ES&T Water | 2690-0637 | Q1 | 1 |
| 1531 | ACS Nanoscience Au | 2694-2496 | Q1 | 1 |
| 1532 | ACS electrochemistry. | 2997-0571 | — | 1 |
| 1533 | AIJR Abstracts |  | — | 1 |
| 1534 | AMBER – ABBS Management Business and Entrepreneurship Review | 0976-3341 | — | 1 |
| 1535 | ANNALI DELL UNIVERSITA DI FERRARA | 0430-3202 | Q3 | 1 |
| 1536 | ANZIAM Journal | 0334-2700 | Q4 | 1 |
| 1537 | APL Energy | 2770-9000 | — | 1 |
| 1538 | APL Engineering Physics | 3066-7380 | — | 1 |
| 1539 | APL Machine Learning | 2770-9019 | Q1 | 1 |
| 1540 | APOPTOSIS | 1360-8185 | Q1 | 1 |
| 1541 | APS Open Science | 3070-2240 | — | 1 |
| 1542 | ASCE-ASME Journal of Risk and Uncertainty in Engineering Systems Part B Mechanical Engineering | 2332-9017 | Q2 | 1 |
| 1543 | ASME Open Journal of Engineering | 2770-3495 | Q2 | 1 |
| 1544 | ASPET Discovery | 3050-5674 | — | 1 |
| 1545 | Academia Letters | 2771-9359 | — | 1 |
| 1546 | Academia green energy. | 2998-3665 | — | 1 |
| 1547 | Acoustics | 2624-599X | Q3 | 1 |
| 1548 | Acta Astronautica | 0094-5765 | Q1 | 1 |
| 1549 | Acta Biomaterialia | 1742-7061 | Q1 | 1 |
| 1550 | Acta Crystallographica Section C Structural Chemistry | 2053-2296 | Q3 | 1 |
| 1551 | Acta Crystallographica Section D Structural Biology | 2059-7983 | Q1 | 1 |
| 1552 | Acta Crystallographica Section F Structural Biology Communications | 2053-230X | Q3 | 1 |
| 1553 | Acta Mathematica Universitatis Comenianae | 0862-9544 | Q3 | 1 |
| 1554 | Acta Mechanica Sinica | 0567-7718 | Q1 | 1 |
| 1555 | Acta Scientific Medical Sciences | 2582-0931 | — | 1 |
| 1556 | Acta Universitatis Sapientiae Mathematica | 1844-6094 | Q3 | 1 |
| 1557 | Additive Manufacturing Frontiers | 2950-4317 | Q1 | 1 |
| 1558 | Additive Manufacturing Letters | 2772-3690 | Q1 | 1 |
| 1559 | Additive manufacturing | 2214-7810 | Q1 | 1 |
| 1560 | Advanced Composite Materials | 0924-3046 | Q2 | 1 |
| 1561 | Advanced Composites and Hybrid Materials | 2522-0128 | Q1 | 1 |
| 1562 | Advanced Drug Delivery Reviews | 0169-409X | Q1 | 1 |
| 1563 | Advanced Materials Letters | 0976-3961 | — | 1 |
| 1564 | Advanced NanoBiomed Research | 2699-9307 | Q1 | 1 |
| 1565 | Advanced Photonics Research | 2699-9293 | — | 1 |
| 1566 | Advanced Robotics | 0169-1864 | Q2 | 1 |
| 1567 | Advanced Science Engineering and Medicine | 2164-6627 | — | 1 |
| 1568 | Advanced Sensor and Energy Materials | 2773-045X | Q2 | 1 |
| 1569 | Advances in Applied Clifford Algebras | 0188-7009 | Q2 | 1 |
| 1570 | Advances in Applied Mathematics and Mechanics | 2070-0733 | Q2 | 1 |
| 1571 | Advances in Atmospheric Sciences | 0256-1530 | Q1 | 1 |
| 1572 | Advances in Civil Engineering | 1687-8086 | Q2 | 1 |
| 1573 | Advances in Civil Engineering Materials | 2165-3984 | Q2 | 1 |
| 1574 | Advances in Differential Equations and Control Processes | 0974-3243 | — | 1 |
| 1575 | Advances in Economics and Business | 2331-5059 | — | 1 |
| 1576 | Advances in Engineering Software | 0965-9978 | Q1 | 1 |
| 1577 | Advances in Manufacturing | 2095-3127 | Q1 | 1 |
| 1578 | Advances in Materials Science and Engineering | 1687-8434 | Q2 | 1 |
| 1579 | Advances in Natural Sciences Nanoscience and Nanotechnology | 2043-6254 | Q2 | 1 |
| 1580 | Advances in Operator Theory | 2538-225X | Q3 | 1 |
| 1581 | Advances in Polymer Technology | 0730-6679 | Q2 | 1 |
| 1582 | Advances in Pure and Applied Mathematics | 1867-1152 | Q3 | 1 |
| 1583 | Advances in Structural Engineering | 1369-4332 | Q2 | 1 |
| 1584 | Aequationes Mathematicae | 0001-9054 | Q2 | 1 |
| 1585 | Aerosol Science and Engineering | 2510-375X | Q2 | 1 |
| 1586 | Aerosol Science and Technology | 0278-6826 | Q2 | 1 |
| 1587 | Agri Gene | 2352-2151 | — | 1 |
| 1588 | Agricultural Systems | 0308-521X | Q1 | 1 |
| 1589 | Agriculture Association of Textile Chemical and Critical Reviews | 3041-5683 | — | 1 |
| 1590 | Air Quality Atmosphere & Health | 1873-9318 | Q2 | 1 |
| 1591 | All Earth | 2766-9645 | Q2 | 1 |
| 1592 | American Journal of Physiology-Cell Physiology | 0363-6143 | Q1 | 1 |
| 1593 | American Journal of Physiology-Heart and Circulatory Physiology | 0363-6135 | Q1 | 1 |
| 1594 | American Scientific Research Journal for Engineering, Technology, and Sciences | 2313-4402 | — | 1 |
| 1595 | American journal of rural development | 2333-4762 | — | 1 |
| 1596 | Amino Acids | 0939-4451 | Q1 | 1 |
| 1597 | Analysis & Sensing | 2629-2742 | Q2 | 1 |
| 1598 | Analysis Mathematica | 0133-3852 | Q2 | 1 |
| 1599 | Analytical Science Advances | 2628-5452 | Q1 | 1 |
| 1600 | Analytical and Bioanalytical Chemistry | 1618-2642 | Q2 | 1 |
| 1601 | Annalen der Physik | 0003-3804 | Q2 | 1 |
| 1602 | Annales d Endocrinologie | 0003-4266 | Q2 | 1 |
| 1603 | Annali di Ca’ Foscari Serie orientale | 1125-3789 | Q3 | 1 |
| 1604 | Annali di Matematica Pura ed Applicata (1923 -) | 0373-3114 | Q1 | 1 |
| 1605 | Annals of Advances in Chemistry | 2576-3768 | — | 1 |
| 1606 | Annals of Combinatorics | 0218-0006 | Q2 | 1 |
| 1607 | Annals of Data Science | 2198-5804 | Q1 | 1 |
| 1608 | Annals of Nuclear Energy | 0306-4549 | Q1 | 1 |
| 1609 | Annual Review of Environment and Resources | 1543-5938 | Q1 | 1 |
| 1610 | Anti-Corrosion Methods and Materials | 0003-5599 | Q2 | 1 |
| 1611 | Apmis | 0903-4641 | Q2 | 1 |
| 1612 | Applicable Analysis | 0003-6811 | Q2 | 1 |
| 1613 | Applicationes Mathematicae | 1233-7234 | Q4 | 1 |
| 1614 | Applied Artificial Intelligence | 0883-9514 | Q1 | 1 |
| 1615 | Applied Biochemistry and Biotechnology | 0273-2289 | Q2 | 1 |
| 1616 | Applied Composite Materials | 0929-189X | Q2 | 1 |
| 1617 | Applied Computational Intelligence and Soft Computing | 1687-9724 | Q1 | 1 |
| 1618 | Applied Economics Letters | 1350-4851 | Q3 | 1 |
| 1619 | Applied Geochemistry | 0883-2927 | Q1 | 1 |
| 1620 | Applied Physics Express | 1882-0778 | Q2 | 1 |
| 1621 | Applied Psychophysiology and Biofeedback | 0363-3586 | Q2 | 1 |
| 1622 | Applied Science and Engineering Progress | 2672-9156 | Q3 | 1 |
| 1623 | Applied Spatial Analysis and Policy | 1874-4621 | Q2 | 1 |
| 1624 | Applied Spectroscopy Practica | 2755-1857 | — | 1 |
| 1625 | Applied Surface Science Advances | 2666-5239 | Q1 | 1 |
| 1626 | AppliedMath | 2673-9909 | Q3 | 1 |
| 1627 | Aquatic Conservation Marine and Freshwater Ecosystems | 1052-7613 | Q1 | 1 |
| 1628 | Archives of Metallurgy and Materials | 0860-7052 | Q3 | 1 |
| 1629 | Archives of Nanomedicine Open Access Journal | 2637-6660 | — | 1 |
| 1630 | Artificial Intelligence in Geosciences | 2666-5441 | Q1 | 1 |
| 1631 | Asia Pacific Journal of Health Management | 1833-3818 | Q4 | 1 |
| 1632 | Asia Pacific Journal of Operational Research | 0217-5959 | Q3 | 1 |
| 1633 | Asia Pacific Journal of Tourism Research | 1094-1665 | Q1 | 1 |
| 1634 | Asia-Pacific Journal of Atmospheric Sciences | 1976-7633 | Q2 | 1 |
| 1635 | Asian Journal of Civil Engineering | 1563-0854 | Q2 | 1 |
| 1636 | Asian Journal of Interdisciplinary Research | 2581-8430 | Q2 | 1 |
| 1637 | Asian Journal of Law and Economics | 2154-4611 | Q3 | 1 |
| 1638 | Asian Journal of Water Environment and Pollution | 0972-9860 | Q4 | 1 |
| 1639 | Asian Pacific Journal of Cancer Care | 2588-3682 | Q4 | 1 |
| 1640 | Asiascape Digital Asia | 2214-2304 | Q2 | 1 |
| 1641 | Astrophysical Bulletin | 1990-3413 | Q3 | 1 |
| 1642 | Astrophysics Source Code Library |  | — | 1 |
| 1643 | Atmospheric Science Letters | 1530-261X | Q2 | 1 |
| 1644 | Austin Journal of Pharmacology and Therapeutics | 2373-6208 | — | 1 |
| 1645 | Australasian Physical & Engineering Sciences in Medicine | 0158-9938 | — | 1 |
| 1646 | Australian Journal of Agricultural and Resource Economics | 1364-985X | Q1 | 1 |
| 1647 | Australian Journal of Mechanical Engineering | 1448-4846 | Q3 | 1 |
| 1648 | Automation | 2673-4052 | Q2 | 1 |
| 1649 | Axioms | 2075-1680 | — | 1 |
| 1650 | Azerbaijan Journal of High Performance Computing | 2616-6127 | — | 1 |
| 1651 | BIO-PROTOCOL | 2331-8325 | Q2 | 1 |
| 1652 | BMC Bioinformatics | 1471-2105 | Q1 | 1 |
| 1653 | BMC Geriatrics | 1471-2318 | Q1 | 1 |
| 1654 | BMC Psychiatry | 1471-244X | Q1 | 1 |
| 1655 | BOHR International Journal of Neurology and Neuroscience | 2583-9268 | — | 1 |
| 1656 | Big Data Research | 2214-5796 | Q1 | 1 |
| 1657 | BioNanoScience | 2191-1630 | Q3 | 1 |
| 1658 | Bioanalysis | 1757-6180 | Q2 | 1 |
| 1659 | Biocatalysis and Agricultural Biotechnology | 1878-8181 | Q1 | 1 |
| 1660 | Biocell | 0327-9545 | Q4 | 1 |
| 1661 | Biochemical Engineering Journal | 1369-703X | Q2 | 1 |
| 1662 | Biochemical Journal | 0264-6021 | Q1 | 1 |
| 1663 | Biochemistry and Biophysics Reports | 2405-5808 | Q2 | 1 |
| 1664 | Biochimica et Biophysica Acta (BBA) - Molecular Basis of Disease | 0925-4439 | Q1 | 1 |
| 1665 | Biochimica et Biophysica Acta (BBA) - Molecular and Cell Biology of Lipids | 1388-1981 | Q2 | 1 |
| 1666 | Biochimica et Biophysica Acta (BBA) - Proteins and Proteomics | 1570-9639 | Q2 | 1 |
| 1667 | Bioelectrochemistry | 1567-5394 | Q2 | 1 |
| 1668 | Biofuels | 1759-7269 | Q3 | 1 |
| 1669 | Bioinspiration & Biomimetics | 1748-3182 | Q2 | 1 |
| 1670 | Biologia | 0006-3088 | Q2 | 1 |
| 1671 | Biology Methods and Protocols | 2396-8923 | Q2 | 1 |
| 1672 | Biomedical Engineering Advances | 2667-0992 | — | 1 |
| 1673 | Biomedical Engineering Letters | 2093-985X | Q2 | 1 |
| 1674 | Biomedicine & Pharmacotherapy | 0753-3322 | Q1 | 1 |
| 1675 | Biomedicines | 2227-9059 | Q1 | 1 |
| 1676 | Biomimetics | 2313-7673 | Q2 | 1 |
| 1677 | Biomolecules | 2218-273X | Q1 | 1 |
| 1678 | Bioorganic & Medicinal Chemistry Letters | 0960-894X | Q2 | 1 |
| 1679 | Biophysical Chemistry | 0301-4622 | Q2 | 1 |
| 1680 | Biopolymers | 0006-3525 | Q2 | 1 |
| 1681 | Bioprocess and Biosystems Engineering | 1615-7591 | Q2 | 1 |
| 1682 | Biosafety and Health | 2590-0536 | Q2 | 1 |
| 1683 | Biostatistics and Biometrics Open Access Journal | 2573-2633 | — | 1 |
| 1684 | Biosystems | 0303-2647 | Q2 | 1 |
| 1685 | Biotechnology Reports | 2215-017X | Q1 | 1 |
| 1686 | Biotechnology and Applied Biochemistry | 0885-4513 | Q2 | 1 |
| 1687 | Biotribology | 2352-5738 | Q3 | 1 |
| 1688 | Blood Cells Molecules and Diseases | 1079-9796 | Q2 | 1 |
| 1689 | Boletín de la Sociedad Matemática Mexicana | 2296-4495 | Q2 | 1 |
| 1690 | Brain Sciences | 2076-3425 | Q2 | 1 |
| 1691 | Brain stimulation | 1876-4754 | Q1 | 1 |
| 1692 | Brain-Computer Interfaces | 2326-2621 | Q2 | 1 |
| 1693 | Brazilian Journal of Physics | 0103-9733 | Q3 | 1 |
| 1694 | Briefings in Bioinformatics | 1467-5463 | Q1 | 1 |
| 1695 | British Journal of Cancer | 0007-0920 | Q1 | 1 |
| 1696 | Bulletin of Atmospheric Science and Technology | 2662-1495 | Q2 | 1 |
| 1697 | Bulletin of the Chemical Society of Japan | 0009-2673 | Q3 | 1 |
| 1698 | Bulletin of the New Zealand Society for Earthquake Engineering | 0110-0718 | Q3 | 1 |
| 1699 | Bulletin of the Russian Academy of Sciences Physics | 1062-8738 | Q3 | 1 |
| 1700 | Bulletin of the Seismological Society of America | 0037-1106 | Q1 | 1 |
| 1701 | Bulletin of the South Ural State University Series Mathematical Modelling Programming and Computer Software | 2071-0216 | Q4 | 1 |
| 1702 | CORROSION | 0010-9312 | Q3 | 1 |
| 1703 | Canadian Journal of Civil Engineering | 0315-1468 | Q3 | 1 |
| 1704 | Cancer Drug Resistance | 2578-532X | Q1 | 1 |
| 1705 | Cancer Gene Therapy | 0929-1903 | Q1 | 1 |
| 1706 | Cancer Informatics | 1176-9351 | Q3 | 1 |
| 1707 | Cancer Pathogenesis and Therapy | 2949-7132 | Q1 | 1 |
| 1708 | Cancer Reports | 2573-8348 | Q3 | 1 |
| 1709 | Cancer and Metastasis Reviews | 0167-7659 | Q1 | 1 |
| 1710 | Cancer/Radiothérapie | 1278-3218 | Q2 | 1 |
| 1711 | Cancers | 2072-6694 | Q1 | 1 |
| 1712 | Caraka Tani Journal of Sustainable Agriculture | 2599-2570 | Q2 | 1 |
| 1713 | Carbohydrate Polymer Technologies and Applications | 2666-8939 | Q1 | 1 |
| 1714 | Carcinogenesis | 0143-3334 | Q1 | 1 |
| 1715 | Cardiovascular Engineering and Technology | 1869-408X | Q2 | 1 |
| 1716 | Cell Biochemistry and Biophysics | 1085-9195 | Q2 | 1 |
| 1717 | Cell Biochemistry and Function | 0263-6484 | Q2 | 1 |
| 1718 | Cell Biology International | 1065-6995 | Q1 | 1 |
| 1719 | Cell Reports Physical Science | 2666-3864 | Q1 | 1 |
| 1720 | Cell Signaling Inflammation & Disease | 3091-3837 | — | 1 |
| 1721 | Cellular Microbiology | 1462-5814 | Q3 | 1 |
| 1722 | Cellular and Molecular Bioengineering | 1865-5025 | Q2 | 1 |
| 1723 | Cellular and Molecular Biology | 0145-5680 | — | 1 |
| 1724 | Cellular and Molecular Neurobiology | 0272-4340 | Q1 | 1 |
| 1725 | Central Asian Journal of Sustainability and Climate Research | 2958-2709 | — | 1 |
| 1726 | ChemTexts | 2199-3793 | Q1 | 1 |
| 1727 | Chemical Data Collections | 2405-8300 | Q4 | 1 |
| 1728 | Chemical Engineering Communications | 0098-6445 | Q2 | 1 |
| 1729 | Chemical Engineering Journal Green and Sustainable | 3051-0031 | — | 1 |
| 1730 | Chemical Engineering Science | 0009-2509 | Q1 | 1 |
| 1731 | Chemical Papers | 0366-6352 | Q2 | 1 |
| 1732 | ChemistryEurope | 2751-4765 | — | 1 |
| 1733 | ChemistryOpen | 2191-1363 | Q2 | 1 |
| 1734 | Chemosensors | 2227-9040 | Q2 | 1 |
| 1735 | China Agricultural Economic Review | 1756-137X | Q1 | 1 |
| 1736 | Chinese Journal of Aeronautics | 1000-9361 | Q1 | 1 |
| 1737 | Chinese Physics C | 1674-1137 | Q1 | 1 |
| 1738 | Chinese Physics Letters | 0256-307X | Q1 | 1 |
| 1739 | Circular Economy and Sustainability | 2730-597X | Q1 | 1 |
| 1740 | Ciência & Tecnologia dos Materiais | 0870-8312 | — | 1 |
| 1741 | Cleaner Materials | 2772-3976 | Q1 | 1 |
| 1742 | Cleaner Water | 2950-2632 | Q1 | 1 |
| 1743 | Cleaner and Circular Bioeconomy | 2772-8013 | Q2 | 1 |
| 1744 | Climate | 2225-1154 | Q2 | 1 |
| 1745 | Climate Change Economics | 2010-0078 | Q2 | 1 |
| 1746 | Clinical Gastroenterology and Hepatology | 1542-3565 | Q1 | 1 |
| 1747 | Clinical and Experimental Vaccine Research | 2287-3651 | Q3 | 1 |
| 1748 | Cognition Technology & Work | 1435-5558 | Q1 | 1 |
| 1749 | Cognitive Computation and Systems | 2517-7567 | Q2 | 1 |
| 1750 | Cognitive Neurodynamics | 1871-4080 | Q2 | 1 |
| 1751 | Cold Regions Science and Technology | 0165-232X | Q1 | 1 |
| 1752 | Colorectal Cancer | 1758-194X | — | 1 |
| 1753 | Communications Biology | 2399-3642 | Q1 | 1 |
| 1754 | Communications Engineering | 2731-3395 | Q1 | 1 |
| 1755 | Communications Physics | 2399-3650 | Q1 | 1 |
| 1756 | Complementary Medicine Research | 1424-7364 | Q3 | 1 |
| 1757 | Complex & Intelligent Systems | 2198-6053 | Q1 | 1 |
| 1758 | Complex Analysis and its Synergies | 2197-120X | Q3 | 1 |
| 1759 | Composites Science and Technology | 0266-3538 | Q1 | 1 |
| 1760 | Comprehensive physiology | 2040-4603 | Q1 | 1 |
| 1761 | Computational Condensed Matter | 2352-2143 | Q2 | 1 |
| 1762 | Computational Intelligence | 0824-7935 | Q2 | 1 |
| 1763 | Computational Mathematics and Modeling | 1046-283X | Q4 | 1 |
| 1764 | Computational and Mathematical Methods in Medicine | 1748-670X | — | 1 |
| 1765 | Computational and Structural Biotechnology Journal | 2001-0370 | Q1 | 1 |
| 1766 | Computer Methods in Applied Mechanics and Engineering | 0045-7825 | Q1 | 1 |
| 1767 | Computer Standards & Interfaces | 0920-5489 | Q1 | 1 |
| 1768 | Computerized Medical Imaging and Graphics | 0730-4862 | Q1 | 1 |
| 1769 | Computers, materials & continua/Computers, materials & continua (Print) | 1546-2218 | Q2 | 1 |
| 1770 | Computing and Informatics | 1335-9150 | Q3 | 1 |
| 1771 | Contemporary Mathematics | 2705-1056 | Q3 | 1 |
| 1772 | Contemporary South Asia | 0958-4935 | Q2 | 1 |
| 1773 | Contemporary Voice of Dalit | 2455-328X | — | 1 |
| 1774 | Continental Shelf Research | 0278-4343 | Q1 | 1 |
| 1775 | Continuum Mechanics and Thermodynamics | 0935-1175 | Q2 | 1 |
| 1776 | Control Engineering Practice | 0967-0661 | Q1 | 1 |
| 1777 | Critical Reviews in Biomedical Engineering | 0278-940X | Q3 | 1 |
| 1778 | Critical Reviews in Biotechnology | 0738-8551 | Q1 | 1 |
| 1779 | Critical Reviews in Food Science and Nutrition | 1040-8398 | Q1 | 1 |
| 1780 | Critical Reviews in Microbiology | 1040-841X | Q1 | 1 |
| 1781 | Critical Reviews in Toxicology | 0045-6446 | Q1 | 1 |
| 1782 | Crystallography Reports | 1063-7745 | Q4 | 1 |
| 1783 | Current Biology | 0960-9822 | Q1 | 1 |
| 1784 | Current Issues in Language Planning | 1466-4208 | Q1 | 1 |
| 1785 | Current Medicinal Chemistry | 0929-8673 | Q1 | 1 |
| 1786 | Current Nanoscience | 1573-4137 | Q3 | 1 |
| 1787 | Current Opinion in Environmental Science & Health | 2468-5844 | Q1 | 1 |
| 1788 | Current Opinion in Solid State and Materials Science | 1359-0286 | Q1 | 1 |
| 1789 | Current Problems in Cancer | 0147-0272 | Q2 | 1 |
| 1790 | Current Problems in Cardiology | 0146-2806 | — | 1 |
| 1791 | Current Research in Neurobiology | 2665-945X | Q1 | 1 |
| 1792 | Current Research in Virological Science | 2666-478X | — | 1 |
| 1793 | Current Topics in Medicinal Chemistry | 1568-0266 | Q3 | 1 |
| 1794 | Cyber security. | 2398-5100 | Q1 | 1 |
| 1795 | DNA and Cell Biology | 1044-5498 | Q2 | 1 |
| 1796 | Deep Sea Research Part I Oceanographic Research Papers | 0967-0637 | Q1 | 1 |
| 1797 | Defect and diffusion forum/Diffusion and defect data, solid state data. Part A, Defect and diffusion forum | 1012-0386 | Q4 | 1 |
| 1798 | Defence Technology | 2214-9147 | Q1 | 1 |
| 1799 | Dental Materials | 0109-5641 | Q1 | 1 |
| 1800 | Design Automation for Embedded Systems | 0929-5585 | Q3 | 1 |
| 1801 | Development Engineering | 2352-7285 | Q1 | 1 |
| 1802 | Developmental Biology | 0012-1606 | Q2 | 1 |
| 1803 | Diabetes | 0012-1797 | Q1 | 1 |
| 1804 | Diabetology International | 2190-1678 | Q3 | 1 |
| 1805 | Digest Journal of Nanomaterials and Biostructures | 1842-3582 | Q3 | 1 |
| 1806 | Digital Discovery | 2635-098X | Q1 | 1 |
| 1807 | Discover Computing | 2948-2992 | Q2 | 1 |
| 1808 | Discover Electrochemistry. | 3005-1215 | — | 1 |
| 1809 | Discover Environment | 2731-9431 | Q1 | 1 |
| 1810 | Discover Geoscience | 2948-1589 | — | 1 |
| 1811 | Discover Life | 2948-2976 | Q3 | 1 |
| 1812 | Discover Plants. | 3005-1207 | — | 1 |
| 1813 | Discover Polymers. | 3004-9377 | — | 1 |
| 1814 | Discover Public Health | 3005-0774 | Q3 | 1 |
| 1815 | Drug Design Development and Therapy | 1177-8881 | Q1 | 1 |
| 1816 | Drug Development Research | 0272-4391 | Q2 | 1 |
| 1817 | ECS Sensors Plus | 2754-2726 | Q1 | 1 |
| 1818 | EMBO Reports | 1469-221X | Q1 | 1 |
| 1819 | EURASIP Journal on Audio Speech and Music Processing | 1687-4714 | Q2 | 1 |
| 1820 | EURASIP Journal on Wireless Communications and Networking | 1687-1472 | Q2 | 1 |
| 1821 | Earth s Future | 2328-4277 | Q1 | 1 |
| 1822 | Earthquake Engineering & Structural Dynamics | 0098-8847 | Q1 | 1 |
| 1823 | Ecohydrology | 1936-0584 | Q1 | 1 |
| 1824 | Ecological Complexity | 1476-945X | Q2 | 1 |
| 1825 | Ecological Modelling | 0304-3800 | Q1 | 1 |
| 1826 | Economic Analysis and Policy | 0313-5926 | Q1 | 1 |
| 1827 | Economic Change and Restructuring | 1573-9414 | Q2 | 1 |
| 1828 | Economic Modelling | 0264-9993 | Q1 | 1 |
| 1829 | Economic Papers A journal of applied economics and policy | 0812-0439 | Q2 | 1 |
| 1830 | Ecotoxicology and Environmental Safety | 0147-6513 | Q1 | 1 |
| 1831 | Eksploatacja i Niezawodnosc - Maintenance and Reliability | 1507-2711 | Q2 | 1 |
| 1832 | Electrical and Electronics Engineering An International Journal | 2200-5846 | — | 1 |
| 1833 | Electroanalysis | 1040-0397 | Q3 | 1 |
| 1834 | Electrochemical Science Advances | 2698-5977 | Q1 | 1 |
| 1835 | Electronic Commerce Research | 1389-5753 | Q1 | 1 |
| 1836 | Electronic Commerce Research and Applications | 1567-4223 | Q1 | 1 |
| 1837 | Electronic Journal of Graph Theory and Applications | 2338-2287 | Q2 | 1 |
| 1838 | Electronic Journal of Linear Algebra | 1081-3810 | Q1 | 1 |
| 1839 | Electronic Materials Letters | 1738-8090 | Q2 | 1 |
| 1840 | Electronic Notes in Discrete Mathematics | 1571-0653 | — | 1 |
| 1841 | Elementa Science of the Anthropocene | 2325-1026 | Q1 | 1 |
| 1842 | Energy & environment materials | 2575-0348 | Q1 | 1 |
| 1843 | Energy Conversion and Management X | 2590-1745 | Q1 | 1 |
| 1844 | Energy Nexus | 2772-4271 | Q1 | 1 |
| 1845 | Energy Research & Social Science | 2214-6296 | Q1 | 1 |
| 1846 | Energy Science | 2972-3795 | — | 1 |
| 1847 | Energy Sources Part B Economics Planning and Policy | 1556-7249 | Q2 | 1 |
| 1848 | Energy Storage and Saving | 2772-6835 | Q1 | 1 |
| 1849 | Energy Strategy Reviews | 2211-467X | Q1 | 1 |
| 1850 | Engineering & Technology Reference | 2056-4007 | — | 1 |
| 1851 | Engineering Analysis with Boundary Elements | 0955-7997 | Q1 | 1 |
| 1852 | Engineering Computations | 0264-4401 | Q2 | 1 |
| 1853 | Environmental Advances | 2666-7657 | Q1 | 1 |
| 1854 | Environmental Development | 2211-4645 | Q1 | 1 |
| 1855 | Environmental Economics and Policy Studies | 1432-847X | Q2 | 1 |
| 1856 | Environmental Geotechnics | 2051-803X | Q2 | 1 |
| 1857 | Environmental Impact Assessment Review | 0195-9255 | Q1 | 1 |
| 1858 | Environmental Modeling & Assessment | 1420-2026 | Q2 | 1 |
| 1859 | Environmental Modelling & Software | 1364-8152 | Q1 | 1 |
| 1860 | Environmental Research Communications | 2515-7620 | Q1 | 1 |
| 1861 | Environmental Sciences Europe | 2190-4715 | Q1 | 1 |
| 1862 | Environmental Technology Reviews | 2162-2515 | Q1 | 1 |
| 1863 | Environmental and Molecular Mutagenesis | 0893-6692 | Q2 | 1 |
| 1864 | Epidemics | 1755-4365 | Q1 | 1 |
| 1865 | European Actuarial Journal | 2190-9733 | Q2 | 1 |
| 1866 | European Journal of Cancer | 0959-8049 | Q1 | 1 |
| 1867 | European Journal of Cell Biology | 0171-9335 | Q1 | 1 |
| 1868 | European Journal of Control | 0947-3580 | Q1 | 1 |
| 1869 | European Journal of Medicinal Chemistry | 0223-5234 | Q1 | 1 |
| 1870 | European Journal of Pharmacology | 0014-2999 | Q1 | 1 |
| 1871 | European Journal of Soil Science | 1351-0754 | Q1 | 1 |
| 1872 | Evolutionary Bioinformatics | 1176-9343 | Q3 | 1 |
| 1873 | Evolutionary Intelligence | 1864-5909 | Q1 | 1 |
| 1874 | Evolving Systems | 1868-6478 | Q1 | 1 |
| 1875 | Experimental Cell Research | 0014-4827 | Q2 | 1 |
| 1876 | Experimental Gerontology | 0531-5565 | Q1 | 1 |
| 1877 | Experimental Parasitology | 0014-4894 | Q2 | 1 |
| 1878 | Experimental and Computational Multiphase Flow | 2661-8869 | Q1 | 1 |
| 1879 | Expert Review of Medical Devices | 1743-4440 | Q2 | 1 |
| 1880 | Exploratory Research and Hypothesis in Medicine | 2472-0712 | — | 1 |
| 1881 | FIIB Business Review | 2319-7145 | Q2 | 1 |
| 1882 | Farming System | 2949-9119 | Q1 | 1 |
| 1883 | Few-Body Systems | 0177-7963 | Q2 | 1 |
| 1884 | Fibers | 2079-6439 | Q1 | 1 |
| 1885 | Field Crops Research | 0378-4290 | Q1 | 1 |
| 1886 | Financial Innovation | 2199-4730 | Q1 | 1 |
| 1887 | Fire and Materials | 0308-0501 | Q2 | 1 |
| 1888 | Flexible and Printed Electronics | 2058-8585 | Q2 | 1 |
| 1889 | Flora | 0367-2530 | Q2 | 1 |
| 1890 | Flow Measurement and Instrumentation | 0955-5986 | Q2 | 1 |
| 1891 | Fluid Dynamics | 0015-4628 | Q3 | 1 |
| 1892 | Fluid Phase Equilibria | 0378-3812 | Q2 | 1 |
| 1893 | Fluids | 2311-5521 | Q2 | 1 |
| 1894 | Food Chemistry | 0308-8146 | Q1 | 1 |
| 1895 | Food Control | 0956-7135 | Q1 | 1 |
| 1896 | Food Safety and Risk | 2731-9245 | Q2 | 1 |
| 1897 | Food and Bioprocess Technology | 1935-5130 | Q1 | 1 |
| 1898 | Foods | 2304-8158 | Q1 | 1 |
| 1899 | Forum Mathematicum | 0933-7741 | Q1 | 1 |
| 1900 | Forum for Social Economics | 0736-0932 | Q3 | 1 |
| 1901 | Fractal and Fractional | 2504-3110 | Q2 | 1 |
| 1902 | Free Radical Biology and Medicine | 0891-5849 | Q1 | 1 |
| 1903 | Frontiers in Aging Neuroscience | 1663-4365 | Q1 | 1 |
| 1904 | Frontiers in Applied Mathematics and Statistics | 2297-4687 | Q2 | 1 |
| 1905 | Frontiers in Batteries and Electrochemistry | 2813-4974 | — | 1 |
| 1906 | Frontiers in Biomaterials Science | 2813-3749 | — | 1 |
| 1907 | Frontiers in Built Environment | 2297-3362 | Q1 | 1 |
| 1908 | Frontiers in Cancer Control and Society | 2813-835X | — | 1 |
| 1909 | Frontiers in Cellular Neuroscience | 1662-5102 | Q2 | 1 |
| 1910 | Frontiers in Communications and Networks | 2673-530X | Q2 | 1 |
| 1911 | Frontiers in Digital Health | 2673-253X | Q1 | 1 |
| 1912 | Frontiers in Energy Research | 2296-598X | Q2 | 1 |
| 1913 | Frontiers in Future Transportation | 2673-5210 | Q2 | 1 |
| 1914 | Frontiers in Genetics | 1664-8021 | Q2 | 1 |
| 1915 | Frontiers in Medicine | 2296-858X | Q1 | 1 |
| 1916 | Frontiers in Neurology | 1664-2295 | Q2 | 1 |
| 1917 | Frontiers in Neuroscience | 1662-453X | Q2 | 1 |
| 1918 | Frontiers in Oncology | 2234-943X | Q2 | 1 |
| 1919 | Frontiers in Plant Science | 1664-462X | Q1 | 1 |
| 1920 | Frontiers in Sensors | 2673-5067 | Q2 | 1 |
| 1921 | Frontiers in Tropical Diseases | 2673-7515 | Q2 | 1 |
| 1922 | Frontiers in Virology | 2673-818X | Q2 | 1 |
| 1923 | Frontiers in artificial intelligence and applications | 0922-6389 | Q4 | 1 |
| 1924 | Frontiers of Urban and Rural Planning | 2731-6661 | — | 1 |
| 1925 | Fuel Processing Technology | 0378-3820 | Q1 | 1 |
| 1926 | Functional Composites and Structures | 2631-6331 | Q2 | 1 |
| 1927 | Future Batteries | 2950-2640 | — | 1 |
| 1928 | Future Science OA | 2056-5623 | Q3 | 1 |
| 1929 | G3 Genes Genomes Genetics | 2160-1836 | Q2 | 1 |
| 1930 | Galaxies | 2075-4434 | Q1 | 1 |
| 1931 | Games | 2073-4336 | Q3 | 1 |
| 1932 | General Relativity and Gravitation | 0001-7701 | Q2 | 1 |
| 1933 | Genes | 2073-4425 | Q2 | 1 |
| 1934 | Genetics | 0016-6731 | Q1 | 1 |
| 1935 | Genome biology | 1465-6906 | Q1 | 1 |
| 1936 | Genomics | 0888-7543 | Q2 | 1 |
| 1937 | GeoJournal | 0343-2521 | Q2 | 1 |
| 1938 | Geoderma | 0016-7061 | Q1 | 1 |
| 1939 | Geoenvironmental Disasters | 2197-8670 | Q1 | 1 |
| 1940 | Geology | 0091-7613 | Q1 | 1 |
| 1941 | Geoscience Letters | 2196-4092 | Q1 | 1 |
| 1942 | Geotechnical Research | 2052-6156 | Q2 | 1 |
| 1943 | Geotextiles and Geomembranes | 0266-1144 | Q1 | 1 |
| 1944 | Geothermics | 0375-6505 | Q1 | 1 |
| 1945 | Global Economic Review | 1226-508X | Q3 | 1 |
| 1946 | Global Finance Journal | 1044-0283 | Q1 | 1 |
| 1947 | Global Health Research and Policy | 2397-0642 | Q1 | 1 |
| 1948 | Global Journal of Business Economics and Management Current Issues | 2301-2579 | — | 1 |
| 1949 | Global Journal of Flexible Systems Management | 0972-2696 | Q1 | 1 |
| 1950 | Global Journal of Human-Social Science | 0975-587X | — | 1 |
| 1951 | Global Social Welfare | 2196-8799 | Q2 | 1 |
| 1952 | Global Society | 1360-0826 | Q1 | 1 |
| 1953 | Global economy journal | 1524-5861 | Q4 | 1 |
| 1954 | Gondwana Research | 1342-937X | Q1 | 1 |
| 1955 | Gravitation and Cosmology | 0202-2893 | Q3 | 1 |
| 1956 | Green Chemistry Letters and Reviews | 1751-7192 | Q1 | 1 |
| 1957 | Green Energy and Intelligent Transportation | 2773-1537 | Q1 | 1 |
| 1958 | Green Finance | 2643-1092 | Q1 | 1 |
| 1959 | Green Technologies and Sustainability | 2949-7361 | Q1 | 1 |
| 1960 | Greenhouse Gases Science and Technology | 2152-3878 | Q2 | 1 |
| 1961 | Grey Systems Theory and Application | 2043-9377 | Q2 | 1 |
| 1962 | Gut Microbes Reports | 2993-3935 | — | 1 |
| 1963 | Gut Science | 2978-1833 | — | 1 |
| 1964 | HTM Journal of Heat Treatment and Materials | 1867-2493 | Q3 | 1 |
| 1965 | Health Systems | 2047-6965 | Q2 | 1 |
| 1966 | Helicobacter | 1083-4389 | Q1 | 1 |
| 1967 | High Energy Chemistry | 0018-1439 | Q4 | 1 |
| 1968 | High Temperature Materials and Processes | 0334-6455 | Q3 | 1 |
| 1969 | High Voltage | 2096-9813 | Q1 | 1 |
| 1970 | Historical Journal Of Film Radio and Television | 0143-9685 | Q2 | 1 |
| 1971 | Human Gene | 2773-0441 | Q4 | 1 |
| 1972 | Human-centric Computing and Information Sciences | 2192-1962 | Q2 | 1 |
| 1973 | Hybrid Advances | 2773-207X | Q1 | 1 |
| 1974 | HydroResearch | 2589-7578 | Q1 | 1 |
| 1975 | ICT Express | 2405-9595 | Q1 | 1 |
| 1976 | IEEE Antennas and Propagation Magazine | 1045-9243 | Q1 | 1 |
| 1977 | IEEE Circuits and Systems Magazine | 0163-6812 | Q2 | 1 |
| 1978 | IEEE Communications Standards Magazine | 2471-2825 | Q1 | 1 |
| 1979 | IEEE Computer Architecture Letters | 1556-6056 | Q2 | 1 |
| 1980 | IEEE Electrification Magazine | 2325-5889 | Q2 | 1 |
| 1981 | IEEE Geoscience and Remote Sensing Magazine | 2168-6831 | Q1 | 1 |
| 1982 | IEEE Industry Applications Magazine | 1077-2618 | Q3 | 1 |
| 1983 | IEEE Journal of Electromagnetics RF and Microwaves in Medicine and Biology | 2469-7249 | Q1 | 1 |
| 1984 | IEEE Journal of Oceanic Engineering | 0364-9059 | Q1 | 1 |
| 1985 | IEEE Journal of Photovoltaics | 2156-3381 | Q1 | 1 |
| 1986 | IEEE Journal of Selected Topics in Signal Processing | 1932-4553 | Q1 | 1 |
| 1987 | IEEE Journal of Translational Engineering in Health and Medicine | 2168-2372 | Q1 | 1 |
| 1988 | IEEE Magnetics Letters | 1949-307X | Q3 | 1 |
| 1989 | IEEE Microwave Magazine | 1527-3342 | Q2 | 1 |
| 1990 | IEEE Microwave and Wireless Technology Letters | 2771-957X | Q1 | 1 |
| 1991 | IEEE Multimedia | 1070-986X | Q1 | 1 |
| 1992 | IEEE Open Journal of Nanotechnology | 2644-1292 | Q2 | 1 |
| 1993 | IEEE Open Journal of Vehicular Technology | 2644-1330 | Q1 | 1 |
| 1994 | IEEE Potentials | 0278-6648 | Q3 | 1 |
| 1995 | IEEE Transactions on AgriFood Electronics | 2771-9529 | — | 1 |
| 1996 | IEEE Transactions on Big Data | 2332-7790 | Q1 | 1 |
| 1997 | IEEE Transactions on Electromagnetic Compatibility | 0018-9375 | Q1 | 1 |
| 1998 | IEEE Transactions on Machine Learning in Communications and Networking | 2831-316X | Q1 | 1 |
| 1999 | IEEE Transactions on Microwave Theory and Techniques | 0018-9480 | Q1 | 1 |
| 2000 | IEEE Transactions on Pattern Analysis and Machine Intelligence | 0162-8828 | Q1 | 1 |
| 2001 | IEEE Transactions on Reliability | 0018-9529 | Q1 | 1 |
| 2002 | IEEE Transactions on Signal and Information Processing over Networks | 2373-776X | Q1 | 1 |
| 2003 | IEEE Transactions on Systems Man and Cybernetics Systems | 2168-2216 | Q1 | 1 |
| 2004 | IEEE Wireless Communications | 1536-1284 | Q1 | 1 |
| 2005 | IEEE data descriptions. | 2995-4274 | — | 1 |
| 2006 | IEEE/ACM Transactions on Audio Speech and Language Processing | 2329-9290 | Q1 | 1 |
| 2007 | IEEE/ACM Transactions on Networking | 1063-6692 | — | 1 |
| 2008 | IEEJ Transactions on Fundamentals and Materials | 0385-4205 | Q4 | 1 |
| 2009 | IET Computer Vision | 1751-9632 | Q2 | 1 |
| 2010 | IET Intelligent Transport Systems | 1751-956X | Q1 | 1 |
| 2011 | IET Microwaves Antennas & Propagation | 1751-8725 | Q3 | 1 |
| 2012 | IET Nanobiotechnology | 1751-8741 | Q1 | 1 |
| 2013 | IMA Journal of Applied Mathematics | 0272-4960 | Q2 | 1 |
| 2014 | INFORMS journal on computing | 0899-1499 | Q1 | 1 |
| 2015 | IOP SciNotes | 2633-1357 | — | 1 |
| 2016 | ISH Journal of Hydraulic Engineering | 0971-5010 | Q3 | 1 |
| 2017 | ISSS Journal of Micro and Smart Systems | 2509-7989 | — | 1 |
| 2018 | ITU Journal on Future and Evolving Technologies | 2616-8375 | — | 1 |
| 2019 | IUBMB Life | 1521-6543 | Q1 | 1 |
| 2020 | ImmunoInformatics | 2667-1190 | — | 1 |
| 2021 | In Silico Pharmacology | 2193-9616 | — | 1 |
| 2022 | Indagationes Mathematicae | 0019-3577 | Q2 | 1 |
| 2023 | Indian Heart Journal | 0019-4832 | Q2 | 1 |
| 2024 | Indian Journal of Labour Economics | 0019-5308 | Q3 | 1 |
| 2025 | Indian Journal of Microbiology | 0046-8991 | Q3 | 1 |
| 2026 | Indian Journal of Orthopaedics | 0019-5413 | Q3 | 1 |
| 2027 | Indian Journal of Pharmacology | 0253-7613 | Q3 | 1 |
| 2028 | Indian Journal of Poultry Science | 0019-5529 | — | 1 |
| 2029 | Indian Science Cruiser | 0970-4256 | — | 1 |
| 2030 | Industrial and Corporate Change | 0960-6491 | Q1 | 1 |
| 2031 | Infection Disease & Health | 2468-0451 | Q3 | 1 |
| 2032 | Informatica | 0350-5596 | Q3 | 1 |
| 2033 | Information Systems | 0306-4379 | Q1 | 1 |
| 2034 | Information Technology & Tourism | 1098-3058 | Q1 | 1 |
| 2035 | Information and Software Technology | 0950-5849 | Q1 | 1 |
| 2036 | Infrastructure Asset Management | 2053-0242 | Q3 | 1 |
| 2037 | Inhalation Toxicology | 0895-8378 | Q3 | 1 |
| 2038 | Innovation and Development | 2157-930X | Q1 | 1 |
| 2039 | Innovations in Systems and Software Engineering | 1614-5046 | Q3 | 1 |
| 2040 | Instrumentation Science & Technology | 1073-9149 | Q3 | 1 |
| 2041 | Integrated Environmental Assessment and Management | 1551-3777 | Q1 | 1 |
| 2042 | Integrative Biology | 1757-9694 | Q3 | 1 |
| 2043 | Intelligent Service Robotics | 1861-2776 | Q1 | 1 |
| 2044 | Intelligent Systems |  | — | 1 |
| 2045 | Interdisciplinary Sciences Computational Life Sciences | 1867-1462 | Q2 | 1 |
| 2046 | Interdisciplinary cancer research | 2731-4561 | — | 1 |
| 2047 | International Dairy Journal | 0958-6946 | Q2 | 1 |
| 2048 | International Economics and Economic Policy | 1612-4804 | Q3 | 1 |
| 2049 | International Environmental Agreements Politics Law and Economics | 1567-9764 | Q1 | 1 |
| 2050 | International Health | 1876-3405 | Q1 | 1 |
| 2051 | International Journal For Multidisciplinary Research | 2582-2160 | — | 1 |
| 2052 | International Journal for Multiscale Computational Engineering | 1543-1649 | Q2 | 1 |
| 2053 | International Journal for Numerical Methods in Biomedical Engineering | 2040-7939 | Q2 | 1 |
| 2054 | International Journal for Numerical Methods in Fluids | 0271-2091 | Q2 | 1 |
| 2055 | International Journal for Research in Applied Science and Engineering Technology | 2321-9653 | — | 1 |
| 2056 | International Journal for the Semiotics of Law - Revue internationale de Sémiotique juridique | 0952-8059 | Q2 | 1 |
| 2057 | International Journal of Adolescence and Youth | 0267-3843 | Q1 | 1 |
| 2058 | International Journal of Advanced Research | 2320-5407 | — | 1 |
| 2059 | International Journal of Agricultural Resources Governance and Ecology | 1462-4605 | Q4 | 1 |
| 2060 | International Journal of Applied Earth Observation and Geoinformation | 0303-2434 | Q1 | 1 |
| 2061 | International Journal of Applied Information Systems | 2249-085X | — | 1 |
| 2062 | International Journal of Applied Metaheuristic Computing | 1947-8283 | Q4 | 1 |
| 2063 | International Journal of Biomedical and Clinical Engineering | 2161-1610 | — | 1 |
| 2064 | International Journal of Cancer | 0020-7136 | Q1 | 1 |
| 2065 | International Journal of Ceramic Engineering & Science | 2578-3270 | Q3 | 1 |
| 2066 | International Journal of Chemical Kinetics | 0538-8066 | Q3 | 1 |
| 2067 | International Journal of Computational Intelligence Systems | 1875-6883 | Q1 | 1 |
| 2068 | International Journal of Computer Aided Engineering and Technology | 1757-2657 | Q4 | 1 |
| 2069 | International Journal of Computer Applications | 0975-8887 | — | 1 |
| 2070 | International Journal of Computers Communications & Control | 1841-9836 | Q2 | 1 |
| 2071 | International Journal of Corporate Strategy and Social Responsibility | 2054-8087 | — | 1 |
| 2072 | International Journal of Crashworthiness | 1358-8265 | Q2 | 1 |
| 2073 | International Journal of Data Science and Analytics | 2364-415X | Q1 | 1 |
| 2074 | International Journal of Development Issues | 1446-8956 | Q2 | 1 |
| 2075 | International Journal of Digital Earth | 1753-8947 | Q1 | 1 |
| 2076 | International Journal of Dynamics and Control | 2195-268X | Q2 | 1 |
| 2077 | International Journal of Electrical Engineering Education | 0020-7209 | Q3 | 1 |
| 2078 | International Journal of Emerging Markets | 1746-8809 | Q1 | 1 |
| 2079 | International Journal of Empirical Economics | 2810-9430 | Q3 | 1 |
| 2080 | International Journal of Engineering & Technology | 2227-524X | — | 1 |
| 2081 | International Journal of Environmental Research and Public Health | 1660-4601 | Q1 | 1 |
| 2082 | International Journal of Fatigue | 0142-1123 | Q1 | 1 |
| 2083 | International Journal of Finance & Economics | 1076-9307 | Q2 | 1 |
| 2084 | International Journal of Food Science & Technology | 0950-5423 | Q1 | 1 |
| 2085 | International Journal of Food Technology and Management | 3139-4655 | — | 1 |
| 2086 | International Journal of Fuzzy Systems | 1562-2479 | Q2 | 1 |
| 2087 | International Journal of Genomics | 2314-436X | Q2 | 1 |
| 2088 | International Journal of Geo-Engineering | 2092-9196 | Q1 | 1 |
| 2089 | International Journal of Geoheritage and Parks | 2577-4441 | Q1 | 1 |
| 2090 | International Journal of Health Geographics | 1476-072X | Q1 | 1 |
| 2091 | International Journal of Human-Computer Interaction | 1044-7318 | Q1 | 1 |
| 2092 | International Journal of Industrial and Systems Engineering | 1748-5037 | Q3 | 1 |
| 2093 | International Journal of Information Security | 1615-5262 | Q1 | 1 |
| 2094 | International Journal of Innovation Management | 1363-9196 | Q3 | 1 |
| 2095 | International Journal of Innovation and Technology Management | 0219-8770 | Q3 | 1 |
| 2096 | International Journal of Intellectual Property Management | 1478-9647 | Q3 | 1 |
| 2097 | International Journal of Intelligent Robotics and Applications | 2366-5971 | Q2 | 1 |
| 2098 | International Journal of Intelligent Systems | 0884-8173 | Q1 | 1 |
| 2099 | International Journal of Lightweight Materials and Manufacture | 2588-8404 | Q1 | 1 |
| 2100 | International Journal of Machining and Machinability of Materials | 1748-5711 | Q3 | 1 |
| 2101 | International Journal of Manufacturing Materials and Mechanical Engineering | 2156-1672 | Q3 | 1 |
| 2102 | International Journal of Manufacturing Research | 1750-0591 | Q3 | 1 |
| 2103 | International Journal of Manufacturing Technology and Management | 1368-2148 | Q4 | 1 |
| 2104 | International Journal of Mathematical Engineering and Management Sciences | 2455-7749 | Q2 | 1 |
| 2105 | International Journal of Mathematical Modelling and Numerical Optimisation | 2040-3607 | Q3 | 1 |
| 2106 | International Journal of Mechatronics and Automation | 2045-1059 | Q4 | 1 |
| 2107 | International Journal of Metalcasting | 1939-5981 | Q2 | 1 |
| 2108 | International Journal of Metallurgical & Materials Engineering | 2455-2372 | — | 1 |
| 2109 | International Journal of Minerals Metallurgy and Materials | 1005-8850 | Q1 | 1 |
| 2110 | International Journal of Modern Physics A | 0217-751X | Q3 | 1 |
| 2111 | International Journal of Nanomedicine | 1176-9114 | Q1 | 1 |
| 2112 | International Journal of Neural Systems | 0129-0657 | Q1 | 1 |
| 2113 | International Journal of Neurooncology | 2590-2652 | — | 1 |
| 2114 | International Journal of Operational Research | 1745-7645 | Q4 | 1 |
| 2115 | International Journal of Polymer Analysis and Characterization | 1023-666X | Q3 | 1 |
| 2116 | International Journal of Power Electronics and Drive Systems/International Journal of Electrical and Computer Engineering | 2722-256X | — | 1 |
| 2117 | International Journal of Power and Energy Systems | 1078-3466 | Q4 | 1 |
| 2118 | International Journal of Production Research | 0020-7543 | Q1 | 1 |
| 2119 | International Journal of Rural Management | 0973-0052 | Q3 | 1 |
| 2120 | International Journal of Satellite Communications and Networking | 1542-0973 | Q2 | 1 |
| 2121 | International Journal of Sensors Wireless Communications and Control | 2210-3279 | Q3 | 1 |
| 2122 | International Journal of Smart and Nano Materials | 1947-5411 | Q1 | 1 |
| 2123 | International Journal of Social Economics | 0306-8293 | Q2 | 1 |
| 2124 | International Journal of Social and Humanistic Computing | 1752-6124 | — | 1 |
| 2125 | International Journal of Spectroscopy | 1687-9449 | — | 1 |
| 2126 | International Journal of Speech Technology | 1381-2416 | Q1 | 1 |
| 2127 | International Journal of Structural Engineering | 1758-7328 | Q4 | 1 |
| 2128 | International Journal of Sustainable Economy | 1756-5804 | Q3 | 1 |
| 2129 | International Journal of Swarm Intelligence | 2049-4041 | — | 1 |
| 2130 | International Journal of Swarm Intelligence Research | 1947-9263 | Q3 | 1 |
| 2131 | International Journal of Tourism Policy | 1750-4090 | Q4 | 1 |
| 2132 | International Journal of Value Chain Management | 1741-5357 | Q4 | 1 |
| 2133 | International Journal of Water Resources Development | 0790-0627 | Q2 | 1 |
| 2134 | International Journal on Electrical Engineering and Informatics | 2085-6830 | Q4 | 1 |
| 2135 | International Journal on Semantic Web and Information Systems | 1552-6283 | Q2 | 1 |
| 2136 | International Journal on Smart Sensing and Intelligent Systems | 1178-5608 | Q3 | 1 |
| 2137 | International Journal on Software Tools for Technology Transfer | 1433-2779 | Q2 | 1 |
| 2138 | International Materials Reviews | 0950-6608 | Q1 | 1 |
| 2139 | International Review of Applied Economics | 0269-2171 | Q2 | 1 |
| 2140 | International Review of Mechanical Engineering (IREME) | 1970-8734 | Q3 | 1 |
| 2141 | International Soil and Water Conservation Research | 2095-6339 | Q1 | 1 |
| 2142 | International journal of Web & Semantic Technology | 0975-9026 | — | 1 |
| 2143 | International journal of industrial engineering | 1072-4761 | Q3 | 1 |
| 2144 | International journal of mechanical system dynamics | 2767-1399 | Q1 | 1 |
| 2145 | Internet of Things | 2542-6605 | Q1 | 1 |
| 2146 | Inverse Problems and Imaging | 1930-8337 | Q2 | 1 |
| 2147 | Iran Journal of Computer Science | 2520-8438 | Q2 | 1 |
| 2148 | Iranian Journal of Science | 2731-8095 | Q2 | 1 |
| 2149 | JACC Asia | 2772-3747 | Q1 | 1 |
| 2150 | Jahrbücher für Nationalökonomie und Statistik | 0021-4027 | Q1 | 1 |
| 2151 | Japanese Geotechnical Society Special Publication | 2188-8027 | — | 1 |
| 2152 | Jordan Journal of Agricultural Sciences | 1815-8625 | — | 1 |
| 2153 | Journal for Labour Market Research | 1614-3485 | Q2 | 1 |
| 2154 | Journal for Manufacturing Science and Production | 0793-6648 | — | 1 |
| 2155 | Journal for Nature Conservation | 1617-1381 | Q1 | 1 |
| 2156 | Journal for ReAttach Therapy and Developmental Diversities | 2589-7799 | — | 1 |
| 2157 | Journal of Advanced Research | 2090-1224 | Q1 | 1 |
| 2158 | Journal of Advances in Management Research | 0972-7981 | Q2 | 1 |
| 2159 | Journal of Advances in Modeling Earth Systems | 1942-2466 | Q1 | 1 |
| 2160 | Journal of Aerosol Science | 0021-8502 | Q1 | 1 |
| 2161 | Journal of Agrometeorology | 0972-1665 | Q2 | 1 |
| 2162 | Journal of Aircraft | 0021-8669 | Q2 | 1 |
| 2163 | Journal of Allergy and Clinical Immunology | 0091-6749 | Q1 | 1 |
| 2164 | Journal of Analytical and Applied Pyrolysis | 0165-2370 | Q1 | 1 |
| 2165 | Journal of Antimicrobial Chemotherapy | 0305-7453 | Q1 | 1 |
| 2166 | Journal of Applied Electrochemistry | 0021-891X | Q2 | 1 |
| 2167 | Journal of Applied Geophysics | 0926-9851 | Q2 | 1 |
| 2168 | Journal of Applied Mathematics and Computing | 1226-0061 | Q2 | 1 |
| 2169 | Journal of Arid Environments | 0140-1963 | Q1 | 1 |
| 2170 | Journal of Arid Land | 1674-6767 | Q1 | 1 |
| 2171 | Journal of Asia-Pacific Business | 1059-9231 | Q3 | 1 |
| 2172 | Journal of Asian Ceramic Societies | 2187-0764 | Q3 | 1 |
| 2173 | Journal of Asian Concrete Federation | 2465-7964 | — | 1 |
| 2174 | Journal of Asian Earth Sciences X | 2590-0560 | Q2 | 1 |
| 2175 | Journal of Asian Public Policy | 1751-6234 | Q2 | 1 |
| 2176 | Journal of Atmospheric Electricity | 0919-2050 | — | 1 |
| 2177 | Journal of Bacteriology | 0021-9193 | Q1 | 1 |
| 2178 | Journal of Banking and Financial Technology | 2524-7956 | — | 1 |
| 2179 | Journal of Basic Microbiology | 0233-111X | Q2 | 1 |
| 2180 | Journal of Bioeconomics | 1387-6996 | Q3 | 1 |
| 2181 | Journal of Biological Systems | 0218-3390 | Q2 | 1 |
| 2182 | Journal of Biomechanics | 0021-9290 | Q1 | 1 |
| 2183 | Journal of Biomedical Optics | 1083-3668 | Q2 | 1 |
| 2184 | Journal of Biosciences | 0250-5991 | Q2 | 1 |
| 2185 | Journal of Biotechnology | 0168-1656 | Q2 | 1 |
| 2186 | Journal of Building Performance Simulation | 1940-1493 | Q1 | 1 |
| 2187 | Journal of Cardiovascular Development and Disease | 2308-3425 | Q1 | 1 |
| 2188 | Journal of Cell Communication and Signaling | 1873-9601 | Q1 | 1 |
| 2189 | Journal of Cellular Physiology | 0021-9541 | Q1 | 1 |
| 2190 | Journal of Chemical Technology & Biotechnology | 0142-0356 | Q2 | 1 |
| 2191 | Journal of Chemical Theory and Computation | 1549-9618 | Q1 | 1 |
| 2192 | Journal of Clinical Medicine | 2077-0383 | Q2 | 1 |
| 2193 | Journal of Clinical Microbiology | 0095-1137 | Q1 | 1 |
| 2194 | Journal of Clinical Orthopaedics and Trauma | 0976-5662 | Q3 | 1 |
| 2195 | Journal of Coastal Research | 0749-0208 | — | 1 |
| 2196 | Journal of Combinatorial Optimization | 1382-6905 | Q3 | 1 |
| 2197 | Journal of Communications and Information Networks | 2096-1081 | Q1 | 1 |
| 2198 | Journal of Composites Science | 2504-477X | Q1 | 1 |
| 2199 | Journal of Computational and Nonlinear Dynamics | 1555-1415 | Q2 | 1 |
| 2200 | Journal of Computational and Theoretical Nanoscience | 1546-1955 | — | 1 |
| 2201 | Journal of Computational and Theoretical Transport | 2332-4309 | Q4 | 1 |
| 2202 | Journal of Computer Virology and Hacking Techniques | 1772-9890 | Q2 | 1 |
| 2203 | Journal of Computer-Aided Molecular Design | 0920-654X | Q2 | 1 |
| 2204 | Journal of Condensed Matter | 2583-9152 | — | 1 |
| 2205 | Journal of Construction Engineering and Management | 0733-9364 | Q1 | 1 |
| 2206 | Journal of Constructional Steel Research | 0143-974X | Q1 | 1 |
| 2207 | Journal of Contaminant Hydrology | 0169-7722 | Q1 | 1 |
| 2208 | Journal of Contemporary Mathematical Analysis (Armenian Academy of Sciences) | 1068-3623 | Q3 | 1 |
| 2209 | Journal of Creative Communications | 0973-2586 | Q2 | 1 |
| 2210 | Journal of Cultural Heritage | 1296-2074 | Q1 | 1 |
| 2211 | Journal of Dharma Studies | 2522-0926 | Q2 | 1 |
| 2212 | Journal of Digital Media & Policy | 2516-3523 | Q2 | 1 |
| 2213 | Journal of Dynamic Systems Measurement and Control | 0022-0434 | Q2 | 1 |
| 2214 | Journal of Dynamical and Control Systems | 1079-2724 | Q2 | 1 |
| 2215 | Journal of Dynamics Monitoring and Diagnostics | 2831-5308 | Q1 | 1 |
| 2216 | Journal of Economic Structures | 2193-2409 | Q2 | 1 |
| 2217 | Journal of Economic Studies | 0144-3585 | Q1 | 1 |
| 2218 | Journal of Economics Business and Management | 2301-3567 | — | 1 |
| 2219 | Journal of Economics and Business | 0148-6195 | Q1 | 1 |
| 2220 | Journal of Elasticity | 0374-3535 | Q2 | 1 |
| 2221 | Journal of Electrical Engineering and Technology | 1975-0102 | Q2 | 1 |
| 2222 | Journal of Electrochemical Science and Engineering | 1847-9286 | Q3 | 1 |
| 2223 | Journal of Energy Chemistry | 2095-4956 | Q1 | 1 |
| 2224 | Journal of Energy Resources Technology | 0195-0738 | Q2 | 1 |
| 2225 | Journal of Engineering Mathematics | 0022-0833 | Q2 | 1 |
| 2226 | Journal of Engineering Mechanics | 0733-9399 | Q1 | 1 |
| 2227 | Journal of Engineering Thermophysics | 1810-2328 | Q3 | 1 |
| 2228 | Journal of Engineering for Gas Turbines and Power | 0742-4795 | Q2 | 1 |
| 2229 | Journal of Environmental Engineering and Landscape Management | 1648-6897 | Q3 | 1 |
| 2230 | Journal of Environmental Planning and Management | 0964-0568 | Q1 | 1 |
| 2231 | Journal of Environmental Science and Health Part B | 0360-1234 | Q2 | 1 |
| 2232 | Journal of Exclusion Studies | 2231-4547 | — | 1 |
| 2233 | Journal of Experimental Botany | 0022-0957 | Q1 | 1 |
| 2234 | Journal of Experimental and Theoretical Physics | 0038-5646 | Q4 | 1 |
| 2235 | Journal of Extracellular Vesicles | 2001-3078 | Q1 | 1 |
| 2236 | Journal of Field Robotics | 1556-4959 | Q1 | 1 |
| 2237 | Journal of Financial Economic Policy | 1757-6385 | Q2 | 1 |
| 2238 | Journal of Fixed Point Theory and Applications | 1661-7738 | Q2 | 1 |
| 2239 | Journal of Fluid Mechanics | 0022-1120 | Q1 | 1 |
| 2240 | Journal of Fluids Engineering | 0098-2202 | Q2 | 1 |
| 2241 | Journal of Fluids and Structures | 0889-9746 | Q1 | 1 |
| 2242 | Journal of Food Composition and Analysis | 0889-1575 | Q1 | 1 |
| 2243 | Journal of Food Quality | 0146-9428 | Q2 | 1 |
| 2244 | Journal of Food Science | 0022-1147 | Q1 | 1 |
| 2245 | Journal of Geochemical Exploration | 0375-6742 | Q1 | 1 |
| 2246 | Journal of Geometric Analysis | 1050-6926 | Q1 | 1 |
| 2247 | Journal of Geophysical Research Earth Surface | 2169-9003 | Q1 | 1 |
| 2248 | Journal of Geophysical Research Machine Learning and Computation | 2993-5210 | Q1 | 1 |
| 2249 | Journal of Geophysical Research Planets | 2169-9097 | Q1 | 1 |
| 2250 | Journal of Global Agriculture and Ecology | 2454-4205 | — | 1 |
| 2251 | Journal of Global Economics Management and Business Research | 2454-2504 | — | 1 |
| 2252 | Journal of Health and Pollution | 2156-9614 | Q4 | 1 |
| 2253 | Journal of High Speed Networks | 0926-6801 | Q3 | 1 |
| 2254 | Journal of Human Development and Capabilities | 1945-2829 | Q1 | 1 |
| 2255 | Journal of Hydro-environment Research | 1570-6443 | Q2 | 1 |
| 2256 | Journal of Imaging Informatics in Medicine | 0897-1889 | Q1 | 1 |
| 2257 | Journal of Industrial Textiles | 0093-4658 | Q2 | 1 |
| 2258 | Journal of Industrial and Business Economics | 0391-2078 | Q1 | 1 |
| 2259 | Journal of Infection and Public Health | 1876-0341 | Q1 | 1 |
| 2260 | Journal of Infrastructure Systems | 1076-0342 | Q2 | 1 |
| 2261 | Journal of Innovations and Sustainability | 2367-8127 | — | 1 |
| 2262 | Journal of Integrative Plant Biology | 0577-7496 | Q1 | 1 |
| 2263 | Journal of Intelligent & Fuzzy Systems | 1064-1246 | Q3 | 1 |
| 2264 | Journal of Intelligent Systems | 0334-1860 | Q2 | 1 |
| 2265 | Journal of Ionic Liquids | 2772-4220 | Q2 | 1 |
| 2266 | Journal of Irrigation and Drainage Engineering | 0733-9437 | Q2 | 1 |
| 2267 | Journal of King Saud University - Computer and Information Sciences | 1319-1578 | Q1 | 1 |
| 2268 | Journal of Language Identity & Education | 1532-7701 | Q1 | 1 |
| 2269 | Journal of Legal Affairs and Dispute Resolution in Engineering and Construction | 1943-4162 | Q2 | 1 |
| 2270 | Journal of Liquid Chromatography & Related Technologies | 1082-6076 | Q3 | 1 |
| 2271 | Journal of Loss Prevention in the Process Industries | 0950-4230 | Q1 | 1 |
| 2272 | Journal of Low Power Electronics and Applications | 2079-9268 | Q3 | 1 |
| 2273 | Journal of Manufacturing and Materials Processing | 2504-4494 | Q1 | 1 |
| 2274 | Journal of Marketing Communications | 1352-7266 | Q1 | 1 |
| 2275 | Journal of Materials Science Materials in Energy | 2948-2151 | — | 1 |
| 2276 | Journal of Materials Science Materials in Engineering | 3004-8958 | Q2 | 1 |
| 2277 | Journal of Materials Science Materials in Medicine | 0957-4530 | Q2 | 1 |
| 2278 | Journal of Materiomics | 2352-8478 | Q1 | 1 |
| 2279 | Journal of Mathematical Physics | 0022-2488 | Q2 | 1 |
| 2280 | Journal of Mathematical Sociology | 0022-250X | Q2 | 1 |
| 2281 | Journal of Medical Engineering & Technology | 0309-1902 | Q3 | 1 |
| 2282 | Journal of Medical Virology | 0146-6615 | Q1 | 1 |
| 2283 | Journal of Medical and Biological Engineering | 1609-0985 | Q3 | 1 |
| 2284 | Journal of Medicinal Chemistry | 0022-2623 | Q1 | 1 |
| 2285 | Journal of Membrane Science | 0376-7388 | Q1 | 1 |
| 2286 | Journal of Micro/Nanopatterning Materials and Metrology | 2708-8340 | Q2 | 1 |
| 2287 | Journal of Microbiological Methods | 0167-7012 | Q3 | 1 |
| 2288 | Journal of Microbiology Biotechnology and Food Sciences | 1338-5178 | Q3 | 1 |
| 2289 | Journal of Modern Applied Statistical Methods | 1538-9472 | — | 1 |
| 2290 | Journal of Molecular Biology | 0022-2836 | Q1 | 1 |
| 2291 | Journal of Molecular Catalysis A Chemical | 1381-1169 | — | 1 |
| 2292 | Journal of Molecular Modeling | 0948-5023 | Q2 | 1 |
| 2293 | Journal of Molecular and Engineering Materials | 2251-2373 | — | 1 |
| 2294 | Journal of Nanobiotechnology | 1477-3155 | Q1 | 1 |
| 2295 | Journal of Nanofluids | 2169-432X | — | 1 |
| 2296 | Journal of Nanophotonics | 1934-2608 | Q4 | 1 |
| 2297 | Journal of Nanotechnology | 1687-9503 | Q2 | 1 |
| 2298 | Journal of Neural Engineering | 1741-2552 | Q1 | 1 |
| 2299 | Journal of Neurochemistry | 0022-3042 | Q1 | 1 |
| 2300 | Journal of Neuroimmunology | 0165-5728 | Q2 | 1 |
| 2301 | Journal of Non-Destructive Testing & Evaluation (JNDE) | 0973-9610 | — | 1 |
| 2302 | Journal of Nondestructive Evaluation | 0195-9298 | Q2 | 1 |
| 2303 | Journal of Nondestructive Evaluation Diagnostics and Prognostics of Engineering Systems | 2572-3898 | Q2 | 1 |
| 2304 | Journal of Nuclear Materials | 0022-3115 | Q1 | 1 |
| 2305 | Journal of Offshore Mechanics and Arctic Engineering | 0892-7219 | Q2 | 1 |
| 2306 | Journal of Oncology | 1687-8450 | — | 1 |
| 2307 | Journal of Operational Oceanography | 1755-876X | Q2 | 1 |
| 2308 | Journal of Optics and Photonics Research | 3029-1348 | — | 1 |
| 2309 | Journal of Oral Biology and Craniofacial Research | 2212-4268 | Q2 | 1 |
| 2310 | Journal of Organizational and End User Computing | 1546-2234 | Q2 | 1 |
| 2311 | Journal of Pathology Informatics | 2153-3539 | Q1 | 1 |
| 2312 | Journal of Pharmaceutical Innovation | 1872-5120 | Q3 | 1 |
| 2313 | Journal of Pharmaceutical Research International | 2231-2919 | — | 1 |
| 2314 | Journal of Pharmaceutical Sciences | 0022-3549 | Q2 | 1 |
| 2315 | Journal of Photochemistry and Photobiology C Photochemistry Reviews | 1389-5567 | Q1 | 1 |
| 2316 | Journal of Photonics for Energy | 1947-7988 | Q3 | 1 |
| 2317 | Journal of Photopolymer Science and Technology | 0914-9244 | Q3 | 1 |
| 2318 | Journal of Physics A Mathematical and Theoretical | 1751-8113 | Q2 | 1 |
| 2319 | Journal of Physics Complexity | 2632-072X | Q2 | 1 |
| 2320 | Journal of Physics Energy | 2515-7655 | Q1 | 1 |
| 2321 | Journal of Physics Photonics | 2515-7647 | Q1 | 1 |
| 2322 | Journal of Polymer Science | 2642-4150 | Q1 | 1 |
| 2323 | Journal of Polymers and the Environment | 1064-7546 | Q1 | 1 |
| 2324 | Journal of Population Research | 1443-2447 | Q2 | 1 |
| 2325 | Journal of Porous Materials | 1380-2224 | Q2 | 1 |
| 2326 | Journal of Posthumanism | 2634-3576 | — | 1 |
| 2327 | Journal of Proteome Research | 1535-3893 | Q1 | 1 |
| 2328 | Journal of Quality Assurance in Hospitality & Tourism | 1528-008X | Q2 | 1 |
| 2329 | Journal of Quality in Maintenance Engineering | 1355-2511 | Q2 | 1 |
| 2330 | Journal of Radioanalytical and Nuclear Chemistry | 0236-5731 | Q3 | 1 |
| 2331 | Journal of Real Estate Construction & Management | 2977-6570 | — | 1 |
| 2332 | Journal of Regulatory Economics | 0922-680X | Q3 | 1 |
| 2333 | Journal of Reliable Intelligent Environments | 2199-4668 | Q1 | 1 |
| 2334 | Journal of Renewable and Sustainable Energy | 1941-7012 | Q3 | 1 |
| 2335 | Journal of Research in Engineering and Applied Sciences | 2456-6403 | — | 1 |
| 2336 | Journal of Revenue and Pricing Management | 1476-6930 | Q3 | 1 |
| 2337 | Journal of Road Engineering | 2097-0498 | Q1 | 1 |
| 2338 | Journal of Seismology | 1383-4649 | Q2 | 1 |
| 2339 | Journal of Ship Production and Design | 2158-2866 | Q3 | 1 |
| 2340 | Journal of Signal Processing Systems | 1939-8018 | Q2 | 1 |
| 2341 | Journal of Soils and Sediments | 1439-0108 | Q1 | 1 |
| 2342 | Journal of Sol-Gel Science and Technology | 0928-0707 | Q2 | 1 |
| 2343 | Journal of Spacecraft and Rockets | 0022-4650 | Q1 | 1 |
| 2344 | Journal of Sports Economics & Management |  | — | 1 |
| 2345 | Journal of Structural Integrity and Maintenance | 2470-5314 | Q1 | 1 |
| 2346 | Journal of Sustainable Forestry | 1054-9811 | Q2 | 1 |
| 2347 | Journal of Systems Science and Complexity | 1009-6124 | Q2 | 1 |
| 2348 | Journal of The Institution of Engineers (India) Series A | 2250-2149 | Q2 | 1 |
| 2349 | Journal of The Institution of Engineers (India) Series B | 2250-2106 | Q3 | 1 |
| 2350 | Journal of The Institution of Engineers (India) Series D | 2250-2122 | Q2 | 1 |
| 2351 | Journal of Theoretical Biology | 0022-5193 | Q2 | 1 |
| 2352 | Journal of Theoretical and Computational Acoustics | 0218-396X | Q3 | 1 |
| 2353 | Journal of Thermal Stresses | 0149-5739 | Q3 | 1 |
| 2354 | Journal of Threatened Taxa | 0974-7893 | Q3 | 1 |
| 2355 | Journal of Transformative Technologies and Sustainable Development | 3059-3336 | Q4 | 1 |
| 2356 | Journal of Translational Gastroenterology | 2994-8754 | — | 1 |
| 2357 | Journal of Travel Medicine | 1195-1982 | Q1 | 1 |
| 2358 | Journal of Turbulence | 1468-5248 | Q2 | 1 |
| 2359 | Journal of Uncertainty Analysis and Applications | 2195-5468 | — | 1 |
| 2360 | Journal of Urban Health | 0028-7091 | Q1 | 1 |
| 2361 | Journal of Vinyl and Additive Technology | 1083-5601 | Q2 | 1 |
| 2362 | Journal of Virology | 0022-538X | Q1 | 1 |
| 2363 | Journal of Water Resources Planning and Management | 0733-9496 | Q1 | 1 |
| 2364 | Journal of Water Sanitation and Hygiene for Development | 2043-9083 | Q2 | 1 |
| 2365 | Journal of Welding and Joining | 1225-6153 | — | 1 |
| 2366 | Journal of Zhejiang University. Science A | 1009-3095 | Q1 | 1 |
| 2367 | Journal of energy resources technology. | 2997-0253 | Q2 | 1 |
| 2368 | Journal of intelligent systems in current computer engineering. | 3050-5070 | — | 1 |
| 2369 | Journal of mechanics of materials and structures | 1559-3959 | Q3 | 1 |
| 2370 | Journal of the Energy Institute | 0144-2600 | Q1 | 1 |
| 2371 | Journal of the Indian Society for Probability and Statistics | 2364-9569 | Q3 | 1 |
| 2372 | Journal of the Knowledge Economy | 1868-7865 | Q2 | 1 |
| 2373 | Journal of the Operational Research Society | 0160-5682 | Q1 | 1 |
| 2374 | Journal of vibration and acoustics | 0739-3717 | Q2 | 1 |
| 2375 | KSCE Journal of Civil Engineering | 1226-7988 | Q2 | 1 |
| 2376 | Korean Journal of Chemical Engineering | 0256-1115 | Q2 | 1 |
| 2377 | Labour & Industry a journal of the social and economic relations of work | 1030-1763 | Q2 | 1 |
| 2378 | Lakes & Reservoirs Science Policy and Management for Sustainable Use | 1320-5331 | Q3 | 1 |
| 2379 | Language Resources and Evaluation | 1574-020X | Q1 | 1 |
| 2380 | Laser Physics Letters | 1612-2011 | Q3 | 1 |
| 2381 | Lasers in Manufacturing and Materials Processing | 2196-7229 | Q2 | 1 |
| 2382 | Lasers in Medical Science | 0268-8921 | Q2 | 1 |
| 2383 | Letters in Spatial and Resource Sciences | 1864-4031 | Q2 | 1 |
| 2384 | Lobachevskii Journal of Mathematics | 1818-9962 | Q2 | 1 |
| 2385 | Machine Intelligence Research | 1476-8186 | Q1 | 1 |
| 2386 | Machine Learning Engineering | 3049-4761 | — | 1 |
| 2387 | Machine Learning with Applications | 2666-8270 | Q1 | 1 |
| 2388 | Macromolecular Materials and Engineering | 1438-7492 | Q1 | 1 |
| 2389 | Macromolecular Rapid Communications | 1022-1336 | Q1 | 1 |
| 2390 | Macromolecules | 0024-9297 | Q1 | 1 |
| 2391 | Magnetochemistry | 2312-7481 | Q2 | 1 |
| 2392 | Main Group Metal Chemistry | 0792-1241 | Q3 | 1 |
| 2393 | Malaysian Journal of Sustainable Agricultural | 2521-2931 | — | 1 |
| 2394 | Mammalian Genome | 0938-8990 | Q2 | 1 |
| 2395 | Marine Environmental Research | 0141-1136 | Q1 | 1 |
| 2396 | Marine Geodesy | 0149-0419 | Q2 | 1 |
| 2397 | Materiale Plastice | 0025-5289 | Q4 | 1 |
| 2398 | Materials Circular Economy | 2524-8146 | — | 1 |
| 2399 | Materials Open | 2811-0862 | — | 1 |
| 2400 | Materials Today Advances | 2590-0498 | Q1 | 1 |
| 2401 | Materials Today Bio | 2590-0064 | Q1 | 1 |
| 2402 | Materials at High Temperatures | 0960-3409 | Q2 | 1 |
| 2403 | Mathematica Moravica | 1450-5932 | — | 1 |
| 2404 | Mathematical Biosciences & Engineering | 1547-1063 | Q2 | 1 |
| 2405 | Mathematical Foundations of Computing | 2577-8838 | Q3 | 1 |
| 2406 | Mathematical Proceedings of the Cambridge Philosophical Society | 0305-0041 | Q1 | 1 |
| 2407 | Mathematical sciences | 2008-1359 | Q2 | 1 |
| 2408 | Mathematics Magazine | 0025-570X | Q4 | 1 |
| 2409 | Mathematics of Climate and Weather Forecasting | 2353-6438 | — | 1 |
| 2410 | Matrix Biology Plus | 2590-0285 | Q1 | 1 |
| 2411 | Matrix Science Medica | 2521-0424 | — | 1 |
| 2412 | Meccanica | 0025-6455 | Q2 | 1 |
| 2413 | Mechanical sciences | 2191-9151 | Q2 | 1 |
| 2414 | Mechanics of Time-Dependent Materials | 1385-2000 | Q2 | 1 |
| 2415 | Mechanisms of Ageing and Development | 0047-6374 | Q1 | 1 |
| 2416 | Media Industries | 2373-9037 | — | 1 |
| 2417 | Media International Australia | 1324-5325 | Q1 | 1 |
| 2418 | Medical Image Analysis | 1361-8415 | Q1 | 1 |
| 2419 | Medicinal Research Reviews | 0198-6325 | Q1 | 1 |
| 2420 | Medicine in Drug Discovery | 2590-0986 | Q1 | 1 |
| 2421 | Medicine in Omics | 2590-1249 | — | 1 |
| 2422 | Mental Health and Social Inclusion | 2042-8308 | Q2 | 1 |
| 2423 | Metabolic Brain Disease | 0885-7490 | Q2 | 1 |
| 2424 | Metallurgical Research & Technology | 2271-3646 | Q3 | 1 |
| 2425 | Methods and Applications in Fluorescence | 2050-6120 | Q2 | 1 |
| 2426 | MethodsX | 2215-0161 | Q1 | 1 |
| 2427 | Micro and Nanostructures | 2773-0123 | Q2 | 1 |
| 2428 | Microbiology Spectrum | 2165-0497 | Q1 | 1 |
| 2429 | Microbiology and Immunology | 0385-5600 | Q2 | 1 |
| 2430 | Microfluidics and Nanofluidics | 1613-4982 | Q3 | 1 |
| 2431 | Minerals Engineering | 0892-6875 | Q1 | 1 |
| 2432 | Mires and Peat | 1819-754X | Q2 | 1 |
| 2433 | Mitigation and Adaptation Strategies for Global Change | 1381-2386 | Q1 | 1 |
| 2434 | Mitochondrial DNA Part B | 2380-2359 | Q4 | 1 |
| 2435 | Mitochondrion | 1567-7249 | Q1 | 1 |
| 2436 | Modelling—International Open Access Journal of Modelling in Engineering Science | 2673-3951 | Q2 | 1 |
| 2437 | Molecular & Cellular Proteomics | 1535-9476 | Q1 | 1 |
| 2438 | Molecular BioSystems | 1742-2051 | — | 1 |
| 2439 | Molecular Biology of the Cell | 1059-1524 | Q2 | 1 |
| 2440 | Molecular Crystals and Liquid Crystals | 1542-1406 | Q4 | 1 |
| 2441 | Molecular Imaging | 1535-3508 | Q2 | 1 |
| 2442 | Molecular Nutrition & Food Research | 1613-4125 | Q1 | 1 |
| 2443 | Molecular Pharmaceutics | 1543-8384 | Q1 | 1 |
| 2444 | Molecular Physics | 0026-8976 | Q3 | 1 |
| 2445 | Molecular Simulation | 0892-7022 | Q3 | 1 |
| 2446 | Molecular and Cellular Biochemistry | 0300-8177 | Q1 | 1 |
| 2447 | Multiscale and Multidisciplinary Modeling Experiments and Design | 2520-8160 | Q3 | 1 |
| 2448 | Nano Communication Networks | 1878-7789 | Q2 | 1 |
| 2449 | Nano Futures | 2399-1984 | Q1 | 1 |
| 2450 | Nano Trends | 2666-9781 | Q1 | 1 |
| 2451 | Nanomaterials and Energy | 2045-9831 | Q4 | 1 |
| 2452 | Nanophotonics | 2192-8606 | Q1 | 1 |
| 2453 | Nanoscale Horizons | 2055-6756 | Q1 | 1 |
| 2454 | Nanoscale Research Letters | 1556-276X | Q2 | 1 |
| 2455 | Nanotechnology Reviews | 2191-9089 | Q1 | 1 |
| 2456 | National Academy Science Letters | 0250-541X | Q3 | 1 |
| 2457 | Natural Hazards Research | 2666-5921 | Q1 | 1 |
| 2458 | Natural Resource Modeling | 0890-8575 | Q3 | 1 |
| 2459 | Nature Cities | 2731-9997 | — | 1 |
| 2460 | Nature Materials | 1476-1122 | Q1 | 1 |
| 2461 | Nature Plants | 2055-026X | Q1 | 1 |
| 2462 | Nature Reviews Earth & Environment | 2662-138X | Q1 | 1 |
| 2463 | Nature and Science of Sleep | 1179-1608 | Q2 | 1 |
| 2464 | Naunyn-Schmiedeberg s Archives of Pharmacology | 0028-1298 | Q2 | 1 |
| 2465 | Nephrology Dialysis Transplantation | 0931-0509 | Q1 | 1 |
| 2466 | Network Modeling Analysis in Health Informatics and Bioinformatics | 2192-6670 | Q2 | 1 |
| 2467 | Network Science | 2050-1242 | Q2 | 1 |
| 2468 | Neural Processing Letters | 1370-4621 | Q2 | 1 |
| 2469 | Neurological Sciences | 1590-1874 | Q1 | 1 |
| 2470 | New Astronomy | 1384-1076 | Q2 | 1 |
| 2471 | New Generation Computing | 0288-3635 | Q2 | 1 |
| 2472 | New Environmentally-Friendly Materials | 2758-3163 | — | 1 |
| 2473 | Nonlinear processes in geophysics | 1023-5809 | Q1 | 1 |
| 2474 | Nonlinear science. | 3050-5178 | — | 1 |
| 2475 | Nonlinear studies | 1359-8678 | Q4 | 1 |
| 2476 | Nuclear Instruments and Methods in Physics Research Section B Beam Interactions with Materials and Atoms | 0168-583X | Q3 | 1 |
| 2477 | Numerical Heat Transfer Part B Fundamentals | 1040-7790 | Q2 | 1 |
| 2478 | Numerical Linear Algebra with Applications | 1070-5325 | Q1 | 1 |
| 2479 | Numerical Methods for Partial Differential Equations | 0749-159X | Q2 | 1 |
| 2480 | Nutrition and Health | 0260-1060 | Q3 | 1 |
| 2481 | Ocean Modelling | 1463-5003 | Q1 | 1 |
| 2482 | Ocean and Coastal Research | 1413-7739 | Q3 | 1 |
| 2483 | Oncoscience | 2331-4737 | — | 1 |
| 2484 | Oncotarget | 1949-2553 | Q2 | 1 |
| 2485 | Open Journal of Earthquake Research | 2169-9623 | — | 1 |
| 2486 | Open Journal of Medicinal Chemistry | 2164-3121 | — | 1 |
| 2487 | Open Journal of Modelling and Simulation | 2327-4018 | — | 1 |
| 2488 | Operations Management Research | 1936-9735 | Q1 | 1 |
| 2489 | Ophthalmology Glaucoma | 2589-4196 | Q1 | 1 |
| 2490 | Optimization | 0233-1934 | Q1 | 1 |
| 2491 | Ore Geology Reviews | 0169-1368 | Q1 | 1 |
| 2492 | Oriental Journal Of Chemistry | 0970-020X | — | 1 |
| 2493 | PAMM | 1617-7061 | — | 1 |
| 2494 | PLoS Biology | 1544-9173 | Q1 | 1 |
| 2495 | PLoS Computational Biology | 1553-734X | Q1 | 1 |
| 2496 | PLoS Genetics | 1553-7390 | Q1 | 1 |
| 2497 | PLoS neglected tropical diseases | 1935-2727 | Q1 | 1 |
| 2498 | PROTEOMICS | 1615-9853 | Q1 | 1 |
| 2499 | PRX Quantum | 2691-3399 | Q1 | 1 |
| 2500 | Paleoceanography and Paleoclimatology | 2572-4517 | Q1 | 1 |
| 2501 | Particle & Particle Systems Characterization | 0934-0866 | Q2 | 1 |
| 2502 | Pathology | 0031-3025 | Q1 | 1 |
| 2503 | Pathology - Research and Practice | 0344-0338 | — | 1 |
| 2504 | Pattern Recognition and Image Analysis | 1054-6618 | Q3 | 1 |
| 2505 | Permafrost and Periglacial Processes | 1045-6740 | Q1 | 1 |
| 2506 | Personal and Ubiquitous Computing | 1617-4909 | Q2 | 1 |
| 2507 | Pervasive and Mobile Computing | 1574-1192 | Q1 | 1 |
| 2508 | Photochemistry and Photobiology | 0031-8655 | Q1 | 1 |
| 2509 | Photonics Research | 2327-9125 | Q1 | 1 |
| 2510 | Photonics and Nanostructures - Fundamentals and Applications | 1569-4410 | Q2 | 1 |
| 2511 | Physical Biology | 1478-3967 | Q2 | 1 |
| 2512 | Physical Review Accelerators and Beams | 2469-9888 | Q1 | 1 |
| 2513 | Physical Review Fluids | 2469-990X | Q1 | 1 |
| 2514 | Physical and Engineering Sciences in Medicine | 2662-4729 | Q2 | 1 |
| 2515 | Physiological Reports | 2051-817X | Q2 | 1 |
| 2516 | Physiology and Molecular Biology of Plants | 0971-5894 | Q1 | 1 |
| 2517 | Phytomedicine | 0944-7113 | Q1 | 1 |
| 2518 | Phytotherapy Research | 0951-418X | Q1 | 1 |
| 2519 | Planetary and Space Science | 0032-0633 | Q2 | 1 |
| 2520 | Plant Biotechnology Journal | 1467-7644 | Q1 | 1 |
| 2521 | Plant Methods | 1746-4811 | Q1 | 1 |
| 2522 | Plant Signaling & Behavior | 1559-2316 | Q1 | 1 |
| 2523 | Plastics Rubber and Composites Macromolecular Engineering | 0959-8111 | Q3 | 1 |
| 2524 | Polymer Degradation and Stability | 0141-3910 | Q1 | 1 |
| 2525 | Polymer Engineering and Science | 0032-3888 | Q2 | 1 |
| 2526 | Polymer Testing | 0142-9418 | Q1 | 1 |
| 2527 | Polymer-Plastics Technology and Materials | 2574-0881 | Q2 | 1 |
| 2528 | Powder Metallurgy and Metal Ceramics | 1068-1302 | Q3 | 1 |
| 2529 | Power Electronics and Drives | 2451-0262 | Q3 | 1 |
| 2530 | Prayogik Rasayan | 2581-3323 | — | 1 |
| 2531 | Preventive Medicine Reports | 2211-3355 | Q1 | 1 |
| 2532 | Probabilistic Engineering Mechanics | 0266-8920 | Q1 | 1 |
| 2533 | Procedia Manufacturing | 2351-9789 | — | 1 |
| 2534 | Procedia Structural Integrity | 2452-3216 | — | 1 |
| 2535 | Proceedings - Mathematical Sciences | 0253-4142 | Q2 | 1 |
| 2536 | Proceedings of the Institution of Civil Engineers - Engineering Sustainability | 1478-4629 | Q2 | 1 |
| 2537 | Proceedings of the Institution of Civil Engineers - Geotechnical Engineering | 1353-2618 | Q2 | 1 |
| 2538 | Proceedings of the Institution of Civil Engineers - Transport | 0965-092X | Q3 | 1 |
| 2539 | Proceedings of the Institution of Mechanical Engineers Part D Journal of Automobile Engineering | 0954-4070 | Q2 | 1 |
| 2540 | Proceedings of the Institution of Mechanical Engineers Part I Journal of Systems and Control Engineering | 0959-6518 | Q3 | 1 |
| 2541 | Proceedings of the Institution of Mechanical Engineers Part N Journal of Nanomaterials Nanoengineering and Nanosystems | 2397-7914 | Q3 | 1 |
| 2542 | Proceedings of the Institution of Mechanical Engineers Part O Journal of Risk and Reliability | 1748-006X | Q2 | 1 |
| 2543 | Progress In Electromagnetics Research B | 1937-6472 | Q3 | 1 |
| 2544 | Progress In Electromagnetics Research C | 1937-8718 | Q3 | 1 |
| 2545 | Progress In Electromagnetics Research M | 1937-8726 | Q3 | 1 |
| 2546 | Progress in Composite Materials | 2982-2734 | — | 1 |
| 2547 | Progress in Computational Fluid Dynamics An International Journal | 1468-4349 | Q4 | 1 |
| 2548 | Progress in Disaster Science | 2590-0617 | Q1 | 1 |
| 2549 | Progress in Earth and Planetary Science | 2197-4284 | Q1 | 1 |
| 2550 | Progress in Energy | 2516-1083 | Q1 | 1 |
| 2551 | Progress in Nuclear Energy | 0149-1970 | Q1 | 1 |
| 2552 | Progress in Physical Geography Earth and Environment | 0309-1333 | Q1 | 1 |
| 2553 | Protection of Metals and Physical Chemistry of Surfaces | 2070-2051 | Q3 | 1 |
| 2554 | Protein and Peptide Letters | 0929-8665 | Q3 | 1 |
| 2555 | Proteomes | 2227-7382 | Q2 | 1 |
| 2556 | Public Health | 0033-3506 | Q1 | 1 |
| 2557 | Qualitative Market Research An International Journal | 1352-2752 | Q2 | 1 |
| 2558 | Quaternary Science Advances | 2666-0334 | Q1 | 1 |
| 2559 | RAIRO - Operations Research | 0399-0559 | Q3 | 1 |
| 2560 | RMS Research in Mathematics & Statistics | 2765-8449 | — | 1 |
| 2561 | RSC Chemical Biology | 2633-0679 | Q1 | 1 |
| 2562 | RSC Pharmaceutics | 2976-8713 | Q1 | 1 |
| 2563 | Radiochimica Acta | 0033-8230 | Q4 | 1 |
| 2564 | Radioengineering | 1210-2512 | Q3 | 1 |
| 2565 | Range Management and Agroforestry | 0971-2070 | Q3 | 1 |
| 2566 | Rare Metals | 1001-0521 | Q1 | 1 |
| 2567 | Reactive and Functional Polymers | 1381-5148 | Q1 | 1 |
| 2568 | Reason-A Technical Journal | 2277-1654 | — | 1 |
| 2569 | Recent Patents on Anti-Cancer Drug Discovery | 1574-8928 | Q2 | 1 |
| 2570 | Regional Environmental Change | 1436-378X | Q2 | 1 |
| 2571 | Renewable energy focus | 1755-0084 | Q1 | 1 |
| 2572 | Reports in Advances of Physical Sciences | 2424-9424 | — | 1 |
| 2573 | Reports on Progress in Physics | 0034-4885 | Q1 | 1 |
| 2574 | Research Journal of Pharmacy and Technology | 0974-360X | Q3 | 1 |
| 2575 | Research in Astronomy and Astrophysics | 1674-4527 | Q2 | 1 |
| 2576 | Research in Globalization | 2590-051X | Q1 | 1 |
| 2577 | Research in Veterinary Science | 0034-5288 | Q1 | 1 |
| 2578 | Resources Conservation & Recycling Advances | 2667-3789 | Q1 | 1 |
| 2579 | Resources Conservation & Recycling X | 2590-289X | — | 1 |
| 2580 | Resources Policy | 0301-4207 | Q1 | 1 |
| 2581 | Review of Social Economy | 0034-6764 | Q2 | 1 |
| 2582 | Revue des composites et des matériaux avancés | 1169-7954 | Q3 | 1 |
| 2583 | Rhizosphere | 2452-2198 | Q1 | 1 |
| 2584 | Risk Analysis | 0272-4332 | Q1 | 1 |
| 2585 | Risk, reliability and safety engineering | 2731-7811 | — | 1 |
| 2586 | River | 2750-4867 | Q2 | 1 |
| 2587 | Robotica | 0263-5747 | Q1 | 1 |
| 2588 | Rocky Mountain Journal of Mathematics | 0035-7596 | Q2 | 1 |
| 2589 | Russian Journal of Applied Chemistry | 0021-888X | Q3 | 1 |
| 2590 | SAE International Journal of Materials and Manufacturing | 1946-3979 | Q3 | 1 |
| 2591 | SAE international journal of fuels and lubricants | 1946-3952 | Q3 | 1 |
| 2592 | SAYAM | 3048-7064 | — | 1 |
| 2593 | SOILS AND FOUNDATIONS | 0038-0806 | Q1 | 1 |
| 2594 | SSM - Population Health | 2352-8273 | Q1 | 1 |
| 2595 | Safety and Reliability | 0961-7353 | Q3 | 1 |
| 2596 | Sampratyaya. | 3048-5851 | — | 1 |
| 2597 | Science Immunology | 2470-9468 | Q1 | 1 |
| 2598 | Science Talks | 2772-5693 | Q4 | 1 |
| 2599 | Science for Sustainability | 2666-7940 | — | 1 |
| 2600 | Science of Remote Sensing | 2666-0172 | Q1 | 1 |
| 2601 | Science of Sintering | 0350-820X | Q2 | 1 |
| 2602 | Scientia Iranica | 1026-3098 | Q3 | 1 |
| 2603 | Scientia Pharmaceutica | 0036-8709 | Q2 | 1 |
| 2604 | Sensing and Bio-Sensing Research | 2214-1804 | Q2 | 1 |
| 2605 | Sensor Letters | 1546-1971 | — | 1 |
| 2606 | Separation Science Plus | 2573-1815 | Q3 | 1 |
| 2607 | Separation and Purification Reviews | 1542-2119 | Q1 | 1 |
| 2608 | Shock and Vibration | 1070-9622 | Q3 | 1 |
| 2609 | Small Ruminant Research | 0921-4488 | Q2 | 1 |
| 2610 | Small Structures | 2688-4062 | Q1 | 1 |
| 2611 | Smart Construction and Sustainable Cities | 2731-9032 | Q1 | 1 |
| 2612 | Smart Science | 2308-0477 | Q2 | 1 |
| 2613 | Social Change | 0049-0857 | Q3 | 1 |
| 2614 | Social Network Analysis and Mining | 1869-5450 | Q1 | 1 |
| 2615 | Software Practice and Experience | 0038-0644 | Q2 | 1 |
| 2616 | Soil and Tillage Research | 0167-1987 | Q1 | 1 |
| 2617 | Solids | 2673-6497 | Q2 | 1 |
| 2618 | Sound&Vibration | 1541-0161 | Q2 | 1 |
| 2619 | Soundings An Interdisciplinary Journal | 0038-1861 | Q4 | 1 |
| 2620 | South African Journal of Botany | 0254-6299 | Q2 | 1 |
| 2621 | Soybean Research | 0973-1830 | — | 1 |
| 2622 | Space Weather | 1542-7390 | Q1 | 1 |
| 2623 | Special Matrices | 2300-7451 | Q2 | 1 |
| 2624 | Statistics in Biopharmaceutical Research | 1946-6315 | Q1 | 1 |
| 2625 | Statistics in Transition New Series | 1234-7655 | Q4 | 1 |
| 2626 | Stem Cell Reviews and Reports | 1550-8943 | Q2 | 1 |
| 2627 | Stochastics and Dynamics | 0219-4937 | Q2 | 1 |
| 2628 | Stroitel stvo nauka i obrazovanie [Construction Science and Education] | 2305-5502 | — | 1 |
| 2629 | Strojnícky časopis/Journal of Mechanical Engineering | 0039-2472 | Q3 | 1 |
| 2630 | Structural Chemistry | 1040-0400 | Q3 | 1 |
| 2631 | Structural Control and Health Monitoring | 1545-2255 | Q1 | 1 |
| 2632 | Structural Safety | 0167-4730 | Q1 | 1 |
| 2633 | Structural and Multidisciplinary Optimization | 1615-147X | Q1 | 1 |
| 2634 | Structure and Infrastructure Engineering | 1573-2479 | Q1 | 1 |
| 2635 | Studia Mathematica | 0039-3223 | Q1 | 1 |
| 2636 | Studies in South Asian Film & Media | 1756-4921 | Q4 | 1 |
| 2637 | Summerhill | 0972-1452 | — | 1 |
| 2638 | Superconductor Science and Technology | 0953-2048 | Q1 | 1 |
| 2639 | Surface Science | 0039-6028 | Q2 | 1 |
| 2640 | Surface Topography Metrology and Properties | 2051-672X | Q3 | 1 |
| 2641 | Sustainability & Circularity NOW | 2940-1852 | — | 1 |
| 2642 | Sustainability Science and Technology | 2977-3504 | — | 1 |
| 2643 | Sustainable Chemistry One World | 2950-3574 | Q1 | 1 |
| 2644 | Sustainable Chemistry and Pharmacy | 2352-5541 | Q1 | 1 |
| 2645 | Sustainable Chemistry for Climate Action | 2772-8269 | Q1 | 1 |
| 2646 | Sustainable and Resilient Infrastructure | 2378-9689 | Q2 | 1 |
| 2647 | Sustainable landscape planning and natural resources management | 2948-1910 | — | 1 |
| 2648 | Sustainable materials and technologies | 2214-9929 | Q1 | 1 |
| 2649 | System Dynamics Review | 0883-7066 | Q1 | 1 |
| 2650 | São Paulo Journal of Mathematical Sciences | 1982-6907 | Q3 | 1 |
| 2651 | Technologies | 2227-7080 | Q1 | 1 |
| 2652 | Technology and Economics of Smart Grids and Sustainable Energy | 2199-4706 | — | 1 |
| 2653 | Telematics and Informatics Reports | 2772-5030 | Q1 | 1 |
| 2654 | Terra Nova | 0954-4879 | Q1 | 1 |
| 2655 | Tetrahedron Green Chem | 2773-2231 | Q2 | 1 |
| 2656 | The ANZIAM Journal | 1446-1811 | Q4 | 1 |
| 2657 | The Electricity Journal | 1040-6190 | Q1 | 1 |
| 2658 | The European Physical Journal D | 1434-6060 | Q3 | 1 |
| 2659 | The European Physical Journal E | 1292-8941 | Q3 | 1 |
| 2660 | The FASEB Journal | 0892-6638 | Q1 | 1 |
| 2661 | The International Journal of Biochemistry & Cell Biology | 1357-2725 | Q2 | 1 |
| 2662 | The International Journal of Health Planning and Management | 0749-6753 | Q2 | 1 |
| 2663 | The International Review of Retail Distribution and Consumer Research | 0959-3969 | Q2 | 1 |
| 2664 | The International Trade Journal | 0885-3908 | Q3 | 1 |
| 2665 | The Journal of Immunology | 0022-1767 | Q1 | 1 |
| 2666 | The Journal of Infection in Developing Countries | 1972-2680 | Q3 | 1 |
| 2667 | The Journal of Infectious Diseases | 0022-1899 | Q1 | 1 |
| 2668 | The Journal of Physiology | 0022-3751 | Q1 | 1 |
| 2669 | The Journal of Supercritical Fluids | 0896-8446 | Q2 | 1 |
| 2670 | The Journal of World Intellectual Property | 1422-2213 | Q2 | 1 |
| 2671 | The Microbe | 2950-1946 | Q2 | 1 |
| 2672 | The Neuroscientist | 1073-8584 | Q1 | 1 |
| 2673 | The Open COVID Journal | 2666-9587 | — | 1 |
| 2674 | The Palaeobotanist | 0031-0174 | — | 1 |
| 2675 | The Physics of Metals and Metallography | 0031-918X | Q3 | 1 |
| 2676 | The Prostate | 0270-4137 | Q1 | 1 |
| 2677 | The Round Table | 0035-8533 | Q2 | 1 |
| 2678 | The Structural Design of Tall and Special Buildings | 1541-7794 | Q1 | 1 |
| 2679 | Theoretical Chemistry Accounts | 1432-2234 | Q3 | 1 |
| 2680 | Theoretical Foundations of Chemical Engineering | 0040-5795 | Q4 | 1 |
| 2681 | Theoretical Population Biology | 0040-5809 | Q2 | 1 |
| 2682 | Theoretical and Computational Fluid Dynamics | 0935-4964 | Q1 | 1 |
| 2683 | Theranostics | 1838-7640 | — | 1 |
| 2684 | Thermal Engineering | 0040-3636 | Q3 | 1 |
| 2685 | Thermal Science | 0354-9836 | Q4 | 1 |
| 2686 | Third World Quarterly | 0143-6597 | Q1 | 1 |
| 2687 | Thrombosis Journal | 1477-9560 | Q2 | 1 |
| 2688 | Tissue Barriers | 2168-8362 | Q1 | 1 |
| 2689 | Tissue Engineering | 1076-3279 | — | 1 |
| 2690 | Topics in Cognitive Science | 1756-8757 | Q1 | 1 |
| 2691 | Topics in Current Chemistry | 2364-8961 | — | 1 |
| 2692 | Towards Excellence | 0974-035X | — | 1 |
| 2693 | Toxicology Research | 2045-452X | Q3 | 1 |
| 2694 | Toxicology and Applied Pharmacology | 0041-008X | Q2 | 1 |
| 2695 | Traffic Injury Prevention | 1538-957X | Q2 | 1 |
| 2696 | Transactions in GIS | 1361-1682 | Q2 | 1 |
| 2697 | Transactions of the Institute of Measurement and Control | 0142-3312 | Q2 | 1 |
| 2698 | Transactions on Electrical and Electronic Materials | 1229-7607 | Q2 | 1 |
| 2699 | Translational Oncology | 1936-5233 | Q1 | 1 |
| 2700 | Transportation Geotechnics | 2214-3912 | Q1 | 1 |
| 2701 | Transportation Research Part F Traffic Psychology and Behaviour | 1369-8478 | Q1 | 1 |
| 2702 | Trees Forests and People | 2666-7193 | Q1 | 1 |
| 2703 | Trends in biotechnology | 0167-7799 | Q1 | 1 |
| 2704 | Tropical Cyclone Research and Review | 2225-6032 | Q1 | 1 |
| 2705 | Tropical Ecology | 0564-3295 | Q2 | 1 |
| 2706 | Tsitologiya | 0041-3771 | — | 1 |
| 2707 | Tuberculosis | 1472-9792 | Q2 | 1 |
| 2708 | Tumour Virus Research | 2666-6790 | Q1 | 1 |
| 2709 | Turkish Journal of Civil Engineering | 1300-3453 | Q3 | 1 |
| 2710 | Value in Health Regional Issues | 2212-1099 | Q1 | 1 |
| 2711 | Vascular Pharmacology | 1537-1891 | Q2 | 1 |
| 2712 | Vehicular Communications | 2214-2096 | Q1 | 1 |
| 2713 | Vessel Plus | 2574-1209 | Q3 | 1 |
| 2714 | Veterinary Quarterly | 0165-2176 | Q1 | 1 |
| 2715 | Vibrational Spectroscopy | 0924-2031 | Q3 | 1 |
| 2716 | Vibroengineering PROCEDIA | 2345-0533 | — | 1 |
| 2717 | Vidyasagar University Journal of Economics | 0975-8003 | — | 1 |
| 2718 | Vilakshan – XIMB Journal of Management | 0973-1954 | — | 1 |
| 2719 | Virus Research | 0168-1702 | Q2 | 1 |
| 2720 | Viruses | 1999-4915 | Q1 | 1 |
| 2721 | Waste Management | 0956-053X | Q1 | 1 |
| 2722 | Waste Management Bulletin | 2949-7507 | Q1 | 1 |
| 2723 | Water and Environment Journal | 0951-7359 | Q2 | 1 |
| 2724 | Weather and Climate Extremes | 2212-0947 | Q1 | 1 |
| 2725 | Wellcome Open Research | 2398-502X | Q3 | 1 |
| 2726 | Wiley Interdisciplinary Reviews Computational Molecular Science | 1759-0876 | Q1 | 1 |
| 2727 | Women s Studies International Forum | 0277-5395 | Q1 | 1 |
| 2728 | Wood Material Science and Engineering | 1748-0272 | Q2 | 1 |
| 2729 | World Patent Information | 0172-2190 | Q2 | 1 |
| 2730 | Zeitschrift für anorganische und allgemeine Chemie | 0044-2313 | Q3 | 1 |
| 2731 | eLife | 2050-084X | Q1 | 1 |
| 2732 | iMetaOmics. | 2996-9506 | — | 1 |
| 2733 | mSphere | 2379-5042 | Q1 | 1 |
| 2734 | mSystems | 2379-5077 | Q1 | 1 |
| 2735 | npj Biomedical Innovations. | 3005-1444 | — | 1 |
| 2736 | npj Microgravity | 2373-8065 | Q1 | 1 |
| 2737 | npj Quantum Materials | 2397-4648 | Q1 | 1 |
| 2738 | npj Spintronics | 2948-2119 | Q1 | 1 |
| 2739 | npj Systems Biology and Applications | 2056-7189 | Q1 | 1 |
| 2740 | npj Thermal Science and Engineering | 3059-3301 | — | 1 |
| 2741 | steel research international | 1611-3683 | Q2 | 1 |
| 2742 | tripleC Communication Capitalism & Critique Open Access Journal for a Global Sustainable Information Society | 1726-670X | Q2 | 1 |
| 2743 | Бизнес-информатика | 1998-0663 | Q4 | 1 |
| 2744 | 中国科学通报：英文版 | 2095-9273 | Q1 | 1 |

### 5.2 Conferences / proceedings (533)

Note: for Springer book series (e.g. *Lecture Notes in Computer Science*) OpenAlex records the series rather than the individual conference.

| # | Conference / proceedings venue | CORE rank | Papers |
|---|---|---|---|
| 1 | Lecture notes in civil engineering | — | 189 |
| 2 | Lecture notes in mechanical engineering | — | 157 |
| 3 | Lecture notes in computer science | — | 126 |
| 4 | AIP conference proceedings | — | 110 |
| 5 | IEEE International Conference on Advanced Networks and Telecommunications Systems | — | 77 |
| 6 | Communications in computer and information science | — | 75 |
| 7 | Springer proceedings in physics | — | 73 |
| 8 | National Conference on Communications | — | 72 |
| 9 | Lecture notes in networks and systems | — | 57 |
| 10 | IEEE Vehicular Technology Conference | B | 40 |
| 11 | IEEE Microwaves, Antennas, and Propagation Conference (MAPCON) | — | 39 |
| 12 | Springer Proceedings in Materials | — | 36 |
| 13 | IOP Conference Series Materials Science and Engineering | — | 35 |
| 14 | International Conference on Communication Systems & Networks (COMSNETS) | — | 33 |
| 15 | International Conference on Microwave, Optical and Communication Engineering | — | 31 |
| 16 | Lecture notes in electrical engineering | — | 30 |
| 17 | Journal of Physics Conference Series | — | 29 |
| 18 | IEEE International Symposium on Smart Electronic Systems (iSES) | — | 28 |
| 19 | Proceeding of Proceedings of the 26thNational and 4th International ISHMT-ASTFE Heat and Mass Transfer Conference December 17-20, 2021, IIT Madras, Chennai-600036, Tamil Nadu, India | — | 28 |
| 20 | National Power Systems Conference | — | 27 |
| 21 | IEEE India Council International Conference (INDICON) | — | 25 |
| 22 | IEEE Region 10 Conference (TENCON) | C | 25 |
| 23 | IEEE International Conference on Power Electronics, Drives and Energy Systems | — | 23 |
| 24 | IEEE Wireless Communications and Networking Conference | B | 23 |
| 25 | IEEE International Conference on Power Electronics, Smart Grid, and Renewable Energy (PESGRE) | — | 20 |
| 26 | IEEE International Symposium on Circuits and Systems proceedings | — | 20 |
| 27 | IEEE Power India International Conference | — | 20 |
| 28 | International Conference on VLSI Design and International Conference on Embedded Systems (VLSID) | — | 20 |
| 29 | National Power Electronics Conference (NPEC) | — | 20 |
| 30 | IEEE International Conference on Sustainable Energy and Future Electric Transportation (SEFET) | — | 19 |
| 31 | IEEE International Geoscience and Remote Sensing Symposium (IGARSS) | C | 19 |
| 32 | International Conference on Computing, Communication and Networking Technologies (ICCCNT) | — | 19 |
| 33 | IEEE India Geoscience and Remote Sensing Symposium (InGARSS) | — | 18 |
| 34 | International Conference on Signal Processing and Communications (SPCOM) | — | 18 |
| 35 | IEEE Symposium Series on Computational Intelligence (SSCI) | — | 16 |
| 36 | International Conference on PErvasive Technologies Related to Assistive Environments (PETRA) | — | 16 |
| 37 | Proceedings of the Annual Conference of the IEEE Industrial Electronics Society | — | 14 |
| 38 | IEEE International Conference on Acoustics Speech and Signal Processing | B | 13 |
| 39 | IEEE International Symposium on Personal, Indoor and Mobile Radio Communications (PIMRC) | B | 13 |
| 40 | IEEE/CVF Winter Conference on Applications of Computer Vision (WACV) | A | 13 |
| 41 | Lecture notes on multidisciplinary industrial engineering | — | 13 |
| 42 | ACS symposium series | — | 12 |
| 43 | Conference proceedings/Conference proceedings - IEEE International Conference on Systems, Man, and Cybernetics | — | 12 |
| 44 | International Conference on Pattern Recognition Applications and Methods | B | 12 |
| 45 | International Conference on Power Systems (ICPS) | — | 12 |
| 46 | Springer proceedings in mathematics & statistics | — | 12 |
| 47 | Advances in intelligent systems and computing | — | 11 |
| 48 | Annual Conference on Large Hadron Collider Physics (LHCP) | — | 11 |
| 49 | Conference record | — | 11 |
| 50 | IEEE International Conference on Emerging Electronics (ICEE) | — | 11 |
| 51 | IEEE International Conference on Nanotechnology (IEEE-NANO) | — | 11 |
| 52 | IEEE International Symposium on Biomedical Imaging (ISBI) | — | 11 |
| 53 | International Conference on Consumer Electronics | — | 11 |
| 54 | International Workshop on Vertex Detectors (VERTEX) | — | 11 |
| 55 | National and International ISHMT-ASTFE Heat and Mass Transfer Conference (IHMTC) | — | 11 |
| 56 | European Signal Processing Conference (EUSIPCO) | — | 10 |
| 57 | Globecom | — | 10 |
| 58 | IEEE Indian Conference on Antennas and Propagation (InCAP) | — | 10 |
| 59 | IEEE International Conference on Identity, Security and Behavior Analysis (ISBA) | — | 10 |
| 60 | IEEE International Conference on Smart Technologies for Power, Energy and Control (STPEC) | — | 10 |
| 61 | IEEE International Joint Conference on Biometrics (IJCB) | B | 10 |
| 62 | IEEE Wireless Antenna and Microwave Symposium (WAMS) | — | 10 |
| 63 | International Conference on Distributed Computing and Networking (ICDCN) | — | 10 |
| 64 | International Conference on Power Electronics and Energy (ICPEE) | — | 10 |
| 65 | International Joint Conference on Biomedical Engineering Systems and Technologies (BIOSTEC) | — | 10 |
| 66 | International Symposium on VLSI Design and Test (VDAT) | — | 10 |
| 67 | International conference on fiber optics and photonics | — | 10 |
| 68 | IEEE Computer Society Annual Symposium on VLSI | — | 9 |
| 69 | IEEE Electron Devices Technology & Manufacturing Conference (EDTM) | — | 9 |
| 70 | IEEE Region 10 Symposium (TENSYMP) | — | 9 |
| 71 | International Conference on Communications | — | 9 |
| 72 | International Conference on Range Technology (ICORT) | — | 9 |
| 73 | URSI Asia-Pacific Radio Science Conference | — | 9 |
| 74 | URSI Regional Conference on Radio Science (URSI-RCRS) | — | 9 |
| 75 | IEEE International Symposium on Nanoelectronic and Information Systems (iNIS) | — | 8 |
| 76 | IEEE National Aerospace and Electronics Conference (NAECON) | — | 8 |
| 77 | International Conference in Advances in Power, Signal, and Information Technology (APSIT) | — | 8 |
| 78 | International Conference on Computers and Devices for Communication | — | 8 |
| 79 | International Conference on Signal Processing and Integrated Networks (SPIN) | — | 8 |
| 80 | Procedia Computer Science | — | 8 |
| 81 | Springer eBooks | — | 8 |
| 82 | IEEE Applied Sensing Conference (APSCON) | — | 7 |
| 83 | IEEE Consumer Communications & Networking Conference (CCNC) | — | 7 |
| 84 | IET conference proceedings. | — | 7 |
| 85 | International Conference on Cyber Situational Awareness, Data Analytics and Assessment (CyberSA) | — | 7 |
| 86 | Mechanisms and machine science | — | 7 |
| 87 | Proceedings of SPIE, the International Society for Optical Engineering/Proceedings of SPIE | — | 7 |
| 88 | EPJ Web of Conferences | — | 6 |
| 89 | Frontiers in Optics + Laser Science (FiO, LS) | — | 6 |
| 90 | IEEE Globecom Workshops (GC Wkshps) | — | 6 |
| 91 | IEEE International Symposium on Antennas and Propagation and USNC-URSI Radio Science Meeting (AP-S/URSI) | — | 6 |
| 92 | IEEE International Workshop on Machine Learning for Signal Processing (MLSP) | — | 6 |
| 93 | IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW) | — | 6 |
| 94 | Indian Control Conference | — | 6 |
| 95 | International Conference on Microwave and Photonics | — | 6 |
| 96 | International Cosmic Ray Conference | — | 6 |
| 97 | International Heat Transfer Conference (IHTC) | — | 6 |
| 98 | Proceedings of IEEE Sensors/Proceedings of IEEE Sensors ... | — | 6 |
| 99 | Springer proceedings in energy | — | 6 |
| 100 | Sustainable civil infrastructures | — | 6 |
| 101 | URSI Atlantic and Asia Pacific Radio Science Meeting (AT-AP-RASC) | — | 6 |
| 102 | 2022 IEEE International Conference on Signal Processing and Communications (SPCOM) | — | 5 |
| 103 | ACM/IEEE International Conference on Formal Methods and Models for System Design (MEMOCODE) | C | 5 |
| 104 | ASME Power Conference | — | 5 |
| 105 | European Conference on Antennas and Propagation | — | 5 |
| 106 | Geo-Chicago | — | 5 |
| 107 | Global Power, Energy and Communication Conference | — | 5 |
| 108 | IEEE Asia Pacific Conference on Circuits and Systems (APCCAS) | — | 5 |
| 109 | IEEE Conference on Electron Devices and Solid-State Circuits | — | 5 |
| 110 | IEEE Conference on Information and Communication Technology (CICT) | — | 5 |
| 111 | IEEE Global Humanitarian Technology Conference (GHTC) | — | 5 |
| 112 | IEEE International Conference on Communications workshops | — | 5 |
| 113 | IEEE International Conference on Energy Technologies for Future Grids (ETFG) | — | 5 |
| 114 | IEEE International Conference on Industrial and Information Systems (ICIIS) | — | 5 |
| 115 | IEEE International Conference on Interdisciplinary Approaches in Technology and Management for Social Innovation (IATMSI) | — | 5 |
| 116 | IEEE International Conference on Power Systems (ICPS) | — | 5 |
| 117 | IEEE International Conference on Solid-State and Integrated Circuit Technology | — | 5 |
| 118 | IEEE International Power and Renewable Energy Conference (IPRECON) | — | 5 |
| 119 | IEEE International Symposium on Computer-Based Medical Systems (CBMS) | — | 5 |
| 120 | IEEE International Symposium on Information Theory (ISIT) | B | 5 |
| 121 | IEEE MTT-S International Microwave and RF Conference (IMaRC) | — | 5 |
| 122 | IEEE Power & Energy Society General Meeting (PESGM) | — | 5 |
| 123 | Innovations in Software Engineering Conference (ISEC) | — | 5 |
| 124 | International Conference on Automatic Face and Gesture Recognition | — | 5 |
| 125 | International Conference on Machine Intelligence for GeoAnalytics and Remote Sensing (MIGARS) | — | 5 |
| 126 | International Conference on Signal Processing, Communication, Power and Embedded System (SCOPES) | C | 5 |
| 127 | International Electronic Conference on Sensors and Applications (ECSA) | A | 5 |
| 128 | Lecture notes in physics | — | 5 |
| 129 | Procedia Engineering | — | 5 |
| 130 | Proceedings - International Conference on Image Processing | — | 5 |
| 131 | Studies in Rhythm Engineering | — | 5 |
| 132 | ASCE Geo-Congress | — | 4 |
| 133 | Conference proceedings | — | 4 |
| 134 | Conference record of the IEEE Photovoltaic Specialists Conference | — | 4 |
| 135 | Energy Procedia | — | 4 |
| 136 | Environmental science and engineering | — | 4 |
| 137 | European Control Conference (ECC) | — | 4 |
| 138 | IEEE Asia-Pacific Microwave Conference (APMC) | — | 4 |
| 139 | IEEE Conference on Computer Vision and Pattern Recognition Workshops (CVPRW) | A* | 4 |
| 140 | IEEE Conference on Virtual Reality and 3D User Interfaces Abstracts and Workshops (VRW) | A* | 4 |
| 141 | IEEE Electrical Design of Advanced Packaging and Systems Symposium (EDAPS) | — | 4 |
| 142 | IEEE India Council International Subsections Conference (INDISCON) | — | 4 |
| 143 | IEEE International Conference on Electronics, Circuits and Systems (ICECS) | — | 4 |
| 144 | IEEE International Conference on Electronics, Computing and Communication Technologies (CONECCT) | — | 4 |
| 145 | IEEE International Conference on Smart Instrumentation, Measurement and Applications (ICSIMA) | — | 4 |
| 146 | IEEE PES Asia-Pacific Power and Energy Engineering Conference | — | 4 |
| 147 | International Conference on Sensing Technology | — | 4 |
| 148 | International Joint Conference on Computer Vision, Imaging and Computer Graphics Theory and Applications (VISIGRAPP) | — | 4 |
| 149 | International Symposium on Quality Electronic Design (ISQED) | — | 4 |
| 150 | International VLSI Symposium on Technology, Systems and Applications (VLSI-TSA) | — | 4 |
| 151 | Odisha International Conference on Electrical Power Engineering, Communication and Computing Technology (ODICON) | — | 4 |
| 152 | Proceedings of the ... American Control Conference/Proceedings of the American Control Conference | — | 4 |
| 153 | Proceedings of the Annual International Conference of the IEEE Engineering in Medicine and Biology Society | — | 4 |
| 154 | ASME International Conference on Nanochannels, Microchannels, and Minichannels (ICNMM) | — | 3 |
| 155 | Advances in Science, Technology & Innovation/Advances in science, technology & innovation | — | 3 |
| 156 | Annual Meeting of the Association for Computational Linguistics (ACL) | A* | 3 |
| 157 | Conference on Control and Fault-Tolerant Systems | — | 3 |
| 158 | E3S Web of Conferences | — | 3 |
| 159 | Frontiers in Optics | — | 3 |
| 160 | IEEE Conference on Cognitive and Computational Aspects of Situation Management (CogSIMA) | — | 3 |
| 161 | IEEE Conference on Computational Intelligence in Bioinformatics and Computational Biology (CIBCB) | C | 3 |
| 162 | IEEE Conference on Computer Communications Workshops (INFOCOM WKSHPS) | A* | 3 |
| 163 | IEEE Conference on Control Technology and Applications (CCTA) | — | 3 |
| 164 | IEEE Conference on Technologies for Sustainability | — | 3 |
| 165 | IEEE Energy Conversion Congress and Exposition (ECCE) | — | 3 |
| 166 | IEEE Future Networks World Forum (FNWF) | — | 3 |
| 167 | IEEE Guwahati Subsection Conference (GCON) | — | 3 |
| 168 | IEEE India International Conference on Power Electronics | — | 3 |
| 169 | IEEE Industrial Electronics Society Annual On-Line Conference (ONCON) | — | 3 |
| 170 | IEEE Information Theory Workshop (ITW) | B | 3 |
| 171 | IEEE International Conference on Human-Machine Systems (ICHMS) | — | 3 |
| 172 | IEEE International Conference on Power Electronics, Intelligent Control and Energy Systems | — | 3 |
| 173 | IEEE International Magnetics Conference | — | 3 |
| 174 | IEEE International Symposium on Mixed and Augmented Reality Adjunct (ISMAR-Adjunct) | — | 3 |
| 175 | IEEE International System-on-Chip Conference (SOCC) | — | 3 |
| 176 | IEEE Photonics Conference | — | 3 |
| 177 | IEEE SOI-3D-Subthreshold Microelectronics Technology Unified Conference | — | 3 |
| 178 | IEEE Texas Power and Energy Conference (TPEC) | — | 3 |
| 179 | IEEE Workshop on Signal and Power Integrity | — | 3 |
| 180 | IEEMA Engineer Infinite Conference (eTechNxT) | — | 3 |
| 181 | International Conference on Availability, Reliability and Security (ARES) | B | 3 |
| 182 | International Conference on Cognitive Computing and Information Processing | — | 3 |
| 183 | International Conference on Computer Applications in Electrical Engineering-Recent Advances (CERA) | — | 3 |
| 184 | International Conference on Computer Vision Theory and Applications | — | 3 |
| 185 | International Conference on Control and Fault-Tolerant Systems (SysTol) | — | 3 |
| 186 | International Conference on Control, Automation, Robotics and Vision (ICARCV) | C | 3 |
| 187 | International Conference on Digital Information Processing and Communications | — | 3 |
| 188 | International Conference on Distributed Computing in Sensor Systems (DCOSS) | B | 3 |
| 189 | International Conference on Electrical, Electronics, and Optimization Techniques | — | 3 |
| 190 | International Conference on Electromagnetics in Advanced Applications (ICEAA) | — | 3 |
| 191 | International Conference on Electronics, Computers and Artificial Intelligence (ECAI) | A | 3 |
| 192 | International Conference on Emerging Electronics (ICEE) | — | 3 |
| 193 | International Conference on Wireless Communications, Signal Processing and Networking (WiSPNET) | — | 3 |
| 194 | International Symposium on Wireless Personal Multimedia Communications (WPMC) | — | 3 |
| 195 | International Workshop on Biometrics and Forensics (IWBF) | — | 3 |
| 196 | JSAP-Optica Joint Symposia | — | 3 |
| 197 | PHM Society European Conference | — | 3 |
| 198 | Proceedings of the IEEE Conference on Decision & Control, including the Symposium on Adaptive Processes | — | 3 |
| 199 | Proceedings of the World Congress on Momentum, Heat and Mass Transfer | — | 3 |
| 200 | Proceedings, IEEE International Conference on Computer Design/Proceedings - IEEE International Conference on Computer Design | — | 3 |
| 201 | Smart innovation, systems and technologies | — | 3 |
| 202 | Springer proceedings in complexity | — | 3 |
| 203 | 2012 International Conference on Computing, Networking and Communications (ICNC) | — | 2 |
| 204 | 2018 2nd International Conference on Power, Energy and Environment: Towards Smart Technology (ICEPE) | — | 2 |
| 205 | 2022 IEEE 18th International Conference on Automation Science and Engineering (CASE) | — | 2 |
| 206 | 2022 International Joint Conference on Neural Networks (IJCNN) | B | 2 |
| 207 | ACM Asia Conference on Computer and Communications Security (ASIA CCS) | A* | 2 |
| 208 | ACM Great Lakes Symposium on VLSI (GLSVLSI) | — | 2 |
| 209 | ACM International Conference on Multimedia (ACM MM) | — | 2 |
| 210 | ASPS Conference Proceedings | — | 2 |
| 211 | Asia Communications and Photonics Conference | — | 2 |
| 212 | Asia-Pacific Conference on Synthetic Aperture Radar (APSAR) | — | 2 |
| 213 | Asia-Pacific Microwave Conference (APMC) | — | 2 |
| 214 | Conference on Information and Communication Technology (CICT) | — | 2 |
| 215 | Conference on Local Computer Networks | — | 2 |
| 216 | Corfu Summer Institute School and Workshops on Elementary Particle Physics and Gravity (CORFU) | — | 2 |
| 217 | ECS Transactions | — | 2 |
| 218 | European Conference on Networks and Communications | — | 2 |
| 219 | European Conference on Power Electronics and Applications | — | 2 |
| 220 | European Microwave Conference (EuMC) | — | 2 |
| 221 | European Workshop on Visual Information Processing | — | 2 |
| 222 | Green energy and technology | — | 2 |
| 223 | IAPR Asian Conference on Pattern Recognition (ACPR) | — | 2 |
| 224 | ICL contribution to landslide disaster risk reduction | — | 2 |
| 225 | IEEE ... International Conference on Data Mining workshops | A* | 2 |
| 226 | IEEE Annual Computer Software and Applications Conference (COMPSAC) | B | 2 |
| 227 | IEEE Applied Power Electronics Conference and Exposition (APEC) | — | 2 |
| 228 | IEEE Applied Signal Processing Conference (ASPCON) | — | 2 |
| 229 | IEEE Asia-Pacific Conference on Communications (APCC) | C | 2 |
| 230 | IEEE Calcutta Conference (CALCON) | — | 2 |
| 231 | IEEE India Conference | — | 2 |
| 232 | IEEE Innovative Smart Grid Technologies-Asia | — | 2 |
| 233 | IEEE International Conference for Convergence in Technology (I2CT) | — | 2 |
| 234 | IEEE International Conference on Advanced Video and Signal Based Surveillance (AVSS) | B | 2 |
| 235 | IEEE International Conference on Bioinformatics and Biomedicine (BIBM) | — | 2 |
| 236 | IEEE International Conference on Communication Systems and Network Technologies (CSNT) | — | 2 |
| 237 | IEEE International Conference on Distributed Computing Systems (ICDCS) | A | 2 |
| 238 | IEEE International Conference on Machine Learning and Applications (ICMLA) | A* | 2 |
| 239 | IEEE International Conference on Power Electronics and Drive Systems (PEDS) | — | 2 |
| 240 | IEEE International Conference on Power and Energy | — | 2 |
| 241 | IEEE International Conference on Soft Robotics (RoboSoft) | — | 2 |
| 242 | IEEE International Magnetic Conference - Short Papers (INTERMAG Short Papers) | — | 2 |
| 243 | IEEE VTS Asia Pacific Wireless Communications Symposium (APWCS) | — | 2 |
| 244 | IEEE World Forum on Internet of Things (WF-IoT) | — | 2 |
| 245 | IEEE/CVF International Conference on Computer Vision (ICCV) | A* | 2 |
| 246 | IEEE/CVF Winter Conference on Applications of Computer Vision Workshops (WACVW) | — | 2 |
| 247 | IFIP advances in information and communication technology | — | 2 |
| 248 | IFIP/IEEE International Conference on Very Large Scale Integration | — | 2 |
| 249 | IOP Conference Series Earth and Environmental Science | — | 2 |
| 250 | India International Conference on Power Electronics (IICPE) | — | 2 |
| 251 | Indian Conference on Computer Vision, Graphics and Image Processing | — | 2 |
| 252 | International Conference on Advanced Computation and Telecommunication (ICACAT) | — | 2 |
| 253 | International Conference on Advances in Electrical, Computing, Communication and Sustainable Technologies (ICAECT) | — | 2 |
| 254 | International Conference on Bio Signals, Images, and Instrumentation (ICBSII) | — | 2 |
| 255 | International Conference on Communication, Control and Intelligent Systems (CCIS) | — | 2 |
| 256 | International Conference on Communications, Signal Processing, and their Applications (ICCSPA) | — | 2 |
| 257 | International Conference on Computational Techniques in Information and Communication Technologies | — | 2 |
| 258 | International Conference on Computing, Analytics and Security Trends | — | 2 |
| 259 | International Conference on Cyber Security and Protection of Digital Services (Cyber Security) | — | 2 |
| 260 | International Conference on Digital Signal Processing and its Applications (DSPA) | — | 2 |
| 261 | International Conference on Electrical Drives & Power Electronics (EDPE) | — | 2 |
| 262 | International Conference on Electrical, Computer and Communication Technologies (ICECCT) | — | 2 |
| 263 | International Conference on Electrical, Computer and Energy Technologies (ICECET) | — | 2 |
| 264 | International Conference on High Energy Physics (ICHEP) | — | 2 |
| 265 | International Conference on Image Information Processing (ICIIP) | — | 2 |
| 266 | International Conference on Innovation and Intelligence for Informatics, Computing, and Technologies (3ICT) | — | 2 |
| 267 | International Conference on Mechatronics and Robotics Engineering (ICMRE) | — | 2 |
| 268 | International Conference on Mixed Design of Integrated Circuits and Systems (MIXDES) | — | 2 |
| 269 | International Conference on Network and Service Management (CNSM) | B | 2 |
| 270 | International Conference on Opto-Electronics and Applied Optics (Optronix) | — | 2 |
| 271 | International Conference on Security of Information and Networks (SIN) | C | 2 |
| 272 | International Conference on Signal Processing, Computing and Control (ISPCC) | — | 2 |
| 273 | International Conference on Spoken Language Translation (IWSLT) | — | 2 |
| 274 | International Electronic Conference on Applied Sciences (ASEC) | — | 2 |
| 275 | International SoC Design Conference | — | 2 |
| 276 | International Symposium on VLSI Technology, Systems and Application (VLSI-TSA) | — | 2 |
| 277 | International Symposium on Wireless Communication Systems | — | 2 |
| 278 | International Workshop on the CKM Unitarity Triangle (CKM) | — | 2 |
| 279 | Joint European Conference on Networks and Communications & 6G Summit (EuCNC/6G Summit) | — | 2 |
| 280 | Lecture notes of the Institute for Computer Sciences, Social Informatics and Telecommunications Engineering | — | 2 |
| 281 | Machine Learning and Data Mining in Pattern Recognition | — | 2 |
| 282 | OCEANS 2016 - Shanghai | — | 2 |
| 283 | Proceedings of ... IEEE International Conference on Fuzzy Systems | B | 2 |
| 284 | Proceedings of the 28th Annual International Conference on Mobile Computing And Networking | — | 2 |
| 285 | Proceedings of the IEEE National Radar Conference | — | 2 |
| 286 | Report | — | 2 |
| 287 | SPIE Medical Imaging: Digital Pathology | — | 2 |
| 288 | Springer series in geomechanics and geoengineering | — | 2 |
| 289 | Structural integrity | — | 2 |
| 290 | Topical Workshop on Electronics for Particle Physics (TWEPP) | — | 2 |
| 291 | Transport Research Forum | — | 2 |
| 292 | Workshop on Recent Advances in Photonics (WRAP) | — | 2 |
| 293 | 2006 14th Mediterranean Conference on Control and Automation | — | 1 |
| 294 | 2018 52nd Asilomar Conference on Signals, Systems, and Computers | — | 1 |
| 295 | 2018 IEEE Electron Devices Kolkata Conference (EDKCON) | — | 1 |
| 296 | 2019 International Conference on Power Electronics, Control and Automation (ICPECA) | — | 1 |
| 297 | 2022 IEEE 20th International Conference on Industrial Informatics (INDIN) | — | 1 |
| 298 | ACM International Conference on AI in Finance (ICAIF) | — | 1 |
| 299 | ACM International Conference on Hybrid Systems: Computation and Control (HSCC) | — | 1 |
| 300 | ACM International Conference on Multimedia in Asia (MMAsia) | — | 1 |
| 301 | ACM International Conference on Supercomputing (ICS) | A | 1 |
| 302 | ACM SIGCOMM Conference Posters and Demos | A* | 1 |
| 303 | ACM Symposium on Applied Computing | — | 1 |
| 304 | ACM/IEEE International Symposium on Low Power Electronics and Design (ISLPED) | — | 1 |
| 305 | AIAA Propulsion and Energy Forum | — | 1 |
| 306 | AIAA SciTech Forum | — | 1 |
| 307 | ASCE International Airfield and Highway Pavements Conference | — | 1 |
| 308 | ASME International Conference on Energy Sustainability (ES) | — | 1 |
| 309 | Abstracts with programs - Geological Society of America | — | 1 |
| 310 | Advances in Robotics - International Conference of The Robotics Society (AIR) | — | 1 |
| 311 | Advances in geographical and environmental sciences | — | 1 |
| 312 | Algorithms for intelligent systems | — | 1 |
| 313 | Allerton Conference on Communication, Control, and Computing | — | 1 |
| 314 | Annals of Computer Science and Information Systems | — | 1 |
| 315 | Annual SIGdial Meeting on Discourse and Dialogue (SIGDIAL) | B | 1 |
| 316 | Asia and South Pacific Design Automation Conference (ASP-DAC) | C | 1 |
| 317 | Asia-Pacific Conference on Communications (APCC) | C | 1 |
| 318 | Asian Conference on Energy, Power and Transportation Electrification (ACEPT) | — | 1 |
| 319 | Asian Conference on Innovation in Technology (ASIANCON) | — | 1 |
| 320 | Asian Hardware Oriented Security and Trust Symposium (AsianHOST) | — | 1 |
| 321 | Australasian Universities Power Engineering Conference | — | 1 |
| 322 | Biophotonics Congress 2021 | — | 1 |
| 323 | Biosystems & biorobotics | — | 1 |
| 324 | Compilers, Architecture, and Synthesis for Embedded Systems | — | 1 |
| 325 | Conference digest | — | 1 |
| 326 | Conference of the European Chapter of the Association for Computational Linguistics | A* | 1 |
| 327 | Conference on Computer and Robot Vision (CRV) | — | 1 |
| 328 | Conference on Information Sciences and Systems | — | 1 |
| 329 | Conference on Information and Knowledge Management | — | 1 |
| 330 | Conference on Lasers and Electro-Optics | — | 1 |
| 331 | Conference on Lasers and Electro-Optics Europe & European Quantum Electronics Conference (CLEO/Europe-EQEC) | — | 1 |
| 332 | Conference on Lasers and Electro-Optics Pacific Rim (CLEO-PR) | — | 1 |
| 333 | Design, Automation, and Test in Europe | — | 1 |
| 334 | Designing Interactive Systems Conference | A | 1 |
| 335 | EAI/Springer Innovations in Communication and Computing | — | 1 |
| 336 | European Physical Society Conference on High Energy Physics (EPS-HEP) | — | 1 |
| 337 | Geo-Extreme | — | 1 |
| 338 | Global Conference for Advancement in Technology (GCAT) | — | 1 |
| 339 | Global Oceans 2020: Singapore – U.S. Gulf Coast | — | 1 |
| 340 | Goldschmidt Abstracts | — | 1 |
| 341 | IEEE Annual Southern Power Electronics Conference | — | 1 |
| 342 | IEEE Applied Imagery Pattern Recognition Workshop | — | 1 |
| 343 | IEEE Automatic Speech Recognition and Understanding Workshop (ASRU) | C | 1 |
| 344 | IEEE Computer Society Conference on Computer Vision and Pattern Recognition/Proceedings - IEEE Computer Society Conference on Computer Vision and Pattern Recognition/Proceedings | — | 1 |
| 345 | IEEE Conference on Electrical Performance of Electronic Packaging and Systems (EPEPS) | — | 1 |
| 346 | IEEE Conference on Games (CoG) | — | 1 |
| 347 | IEEE Congress on Evolutionary Computation (CEC) | B | 1 |
| 348 | IEEE Electron Devices Technology and Manufacturing Conference (EDTM) | — | 1 |
| 349 | IEEE Eurasia Conference on IOT, Communication and Engineering (ECICE) | — | 1 |
| 350 | IEEE European Symposium on Security and Privacy Workshops (EuroS&PW) | A | 1 |
| 351 | IEEE Global Conference for Advancement in Technology (GCAT) | — | 1 |
| 352 | IEEE Global Conference on Signal and Information Processing | — | 1 |
| 353 | IEEE IAS Global Conference on Emerging Technologies (GlobConET) | C | 1 |
| 354 | IEEE International Black Sea Conference on Communications and Networking | — | 1 |
| 355 | IEEE International Conference on Antenna Innovations & Modern Technologies for Ground, Aircraft and Satellite Applications (iAIM) | — | 1 |
| 356 | IEEE International Conference on Big Data Computing Service and Applications (BigDataService) | B | 1 |
| 357 | IEEE International Conference on Big Data and Smart Computing (BigComp) | B | 1 |
| 358 | IEEE International Conference on Bioinformatics and Bioengineering (BIBE) | C | 1 |
| 359 | IEEE International Conference on Cloud Computing in Emerging Markets (CCEM) | B | 1 |
| 360 | IEEE International Conference on Communications, Control, and Computing Technologies for Smart Grids (SmartGridComm) | — | 1 |
| 361 | IEEE International Conference on Compatibility, Power Electronics and Power Engineering | — | 1 |
| 362 | IEEE International Conference on Computer Vision and Machine Intelligence (CVMI) | A* | 1 |
| 363 | IEEE International Conference on Computing, Communication and Automation (ICCCA) | — | 1 |
| 364 | IEEE International Conference on E-health Networking, Application & Services (HealthCom) | — | 1 |
| 365 | IEEE International Conference on Electrical Power and Energy Systems (ICEPES) | — | 1 |
| 366 | IEEE International Conference on Emerging Technologies and Factory Automation (ETFA) | — | 1 |
| 367 | IEEE International Conference on Intelligent Engineering Systems (INES) | — | 1 |
| 368 | IEEE International Conference on Mobile Ad-Hoc and Sensor Systems (MASS) | B | 1 |
| 369 | IEEE International Conference on Multimedia Big Data | — | 1 |
| 370 | IEEE International Conference on Networking, Architecture and Storage (NAS) | — | 1 |
| 371 | IEEE International Conference on Parallel and Distributed Systems (ICPADS) | B | 1 |
| 372 | IEEE International Conference on Power System Technology | — | 1 |
| 373 | IEEE International Conference on Signal and Image Processing Applications (ICSIPA) | — | 1 |
| 374 | IEEE International Conference on Software Architecture (ICSA) | A | 1 |
| 375 | IEEE International Conference on Software Architecture Companion (ICSA-C) | — | 1 |
| 376 | IEEE International Conference on Trust, Security and Privacy in Computing and Communications (TrustCom) | B | 1 |
| 377 | IEEE International Energy Conference (ENERGYCON) | — | 1 |
| 378 | IEEE International Instrumentation and Measurement Technology Conference | — | 1 |
| 379 | IEEE International Mediterranean Conference on Communications and Networking (MeditCom) | — | 1 |
| 380 | IEEE International New Circuits and Systems Conference (NEWCAS) | — | 1 |
| 381 | IEEE International Symposium on Antennas and Propagation and North American Radio Science Meeting (AP-S/URSI) | — | 1 |
| 382 | IEEE International Symposium on Defect and Fault Tolerance in VLSI and Nanotechnology Systems (DFT) | — | 1 |
| 383 | IEEE International Symposium on Diagnostics for Electrical Machines, Power Electronics and Drives (SDEMPED) | — | 1 |
| 384 | IEEE International Symposium on Network Computing and Applications (NCA) | B | 1 |
| 385 | IEEE International Symposium on Semiconductor Manufacturing conference proceedings | — | 1 |
| 386 | IEEE International Women in Engineering (WIE) Conference on Electrical and Computer Engineering (WIECON-ECE) | — | 1 |
| 387 | IEEE International Workshop on Antenna Technology (iWAT) | — | 1 |
| 388 | IEEE International Workshop on Signal Processing Advances in Wireless Communications (SPAWC) | — | 1 |
| 389 | IEEE Kansas Power and Energy Conference (KPEC) | — | 1 |
| 390 | IEEE Latin-American Conference on Communications | — | 1 |
| 391 | IEEE Nanotechnology Materials and Devices Conference (NMDC) | — | 1 |
| 392 | IEEE PES Innovative Smart Grid Technologies - Asia (ISGT Asia) | — | 1 |
| 393 | IEEE Power and Energy Society General Meeting (PESGM) | — | 1 |
| 394 | IEEE Silchar Subsection Conference (SILCON) | — | 1 |
| 395 | IEEE Students’ Technology Symposium | — | 1 |
| 396 | IEEE Transportation Electrification Conference & Expo (ITEC) | — | 1 |
| 397 | IEEE Transportation Electrification Conference (ITEC-India) | — | 1 |
| 398 | IEEE VLSI Device Circuit and System (VLSI DCS) | — | 1 |
| 399 | IEEE Winter Applications of Computer Vision Workshops (WACVW) | — | 1 |
| 400 | IEEE Wireless Communications and Networking Conference Workshops (WCNCW) | B | 1 |
| 401 | IEEE Wireless Power Technology Conference and Expo (WPTCE) | — | 1 |
| 402 | IEEE Workshop on Control and Modelling of Power Electronics (COMPEL) | — | 1 |
| 403 | IEEE Workshop on Recent Advances in Photonics (WRAP) | — | 1 |
| 404 | IEEE Workshop on Wide Bandgap Power Devices and Applications | — | 1 |
| 405 | IEEE-APS Topical Conference on Antennas and Propagation in Wireless Communications (APWC) | — | 1 |
| 406 | IEEE-EMBS International Conference on Biomedical and Health Informatics (BHI ...) | — | 1 |
| 407 | IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining (ASONAM) | B | 1 |
| 408 | IEEE/ASME International Conference on Advanced Intelligent Mechatronics | — | 1 |
| 409 | International Balkan Conference on Communications and Networking (BalkanCom) | — | 1 |
| 410 | International Conference Radioelektronika | — | 1 |
| 411 | International Conference for Advancement in Technology (ICONAT) | — | 1 |
| 412 | International Conference on AI-ML Systems (AIMLSystems) | — | 1 |
| 413 | International Conference on Advanced Communication Technologies and Networking (CommNet) | — | 1 |
| 414 | International Conference on Advanced Computing and Communication Systems (ICACCS) | — | 1 |
| 415 | International Conference on Advances in Computing, Communication and Applied Informatics (ACCAI) | — | 1 |
| 416 | International Conference on Advances in Computing, Communications and Informatics (ICACCI) | — | 1 |
| 417 | International Conference on Artificial Intelligence and Signal Processing (AISP) | — | 1 |
| 418 | International Conference on Bio-engineering for Smart Technologies (BioSMART) | — | 1 |
| 419 | International Conference on Bioinformatics and Systems Biology (BSB) | — | 1 |
| 420 | International Conference on Blockchain Computing and Applications (BCCA) | — | 1 |
| 421 | International Conference on Circuit, Power and Computing Technologies | — | 1 |
| 422 | International Conference on Circuits, Power and Intelligent Systems (CCPIS) | — | 1 |
| 423 | International Conference on Compilers, Architectures and Synthesis for Embedded Systems (CASES) | — | 1 |
| 424 | International Conference on Computation of Power, Energy, Information and Communication (ICCPEIC) | — | 1 |
| 425 | International Conference on Computational Intelligence and Communication Networks (CICN) | — | 1 |
| 426 | International Conference on Computational Intelligence and Communication Technologies (CCICT) | — | 1 |
| 427 | International Conference on Computational Performance Evaluation (ComPE) | — | 1 |
| 428 | International Conference on Computational Systems and Information Technology for Sustainable Solution (CSITSS) | — | 1 |
| 429 | International Conference on Computer and Information Technology (ICCIT) | — | 1 |
| 430 | International Conference on Control, Automation and Robotics (ICCAR) | — | 1 |
| 431 | International Conference on Control, Decision and Information Technologies (CoDIT) | C | 1 |
| 432 | International Conference on Data Science, Agents & Artificial Intelligence (ICDSAAI) | — | 1 |
| 433 | International Conference on Decision Aid Sciences and Applications (DASA) | — | 1 |
| 434 | International Conference on Electrical & Electronic Engineering (ICEEE) | — | 1 |
| 435 | International Conference on Electrical, Computer, Communications and Mechatronics Engineering (ICECCME) | — | 1 |
| 436 | International Conference on Electrical, Control and Instrumentation Engineering (ICECIE) | — | 1 |
| 437 | International Conference on Electronics, Materials Engineering & Nano-Technology (IEMENTech) | — | 1 |
| 438 | International Conference on Emerging Techniques in Computational Intelligence (ICETCI) | — | 1 |
| 439 | International Conference on Emerging Trends in Engineering and Technology (ICETET) | — | 1 |
| 440 | International Conference on Fracture Mechanics of Concrete and Concrete Structures (FraMCoS) | — | 1 |
| 441 | International Conference on Harmonics and Quality of Power | — | 1 |
| 442 | International Conference on Hot Information-Centric Networking (HotICN) | — | 1 |
| 443 | International Conference on Information Management & Machine Intelligence (ICIMMI) | — | 1 |
| 444 | International Conference on Information Networking | — | 1 |
| 445 | International Conference on Information Systems and Computer Networks (ISCON) | — | 1 |
| 446 | International Conference on Information and Communication Technology for Competitive Strategies (ICTCS) | — | 1 |
| 447 | International Conference on Infrared, Millimeter, and Terahertz Waves (IRMMW-THz) | — | 1 |
| 448 | International Conference on Instrumentation, Control, and Automation (ICA) | — | 1 |
| 449 | International Conference on Integration of Computational Intelligent System (ICICIS) | — | 1 |
| 450 | International Conference on Intelligent Controller and Computing for Smart Power (ICICCSP) | — | 1 |
| 451 | International Conference on Intelligent Engineering and Management (ICIEM) | — | 1 |
| 452 | International Conference on Intelligent System Application to Power Systems (ISAP) | — | 1 |
| 453 | International Conference on Intelligent Systems and Control | — | 1 |
| 454 | International Conference on Intelligent and Innovative Technologies in Computing, Electrical and Electronics (IITCEE) | — | 1 |
| 455 | International Conference on Inventive Research in Computing Applications (ICIRCA) | — | 1 |
| 456 | International Conference on Machine Learning Technologies (ICMLT) | A* | 1 |
| 457 | International Conference on Medical and Health Informatics (ICMHI) | — | 1 |
| 458 | International Conference on Microwave, Antenna and Communication (MAC) | — | 1 |
| 459 | International Conference on Nanoscience and Nanotechnology | — | 1 |
| 460 | International Conference on Next Generation Electronics (NELEX) | — | 1 |
| 461 | International Conference on Optical Fiber Sensors (OFS) | — | 1 |
| 462 | International Conference on Power Electronics and ECCE Asia (ICPE-ECCE Asia) | — | 1 |
| 463 | International Conference on Quarks and Nuclear Physics (QNP) | — | 1 |
| 464 | International Conference on Recent Innovations in Electrical, Electronics & Communication Engineering (ICRIEECE) | — | 1 |
| 465 | International Conference on Remote Sensing and Geoinformation of the Environment (RSCy) | — | 1 |
| 466 | International Conference on Renewable Energy Research and Applications (ICRERA) | — | 1 |
| 467 | International Conference on Robotics and Automation Sciences (ICRAS) | — | 1 |
| 468 | International Conference on Signal Processing and Communication Systems | — | 1 |
| 469 | International Conference on Signal Processing and Information Security (ICSPIS) | — | 1 |
| 470 | International Conference on Signal-Image Technology & Internet-Based Systems (SITIS) | — | 1 |
| 471 | International Conference on Simulation of Semiconductor Processes and Devices | — | 1 |
| 472 | International Conference on Software Defined Systems (SDS) | — | 1 |
| 473 | International Joint Conference on Natural Language Processing and Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics (IJCNLP-AACL) | A* | 1 |
| 474 | International Symposium on Computational and Business Intelligence (ISCBI) | — | 1 |
| 475 | International Symposium on Embedded Computing and System Design (ISED) | — | 1 |
| 476 | International Symposium on Information Theory and its Applications | C | 1 |
| 477 | International Symposium on Power Electronics, Electrical Drives, Automation and Motion (SPEEDAM) | — | 1 |
| 478 | International Symposium on Stochastic Models in Reliability Engineering, Life Science and Operations Management | — | 1 |
| 479 | International Symposium on VLSI Design, Automation and Test | — | 1 |
| 480 | International Telecommunications Conference (ITC-Egypt) | — | 1 |
| 481 | International Wireless Communications and Mobile Computing Conference (IWCMC) | B | 1 |
| 482 | International Workshop on Active-Matrix Flatpanel Displays and Devices | — | 1 |
| 483 | Irish Signals and Systems Conference | — | 1 |
| 484 | Joint International Conference on Data Science & Management of Data (CODS-COMAD) | — | 1 |
| 485 | Language Resources and Evaluation Conference (LREC) | B | 1 |
| 486 | Lecture notes in intelligent transportation and infrastructure | — | 1 |
| 487 | Lecture notes in social networks | — | 1 |
| 488 | Lecture notes on data engineering and communications technologies | — | 1 |
| 489 | NODYCON conference proceedings series | — | 1 |
| 490 | OCEANS 2022 - Chennai | — | 1 |
| 491 | OITS International Conference on Information Technology (OCIT) | — | 1 |
| 492 | OSA Advanced Photonics Congress | — | 1 |
| 493 | OSA Optical Sensors and Sensing Congress 2021 (AIS, FTS, HISE, SENSORS, ES) | — | 1 |
| 494 | Optica Advanced Photonics Congress | — | 1 |
| 495 | Optica Quantum 2.0 Conference and Exhibition | — | 1 |
| 496 | Optical Fiber Communication Conference | — | 1 |
| 497 | PanAm Unsaturated Soils 2017 | — | 1 |
| 498 | Picture Coding Symposium | — | 1 |
| 499 | Proceeding of Proceedings of CHT-17 ICHMT International Symposium on Advances in Computational Heat Transfer May 28-June 1, 2017, Napoli, Italy | — | 1 |
| 500 | Proceeding of Second Thermal and Fluids Engineering  Conference | — | 1 |
| 501 | Proceedings | — | 1 |
| 502 | Proceedings - IEEE International Symposium on Applications of Ferroelectrics/Proceedings of the ... IEEE International Symposium on Applications of Ferroelectrics | — | 1 |
| 503 | Proceedings - IEEE Symposium on Computers and Communications/IEEE Symposium on Computers and Communications | C | 1 |
| 504 | Proceedings - International Conference on Pattern Recognition/Proceedings/International Conference on Pattern Recognition | B | 1 |
| 505 | Proceedings IMCS 2018 | — | 1 |
| 506 | Proceedings of meetings on acoustics | — | 1 |
| 507 | Proceedings of the AAAI Conference on Artificial Intelligence | A* | 1 |
| 508 | Proceedings of the International AAAI Conference on Web and Social Media | A* | 1 |
| 509 | Proceedings of the International Ocean Discovery Program. Expedition reports | — | 1 |
| 510 | Proceedings/Proceedings - International Conference on Computer Communications and Networks | — | 1 |
| 511 | Proceedings/Proceedings - International Conference on Network Protocols | B | 1 |
| 512 | Proceedings/Proceedings - Symposium on Computer Arithmetic | — | 1 |
| 513 | Prognostics and System Health Management Conference | — | 1 |
| 514 | Rilem bookseries | — | 1 |
| 515 | Risk, reliability and safety engineering | — | 1 |
| 516 | SAE technical papers on CD-ROM/SAE technical paper series | — | 1 |
| 517 | SPIE Conference on Nonlinear Optics and its Applications | — | 1 |
| 518 | SPIE Future Sensing Technologies | — | 1 |
| 519 | SPIE Medical Imaging: Image Processing | — | 1 |
| 520 | SPIE Novel Patterning Technologies | — | 1 |
| 521 | Scientific School Dynamics of Complex Networks and their Applications (DCNA) | — | 1 |
| 522 | Sensor Signal Processing for Defence Conference (SSPD) | — | 1 |
| 523 | Springer aerospace technology | — | 1 |
| 524 | Springer proceedings in business and economics | — | 1 |
| 525 | Springer proceedings in earth and environmental sciences | — | 1 |
| 526 | TEQIP III Sponsored International Conference on Microwave Integrated Circuits, Photonics and Wireless Networks (IMICPW) | — | 1 |
| 527 | USNC-URSI Radio Science Meeting | — | 1 |
| 528 | Volume 2A: Advanced Manufacturing | — | 1 |
| 529 | Volume 2B: Advanced Manufacturing | — | 1 |
| 530 | Workshop on Hyperspectral Image and Signal Processing: Evolution in Remote Sensing | — | 1 |
| 531 | XV International Conference on Durability of Building Materials and Components. eBook of Proceedings | — | 1 |
| 532 | Zooming Innovation in Consumer Technologies Conference (ZINC) | — | 1 |
| 533 | The minerals, metals & materials series | — | 1 |

## 6. Indian partner institutions (863)

Institutions that appear as co-authors or citers in `indian_connections.csv` and the network files. Names and affiliations are taken from OpenAlex authorship data.

- ABB (India)
- Abasaheb Garware College
- Academy of Scientific and Innovative Research
- Acharya Institute of Technology
- Adamas University
- Adichunchanagiri University
- Aditya University
- Advanced Centre for Treatment, Research and Education in Cancer
- Advanced Materials and Processes Research Institute
- Advanced Systems Laboratory
- Aeronautical Development Establishment
- Agartala Government Medical College
- Agharkar Research Institute
- Ahmedabad University
- Akal University
- Alagappa University
- Aliah University
- Aligarh Muslim University
- All India Council for Technical Education
- All India Institute of Ayurveda, New Delhi
- All India Institute of Medical Sciences
- All India Institute of Medical Sciences Bhopal
- All India Institute of Medical Sciences Bhubaneswar
- All India Institute of Medical Sciences Bibinagar
- All India Institute of Medical Sciences Raipur
- All India Institute of Medical Sciences, Bilaspur
- All India Institute of Medical Sciences, Patna
- Ambedkar University Delhi
- American College, Madurai
- Amicable Knowledge Solution University
- Amity University
- Amity University Chhatisgarh
- Amity University Gurugram
- Amity University Jaipur
- Amity University Mumbai
- Amrita Institute of Medical Sciences and Research Centre
- Amrita Vishwa Vidyapeetham
- Anand Agricultural University
- Ananda Mohan College
- Andhra University
- Anil Neerukonda Institute of Technology & Sciences
- Anna University, Chennai
- Annasaheb Magar Mahavidyalaya, Hadapsar, Pune
- Armament Research and Development Establishment
- Army Institute of Technology, Pune
- Artemis Hospitals
- Arya Vaidya Sala
- Aryabhatta Research Institute of Observational Sciences
- Ashoka Trust for Research in Ecology and the Environment
- Ashoka University
- Assam Agricultural University
- Assam Down Town University
- Assam Science and Technology University
- Asutosh College
- Atal Bihari Vajpayee Indian Institute of Information Technology and Management
- Atal Bihari Vajpayee Institute of Medical Sciences and Dr. Ram Manohar Lohia Hospital
- B. V. Patel Pharmaceutical Education and Research Development Centre
- B.S. Abdur Rahman Crescent Institute of Science & Technology
- BLDE (Deemed to be University)
- BML Munjal University
- Babasaheb Bhimrao Ambedkar University
- Banaras Hindu University
- Banasthali University
- Bankura University
- Banwarilal Bhalotia College
- Barkatullah University
- Bengaluru City University
- Bennett University
- Berhampur University
- Bhabha Atomic Research Center Hospital
- Bhabha Atomic Research Centre
- Bharat Electronics (India)
- Bharat Forge (India)
- Bharat Heavy Electricals (India)
- Bharat Petroleum (India)
- Bharath University
- Bharathiar University
- Bharathidasan University
- Bharati Vidyapeeth (Deemed to be University)
- Bhartiya Skill Development University
- Bidhan Chandra Krishi Viswavidyalaya
- Bihar Engineering University
- Biju Patnaik University of Technology
- Binod Bihari Mahto Koyalanchal University
- Birbal Sahni Institute of Palaeosciences
- Birla Global University
- Birla Institute of Technology and Science - Hyderabad Campus
- Birla Institute of Technology and Science, Pilani
- Birla Institute of Technology and Science, Pilani - Goa Campus
- Birla Institute of Technology, Mesra
- Bishop Heber College
- Bombay Natural History Society
- Bose Institute
- Brainware University
- Bundelkhand University
- CMR University
- COEP Technological University
- CSIR National Physical Laboratory of India
- CUTS International
- Career Point University
- Center for Excellence in Basic Sciences
- Center for Study of Science Technology and Policy
- Central Agricultural University
- Central Arid Zone Research Institute
- Central Avian Research Institute
- Central Building Research Institute
- Central Council for Research in Ayurvedic Science
- Central Drug Research Institute
- Central Electrochemical Research Institute
- Central Electronics Engineering Research Institute
- Central Food Technological Research Institute
- Central Forensic Science Laboratory
- Central Glass and Ceramic Research Institute
- Central Ground Water Board
- Central Institute for Cotton Research
- Central Institute of Agricultural Engineering
- Central Institute of Medicinal and Aromatic Plants
- Central Institute of Mining and Fuel Research
- Central Institute of Plastics Engineering and Technology
- Central Leather Research Institute
- Central Marine Fisheries Research Institute
- Central Mechanical Engineering Research Institute
- Central Pollution Control Board
- Central Potato Research Institute
- Central Power Research Institute
- Central Rice Research Institute
- Central Road Research Institute
- Central Salt and Marine Chemicals Research Institute
- Central Scientific Instruments Organisation
- Central University of Gujarat
- Central University of Haryana
- Central University of Himachal Pradesh
- Central University of Jammu
- Central University of Jharkhand
- Central University of Karnataka
- Central University of Kerala
- Central University of Odisha
- Central University of Punjab
- Central University of Rajasthan
- Central University of South Bihar
- Central University of Tamil Nadu
- Centre For Development Studies
- Centre for Artificial Intelligence and Robotics
- Centre for Cellular and Molecular Biology
- Centre for Development Economics
- Centre for Development of Advanced Computing
- Centre for Development of Telematics
- Centre for Economic and Social Studies
- Centre for Fire, Explosive and Environment Safety
- Centre for Incubation, Innovation, Research and Consultancy
- Centre for Materials for Electronics Technology
- Centre of Biomedical Research
- Centurion University of Technology and Management
- Chaitanya Bharathi Institute of Technology
- Chandigarh University
- Charotar University of Science and Technology
- Chaudhary Charan Singh Haryana Agricultural University
- Chaudhary Charan Singh University
- Chaudhary Ranbir Singh University
- Chhatrapati Shahu Ji Maharaj University
- Chhattisgarh Swami Vivekanand Technical University
- Chilika Development Authority
- Chirayu Medical College & Hospital
- Chitkara University
- Chittaranjan National Cancer Institute
- Choithram Hospital and Research Centre
- Christ University
- Christian Medical College
- Christian Medical College, Vellore
- Cluster University Srinagar
- Cochin University of Science and Technology
- Cotton University
- Council of Scientific and Industrial Research
- D Y Patil International University
- D. Y. Patil Agriculture and Technical University
- D.A.V. College Chandigarh
- D.Y. Patil University
- DAV University
- Datta Meghe Institute of Higher Education and Research
- Dayalbagh Educational Institute
- Dayanand Medical College & Hospital
- Dayananda Sagar University
- Deen Dayal Upadhyaya Gorakhpur University
- Deenbandhu Chhotu Ram University of Science and Technology
- Defence Institute of Advanced Technology
- Defence Institute of High Altitude Research
- Defence Laboratory Jodhpur
- Defence Metallurgical Research Laboratory
- Defence Research and Development Establishment
- Defence Research and Development Laboratory
- Defence Research and Development Organisation
- Defence Terrain Research Laboratory
- Dehradun Institute of Technology University
- Delhi Technological University
- Department of Agriculture & Co-operation
- Department of Atomic Energy
- Department of Public
- Department of Science and Technology
- Department of Space
- Devi Ahilya Vishwavidyalaya
- Dhirubhai Ambani University
- Diamond Harbour Women's University
- Dibrugarh University
- Doon University
- Dr. A.P.J. Abdul Kalam Technical University
- Dr. B. R. Ambedkar National Institute of Technology Jalandhar
- Dr. B.C. Roy Engineering College
- Dr. B.R. Ambedkar State Institute of Medical Sciences
- Dr. Babasaheb Ambedkar Marathwada University
- Dr. Babasaheb Ambedkar Technological University
- Dr. D.Y. Patil Vidyapeeth, Pune
- Dr. Daulatrao Aher College of Engineering
- Dr. Hari Singh Gour University
- Dr. Homi Bhabha State University
- Dr. Rajendra Prasad Central Agriculture University
- Dr. Ram Manohar Lohia Avadh University
- Dr. Yashwant Singh Parmar University of Horticulture and Forestry
- Electronics Corporation of India
- Electronics and Radar Development Establishment
- Energy and Resources Institute
- Engineering Staff College of India
- Entrepreneurship Development Institute of India
- Fakir Mohan University
- Fergusson College
- Foundation for Innovation and Technology Transfer
- G.B. Pant Institute of Himalayan Environment and Development
- G.L. Bajaj Institute of Technology and Management Greater Noida
- GD Goenka University
- GITAM University
- GLA University
- Galgotias University
- Gandhi Institute for Technological Advancement
- Gandhigram Rural Institute
- Ganpat University
- Gati Shakti Vishwavidyalaya
- Gauhati Medical College and Hospital
- Gauhati University
- Gautam Buddha University
- Gayatri Vidya Parishad College of Engineering for Women
- General Electric (India)
- Geological Survey of India
- Glocal University
- Gnanamani College of Technology
- Goa University
- Goalpara College
- Gokhale Institute of Politics and Economics
- Government of Andhra Pradesh
- Government of Haryana
- Government of Himachal Pradesh
- Government of India
- Government of Karnataka
- Government of Kerala
- Government of Maharashtra
- Government of Sikkim
- Government of Tamil Nadu
- Government of Uttar Pradesh
- Government of West Bengal
- Govind Ballabh Pant University of Agriculture and Technology
- Graphic Era University
- Gujarat Biotechnology Research Centre
- Gujarat Technological University
- Gujarat University
- Guru Angad Dev Veterinary and Animal Sciences University
- Guru Ghasidas Vishwavidyalaya
- Guru Gobind Singh Indraprastha University
- Guru Jambheshwar University Moradabad
- Guru Jambheshwar University of Science and Technology
- Guru Kashi University
- Guru Nanak Dev University
- Guru Nanak Institutions
- Gurugram University
- Gurukul Kangri Vishwavidyalaya
- Gyan Vihar University
- HCL Technologies (India)
- Haldia Institute of Technology
- Harcourt Butler Technical University
- Harish-Chandra Research Institute
- Healthcare Technology Innovation Centre
- Hemwati Nandan Bahuguna Garhwal University
- Heritage Institute of Technology
- Hi-Tech Medical College & Hospital
- Himachal Pradesh University
- Hindustan Aeronautics Limited (India)
- Hindustan Institute of Technology and Science
- Homi Bhabha National Institute
- IBM (India)
- ICAR Research Complex for NEH Region
- ICAR-Indian Institute of Farming Systems Research
- ICFAI Foundation for Higher Education
- ICFAI University, Tripura
- IILM Institute for Higher Education
- IITB-Monash Research Academy
- IMS Ghaziabad
- IPS Academy
- ISRO Propulsion Complex
- Index Medical College, Hospital & Research Centre
- India Meteorological Department
- Indian Agricultural Research Institute
- Indian Agricultural Statistics Research Institute
- Indian Association for the Cultivation of Science
- Indian Council for Research on International Economic Relations
- Indian Council of Agricultural Research
- Indian Council of Forestry Research and Education
- Indian Council of Medical Research
- Indian Institute of Astrophysics
- Indian Institute of Chemical Biology
- Indian Institute of Chemical Technology
- Indian Institute of Engineering Science and Technology, Shibpur
- Indian Institute of Foreign Trade
- Indian Institute of Forest Management
- Indian Institute of Geomagnetism
- Indian Institute of Information Technology Allahabad
- Indian Institute of Information Technology Bhopal
- Indian Institute of Information Technology Design and Manufacturing Jabalpur
- Indian Institute of Information Technology Guwahati
- Indian Institute of Information Technology Kalyani
- Indian Institute of Information Technology Kota
- Indian Institute of Information Technology Lucknow
- Indian Institute of Information Technology Ranchi
- Indian Institute of Information Technology Surat
- Indian Institute of Information Technology Una
- Indian Institute of Information Technology Vadodara
- Indian Institute of Information Technology and Management, Kerala
- Indian Institute of Information Technology, Design and Manufacturing, Kancheepuram
- Indian Institute of Information Technology, Nagpur
- Indian Institute of Information Technology, Pune
- Indian Institute of Information Technology, Sonepat
- Indian Institute of Integrative Medicine
- Indian Institute of Management Ahmedabad
- Indian Institute of Management Amritsar
- Indian Institute of Management Calcutta
- Indian Institute of Management Indore
- Indian Institute of Management Jammu
- Indian Institute of Management Lucknow
- Indian Institute of Management Mumbai
- Indian Institute of Management Raipur
- Indian Institute of Management Ranchi
- Indian Institute of Management Rohtak
- Indian Institute of Petroleum
- Indian Institute of Petroleum and Energy
- Indian Institute of Remote Sensing
- Indian Institute of Science Bangalore
- Indian Institute of Science Education and Research Berhampur
- Indian Institute of Science Education and Research Kolkata
- Indian Institute of Science Education and Research Mohali
- Indian Institute of Science Education and Research Pune
- Indian Institute of Science Education and Research Thiruvananthapuram
- Indian Institute of Science Education and Research, Bhopal
- Indian Institute of Science Education and Research, Tirupati
- Indian Institute of Soil Science
- Indian Institute of Soybean Research
- Indian Institute of Space Science and Technology
- Indian Institute of Technology BHU
- Indian Institute of Technology Bhilai
- Indian Institute of Technology Bhubaneswar
- Indian Institute of Technology Bombay
- Indian Institute of Technology Delhi
- Indian Institute of Technology Dhanbad
- Indian Institute of Technology Dharwad
- Indian Institute of Technology Gandhinagar
- Indian Institute of Technology Goa
- Indian Institute of Technology Guwahati
- Indian Institute of Technology Hyderabad
- Indian Institute of Technology Indore
- Indian Institute of Technology Jammu
- Indian Institute of Technology Jodhpur
- Indian Institute of Technology Kanpur
- Indian Institute of Technology Kharagpur
- Indian Institute of Technology Madras
- Indian Institute of Technology Mandi
- Indian Institute of Technology Palakkad
- Indian Institute of Technology Patna
- Indian Institute of Technology Roorkee
- Indian Institute of Technology Ropar
- Indian Institute of Technology Tirupati
- Indian Institute of Toxicology Research
- Indian Institute of Tropical Meteorology
- Indian Institute of Vegetable Research
- Indian National Centre for Ocean Information Services
- Indian Oil Corporation (India)
- Indian Space Research Organisation
- Indian Statistical Institute
- Indian Statistical Institute, Bangalore Centre
- Indian Statistical Institute, Delhi Centre
- Indira Gandhi Centre for Atomic Research
- Indira Gandhi Delhi Technical University for Women
- Indira Gandhi Institute of Technology
- Indira Gandhi Medical College
- Indira Gandhi National Tribal University
- Indira Gandhi University, Meerpur
- Indo Korea Science and Technology
- Indraprastha Institute of Information Technology Delhi
- Indrashil University
- Institute for Development and Research in Banking Technology
- Institute for Plasma Research
- Institute for Social and Economic Change
- Institute for Stem Cell Biology and Regenerative Medicine
- Institute of Advanced Study in Science and Technology
- Institute of Astronomy Space and Earth Science
- Institute of Bioinformatics and Applied Biotechnology
- Institute of Chemical Technology
- Institute of Economic Growth
- Institute of Engineering & Technology
- Institute of Genomics and Integrative Biology
- Institute of Himalayan Bioresource Technology
- Institute of Infrastructure Technology Research and Management
- Institute of Life Sciences
- Institute of Liver and Biliary Sciences
- Institute of Mathematical Sciences
- Institute of Medical Sciences
- Institute of Medical Sciences and Sum Hospital
- Institute of Microbial Technology
- Institute of Minerals and Materials Technology
- Institute of Molecular Medicine
- Institute of Nuclear Medicine & Allied Sciences
- Institute of Physics, Bhubaneshwar
- Institute of Post Graduate Medical Education and Research
- Institute of Rural Management Anand
- Instruments Research & Development Establishment
- Intas Pharmaceuticals (India)
- Integral University
- Integrated Test Range
- Intel (India)
- Inter-University Accelerator Centre
- Inter-University Centre for Astronomy and Astrophysics
- International Advanced Research Centre for Powder Metallurgy and New Materials
- International Centre for Genetic Engineering and Biotechnology
- International Centre for Theoretical Sciences
- International Institute for Population Sciences
- International Institute of Information Technology
- International Institute of Information Technology Bangalore
- International Institute of Information Technology, Hyderabad
- International Management Institute
- Invertis University
- Islamic University of Science and Technology
- Islamic University of Science and Technology, Kashmir
- Ispat General Hospital
- J.C. Bose University of Science & Technology, YMCA
- JECRC University
- JIS University
- JK Lakshmipat University
- JSPM University
- Jabalpur Engineering College
- Jadavpur University
- Jai Prakash University
- Jain University
- Jaipur National University
- Jamalpur Mahavidyalaya
- Jamia Hamdard
- Jamia Millia Islamia
- Jawaharlal Nehru Centre for Advanced Scientific Research
- Jawaharlal Nehru Technological University Anantapur
- Jawaharlal Nehru Technological University, Hyderabad
- Jawaharlal Nehru Technological University, Kakinada
- Jawaharlal Nehru University
- Jaypee Institute of Information Technology
- Jaypee University Anoopshahr
- Jaypee University of Engineering and Technology, Guna
- Jaypee University of Information Technology
- Jhargram Raj College
- Jiwaji University
- KCG College of Technology
- KIIT University
- KLE Academy of Higher Education and Research
- KLE Technological University
- KPR Institute of Engineering and Technology
- KR Mangalam University
- Kakatiya University
- Kalasalingam Academy of Research and Education
- Kalinga Institute of Social Sciences
- Kalpavriksh
- Kameshwar Singh Darbhanga Sanskrit University
- Kamla Nehru Institute of Technology
- Kannur University
- Karmaveer Bhaurao Patil University, Satara
- Karnatak University
- Karnataka State Open University
- Karpagam Academy of Higher Education
- Kashi Naresh Government Post Graduate College
- Kasturba Medical College Hospital
- Kasturba Medical College, Manipal
- Kavayitri Bahinabai Chaudhari North Maharashtra University
- Kerala Agricultural University
- Kerala University of Digital Sciences, Innovation and Technology
- Khallikote Unitary University
- King Edward Memorial Hospital Research Centre
- King George's Medical University
- Koneru Lakshmaiah Education Foundation
- Krantiguru Shyamji Krishna Verma Kachchh University
- Krishna University
- Kumaun University
- Kurukshetra University
- L V Prasad Eye Institute
- LG (India)
- LNM Institute of Information Technology
- Lalit Narayan Mithila University
- Larsen & Toubro (India)
- Lovely Professional University
- M S Ramaiah University of Applied Sciences
- M.J.P. Rohilkhand University
- MIT Art, Design and Technology University
- MIT World Peace University
- Madan Mohan Malaviya University of Technology
- Madurai Kamaraj University
- Magadh University
- Maharaja Ranjit Singh Punjab Technical University
- Maharaja Sayajirao University of Baroda
- Maharaja Sriram Chandra Bhanja Deo University
- Maharaja Surajmal Institute of Technology
- Maharaja Yeshwantrao Hospital
- Maharana Pratap Horticultural University, Karnal
- Maharana Pratap University of Agriculture and Technology
- Maharishi Markandeshwar University, Mullana
- Maharshi Dayanand University
- Mahatma Gandhi Memorial Medical College
- Mahatma Gandhi University
- Mahaveer University
- Mahindra Group (India)
- Mahindra University
- Malaviya National Institute of Technology Jaipur
- Malla Reddy University
- Manav Rachna International Institute of Research and Studies
- Mandsaur University
- Mangalayatan University
- Manipal Academy of Higher Education
- Manipal Centre for Natural Sciences
- Marathwada Mitra Mandal's College of Engineering
- Marwari College, Darbhanga
- Maulana Azad National Institute of Technology
- Maulana Azad National Urdu University
- Medi-Caps University
- Medical College and Hospital, Kolkata
- Medtronic (India)
- Meerut College
- Meghnad Saha Institute of Technology
- Melmaruvathur Adhiparasakthi Institute of Medical Sciences and Research
- Mepco Schlenk Engineering College
- Microsoft (India)
- Midnapore Medical College and Hospital
- Ministry of AYUSH
- Ministry of Agriculture & Farmers Welfare
- Ministry of Defence
- Ministry of Earth Sciences
- Ministry of Electronics and Information Technology
- Ministry of Home Affairs
- Ministry of Railways
- Ministry of Science and Technology
- Mizoram University
- Mody University of Science and Technology
- Mohan Babu University
- Mohanlal Sukhadia University
- Motilal Nehru National Institute of Technology
- Munger University
- Murshidabad University
- NIMS University
- Nagaland University
- Nalanda Open University
- Nalanda University
- Nanaji Deshmukh Veterinary Science University
- Narsee Monjee Institute of Management Studies
- National AIDS Research Institute
- National Aerospace Laboratories
- National Atmospheric Research Laboratory
- National Brain Research Centre
- National Bureau of Agriculturally Important Microorganisms
- National Centre for Biological Sciences
- National Centre for Cell Science
- National Centre for Medium Range Weather Forecasting
- National Centre for Polar and Ocean Research
- National Centre for Radio Astrophysics
- National Chemical Laboratory
- National Council Of Educational Research And Training
- National Council of Applied Economic Research
- National Environmental Engineering Research Institute
- National Geophysical Research Institute
- National Institute Of Technology Silchar
- National Institute Of Veterinary Epidemiology And Disease Informatics
- National Institute for Implementation Research on Non-Communicable Diseases
- National Institute for Interdisciplinary Science and Technology
- National Institute of Animal Biotechnology
- National Institute of Construction Management and Research
- National Institute of Disaster Management
- National Institute of Food Technology Entrepreneurship and Management
- National Institute of Hydrology
- National Institute of Immunology
- National Institute of Malaria Research
- National Institute of Mental Health and Neurosciences
- National Institute of Ocean Technology
- National Institute of Pathology
- National Institute of Pharmaceutical Education and Research
- National Institute of Pharmaceutical Education and Research - Ahmedabad
- National Institute of Plant Genome Research
- National Institute of Public Finance and Policy
- National Institute of Science Education and Research
- National Institute of Science and Technology
- National Institute of Solar Energy
- National Institute of Technical Teachers Training and Research, Chandigarh
- National Institute of Technical Teachers’ Training and Research
- National Institute of Technology Agartala
- National Institute of Technology Andhra Pradesh
- National Institute of Technology Arunachal Pradesh
- National Institute of Technology Calicut
- National Institute of Technology Delhi
- National Institute of Technology Durgapur
- National Institute of Technology Goa
- National Institute of Technology Jamshedpur
- National Institute of Technology Karnataka
- National Institute of Technology Kurukshetra
- National Institute of Technology Meghalaya
- National Institute of Technology Nagaland
- National Institute of Technology Patna
- National Institute of Technology Raipur
- National Institute of Technology Rourkela
- National Institute of Technology Sikkim
- National Institute of Technology Srinagar
- National Institute of Technology Tiruchirappalli
- National Institute of Technology Warangal
- National Institute of Urban Affairs
- National Institution for Transforming India Aayog
- National JALMA Institute for Leprosy & Other Mycobacterial Diseases
- National Metallurgical Laboratory
- National Power Training Institute
- National Remote Sensing Centre
- National Research Centre for Grapes
- National Research Centre on Seed Spices
- Naval Materials Research Laboratory
- Netaji Subhas University
- Netaji Subhas University of Technology
- New Alipore College
- New Horizon College of Engineering
- Nirma University
- Nitte Meenakshi Institute of Technology
- Nizam's Institute of Medical Sciences
- Noida Institute of Engineering and Technology
- Noida International University
- North Bengal University
- North East Institute of Science and Technology
- North Eastern Hill University
- North Eastern Regional Institute of Science and Technology
- North Eastern Space Applications Centre
- O. P. Jindal Global University
- Odisha University of Agriculture and Technology
- Osmania University
- PES University
- PSG College of Arts & Science
- PSG College of Pharmacy
- PSG College of Technology
- Pandit Bhagwat Dayal Sharma Post Graduate Institute of Medical Sciences
- Pandit Deendayal Energy University
- Pandit Ravishankar Shukla University
- Panjab University
- Parala Maharaja Engineering College
- Patliputra University
- Patna University
- Periyar University
- Physical Research Laboratory
- Pondicherry University
- Poornima University
- Post Graduate Institute of Medical Education and Research
- Prananath College (Autonomous)
- Premium Serums & Vaccines Pvt. Ltd. (India)
- Presidency University
- Proof & Experimental Establishment
- Punjab Agricultural University
- Punjab Engineering College
- Punjab Remote Sensing Centre
- Punjab Technical University
- Qure.ai Technologies Private Limited (India)
- REVA University
- RK University
- RV University
- Raiganj University
- Raja Ramanna Centre for Advanced Technology
- Rajah Serfoji Government College (Autonomous)
- Rajiv Gandhi Centre for Biotechnology
- Rajiv Gandhi Institute of Petroleum Technology
- Rajiv Gandhi National Aviation University
- Rajiv Gandhi Technical University
- Rajkiya Engineering College Kannauj
- Rajkiya Engineering College Mainpuri
- Rama University
- Ramaiah Institute of Technology
- Ramakrishna Mission Residential College
- Ramakrishna Mission Vidyamandira
- Ramakrishna Mission Vivekananda Centenary College
- Raman Research Institute
- Rani Durgavati University
- Rani Lakshmi Bai Central Agricultural University, Jhansi
- Rashtrasant Tukadoji Maharaj Nagpur University
- Rashtriya Raksha University
- Rathinam College of Arts & Science
- Ravenshaw University
- Rayat Bahra University
- Regional Centre for Biotechnology
- Regional Institute of Education, Bhubaneswar
- Regional Medical Research Center
- Reliance Industries (India)
- Research & Development Establishment (Engrs.)
- Research Centre Imarat
- Robert Bosch (India)
- Rungta College of Engineering and Technology
- S.N. Bose National Centre for Basic Sciences
- SASTRA University
- SR University
- SRM Institute of Science and Technology
- SRM University
- SRM University, Andhra Pradesh
- STMicroelectronics (India)
- Sacred Heart College (Autonomous)
- Safdarjang Hospital
- Saha Institute of Nuclear Physics
- Sam Higginbottom Institute of Agriculture
- Sambalpur University
- Sambalpur University Institute of Information Technology
- Samsung (India)
- Sandip Institute of Technology & Research Centre
- Sanjay Gandhi Post Graduate Institute of Medical Sciences
- Sant Longowal Institute of Engineering and Technology
- Sardar Patel University
- Sardar Patel University Mandi
- Sardar Vallabhbhai National Institute of Technology Surat
- Sarojini Naidu Medical College
- Sathyabama Institute of Science and Technology
- Saveetha University
- Savitribai Phule Pune University
- Scientific Analysis Group
- Sharda University
- Sher-e-Kashmir University of Agricultural Sciences and Technology of Kashmir
- Sher-i-Kashmir Institute of Medical Sciences
- Shiv Nadar University
- Shiv Nadar University, Chennai
- Shivaji University
- Shoolini University
- Shree Guru Gobind Singh Tricentenary University
- Shri BM Patil Medical College
- Shri Govindram Seksaria Institute of Technology and Science
- Shri Jagdishprasad Jhabarmal Tibrewala University
- Shri Mata Vaishno Devi University
- Shri Neelkantheshwar Government Post-Graduate College
- Shri Ramswaroop Memorial University
- Shri Shikshayatan College
- Shri Vaishnav Vidyapeeth Vishwavidyalaya, Indore
- Shri Vile Parle Kelavani Mandal
- Shri Vishwakarma Skill University
- Shri Yashwantrao Patil Science College, Solankur
- Siddaganga Institute of Technology
- Siddhartha Academy of Higher Education
- Sidho-Kanho-Birsha University
- Sikkim Manipal University
- Sikkim University
- Siksha O Anusandhan University
- Silchar Medical College and Hospital
- Sister Nivedita University
- Sitamarhi Institute of Technology
- Snow & Avalanche Study Estt
- Soban Singh Jeena University
- Solapur University
- Solid State Physics Laboratory
- Somaiya Vidyavihar University
- South Asian University
- Space Applications Centre
- Sree Sankaracharya University of Sanskrit
- Sri Aurobindo Institute of Medical Sciences
- Sri Balaji University, Pune
- Sri Guru Granth Sahib World University
- Sri Pratap College
- Sri Sathya Sai Institute of Higher Learning
- Sri Sivasubramaniya Nadar College of Engineering
- Sri Sri University
- Sri Venkateswara Institute of Medical Sciences
- Sri Venkateswara University
- Sriram Chandra Bhanja Medical College Hospital
- Srushti Conservation Foundation
- St Joseph's University, Bengaluru, India
- St. Stephen's College
- St. Xavier's College (Autonomous), Kolkata
- Structural Engineering Research Centre
- Swami Rama Himalayan University
- Swami Vivekanand College of Pharmacy
- Symbiosis International University
- Symbiosis University of Applied Sciences
- Syneos Health (India)
- TCG Crest
- TERI University
- TIFR Centre for Interdisciplinary Sciences
- Tagore Centre for Natural Sciences and Philosophy
- Tamil Nadu Agricultural University
- Tata Consultancy Services (India)
- Tata Institute for Genetics and Society
- Tata Institute of Fundamental Research
- Tata Institute of Social Sciences
- Tata Memorial Hospital
- Tata Steel (India)
- Techno India University
- Teerthanker Mahaveer University
- Tehatta Sadananda Mahavidyalaya
- Terminal Ballistics Research Laboratory
- Tezpur University
- Thapar Institute of Engineering & Technology
- The Madura College
- The NorthCap University
- Tilka Manjhi Bhagalpur University
- Translational Health Science and Technology Institute
- Trident Academy of Technology
- Tropical Forest Research Institute
- U. R. Rao Satellite Centre
- UGC DAE Consortium for Scientific Research
- UGC-DAE Consortium for Scientific Research, Mumbai Centre
- Udaipur Solar Observatory
- University Grants Commission
- University of Agricultural Sciences, Bangalore
- University of Agricultural Sciences, Dharwad
- University of Allahabad
- University of Burdwan
- University of Calcutta
- University of Calicut
- University of Delhi
- University of Engineering & Management
- University of Gour Banga
- University of Hyderabad
- University of Jammu
- University of Kalyani
- University of Kashmir
- University of Kerala
- University of Kota
- University of Lucknow
- University of Madras
- University of Mumbai
- University of Mysore
- University of Petroleum and Energy Studies
- University of Rajasthan
- Utkal University
- Uttarakhand State Council for Science and Technology
- Uttarakhand Technical University
- Uttaranchal University
- VIT Bhopal University
- Vardhman Mahavir Medical College & Safdarjung Hospital
- Variable Energy Cyclotron Centre
- Veer Chandra Singh Garhwali Uttarakhand University of Horticulture & Forestry
- Veer Surendra Sai University of Technology
- Vel Tech Rangarajan Dr. Sagunthala R&D Institute of Science and Technology
- Vellore Institute of Technology University
- Vels University
- Vidyasagar University
- Vignan's Foundation for Science, Technology & Research
- Vikram Sarabhai Space Centre
- Vikramajit Singh Sanatan Dharma College
- Visva-Bharati University
- Visvesvaraya National Institute of Technology
- Visvesvaraya Technological University
- Vivekananda Global University
- Vivekananda Institute of Professional Studies
- WWF-India
- Wadia Institute of Himalayan Geology
- West Bengal State University
- West Bengal University of Animal and Fishery Sciences
- Women's Christian College
- Woxsen School of Business
- XIM University
- Yenepoya Research Centre
- Yenepoya University
- Yogi Vemana University
- Zoological Survey of India
