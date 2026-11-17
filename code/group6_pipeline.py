#!/usr/bin/env python3
"""
DPCN Research Mapping Project - Group 6 (IIT Cluster)
IIT Bhubaneswar · IIT Indore · IIT Mandi · 2016-2026

One script that produces every Week 1-2 deliverable plus the dashboard:

  out/group6_data.csv            main dataset (one row per paper x institutional author)
  out/citation_network.csv       directed edges: paper A cites paper B
  out/authorship_network.csv     undirected co-authorship edges
  out/indian_connections.csv     aggregated cross-institute links
  out/paper_metrics.csv          in-degree + PageRank per paper (citation network)
  out/author_metrics.csv         degree / betweenness / Louvain community per author
  out/faculty_summary.csv        faculty-level table (papers, citations, h-index, top journal)
  out/group6_dashboard.html      interactive dashboard with all data embedded

Usage
-----
  pip install requests pandas networkx
  export OPENALEX_API_KEY=...        # free key from openalex.org (strongly recommended)
  python group6_pipeline.py

Optional inputs (put next to this script):
  faculty_list.csv   columns: name,institution,department
                     -> restricts "faculty" to these people and uses their departments.
                     institution must be one of: IIT Bhubaneswar / IIT Indore / IIT Mandi
  scimagojr.csv      Scimago journal ranking export (scimagojr.com -> Journal Rankings -> Download data)
                     -> journal quartiles. The script tries to download it automatically.
  core_ranks.csv     CORE conference ranking export (portal.core.edu.au -> Export)
                     -> CORE A*/A/B/C for conference papers. Also tried automatically.

All API responses are cached in ./cache, so you can stop and re-run at any time without
re-spending API credits.
"""

import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import networkx as nx
import pandas as pd
import requests

# --------------------------------------------------------------------------- config
GROUP = 6
CLUSTER = "IIT Cluster"
YEAR_FROM, YEAR_TO = 2016, 2026

# Verified against OpenAlex / ROR
INSTITUTIONS = {
    "I99729588": {"name": "IIT Bhubaneswar", "ror": "https://ror.org/04gx72j20", "state": "Odisha"},
    "I64295750": {"name": "IIT Indore", "ror": "https://ror.org/01hhf7w52", "state": "Madhya Pradesh"},
    "I9579091": {"name": "IIT Mandi", "ror": "https://ror.org/05r9r2f34", "state": "Himachal Pradesh"},
}
INST_BY_NAME = {v["name"]: k for k, v in INSTITUTIONS.items()}

API = "https://api.openalex.org"
BATCH = 100                      # OpenAlex: max 100 OR-values per filter, max 100 per page
MAX_AUTHORS_FOR_COAUTH = 50      # above this, only pairs among Group 6 authors are kept (mega-collaborations)
MIN_PAPERS_FACULTY = 5           # heuristic when no faculty_list.csv: >= N papers at the institute
TOP_PARTNERS_FOR_JACCARD = None  # None = every partner institution; set e.g. 25 to save API calls
VIZ_MAX_NODES = 300              # nodes shipped to the dashboard network panels
WORKERS = 8                      # parallel API requests (OpenAlex allows up to 100/s with a key)

HERE = Path(__file__).resolve().parent


def log(*a):
    print(time.strftime("[%H:%M:%S]"), *a, flush=True)


# --------------------------------------------------------------------------- API client
class BadRequest(RuntimeError):
    pass


class OpenAlex:
    def __init__(self, cache_dir, api_key=None, mailto=None, offline=False):
        self.cache = Path(cache_dir)
        self.cache.mkdir(parents=True, exist_ok=True)
        self.api_key = api_key
        self.mailto = mailto
        self.offline = offline
        self.calls = 0
        self.hits = 0
        self._local = threading.local()
        self._lock = threading.Lock()
        self.workers = WORKERS

    @property
    def s(self):
        if not hasattr(self._local, "s"):
            self._local.s = requests.Session()
        return self._local.s

    def pmap(self, fn, items, label=""):
        """Run fn over items with a thread pool, logging progress."""
        items = list(items)
        out, done = [None] * len(items), 0
        step = max(1, len(items) // 10)
        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            futs = {ex.submit(fn, it): i for i, it in enumerate(items)}
            for fut in futs:
                out[futs[fut]] = fut.result()
                done += 1
                if label and (done % step == 0 or done == len(items)):
                    log(f"  {label}: {done}/{len(items)}")
        return out

    def _key(self, path, params):
        raw = path + "?" + "&".join(f"{k}={params[k]}" for k in sorted(params))
        return hashlib.sha1(raw.encode()).hexdigest()

    def get(self, path, params):
        params = {k: v for k, v in params.items() if v is not None}
        f = self.cache / (self._key(path, params) + ".json")
        if f.exists():
            with self._lock:
                self.hits += 1
            return json.loads(f.read_text())
        if os.environ.get("G6_COLLECT"):
            # record the missing request for an external fetcher and continue with an empty answer
            with self._lock:
                with open(os.environ["G6_COLLECT"], "a") as fh:
                    fh.write(json.dumps({"path": path, "params": params}) + "\n")
            return {"results": [], "meta": {"count": 0, "next_cursor": None}, "group_by": []}
        if self.offline:
            raise RuntimeError(f"offline and not cached: {path} {params}")
        q = dict(params)
        if self.api_key:
            q["api_key"] = self.api_key
        if self.mailto:
            q["mailto"] = self.mailto
        for attempt in range(8):
            try:
                r = self.s.get(API + path, params=q, timeout=60)
            except requests.RequestException as e:
                wait = 2 ** attempt
                log(f"network error {e!r}; retry in {wait}s")
                time.sleep(wait)
                continue
            if r.status_code == 200:
                with self._lock:
                    self.calls += 1
                data = r.json()
                tmp = f.with_suffix(f".{threading.get_ident()}.tmp")
                tmp.write_text(json.dumps(data))
                tmp.replace(f)
                return data
            if r.status_code == 429:
                if attempt >= 5:
                    sys.exit("\nOpenAlex keeps returning HTTP 429 - the daily budget is probably used up. "
                             "Everything fetched so far is cached: re-run tomorrow (or with an API key) and it "
                             "resumes where it stopped.\n" + r.text[:300])
                wait = 2 ** attempt
                log(f"429 rate-limited; retry in {wait}s")
                time.sleep(wait)
                continue
            if r.status_code >= 500:
                time.sleep(2 ** attempt)
                continue
            if r.status_code == 400:
                raise BadRequest(f"OpenAlex 400: {r.url.split('api_key')[0]}\n{r.text[:300]}")
            raise RuntimeError(f"OpenAlex {r.status_code}: {r.url.split('api_key')[0]}\n{r.text[:500]}")
        raise RuntimeError(f"giving up on {path} {params}")

    def paginate(self, path, filt, select=None, label=""):
        out, cursor, page = [], "*", 0
        while cursor:
            d = self.get(path, {"filter": filt, "select": select, "per_page": 100, "cursor": cursor})
            res = d.get("results", [])
            out.extend(res)
            page += 1
            if page == 1 and label:
                log(f"  {label}: {d.get('meta', {}).get('count', '?')} records")
            cursor = d.get("meta", {}).get("next_cursor")
            if not res:
                break
        return out


def tf(df):
    """Write booleans as TRUE/FALSE, as the instruction note specifies."""
    for c in df.columns:
        if df[c].dtype == bool:
            df[c] = df[c].map({True: "TRUE", False: "FALSE"})
    return df


def chunks(seq, n):
    seq = list(seq)
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def short(oid):
    return (oid or "").rsplit("/", 1)[-1]


# --------------------------------------------------------------------------- helpers
DEPT_RE = re.compile(
    r"(?:Department|Dept\.?|School|Centre|Center|Discipline)\s+(?:of|for)\s+([A-Za-z&\-\s]+?)\s*(?:,|;|\(|$)",
    re.I)


def department_from(raw_affs):
    """First department/school named in the affiliation strings; centres only if no department is named."""
    found = []
    for s in raw_affs or []:
        found += [m for m in DEPT_RE.finditer(s)]
    found.sort(key=lambda m: bool(re.match(r"\s*(Centre|Center)", m.group(0), re.I)))
    for m in found[:1]:
        if m:
            d = re.sub(r"\s+", " ", m.group(1)).strip(" -&")
            # "School of Basic Sciences and Advanced Materials Research Center" -> two units joined by "and"
            d = re.split(r"\s+and\s+(?=(?:Advanced|Centre|Center|Research|Mems)\b)", d, flags=re.I)[0]
            if 2 < len(d) < 80:
                return d.title().replace(" And ", " and ").replace(" Of ", " of ")
    return ""


FIELD_TO_UNIT = {
    "IIT Indore": {"Chemistry": "Chemistry", "Physics and Astronomy": "Physics", "Mathematics": "Mathematics"},
    "IIT Mandi": {"Chemistry": "Chemical Sciences", "Physics and Astronomy": "Physical Sciences",
                  "Mathematics": "Mathematical and Statistical Sciences", "Computer Science": "Computing and Electrical Engineering",
                  "Biochemistry, Genetics and Molecular Biology": "Biosciences and Bioengineering",
                  "Materials Science": "Mechanical and Materials Engineering", "Engineering": "Mechanical and Materials Engineering",
                  "Energy": "Mechanical and Materials Engineering", "Environmental Science": "Civil and Environmental Engineering",
                  "Earth and Planetary Sciences": "Civil and Environmental Engineering"},
}
# official department / school names per institute; first matching pattern wins
UNIT_RULES = {
    "IIT Bhubaneswar": [
        (r"advanced computing", None),
        (r"electric|computer|\bcse\b|electronics", "Electrical and Computer Sciences"),
        (r"infrastructure|civil", "Infrastructure"),
        (r"mechanical", "Mechanical Sciences"),
        (r"earth|ocean|climate|geolog|marine|atmospher|water|agricultur", "Earth, Ocean and Climate Sciences"),
        (r"mineral|metallurg|material", "Minerals, Metallurgical and Materials Engineering"),
        (r"humanit|social|management|economic|english", "Humanities, Social Sciences and Management"),
        (r"basic|physic|chemi|mathemat", "Basic Sciences")],
    "IIT Indore": [
        (r"electric vehicle", "Centre for Electric Vehicles and Intelligent Transport Systems"),
        (r"advanced electronics", "Centre for Advanced Electronics"),
        (r"astronom|space", "Astronomy, Astrophysics and Space Engineering"),
        (r"\bbio", "Biosciences and Biomedical Engineering"),
        (r"chemi", "Chemistry"),
        (r"civil", "Civil Engineering"),
        (r"computer|\bcse\b", "Computer Science and Engineering"),
        (r"electric", "Electrical Engineering"),
        (r"humanit|social|english|economic|philosoph|psycholog", "Humanities and Social Sciences"),
        (r"mathemat", "Mathematics"),
        (r"metallurg|material", "Metallurgy Engineering and Materials Science"),
        (r"mechanical|fluid", "Mechanical Engineering"),
        (r"physic", "Physics"),
        (r"^basic sciences$", "@field")],
    "IIT Mandi": [
        (r"computing|electrical|computer|\bee\b", "Computing and Electrical Engineering"),
        (r"mechanical|aerospace", "Mechanical and Materials Engineering"),
        (r"civil|environmental engineering", "Civil and Environmental Engineering"),
        (r"chemi", "Chemical Sciences"),
        (r"physic|theoretical", "Physical Sciences"),
        (r"mathemat|statist", "Mathematical and Statistical Sciences"),
        (r"\bbio", "Biosciences and Bioengineering"),
        (r"humanit|social|philosoph|cognitive", "Humanities and Social Sciences"),
        (r"^(basic sciences|engineering)$", "@field")],
}


def official_unit(inst, dept, field_counts):
    """Map a parsed department string to the institute's official department/school name."""
    d = re.split(r"\s+(?:indian institute of technology|iit)\b", dept, flags=re.I)[0].strip(" ,")
    low = d.lower()
    for pat, unit in UNIT_RULES.get(inst, []):
        if re.search(pat, low):
            if unit == "@field":
                for f, _ in field_counts.most_common():
                    if f in FIELD_TO_UNIT.get(inst, {}):
                        return FIELD_TO_UNIT[inst][f]
                return d
            return unit or d
    return d


def dept_norm(d):
    """Key that treats spelling variants of one department as the same unit."""
    k = d.lower().replace("&", " and ")
    k = re.sub(r"\bmetallurgical\b", "metallurgy", k)
    k = re.sub(r"\bengg\.?\b", "engineering", k)
    k = re.sub(r"\b(and|of|the|dept|department|school|discipline)\b", " ", k)
    return " ".join(k.split())


def norm_name(n):
    n = re.sub(r"\b(dr|prof|professor|mr|ms|mrs)\.?\s+", " ", n.lower())
    n = re.sub(r"[^a-z\s]", " ", n)
    return [t for t in n.split() if t]


def name_key(n):
    t = norm_name(n)
    if not t:
        return ""
    return f"{t[-1]}|{t[0][0]}"


def norm_title(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


CSIR_LABS = ["NCL", "IICT", "CECRI", "CFTRI", "NIIST", "NML", "NPL", "CSIO", "CGCRI", "CMERI", "CRRI", "CIMFR",
             "CBRI", "CEERI", "SERC", "AMPRI", "CDRI", "CCMB", "IGIB", "IMTECH", "NEERI", "NIO", "IICB", "CSMCRI",
             "NGRI", "IIIM", "CLRI", "NBRI", "CIMAP", "NAL", "IMMT", "CMRI", "NIScPR", "CSIR"]


def cluster_of(name):
    n = name or ""
    u = n.upper()
    if re.search(r"Indian Institute of Technology|\bIIT\b", n) and "Information" not in n:
        return "IIT"
    if re.search(r"Indian Institute of Information Technology|\bIIIT", n):
        return "IIIT"
    if re.search(r"National Institute of Technology|\bNIT\b", n):
        return "NIT"
    if re.search(r"Indian Institute of Science Education|IISER", n):
        return "IISER"
    if "Indian Institute of Science" in n:
        return "IISc"
    if re.search(r"Council of Scientific|\bCSIR\b", n) or any(re.search(rf"\b{l}\b", u) for l in CSIR_LABS):
        return "CSIR"
    if re.search(r"Bhabha Atomic|BARC|Indira Gandhi Centre for Atomic|Raja Ramanna|NISER|National Institute of "
                 r"Science Education and Research|Tata Institute of Fundamental|Homi Bhabha|Saha Institute|"
                 r"Institute of Physics, Bhubaneswar|Harish-Chandra|Institute of Mathematical Sciences|"
                 r"Variable Energy Cyclotron|Atomic Energy", n):
        return "DAE"
    if re.search(r"Indian Statistical Institute|Chennai Mathematical|National Centre for Biological|"
                 r"S\. ?N\. Bose|Bose Institute|Raman Research|Jawaharlal Nehru Centre", n):
        return "Premier Science"
    if re.search(r"All India Institute of Medical|AIIMS|Postgraduate Institute of Medical|Medical College|"
                 r"Indian Council of Medical", n):
        return "Medical"
    if re.search(r"Indian Institute of Management", n):
        return "IIM"
    if re.search(r"Indian Space|ISRO|Defence Research|DRDO|Vikram Sarabhai|Space Applications", n):
        return "ISRO/DRDO"
    if re.search(r"Central University|Jawaharlal Nehru University|University of Delhi|Banaras Hindu|"
                 r"Jadavpur|Jamia Millia|University of Hyderabad|Aligarh Muslim", n):
        return "Central University"
    if re.search(r"University|Vishwavidyalaya", n):
        return "Other University"
    return "Other"


# --------------------------------------------------------------------------- ranking tables
def load_scimago(path, auto_download):
    if not path.exists() and auto_download:
        try:
            log("downloading Scimago journal ranks ...")
            r = requests.get("https://www.scimagojr.com/journalrank.php?out=xls", timeout=120,
                             headers={"User-Agent": "Mozilla/5.0 (DPCN course project)"})
            if r.ok and "SJR" in r.text[:2000]:
                path.write_bytes(r.content)
        except requests.RequestException as e:
            log(f"  Scimago download failed ({e}); continuing without quartiles")
    if not path.exists():
        log("  no scimagojr.csv -> quartile column left blank for journals. "
            "Download it from https://www.scimagojr.com/journalrank.php and re-run.")
        return {}, {}
    df = pd.read_csv(path, sep=";", dtype=str, on_bad_lines="skip")
    qcol = next((c for c in df.columns if "Quartile" in c), None)
    by_issn, by_title = {}, {}
    for _, row in df.iterrows():
        q = (row.get(qcol) or "").strip()
        if q not in ("Q1", "Q2", "Q3", "Q4"):
            continue
        for issn in str(row.get("Issn", "")).split(","):
            issn = issn.strip().replace("-", "").upper()
            if len(issn) == 8:
                by_issn.setdefault(issn, q)
        by_title.setdefault(norm_title(row.get("Title")), q)
    log(f"  Scimago: {len(by_issn)} ISSNs with quartiles")
    return by_issn, by_title


def load_core(path, auto_download):
    if not path.exists() and auto_download:
        try:
            log("downloading CORE conference ranks ...")
            r = requests.get("https://portal.core.edu.au/conf-ranks/?search=&by=all&source=CORE2023&sort=arank"
                             "&page=1&do=Export", timeout=120,
                             headers={"User-Agent": "Mozilla/5.0 (DPCN course project)"})
            if r.ok and r.text.count(",") > 100:
                path.write_bytes(r.content)
        except requests.RequestException as e:
            log(f"  CORE download failed ({e}); continuing without conference ranks")
    if not path.exists():
        return {}, {}
    by_title, by_acr = {}, {}
    with open(path, newline="", encoding="utf-8", errors="ignore") as fh:
        for row in csv.reader(fh):
            if len(row) < 5:
                continue
            title, acr, rank = row[1], row[2].strip(), row[4].strip()
            if rank not in ("A*", "A", "B", "C"):
                continue
            by_title[norm_title(title)] = rank
            if len(acr) >= 3:
                by_acr[acr.upper()] = rank
    log(f"  CORE: {len(by_title)} ranked conferences")
    return by_title, by_acr


def core_rank(venue, by_title, by_acr):
    if not venue:
        return ""
    t = norm_title(venue)
    for k, r in by_title.items():
        if len(k) > 15 and k in t:
            return r
    for tok in re.findall(r"\b[A-Z][A-Za-z\-]{2,}\b", venue):
        tu = tok.upper()
        if tu in by_acr and tok.isupper():
            return by_acr[tu]
    return ""


# --------------------------------------------------------------------------- pipeline
WORK_SELECT = ("id,doi,display_name,publication_year,type,cited_by_count,primary_location,"
               "authorships,referenced_works,primary_topic")
LITE_SELECT = "id,doi,display_name,publication_year,authorships"
CONF_WORDS = re.compile(r"proceedings|conference|symposium|workshop|lecture notes|congress|meeting", re.I)


def venue_type(work):
    src = ((work.get("primary_location") or {}).get("source") or {})
    st, name = src.get("type"), src.get("display_name") or ""
    if work.get("type") == "conference-paper":
        # OpenAlex's own conference-paper type (proceedings in IEEE Xplore, LNCS, AISC, J. Phys. Conf. Ser. ...)
        return "conference" if name and st != "repository" else ""
    if st == "journal":
        return "journal"
    if st == "conference" or (st in ("book series", "ebook platform", None) and CONF_WORDS.search(name)):
        return "conference" if name else ""
    return ""


def indian_insts(work):
    """{institution_id: display_name} for Indian institutions on a work."""
    out = {}
    for a in work.get("authorships") or []:
        for i in a.get("institutions") or []:
            if i.get("country_code") == "IN" and i.get("id"):
                out[short(i["id"])] = i.get("display_name") or short(i["id"])
    return out


def run(args):
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    oa = OpenAlex(args.cache, (os.environ.get("OPENALEX_API_KEY") or "").strip() or None, os.environ.get("OPENALEX_MAILTO"),
                  offline=args.offline)
    oa.workers = getattr(args, "workers", WORKERS)
    if not oa.api_key and not args.offline:
        log("WARNING: no OPENALEX_API_KEY set. The keyless daily budget (~1,000 list calls) is too small for a "
            "full run; the script will stop when it runs out and resume from cache next time.")
    ours = set(INSTITUTIONS)

    # ---------------- 1. corpus
    log("1/8 fetching publications 2016-2026")
    works = {}
    for iid, meta in INSTITUTIONS.items():
        res = oa.paginate("/works",
                          f"institutions.id:{iid},publication_year:{YEAR_FROM}-{YEAR_TO},"
                          f"type:article|review|letter|book-chapter",
                          WORK_SELECT, label=meta["name"])
        for w in res:
            works[short(w["id"])] = w
    # second pass: OpenAlex's "conference-paper" work type. Kept as a separate query (appended after the first
    # pass) so request batches of the first pass stay identical and remain valid in the cache.
    for iid, meta in INSTITUTIONS.items():
        res = oa.paginate("/works",
                          f"institutions.id:{iid},publication_year:{YEAR_FROM}-{YEAR_TO},type:conference-paper",
                          WORK_SELECT, label=meta["name"] + " conference papers")
        for w in res:
            works.setdefault(short(w["id"]), w)
    log(f"  {len(works)} unique works before venue filter")

    by_issn, by_stitle = load_scimago(HERE / "scimagojr.csv", not args.offline)
    core_t, core_a = load_core(HERE / "core_ranks.csv", not args.offline)

    papers = {}
    for wid, w in works.items():
        vt = venue_type(w)
        if not vt and not args.keep_other:
            continue
        src = ((w.get("primary_location") or {}).get("source") or {})
        venue = src.get("display_name") or ""
        issns = [x for x in (src.get("issn") or []) if x]
        issn_l = src.get("issn_l") or (issns[0] if issns else "")
        if vt == "journal":
            q = next((by_issn[i.replace("-", "").upper()] for i in ([issn_l] + issns)
                      if i and i.replace("-", "").upper() in by_issn), "") or by_stitle.get(norm_title(venue), "")
        else:
            q = core_rank(venue, core_t, core_a)
        pt = w.get("primary_topic") or {}
        our_insts = set()
        for a in w.get("authorships") or []:
            for i in a.get("institutions") or []:
                if short(i.get("id")) in ours:
                    our_insts.add(short(i["id"]))
        if not our_insts:
            continue
        papers[wid] = {
            "id": wid, "doi": w.get("doi") or "", "title": (w.get("display_name") or "").strip(),
            "year": w.get("publication_year"), "type": vt or "other", "venue": venue,
            "issn": issn_l if vt == "journal" else "", "citations": w.get("cited_by_count") or 0,
            "quartile": q, "field": ((pt.get("field") or {}).get("display_name")) or "Unclassified",
            "domain": ((pt.get("domain") or {}).get("display_name")) or "Unclassified",
            "subfield": ((pt.get("subfield") or {}).get("display_name")) or "",
            "our_insts": sorted(our_insts), "indian": indian_insts(w),
            "refs": [short(r) for r in w.get("referenced_works") or []], "work_type": w.get("type"),
            "authorships": w.get("authorships") or [],
        }
    log(f"  {len(papers)} journal/conference papers kept")

    # OpenAlex list results show at most 100 authors per work. For works with 100+ authors the full author list was
    # fetched separately (single-work endpoint) and the Group 6 authors hidden by the cut-off are added back here.
    full_path = HERE / "full_authors.json"
    if full_path.exists():
        full = json.loads(full_path.read_text())
        inst_ids = list(INSTITUTIONS)
        added = 0
        for wnum, (n_total, rows) in full["w"].items():
            wid = "W" + wnum
            if wid not in papers:
                continue
            papers[wid]["n_authors_full"] = n_total
            have = {short((a.get("author") or {}).get("id")) for a in papers[wid]["authorships"]}
            for item in filter(None, rows.split(",")):
                anum, idx = item.split(":")
                aid = "A" + anum
                if aid in have:
                    continue
                have.add(aid)
                iid = inst_ids[int(idx)]
                papers[wid]["authorships"].append({
                    "author": {"id": "https://openalex.org/" + aid, "display_name": full["n"].get(anum, "")},
                    "institutions": [{"id": "https://openalex.org/" + iid, "display_name": INSTITUTIONS[iid]["name"],
                                      "country_code": "IN", "type": "education"}],
                    "raw_affiliation_strings": [], "author_position": "middle", "is_corresponding": False,
                    "_restored": True})
                added += 1
        log(f"  restored {added} Group 6 authors hidden by the 100-author cut-off on {len(full['w'])} large papers")
    corpus = set(papers)

    # ---------------- 2. authors
    log("2/8 institutional authors, departments, h-index")
    author_rows = []            # (paper_id, author_id, name, inst_id, dept_guess)
    restored_ids = set()
    role = defaultdict(lambda: {"last": 0, "corr": 0, "years": set()})
    for p in papers.values():
        for a in p["authorships"]:
            inst_here = [short(i.get("id")) for i in a.get("institutions") or [] if short(i.get("id")) in ours]
            if not inst_here or not (a.get("author") or {}).get("id"):
                continue
            aid = short(a["author"]["id"])
            author_rows.append((p["id"], aid, a["author"].get("display_name") or "",
                                inst_here[0], department_from(a.get("raw_affiliation_strings"))))
            if a.get("_restored"):
                restored_ids.add((p["id"], aid))
            r = role[(aid, inst_here[0])]
            r["last"] += a.get("author_position") == "last"
            r["corr"] += bool(a.get("is_corresponding"))
            r["years"].add(p["year"])

    # stable batching: authors of non-conference papers first (sorted), then authors only on conference papers
    # batches are built separately for the two corpus passes so cached batches stay valid when one pass grows
    is_conf = lambda pid: papers[pid]["work_type"] == "conference-paper"
    orig = [r for r in author_rows if (r[0], r[1]) not in restored_ids]
    seen_orig = {r[1] for r in orig}
    author_batches = (list(chunks(sorted({r[1] for r in orig if not is_conf(r[0])}), BATCH)) +
                      list(chunks(sorted({r[1] for r in orig if is_conf(r[0])}), BATCH)) +
                      list(chunks(sorted({a for _, a in restored_ids} - seen_orig), BATCH)))
    author_ids = sorted({r[1] for r in author_rows})
    author_info = {}

    def fetch_authors(batch):
        return oa.get("/authors", {"filter": "openalex:" + "|".join(batch), "per_page": 100,
                                   "select": "id,display_name,works_count,cited_by_count,summary_stats"})
    for d in oa.pmap(fetch_authors, author_batches, "author batches"):
        for a in d.get("results", []):
            author_info[short(a["id"])] = a
    log(f"  {len(author_ids)} institutional authors, {len(author_info)} profiles fetched")

    # per (author, inst) aggregation
    pa = defaultdict(list)
    dept_votes = defaultdict(Counter)       # (aid, iid) -> Counter(normalised dept key) over the latest 3 active years
    dept_years = defaultdict(list)
    spelling = defaultdict(Counter)         # (iid, normalised key) -> Counter(original spellings)
    names = {}
    for pid, aid, nm, iid, dept in author_rows:
        pa[(aid, iid)].append(pid)
        names[aid] = nm
        if dept:
            k = dept_norm(dept)
            spelling[(iid, k)][dept] += 1
            dept_years[(aid, iid)].append((papers[pid]["year"], k))
    for key, lst in dept_years.items():
        recent = sorted({y for y, _ in lst})[-3:]          # departments get renamed: use the current one
        dept_votes[key] = Counter(k for y, k in lst if y in recent)
    canon = {key: c.most_common(1)[0][0] for key, c in spelling.items()}
    author_fields = defaultdict(Counter)
    for pid, aid, nm, iid, dept in author_rows:
        author_fields[(aid, iid)][papers[pid]["field"]] += 1

    # faculty identification
    fac_list_path = HERE / "faculty_list.csv"
    faculty = set()
    dept_override = {}
    if fac_list_path.exists():
        fl = pd.read_csv(fac_list_path, dtype=str).fillna("")
        full = lambda n: " ".join(norm_name(n))
        # index OpenAlex profiles at each institute by full normalised name and by "surname|initial"
        by_full, by_key = defaultdict(list), defaultdict(list)
        for (aid, iid) in pa:
            by_full[(full(names[aid]), iid)].append((aid, iid))
            by_key[(name_key(names[aid]), iid)].append((aid, iid))
        list_keys = Counter((name_key(r["name"]), INST_BY_NAME.get(r["institution"].strip())) for _, r in fl.iterrows())
        cov = []
        for _, r in fl.iterrows():
            iid = INST_BY_NAME.get(r["institution"].strip())
            how, hits = "", []
            if iid:
                hits = by_full.get((full(r["name"]), iid), [])
                how = "full name" if hits else ""
                if not hits:
                    # initials fallback only when unambiguous on both sides (one listed person, one profile)
                    k = (name_key(r["name"]), iid)
                    cand = by_key.get(k, [])
                    if list_keys[k] == 1 and len(cand) == 1:
                        hits, how = cand, "surname + initial"
            for h in hits:
                faculty.add(h)
                if r.get("department", "").strip():
                    dept_override[h] = r["department"].strip()
            cov.append({"name": r["name"], "institution": r["institution"], "department": r.get("department", ""),
                        "found_in_openalex": "TRUE" if hits else "FALSE", "matched_by": how,
                        "openalex_profiles": len(hits),
                        "papers_2016_2026": len({x for h in hits for x in pa[h]})})
        (Path(args.out) / "supplementary").mkdir(parents=True, exist_ok=True)
        pd.DataFrame(cov).to_csv(Path(args.out) / "supplementary" / "faculty_coverage.csv", index=False)
        found = sum(1 for c in cov if c["found_in_openalex"] == "TRUE")
        log(f"  faculty_list.csv: {found} of {len(fl)} listed faculty matched to {len(faculty)} OpenAlex profiles "
            f"({len(fl) - found} not found -> supplementary/faculty_coverage.csv)")
        faculty_source = "faculty_list.csv"
    else:
        # faculty lead papers: they are last/corresponding authors, students are mostly first/middle authors
        faculty = {k for k, v in pa.items()
                   if len(set(v)) >= MIN_PAPERS_FACULTY and max(role[k]["last"], role[k]["corr"]) >= 3
                   and len(role[k]["years"]) >= 3}
        log(f"  no faculty_list.csv -> author-role heuristic: {len(faculty)} faculty "
            f"({ {INSTITUTIONS[i]['name']: sum(1 for _, j in faculty if j == i) for i in INSTITUTIONS} })")
        faculty_source = (f"author-role heuristic: >= {MIN_PAPERS_FACULTY} papers at the institute (2016-2026), "
                          f">= 3 as last or corresponding author, active in >= 3 years")

    def dept_of(key):
        if key in dept_override:
            raw = re.split(r"\s+(?:indian institute of technology|iit)\b", dept_override[key], flags=re.I)[0].strip(" ,")
            return official_unit(INSTITUTIONS[key[1]]["name"], raw, author_fields[key])
        if not dept_votes[key]:
            return "Unknown"
        inst = INSTITUTIONS[key[1]]["name"]
        units = [official_unit(inst, canon[(key[1], k)], author_fields[key]) for k, _ in dept_votes[key].most_common()]
        home = [u for u in units if not u.lower().startswith(("centre", "center"))]
        return (home or units)[0]

    # ---------------- 3. citations out (refs that are Indian)
    log("3/8 references to Indian institutions (out-flow)")
    ref_indian = {}   # work id -> {"insts": {id:name}, "year":, "doi":}
    for p in papers.values():
        for r in p["refs"]:
            if r in corpus:
                ref_indian[r] = {"insts": papers[r]["indian"], "year": papers[r]["year"], "doi": papers[r]["doi"]}
    srcs = [pid for pid, p in papers.items() if p["refs"]]
    src_batches = (list(chunks([x for x in srcs if not is_conf(x)], BATCH)) +
                   list(chunks([x for x in srcs if is_conf(x)], BATCH)))

    def batched_filter(key, batch, select):
        try:
            return oa.paginate("/works", f"{key}:" + "|".join(batch) + ",institutions.country_code:IN", select)
        except BadRequest:
            # OpenAlex rejected the 100-ID OR filter: fall back to one request per paper (slower, same result)
            res = []
            for one in batch:
                res.extend(oa.paginate("/works", f"{key}:{one},institutions.country_code:IN", select))
            return res

    for res in oa.pmap(lambda b: batched_filter("cited_by", b, LITE_SELECT), src_batches, "reference batches"):
        for w in res:
            ref_indian.setdefault(short(w["id"]), {"insts": indian_insts(w), "year": w.get("publication_year"),
                                                   "doi": w.get("doi") or ""})

    # ---------------- 4. citations in (Indian works citing ours)
    log("4/8 Indian works citing our papers (in-flow)")
    citing = {}       # citing work id -> {"insts":, "year":, "doi":, "refs": set}
    cited = [pid for pid, p in papers.items() if p["citations"] > 0]
    cited_batches = (list(chunks([x for x in cited if not is_conf(x)], BATCH)) +
                     list(chunks([x for x in cited if is_conf(x)], BATCH)))
    for res in oa.pmap(lambda b: batched_filter("cites", b, "id,doi,publication_year,authorships,referenced_works"),
                       cited_batches, "citing batches"):
        for w in res:
            wid = short(w["id"])
            if wid in corpus:
                continue
            refs = {short(r) for r in w.get("referenced_works") or []} & corpus
            if refs:
                citing[wid] = {"insts": indian_insts(w), "year": w.get("publication_year"),
                               "doi": w.get("doi") or "", "refs": refs}
    log(f"  {len(citing)} external Indian citing works")

    # ---------------- scope: the dataset is faculty publications ("Fetch all faculty publications (2016-2026)")
    # Fetching above used every institute paper so cached request batches stay stable; analysis uses only papers
    # with at least one Group 6 faculty author. A paper belongs to the institutes of its faculty authors.
    # snapshot of the full institute corpus (students included) for publication statistics / Phase II analysis
    import copy
    full_state = {"papers": {k: dict(v) for k, v in papers.items()}, "author_rows": list(author_rows),
                  "citing": copy.deepcopy(citing), "ref_indian": ref_indian, "faculty": set(faculty),
                  "author_info": author_info, "names": names, "role": {k: dict(v) for k, v in role.items()},
                  "dept": {k: dept_of(k) for k in pa}}
    # Assumption (as instructed): every paper has at least one faculty author. If the faculty rule found none on a
    # paper, its lead Group 6 author counts as the faculty author: corresponding author first, else the last-listed.
    fac_insts = defaultdict(set)
    for pid, aid, nm, iid, _ in author_rows:
        if (aid, iid) in faculty:
            fac_insts[pid].add(iid)
    designated = set()                       # (paper, author, inst) rows assumed to be faculty
    for pid, p in papers.items():
        if pid in fac_insts or faculty_source == "faculty_list.csv":
            continue                         # with a faculty list, only listed people count as faculty
        cands = []
        for pos, a in enumerate(p["authorships"]):
            ins = [short(i.get("id")) for i in a.get("institutions") or [] if short(i.get("id")) in ours]
            if ins and (a.get("author") or {}).get("id"):
                cands.append((bool(a.get("is_corresponding")), a.get("author_position") == "last", pos,
                              short(a["author"]["id"]), ins[0]))
        if cands:
            *_, aid, iid = max(cands)
            designated.add((pid, aid, iid))
            fac_insts[pid].add(iid)
    is_fac_row = lambda pid, aid, iid: (aid, iid) in faculty or (pid, aid, iid) in designated
    n_before = len(papers)
    papers = {pid: p for pid, p in papers.items() if pid in fac_insts}
    for pid, p in papers.items():
        p["our_insts"] = sorted(fac_insts[pid])
    corpus = set(papers)
    author_rows = [r for r in author_rows if is_fac_row(r[0], r[1], r[3])]
    if designated:
        log(f"  {len(designated)} papers had no author matching the faculty rule -> lead Group 6 author used as faculty")
    for cid in list(citing):
        citing[cid]["refs"] &= corpus
        if not citing[cid]["refs"]:
            del citing[cid]
    log(f"  faculty publications: {len(papers)} of {n_before} institute papers")
    sup = out / "supplementary"
    sup.mkdir(parents=True, exist_ok=True)

    # ---------------- 5. citation network
    log("5/8 citation network")
    inst_name = lambda iid: INSTITUTIONS[iid]["name"] if iid in INSTITUTIONS else iid
    our_label = lambda p: ";".join(INSTITUTIONS[i]["name"] for i in p["our_insts"])
    doi_or = lambda doi, wid: doi or f"openalex:{wid}"

    cit_rows = []
    cites_other = defaultdict(set)     # paper -> set of our inst ids for which it cites ANOTHER Indian inst
    cited_by_other = defaultdict(set)
    outflow = defaultdict(Counter)     # our inst -> partner inst name -> count
    inflow = defaultdict(Counter)
    out_year = defaultdict(Counter)    # our inst -> year -> count
    in_year = defaultdict(Counter)
    G = nx.DiGraph()
    G.add_nodes_from(corpus)

    for pid, p in papers.items():
        for r in p["refs"]:
            if r == pid:
                continue
            internal = r in corpus
            info = ref_indian.get(r)
            if not internal and not info:
                continue
            if internal:
                G.add_edge(pid, r)
                tgt_label = our_label(papers[r])
                tgt_ind = papers[r]["indian"]
            else:
                tgt_label = ";".join(sorted(set(info["insts"].values())))
                tgt_ind = info["insts"]
            cross = False
            for oi in p["our_insts"]:
                others = {k: v for k, v in tgt_ind.items() if k != oi}
                if others:
                    cross = True
                    cites_other[pid].add(oi)
                    out_year[oi][p["year"]] += 1
                    for k, v in others.items():
                        outflow[oi][v] += 1
            cit_rows.append({
                "source_doi": doi_or(p["doi"], pid), "target_doi": doi_or(papers[r]["doi"] if internal else
                                                                           info["doi"], r),
                "source_inst": our_label(p), "target_inst": tgt_label, "year": p["year"],
                "edge_scope": "within_corpus" if internal else "out_to_indian",
                "cross_institute": cross, "source_openalex": pid, "target_openalex": r})

    for cid, c in citing.items():
        for r in c["refs"]:
            p = papers[r]
            cross = False
            for oi in p["our_insts"]:
                others = {k: v for k, v in c["insts"].items() if k != oi}
                if others:
                    cross = True
                    cited_by_other[r].add(oi)
                    in_year[oi][c["year"]] += 1
                    for k, v in others.items():
                        inflow[oi][v] += 1
            cit_rows.append({
                "source_doi": doi_or(c["doi"], cid), "target_doi": doi_or(p["doi"], r),
                "source_inst": ";".join(sorted(set(c["insts"].values()))), "target_inst": our_label(p),
                "year": c["year"], "edge_scope": "in_from_indian", "cross_institute": cross,
                "source_openalex": cid, "target_openalex": r})
    # within-corpus edges between our institutes also count as cited_by_other for the target
    for u, v in G.edges():
        for oi in papers[v]["our_insts"]:
            if set(papers[u]["indian"]) - {oi}:
                cited_by_other[v].add(oi)
                in_year[oi][papers[u]["year"]] += 1
                for k, nm in papers[u]["indian"].items():
                    if k != oi:
                        inflow[oi][nm] += 1

    pagerank = nx.pagerank(G, alpha=0.85) if G.number_of_edges() else {n: 1 / max(1, len(G)) for n in G}
    indeg = dict(G.in_degree())
    # in-degree within each institution's own corpus (citing paper shares that institution)
    indeg_inst = defaultdict(Counter)
    for u, v in G.edges():
        for oi in set(papers[u]["our_insts"]) & set(papers[v]["our_insts"]):
            indeg_inst[v][oi] += 1
    cit_df = pd.DataFrame(cit_rows, columns=["source_doi", "target_doi", "source_inst", "target_inst", "year",
                                             "edge_scope", "cross_institute", "source_openalex", "target_openalex"])
    tf(cit_df.copy()).to_csv(sup / "citation_network_extended.csv", index=False)
    has_doi = (~cit_df["source_doi"].str.startswith("openalex:") & ~cit_df["target_doi"].str.startswith("openalex:")
               & pd.to_numeric(cit_df["year"], errors="coerce").between(YEAR_FROM, YEAR_TO))
    cit_df.loc[has_doi, ["source_doi", "target_doi", "source_inst", "target_inst", "year"]].to_csv(
        out / "citation_network.csv", index=False)
    log(f"  citation_network.csv: {int(has_doi.sum())} edges with DOIs on both ends "
        f"({int((~has_doi).sum())} edges without a DOI or dated outside 2016-2026 kept only in supplementary/)")
    pm = pd.DataFrame([{"openalex_id": pid, "doi": p["doi"], "title": p["title"], "year": p["year"],
                        "institutions": our_label(p), "in_degree_within_corpus": indeg.get(pid, 0),
                        **{f"in_degree_within_{INSTITUTIONS[i]['name'].replace(' ', '_')}": indeg_inst[pid].get(i, 0)
                           for i in INSTITUTIONS},
                        "pagerank": pagerank.get(pid, 0), "openalex_citations": p["citations"]}
                       for pid, p in papers.items()]).sort_values("pagerank", ascending=False)
    pm.to_csv(sup / "paper_metrics.csv", index=False)
    log(f"  {len(cit_rows)} citation edges ({G.number_of_edges()} within corpus)")

    # ---------------- 6. authorship network
    log("6/8 authorship network")
    auth_rows = []
    mega = 0
    AG = nx.Graph()
    for p in papers.values():
        auths = []
        for a in p["authorships"]:
            if not (a.get("author") or {}).get("id"):
                continue
            insts = a.get("institutions") or []
            ours_here = [short(i["id"]) for i in insts if short(i.get("id")) in ours]
            if ours_here:
                inst, iid = inst_name(ours_here[0]), ours_here[0]
            elif insts:
                inst, iid = insts[0].get("display_name") or "", short(insts[0].get("id"))
            else:
                inst, iid = "", ""
            aid_ = short(a["author"]["id"])
            g6 = bool(ours_here) and is_fac_row(p["id"], aid_, iid)
            ind = [i for i in insts if i.get("country_code") == "IN" and short(i.get("id")) not in ours]
            if not ours_here and ind:
                inst, iid = ind[0].get("display_name") or "", short(ind[0].get("id"))
            # nodes: Group 6 faculty, plus authors at other Indian institutes (the inter-institute connections)
            if g6 or (not ours_here and ind):
                auths.append((aid_, a["author"].get("display_name") or "", inst, iid, g6))
        if len(auths) > MAX_AUTHORS_FOR_COAUTH:
            mega += 1
            auths = [x for x in auths if x[4]]     # keep pairs among Group 6 faculty only
        seen = set()
        for x, y in combinations(auths, 2):
            if x[0] == y[0] or not (x[4] or y[4]):
                continue
            pair = tuple(sorted((x[0], y[0])))
            if pair in seen:
                continue
            seen.add(pair)
            auth_rows.append({"author_a": x[1], "author_b": y[1], "paper_doi": doi_or(p["doi"], p["id"]),
                              "inst_a": x[2], "inst_b": y[2], "year": p["year"],
                              "cross_institution": x[2] != y[2], "author_a_id": x[0], "author_b_id": y[0]})
            if x[4] and y[4]:
                if AG.has_edge(x[0], y[0]):
                    AG[x[0]][y[0]]["weight"] += 1
                else:
                    AG.add_edge(x[0], y[0], weight=1)
                for n, iid in ((x[0], x[3]), (y[0], y[3])):
                    AG.nodes[n].setdefault("inst", inst_name(iid))
    au_df = pd.DataFrame(auth_rows, columns=["author_a", "author_b", "paper_doi", "inst_a", "inst_b", "year",
                                             "cross_institution", "author_a_id", "author_b_id"])
    tf(au_df.copy()).to_csv(sup / "authorship_network_extended.csv", index=False)
    au_has = ~au_df["paper_doi"].str.startswith("openalex:")
    au_df.loc[au_has, ["author_a", "author_b", "paper_doi", "inst_a", "inst_b", "year"]].to_csv(
        out / "authorship_network.csv", index=False)
    if mega:
        log(f"  {mega} papers with > {MAX_AUTHORS_FOR_COAUTH} authors: kept only pairs among Group 6 authors")

    # scope: metrics on the network of authors at our institutes (faculty only)
    fac_ids = {a for a, _ in faculty}
    FG = AG.copy()          # nodes = faculty (roster + lead authors assumed faculty on their papers)
    deg_c = nx.degree_centrality(FG) if len(FG) > 1 else {}
    k = None if len(FG) <= 2000 else 500
    btw = nx.betweenness_centrality(FG, k=k, seed=42, normalized=True) if len(FG) > 2 else {}
    comms = nx.community.louvain_communities(FG, weight="weight", seed=42) if FG.number_of_edges() else []
    comm_of = {n: ci for ci, c in enumerate(sorted(comms, key=len, reverse=True)) for n in c}
    modularity = nx.community.modularity(FG, comms, weight="weight") if comms else 0
    log(f"  {len(auth_rows)} co-author pairs; faculty graph {len(FG)} nodes / {FG.number_of_edges()} edges, "
        f"{len(comms)} communities (Q={modularity:.3f})")

    # ---------------- 7. dataset + faculty table
    log("7/8 writing group6_data.csv and faculty_summary.csv")
    rows = []
    for pid, aid, nm, iid, _ in author_rows:
        p = papers[pid]
        co = sorted({v for k2, v in p["indian"].items() if k2 != iid})
        rows.append({
            "group": GROUP, "institution": INSTITUTIONS[iid]["name"], "author": nm, "title": p["title"],
            "year": p["year"], "type": p["type"], "journal_name": p["venue"], "issn": p["issn"],
            "doi": p["doi"], "citations": p["citations"], "quartile": p["quartile"],
            "coauthor_institutes": ";".join(co),
            "cites_indian_inst": iid in cites_other[pid], "cited_by_indian_inst": iid in cited_by_other[pid],
            "department": dept_of((aid, iid)), "is_faculty": is_fac_row(pid, aid, iid), "faculty_source": "rule" if (aid, iid) in faculty else "lead author (assumed)", "field": p["field"],
            "domain": p["domain"], "openalex_work_id": pid, "openalex_author_id": aid})
    data = pd.DataFrame(rows).drop_duplicates(["openalex_work_id", "openalex_author_id", "institution"])
    data = data.sort_values(["institution", "author", "year"])
    SPEC_COLS = ["group", "institution", "author", "title", "year", "type", "journal_name", "issn", "doi",
                 "citations", "quartile", "coauthor_institutes", "cites_indian_inst", "cited_by_indian_inst"]
    tf(data[SPEC_COLS].copy()).to_csv(out / f"group{GROUP}_data.csv", index=False)
    tf(data.copy()).to_csv(sup / f"group{GROUP}_data_extended.csv", index=False)

    fac_rows = []
    for (aid, iid), pids in pa.items():
        if (aid, iid) not in faculty:
            continue
        cits = sorted((papers[x]["citations"] for x in pids), reverse=True)
        h_win = sum(1 for i, c in enumerate(cits, 1) if c >= i)
        venues = Counter(papers[x]["venue"] for x in pids if papers[x]["venue"])
        info = author_info.get(aid, {})
        fac_rows.append({
            "name": names[aid], "institution": INSTITUTIONS[iid]["name"], "department": dept_of((aid, iid)),
            "papers": len(set(pids)), "citations": sum(cits),
            "h_index": (info.get("summary_stats") or {}).get("h_index", h_win),
            "h_index_2016_2026": h_win,
            "q1_papers": sum(1 for x in pids if papers[x]["quartile"] == "Q1"),
            "top_journal": venues.most_common(1)[0][0] if venues else "",
            "degree_centrality": round(deg_c.get(aid, 0), 5), "betweenness": round(btw.get(aid, 0), 6),
            "community": comm_of.get(aid, -1), "openalex_author_id": aid})
    FAC_COLS = ["name", "institution", "department", "papers", "citations", "h_index", "h_index_2016_2026",
                "q1_papers", "top_journal", "degree_centrality", "betweenness", "community", "openalex_author_id"]
    fac = pd.DataFrame(fac_rows, columns=FAC_COLS).sort_values(["institution", "papers"], ascending=[True, False])
    fac.to_csv(sup / "faculty_summary.csv", index=False)
    am = fac[["name", "institution", "department", "degree_centrality", "betweenness", "community",
              "openalex_author_id"]].sort_values("degree_centrality", ascending=False)
    am.to_csv(sup / "author_metrics.csv", index=False)

    # department level (for the statistics report: faculty / department / institution levels)
    dep_rows = []
    fd = data[data["is_faculty"]]
    for (inst, dep), g in fd.groupby(["institution", "department"]):
        ups = g.drop_duplicates("openalex_work_id")
        jp = ups[ups["type"] == "journal"]
        fh = fac[(fac["institution"] == inst) & (fac["department"] == dep)]
        dep_rows.append({"institution": inst, "department": dep, "faculty": len(fh), "papers": len(ups),
                         "citations": int(ups["citations"].sum()),
                         "q1_fraction": round((jp["quartile"] == "Q1").mean(), 4) if len(jp) else "",
                         "median_h_index": float(fh["h_index"].median()) if len(fh) else "",
                         "top_journal": jp["journal_name"].mode().iat[0] if len(jp) else ""})
    pd.DataFrame(dep_rows).sort_values(["institution", "papers"], ascending=[True, False]).to_csv(
        sup / "department_summary.csv", index=False)

    # ---------------- 8. Indian connections + topic Jaccard
    log("8/8 Indian connections and topic similarity")
    conn = defaultdict(lambda: {"shared_papers": 0, "total_citations": 0, "partner_id": ""})
    for p in papers.values():
        for oi in p["our_insts"]:
            for k2, nm in p["indian"].items():
                if k2 == oi:
                    continue
                c = conn[(oi, nm)]
                c["shared_papers"] += 1
                c["total_citations"] += p["citations"]
                c["partner_id"] = k2

    def fetch_topics(iid):
        try:
            d = oa.get("/works", {"filter": f"institutions.id:{iid},publication_year:{YEAR_FROM}-{YEAR_TO}",
                                  "group_by": "primary_topic.subfield.id"})
        except (BadRequest, RuntimeError) as e:
            log(f"  topic lookup failed for {iid}: {str(e)[:120]}")
            return set()
        g = sorted(d.get("group_by", []), key=lambda x: -x["count"])
        return {x["key"] for x in g[:30] if x.get("key") and x["key"] != "unknown"}

    want = set(INSTITUTIONS)
    for oi in INSTITUTIONS:
        ranked = sorted((c for (o, _), c in conn.items() if o == oi), key=lambda c: -c["shared_papers"])
        want |= {c["partner_id"] for c in ranked[:TOP_PARTNERS_FOR_JACCARD]}
    want = sorted(w for w in want if w)
    topic_sets = dict(zip(want, oa.pmap(fetch_topics, want, "topic profiles")))
    topics = lambda iid: topic_sets.get(iid, set())

    conn_rows = []
    for oi in INSTITUTIONS:
        partners = sorted(((nm, c) for (o, nm), c in conn.items() if o == oi), key=lambda x: -x[1]["shared_papers"])
        for rank, (nm, c) in enumerate(partners):
            jac = ""
            if c["partner_id"] in topic_sets:
                a, b = topics(oi), topics(c["partner_id"])
                jac = round(len(a & b) / len(a | b), 3) if (a | b) else ""
            cl = cluster_of(nm)
            conn_rows.append({"your_inst": INSTITUTIONS[oi]["name"], "partner_inst": nm,
                              "shared_papers": c["shared_papers"], "total_citations": c["total_citations"],
                              "partner_cluster": cl, "cross_cluster": f"IIT <-> {cl}" if cl != "IIT" else "",
                              "citations_received_from_partner": inflow[oi].get(nm, 0),
                              "citations_given_to_partner": outflow[oi].get(nm, 0),
                              "topic_jaccard": jac, "partner_openalex_id": c["partner_id"]})
    conn_df = pd.DataFrame(conn_rows)
    conn_df[["your_inst", "partner_inst", "shared_papers", "total_citations"]].to_csv(
        out / "indian_connections.csv", index=False)
    conn_df.to_csv(sup / "indian_connections_extended.csv", index=False)

    # ---------------- dashboard
    dash = build_dashboard_data(papers, data, fac, conn_rows, inflow, outflow, in_year, out_year, G, pagerank,
                                indeg, indeg_inst, FG, comm_of, deg_c, btw, modularity, names, faculty_source, oa)
    (sup / "dashboard_data.json").write_text(json.dumps(dash))
    import pickle
    full_state["faculty_papers"] = set(papers)
    with open(Path(args.cache).parent / "phase2_state.pkl", "wb") as fh:
        pickle.dump(full_state, fh)
    tpl = (HERE / "dashboard_template.html").read_text(encoding="utf-8")
    html = tpl.replace("__DASHBOARD_DATA__", json.dumps(dash).replace("</", "<\\/"))
    (out / f"group{GROUP}_dashboard.html").write_text(html, encoding="utf-8")
    log(f"done. API calls this run: {oa.calls}, cache hits: {oa.hits}. Outputs in {out}/")


# --------------------------------------------------------------------------- dashboard payload
def build_dashboard_data(papers, data, fac, conn_rows, inflow, outflow, in_year, out_year, G, pagerank, indeg,
                         indeg_inst, FG, comm_of, deg_c, btw, modularity, names, faculty_source, oa):
    years = list(range(YEAR_FROM, YEAR_TO + 1))
    inst = {}
    for iid, meta in INSTITUTIONS.items():
        ps = [p for p in papers.values() if iid in p["our_insts"]]
        js = [p for p in ps if p["type"] == "journal"]
        cs = [p for p in ps if p["type"] == "conference"]
        qc = Counter(p["quartile"] or "Unranked" for p in js)
        cc = Counter(p["quartile"] or "Unranked" for p in cs)
        fd = fac[fac["institution"] == meta["name"]]
        dept = data[(data["institution"] == meta["name"])].drop_duplicates(["openalex_work_id", "department"])
        dept_counts = dept.groupby("department")["openalex_work_id"].nunique().sort_values(ascending=False)
        top_cited = sorted(ps, key=lambda p: -p["citations"])[:10]
        pr_top = sorted(ps, key=lambda p: -pagerank.get(p["id"], 0))[:10]
        in_tot, out_tot = sum(in_year[iid].values()), sum(out_year[iid].values())
        inst[meta["name"]] = {
            "state": meta["state"], "ror": meta["ror"],
            "papers": len(ps), "journal_papers": len(js), "conference_papers": len(cs),
            "citations": sum(p["citations"] for p in ps),
            "faculty": int(len(fd)),
            "trend": {"years": years,
                      "journal": [sum(1 for p in js if p["year"] == y) for y in years],
                      "conference": [sum(1 for p in cs if p["year"] == y) for y in years]},
            "quartiles": {k: qc.get(k, 0) for k in ["Q1", "Q2", "Q3", "Q4", "Unranked"]},
            "q1_fraction": round(qc.get("Q1", 0) / len(js), 4) if js else 0,
            "q1_fraction_ranked": round(qc.get("Q1", 0) / max(1, len(js) - qc.get("Unranked", 0)), 4),
            "core": {k: cc.get(k, 0) for k in ["A*", "A", "B", "C", "Unranked"]},
            "top_journals": [{"name": n, "papers": c} for n, c in
                             Counter(p["venue"] for p in js if p["venue"]).most_common(5)],
            "fields": [{"name": n, "papers": c} for n, c in Counter(p["field"] for p in ps).most_common()],
            "domains": [{"name": n, "papers": c} for n, c in Counter(p["domain"] for p in ps).most_common()],
            "departments": [{"name": n, "papers": int(c)} for n, c in dept_counts.head(20).items()],
            "most_cited": [{"title": p["title"], "journal": p["venue"], "year": p["year"],
                            "citations": p["citations"], "doi": p["doi"]} for p in top_cited],
            "pagerank_top": [{"title": p["title"], "year": p["year"], "pagerank": round(pagerank.get(p["id"], 0), 6),
                              "in_degree": indeg.get(p["id"], 0), "doi": p["doi"]} for p in pr_top],
            "in_degree_hist": Counter(min(indeg_inst[p["id"]].get(iid, 0), 20) for p in ps),
            "flow": {"years": years, "in": [in_year[iid].get(y, 0) for y in years],
                     "out": [out_year[iid].get(y, 0) for y in years],
                     "in_total": in_tot, "out_total": out_tot,
                     "impact_ratio": round(in_tot / out_tot, 3) if out_tot else None,
                     "top_citing": [{"name": n, "citations": c} for n, c in inflow[iid].most_common(10)],
                     "top_cited": [{"name": n, "citations": c} for n, c in outflow[iid].most_common(10)]},
            "partners": [r for r in conn_rows if r["your_inst"] == meta["name"]][:40],
        }
        inst[meta["name"]]["in_degree_hist"] = {str(k): v for k, v in sorted(inst[meta["name"]]["in_degree_hist"].items())}

    faculty = fac[["name", "institution", "department", "papers", "citations", "h_index", "h_index_2016_2026",
                   "q1_papers", "top_journal", "degree_centrality", "betweenness", "community"]].to_dict("records")

    # citation viz: top papers by PageRank and the edges among them
    # snowball sample for the picture: the most influential papers plus the corpus papers that cite them,
    # so the panel shows connected citation clusters instead of hundreds of isolated dots
    ranked = [n for n, _ in sorted(pagerank.items(), key=lambda x: -x[1])]
    top_nodes, seen = [], set()
    for seed in ranked:
        if len(top_nodes) >= VIZ_MAX_NODES:
            break
        if G.in_degree(seed) == 0 or seed in seen:
            continue
        group = [seed] + sorted(G.predecessors(seed), key=lambda n: -pagerank.get(n, 0))[:12]
        for n in group:
            if n not in seen and len(top_nodes) < VIZ_MAX_NODES:
                seen.add(n)
                top_nodes.append(n)
    tn = set(top_nodes)
    cit_viz = {"nodes": [{"id": n, "label": papers[n]["title"][:80], "inst": papers[n]["our_insts"] and
                          INSTITUTIONS[papers[n]["our_insts"][0]]["name"], "multi": len(papers[n]["our_insts"]) > 1,
                          "year": papers[n]["year"], "pr": pagerank[n], "indeg": indeg.get(n, 0),
                          "cites": papers[n]["citations"], "doi": papers[n]["doi"]} for n in top_nodes],
               "edges": [{"s": u, "t": v} for u, v in G.edges() if u in tn and v in tn],
               "total_nodes": G.number_of_nodes(), "total_edges": G.number_of_edges()}

    # authorship picture: the largest connected collaboration components, highest-degree faculty first
    comps = sorted(nx.connected_components(FG), key=len, reverse=True) if len(FG) else []
    top_auth = []
    for c in comps:
        if len(c) < 3 or len(top_auth) >= VIZ_MAX_NODES:
            break
        top_auth += sorted(c, key=lambda n: -FG.degree(n))[:VIZ_MAX_NODES - len(top_auth)]
    ta = set(top_auth)
    auth_viz = {"nodes": [{"id": n, "label": names.get(n, n), "inst": FG.nodes[n].get("inst", ""),
                           "community": comm_of.get(n, -1), "degree": FG.degree(n),
                           "dc": deg_c.get(n, 0), "btw": btw.get(n, 0)} for n in top_auth],
                "edges": [{"s": u, "t": v, "w": d["weight"]} for u, v, d in FG.edges(data=True) if u in ta and v in ta],
                "total_nodes": FG.number_of_nodes(), "total_edges": FG.number_of_edges(),
                "communities": len(set(comm_of.values())), "modularity": round(modularity, 4),
                "community_sizes": Counter(comm_of.values()).most_common(10)}

    return {"meta": {"group": GROUP, "cluster": CLUSTER, "years": [YEAR_FROM, YEAR_TO],
                     "generated": time.strftime("%Y-%m-%d"), "source": "OpenAlex",
                     "faculty_source": faculty_source, "demo": bool(os.environ.get("G6_DEMO"))},
            "institutions": inst, "faculty": faculty, "citation_network": cit_viz, "authorship_network": auth_viz}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(HERE / "out"))
    ap.add_argument("--cache", default=str(HERE / "cache"))
    ap.add_argument("--offline", action="store_true", help="use cached responses only (rebuild outputs)")
    ap.add_argument("--workers", type=int, default=WORKERS, help="parallel API requests (default 8)")
    ap.add_argument("--keep-other", action="store_true",
                    help="keep works whose venue is neither a journal nor a conference")
    run(ap.parse_args())
