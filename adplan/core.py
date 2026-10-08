"""Deterministic synthetic media planning demonstration."""
from dataclasses import dataclass, asdict
import re

INVENTORY = [
    {"channel": "Connected TV", "cpm": 22.0, "capacity": 12000000, "reach_factor": .76},
    {"channel": "Mobile Video", "cpm": 15.0, "capacity": 18000000, "reach_factor": .58},
    {"channel": "Desktop Video", "cpm": 12.0, "capacity": 10000000, "reach_factor": .48},
]

@dataclass
class Brief:
    budget: float
    max_cpm: float = 25.0
    objective: str = "reach"

def parse_brief(text: str) -> Brief:
    """Extract a dollar budget and optional CPM ceiling."""
    match = re.search(r'\$\s*([\d,]+(?:\.\d+)?)\s*([kKmM]?)', text)
    if not match:
        raise ValueError("Include a dollar budget, e.g. $500,000 or $500k")
    budget = float(match.group(1).replace(',', '')) * {'': 1, 'k': 1000, 'm': 1000000}[match.group(2).lower()]
    if budget <= 0:
        raise ValueError("Budget must be positive")
    cpm = re.search(r'(?:cpm\s*(?:below|under|<=|of)?|(?:below|under)\s*(?:a\s*)?cpm\s*(?:of)?)\s*\$?\s*(\d+(?:\.\d+)?)', text, re.I)
    return Brief(budget, float(cpm.group(1)) if cpm else 25.0)

def optimize(brief: Brief) -> dict:
    """Maximize synthetic reach proxy subject to budget, inventory and blended CPM."""
    from scipy.optimize import linprog
    channels = INVENTORY
    costs = [c['cpm'] / 1000 for c in channels]
    res = linprog(
        c=[-c['reach_factor'] for c in channels],
        A_ub=[costs, [costs[i] - brief.max_cpm / 1000 for i in range(len(channels))]],
        b_ub=[brief.budget, 0],
        bounds=[(0, c['capacity']) for c in channels],
        method='highs',
    )
    if not res.success:
        raise ValueError(f"No feasible media plan: {res.message}")
    rows = []
    for c, impressions in zip(channels, res.x):
        rows.append({"channel": c['channel'], "impressions": round(float(impressions)),
                     "spend": round(float(impressions) * c['cpm'] / 1000, 2),
                     "cpm": c['cpm'], "reach_proxy": round(float(impressions) * c['reach_factor'])})
    spent = sum(r['spend'] for r in rows)
    impressions = sum(r['impressions'] for r in rows)
    return {"brief": asdict(brief), "allocation": rows, "total_spend": round(spent, 2),
            "unspent_budget": round(brief.budget - spent, 2),
            "blended_cpm": round(spent * 1000 / impressions, 2) if impressions else 0,
            "estimated_reach_proxy": sum(r['reach_proxy'] for r in rows),
            "disclaimer": "Synthetic inventory; reach proxy is not deduplicated reach or a real forecast."}
