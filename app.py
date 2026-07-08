import streamlit as st
import pandas as pd
import plotly.express as px
import random
import re
import os
from datetime import datetime

st.set_page_config(page_title="AuraGuard | AI Governance Shield", layout="wide", initial_sidebar_state="expanded")

# --- FILE PATH FOR PERSISTENCE ---
AUDIT_FILE = "auraguard_audit.csv"

# --- HELPER FUNCTIONS TO MANAGE LOCAL FILE DATABASE ---
def load_audit_trail():
    if os.path.exists(AUDIT_FILE):
        try:
            return pd.read_csv(AUDIT_FILE).to_dict(orient="records")
        except Exception:
            pass
    return [
        {"Timestamp": "2026-07-07 12:05:23", "Payload_ID": "req-1000", "PII_Masked_Count": 2, "Primary_PII_Type": "EMAIL", "Verdict": "PASS", "Triggered_Rule": "NONE", "Tokens_Processed": 142},
        {"Timestamp": "2026-07-07 12:08:11", "Payload_ID": "req-1001", "PII_Masked_Count": 0, "Primary_PII_Type": "NONE", "Verdict": "PASS", "Triggered_Rule": "NONE", "Tokens_Processed": 88},
        {"Timestamp": "2026-07-07 12:15:44", "Payload_ID": "req-1002", "PII_Masked_Count": 1, "Primary_PII_Type": "IP_ADDRESS", "Verdict": "FAIL", "Triggered_Rule": "GDPR-001", "Tokens_Processed": 215},
    ]

def save_audit_trail(data):
    pd.DataFrame(data).to_csv(AUDIT_FILE, index=False)

# --- INITIALIZE PERSISTENT STATE ---
if 'ledger_data' not in st.session_state:
    st.session_state.ledger_data = load_audit_trail()

# --- APP UI HEADER WITH EXPANDED LOGO CONFIGURATION ---
col_logo, col_title = st.columns([1, 4])  # Shifted column layout to offer optimal space
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=175)  # Scale increased from 110 to 175 pixels
    else:
        st.info("ℹ️ logo.png pending placement")
with col_title:
    st.title("AuraGuard | AI Governance & Compliance Shield")
    st.caption("Real-time telemetry, PII redaction tracking, and regulatory audit middleware for IBM watsonx.ai.")
st.markdown("---")

# --- NAVIGATION TABS ---
tab1, tab2 = st.tabs(["📊 Live Telemetry Dashboard", "🎛️ Prompt Sanitizer Sandbox"])

# ==========================================
# TAB 1: TELEMETRY DASHBOARD
# ==========================================
with tab1:
    st.sidebar.header("📥 Direct Log Injector Interceptor")
    st.sidebar.markdown("Paste or register raw agent payloads directly into the gateway shield.")

    input_text = st.sidebar.text_area("Raw Transaction Text / Payload Data", placeholder="e.g., Request contained admin@company.com and IP 192.168.1.50")
    tokens_input = st.sidebar.number_input("Tokens Audited", min_value=10, max_value=5000, value=120)
    rule_trigger = st.sidebar.selectbox("Regulatory Compliance Violation", ["NONE", "GDPR-001 (EU PII)", "HIPAA-001 (Health)", "CCPA-003 (Privacy)"])

    if st.sidebar.button("Intercept & Log Transaction"):
        if input_text:
            has_email = "@" in input_text
            has_ip = "." in input_text
            
            pii_type = "EMAIL" if has_email else ("IP_ADDRESS" if has_ip else "CREDIT_CARD")
            verdict = "FAIL" if rule_trigger != "NONE" else "PASS"
            rule_name = rule_trigger.split(" ")[0]
            pii_count = random.randint(1, 3) if rule_trigger != "NONE" else (1 if (has_email or has_ip) else 0)
            
            new_entry = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Payload_ID": f"req-{random.randint(1004, 9999)}",
                "PII_Masked_Count": pii_count,
                "Primary_PII_Type": pii_type if (rule_trigger != "NONE" or has_email or has_ip) else "NONE",
                "Verdict": verdict,
                "Triggered_Rule": rule_name,
                "Tokens_Processed": tokens_input
            }
            st.session_state.ledger_data.insert(0, new_entry)
            save_audit_trail(st.session_state.ledger_data)
            st.toast("Telemetry record synchronized and saved to local file!", icon="✅")

    df = pd.DataFrame(st.session_state.ledger_data)
    total_requests = len(df)
    passed = len(df[df["Verdict"] == "PASS"])
    failed = len(df[df["Verdict"] == "FAIL"])
    total_tokens = df["Tokens_Processed"].sum()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Requests Audited", total_requests)
    m2.metric("Compliance Verdict: PASS ✅", passed, f"+{passed} Cleared")
    m3.metric("Security Violations: HALTED 🛑", failed, f"{failed} Blocked")
    m4.metric("Total Tokens Scrubbed 🪙", f"{total_tokens:,}")
    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📊 PII Risk Categories Detected")
        pii_df = df[df["Primary_PII_Type"] != "NONE"]
        if not pii_df.empty:
            fig1 = px.bar(pii_df, x="Primary_PII_Type", title="Incidents Found by Type", color="Primary_PII_Type")
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No risky PII data encountered yet.")

    with c2:
        st.subheader("⚖️ Triggered Regulatory Violations")
        fail_df = df[df["Triggered_Rule"] != "NONE"]
        if not fail_df.empty:
            fig2 = px.pie(fail_df, names="Triggered_Rule", hole=0.4, color_discrete_sequence=px.colors.sequential.Reds_r)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("System fully compliant. Zero rules broken.")

    st.subheader("📜 Forensic Compliance Ledger")
    search_query = st.text_input("🔍 Filter ledger by Triggered Rule or Payload ID:")

    if search_query:
        filtered_df = df[df["Triggered_Rule"].str.contains(search_query, case=False) | df["Payload_ID"].str.contains(search_query, case=False)]
    else:
        filtered_df = df

    st.dataframe(filtered_df, use_container_width=True)

# ==========================================
# TAB 2: PROMPT SANITIZER SANDBOX
# ==========================================
with tab2:
    st.subheader("🎛️ Automated IBM watsonx.ai Gateway Interceptor")
    st.markdown("Test the live pattern-matching logic. Type or paste a prompt containing sensitive information below to witness real-time redaction transformation.")

    default_prompt = (
        "System check prompt. Connection configuration string:\n"
        "User: admin_dev\n"
        "Email: internal-key@aura-shield.org\n"
        "Host IP: 10.0.115.42\n"
        "Billing Phone: +254 712 345 678\n"
        "Corporate Card: 4111-2222-3333-4444\n"
        "Auth Token: sk_live_51NzABC123secretTokenXYZ\n"
        "Please re-write this connection setup block."
    )

    user_prompt = st.text_area("Enter Raw Creative Prompt / AI Input:", value=default_prompt, height=180)
    
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        sanitize_clicked = st.button("🚀 Sanitize and Process Prompt")

    if user_prompt:
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        ip_regex = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        phone_regex = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        card_regex = r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        api_regex = r'(sk_live_[a-zA-Z0-9]{24,})|(eyJhbGciOi[a-zA-Z0-9-_.]+)'

        emails = len(re.findall(email_regex, user_prompt))
        ips = len(re.findall(ip_regex, user_prompt))
        phones = len(re.findall(phone_regex, user_prompt))
        cards = len(re.findall(card_regex, user_prompt))
        apis = len(re.findall(api_regex, user_prompt))
        
        total_pii = emails + ips + phones + cards + apis
        
        primary_vector = "NONE"
        if apis > 0: primary_vector = "API_SECRET_KEY"
        elif cards > 0: primary_vector = "CREDIT_CARD"
        elif emails > 0: primary_vector = "EMAIL"
        elif ips > 0: primary_vector = "IP_ADDRESS"
        elif phones > 0: primary_vector = "PHONE_NUMBER"

        sanitized_prompt = re.sub(email_regex, "[REDACTED_EMAIL_ADDRESS]", user_prompt)
        sanitized_prompt = re.sub(ip_regex, "[REDACTED_IP_V4]", sanitized_prompt)
        sanitized_prompt = re.sub(phone_regex, "[REDACTED_PHONE_NUMBER]", sanitized_prompt)
        sanitized_prompt = re.sub(card_regex, "[REDACTED_PCI_CREDIT_CARD]", sanitized_prompt)
        sanitized_prompt = re.sub(api_regex, "[REDACTED_BEARER_API_SECRET]", sanitized_prompt)

        if sanitize_clicked:
            new_payload_id = f"sandbox-{random.randint(1000, 9999)}"
            simulated_tokens = len(user_prompt.split()) + 22
            
            sandbox_log = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Payload_ID": new_payload_id,
                "PII_Masked_Count": total_pii,
                "Primary_PII_Type": primary_vector,
                "Verdict": "PASS",
                "Triggered_Rule": "NONE",
                "Tokens_Processed": simulated_tokens
            }
            st.session_state.ledger_data.insert(0, sandbox_log)
            save_audit_trail(st.session_state.ledger_data)
            st.success(f"Successfully processed and committed to disk database under ID: {new_payload_id}!")

        sc1, sc2 = st.columns(2)
        with sc1:
            st.info("### 🛑 Inbound Raw Prompt (Interception)")
            st.markdown(f"```text\n{user_prompt}\n```")
            
            if total_pii > 0:
                st.markdown("#### 🚨 Risks Flagged by Parser Middleware:")
                if apis > 0: st.error(f"✖ Found {apis} API Secret Token(s) — Extreme Threat")
                if cards > 0: st.error(f"✖ Found {cards} Credit Card String(s) — PCI Violation")
                if emails > 0: st.warning(f"⚠ Found {emails} Email Address(es) — Identity Risk")
                if ips > 0: st.warning(f"⚠ Found {ips} IPv4 Endpoint Address(es) — Infrastructure Leak")
                if phones > 0: st.warning(f"⚠ Found {phones} Phone Number Record(s) — Contact Leak")
            else:
                st.success("✅ Clean payload. Zero identity vectors detected.")
                
        with sc2:
            st.success("### 🚀 Outbound Sanitized Prompt (To watsonx.ai)")
            st.markdown(f"```text\n{sanitized_prompt}\n```")
            st.caption("Secure scrub completed. Fully dynamic mask prevents cloud tracing vectors while maintaining structural query integrity.")