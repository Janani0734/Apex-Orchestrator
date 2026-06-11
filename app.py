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

# --- SYSTEM DASHBOARD HEADERS ---
st.markdown("<h1 style='margin:0;'>⚙️ Apex-Orchestrator Control Console</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#64748b; font-size:15px;'>Live Multi-Agent Autonomous Communication Mesh</p>", unsafe_allow_html=True)
st.markdown("---")

# --- LIVE TELEMETRY CONTROL PANEL (SIDEBAR FIRST, BEFORE CLIENT INIT) ---
with st.sidebar:
    st.header("📊 Live Signals Ingest")
    target_track = st.text_input("Target Certification Path", "AZ-204: Developing Solutions for Azure")
    meeting_hours = st.slider("Weekly Meeting Density (Work IQ)", 0, 40, 26)
    focus_hours = st.slider("Available Focus Reserve (Fabric IQ)", 0, 40, 6)

    st.markdown("---")
    st.markdown("### 🔑 Live Credential Override")
    user_key_input = st.text_input("Paste Groq API Key:", type="password")

# --- SECURE CREDENTIAL RESOLUTION (AFTER SIDEBAR) ---
# Priority: sidebar input > streamlit secrets > environment variable
api_key = ""
if user_key_input and len(user_key_input) > 10:
    api_key = user_key_input
else:
    try:
        api_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        pass
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY", "")

# --- GROQ CLIENT INITIALIZATION ---
client = None
if api_key:
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
    except Exception as e:
        st.error(f"Client Initialization Error: {str(e)}")

MODEL = "llama-3.1-8b-instant"

# --- EXECUTION INFRASTRUCTURE BUTTON TRIGGER ---
if st.button("⚡ Execute Infrastructure Inference Loop", type="primary"):
    agent1_output = ""
    agent2_output = ""
    is_overridden = meeting_hours > 20
    is_fallback = False

    col1, col2 = st.columns(2)

    with st.spinner("Initiating live cross-agent validation loop..."):

        # ──► STEP 1: LIVE LLM INFERENCE
        try:
            if client is None:
                raise ValueError("No API key configured.")

            # AGENT 1: FABRIC IQ — Study Plan Generator
            a1_system = (
                "You are the Fabric IQ Agent inside the Apex-Orchestrator multi-agent system. "
                "Generate a concise, high-impact weekly study plan for an IT engineer. "
                "Show your reasoning step by step. Keep it under 4 bullet points. "
                "Be specific about hours, milestones, and topics."
            )
            a1_response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": a1_system},
                    {"role": "user", "content": (
                        f"Create a study track for: {target_track}. "
                        f"The engineer has {focus_hours} focus hours/week and {meeting_hours} meeting hours/week."
                    )}
                ],
                max_tokens=300,
                temperature=0.3
            )
            agent1_output = a1_response.choices[0].message.content

            # AGENT 2: WORK IQ — Burnout Guard & Conflict Resolver
            a2_system = (
                "You are the Work IQ Governance Agent inside the Apex-Orchestrator multi-agent system. "
                "Your job is to audit Agent 1's study plan and protect the engineer from burnout. "
                f"Current telemetry: meeting_hours={meeting_hours}, focus_hours={focus_hours}. "
                f"Burnout index = {round(meeting_hours / max(focus_hours, 1), 2)} (meetings/focus). "
                "If meetings > 20 hours OR burnout index > 2.0, you MUST trigger an OVERRIDE. "
                "Show your conflict resolution reasoning explicitly. "
                "Start your response with either OVERRIDE ACTIVATED or PLAN APPROVED."
            )
            a2_response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": a2_system},
                    {"role": "user", "content": f"Audit this Agent 1 plan:\n\n{agent1_output}"}
                ],
                max_tokens=300,
                temperature=0.3
            )
            agent2_output = a2_response.choices[0].message.content
            is_overridden = "OVERRIDE" in agent2_output.upper() or meeting_hours > 20

        except Exception as e:
            # ──► STEP 2: GRACEFUL FALLBACK
            is_fallback = True
            st.toast(f"⚙️ Running in simulation mode: {str(e)[:60]}", icon="🔄")

            agent1_output = (
                f"• **Core Focus**: High-Availability System Integration for **{target_track}**\n"
                f"• **Target Milestone**: Architectural Ingestion & Telemetry Processing\n"
                f"• **Assigned Velocity Load**: 12 Hours / Week baseline track pacing strategy.\n"
                f"• **Recommended Tools**: Azure Portal, MS Learn sandbox environments."
            )

            if meeting_hours > 20:
                agent2_output = (
                    f"⚠️ **OVERRIDE ACTIVATED**\n\n"
                    f"Burnout index = {round(meeting_hours / max(focus_hours, 1), 2)} — exceeds threshold 2.0. "
                    f"Meeting density: **{meeting_hours}h** vs focus reserve: **{focus_hours}h**. "
                    f"Fabric load downgraded from 12h → **4h maximum** to protect deep-work zones."
                )
                is_overridden = True
            else:
                agent2_output = (
                    f"✅ **PLAN APPROVED**\n\n"
                    f"Burnout index = {round(meeting_hours / max(focus_hours, 1), 2)} — within safe limits. "
                    f"Meeting density: {meeting_hours}h. Focus reserve: {focus_hours}h. "
                    f"No override required. Agent 1 plan cleared for execution."
                )
                is_overridden = False

        # ──► STEP 3: RENDER OUTPUTS
        with col1:
            badge_label = "AGENT 01 // FABRIC IQ (Simulation)" if is_fallback else "AGENT 01 // FABRIC IQ ✅ Live LLM"
            badge_color = "#0284c7" if not is_fallback else "#6b7280"
            badge_bg = "#e0f2fe" if not is_fallback else "#f1f5f9"
            st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
            st.markdown(f"<span class='metric-badge' style='color:{badge_color}; background:{badge_bg};'>{badge_label}</span>", unsafe_allow_html=True)
            st.markdown("### 🚀 Dynamic Curriculum Generation")
            st.write(agent1_output)

            with st.expander("👁️ View Agent 1 Reasoning Logs"):
                st.markdown("#### 🛠️ Agent Execution Context")
                st.json({
                    "agent_name": "Fabric IQ Curriculum Allocator",
                    "model": "Simulation" if is_fallback else MODEL,
                    "provider": "Local Fallback" if is_fallback else "Groq (LLaMA-3.1)",
                    "temperature": 0.3,
                    "inputs": {
                        "target_track": target_track,
                        "focus_hours": focus_hours,
                        "meeting_hours": meeting_hours
                    },
                    "lifecycle_state": "EXECUTION_COMPLETED"
                })
                st.markdown("#### 📋 Reasoning Trace")
                if is_fallback:
                    st.code("[SIMULATION] No API key detected. Serving deterministic fallback plan.", language="bash")
                else:
                    st.code(
                        f"[INFO] Target track: '{target_track}'\n"
                        f"[INFO] Focus hours available: {focus_hours}h/week\n"
                        f"[PROCESSING] Sending to Groq LLaMA-3.1 for curriculum generation...\n"
                        f"[SUCCESS] Live LLM response parsed and rendered.",
                        language="bash"
                    )
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            badge_label = "AGENT 02 // WORK IQ (Simulation)" if is_fallback else "AGENT 02 // WORK IQ ✅ Live LLM"
            bg_color = "#fee2e2" if is_overridden else "#d1fae5"
            border_color = "#f8b4b4" if is_overridden else "#bbf7d0"

            st.markdown(f"<div class='agent-card' style='background:{bg_color}; border-color:{border_color};'>", unsafe_allow_html=True)
            st.markdown(f"<span class='metric-badge' style='color:#b91c1c; background:#fee2e2;'>{badge_label}</span>", unsafe_allow_html=True)
            st.markdown("### 🛡️ Active Burnout Safety Audit")
            st.write(agent2_output)

            with st.expander("👁️ View Agent 2 Conflict & Override Logs"):
                st.markdown("#### 🛡️ Governance Matrix Validation")
                st.json({
                    "agent_name": "Work IQ Burnout Guard",
                    "model": "Simulation" if is_fallback else MODEL,
                    "provider": "Local Fallback" if is_fallback else "Groq (LLaMA-3.1)",
                    "telemetry": {
                        "weekly_meeting_density": f"{meeting_hours}h",
                        "available_focus_reserve": f"{focus_hours}h",
                        "burnout_index_score": round(meeting_hours / max(focus_hours, 1), 2)
                    },
                    "action_taken": "FORCE_DOWNGRADE_OVERRIDE" if is_overridden else "APPROVE_PASS_THROUGH"
                })
                st.markdown("#### 📋 Consensus Loop Feedback Trace")
                if is_overridden:
                    st.code(
                        f"[CRITICAL] Burnout index {round(meeting_hours / max(focus_hours,1), 2)} exceeds threshold 2.0\n"
                        f"[CONFLICT] Agent 2 overriding Agent 1 study velocity...\n"
                        f"[RESOLUTION] Study load reduced to protect {focus_hours}h focus reserve.\n"
                        f"[ACTION] FORCE_DOWNGRADE_OVERRIDE applied.",
                        language="bash"
                    )
                else:
                    st.code(
                        f"[OK] Burnout index {round(meeting_hours / max(focus_hours,1), 2)} within safe limits.\n"
                        f"[CONSENSUS] Agent 1 plan approved by Work IQ governance layer.\n"
                        f"[ACTION] APPROVE_PASS_THROUGH.",
                        language="bash"
                    )
            st.markdown("</div>", unsafe_allow_html=True)

# --- PIPELINE METRIC LEDGER ---
st.markdown("### 🔄 Core Process Monitoring Ledgers")
if client:
    st.success("✅ Live LLM Connected — Groq LLaMA-3.1 active. Enter telemetry and click Execute.")
else:
    st.warning("⚠️ Running in simulation mode. Add your Groq API key in the sidebar to enable live LLM reasoning.")
