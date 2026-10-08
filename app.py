import streamlit as st
from adplan.core import parse_brief, optimize

st.set_page_config(page_title="AdPlan AI", layout="wide")
st.title("AdPlan AI | Media Planning Sandbox")
st.caption("Independent portfolio demonstration using synthetic inventory, not Netflix data.")
brief = st.text_area("Advertiser brief", "We have $500,000 for an electric SUV campaign. Keep CPM below $25 and maximize reach.")
if st.button("Generate optimized plan", type="primary"):
    try:
        result = optimize(parse_brief(brief))
        a, b, c = st.columns(3)
        a.metric("Planned spend", f"${result['total_spend']:,.0f}")
        b.metric("Blended CPM", f"${result['blended_cpm']:,.2f}")
        c.metric("Reach proxy", f"{result['estimated_reach_proxy']:,}")
        st.dataframe(result["allocation"], use_container_width=True)
        st.bar_chart({row["channel"]: row["spend"] for row in result["allocation"]})
        st.info(result["disclaimer"])
    except ValueError as exc:
        st.error(str(exc))
