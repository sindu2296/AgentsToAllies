import json
import asyncio
import logging
from typing import Any, Dict, List

from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent

from agents.router_agent import build_router_agent, route_categories
from agents.category_agent import build_category_agent
from agents.summarizer_agent import build_summarizer_agent
from utils.dedup import dedup_articles, _host

CATEGORIES = ["technology","sports","business","science","health","entertainment","general"]

async def _fetch_from_category(agent: ChatCompletionAgent, category: str) -> List[Dict[str, Any]]:
    prompt = f"Fetch JSON news for category='{category}'. If needed, call the tool."
    logging.info(f"\n[FETCHING] Category: {category}")
    
    response = ""
    async for msg in agent.invoke(prompt):
        response += msg.content.content
        
    logging.info(f"\n[RESPONSE] Raw response for {category}:\n{response}\n")
    
    try:
        data = json.loads(response)
        articles = data if isinstance(data, list) else []
        logging.info(f"[SUCCESS] Found {len(articles)} articles for {category}")
        return articles
    except Exception as e:
        logging.error(f"[ERROR] Failed to parse JSON for {category}: {str(e)}")
        return []

class ProNewsOrchestrator:
    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.router = build_router_agent(kernel)
        self.summarizer = build_summarizer_agent(kernel)

    async def run(self, user_query: str) -> str:
        logging.info(f"\n[ROUTING] Processing query: {user_query}")
        targets = await route_categories(self.router, user_query)
        logging.info(f"[ROUTING] Selected categories: {targets}")
        
        cat_agents = [build_category_agent(self.kernel, f"{c}_agent", c) for c in targets]
        results = await asyncio.gather(*[
            _fetch_from_category(agent, c) for agent, c in zip(cat_agents, targets)
        ], return_exceptions=True)

        merged: List[Dict[str, Any]] = []
        for r in results:
            if isinstance(r, Exception):
                continue
            merged.extend(r)
        merged = dedup_articles(merged)

        if not merged:
            return "No articles found."

        maps: List[str] = []
        for i in range(0, len(merged), 6):
            batch = merged[i : i + 6]
            payload = json.dumps(batch)
            response = ""
            async for m in self.summarizer.invoke(
                f"Summarize these articles to 3 bullets with inline sources (JSON provided):\n{payload}"
            ):
                response += m.content.content
            maps.append(response)

        combined = "\n\n".join(maps)
        response = ""
        async for final_msg in self.summarizer.invoke(
            "Synthesize a 5-bullet executive brief for an engineering leader from the following partial summaries.\n"
            + combined
        ):
            response += final_msg.content.content
        brief = response

        sources = sorted({(a.get("source") or "", _host(a.get("url"))) for a in merged})
        src_lines = "\n".join([f"- {s} ({h})" for s, h in sources if s or h])
        header = "Selected categories: " + ", ".join(targets)
        return f"{header}\n\n{brief}\n\nTop sources:\n{src_lines}"
