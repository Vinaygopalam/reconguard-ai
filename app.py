from __future__ import annotations
import pandas as pd
import streamlit as st
from src.data.synthetic_generator import generate_demo_data
from src.data.schema_normalizer import load_csv
from src.reconciliation.reconciliation_engine import reconcile
from src.intelligence.exception_grouper import group_exceptions
from src.analytics.metrics import summarize
from src.analytics.financial_summary import build_close_summary
from src.utils import enrich_results

st.set_page_config(page_title="ReconGuard AI", page_icon="RG", layout="wide", initial_sidebar_state="expanded")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;600;700;800&display=swap');
:root { --bg:#0b1120; --surface:#111827; --elevated:#1b2638; --accent:#38bdf8; --ink:#f8fafc; --muted:#94a3b8; --line:rgba(148,163,184,.16); --green:#4ade80; --amber:#fbbf24; --red:#fb7185; }
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { font-family:Manrope,sans-serif; color:var(--ink) !important; background:var(--bg) !important; }
[data-testid="stSidebar"] { background:#0e1728; border-right:1px solid var(--line); } [data-testid="stSidebar"] * { color:var(--ink) !important; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:var(--muted) !important; }
section.main, section.main h1, section.main h2, section.main h3, section.main h4, section.main p, section.main li, section.main label, section.main [data-testid="stCaptionContainer"] { color:var(--ink) !important; }
section.main h1 { font-size:clamp(2rem, 3.5vw, 3.15rem); line-height:1.08; max-width:850px; margin:8px 0 14px; letter-spacing:-.02em; }
section.main h2, section.main h3 { letter-spacing:0; } section.main p { color:var(--muted) !important; line-height:1.6; }
.eyebrow, .section-kicker { color:var(--accent) !important; font:500 11px 'DM Mono'; text-transform:uppercase; letter-spacing:.1em; }
.app-header { display:flex; align-items:center; justify-content:space-between; padding:12px 0 18px; margin-bottom:28px; border-bottom:1px solid var(--line); }
.brand-mark { color:var(--ink); font:700 17px 'DM Mono'; letter-spacing:.02em; } .brand-sub { color:var(--muted); font-size:12px; margin-left:12px; }
.system-ready { color:var(--green); font:500 11px 'DM Mono'; text-transform:uppercase; letter-spacing:.06em; } .system-dot { color:var(--green); font-size:17px; vertical-align:-1px; }
.page-header { border-bottom:1px solid var(--line); padding-bottom:22px; margin-bottom:24px; }
.stat-card, .panel, .source-card, .insight-card, .trust-card { background:var(--surface); border:1px solid var(--line); border-radius:10px; box-sizing:border-box; }
.stat-card { padding:17px 18px 16px; min-height:112px; } .stat-label { color:var(--muted); font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:.07em; }
.stat-value { color:var(--ink); font:500 29px 'DM Mono'; margin-top:12px; } .stat-note { color:var(--muted); font-size:12px; margin-top:5px; }
.panel { padding:22px; height:100%; } .source-card { padding:20px; min-height:210px; } .source-title { color:var(--ink); font-size:16px; font-weight:700; } .source-copy { color:var(--muted); font-size:13px; min-height:42px; }
.insight-card { background:linear-gradient(135deg, #122638, #111827); border-left:3px solid var(--accent); padding:20px; margin:12px 0 18px; } .insight-title { color:var(--accent); font:500 11px 'DM Mono'; text-transform:uppercase; letter-spacing:.1em; } .insight-copy { color:var(--ink); line-height:1.65; margin-top:10px; }
.trust-card { padding:18px; } .trust-number { color:var(--accent); font:500 36px 'DM Mono'; } .trust-caption { color:var(--muted); font-size:12px; } .trust-track { height:7px; background:#253247; border-radius:5px; overflow:hidden; margin:12px 0 7px; } .trust-fill { height:100%; background:var(--accent); border-radius:5px; }
.badge { display:inline-block; padding:5px 9px; border-radius:999px; font:500 10px 'DM Mono'; letter-spacing:.05em; text-transform:uppercase; border:1px solid var(--line); } .badge-auto { color:var(--green); background:rgba(74,222,128,.10); } .badge-review { color:var(--amber); background:rgba(251,191,36,.10); } .badge-exception { color:var(--red); background:rgba(251,113,133,.10); } .badge-neutral { color:var(--muted); background:rgba(148,163,184,.08); }
[data-testid="stMetric"], [data-testid="stExpander"], [data-testid="stDataFrame"] { background:var(--surface); border-color:var(--line); }
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] p, [data-testid="stMetricDelta"] { color:var(--muted) !important; } [data-testid="stMetricValue"] { color:var(--ink) !important; font-family:'DM Mono',monospace; }
[data-testid="stAlert"] { background:var(--elevated); border-color:var(--line); } [data-testid="stAlert"] p, [data-testid="stAlert"] div { color:var(--ink) !important; }
[data-testid="stDataFrame"] { border:1px solid var(--line); } [data-testid="stFileUploader"] section { border-color:var(--line); background:var(--elevated); }
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div { background:var(--surface); border-color:var(--line); } div[data-baseweb="select"] span, div[data-baseweb="input"] input { color:var(--ink) !important; }
button[kind="primary"] { background:var(--accent); border-color:var(--accent); color:#07111f; font-weight:800; } button[kind="secondary"] { background:transparent; border:1px solid var(--line); color:var(--ink); }
[data-testid="stProgressBar"] > div > div { background:var(--accent); }
@media (max-width: 700px) { section.main h1 { font-size:2.2rem; } .app-header { align-items:flex-start; gap:10px; flex-direction:column; } .brand-sub { display:block; margin:5px 0 0; } .stat-card { min-height:100px; } }
</style>""", unsafe_allow_html=True)

@st.cache_data
def demo(): return generate_demo_data(150, 42)

def process(sources):
    raw = reconcile({key: sources[key] for key in ["BANK", "GATEWAY", "LEDGER"]})
    enriched = enrich_results(raw)
    for item in enriched: item["priority"] = item.get("priority", {})
    return enriched

if "sources" not in st.session_state: st.session_state.sources = demo(); st.session_state.results = process(st.session_state.sources)
with st.sidebar:
    st.markdown("<div style='display:flex;align-items:center;gap:12px;margin:8px 0 26px'><div style='background:#38bdf8;color:#07111f;font:700 16px DM Mono;padding:10px;border-radius:8px'>RG</div><div><div style='font-weight:800'>ReconGuard AI</div><div style='font-size:11px;color:#94a3b8'>Financial intelligence</div></div></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-kicker'>Workspace</div>", unsafe_allow_html=True)
    page = st.radio("Workspace", ["Overview", "Data Workspace", "Reconciliation", "Investigation", "AI Close Summary", "Methodology"], label_visibility="collapsed")
    st.markdown("<div style='height:24px'></div><div class='section-kicker'>System</div><div style='border:1px solid rgba(74,222,128,.22);background:rgba(74,222,128,.07);border-radius:8px;padding:11px;font-size:12px;color:#4ade80'>● System Ready<br><span style='color:#94a3b8'>Evidence engine online</span></div>", unsafe_allow_html=True)

results = st.session_state.results; frame = pd.DataFrame([{**{k:v for k,v in x.items() if k not in ["evidence","trust_breakdown","source_records"]}, "priority": x["priority"]["category"], "priority_score": x["priority"]["score"]} for x in results])
metrics = summarize(results, st.session_state.sources.get("GROUND_TRUTH"))

def header(kicker, title, copy):
    st.markdown('<div class="app-header"><div><span class="brand-mark">ReconGuard AI</span><span class="brand-sub">Financial Reconciliation Intelligence</span></div><div class="system-ready"><span class="system-dot">●</span> System Ready</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-header"><div class="eyebrow">{kicker}</div><h1>{title}</h1><p>{copy}</p></div>', unsafe_allow_html=True)

def metric_row():
    cards = [("Transactions", metrics["total"], "Across three source books"), ("Auto matched", metrics["auto_matches"], "Ready to clear"), ("Human review", metrics["human_review"], "Needs a decision"), ("Exceptions", metrics["exceptions"], "Requires investigation"), ("Avg trust", f'{metrics["average_trust"]}/100', "Evidence confidence")]
    cols = st.columns(5)
    for col, (label, value, note) in zip(cols, cards):
        col.markdown(f'<div class="stat-card"><div class="stat-label">{label}</div><div class="stat-value">{value}</div><div class="stat-note">{note}</div></div>', unsafe_allow_html=True)

if page == "Overview":
    header("FINANCIAL OPERATIONS INTELLIGENCE / 01", "Reconciliation, explained.", "Automatically reconcile financial records, investigate exceptions, and route uncertain cases for human review.")
    metric_row(); st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True); left, right = st.columns([1.35, 1])
    with left:
        st.markdown('<div class="panel"><div class="section-kicker">Decision distribution</div><h3>Reconciliation status</h3><p>Every record moves through an evidence-led decision path.</p>', unsafe_allow_html=True)
        status_data = [("Auto matched", metrics["auto_matches"], "#4ade80", "Ready to clear"), ("Human review", metrics["human_review"], "#fbbf24", "Needs a decision"), ("Exceptions", metrics["exceptions"], "#fb7185", "Requires investigation")]
        for label, count, color, note in status_data:
            width = count / max(metrics["total"], 1) * 100
            st.markdown(f'<div style="display:flex;justify-content:space-between;margin:18px 0 7px"><span style="color:#f8fafc;font-size:13px;font-weight:700">{label}</span><span style="color:#94a3b8;font:12px DM Mono">{count:,} · {note}</span></div><div style="height:8px;background:#253247;border-radius:5px;overflow:hidden"><div style="width:{width}%;height:100%;background:{color};border-radius:5px"></div></div>', unsafe_allow_html=True)
        st.markdown('<div style="display:flex;justify-content:space-between;color:#64748b;font:10px DM Mono;margin-top:12px"><span>0%</span><span>100% OF RECORDS</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><div class="section-kicker">System posture</div><h3>What the system knows</h3><div class="insight-card"><div class="insight-title">Trust protocol</div><div class="insight-copy">Every decision carries source-level evidence, confidence, classification, priority, and a recommended next action.</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-card"><div class="stat-label">Reconciliation rate</div><div class="stat-value">{metrics["reconciliation_rate"]}%</div></div>', unsafe_allow_html=True)
        if "accuracy" in metrics: st.markdown(f'<div class="stat-card"><div class="stat-label">Synthetic accuracy</div><div class="stat-value">{metrics["accuracy"]}%</div></div>', unsafe_allow_html=True)
        st.caption("Low-confidence cases remain human-owned.")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Data Workspace":
    header("DATA WORKSPACE / 02", "Connect the source books.", "Upload the three records that establish your financial truth. ReconGuard validates and normalizes each source before matching.")
    upload_copy = {"BANK": ("Bank records", "Settlement and transaction records from the bank."), "GATEWAY": ("Payment gateway", "Payment processing and gateway transaction records."), "LEDGER": ("Internal ledger", "Internal accounting and ledger records.")}
    uploads = {}
    cards = st.columns(3)
    for card, source in zip(cards, ["BANK", "GATEWAY", "LEDGER"]):
        title, copy = upload_copy[source]
        with card:
            st.markdown(f'<div class="source-card"><div class="section-kicker">{source}</div><div class="source-title">{title}</div><div class="source-copy">{copy}</div>', unsafe_allow_html=True)
            uploads[source] = st.file_uploader("Choose CSV", type="csv", key=source, label_visibility="collapsed")
            if uploads[source]: st.markdown('<span class="badge badge-auto">File ready</span>', unsafe_allow_html=True)
            else: st.markdown('<span class="badge badge-neutral">Awaiting file</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    action_a, action_b = st.columns([1, 1])
    with action_a:
        if st.button("Run reconciliation", type="primary", width="stretch") and all(uploads.values()):
            try:
                st.session_state.sources = {source: load_csv(upload, source) for source, upload in uploads.items()}; st.session_state.results = process(st.session_state.sources); st.success("Reconciliation completed."); st.rerun()
            except ValueError as error: st.error(str(error))
    with action_b:
        if st.button("Load demo dataset", width="stretch"): st.session_state.sources = demo(); st.session_state.results = process(st.session_state.sources); st.rerun()
    if not all(uploads.values()): st.caption("Add all three CSV files to enable reconciliation, or load the reproducible demo dataset.")
    for source, source_frame in st.session_state.sources.items():
        if source != "GROUND_TRUTH":
            with st.expander(f"{source} · {len(source_frame):,} records", expanded=False): st.dataframe(source_frame.head(8), width="stretch", hide_index=True)

elif page == "Reconciliation":
    header("RECONCILIATION / 03", "Decisions at a glance.", "Review automated decisions and investigate records requiring attention."); metric_row()
    st.progress(metrics["auto_matches"] / max(metrics["total"], 1), text=f'{metrics["reconciliation_rate"]}% of records are ready to clear')
    tab_all, tab_auto, tab_review, tab_exception = st.tabs(["All records", "Auto matched", "Human review", "Exceptions"])
    columns = ["transaction_id", "status", "trust_score", "exception_type", "priority", "priority_score"]
    for tab, subset in [(tab_all, frame), (tab_auto, frame[frame.status == "AUTO_MATCH"]), (tab_review, frame[frame.status == "HUMAN_REVIEW"]), (tab_exception, frame[frame.status == "EXCEPTION"])]:
        with tab:
            st.dataframe(subset[columns].sort_values("trust_score"), width="stretch", hide_index=True)

elif page == "Investigation":
    header("INVESTIGATION / 04", "Investigate with evidence.", "Select a record from the attention queue and inspect the exact source evidence behind the recommendation.")
    f1, f2, f3 = st.columns(3); status = f1.multiselect("Status", sorted(frame.status.unique()), default=sorted(frame.status.unique())); types = f2.multiselect("Exception type", sorted(frame.exception_type.unique()), default=sorted(frame.exception_type.unique())); priorities = f3.multiselect("Priority", sorted(frame.priority.unique()), default=sorted(frame.priority.unique()))
    filtered = frame[frame.status.isin(status) & frame.exception_type.isin(types) & frame.priority.isin(priorities)]
    selected = st.selectbox("Transaction", filtered.transaction_id.tolist() or ["No matching transactions"])
    if selected != "No matching transactions":
        item = next(x for x in results if x["transaction_id"] == selected)
        st.markdown(f'<div class="panel"><div class="section-kicker">Case file</div><h2>{selected}</h2><span class="badge badge-{ "auto" if item["status"] == "AUTO_MATCH" else "review" if item["status"] == "HUMAN_REVIEW" else "exception"}">{item["status"].replace("_", " ")}</span> <span class="badge badge-neutral">{item["priority"]["category"]} priority</span></div>', unsafe_allow_html=True)
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        left, right = st.columns([.8, 1.5])
        with left:
            trust = item["trust_score"]; caption = "High confidence" if trust >= 85 else "Moderate confidence" if trust >= 60 else "Low confidence"
            st.markdown(f'<div class="trust-card"><div class="section-kicker">Trust score</div><div class="trust-number">{trust}<span style="font-size:15px;color:#94a3b8"> / 100</span></div><div class="trust-caption">{caption}</div><div class="trust-track"><div class="trust-fill" style="width:{trust}%"></div></div></div>', unsafe_allow_html=True)
            with st.expander("Evidence trail", expanded=True):
                for source, scores in item["evidence"].items():
                    st.markdown(f"**{source}**")
                    for label, value in scores.items(): st.progress(value / 100, text=f"{label.replace('_', ' ').title()} · {value:.0f}%")
        with right:
            st.markdown(f'<div class="insight-card"><div class="insight-title">ReconGuard Insight</div><div class="insight-copy">{item["reason"]}</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-kicker">Source comparison</div>', unsafe_allow_html=True)
            source_cols = st.columns(3)
            for source_col, source in zip(source_cols, ["BANK", "GATEWAY", "LEDGER"]):
                record = item["source_records"].get(source)
                with source_col:
                    if record: st.markdown(f'<div class="source-card"><div class="section-kicker">{source}</div><div class="trust-number" style="font-size:22px">INR {float(record["amount"]):,.0f}</div><div class="trust-caption">{pd.Timestamp(record["transaction_date"]).strftime("%d %b %Y")}</div><div class="trust-caption">{record["merchant"]}</div></div>', unsafe_allow_html=True)
                    else: st.markdown(f'<div class="source-card"><div class="section-kicker">{source}</div><div class="trust-caption">No matching record</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-card"><div class="insight-title">Recommended action</div><div class="insight-copy">{item["recommended_action"]}</div></div>', unsafe_allow_html=True)

elif page == "AI Close Summary":
    groups = group_exceptions(results); header("FINANCIAL CLOSE INTELLIGENCE / 05", "The close, briefed.", "A controller-ready summary generated directly from current reconciliation evidence."); metric_row(); st.progress(metrics["auto_matches"] / max(metrics["total"], 1), text=f'{metrics["reconciliation_rate"]}% close completion')
    st.markdown(f'<div class="insight-card"><div class="insight-title">AI financial briefing</div><div class="insight-copy">{build_close_summary(results, groups)}</div></div>', unsafe_allow_html=True)
    if groups: st.subheader("Top investigation patterns"); st.dataframe(pd.DataFrame(groups), width="stretch", hide_index=True)
    st.subheader("Synthetic evaluation")
    if "accuracy" in metrics: st.dataframe(pd.DataFrame([metrics]).T.rename(columns={0:"value"}), width="content")
    else: st.info("Evaluation metrics are available for the generated demo dataset only.")

elif page == "Methodology":
    header("METHOD / 06", "A transparent decision system.", "Deterministic evidence is the source of truth. AI-style language helps people act on it; it never changes the match result.")
    st.subheader("Pipeline"); st.write("1. Normalize source schemas → 2. Match exact identifiers and fuzzy fields → 3. Calculate weighted similarity → 4. Apply configurable thresholds → 5. Score trust and classify exceptions → 6. Route uncertain cases to humans.")
    st.subheader("Trust score"); st.latex(r"Trust = Match\ confidence + Agreement\ bonus + Completeness\ bonus - Ambiguity\ penalty - Duplicate\ penalty")
    st.subheader("Decision policy"); st.dataframe(pd.DataFrame({"Score": ["85–100", "60–84", "0–59"], "Decision": ["AUTO MATCH", "HUMAN REVIEW", "EXCEPTION"], "Principle": ["Evidence is consistent", "Likely, but verify", "Do not resolve automatically"]}), hide_index=True)
    st.warning("Limitations: fuzzy matching cannot infer business context that is absent from exports. Fees, refunds, and partial settlements remain recommendations for human verification.")
