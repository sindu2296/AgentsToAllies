from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

def _norm_title(t: Optional[str]) -> str:
    return (t or "").strip().lower().rstrip(".-!?$")

def _host(u: Optional[str]) -> str:
    try:
        return urlparse(u or "").netloc
    except Exception:
        return ""

def dedup_articles(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen_urls, seen_titles = set(), set()
    out = []
    for a in articles:
        url = (a.get("url") or "").strip()
        title = _norm_title(a.get("title"))
        if not title and not url:
            continue
        if url and url in seen_urls:
            continue
        if title and title in seen_titles:
            continue
        seen_urls.add(url)
        seen_titles.add(title)
        out.append(a)
    return out
