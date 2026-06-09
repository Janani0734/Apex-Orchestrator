import streamlit as st
import json
import os

# Premium presentation configuration
st.set_page_config(page_title="Apex-Orchestrator AI", page_icon="🚀", layout="wide")

# ==========================================
# CORE REASONING LOGIC FUNCTIONS
# ==========================================
def run_study_planner_agent(cert, work_metrics, skills):
    meetings = work_metrics["meeting_hours_per_week"]
    base_hours = 20 if cert == "AZ-204" else 25
    
    if meetings > 20:
        pace, weeks = "Extended Pace (Burnout Guard Active)", 4
    elif meetings > 12:
        pace, weeks = "Moderate Pace", 3
    else:
        pace, weeks = "Accelerated Pace", 2
        
    return {
        "pace_tier": pace,
        "duration_weeks": weeks,
        "weekly_hours": round(base_hours / weeks, 1),
        "modules": [{"phase": f"Module {i+1}", "topic": skill} for i, skill in enumerate(skills)]
    }

def run_engagement_agent(work_metrics):
    focus = work_metrics["focus_hours_per_week"]
    if focus > 15:
        return {"channel": "Weekly Digest Email", "window": "Friday 16:00 (Focus Zone Protected)", "risk": "Low Risk"}
    return {"channel": "Daily Teams Ping", "window": "09:00" if work_metrics["preferred_learning_slot"] == "Morning" else "14:00", "risk": "Normal Operational Risk"}

def run_assessment_agent(learner_data):
    score = learner_data["practice_score_avg"]
    if score >= 75:
        return {"status": "APPROVED FOR VOUCHER", "next": "Issue certification voucher code immediately via Foundry IQ."}
    return {"status": "REMEDIATION_LOOP_TRIGGERED", "next": "Identify sub-skill gaps and route back to Fabric IQ Planner node."}

# ==========================================
# WEB UI PRESENTATION LAYER
# ==========================================
st.title("🚀 Apex-Orchestrator")
st.subheader("Enterprise Multi-Agent Upskilling & Operational Burnout Guard")
st.write("---")

# Absolute path resolution to ensure the app works seamlessly on the cloud servers
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")

try:
    with open(DATA_PATH, "r") as f:
        dataset = json.load(f)

    # Sidebar layout controller
    st.sidebar.header("🎯 Simulation Control Panel")
    selected_id = st.sidebar.selectbox("Select Fictional Learner ID", ["L-1001", "L-1002"])

    learner = next(l for l in dataset["learners"] if l["learner_id"] == selected_id)
    signals = next(s for s in dataset["work_signals"] if s["employee_id"] == selected_id)
    skills = dataset["fabric_iq_skills"].get(learner["certification"], ["Cloud Basics"])

    # Run execution pipeline
    plan = run_study_planner_agent(learner["certification"], signals, skills)
    engagement = run_engagement_agent(signals)
    assessment = run_assessment_agent(learner)

    # Metrics Display Columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Target Certification Track", value=learner["certification"])
    with col2:
        st.metric(label="Simulated Practice Exam Avg", value=f"{learner['practice_score_avg']}%")
    with col3:
        st.metric(label="System Gate Status", value=assessment["status"])

    st.write("### 🧠 Autonomous Multi-Agent Reasoning Logs")
    left_col, right_col = st.columns(2)

    with left_col:
        st.info("#### 📋 Agent 1: Fabric IQ Study Planner")
        st.write(f"**Calculated Pace:** {plan['pace_tier']}")
        st.write(f"**Program Timeline:** {plan['duration_weeks']} Weeks")
        st.write(f"**Target Allocation:** {plan['weekly_hours']} Hours/Week")
        st.write("**Generated Modules Structure:**")
        st.json(plan["modules"])

    with right_col:
        st.warning("#### ⏰ Agent 2: Work IQ Engagement Router")
        st.write(f"**Communication Pathway:** {engagement['channel']}")
        st.write(f"**Optimal Notification Window:** {engagement['window']}")
        st.write(f"**Workplace Disruption Risk:** {engagement['risk']}")
        
        st.error("#### 🛡️ Agent 3: Foundry IQ Evaluation Gate")
        st.write(f"**Current Status:** {assessment['status']}")
        st.write(f"**Next Action Item:** {assessment['next']}")

    st.write("---")
    st.info("#### 📊 Agent 4: Anonymized Manager Insights Dashboard (PII Stripped)")
    st.write(f"**Cohort Reference ID:** TRACK-{learner['certification']}")
    st.write(f"**Cohort Readiness Forecast:** " + ("High-Probability Pass" if assessment["status"] == "APPROVED FOR VOUCHER" else "Critical Intervention Needed"))
    st.write(f"**Team Capacity Risk Flag:** " + ("True - High Workloads Detected" if plan['duration_weeks'] == 4 else "False - Stable Operational Headroom"))

except FileNotFoundError:
    st.error("Error: `data.json` file not found in the same folder repository directory. Please commit it to GitHub.")
