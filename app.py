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

st.markdown("<h1 style='margin:0;'>⚙️ Apex-Orchestrator Control Console</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#64748b; font-size:15px;'>Live Multi-Agent Autonomous Communication Mesh</p>", unsafe_allow_html=True)
st.markdown("---")

# --- SIDEBAR & CREDENTIALS ---
with st.sidebar:
    st.header("📊 Live Signals Ingest")
    target_track = st.text_input("Target Certification Path", "AZ-204: Developing Solutions for Azure")
    meeting_hours = st.slider("Weekly Meeting Density", 0, 40, 26)
    focus_hours = st.slider("Available Focus Reserve", 0, 40, 6)
    st.markdown("### 🔑 Live Credential Override")
    user_key_input = st.text_input("Paste Groq API Key:", type="password")

# --- CENTRALIZED CLIENT FACTORY ---
def get_groq_client(user_key):
    # Try Sidebar > Secrets > Env
    key = user_key or st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    if key and len(key) > 10:
        return OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1")
    return None

MODEL = "llama-3.1-8b-instant"

# --- EXECUTION LOOP ---
if st.button("⚡ Execute Infrastructure Inference Loop", type="primary"):
    client = get_groq_client(user_key_input)
    is_fallback = client is None
    
    col1, col2 = st.columns(2)
    with st.spinner("Initiating live cross-agent validation..."):
        try:
            if is_fallback: raise ValueError("No valid API Key detected.")
            
            # Agent Calls
            a1 = client.chat.completions.create(model=MODEL, messages=[{"role":"user", "content":f"Study plan for {target_track} with {focus_hours}h focus."}])
            agent1_output = a1.choices[0].message.content
            
            a2 = client.chat.completions.create(model=MODEL, messages=[{"role":"user", "content":f"Audit this plan:\n{agent1_output}"}])
            agent2_output = a2.choices[0].message.content
        except Exception as e:
            is_fallback = True
            agent1_output = "• **Core Focus**: System Integration\n• **Velocity**: 12h/week (Simulation Mode)"
            agent2_output = "⚠️ **PLAN APPROVED (Simulated)**: API Unavailable."
            st.toast(f"Fallback engaged: {str(e)[:30]}", icon="🔄")

    # Display results
    with col1:
        st.markdown(f"<div class='agent-card'><h5>Agent 01 // Fabric IQ</h5>{agent1_output}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='agent-card'><h5>Agent 02 // Work IQ</h5>{agent2_output}</div>", unsafe_allow_html=True)

# Final Status
if get_groq_client(user_key_input):
    st.success("✅ Live LLM Connected.")
else:
    st.warning("⚠️ Running in simulation mode.")
