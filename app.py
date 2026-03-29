"""
CRM Antonio Tritto - Private Banking
App Streamlit con Supabase - Design Premium Dark Theme
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from supabase import create_client, Client
import os

# ========== CONFIGURAZIONE ==========

st.set_page_config(
    page_title="CRM Antonio Tritto",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Premium Dark Theme
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Main Theme */
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a2332 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
        border-right: 1px solid #30363d;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #c9d1d9;
    }

    /* Logo Container */
    .logo-container {
        display: flex;
        align-items: center;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .logo-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        margin-right: 12px;
    }

    .logo-text {
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
    }

    .logo-subtitle {
        color: #8b949e;
        font-size: 0.75rem;
    }

    /* Menu Section Headers */
    .menu-header {
        color: #8b949e;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 1rem 0 0.5rem 0;
        margin-top: 1rem;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #21262d 0%, #1a2332 100%);
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
    }

    .kpi-card-blue {
        border-left: 4px solid #58a6ff;
    }

    .kpi-card-green {
        border-left: 4px solid #3fb950;
    }

    .kpi-card-orange {
        border-left: 4px solid #d29922;
    }

    .kpi-card-yellow {
        border-left: 4px solid #f0c000;
    }

    .kpi-icon {
        position: absolute;
        top: 1rem;
        right: 1rem;
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }

    .kpi-icon-blue { background: rgba(88, 166, 255, 0.2); }
    .kpi-icon-green { background: rgba(63, 185, 80, 0.2); }
    .kpi-icon-orange { background: rgba(210, 153, 34, 0.2); }
    .kpi-icon-yellow { background: rgba(240, 192, 0, 0.2); }

    .kpi-label {
        color: #8b949e;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    .kpi-value {
        color: #f0f6fc;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .kpi-value-blue { color: #58a6ff; }
    .kpi-value-green { color: #3fb950; }
    .kpi-value-orange { color: #d29922; }
    .kpi-value-yellow { color: #f0c000; }

    .kpi-change {
        font-size: 0.8rem;
    }

    .kpi-change-up { color: #3fb950; }
    .kpi-change-down { color: #f85149; }

    /* Section Cards */
    .section-card {
        background: #21262d;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .section-title {
        color: #f0f6fc;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }

    .section-subtitle {
        color: #8b949e;
        font-size: 0.8rem;
        margin-bottom: 1rem;
    }

    /* Pipeline Bar */
    .pipeline-row {
        display: flex;
        align-items: center;
        margin-bottom: 0.75rem;
    }

    .pipeline-label {
        width: 140px;
        color: #c9d1d9;
        font-size: 0.85rem;
    }

    .pipeline-bar-container {
        flex: 1;
        height: 28px;
        background: #30363d;
        border-radius: 6px;
        overflow: hidden;
        margin: 0 1rem;
    }

    .pipeline-bar {
        height: 100%;
        border-radius: 6px;
        display: flex;
        align-items: center;
        padding-left: 10px;
        color: white;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .pipeline-value {
        color: #8b949e;
        font-size: 0.85rem;
        min-width: 80px;
        text-align: right;
    }

    /* Alert Items */
    .alert-item {
        display: flex;
        align-items: center;
        padding: 0.75rem;
        background: #161b22;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }

    .alert-icon {
        width: 36px;
        height: 36px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
        font-size: 1rem;
    }

    .alert-icon-warning { background: rgba(210, 153, 34, 0.2); }
    .alert-icon-danger { background: rgba(248, 81, 73, 0.2); }
    .alert-icon-info { background: rgba(88, 166, 255, 0.2); }

    .alert-content {
        flex: 1;
    }

    .alert-title {
        color: #f0f6fc;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .alert-subtitle {
        color: #8b949e;
        font-size: 0.75rem;
    }

    .alert-count {
        color: #f0f6fc;
        font-size: 1.1rem;
        font-weight: 600;
    }

    /* Deal Item */
    .deal-item {
        display: flex;
        align-items: center;
        padding: 0.6rem 0;
        border-bottom: 1px solid #30363d;
    }

    .deal-item:last-child {
        border-bottom: none;
    }

    .deal-number {
        width: 24px;
        height: 24px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 12px;
    }

    .deal-info {
        flex: 1;
    }

    .deal-name {
        color: #f0f6fc;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .deal-stage {
        color: #8b949e;
        font-size: 0.75rem;
    }

    .deal-value {
        color: #3fb950;
        font-size: 1rem;
        font-weight: 600;
    }

    /* Login Page */
    .login-container {
        max-width: 400px;
        margin: 4rem auto;
        padding: 2rem;
        background: linear-gradient(135deg, #21262d 0%, #1a2332 100%);
        border: 1px solid #30363d;
        border-radius: 20px;
        text-align: center;
    }

    .login-logo {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-weight: bold;
        color: white;
        margin: 0 auto 1.5rem;
    }

    .login-title {
        color: #f0f6fc;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .login-subtitle {
        color: #8b949e;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    /* Input Fields */
    .stTextInput > div > div > input {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        color: #f0f6fc;
        padding: 0.75rem 1rem;
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #161b22;
    }

    ::-webkit-scrollbar-thumb {
        background: #30363d;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #484f58;
    }

    /* User profile in sidebar */
    .user-profile {
        display: flex;
        align-items: center;
        padding: 1rem;
        background: #161b22;
        border-radius: 10px;
        margin-top: auto;
    }

    .user-avatar {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        margin-right: 10px;
    }

    .user-name {
        color: #f0f6fc;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .user-email {
        color: #8b949e;
        font-size: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# ========== SUPABASE ==========

@st.cache_resource
def init_supabase():
    url = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", ""))
    key = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", ""))
    if url and key:
        return create_client(url, key)
    return None

supabase = init_supabase()

# Stadi pipeline con colori
STAGES = ['Lead', 'Contatto', 'Contratto Inviato', 'Negoziazione', 'Proposta Inviata', 'Qualificato', 'Cliente Attivo']
STAGE_COLORS = {
    'Lead': '#58a6ff',
    'Contatto': '#8b5cf6',
    'Contratto Inviato': '#a855f7',
    'Negoziazione': '#d946ef',
    'Proposta Inviata': '#ec4899',
    'Qualificato': '#f97316',
    'Cliente Attivo': '#3fb950'
}
STAGE_PROB = {'Lead': 10, 'Contatto': 20, 'Contratto Inviato': 40, 'Negoziazione': 50, 'Proposta Inviata': 60, 'Qualificato': 75, 'Cliente Attivo': 100}

# ========== DATABASE FUNCTIONS ==========

def get_contatti():
    if not supabase:
        return pd.DataFrame()
    try:
        response = supabase.table('contatti').select('*').execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except:
        return pd.DataFrame()

def get_pipeline():
    if not supabase:
        return pd.DataFrame()
    try:
        response = supabase.table('pipeline').select('*').execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except:
        return pd.DataFrame()

def add_contatto(data):
    if not supabase:
        return None
    try:
        response = supabase.table('contatti').insert(data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        st.error(f"Errore: {e}")
        return None

def update_contatto(id, data):
    if not supabase:
        return None
    try:
        response = supabase.table('contatti').update(data).eq('id', id).execute()
        return response.data[0] if response.data else None
    except:
        return None

def delete_contatto(id):
    if not supabase:
        return False
    try:
        supabase.table('contatti').delete().eq('id', id).execute()
        return True
    except:
        return False

def add_deal(data):
    if not supabase:
        return None
    try:
        response = supabase.table('pipeline').insert(data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        st.error(f"Errore: {e}")
        return None

def update_deal(id, data):
    if not supabase:
        return None
    try:
        response = supabase.table('pipeline').update(data).eq('id', id).execute()
        return response.data[0] if response.data else None
    except:
        return None

def delete_deal(id):
    if not supabase:
        return False
    try:
        supabase.table('pipeline').delete().eq('id', id).execute()
        return True
    except:
        return False

# ========== AUTH FUNCTIONS ==========

def show_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-logo">AT</div>
            <div class="login-title">CRM Antonio Tritto</div>
            <div class="login-subtitle">Private Banking Dashboard</div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Accedi", "Registrati"])

        with tab1:
            email = st.text_input("Email", placeholder="tua@email.com", key="login_email")
            password = st.text_input("Password", type="password", placeholder="La tua password", key="login_pass")

            if st.button("Accedi", key="btn_login"):
                if email and password:
                    try:
                        response = supabase.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })
                        st.session_state.user = response.user
                        st.session_state.logged_in = True
                        st.rerun()
                    except Exception as e:
                        st.error("Email o password non validi")
                else:
                    st.warning("Inserisci email e password")

            st.markdown("---")
            st.markdown("<center><small style='color: #8b949e;'>oppure</small></center>", unsafe_allow_html=True)

            if st.button("🔑 Accesso Demo", key="btn_demo"):
                st.session_state.logged_in = True
                st.session_state.user = {"email": "demo@antoniotritto.com"}
                st.rerun()

        with tab2:
            reg_email = st.text_input("Email", placeholder="tua@email.com", key="reg_email")
            reg_password = st.text_input("Password", type="password", placeholder="Crea password", key="reg_pass")
            reg_password2 = st.text_input("Conferma Password", type="password", placeholder="Conferma password", key="reg_pass2")

            if st.button("Registrati", key="btn_register"):
                if reg_password != reg_password2:
                    st.error("Le password non coincidono")
                elif reg_email and reg_password:
                    try:
                        response = supabase.auth.sign_up({
                            "email": reg_email,
                            "password": reg_password
                        })
                        st.success("Registrazione completata! Controlla la tua email.")
                    except Exception as e:
                        st.error(f"Errore registrazione: {e}")

# ========== SIDEBAR ==========

def show_sidebar():
    with st.sidebar:
        # Logo
        st.markdown("""
        <div class="logo-container">
            <div class="logo-icon">AT</div>
            <div>
                <div class="logo-text">CRM Antonio Tritto</div>
                <div class="logo-subtitle">PRIVATE BANKING</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Menu Principale
        st.markdown('<div class="menu-header">MENU PRINCIPALE</div>', unsafe_allow_html=True)

        menu_options = {
            "Dashboard": "📊",
            "Contatti": "👥",
            "Pipeline": "🎯",
            "Contratti": "📄"
        }

        selected = st.radio(
            "Menu",
            list(menu_options.keys()),
            format_func=lambda x: f"{menu_options[x]} {x}",
            label_visibility="collapsed"
        )

        # Operatività
        st.markdown('<div class="menu-header">OPERATIVITÀ</div>', unsafe_allow_html=True)

        op_options = ["Rubrica Contatti", "Chiamate", "AUM Tracking", "Email Marketing"]
        op_selected = st.radio("Operatività", op_options, label_visibility="collapsed", key="op_menu")

        # Analisi
        st.markdown('<div class="menu-header">ANALISI</div>', unsafe_allow_html=True)

        an_options = ["Dashboard Revenue", "Analisi Conversione", "Cash Flow 12 mesi", "Analytics", "Report"]
        an_selected = st.radio("Analisi", an_options, label_visibility="collapsed", key="an_menu")

        st.markdown("---")

        # User Profile
        user_email = st.session_state.get('user', {}).get('email', 'demo@antoniotritto.com')
        st.markdown(f"""
        <div class="user-profile">
            <div class="user-avatar">AT</div>
            <div>
                <div class="user-name">Antonio Tritto</div>
                <div class="user-email">{user_email}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Esci", key="logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

        return selected

# ========== DASHBOARD ==========

def page_dashboard():
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h1 style='color: #f0f6fc; margin-bottom: 0;'>Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8b949e;'>Panoramica performance e KPI</p>", unsafe_allow_html=True)
    with col2:
        col_a, col_b = st.columns(2)
        with col_a:
            st.button("🔄 Aggiorna")
        with col_b:
            st.button("⚡ Azione Rapida")

    # Load data
    contatti = get_contatti()
    pipeline = get_pipeline()

    # KPI Cards
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    aum_totale = pipeline['aum_previsto'].sum() if len(pipeline) > 0 and 'aum_previsto' in pipeline.columns else 0
    clienti_attivi = len(pipeline[pipeline['stage'] == 'Cliente Attivo']) if len(pipeline) > 0 and 'stage' in pipeline.columns else 0
    pipeline_value = pipeline[pipeline['stage'] != 'Cliente Attivo']['aum_previsto'].sum() if len(pipeline) > 0 else 0
    fee_annuali = aum_totale * 0.005  # 0.5% fee

    with col1:
        st.markdown(f"""
        <div class="kpi-card kpi-card-blue">
            <div class="kpi-icon kpi-icon-blue">💰</div>
            <div class="kpi-label">AUM TOTALE</div>
            <div class="kpi-value kpi-value-blue">€{aum_totale/1000000:.2f}M</div>
            <div class="kpi-change kpi-change-up">↑ vs mese precedente</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card kpi-card-green">
            <div class="kpi-icon kpi-icon-green">👥</div>
            <div class="kpi-label">CLIENTI ATTIVI</div>
            <div class="kpi-value kpi-value-green">{clienti_attivi}</div>
            <div class="kpi-change kpi-change-up">↑ nuovi clienti</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card kpi-card-orange">
            <div class="kpi-icon kpi-icon-orange">📊</div>
            <div class="kpi-label">PIPELINE VALUE</div>
            <div class="kpi-value kpi-value-orange">€{pipeline_value/1000000:.2f}M</div>
            <div class="kpi-change">{len(pipeline)} deal attivi</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card kpi-card-yellow">
            <div class="kpi-icon kpi-icon-yellow">💵</div>
            <div class="kpi-label">FEE ANNUALI</div>
            <div class="kpi-value kpi-value-yellow">€{fee_annuali/1000:.0f}K</div>
            <div class="kpi-change">Tasso conv: 40%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Sales Pipeline & Distribution
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Sales Pipeline</div>
            <div class="section-subtitle">Distribuzione deal per stage</div>
        """, unsafe_allow_html=True)

        if len(pipeline) > 0 and 'stage' in pipeline.columns:
            for stage in STAGES:
                stage_data = pipeline[pipeline['stage'] == stage]
                count = len(stage_data)
                aum = stage_data['aum_previsto'].sum() if 'aum_previsto' in stage_data.columns else 0
                max_aum = pipeline['aum_previsto'].max() if 'aum_previsto' in pipeline.columns else 1
                width = (aum / max_aum * 100) if max_aum > 0 else 0
                color = STAGE_COLORS.get(stage, '#667eea')

                st.markdown(f"""
                <div class="pipeline-row">
                    <div class="pipeline-label">{stage}</div>
                    <div class="pipeline-bar-container">
                        <div class="pipeline-bar" style="width: {max(width, 5)}%; background: {color};">{count}</div>
                    </div>
                    <div class="pipeline-value">€{aum/1000:.0f}K</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Distribuzione Clienti</div>
            <div class="section-subtitle">Per tier di valore</div>
        </div>
        """, unsafe_allow_html=True)

        if len(contatti) > 0 and 'tier' in contatti.columns:
            tier_counts = contatti['tier'].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=tier_counts.index,
                values=tier_counts.values,
                hole=0.6,
                marker_colors=['#3fb950', '#58a6ff', '#d29922', '#8b949e']
            )])
            fig.update_layout(
                showlegend=True,
                legend=dict(orientation="v", x=1, y=0.5, font=dict(color='#c9d1d9')),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=20, b=20),
                height=250
            )
            st.plotly_chart(fig, use_container_width=True)

    # Bottom Row: Alerts, Top Opportunities, Activity
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Alert & Notifiche</div>
            <div class="section-subtitle">Azioni richieste</div>

            <div class="alert-item">
                <div class="alert-icon alert-icon-warning">📞</div>
                <div class="alert-content">
                    <div class="alert-title">Follow-up Scaduti</div>
                    <div class="alert-subtitle">Chiamate da recuperare</div>
                </div>
                <div class="alert-count">0</div>
            </div>

            <div class="alert-item">
                <div class="alert-icon alert-icon-danger">⚠️</div>
                <div class="alert-content">
                    <div class="alert-title">Deal in Stallo</div>
                    <div class="alert-subtitle">Più di 14 giorni</div>
                </div>
                <div class="alert-count">7</div>
            </div>

            <div class="alert-item">
                <div class="alert-icon alert-icon-info">📋</div>
                <div class="alert-content">
                    <div class="alert-title">Contratti in Scadenza</div>
                    <div class="alert-subtitle">Prossimi 60 giorni</div>
                </div>
                <div class="alert-count">0</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Top Opportunità</div>
            <div class="section-subtitle">Deal più promettenti</div>
        """, unsafe_allow_html=True)

        if len(pipeline) > 0:
            top_deals = pipeline.nlargest(5, 'aum_previsto') if 'aum_previsto' in pipeline.columns else pipeline.head(5)
            for i, (_, deal) in enumerate(top_deals.iterrows(), 1):
                nome = deal.get('nome_deal', 'N/A')
                stage = deal.get('stage', 'N/A')
                prob = deal.get('probabilita', 0)
                aum = deal.get('aum_previsto', 0)
                st.markdown(f"""
                <div class="deal-item">
                    <div class="deal-number">{i}</div>
                    <div class="deal-info">
                        <div class="deal-name">{nome}</div>
                        <div class="deal-stage">{stage} - {prob}%</div>
                    </div>
                    <div class="deal-value">€{aum/1000:.0f}K</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Attività 30 Giorni</div>
            <div class="section-subtitle">Riepilogo operativo</div>
        </div>
        """, unsafe_allow_html=True)

        # Activity chart
        activities = ['Chiamate', 'Email', 'Meeting', 'Nuovi', 'Chiusi']
        values = [15, 12, 8, 5, 3]

        fig = go.Figure(data=[go.Bar(
            x=activities,
            y=values,
            marker_color=['#58a6ff', '#58a6ff', '#58a6ff', '#58a6ff', '#58a6ff']
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=40),
            height=200,
            xaxis=dict(color='#8b949e'),
            yaxis=dict(color='#8b949e', gridcolor='#30363d')
        )
        st.plotly_chart(fig, use_container_width=True)

# ========== CONTATTI ==========

def page_contatti():
    st.markdown("<h1 style='color: #f0f6fc;'>👥 Gestione Contatti</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Nuovo Contatto", type="primary"):
            st.session_state.show_new_contact = True

    if st.session_state.get('show_new_contact', False):
        with st.expander("Nuovo Contatto", expanded=True):
            with st.form("new_contact"):
                col1, col2 = st.columns(2)
                with col1:
                    nome = st.text_input("Nome *")
                    cognome = st.text_input("Cognome")
                    email = st.text_input("Email")
                    telefono = st.text_input("Telefono")
                with col2:
                    azienda = st.text_input("Azienda")
                    ruolo = st.text_input("Ruolo")
                    tier = st.selectbox("Tier", ['A', 'B', 'C'])
                    fonte = st.text_input("Fonte")

                aum_potenziale = st.number_input("AUM Potenziale (€)", min_value=0, value=0)
                note = st.text_area("Note")

                if st.form_submit_button("💾 Salva Contatto"):
                    if nome:
                        data = {
                            'nome': nome, 'cognome': cognome, 'email': email,
                            'telefono': telefono, 'azienda': azienda, 'ruolo': ruolo,
                            'tier': tier, 'fonte': fonte, 'aum_potenziale': aum_potenziale,
                            'note': note, 'is_cliente': False
                        }
                        if add_contatto(data):
                            st.success("✅ Contatto creato!")
                            st.session_state.show_new_contact = False
                            st.rerun()

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_tier = st.selectbox("Tier", ['Tutti', 'A', 'B', 'C'])
    with col2:
        filtro_tipo = st.selectbox("Tipo", ['Tutti', 'Clienti', 'Prospect'])
    with col3:
        filtro_search = st.text_input("🔍 Cerca", placeholder="Nome, azienda...")

    contatti = get_contatti()

    if len(contatti) > 0:
        if filtro_tier != 'Tutti' and 'tier' in contatti.columns:
            contatti = contatti[contatti['tier'] == filtro_tier]
        if filtro_tipo == 'Clienti' and 'is_cliente' in contatti.columns:
            contatti = contatti[contatti['is_cliente'] == True]
        elif filtro_tipo == 'Prospect' and 'is_cliente' in contatti.columns:
            contatti = contatti[contatti['is_cliente'] == False]
        if filtro_search:
            contatti = contatti[
                contatti['nome'].str.contains(filtro_search, case=False, na=False) |
                contatti.get('cognome', pd.Series()).str.contains(filtro_search, case=False, na=False) |
                contatti.get('azienda', pd.Series()).str.contains(filtro_search, case=False, na=False)
            ]

        st.dataframe(contatti, use_container_width=True, hide_index=True)
    else:
        st.info("Nessun contatto. Clicca 'Nuovo Contatto' per iniziare.")

# ========== PIPELINE ==========

def page_pipeline():
    st.markdown("<h1 style='color: #f0f6fc;'>🎯 Sales Pipeline</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Nuovo Deal", type="primary"):
            st.session_state.show_new_deal = True

    if st.session_state.get('show_new_deal', False):
        with st.expander("Nuovo Deal", expanded=True):
            with st.form("new_deal"):
                col1, col2 = st.columns(2)
                with col1:
                    nome_deal = st.text_input("Nome Deal *")
                    stage = st.selectbox("Stage", STAGES)
                    aum_previsto = st.number_input("AUM Previsto (€)", min_value=0, value=0)
                with col2:
                    fonte = st.text_input("Fonte")
                    responsabile = st.text_input("Responsabile", value="Antonio Tritto")
                    fee = st.number_input("Fee %", min_value=0.0, max_value=5.0, value=0.5)

                note = st.text_area("Note")

                if st.form_submit_button("💾 Salva Deal"):
                    if nome_deal:
                        data = {
                            'nome_deal': nome_deal, 'stage': stage,
                            'aum_previsto': aum_previsto, 'probabilita': STAGE_PROB.get(stage, 10),
                            'fee_percentuale': fee, 'fee_stimata': aum_previsto * fee / 100,
                            'fonte': fonte, 'responsabile': responsabile, 'note': note
                        }
                        if add_deal(data):
                            st.success("✅ Deal creato!")
                            st.session_state.show_new_deal = False
                            st.rerun()

    pipeline = get_pipeline()

    if len(pipeline) > 0 and 'stage' in pipeline.columns:
        # Kanban view
        cols = st.columns(len(STAGES))

        for i, stage in enumerate(STAGES):
            with cols[i]:
                stage_deals = pipeline[pipeline['stage'] == stage]
                count = len(stage_deals)
                aum = stage_deals['aum_previsto'].sum() if 'aum_previsto' in stage_deals.columns else 0
                color = STAGE_COLORS.get(stage, '#667eea')

                st.markdown(f"""
                <div style="background: {color}20; border-radius: 8px; padding: 0.5rem; margin-bottom: 0.5rem; border-top: 3px solid {color};">
                    <div style="color: {color}; font-weight: 600; font-size: 0.85rem;">{stage}</div>
                    <div style="color: #8b949e; font-size: 0.75rem;">{count} deal | €{aum/1000:.0f}K</div>
                </div>
                """, unsafe_allow_html=True)

                for _, deal in stage_deals.iterrows():
                    st.markdown(f"""
                    <div style="background: #21262d; border: 1px solid #30363d; border-radius: 8px; padding: 0.75rem; margin-bottom: 0.5rem;">
                        <div style="color: #f0f6fc; font-weight: 500;">{deal.get('nome_deal', 'N/A')}</div>
                        <div style="color: #3fb950; font-size: 0.9rem;">€{deal.get('aum_previsto', 0)/1000:.0f}K</div>
                        <div style="color: #8b949e; font-size: 0.75rem;">{deal.get('probabilita', 0)}%</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("---")

        # Move deal
        col1, col2, col3 = st.columns(3)
        with col1:
            deal_options = pipeline['id'].tolist()
            deal_names = {row['id']: row['nome_deal'] for _, row in pipeline.iterrows()}
            deal_id = st.selectbox("Seleziona Deal", deal_options, format_func=lambda x: deal_names.get(x, str(x)))
        with col2:
            nuovo_stage = st.selectbox("Sposta a", STAGES)
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Sposta"):
                update_deal(deal_id, {'stage': nuovo_stage, 'probabilita': STAGE_PROB.get(nuovo_stage, 10)})
                st.success(f"Deal spostato a {nuovo_stage}")
                st.rerun()
    else:
        st.info("Nessun deal. Clicca 'Nuovo Deal' per iniziare.")

# ========== CONTRATTI ==========

def page_contratti():
    st.markdown("<h1 style='color: #f0f6fc;'>📄 Contratti</h1>", unsafe_allow_html=True)
    st.info("Sezione in sviluppo - Gestione contratti e documenti")

# ========== MAIN ==========

def main():
    # Check login
    if not st.session_state.get('logged_in', False):
        show_login()
        return

    # Show sidebar and get selected page
    selected = show_sidebar()

    # Route to page
    if selected == "Dashboard":
        page_dashboard()
    elif selected == "Contatti":
        page_contatti()
    elif selected == "Pipeline":
        page_pipeline()
    elif selected == "Contratti":
        page_contratti()

if __name__ == "__main__":
    main()
