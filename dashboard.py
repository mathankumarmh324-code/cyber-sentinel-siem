import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Page Setup & Dark Theme Configuration
st.set_page_config(
    page_title="Cyber Sentinel | SOC Operations Portal",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Cyberpunk / SIEM Dark Theme CSS
st.markdown("""
<style>
    .stApp { background-color: #090C10 !important; color: #E6EDF3; }
    h1, h2, h3 { color: #00E5FF !important; font-family: 'Consolas', 'Segoe UI', monospace; }
    
    div[data-testid="stMetric"] {
        background: #161B22;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #30363D;
        border-left: 6px solid #00E5FF;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    div[data-testid="stMetricValue"] { color: #58A6FF !important; font-size: 34px; font-weight: bold; }
    div[data-testid="stMetricLabel"] { color: #8B949E !important; font-size: 14px; text-transform: uppercase; }

    .stDataFrame {
        border: 1px solid #30363D !important;
        border-radius: 10px;
        background-color: #161B22 !important;
    }
    hr { border-color: #30363D !important; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Cyber Threat & Anomaly Sentinel")
st.caption("Autonomous Real-Time Security Operations Center (SOC) Monitoring Dashboard")
st.markdown("---")

# Enhanced Attack Vector Parser
def parse_attack_type(row):
    evidence_lower = str(row['evidence']).lower()
    risk = row['risk_score']
    
    if "failed login" in evidence_lower or "auth" in evidence_lower:
        return "🔑 BRUTE FORCE"
    elif "outbound" in evidence_lower or "bytes" in evidence_lower or "traffic" in evidence_lower:
        return "📡 DATA EXFILTRATION"
    elif "port" in evidence_lower or "scan" in evidence_lower:
        return "🔍 PORT SCANNING"
    elif risk < 40:
        return "🟢 RECONNAISSANCE"
    return "⚡ ANOMALOUS BEHAVIOR"

# Auto-Refresh Fragment
@st.fragment(run_every=2)
def render_dashboard():
    try:
        conn = sqlite3.connect("file:alerts.db?mode=ro", uri=True, timeout=10)
        total_count = conn.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
        df = pd.read_sql_query("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 200", conn)
        conn.close()
    except Exception:
        df = pd.DataFrame()
        total_count = 0

    if not df.empty:
        # Dynamic Attack Vector classification across full row data
        df['Attack Vector'] = df.apply(parse_attack_type, axis=1)

        # High Level Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        high_risk_alerts = len(df[df['risk_score'] >= 70])
        max_risk = df['risk_score'].max()
        unique_ips = df['source_ip'].nunique()

        col1.metric("Total Live Logs", total_count)
        col2.metric("Critical Threats (Risk ≥ 70)", high_risk_alerts)
        col3.metric("Peak Risk Severity", f"{max_risk}/100")
        col4.metric("Attacking IP Sources", unique_ips)

        st.markdown("<br>", unsafe_allow_html=True)

        left_col, right_col = st.columns([1.3, 1])

        with left_col:
            st.subheader("🚨 Real-Time Security Incident Stream")
            
            def style_classification(val):
                if val == 'MALICIOUS':
                    return 'background-color: #4C0000; color: #FF4D4D; font-weight: bold;'
                elif val == 'SUSPICIOUS':
                    return 'background-color: #3D2B00; color: #FFC107; font-weight: bold;'
                return 'background-color: #0D331A; color: #00E676; font-weight: bold;'

            display_df = df[['timestamp', 'source_ip', 'Attack Vector', 'classification', 'risk_score', 'evidence']].copy()
            display_df['timestamp'] = display_df['timestamp'].apply(lambda x: str(x).split('.')[0].replace('T', ' '))

            st.dataframe(
                display_df.style.map(style_classification, subset=['classification']),
                use_container_width=True,
                height=420,
                hide_index=True
            )

        with right_col:
            st.subheader("📊 Attack Vectors & Threat Severity")
            
            fig = px.histogram(
                df, 
                x="risk_score", 
                nbins=15,
                color="Attack Vector",
                color_discrete_sequence=px.colors.qualitative.Bold,
                labels={'risk_score': 'Risk Score (0-100)', 'count': 'Incidents'},
                template="plotly_dark",
                title="Risk Spectrum by Incident Type"
            )
            fig.update_layout(
                paper_bgcolor="#161B22",
                plot_bgcolor="#161B22",
                font=dict(color="#E6EDF3"),
                margin=dict(l=20, r=20, t=40, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("⚡ Live stream waiting... Run generator and main engine.")

render_dashboard()