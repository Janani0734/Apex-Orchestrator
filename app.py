import streamlit as st
import os
import json
import time

# Force wide mode and set a professional title
st.set_page_config(page_title="Apex-Orchestrator Management Console", layout="wide")

# --- CUSTOM CSS FOR ENTERPRISE APP FEEL ---
st.markdown("""
    <style>
        /* Remove default streamlit padding to maximize app space */
        .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
        
        /* App Canvas background color */
        .stApp { background-color: #f4f6f9; }
        
        /* Professional Card Grid Styling */
        .app-card {
            background-color: #ffffff;
            padding: 24px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            border: 1px solid #e2e8f0;
            margin-bottom: 20px;
        }
        
        /* Sub-component Badges */
        .agent-badge {
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
            margin-bottom: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# --- APP NAVIGATION & CONTROL SIDEBAR ---
with st.sidebar:
    st.markdown("### 🏢 Core Engine Control")
    profile_mode = st.selectbox(
        "Select Target Learner Stream:", 
        ["L-1001 (Failure & Remediation)", "L-1002 (Optimal Happy Path)"]
    )
    st.markdown("---")
    st.markdown("### 📊 Live Telemetry Inputs")
    
    if profile_mode == "L-1001 (Failure & Remediation)":
        status_state = "WARNING"
        st.metric("Meeting Overload", "26 Hours", "Threshold > 20", delta_color="inverse")
        st.metric("Focus Availability", "6 Hours", "-15 Hours", delta_color="inverse")
    else:
        status_state = "OK"
        st.metric("Meeting Overload", "6 Hours", "Within Bounds")
        st.metric("Focus Availability", "32 Hours", "+12 Hours")

# --- 1. FIXED TOP APP HEADER & STATUS ---
header_col, status_col = st.columns([3, 1])

with header_col:
    st.markdown("<h1 style='margin:0; padding:0; color:#1e293b;'>⚙️ Apex-Orchestrator Center</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:14px; margin-top:4px;'>Enterprise Multi-Agent Resource Allocation Engine</p>", unsafe_allow_html=True)

with status_col:
    if status_state == "WARNING":
        st.markdown(
            """<div style='background-color:#fff3cd; padding:12px; border-radius:6px; border:1px solid #ffeeba; text-align:center;'>
            <span style='color:#856404; font-weight:bold; font-size:13px;'>⚠️ ACTIVE MITIGATION LOOP</span>
            </div>""", unsafe_allow_html=True
        )
    else:
        st.markdown(
            """<div style='background-color:#d4edda; padding:12px; border-radius:6px; border:1px solid #c3e6cb; text-align:center;'>
            <span style='color:#155724; font-weight:bold; font-size:13px;'>🟢 NOMINAL CORE SYSTEM</span>
            </div>""", unsafe_allow_html=True
        )

st.markdown("<hr style='margin-top:10px; margin-bottom:20px;'>", unsafe_allow_html=True)

# --- 2. CONTROL DASHBOARD ACTION ROW ---
exec_col, timeline_col = st.columns([1, 3])

if f"triggered_{profile_mode}" not in st.session_state:
    st.session_state[f"triggered_{profile_mode}"] = False

with exec_col:
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    if st.button("⚡ Run Core Loop Inference", use_container_width=True):
        with st.spinner("Processing..."):
            time.sleep(1)
            st.session_state[f"triggered_{profile_mode}"] = True

with timeline_col:
    if st.session_state[f"triggered_{profile_mode}"]:
        if status_state == "WARNING":
            st.markdown(
                """<div style='background-color:#ffffff; padding:12px; border-radius:6px; border:1px solid #cbd5e1; font-family:monospace; font-size:12px;'>
                <b>Workflow Node Trace:</b> Ingest <span style='color:#3b82f6;'>──►</span> Overload Intercepted <span style='color:#f59e0b;'>──►</span> Remediation Loop Active <span style='color:#10b981;'>──►</span> Cert Authorized
                </div>""", unsafe_allow_html=True
            )
        else:
            st.markdown(
                """<div style='background-color:#ffffff; padding:12px; border-radius:6px; border:1px solid #cbd5e1; font-family:monospace; font-size:12px;'>
                <b>Workflow Node Trace:</b> Ingest <span style='color:#3b82f6;'>──►</span> Baseline Clean Clearance <span style='color:#10b981;'>──►</span> Voucher Authorized Directly
                </div>""", unsafe_allow_html=True
            )

# --- 3. THE MULTI-AGENT WORKSPACE GRID ---
if st.session_state[f"triggered_{profile_mode}"]:
    st.markdown("<h3 style='color:#334155; margin-bottom:15px;'>🤖 Real-Time Agent Consensus Dashboard</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    if status_state == "WARNING":
        a1_track, a1_hours = "AZ-204 (Developing Solutions for Azure)", 8
        a1_log = "Detected student profile skill_level='Intermediate'. Allocating curriculum path parameters to target immediate baseline benchmarks."
        a2_status, a2_hours = "OVERRIDDEN", 5
        a2_log = "CRITICAL LIMIT REACHED: Weekly meeting block density exceeds 20-hour maximum threshold limit. Mitigating burnout triggers by forcing workload structural containment shift down."
        a2_index = 3.71
    else:
        a1_track, a1_hours = "AZ-400 (Designing DevOps Solutions)", 12
        a1_log = "Advanced operational classification profile confirmed. Direct pipeline matching to high-velocity stream track active."
        a2_status, a2_hours = "APPROVED", 12
        a2_log = "System checks verified target availability bounds are highly optimal. Focus reserve limits cleared without risk flags."
        a2_index = 0.18

    # --- AGENT 1 WRAPPER CARD ---
    with col1:
        st.markdown(f"""
            <div class="app-card">
                <span class="agent-badge" style="background-color:#e0f2fe; color:#0369a1;">Agent 01 // Input Planner</span>
                <h4 style="margin: 5px 0 15px 0; color:#1e293b;">🚀 Fabric IQ Curriculum Allocator</h4>
                <p style="margin:4px 0; font-size:14px;"><b>Assigned Path:</b> {a1_track}</p>
                <p style="margin:4px 0; font-size:14px;"><b>Calculated Pace Load:</b> {a1_hours} hrs/week</p>
            </div>
        """, unsafe_allow_html=True)
        with st.expander("👁️ View Agent 1 Technical Logs", expanded=True):
            st.info(a1_log)
            st.code("Formula: track_allocation = Max(enterprise_need) WHERE capability >= Intermediate")

    # --- AGENT 2 WRAPPER CARD ---
    with col2:
        badge_bg = "#fee2e2" if a2_status == "OVERRIDDEN" else "#d1fae5"
        badge_fg = "#991b1b" if a2_status == "OVERRIDDEN" else "#065f46"
        
        st.markdown(f"""
            <div class="app-card">
                <span class="agent-badge" style="background-color:{badge_bg}; color:{badge_fg};">Agent 02 // Core Guard</span>
                <h4 style="margin: 5px 0 15px 0; color:#1e293b;">🛡️ Work IQ Governance Guard</h4>
                <p style="margin:4px 0; font-size:14px;"><b>Consensus Resolution:</b> <code style="font-weight:bold; color:{badge_fg};">{a2_status}</code></p>
                <p style="margin:4px 0; font-size:14px;"><b>Safe Allocation Cap:</b> {a2_hours} hrs/week</p>
            </div>
        """, unsafe_allow_html=True)
        with st.expander("👁️ View Agent 2 Consensus Decision Trace", expanded=True):
            st.metric("Internal Disruption Coefficient Index", f"{a2_index} pts")
            if a2_status == "OVERRIDDEN":
                st.error(a2_log)
            else:
                st.success(a2_log)
            st.code("Formula: disruption_score = meeting_hrs / (focus_hrs + 1)")

    # --- 4. DATA ENGINE TRAIL TRACKER ---
    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#334155; margin-bottom:15px;'>🔄 Autonomous Competency Pipeline Registry</h3>", unsafe_allow_html=True)
    
    if status_state == "WARNING":
        with st.container():
            st.markdown(
                """<div style='background-color:#ffffff; padding:20px; border-radius:8px; border:1px solid #cbd5e1;'>
                <div style='display:flex; justify-content:space-between; margin-bottom:15px;'>
                    <b>Verification Trace Lifecycle:</b> <span style='color:#e11d48; font-weight:bold;'>PASSED_AFTER_REMEDIATION</span>
                    <b>Target Score Readiness:</b> <span style='color:#10b981; font-weight:bold;'>78% Verified</span>
                </div>
                <details style='margin-bottom:10px; padding:10px; background:#f8fafc; border-radius:4px;' open>
                    <summary style='color:#991b1b; font-weight:bold; cursor:pointer;'>❌ Loop Pass #01 — Evaluation Blocked</summary>
                    <p style='font-size:13px; margin:5px 0 0 15px; color:#475569;'>Raw Mock Diagnostic score recorded at 64%, missing target validation threshold (75%). Feedback loop rerouted back to Core Ingest.</p>
                </details>
                <details style='padding:10px; background:#f8fafc; border-radius:4px;' open>
                    <summary style='color:#065f46; font-weight:bold; cursor:pointer;'>✅ Loop Pass #02 — Pipeline Cleared</summary>
                    <p style='font-size:13px; margin:5px 0 10px 15px; color:#475569;'>Dynamic sprint targeted actions applied. Evaluation metrics optimized directly up to 78%.</p>
                </div>""", unsafe_allow_html=True
            )
            st.json(["Enforce isolated environment variable tokens", "Implement consensus structures over core storage trees"])
    else:
        st.markdown(
            """<div style='background-color:#ffffff; padding:20px; border-radius:8px; border:1px solid #cbd5e1; display:flex; justify-content:space-between;'>
            <span><b>Status:</b> <span style='color:#10b981; font-weight:bold;'>PASSED_DIRECTLY</span></span>
            <span><b>Initial Readiness Grade:</b> <span style='color:#10b981; font-weight:bold;'>85%</span></span>
            <span style='color:#475569;'>🟢 Initial performance attributes clear target benchmarks. No remediation iterations needed.</span>
            </div>""", unsafe_allow_html=True
        )
else:
    st.markdown(
        """<div style='text-align:center; padding:60px; border:2px dashed #cbd5e1; border-radius:8px; background:#ffffff;'>
        <p style='color:#64748b; font-size:16px; margin:0;'>🎛️ Control Console Idle: Click <b>"Run Core Loop Inference"</b> above to populate active multi-agent pipelines.</p>
        </div>""", unsafe_allow_html=True
    )
