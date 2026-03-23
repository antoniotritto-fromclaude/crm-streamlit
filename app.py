"""
CRM Antonio Tritto - Private Banking
App Streamlit con Supabase
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from supabase import create_client, Client
import os

# Configurazione pagina
st.set_page_config(
    page_title="CRM Private Banking",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizzato
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1e3a5f;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    .stage-prospect { background-color: #e3f2fd; }
    .stage-lead { background-color: #fff3e0; }
    .stage-contatto { background-color: #f3e5f5; }
    .stage-appuntamento { background-color: #e8f5e9; }
    .stage-chiusura { background-color: #fff8e1; }
    .stage-cliente { background-color: #e8f5e9; }
</style>
""", unsafe_allow_html=True)

# Inizializza Supabase
@st.cache_resource
def init_supabase():
    url = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", ""))
    key = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", ""))
    if url and key:
        return create_client(url, key)
    return None

supabase = init_supabase()

# Stadi pipeline
STAGES = ['Prospect', 'Lead', 'Primo Contatto', 'Appuntamento', 'Secondo Appuntamento', 'Chiusura', 'Cliente Attivo']
STAGE_PROB = {'Prospect': 10, 'Lead': 20, 'Primo Contatto': 40, 'Appuntamento': 60, 'Secondo Appuntamento': 75, 'Chiusura': 90, 'Cliente Attivo': 100, 'Chiuso Perso': 0}

# ========== FUNZIONI DATABASE ==========

def get_contatti():
    """Recupera tutti i contatti"""
    if not supabase:
        return pd.DataFrame()
    try:
        response = supabase.table('contatti').select('*').execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception as e:
        st.error(f"Errore caricamento contatti: {e}")
        return pd.DataFrame()

def get_pipeline():
    """Recupera tutti i deal della pipeline"""
    if not supabase:
        return pd.DataFrame()
    try:
        response = supabase.table('pipeline').select('*').execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception as e:
        st.error(f"Errore caricamento pipeline: {e}")
        return pd.DataFrame()

def add_contatto(data):
    """Aggiunge un nuovo contatto"""
    if not supabase:
        return None
    try:
        response = supabase.table('contatti').insert(data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        st.error(f"Errore creazione contatto: {e}")
        return None

def update_contatto(id, data):
    """Aggiorna un contatto"""
    if not supabase:
        return None
    try:
        response = supabase.table('contatti').update(data).eq('id', id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        st.error(f"Errore aggiornamento contatto: {e}")
        return None

def delete_contatto(id):
    """Elimina un contatto"""
    if not supabase:
        return False
    try:
        supabase.table('contatti').delete().eq('id', id).execute()
        return True
    except Exception as e:
        st.error(f"Errore eliminazione contatto: {e}")
        return False

def add_deal(data):
    """Aggiunge un nuovo deal"""
    if not supabase:
        return None
    try:
        response = supabase.table('pipeline').insert(data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        st.error(f"Errore creazione deal: {e}")
        return None

def update_deal(id, data):
    """Aggiorna un deal"""
    if not supabase:
        return None
    try:
        response = supabase.table('pipeline').update(data).eq('id', id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        st.error(f"Errore aggiornamento deal: {e}")
        return None

def delete_deal(id):
    """Elimina un deal"""
    if not supabase:
        return False
    try:
        supabase.table('pipeline').delete().eq('id', id).execute()
        return True
    except Exception as e:
        st.error(f"Errore eliminazione deal: {e}")
        return False

# ========== PAGINE ==========

def page_dashboard():
    """Dashboard principale"""
    st.markdown('<h1 class="main-header">Dashboard CRM</h1>', unsafe_allow_html=True)

    contatti = get_contatti()
    pipeline = get_pipeline()

    # Metriche principali
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Contatti Totali", len(contatti))

    with col2:
        clienti = len(contatti[contatti.get('is_cliente', False) == True]) if len(contatti) > 0 and 'is_cliente' in contatti.columns else 0
        st.metric("Clienti Attivi", clienti)

    with col3:
        aum_totale = pipeline['aum_previsto'].sum() if len(pipeline) > 0 and 'aum_previsto' in pipeline.columns else 0
        st.metric("AUM Pipeline", f"€{aum_totale:,.0f}")

    with col4:
        deal_attivi = len(pipeline[pipeline['stage'] != 'Chiuso Perso']) if len(pipeline) > 0 and 'stage' in pipeline.columns else 0
        st.metric("Deal Attivi", deal_attivi)

    st.divider()

    # Grafici
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pipeline per Stage")
        if len(pipeline) > 0 and 'stage' in pipeline.columns:
            stage_counts = pipeline['stage'].value_counts().reindex(STAGES, fill_value=0)
            fig = px.bar(x=stage_counts.index, y=stage_counts.values,
                        color=stage_counts.values,
                        color_continuous_scale='Blues')
            fig.update_layout(xaxis_title="Stage", yaxis_title="Numero Deal", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nessun deal nella pipeline")

    with col2:
        st.subheader("AUM per Stage")
        if len(pipeline) > 0 and 'stage' in pipeline.columns and 'aum_previsto' in pipeline.columns:
            aum_by_stage = pipeline.groupby('stage')['aum_previsto'].sum().reindex(STAGES, fill_value=0)
            fig = px.pie(values=aum_by_stage.values, names=aum_by_stage.index, hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nessun dato AUM")

    # Ultimi deal
    st.subheader("Ultimi Deal")
    if len(pipeline) > 0:
        cols_to_show = ['nome_deal', 'stage', 'aum_previsto', 'probabilita']
        cols_available = [c for c in cols_to_show if c in pipeline.columns]
        if cols_available:
            st.dataframe(pipeline[cols_available].head(10), use_container_width=True)
    else:
        st.info("Nessun deal presente")


def page_contatti():
    """Gestione contatti"""
    st.markdown('<h1 class="main-header">Gestione Contatti</h1>', unsafe_allow_html=True)

    # Bottone nuovo contatto
    if st.button("➕ Nuovo Contatto", type="primary"):
        st.session_state.show_new_contact = True

    # Form nuovo contatto
    if st.session_state.get('show_new_contact', False):
        with st.expander("Nuovo Contatto", expanded=True):
            with st.form("new_contact_form"):
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

                aum_potenziale = st.number_input("AUM Potenziale", min_value=0, value=0)
                note = st.text_area("Note")

                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Salva", type="primary"):
                        if nome:
                            data = {
                                'nome': nome,
                                'cognome': cognome,
                                'email': email,
                                'telefono': telefono,
                                'azienda': azienda,
                                'ruolo': ruolo,
                                'tier': tier,
                                'fonte': fonte,
                                'aum_potenziale': aum_potenziale,
                                'note': note,
                                'is_cliente': False,
                                'created_at': datetime.now().isoformat()
                            }
                            if add_contatto(data):
                                st.success("Contatto creato!")
                                st.session_state.show_new_contact = False
                                st.rerun()
                        else:
                            st.error("Nome obbligatorio")
                with col2:
                    if st.form_submit_button("Annulla"):
                        st.session_state.show_new_contact = False
                        st.rerun()

    # Filtri
    st.subheader("Filtri")
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_tier = st.selectbox("Tier", ['Tutti', 'A', 'B', 'C'])
    with col2:
        filtro_cliente = st.selectbox("Tipo", ['Tutti', 'Clienti', 'Prospect'])
    with col3:
        filtro_search = st.text_input("Cerca")

    # Tabella contatti
    contatti = get_contatti()

    if len(contatti) > 0:
        # Applica filtri
        if filtro_tier != 'Tutti' and 'tier' in contatti.columns:
            contatti = contatti[contatti['tier'] == filtro_tier]
        if filtro_cliente == 'Clienti' and 'is_cliente' in contatti.columns:
            contatti = contatti[contatti['is_cliente'] == True]
        elif filtro_cliente == 'Prospect' and 'is_cliente' in contatti.columns:
            contatti = contatti[contatti['is_cliente'] == False]
        if filtro_search and 'nome' in contatti.columns:
            contatti = contatti[contatti['nome'].str.contains(filtro_search, case=False, na=False) |
                               contatti.get('cognome', pd.Series()).str.contains(filtro_search, case=False, na=False) |
                               contatti.get('azienda', pd.Series()).str.contains(filtro_search, case=False, na=False)]

        # Mostra tabella
        st.dataframe(contatti, use_container_width=True, hide_index=True)

        # Selezione per modifica/elimina
        st.subheader("Azioni")
        if 'id' in contatti.columns:
            contatto_id = st.selectbox("Seleziona contatto", contatti['id'].tolist(),
                                       format_func=lambda x: contatti[contatti['id']==x]['nome'].values[0] if len(contatti[contatti['id']==x]) > 0 else str(x))

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Elimina", type="secondary"):
                    if delete_contatto(contatto_id):
                        st.success("Contatto eliminato")
                        st.rerun()
    else:
        st.info("Nessun contatto presente. Clicca 'Nuovo Contatto' per iniziare.")


def page_pipeline():
    """Gestione pipeline (Kanban)"""
    st.markdown('<h1 class="main-header">Sales Pipeline</h1>', unsafe_allow_html=True)

    # Bottone nuovo deal
    if st.button("➕ Nuovo Deal", type="primary"):
        st.session_state.show_new_deal = True

    # Form nuovo deal
    if st.session_state.get('show_new_deal', False):
        with st.expander("Nuovo Deal", expanded=True):
            with st.form("new_deal_form"):
                col1, col2 = st.columns(2)
                with col1:
                    nome_deal = st.text_input("Nome Deal *")
                    stage = st.selectbox("Stage", STAGES)
                    aum_previsto = st.number_input("AUM Previsto", min_value=0, value=0)
                with col2:
                    fonte = st.text_input("Fonte")
                    responsabile = st.text_input("Responsabile", value="Antonio Tritto")
                    fee_percentuale = st.number_input("Fee %", min_value=0.0, max_value=5.0, value=0.5, step=0.1)

                note = st.text_area("Note")

                if st.form_submit_button("Salva", type="primary"):
                    if nome_deal:
                        data = {
                            'nome_deal': nome_deal,
                            'stage': stage,
                            'aum_previsto': aum_previsto,
                            'probabilita': STAGE_PROB.get(stage, 10),
                            'fee_percentuale': fee_percentuale,
                            'fee_stimata': aum_previsto * fee_percentuale / 100,
                            'fonte': fonte,
                            'responsabile': responsabile,
                            'note': note,
                            'created_at': datetime.now().isoformat()
                        }
                        if add_deal(data):
                            st.success("Deal creato!")
                            st.session_state.show_new_deal = False
                            st.rerun()
                    else:
                        st.error("Nome deal obbligatorio")

    # Pipeline Kanban
    pipeline = get_pipeline()

    if len(pipeline) > 0 and 'stage' in pipeline.columns:
        # Crea colonne per ogni stage
        cols = st.columns(len(STAGES))

        for i, stage in enumerate(STAGES):
            with cols[i]:
                st.markdown(f"**{stage}**")
                stage_deals = pipeline[pipeline['stage'] == stage]

                # Conta e AUM
                count = len(stage_deals)
                aum = stage_deals['aum_previsto'].sum() if 'aum_previsto' in stage_deals.columns else 0
                st.caption(f"{count} deal | €{aum:,.0f}")

                # Card per ogni deal
                for _, deal in stage_deals.iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div style="background: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #667eea;">
                            <strong>{deal.get('nome_deal', 'N/A')}</strong><br>
                            <small>€{deal.get('aum_previsto', 0):,.0f} | {deal.get('probabilita', 0)}%</small>
                        </div>
                        """, unsafe_allow_html=True)

        st.divider()

        # Gestione deal
        st.subheader("Sposta Deal")
        col1, col2, col3 = st.columns(3)

        with col1:
            deal_id = st.selectbox("Seleziona Deal", pipeline['id'].tolist(),
                                  format_func=lambda x: pipeline[pipeline['id']==x]['nome_deal'].values[0] if len(pipeline[pipeline['id']==x]) > 0 else str(x))

        with col2:
            nuovo_stage = st.selectbox("Nuovo Stage", STAGES)

        with col3:
            if st.button("Sposta"):
                if update_deal(deal_id, {'stage': nuovo_stage, 'probabilita': STAGE_PROB.get(nuovo_stage, 10)}):
                    st.success(f"Deal spostato a {nuovo_stage}")
                    st.rerun()

        # Elimina deal
        if st.button("Elimina Deal Selezionato", type="secondary"):
            if delete_deal(deal_id):
                st.success("Deal eliminato")
                st.rerun()
    else:
        st.info("Nessun deal nella pipeline. Clicca 'Nuovo Deal' per iniziare.")


def page_report():
    """Report e Analytics"""
    st.markdown('<h1 class="main-header">Report & Analytics</h1>', unsafe_allow_html=True)

    pipeline = get_pipeline()
    contatti = get_contatti()

    if len(pipeline) == 0:
        st.info("Nessun dato disponibile per i report")
        return

    # Funnel di conversione
    st.subheader("Funnel di Conversione")
    if 'stage' in pipeline.columns:
        funnel_data = []
        for stage in STAGES:
            count = len(pipeline[pipeline['stage'] == stage])
            aum = pipeline[pipeline['stage'] == stage]['aum_previsto'].sum() if 'aum_previsto' in pipeline.columns else 0
            funnel_data.append({'Stage': stage, 'Deal': count, 'AUM': aum})

        funnel_df = pd.DataFrame(funnel_data)

        fig = go.Figure(go.Funnel(
            y=funnel_df['Stage'],
            x=funnel_df['Deal'],
            textinfo="value+percent initial"
        ))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Revenue prevista
    st.subheader("Revenue Prevista")
    if 'aum_previsto' in pipeline.columns and 'probabilita' in pipeline.columns and 'fee_percentuale' in pipeline.columns:
        pipeline['revenue_pesata'] = pipeline['aum_previsto'] * pipeline['probabilita'] / 100 * pipeline['fee_percentuale'] / 100

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Revenue Totale Potenziale", f"€{pipeline['fee_stimata'].sum():,.0f}" if 'fee_stimata' in pipeline.columns else "N/A")
        with col2:
            st.metric("Revenue Pesata", f"€{pipeline['revenue_pesata'].sum():,.0f}")
        with col3:
            st.metric("Deal Medi", f"€{pipeline['aum_previsto'].mean():,.0f}")


def page_settings():
    """Impostazioni"""
    st.markdown('<h1 class="main-header">Impostazioni</h1>', unsafe_allow_html=True)

    st.subheader("Configurazione Supabase")

    if supabase:
        st.success("✅ Connesso a Supabase")
    else:
        st.warning("⚠️ Supabase non configurato")
        st.markdown("""
        Per configurare Supabase:
        1. Crea un account su [supabase.com](https://supabase.com)
        2. Crea un nuovo progetto
        3. Vai su Settings > API
        4. Copia URL e anon key
        5. Aggiungi i secrets in Streamlit Cloud o nel file `.streamlit/secrets.toml`:

        ```toml
        SUPABASE_URL = "https://xxx.supabase.co"
        SUPABASE_KEY = "eyJhbG..."
        ```
        """)

    st.divider()

    st.subheader("Schema Database")
    st.markdown("""
    Crea queste tabelle in Supabase (SQL Editor):

    ```sql
    -- Tabella Contatti
    CREATE TABLE contatti (
        id SERIAL PRIMARY KEY,
        nome TEXT NOT NULL,
        cognome TEXT,
        azienda TEXT,
        ruolo TEXT,
        email TEXT,
        telefono TEXT,
        tier TEXT DEFAULT 'C',
        fonte TEXT,
        aum_potenziale DECIMAL DEFAULT 0,
        is_cliente BOOLEAN DEFAULT FALSE,
        note TEXT,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );

    -- Tabella Pipeline
    CREATE TABLE pipeline (
        id SERIAL PRIMARY KEY,
        nome_deal TEXT NOT NULL,
        contatto_id INTEGER REFERENCES contatti(id),
        stage TEXT DEFAULT 'Lead',
        aum_previsto DECIMAL DEFAULT 0,
        probabilita INTEGER DEFAULT 10,
        fee_percentuale DECIMAL DEFAULT 0.5,
        fee_stimata DECIMAL DEFAULT 0,
        fonte TEXT,
        responsabile TEXT DEFAULT 'Antonio Tritto',
        note TEXT,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );

    -- Abilita RLS
    ALTER TABLE contatti ENABLE ROW LEVEL SECURITY;
    ALTER TABLE pipeline ENABLE ROW LEVEL SECURITY;

    -- Policy per accesso pubblico (per test)
    CREATE POLICY "Allow all" ON contatti FOR ALL USING (true);
    CREATE POLICY "Allow all" ON pipeline FOR ALL USING (true);
    ```
    """)


# ========== MAIN ==========

def main():
    # Sidebar navigazione
    st.sidebar.title("🏦 CRM Private Banking")
    st.sidebar.markdown("---")

    pagina = st.sidebar.radio(
        "Navigazione",
        ["Dashboard", "Contatti", "Pipeline", "Report", "Impostazioni"],
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Antonio Tritto - Private Banking")

    # Routing pagine
    if pagina == "Dashboard":
        page_dashboard()
    elif pagina == "Contatti":
        page_contatti()
    elif pagina == "Pipeline":
        page_pipeline()
    elif pagina == "Report":
        page_report()
    elif pagina == "Impostazioni":
        page_settings()


if __name__ == "__main__":
    main()
