import streamlit as st
import pandas as pd
import os
import altair as alt
import json

# 1. IMPOSTAZIONI PAGINA E DESIGN
st.set_page_config(page_title="Hub Carriera Universitaria", page_icon="🎓", layout="wide")

# Gestione Notifiche Sopravvissute al Rerun
if 'toast_msg' in st.session_state and st.session_state.toast_msg:
    st.toast(st.session_state.toast_msg, icon=st.session_state.toast_icon)
    st.session_state.toast_msg = ""
    st.session_state.toast_icon = ""

# CSS Personalizzato — design raffinato con palette teal/verde smeraldo su nero profondo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

    /* ── Reset e Base ── */
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }
    .stApp {
        background-color: #050a0a;
        background-image:
            radial-gradient(ellipse 80% 50% at 20% -10%, rgba(0,190,150,0.08) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 110%, rgba(0,250,154,0.05) 0%, transparent 55%);
        color: #a8d8d0;
    }

    /* ── Tipografia Globale ── */
    h1, h2, h3, h4, h5, h6, p, span, div, label, li, .stMarkdown {
        color: #c8eae4 !important;
    }

    /* ── Titolo principale ── */
    h1 {
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
        background: linear-gradient(135deg, #00fa9a 0%, #20b2aa 60%, #008b7d 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        padding-bottom: 0.2rem;
    }

    /* ── Sottotitoli tab ── */
    h2, h3 {
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
        color: #7ecdc6 !important;
        -webkit-text-fill-color: #7ecdc6 !important;
    }

    /* ── Metriche ── */
    [data-testid="stMetricValue"] {
        font-family: 'Space Mono', monospace !important;
        font-size: 1.7rem !important;
        font-weight: 700 !important;
        color: #00fa9a !important;
        -webkit-text-fill-color: #00fa9a !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: #4a9990 !important;
        -webkit-text-fill-color: #4a9990 !important;
    }
    [data-testid="stMetricDelta"] svg { display: none; }
    [data-testid="stMetricDelta"] > div {
        font-family: 'Space Mono', monospace !important;
        font-size: 0.8rem !important;
    }
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #0a1f1d 0%, #081a18 100%);
        border: 1px solid #1a4a44;
        border-radius: 12px;
        padding: 1.2rem 1.4rem !important;
        box-shadow: 0 4px 24px rgba(0,250,154,0.05);
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }
    [data-testid="metric-container"]:hover {
        border-color: #20b2aa;
        box-shadow: 0 4px 32px rgba(0,250,154,0.12);
    }

    /* ── Bottoni ── */
    .stButton > button {
        background: linear-gradient(135deg, #0d3d38 0%, #0a2e2a 100%) !important;
        color: #00fa9a !important;
        border: 1px solid #1e6b62 !important;
        border-radius: 8px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.02em !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.18s ease !important;
        box-shadow: 0 2px 12px rgba(0,250,154,0.08) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #00fa9a 0%, #00c87a 100%) !important;
        color: #000e0c !important;
        border-color: #00fa9a !important;
        box-shadow: 0 4px 20px rgba(0,250,154,0.3) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00fa9a 0%, #00c87a 100%) !important;
        color: #000e0c !important;
        border-color: #00fa9a !important;
        font-weight: 700 !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #00ffaa 0%, #00e088 100%) !important;
        box-shadow: 0 6px 28px rgba(0,250,154,0.45) !important;
    }

    /* ── Input ── */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #0a1f1d !important;
        color: #c8eae4 !important;
        border: 1px solid #1a4a44 !important;
        border-radius: 8px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #20b2aa !important;
        box-shadow: 0 0 0 3px rgba(32,178,170,0.15) !important;
    }
    .stTextInput > label, .stNumberInput > label {
        font-size: 0.78rem !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        color: #4a9990 !important;
        -webkit-text-fill-color: #4a9990 !important;
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        background-color: #0a1f1d !important;
        border: 1px solid #1a4a44 !important;
        border-radius: 8px !important;
        color: #c8eae4 !important;
    }

    /* ── Tab ── */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid #1a4a44 !important;
        gap: 0.2rem;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #4a9990 !important;
        border-radius: 8px 8px 0 0 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.01em !important;
        padding: 0.6rem 1.4rem !important;
        border-bottom: 2px solid transparent !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #20b2aa !important;
        background-color: rgba(32,178,170,0.07) !important;
    }
    .stTabs [aria-selected="true"] {
        color: #00fa9a !important;
        border-bottom: 2px solid #00fa9a !important;
        background-color: rgba(0,250,154,0.05) !important;
    }

    /* ── Data Editor / Tabelle ── */
    [data-testid="stDataFrame"],
    .stDataEditor {
        background-color: #081816 !important;
        border: 1px solid #1a4a44 !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    [data-testid="stDataFrameResizable"] { border-radius: 10px !important; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #040d0c 0%, #060f0e 100%) !important;
        border-right: 1px solid #0f2e2a !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background-color: #0a1f1d !important;
        border: 1px solid #1a4a44 !important;
        border-radius: 8px !important;
        color: #7ecdc6 !important;
        font-weight: 600 !important;
    }
    .streamlit-expanderContent {
        background-color: #081816 !important;
        border: 1px solid #1a4a44 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }

    /* ── Radio ── */
    .stRadio > div { gap: 0.8rem !important; }
    .stRadio label {
        background-color: #0a1f1d !important;
        border: 1px solid #1a4a44 !important;
        border-radius: 8px !important;
        padding: 0.4rem 1rem !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    .stRadio label:hover { border-color: #20b2aa !important; }

    /* ── Info / Warning / Error box ── */
    .stInfo, [data-testid="stInfo"] {
        background-color: rgba(32,178,170,0.08) !important;
        border: 1px solid #1a4a44 !important;
        border-left: 3px solid #20b2aa !important;
        border-radius: 8px !important;
        color: #7ecdc6 !important;
    }
    .stWarning, [data-testid="stWarning"] {
        background-color: rgba(255,180,50,0.07) !important;
        border-left: 3px solid #f0a830 !important;
        border-radius: 8px !important;
    }

    /* ── Divider ── */
    hr {
        border: none !important;
        border-top: 1px solid #0f2e2a !important;
        margin: 1.5rem 0 !important;
    }

    /* ── Checkbox ── */
    .stCheckbox label { color: #7ecdc6 !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #050a0a; }
    ::-webkit-scrollbar-thumb { background: #1a4a44; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #20b2aa; }

    /* ── Badge "Stai visualizzando" ── */
    .percorso-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, #0a1f1d 0%, #081a18 100%);
        border: 1px solid #1a4a44;
        border-radius: 10px;
        padding: 0.5rem 1.2rem;
        font-size: 0.95rem;
        color: #7ecdc6;
        margin-bottom: 1.2rem;
    }
    .percorso-badge strong { color: #00fa9a; }
    .percorso-badge .cfu-tag {
        background-color: rgba(0,250,154,0.1);
        border: 1px solid rgba(0,250,154,0.25);
        border-radius: 6px;
        padding: 0.1rem 0.5rem;
        font-family: 'Space Mono', monospace;
        font-size: 0.78rem;
        color: #00fa9a;
    }
    </style>
""", unsafe_allow_html=True)

CSV_FILE = "libretto_universitario.csv"
PERCORSI_FILE = "percorsi.json"

# 2. FUNZIONI DI BACKEND
def carica_percorsi():
    if os.path.exists(PERCORSI_FILE):
        try:
            with open(PERCORSI_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def salva_percorsi(percorsi):
    with open(PERCORSI_FILE, "w") as f:
        json.dump(percorsi, f)

def carica_dati():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=['Percorso', 'Esame', 'Tipo', 'Voto', 'Lode', 'CFU'])

def salva_dati(df):
    df.to_csv(CSV_FILE, index=False)

def imposta_notifica(messaggio, icona):
    st.session_state.toast_msg = messaggio
    st.session_state.toast_icon = icona

# Inizializzazione dati
if 'df_esami' not in st.session_state:
    st.session_state.df_esami = carica_dati()

if 'percorsi_salvati' not in st.session_state:
    st.session_state.percorsi_salvati = carica_percorsi()

# ── Header con tagline ──
st.title("🎓 Hub Carriera Universitaria")
st.markdown(
    "<p style='color:#4a9990 !important; font-size:0.95rem; margin-top:-0.8rem; margin-bottom:1.5rem; letter-spacing:0.02em;'>"
    "Tieni traccia dei tuoi esami, monitora la media e simula il tuo futuro accademico."
    "</p>",
    unsafe_allow_html=True
)

# Blocco iniziale se non ci sono percorsi
if not st.session_state.percorsi_salvati:
    st.warning("⚠️ Non hai ancora registrato nessun corso di laurea. Creane uno per iniziare!")
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        n_perc = st.text_input("Nome del corso di laurea (es. Ingegneria Meccanica):")
    with col_i2:
        c_perc = st.number_input("CFU totali necessari per la laurea:", min_value=1, value=180)
    if st.button("🚀 Crea il tuo primo Percorso", type="primary"):
        if n_perc.strip():
            st.session_state.percorsi_salvati[n_perc] = c_perc
            salva_percorsi(st.session_state.percorsi_salvati)
            st.session_state.percorso_attivo = n_perc
            imposta_notifica(f"Benvenuto! Percorso '{n_perc}' creato.", "🎉")
            st.rerun()
        else:
            st.error("Inserisci un nome valido per il percorso.")
    st.stop()

# 3. BARRA LATERALE
st.sidebar.markdown(
    "<div style='font-size:1.1rem; font-weight:700; color:#00fa9a !important; "
    "-webkit-text-fill-color:#00fa9a !important; letter-spacing:-0.02em; margin-bottom:0.8rem;'>"
    "⚙️ Gestione Percorsi</div>",
    unsafe_allow_html=True
)

lista_percorsi = list(st.session_state.percorsi_salvati.keys())
if 'percorso_attivo' not in st.session_state or st.session_state.percorso_attivo not in lista_percorsi:
    st.session_state.percorso_attivo = lista_percorsi[0]

scelta = st.sidebar.selectbox(
    "Percorso attivo:",
    lista_percorsi,
    index=lista_percorsi.index(st.session_state.percorso_attivo)
)
st.session_state.percorso_attivo = scelta
cfu_totali_corso = st.session_state.percorsi_salvati[st.session_state.percorso_attivo]

with st.sidebar.expander("✏️ Modifica / Elimina Percorso"):
    nuovo_nome_perc = st.text_input("Rinomina percorso:", value=st.session_state.percorso_attivo)
    nuovi_cfu_perc = st.number_input("CFU Totali:", min_value=1, value=cfu_totali_corso)
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 Salva"):
            if nuovo_nome_perc != st.session_state.percorso_attivo or nuovi_cfu_perc != cfu_totali_corso:
                if nuovo_nome_perc != st.session_state.percorso_attivo:
                    st.session_state.df_esami.loc[
                        st.session_state.df_esami['Percorso'] == st.session_state.percorso_attivo, 'Percorso'
                    ] = nuovo_nome_perc
                    salva_dati(st.session_state.df_esami)
                    del st.session_state.percorsi_salvati[st.session_state.percorso_attivo]
                st.session_state.percorsi_salvati[nuovo_nome_perc] = nuovi_cfu_perc
                salva_percorsi(st.session_state.percorsi_salvati)
                st.session_state.percorso_attivo = nuovo_nome_perc
                imposta_notifica("Percorso aggiornato!", "🔄")
                st.rerun()
    with col_btn2:
        if st.button("🗑️ Elimina"):
            del st.session_state.percorsi_salvati[st.session_state.percorso_attivo]
            salva_percorsi(st.session_state.percorsi_salvati)
            st.session_state.df_esami = st.session_state.df_esami[
                st.session_state.df_esami['Percorso'] != st.session_state.percorso_attivo
            ]
            salva_dati(st.session_state.df_esami)
            imposta_notifica("Percorso eliminato definitivamente.", "🗑️")
            st.rerun()

with st.sidebar.expander("➕ Aggiungi nuovo percorso"):
    nuovo_p = st.text_input("Nome corso (es. Magistrale):", key="np")
    nuovo_c = st.number_input("CFU totali:", min_value=1, value=120, key="nc")
    if st.button("Crea Percorso"):
        if nuovo_p and nuovo_p not in st.session_state.percorsi_salvati:
            st.session_state.percorsi_salvati[nuovo_p] = nuovo_c
            salva_percorsi(st.session_state.percorsi_salvati)
            st.session_state.percorso_attivo = nuovo_p
            imposta_notifica(f"Percorso '{nuovo_p}' creato!", "🎉")
            st.rerun()

# Badge percorso attivo
st.markdown(
    f"<div class='percorso-badge'>"
    f"Percorso attivo: <strong>{st.session_state.percorso_attivo}</strong>"
    f"<span class='cfu-tag'>{cfu_totali_corso} CFU</span>"
    f"</div>",
    unsafe_allow_html=True
)

df_totale = st.session_state.df_esami
df_corso = df_totale[df_totale['Percorso'] == st.session_state.percorso_attivo].copy()

if 'percorso_simulato_attuale' not in st.session_state or st.session_state.percorso_simulato_attuale != st.session_state.percorso_attivo:
    st.session_state.df_simulato = df_corso.copy()
    st.session_state.percorso_simulato_attuale = st.session_state.percorso_attivo

# 4. TAB
tab_libretto, tab_statistiche, tab_simulatore = st.tabs([
    "📝 Libretto Ufficiale",
    "📊 Statistiche & Andamento",
    "🔮 Simulatore Voti"
])

# ── TAB 1: LIBRETTO ──
with tab_libretto:
    st.subheader("Registra nuovo esame")

    tipo_esame = st.radio("Tipo di valutazione:", ["Esame con voto", "Idoneità (Pass/Fail)"], horizontal=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        nome_esame = st.text_input("Nome dell'insegnamento", placeholder="Es. Analisi Matematica I")
    with col2:
        if tipo_esame == "Esame con voto":
            voto = st.number_input("Voto", min_value=18, max_value=30, value=25, step=1)
            lode = st.checkbox("Lode ✨", disabled=(voto < 30))
            if voto < 30:
                lode = False
        else:
            voto = 0
            lode = False
            st.write("Solo CFU")
    with col3:
        cfu = st.number_input("CFU", min_value=1, max_value=30, value=6, step=1)

    if st.button("💾 Registra nel Libretto", type="primary"):
        if nome_esame.strip() == "":
            st.error("Inserisci il nome dell'esame prima di salvare.")
        else:
            nuovo_record = pd.DataFrame([{
                'Percorso': st.session_state.percorso_attivo,
                'Esame': nome_esame,
                'Tipo': tipo_esame,
                'Voto': int(voto) if tipo_esame == "Esame con voto" else "-",
                'Lode': lode if tipo_esame == "Esame con voto" else False,
                'CFU': int(cfu)
            }])
            st.session_state.df_esami = pd.concat([st.session_state.df_esami, nuovo_record], ignore_index=True)
            salva_dati(st.session_state.df_esami)
            st.session_state.df_simulato = st.session_state.df_esami[
                st.session_state.df_esami['Percorso'] == st.session_state.percorso_attivo
            ].copy()
            imposta_notifica("Esame registrato nel libretto!", "💾")
            st.rerun()

    st.divider()
    st.subheader("Gestione esami registrati")

    if not df_corso.empty:
        n_esami_totali = len(df_corso)
        n_esami_con_voto = len(df_corso[df_corso['Tipo'] == "Esame con voto"])
        n_idoneita = n_esami_totali - n_esami_con_voto
        
        # Intestazione con conteggio esami
        col_hd1, col_hd2, col_hd3 = st.columns([2, 1, 1])
        with col_hd1:
            st.info("💡 **Modifica:** doppio clic sulla cella. **Elimina:** spunta la casella nell'ultima colonna, poi clicca Aggiorna.")
        with col_hd2:
            st.markdown(
                f"<div style='background:linear-gradient(135deg,#0a1f1d,#081a18); border:1px solid #1a4a44; "
                f"border-radius:10px; padding:0.7rem 1rem; text-align:center;'>"
                f"<div style='font-family:Space Mono,monospace; font-size:1.6rem; font-weight:700; "
                f"color:#00fa9a !important; -webkit-text-fill-color:#00fa9a !important; line-height:1;'>{n_esami_totali}</div>"
                f"<div style='font-size:0.7rem; text-transform:uppercase; letter-spacing:0.08em; "
                f"color:#4a9990 !important; -webkit-text-fill-color:#4a9990 !important; margin-top:0.2rem;'>Esami registrati</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with col_hd3:
            st.markdown(
                f"<div style='background:linear-gradient(135deg,#0a1f1d,#081a18); border:1px solid #1a4a44; "
                f"border-radius:10px; padding:0.7rem 1rem; text-align:center;'>"
                f"<div style='font-family:Space Mono,monospace; font-size:1.6rem; font-weight:700; "
                f"color:#20b2aa !important; -webkit-text-fill-color:#20b2aa !important; line-height:1;'>{n_esami_con_voto}</div>"
                f"<div style='font-size:0.7rem; text-transform:uppercase; letter-spacing:0.08em; "
                f"color:#4a9990 !important; -webkit-text-fill-color:#4a9990 !important; margin-top:0.2rem;'>Con voto</div>"
                f"</div>",
                unsafe_allow_html=True
            )

        # Numero progressivo — hide_index=True rimuove la colonna indice di default di Streamlit
        df_edit_view = df_corso[['Esame', 'Voto', 'CFU', 'Lode', 'Tipo']].copy().reset_index(drop=True)
        df_edit_view.insert(0, "#", range(1, len(df_edit_view) + 1))
        df_edit_view["🗑️"] = False   # ultima colonna

        df_editato = st.data_editor(
            df_edit_view,
            use_container_width=True,
            num_rows="fixed",
            hide_index=True,
            disabled=["Lode", "#"],
            column_config={
                "#": st.column_config.NumberColumn(
                    "#",
                    help="Numero progressivo esame",
                    width="small",
                    format="%d"
                ),
                "🗑️": st.column_config.CheckboxColumn(
                    "🗑️ Elimina",
                    help="Seleziona per eliminare questa riga",
                    default=False,
                    width="small"
                )
            },
            key="editor_reale"
        )

        if st.button("Aggiorna Libretto"):
            df_da_salvare = df_editato[df_editato["🗑️"] == False].drop(columns=["🗑️", "#"])
            df_restante = df_totale[df_totale['Percorso'] != st.session_state.percorso_attivo]
            df_da_salvare['Percorso'] = st.session_state.percorso_attivo
            st.session_state.df_esami = pd.concat([df_restante, df_da_salvare], ignore_index=True)
            salva_dati(st.session_state.df_esami)
            st.session_state.df_simulato = df_da_salvare.copy()
            imposta_notifica("Libretto aggiornato!", "📝")
            st.rerun()
    else:
        st.markdown(
            "<div style='text-align:center; padding:2.5rem; color:#2a6b64 !important; "
            "-webkit-text-fill-color:#2a6b64 !important; font-size:0.95rem;'>"
            "📭 Nessun esame registrato in questo percorso.<br>"
            "<span style='font-size:0.82rem;'>Usa il modulo qui sopra per aggiungere il tuo primo esame.</span>"
            "</div>",
            unsafe_allow_html=True
        )

# ── TAB 2: STATISTICHE ──
with tab_statistiche:
    df_voti_validi = df_corso[df_corso['Tipo'] == "Esame con voto"].copy()
    cfu_acquisiti_totali = int(df_corso['CFU'].sum()) if not df_corso.empty else 0
    cfu_mancanti = max(0, cfu_totali_corso - cfu_acquisiti_totali)

    if not df_voti_validi.empty:
        df_voti_validi['Voto'] = pd.to_numeric(df_voti_validi['Voto'])
        somma_ponderata = (df_voti_validi['Voto'] * df_voti_validi['CFU']).sum()
        cfu_per_media = df_voti_validi['CFU'].sum()
        media_ponderata_attuale = somma_ponderata / cfu_per_media if cfu_per_media > 0 else 0
        voto_partenza_laurea = (media_ponderata_attuale * 11) / 3
    else:
        media_ponderata_attuale = 0.0
        voto_partenza_laurea = 0.0

    if not df_corso.empty:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("CFU Conseguiti", f"{cfu_acquisiti_totali} / {cfu_totali_corso}")
        col_m2.metric("CFU Mancanti", cfu_mancanti)
        col_m3.metric("Media Ponderata", f"{media_ponderata_attuale:.2f}")
        col_m4.metric("Voto d'Entrata", f"{voto_partenza_laurea:.2f} / 110")

        st.divider()

        col_pie, col_line = st.columns([1, 2])

        with col_pie:
            st.subheader("Progresso CFU")
            percentuale = (cfu_acquisiti_totali / cfu_totali_corso) * 100 if cfu_totali_corso > 0 else 0
            st.markdown(
                f"<p style='font-family:Space Mono,monospace; font-size:2rem; font-weight:700; "
                f"color:#00fa9a !important; -webkit-text-fill-color:#00fa9a !important; margin:0;'>"
                f"{percentuale:.1f}%</p>"
                f"<p style='font-size:0.78rem; color:#4a9990 !important; -webkit-text-fill-color:#4a9990 !important; "
                f"text-transform:uppercase; letter-spacing:0.08em; margin-top:0;'>completato</p>",
                unsafe_allow_html=True
            )

            df_pie = pd.DataFrame({
                "Stato": ["Conseguiti", "Da Conseguire"],
                "CFU": [cfu_acquisiti_totali, cfu_mancanti]
            })

            pie_chart = alt.Chart(df_pie).mark_arc(innerRadius=55, outerRadius=100).encode(
                theta=alt.Theta(field="CFU", type="quantitative"),
                color=alt.Color(
                    field="Stato",
                    type="nominal",
                    scale=alt.Scale(
                        domain=["Conseguiti", "Da Conseguire"],
                        range=["#00fa9a", "#0f3530"]
                    ),
                    legend=alt.Legend(
                        labelColor="#7ecdc6",
                        titleColor="#4a9990",
                        orient="bottom"
                    )
                ),
                tooltip=["Stato", "CFU"]
            ).properties(height=280, background='transparent')

            st.altair_chart(pie_chart, use_container_width=True)

        with col_line:
            if not df_voti_validi.empty:
                st.subheader("Andamento media nel tempo")
                df_voti_validi = df_voti_validi.reset_index(drop=True)
                df_voti_validi['CFU_Cumulati'] = df_voti_validi['CFU'].cumsum()
                df_voti_validi['Punti_Cumulati'] = (df_voti_validi['Voto'] * df_voti_validi['CFU']).cumsum()
                df_voti_validi['Media Evolutiva'] = df_voti_validi['Punti_Cumulati'] / df_voti_validi['CFU_Cumulati']
                df_voti_validi['Ordine'] = df_voti_validi.index + 1
                # Etichetta corta per tooltip (max 22 char)
                df_voti_validi['Label'] = df_voti_validi['Esame'].str[:22]

                # Banda di riferimento: media finale come regola orizzontale
                media_finale = float(media_ponderata_attuale)
                df_rule = pd.DataFrame({'media': [media_finale]})

                base = alt.Chart(df_voti_validi).encode(
                    x=alt.X(
                        'Ordine:Q',
                        title='Esame n°',
                        scale=alt.Scale(
                            domain=[0.5, len(df_voti_validi) + 0.5],
                            nice=False
                        ),
                        axis=alt.Axis(
                            labelColor='#4a9990',
                            titleColor='#4a9990',
                            gridColor='#0e2825',
                            domainColor='#1a4a44',
                            tickColor='#1a4a44',
                            tickCount=len(df_voti_validi),
                            format='d',
                            labelFontSize=11,
                            titleFontSize=11,
                            titlePadding=10
                        )
                    )
                )

                # Area sfumata sotto la curva voti
                area = base.mark_area(
                    line={'color': '#20b2aa', 'strokeWidth': 2.5},
                    color=alt.Gradient(
                        gradient='linear',
                        stops=[
                            alt.GradientStop(color='rgba(32,178,170,0.25)', offset=0),
                            alt.GradientStop(color='rgba(32,178,170,0.0)', offset=1)
                        ],
                        x1=1, x2=1, y1=1, y2=0
                    ),
                    interpolate='monotone'
                ).encode(
                    y=alt.Y(
                        'Voto:Q',
                        scale=alt.Scale(domain=[18, 30], clamp=True),
                        title='Voto',
                        axis=alt.Axis(
                            labelColor='#4a9990',
                            titleColor='#4a9990',
                            gridColor='#0e2825',
                            domainColor='#1a4a44',
                            tickColor='#1a4a44',
                            tickCount=13,
                            values=list(range(18, 31)),
                            labelFontSize=11,
                            titleFontSize=11,
                            titlePadding=10
                        )
                    )
                )

                # Punti sui voti con tooltip
                punti = base.mark_circle(
                    size=80,
                    color='#20b2aa',
                    opacity=1
                ).encode(
                    y=alt.Y('Voto:Q', scale=alt.Scale(domain=[18, 30], clamp=True)),
                    tooltip=[
                        alt.Tooltip('Label:N', title='Esame'),
                        alt.Tooltip('Voto:Q', title='Voto'),
                        alt.Tooltip('CFU:Q', title='CFU'),
                        alt.Tooltip('Media Evolutiva:Q', title='Media prog.', format='.2f')
                    ]
                )

                # Linea media evolutiva
                linea_media = base.mark_line(
                    color='#00fa9a',
                    strokeDash=[5, 4],
                    strokeWidth=1.8,
                    interpolate='monotone'
                ).encode(
                    y=alt.Y('Media Evolutiva:Q', scale=alt.Scale(domain=[18, 30], clamp=True)),
                    tooltip=[
                        alt.Tooltip('Label:N', title='Esame'),
                        alt.Tooltip('Media Evolutiva:Q', title='Media progressiva', format='.2f')
                    ]
                )

                # Linea orizzontale media finale
                rule_media = alt.Chart(df_rule).mark_rule(
                    color='rgba(0,250,154,0.35)',
                    strokeDash=[2, 4],
                    strokeWidth=1.2
                ).encode(
                    y=alt.Y('media:Q', scale=alt.Scale(domain=[18, 30], clamp=True))
                )

                # Label media finale (a destra del grafico)
                testo_media = alt.Chart(df_rule).mark_text(
                    align='right',
                    baseline='bottom',
                    color='rgba(0,250,154,0.6)',
                    fontSize=10,
                    fontWeight=600,
                    dx=-4,
                    dy=-4
                ).encode(
                    y=alt.Y('media:Q'),
                    x=alt.value(0),
                    text=alt.value(f"media {media_finale:.2f}")
                )

                chart_final = (rule_media + area + linea_media + punti).properties(
                    height=300,
                    background='transparent'
                ).configure_axis(
                    gridColor='#0e2825',
                    domainColor='#1a4a44',
                    labelFont='Space Grotesk, sans-serif',
                    titleFont='Space Grotesk, sans-serif'
                ).configure_view(
                    strokeWidth=0
                ).configure_legend(
                    disable=True
                )

                st.altair_chart(chart_final, use_container_width=True)

                # Legenda manuale curata
                st.markdown(
                    "<div style='display:flex; gap:2rem; font-size:0.78rem; margin-top:-0.5rem; padding-left:0.2rem;'>"
                    "<span style='display:flex;align-items:center;gap:0.4rem;'>"
                    "<span style='display:inline-block;width:20px;height:3px;background:#20b2aa;border-radius:2px;'></span>"
                    "<span style='color:#7ecdc6 !important;-webkit-text-fill-color:#7ecdc6 !important;'>Voti</span></span>"
                    "<span style='display:flex;align-items:center;gap:0.4rem;'>"
                    "<span style='display:inline-block;width:20px;height:2px;background:#00fa9a;border-radius:2px;"
                    "background-image:repeating-linear-gradient(90deg,#00fa9a 0 5px,transparent 5px 9px);'></span>"
                    "<span style='color:#7ecdc6 !important;-webkit-text-fill-color:#7ecdc6 !important;'>Media progressiva</span></span>"
                    "<span style='display:flex;align-items:center;gap:0.4rem;'>"
                    "<span style='display:inline-block;width:20px;height:1px;background:rgba(0,250,154,0.4);'></span>"
                    "<span style='color:#7ecdc6 !important;-webkit-text-fill-color:#7ecdc6 !important;'>Media attuale</span></span>"
                    "</div>",
                    unsafe_allow_html=True
                )
    else:
        st.markdown(
            "<div style='text-align:center; padding:3rem; color:#2a6b64 !important; "
            "-webkit-text-fill-color:#2a6b64 !important;'>"
            "📊 Registra i tuoi esami per sbloccare le statistiche.</div>",
            unsafe_allow_html=True
        )

# ── TAB 3: SIMULATORE ──
with tab_simulatore:
    st.subheader("Aggiungi esame ipotetico")
    st.markdown(
        "<p style='color:#4a9990 !important; -webkit-text-fill-color:#4a9990 !important; "
        "font-size:0.88rem; margin-top:-0.5rem;'>"
        "Sperimenta scenari futuri. Le modifiche esistono solo qui, il libretto reale non viene toccato."
        "</p>",
        unsafe_allow_html=True
    )

    col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
    with col_s1:
        nome_sim = st.text_input("Nome esame ipotetico", key="nome_sim")
    with col_s2:
        voto_sim = st.number_input("Voto ipotetico", min_value=18, max_value=30, value=25, step=1, key="voto_sim")
    with col_s3:
        cfu_sim_input = st.number_input("CFU", min_value=1, max_value=30, value=6, step=1, key="cfu_sim_input")

    if st.button("✨ Aggiungi alla Simulazione", type="primary"):
        if nome_sim.strip() == "":
            st.error("Inserisci il nome dell'esame!")
        else:
            nuovo_record_sim = pd.DataFrame([{
                'Percorso': st.session_state.percorso_attivo,
                'Esame': f"✨ {nome_sim}",
                'Tipo': "Esame con voto",
                'Voto': int(voto_sim),
                'Lode': False,
                'CFU': int(cfu_sim_input)
            }])
            st.session_state.df_simulato = pd.concat(
                [st.session_state.df_simulato, nuovo_record_sim], ignore_index=True
            )
            imposta_notifica("Esame ipotetico aggiunto al simulatore!", "✨")
            st.rerun()

    st.divider()
    st.subheader("Gestione voti simulati")
    st.info("💡 Modifica i voti direttamente nella tabella. Usa l'ultima colonna per eliminare righe.")

    if not st.session_state.df_simulato.empty:
        # Numero progressivo — hide_index=True rimuove la colonna indice di default
        df_sim_view = st.session_state.df_simulato[['Esame', 'Voto', 'CFU', 'Lode', 'Tipo']].copy().reset_index(drop=True)
        df_sim_view.insert(0, "#", range(1, len(df_sim_view) + 1))
        df_sim_view["🗑️"] = False   # ultima colonna

        df_sim_editato = st.data_editor(
            df_sim_view,
            use_container_width=True,
            num_rows="fixed",
            hide_index=True,
            disabled=["Lode", "#"],
            column_config={
                "#": st.column_config.NumberColumn(
                    "#",
                    help="Numero progressivo esame simulato",
                    width="small",
                    format="%d"
                ),
                "🗑️": st.column_config.CheckboxColumn(
                    "🗑️ Elimina",
                    help="Seleziona per eliminare questa riga dalla simulazione",
                    default=False,
                    width="small"
                )
            },
            key="editor_simulato"
        )

        col_upd, col_rst = st.columns([1, 1])
        with col_upd:
            if st.button("Applica modifiche simulate"):
                df_sim_salvato = df_sim_editato[df_sim_editato["🗑️"] == False].drop(columns=["🗑️", "#"])
                st.session_state.df_simulato = df_sim_salvato.copy()
                imposta_notifica("Simulatore aggiornato!", "🔄")
                st.rerun()
        with col_rst:
            if st.button("🔄 Resetta simulazione"):
                st.session_state.df_simulato = df_corso.copy()
                imposta_notifica("Simulatore resettato ai dati reali.", "🧹")
                st.rerun()

    # Calcolo live
    df_sim_validi = st.session_state.df_simulato[
        st.session_state.df_simulato['Tipo'] == "Esame con voto"
    ].copy()

    if not df_sim_validi.empty:
        df_sim_validi['Voto'] = pd.to_numeric(df_sim_validi['Voto'], errors='coerce').fillna(0)
        df_sim_validi['CFU'] = pd.to_numeric(df_sim_validi['CFU'], errors='coerce').fillna(0)

        somma_pond_sim = (df_sim_validi['Voto'] * df_sim_validi['CFU']).sum()
        cfu_sim_tot = df_sim_validi['CFU'].sum()
        media_sim = somma_pond_sim / cfu_sim_tot if cfu_sim_tot > 0 else 0
        voto_laurea_sim = (media_sim * 11) / 3

        st.divider()
        st.subheader("Risultato simulazione")
        m1, m2, m3 = st.columns(3)
        m1.metric("CFU Simulati", int(cfu_sim_tot))

        if not df_voti_validi.empty and media_ponderata_attuale > 0:
            delta_media = media_sim - media_ponderata_attuale
            delta_laurea = voto_laurea_sim - voto_partenza_laurea
            m2.metric("Nuova Media", f"{media_sim:.2f}", f"{delta_media:+.2f}")
            m3.metric("Nuovo Voto d'Entrata", f"{voto_laurea_sim:.2f}", f"{delta_laurea:+.2f}")
        else:
            m2.metric("Nuova Media", f"{media_sim:.2f}")
            m3.metric("Nuovo Voto d'Entrata", f"{voto_laurea_sim:.2f}")
