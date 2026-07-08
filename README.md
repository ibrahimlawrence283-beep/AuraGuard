# AuraGuard | Creative Workflows & AI Governance Shield

A real-time telemetry, PII redaction tracking, and intellectual property (IP) protection middleware interface built to act as a secure compliance layer for enterprise creative workflows and media deployments leveraging **IBM watsonx.ai**.

---

## 🎯 Challenge Alignment
- **Selected Challenge Theme:** Creative Production & Workflows (AI Safety & Compliance Layer)
- **Primary Development Core:** Managed via automated pattern matching, dynamic regex filtration arrays, and secure payload interception.

---

## 📋 Problem Statement
As creative agencies, media houses, and digital storytelling platforms rapidly integrate large language models (LLMs) into their content generation engines via APIs like IBM watsonx.ai, they face an immediate compliance and security crisis. 

Content creators, writers, and automated agents frequently pass unstructured prompt data containing sensitive personal information (PII), proprietary scripts, unreleased brand assets, and digital credentials directly to third-party environments. This data exposure risks immediate regulatory breaches (GDPR, CCPA) and compromises creative intellectual property, restricting enterprises from safely leveraging AI tools in production.

---

## 🚀 Solution Description
**AuraGuard** serves as an inline, defensive proxy gateway shield tailor-made for creative production environments. It sits symmetrically between content applications and downstream enterprise foundation models. 

AuraGuard intercepts prompt transactions in real-time, instantly identifying and masking high-risk identity signatures, creative text leakage, and credentials before they ever touch the network. By stripping out vulnerable vectors while preserving the semantic and narrative structure of the prompt, AuraGuard allows creative professionals to maximize their utilization of advanced AI tools safely and compliantly.

---

## 🛠️ AI Approach & Architecture

AuraGuard employs a decoupled, multi-stage interception pipeline optimized for seamless, low-latency content workflows:

1. **Inbound Gateway Interception:** The middleware captures raw creative agent payloads or text prompts at the generation entry interface.
2. **Deterministic Token & Pattern Parsing:** Advanced multi-track regular expression (Regex) matrices inspect the text strings to catch high-risk data signatures, including:
   - Global Communication Identifiers (Emails, Phone Numbers)
   - Creative & Operational Infrastructure Assets (IPv4 Endpoints)
   - Exposed API Keys and Digital Content Platform Authentication Materials
3. **Dynamic Synthetic Masking Layer:** Flagged elements are dynamically rewritten into standardized structural tokens (e.g., `[REDACTED_EMAIL_ADDRESS]`, `[REDACTED_CREDENTIALS]`). This maintains the narrative, creative, and grammatical integrity of the query, ensuring the downstream model retains context.
4. **Persistent Audit & Forensic Ledger:** Every compliance event, text metrics check, and security verdict is committed to a local persistent data warehouse file (`auraguard_audit.csv`), supplying a comprehensive trail for media compliance officers.

---

## 💼 How IBM Integration is Orchestrated
AuraGuard is architected intentionally to serve as a secure gateway layer for **IBM watsonx.ai** within creative industries. 
- It functions as a pre-processing content sanitization proxy. 
- It guarantees that any prompt payload delivered downstream to IBM foundation models is verified clean, fully compliant, and stripped of operational risk factors. 
- This approach empowers creative agencies and developers to maximize their utilization of enterprise cloud tools while ensuring 100% adherence to data boundaries.

---

## 💻 Local Installation & Quick Start

To execute the AuraGuard telemetry dashboard and sanitizer sandbox interface on a local environment:

### Prerequisites
Ensure your local environment includes Python 3.8+ and the necessary frontend and data libraries:
```bash
pip install streamlit pandas plotly
