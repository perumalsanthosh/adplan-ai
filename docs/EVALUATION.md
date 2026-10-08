# Evaluation & Scientific Validation Plan

**Status:** test suite exists; the extended evaluation program below is a **proposal**, not completed experiments.

## Existing tests

See [tests/test_core.py](../tests/test_core.py). The current tests cover:
- Extracting a budget and CPM ceiling
- Rejecting missing dollar budgets
- Rejecting a zero budget
- Checking that a sample plan respects budget, blended CPM and inventory limits

Run `python -m pytest -q`. A passing suite validates these specific checks only; it does not demonstrate predictive accuracy, online lift, or production reliability.

## Next evaluation layers

| Area | Proposed metric | Baseline / comparison | Failure examples |
|---|---|---|---|
| Brief understanding | Exact match on budget, CPM and objective; parse failure rate | Regex parser | "$1.2M", ambiguous currency, multiple budgets |
| Optimization | Objective value, budget utilization, violations, solver success | Equal spend, cheapest CPM | Zero delivery, impossible inventory, rounding |
| Forecasting (future) | MAE/RMSE, calibration, interval coverage | Mean and segment baselines | Data leakage, distribution shift |
| Agent quality (future) | Valid tool calls, grounded outputs, constraint adherence | Deterministic pipeline | Hallucinated inventory, wrong budgets |
| Reliability (future) | p50/p95 latency, error rate, cost per plan | Current deterministic endpoint | Timeouts, retries, malformed requests |
| Human review (future) | Seller acceptance and edit frequency | Non-agent recommendation | Unsafe or infeasible suggestions |

## Experimental design

1. Version and seed synthetic data; record assumptions.
2. Hold out evaluation briefs before modifying parsing logic.
3. Report numerator, denominator and uncertainty where appropriate.
4. Compare against explicit baselines, not only absolute scores.
5. Record failure cases and avoid claiming real-world business lift from synthetic results.
6. Re-run the full suite after changes to models, prompts or optimization constraints.

## Claim policy

Use **"synthetic optimization prototype"**, **"sample allocation"**, and **"reach proxy"**. Do **not** claim real CTR improvements, incremental reach, live seller adoption, production deployment, trained ML, or agent evaluation until directly demonstrated and measured.
