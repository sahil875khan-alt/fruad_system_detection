import streamlit as st

# Page Configuration (Must be the first streamlit command)
st.set_page_config(
    page_title="FinGuard AML Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for styling and professional look
st.markdown("""
    <style>
    .main-header {
        font-size: 28px;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-text {
        color: #64748B;
        font-size: 14px;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F8FAFC;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<p class="main-header">🛡️ Intelligent Financial Fraud & AML Monitoring System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">AI & Rule-Based Real-time Transaction Security & Risk Assessment Dashboard</p>', unsafe_allow_html=True)

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Transactions Scanned", value="1,428", delta="+12 today")
with col2:
    st.metric(label="High-Risk Alerts", value="23", delta="-3 from avg", delta_color="inverse")
with col3:
    st.metric(label="Blocked Fraud Volume", value="₹14.2 Lakhs", delta="+₹2.1L")
with col4:
    st.metric(label="System Status", value="🟢 Active", delta="Real-time")

st.divider()

# Sidebar for Live Testing
st.sidebar.header("🔍 Test Live Transaction")
st.sidebar.markdown("Check custom data against fraud & AML rules.")

amount = st.sidebar.number_input("Transaction Amount (₹)", min_value=100, max_value=1000000, value=49000, step=1000)
time_gap = st.sidebar.slider("Minutes since last transaction", 1, 120, 2)
location_risk = st.sidebar.selectbox("Transaction Location", ["Local (Home City)", "Other State", "International High-Risk"])

# Fraud Detection Logic
def analyze(amt, gap, loc):
    score = 0
    reasons = []
    
    if amt >= 80000:
        score += 50
        reasons.append("Abnormally high transaction amount (> ₹80,000)")
    
    if 45000 <= amt < 50000 and gap <= 5:
        score += 45
        reasons.append("Potential AML Splitting: Multiple rapid transfers just below ₹50k reporting limit")
        
    if gap <= 3:
        score += 30
        reasons.append(f"Rapid transaction frequency ({gap} mins gap between transfers)")
        
    if loc == "International High-Risk":
        score += 25
        reasons.append("Geographical anomaly: Initiated from high-risk international zone")
        
    score = min(score, 100)
    
    if score >= 70:
        return "HIGH RISK (FRAUD ALERT)", score, reasons, "red"
    elif score >= 40:
        return "MEDIUM RISK (WATCH)", score, reasons, "orange"
    else:
        return "LOW RISK (SAFE)", score, reasons, "green"

status, score, reasons, color = analyze(amount, time_gap, location_risk)

# Main Dashboard Layout
left_column, right_column = st.columns([1, 1])

with left_column:
    st.subheader("Live Analysis Result")
    st.markdown(f"### Risk Status: :{color}[{status}]")
    st.progress(score / 100)
    st.write(f"**Calculated Risk Score:** `{score}/100`")
    
    if reasons:
        st.markdown("**Explainability (Why flagged):**")
        for r in reasons:
            st.error(r)
    else:
        st.success("Explainability: Transaction behaviour pattern is normal and safe.")

with right_column:
    st.subheader("Recent Suspicious Alerts")
    alert_data = [
        {"ID": "TXN-1042", "Sender": "ACC_09", "Amount": "₹49,000", "Flag": "AML Splitting"},
        {"ID": "TXN-1045", "Sender": "ACC_15", "Amount": "₹95,000", "Flag": "High Amount"},
        {"ID": "TXN-1089", "Sender": "ACC_22", "Amount": "₹48,500", "Flag": "Rapid Transfer"},
    ]
    st.table(alert_data)
    