# AdPlan AI — Agentic Media Planning & Optimization (Prototype)

An independent, synthetic-data portfolio prototype inspired by advertising media-planning problems. **Not affiliated with Netflix.**

## Features
- Parse campaign budgets, target audience and CPM constraints from a brief
- Generate reproducible synthetic ad inventory
- Optimize spend allocation using SciPy linear programming
- Explore plans in a Streamlit interface
- Request plans through a FastAPI endpoint
- Run automated tests

**Status:** v0.1 optimization prototype. No LLM agent, trained forecasting model, real advertising data, production deployment or real-world performance claims are included yet.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Run the API: `uvicorn api:app --reload`

Run tests: `pytest -q`

## Roadmap
1. Structured LLM brief parsing with validation
2. Forecasting model and uncertainty estimation
3. Multi-objective allocation and feasibility diagnostics
4. Agent evaluation, feedback loops and experiment tracking
5. Docker, CI, observability and deployment

## Responsible disclosure
All campaign examples and inventory data are synthetic. Optimization output is not a forecast of real advertising outcomes.
