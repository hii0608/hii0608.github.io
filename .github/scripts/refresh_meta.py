#!/usr/bin/env python3
"""Refresh ONLY lastCommit / commitCount / languages in data/graph.json.

Human-authored fields (summary, status, demo, detail, period, label, ...) are
never touched. Target repos and their node ids are read from data/repos.txt.
Auth via the REPO_PAT environment variable.
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GRAPH = os.path.join(ROOT, "data", "graph.json")
REPOS = os.path.join(ROOT, "data", "repos.txt")
TOKEN = os.environ.get("REPO_PAT", "")
API = "https://api.github.com"


def gh(path):
    req = urllib.request.Request(API + path)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    return urllib.request.urlopen(req, timeout=30)


def last_page_from_link(header):
    if not header:
        return None
    m = re.search(r'[?&]page=(\d+)[^>]*>;\s*rel="last"', header)
    return int(m.group(1)) if m else None


def repo_meta(owner, name):
    """Return (last_commit 'YYYY-MM', commit_count int|None, languages list)."""
    last_commit, commit_count, languages = None, None, []

    # languages
    try:
        with gh(f"/repos/{owner}/{name}/languages") as r:
            languages = list(json.load(r).keys())
    except urllib.error.HTTPError as e:
        print(f"  ! languages {owner}/{name}: {e.code}")

    # latest commit date + total count (via Link rel=last on per_page=1)
    try:
        with gh(f"/repos/{owner}/{name}/commits?per_page=1") as r:
            link = r.headers.get("Link")
            data = json.load(r)
        if data:
            date = data[0].get("commit", {}).get("committer", {}).get("date", "")
            if len(date) >= 7:
                last_commit = date[:7].replace("-", "-")  # YYYY-MM
        lp = last_page_from_link(link)
        commit_count = lp if lp else (1 if data else 0)
    except urllib.error.HTTPError as e:
        print(f"  ! commits {owner}/{name}: {e.code}")

    return last_commit, commit_count, languages


def parse_repos():
    pairs = []
    with open(REPOS, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 2 and "/" in parts[0]:
                pairs.append((parts[0], parts[1]))
    return pairs


def main():
    with open(GRAPH, encoding="utf-8") as f:
        graph = json.load(f)
    by_id = {n["id"]: n for n in graph["nodes"]}

    changed = False
    for full, node_id in parse_repos():
        owner, name = full.split("/", 1)
        node = by_id.get(node_id)
        if not node:
            print(f"  ? node id not found: {node_id}")
            continue
        last_commit, commit_count, languages = repo_meta(owner, name)
        print(f"  {full}: last={last_commit} count={commit_count} langs={languages}")
        for field, value in (("lastCommit", last_commit),
                             ("commitCount", commit_count),
                             ("languages", languages)):
            if value in (None, [], ""):
                continue
            if node.get(field) != value:
                node[field] = value
                changed = True

    if changed:
        with open(GRAPH, "w", encoding="utf-8") as f:
            json.dump(graph, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("graph.json updated.")
    else:
        print("No metadata changes.")


if __name__ == "__main__":
    sys.exit(main())
