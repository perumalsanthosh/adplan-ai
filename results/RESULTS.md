# AdPlan AI — Verified Prototype Results

> **Scope:** v0.1, deterministic optimization prototype with synthetic inventory. These are local code execution results, **not Netflix data, real advertising performance, a production deployment, or a trained ML/LLM evaluation**.

## Executive summary

AdPlan AI converts a simple advertiser budget/CPM brief into a channel allocation by solving a linear program that maximizes a synthetic *reach proxy* while respecting spend, available inventory, and blended CPM constraints.

### Scenario A — $500,000 electric SUV campaign

**Input:** `We have $500,000 for an electric SUV campaign. Keep CPM below $25 and maximize reach.`

| Channel | Allocated spend | Impressions | Channel CPM | Synthetic reach proxy |
|---|---:|---:|---:|---:|
| Connected TV | $110,000 | 5,000,000 | $22.00 | 3,800,000 |
| Mobile Video | $270,000 | 18,000,000 | $15.00 | 10,440,000 |
| Desktop Video | $120,000 | 10,000,000 | $12.00 | 4,800,000 |
| **Total** | **$500,000** | **33,000,000** | **$15.15 blended** | **19,040,000** |

- Budget utilized: **100%**; unspent: **$0**
- Blended CPM: **$15.15**, below the requested $25 ceiling
- Inventory capacity respected for all three channels

### Scenario B — $200,000 campaign, CPM below $18

**Input:** `We have $200k. CPM below $18.`

| Channel | Allocated spend | Impressions | Channel CPM | Synthetic reach proxy |
|---|---:|---:|---:|---:|
| Connected TV | $0 | 0 | $22.00 | 0 |
| Mobile Video | $80,000 | 5,333,333 | $15.00 | 3,093,333 |
| Desktop Video | $120,000 | 10,000,000 | $12.00 | 4,800,000 |
| **Total** | **$200,000** | **15,333,333** | **$13.04 blended** | **7,893,333** |

### Automated tests

Executed locally with `python -m pytest -q`:

```text
....                                                                     [100%]
4 passed in 0.29s
```

Tests cover budget/CPM parsing, rejection of missing or zero budgets, and optimizer constraints.

## Methodology and reproducibility

Source: [adplan/core.py](../adplan/core.py). The optimizer uses SciPy's `linprog(method="highs")`. Decision variables are impressions purchased per channel. It maximizes the sum of impressions weighted by synthetic reach factors, subject to:
- Total spend not exceeding the brief's budget
- Each channel's impression inventory cap
- Weighted average CPM not exceeding the stated maximum

To reproduce:

```bash
pip install -r requirements.txt
python -m pytest -q
python - <<'PY'
from adplan.core import parse_brief, optimize
import json
brief = "We have $500,000 for an electric SUV campaign. Keep CPM below $25 and maximize reach."
print(json.dumps(optimize(parse_brief(brief)), indent=2))
PY
```

## Limitations

1. All inventory, CPMs and reach factors are fixed, **synthetic** inputs.
2. The *reach proxy* is not deduplicated people reached and should not be described as a validated reach forecast.
3. The brief parser is regex-based, not a conversational AI agent; it only extracts budget and some CPM formats.
4. The system does not yet train or evaluate predictive ML models.
5. No real seller feedback, online experiments, production monitoring, or real campaign outcomes have been measured.
6. Displayed impression counts are rounded; underlying optimization uses continuous values.

## Next experiments

- Compare optimization against equal-split and cheapest-CPM baselines
- Evaluate parser correctness across a diverse, labeled brief suite
- Add uncertainty-aware forecasting and constrained scenario comparison
- Implement an agent with structured tool calls and automated evaluation
- Add CI, deployment, and monitoring

*Independent portfolio project. Not affiliated with Netflix.*
