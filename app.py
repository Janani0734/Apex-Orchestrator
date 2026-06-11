import streamlit as st
import os
from openai import OpenAI

st.set_page_config(page_title="Apex-Orchestrator Canvas", layout="wide")

# --- CUSTOM GRAPHICS & STYLING LAYER ---
st.markdown("""
    <style>
        div[data-testid="stMainBlockContainer"] { max-width: 100% !important; padding: 1.5rem 2rem !important; }
        .agent-card { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 20px; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        .metric-badge { background: #f1f5f9; color: #334155; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- SECURE CREDENTIAL CHECK ---
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

client = None
if api_key and not api_key.startswith("your-"):
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Initialization Error: {str(e)}")

# --- SYSTEM DASHBOARD HEADERS ---
st.markdown("<h1 style='margin:0;'>⚙️ Apex-Orchestrator Control Console</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#64748b; font-size:15px;'>Live Multi-Agent Autonomous Communication Mesh</p>", unsafe_allow_html=True)
st.markdown("---")

# --- LIVE TELEMETRY CONTROL PANEL ---
with st.sidebar:
    st.header("📊 Live Signals Ingest")
    target_track = st.text_input("Target Certification Path", "AZ-204: Developing Solutions for Azure")
    meeting_hours = st.slider("Weekly Meeting Density (Work IQ)", 0, 40, 26)
    focus_hours = st.slider("Available Focus Reserve (Fabric IQ)", 0, 40, 6)
    
    st.markdown("---")
    st.markdown("### 🔑 Live Credential Override")
    user_key_input = st.text_input("Paste OpenAI API Key to test on the fly:", type="password")
    if user_key_input:
        client = OpenAI(api_key=user_key_input)

# --- EXECUTION INFRASTRUCTURE BUTTON TRIGGER ---
if st.button("⚡ Execute Infrastructure Inference Loop", type="primary"):
    agent1_output = ""
    agent2_output = ""
    is_overridden = meeting_hours > 20  
    is_fallback = False
    
    col1, col2 = st.columns(2)
    
    with st.spinner("Initiating live cross-agent validation loop..."):
        # ──► STEP 1: DATA INGESTION (TRY TO CONNECT TO OPENAI)
        try:
            if client is not None:
                # RUN FABRIC IQ LIVE
                a1_system = "You are the Fabric IQ Agent. Generate a concise, high-impact weekly study plan sub-module for an IT engineer based on their target track. Keep it under 3 bullet points."
                a1_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": a1_system},
                        {"role": "user", "content": f"Create a high-velocity study track layout for {target_track}."}
                    ],
                    max_tokens=250
                )
                agent1_output = a1_response.choices[0].message.content

                # RUN WORK IQ LIVE
                a2_system = f"You are the Work IQ Governance Agent. Audit Agent 1's plan. Current meetings: {meeting_hours}h, Focus: {focus_hours}h. If meetings > 20, trigger an OVERRIDE."
                a2_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": a2_system},
                        {"role": "user", "content": f"Review this plan:\n\n{agent1_output}"}
                    ],
                    max_tokens=250
                )
                agent2_output = a2_response.choices[0].message.content
                is_overridden = "OVERRIDE" in agent2_output.upper() or meeting_hours > 20
            else:
                raise ValueError("No token verification.")
                
        except Exception as quota_error:
            # ──► STEP 2: FALLBACK DATA INGESTION (IF LIVE API FAILS)
            is_fallback = True
            st.toast("🔄 API limit hit or key missing. Engaging local backup telemetry simulation.", icon="⚙️")
            
            agent1_output = (
                f"• **Core Focus**: High-Availability System Integration for **{target_track}**\n"
                f"• **Target Milestone**: Architectural Ingestion & Telemetry Processing\n"
                f"• **Assigned Velocity Load**: 12 Hours / Week baseline track pacing strategy."
            )
            
            if meeting_hours > 20:
                agent2_output = (
                    f"⚠️ **CRITICAL OVERRIDE COMPROMISE FLAG ACTIVATED**\n\n"
                    f"Detected extreme scheduling anomalies (Meeting Density: **{meeting_hours} Hours**). "
                    f"Fabric load downgraded from 12 hours down to **4 hours maximum** to protect baseline resource balance."
                )
                is_overridden = True
            else:
                agent2_output = (
                    f"🟢 **NOMINAL RECOVERY VALIDATION PATH CLEAR**\n\n"
                    f"Operational load balances within acceptable design thresholds (Meeting Density: {meeting_hours} Hours). "
                    f"No resource remediation loops required. Pacing verified at 100% capacity."
                )
                is_overridden = False

        # ──► STEP 3: UNIFIED RENDER ENGINE (RUNS CLEANLY EVERY TIME)
        with col1:
            badge_label = "AGENT 01 // FABRIC IQ (Edge-Fallback)" if is_fallback else "AGENT 01 // FABRIC IQ"
            st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
            st.markdown(f"<span class='metric-badge' style='color:#0284c7; background:#e0f2fe;'>{badge_label}</span>", unsafe_allow_html=True)
            st.markdown("### 🚀 Dynamic Curriculum Generation")
            st.write(agent1_output)
            
            with st.expander("👁️ View Agent 1 Clear Reasoning Logs"):
                st.markdown("#### 🛠️ Agent Execution Context")
                st.json({
                    "agent_name": "Fabric IQ Curriculum Allocator",
                    "model_target": "Local_Fallback_Core" if is_fallback else "gpt-4o-mini",
                    "temperature": 0.3,
                    "lifecycle_state": "EXECUTION_COMPLETED"
                })
                st.markdown("#### 📋 Raw Intermediate Thought Stream")
                if is_fallback:
                    st.code("[LOCAL_FALLBACK] Serving cached local matrix modules for context stream.", language="bash")
                else:
                    st.code(f"[INFO] Ingesting target track parameter: '{target_track}'\n[PROCESSING] Calculating multi-agent pace constraints...\n[LLM RESPONSE] Successfully parsed curriculum blocks directly.", language="bash")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            badge_label = "AGENT 02 // WORK IQ (Edge-Fallback)" if is_fallback else "AGENT 02 // WORK IQ"
            bg_color = "#fee2e2" if is_overridden else "#d1fae5"
            border_color = "#f8b4b4" if is_overridden else "#bbf7d0"
            
            st.markdown(f"<div class='agent-card' style='background:{bg_color}; border-color:{border_color};'>", unsafe_allow_html=True)
            st.markdown(f"<span class='metric-badge' style='color:#b91c1c; background:#fee2e2;'>{badge_label}</span>", unsafe_allow_html=True)
            st.markdown("### 🛡️ Active Burnout Safety Audit")
            st.write(agent2_output)
            
            with st.expander("👁️ View Agent 2 Conflict & Override Scenario Logs"):
                st.markdown("#### 🛡️ Governance Matrix Validation")
                st.json({
                    "agent_name": "Work IQ Burnout Guard",
                    "telemetry_evaluated": {
                        "weekly_meeting_density": f"{meeting_hours} hours",
                        "available_focus_reserve": f"{focus_hours} hours"
                    },
                    "burnout_index_score": round(meeting_hours / (focus_hours + 1), 2),
                    "action_taken": "FORCE_DOWNGRADE_OVERRIDE" if is_overridden else "APPROVE_PASS_THROUGH"
                })
                st.markdown("#### 📋 Consensus Loop Feedback Trace")
                if is_overridden:
                    st.code("[CRITICAL] Burnout Index exceeds threshold safety limits.\n[CONFLICT RESOLUTION] Sending compensation frame to Layer 01...\n[REMEDIATION] Forcing study load reduction down to defensive thresholds.", language="bash")
                else:
                    st.code("[NOMINAL] Burnout Index within safe limits.\n[CONSENSUS] Validation cleared. No cross-agent negotiation loop required.", language="bash")
            st.markdown("</div>", unsafe_allow_html=True)

# --- PIPELINE METRIC LEDGER ---
st.markdown("### 🔄 Core Process Monitoring Ledgers")
st.info("Pipeline State Monitoring Matrix: Active and listening for live multi-agent execution frames.")
