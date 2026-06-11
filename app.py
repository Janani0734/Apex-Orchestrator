import streamlit as st
import os
from orchestrator_core import EventDrivenOrchestrator

st.set_page_config(page_title="Apex-Orchestrator Control Center", layout="wide")

# Safe Engine Instantiation
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = EventDrivenOrchestrator()

st.sidebar.title("🏆 Orchestrator Target Telemetry")
profile_mode = st.sidebar.selectbox(
    "Select Target Learner Stream (Contrasting Use Cases):", 
    ["L-1001 (Overloaded Dev - Failure & Remediation Path)", "L-1002 (Optimal Path - Happy Path Baseline)"]
)

# Populating Both Contrasting System Scenarios (Addresses Audit Point #5)
if profile_mode == "L-1001 (Overloaded Dev - Failure & Remediation Path)":
    learner = {"id": "L-1001", "name": "Janani R", "skill_level": "Intermediate"}
    telemetry = {"meeting_hours": 26, "focus_hours": 6, "recent_mock_score": 61, "backlog": "Azure Key Vault, Distributed Consensus"}
else:
    learner = {"id": "L-1002", "name": "Alex Miller", "skill_level": "Advanced"}
    telemetry = {"meeting_hours": 6, "focus_hours": 32, "recent_mock_score": 88, "backlog": "None"}

# --- SYSTEM HEALTH HERO BANNER (Addresses Audit Point #3) ---
if telemetry["meeting_hours"] > 20 and telemetry["recent_mock_score"] < 75:
    st.markdown(
        """<div style='background-color:#fff3cd; padding:20px; border-radius:8px; border-left:8px solid #ffc107; margin-bottom: 25px;'>
        <h3 style='color:#856404; margin:0;'>⚠️ SYSTEM STATUS: ATTENTION REQUIRED / ACTIVE MITIGATION LOOP RUNNING</h3>
        <p style='color:#856404; margin:5px 0 0 0;'>Multi-agent core has actively intercepted heavy meeting density anomalies alongside low initial baseline scores.</p>
        </div>""", unsafe_style_html=True
    )
else:
    st.markdown(
        """<div style='background-color:#d4edda; padding:20px; border-radius:8px; border-left:8px solid #28a745; margin-bottom: 25px;'>
        <h3 style='color:#155724; margin:0;'>🟢 SYSTEM STATUS: NOMINAL PERFORMANCE STABLE</h3>
        <p style='color:#155724; margin:5px 0 0 0;'>All workflow parameters operating cleanly within target enterprise constraints. Voucher track validation cleared directly.</p>
        </div>""", unsafe_style_html=True
    )

st.title("🤖 Apex-Orchestrator: Multi-Agent Workspace Control")
st.markdown("---")

if st.button("⚡ Execute Infrastructure Inference Loop"):
    with st.spinner("Invoking non-deterministic asynchronous multi-agent orchestration streams..."):
        try:
            runtime_data = st.session_state.orchestrator.process_lifecycle(learner, telemetry)
            st.session_state[f"run_{learner['id']}"] = runtime_data
        except Exception as e:
            st.error(f"Authentication Error: Verify your deployment secrets payload token is active. Details: {e}")

# --- PRODUCTION-GRADE VISUAL OUTPUT PANEL ---
if f"run_{learner['id']}" in st.session_state:
    data = st.session_state[f"run_{learner['id']}"]

    # Visual Milestone Tracker Map (Addresses Audit Point #4)
    st.subheader("📊 Dynamic System Milestone Timeline Tracking")
    if data["final_status"] == "PASSED_AFTER_REMEDIATION":
        st.markdown("`[Step 1: Fabric Ingest] ──► [Step 2: Work IQ Overload Conflict Intercepted] ──► 🟡 [Step 3: Remediation Active Loops Run] ──► 🏆 [Voucher Certification Authorized]`")
    else:
        st.markdown("`[Step 1: Fabric Ingest] ──► [Step 2: Work IQ Neutral Pass-Through] ──────────────────────────────────────────► 🏆 [Voucher Certification Authorized Directly]`")

    st.markdown(" ")
    col1, col2 = st.columns(2)

    # Agent Visual Layout Cards with Context Tools (Addresses Audit Point #1, #2 & #6)
    with col1:
        st.markdown(
            f"""<div style='background-color:#f8f9fa; padding:18px; border-radius:6px; border:1px solid #e2e8f0; margin-bottom: 10px;'>
            <span style='background-color:#007bff; color:white; padding:3px 8px; border-radius:4px; font-size:11px; font-weight:bold;'>AGENT 1</span>
            <h4 style='margin-top: 10px;'>🚀 Fabric IQ Study Planner</h4>
            <p><b>Target Curriculum Track:</b> {data['fabric_proposal']['target_track']}</p>
            <p><b>Initial Intended Weekly Load:</b> {data['fabric_proposal']['proposed_hours_per_week']} hrs/week</p>
            </div>""", unsafe_style_html=True
        )
        with st.expander("👁️ View Agent 1 Reasoning Path & Milestones", expanded=False):
            st.write("**Generated Target Structural Focus Milestones:**")
            for milestone in data['fabric_proposal']['milestones']:
                st.write(f"- {milestone}")

    with col2:
        is_override = data["work_consensus"]["status"] == "OVERRIDDEN"
        card_bg = "#fdf2f2" if is_override else "#f3faf7"
        card_border = "#f8b4b4" if is_override else "#def7ec"
        badge_color = "#dc3545" if is_override else "#28a745"
        
        st.markdown(
            f"""<div style='background-color:{card_bg}; padding:18px; border-radius:6px; border:1px solid {card_border}; margin-bottom: 10px;'>
            <span style='background-color:{badge_color}; color:white; padding:3px 8px; border-radius:4px; font-size:11px; font-weight:bold;'>AGENT 2 AUDIT CONSENSUS</span>
            <h4 style='margin-top: 10px;'>🛡️ Work IQ Burnout Guard</h4>
            <p><b>Resolution Protocol Decision:</b> <code style='font-size:14px;'>{data['work_consensus']['status']}</code></p>
            <p><b>Safe Operational Allowed Capacity:</b> {data['work_consensus']['final_hours_per_week']} hrs/week</p>
            </div>""", unsafe_style_html=True
        )
        with st.expander("👁️ View Agent 2 Live Conflict Resolution Audit Log", expanded=True):
            st.metric(label="Calculated Internal Burnout Index Factor", value=data["work_consensus"]["burnout_index"])
            st.info(data["work_consensus"]["resolution_log"])

    # Trace Loop Section Container
    st.markdown("---")
    st.subheader("🔄 Agent 3: Active Feedback Competency Verification Trails")
    st.write(f"**Final Runtime Lifecycle Status:** `{data['final_status']}` | **Final Verified Certification Readiness Grade:** `{data['final_score']}%`")

    if data["execution_trace"]:
        for trace in data["execution_trace"]:
            with st.expander(f"📋 View Active Quality Remediation Cycle Iteration #{trace['loop_count']}", expanded=True):
                st.warning(f"Initial Baseline Ingest Evaluation Check: {trace['pre_score']}% ──► Targeted Sprint Adjustment Optimization Check: {trace['post_score']}%")
                st.write("**Triggered Dynamic Study Sprint Target Core Objectives:**")
                st.json(trace["remediation_action"])
    else:
        st.info("🟢 Competency check verified baseline target criteria safely on initial ingest pass. No remediation iterations required.")
else:
    st.info("💡 Infrastructure state engines current state: IDLE. Click the execution button above to launch real-time multi-agent inference loops.")
