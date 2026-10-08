import pytest
from adplan.core import Brief, parse_brief, optimize, INVENTORY

def test_parse_budget_and_cpm():
    assert parse_brief("Spend $500k, CPM below $20") == Brief(500000, 20)

def test_missing_budget_rejected():
    with pytest.raises(ValueError):
        parse_brief("Please maximize reach")

def test_optimizer_respects_constraints():
    brief = Brief(200000, 18)
    result = optimize(brief)
    assert result["total_spend"] <= brief.budget + .01
    assert result["blended_cpm"] <= brief.max_cpm + .01
    assert all(row["impressions"] <= inv["capacity"] + 1 for row, inv in zip(result["allocation"], INVENTORY))

def test_zero_budget_rejected():
    with pytest.raises(ValueError):
        parse_brief("Spend $0")
