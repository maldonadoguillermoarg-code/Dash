import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ==============================================================================
# 1. CONFIGURACIÓN ESTRATÉGICA Y ZOOM OPTIMIZATION
# ==============================================================================
st.set_page_config(
    page_title="GRIMOLDI CX | Intelligence System", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

CX_THEME = {
    "bg_card": "#E2EBEE",     # Gris azulado claro
    "primary": "#086890",     # Azul profundo
    "accent": "#CE516F",      # Rojo/Pink Alerta
    "neutral": "#8A8F90",     # Gris etiquetas
    "cyan": "#57C5E4",        # Cyan comparativo
    "white": "#FFFFFF",
    "text": "#1A1F2B",
    "success": "#2D8A4E",
    "warning": "#F39C12"
}

if 'view' not in st.session_state: st.session_state.view = 'Home'
if 'category' not in st.session_state: st.session_state.category = None

# ==============================================================================
# 2. MOTOR DE ESTILOS CX (CONSERVANDO LA VISUAL ORIGINAL)
# ==============================================================================
def inject_cx_industrial_design():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        
        * {{ font-family: 'Inter', sans-serif !important; }}
        .stApp {{ background-color: {CX_THEME["white"]}; }}
        
        #MainMenu, footer, header {{ visibility: hidden; }}

        /* CX Cards - Optimización Zoom 100% */
        .cx-card {{
            background-color: {CX_THEME["bg_card"]};
            padding: 25px;
            border-radius: 16px;
            border-left: 6px solid {CX_THEME["primary"]};
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }}
        .cx-card:hover {{ transform: translateY(-2px); }}

        /* Progress Bars */
        .pg-container {{ background: #D1D9DB; border-radius: 20px; height: 12px; margin: 10px 0; overflow: hidden; }}
        .pg-bar {{ background: {CX_THEME["primary"]}; height: 100%; border-radius: 20px; transition: width 0.8s ease-in-out; }}

        /* Tipografía */
        h1, h2, h3 {{ color: {CX_THEME["primary"]}; font-weight: 800 !important; }}
        .label-cx {{ color: {CX_THEME["neutral"]}; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }}
        
        /* Bloques de Información */
        .info-block {{
            background: #F8FAFB;
            border: 1px solid #D1D9DB;
            padding: 20px;
            border-radius: 10px;
            margin-top: 10px;
            font-size: 0.9rem;
            color: #4A5568;
            line-height: 1.6;
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
        .stTabs [data-baseweb="tab"] {{
            padding: 8px 16px; background-color: {CX_THEME["bg_card"]};
            border-radius: 5px; color: {CX_THEME["neutral"]};
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {CX_THEME["primary"]} !important; color: white !important;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GENERADOR DE DATOS MASIVOS (DATA ENGINE)
# ==============================================================================

@st.cache_data
def get_massive_data():
    data = []
    base_date = datetime(2026, 1, 1)
    for i in range(1000):
        data.append({
            "Timestamp": base_date + timedelta(hours=i),
            "SKU_ID": f"GR-{np.random.randint(1000, 9999)}",
            "Local": np.random.choice(["Florida 251", "Unicenter", "Alto Palermo", "E-Comm", "Córdoba Sh"]),
            "Venta_Neta": np.random.uniform(5000, 55000),
            "Costo_Directo": np.random.uniform(2000, 25000),
            "Feedback_Score": np.random.randint(1, 6),
            "Status": np.random.choice(["Validado", "Pendiente", "Error Conciliación"])
        })
    return pd.DataFrame(data)

# ==============================================================================
# 4. COMPONENTES GRÁFICOS (REQUISITOS CX)
# ==============================================================================

def get_cx_template():
    return go.layout.Template(
        layout=go.Layout(
            font=dict(family="Inter", color=CX_THEME["text"]),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, zeroline=False, color=CX_THEME["neutral"]),
            yaxis=dict(showgrid=True, gridcolor="#D1D9DB", zeroline=False, color=CX_THEME["neutral"]),
            margin=dict(l=10, r=10, t=30, b=10)
        )
    )

def chart_stepped(y):
    fig = go.Figure(go.Scatter(y=y, line_shape='hv', line=dict(color=CX_THEME["accent"], width=4)))
    fig.update_layout(template=get_cx_template(), height=300)
    return fig

def chart_multi_donut():
    fig = go.Figure()
    fig.add_trace(go.Pie(values=[65, 35], hole=0.8, marker=dict(colors=[CX_THEME["primary"], "#D1D9DB"]), domain={'x': [0, 1], 'y': [0, 1]}))
    fig.add_trace(go.Pie(values=[45, 55], hole=0.6, marker=dict(colors=[CX_THEME["accent"], "#E2EBEE"]), domain={'x': [0.15, 0.85], 'y': [0.15, 0.85]}))
    fig.update_layout(showlegend=False, height=300, template=get_cx_template())
    return fig

def chart_stacked_area(data_y):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=data_y, fill='tozeroy', fillcolor='rgba(87, 197, 228, 0.2)', 
                             line=dict(color=CX_THEME["cyan"], width=4), mode='lines'))
    fig.update_layout(template=get_cx_template(), height=350)
    return fig

def chart_dual_line():
    fig = go.Figure()
    x = ["S1", "S2", "S3", "S4", "S5", "S6"]
    fig.add_trace(go.Scatter(x=x, y=[40, 55, 42, 68, 70, 85], name="Real", line=dict(color=CX_THEME["primary"], width=4)))
    fig.add_trace(go.Scatter(x=x, y=[45, 50, 50, 60, 65, 75], name="Target", line=dict(color=CX_THEME["neutral"], dash='dot')))
    fig.update_layout(template=get_cx_template(), height=300, legend=dict(orientation="h", y=-0.2))
    return fig

# ==============================================================================
# 5. DICCIONARIO DE CONOCIMIENTO
# ==============================================================================

KPI_INTELLIGENCE = {
    "Ventas vs Costos": {
        "detalle": "Análisis de la eficiencia marginal por canal de venta. El canal E-Comm muestra una erosión del 12% por costos logísticos.",
        "tecnica": "Algoritmo de correlación Pearson entre volumen de carga y costo regional."
    },
    "Market Share": {
        "detalle": "Grimoldi mantiene un 22% del market share en el segmento confort. Riesgo detectado en segmento Youth.",
        "tecnica": "Modelado econométrico basado en tráfico en centros comerciales."
    }
}

# ==============================================================================
# 6. VISTA HOME
# ==============================================================================

def render_home():
    st.markdown("<h1>SISTEMA DE ANÁLISIS INTEGRAL (D.A.I.)</h1>", unsafe_allow_html=True)
    st.markdown("<p class='label-cx'>Consolidado Estratégico Grimoldi S.A. | Inteligencia de Negocio Q1 2026</p>", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="cx-card"><p class="label-cx">ROI OPERATIVO</p><h2>28.4%</h2>'
                    f'<div class="pg-container"><div class="pg-bar" style="width:75%"></div></div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="cx-card"><p class="label-cx">MARGEN NETO</p><h2>14.8%</h2>'
                    f'<div class="pg-container"><div class="pg-bar" style="width:45%"></div></div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="cx-card"><p class="label-cx">EBITDA M$</p><h2>18.2</h2>'
                    f'<div class="pg-container"><div class="pg-bar" style="width:90%"></div></div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="cx-card"><p class="label-cx">STOCK HEALTH</p><h2>82.0%</h2>'
                    f'<div class="pg-container"><div class="pg-bar" style="width:82%"></div></div></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.subheader("Navegación Estratégica")
        if st.button("🛒 ÁREA COMERCIAL", use_container_width=True):
            st.session_state.view = 'Category'; st.session_state.category = 'Comercial'; st.rerun()
        if st.button("👥 CAPITAL HUMANO", use_container_width=True):
            st.session_state.view = 'Category'; st.session_state.category = 'Capital Humano'; st.rerun()
        if st.button("📦 EFICIENCIA LOGÍSTICA", use_container_width=True):
            st.session_state.view = 'Category'; st.session_state.category = 'Logística'; st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("**Monitor de Estado Crítico (Stepped Chart)**")
        st.plotly_chart(chart_stepped([10, 10, 25, 25, 40, 35]), use_container_width=True)

    with col_r:
        st.write("**Performance Histórica Consolidada (Stacked Area)**")
        st.plotly_chart(chart_stacked_area([12, 45, 30, 78, 60, 95, 110]), use_container_width=True)

# ==============================================================================
# 7. VISTA CATEGORÍA
# ==============================================================================

def render_category():
    cat = st.session_state.category
    st.markdown(f"<h2>{cat.upper()} | Análisis Profundo</h2>", unsafe_allow_html=True)
    if st.button("↩ VOLVER AL PANEL GLOBAL"):
        st.session_state.view = 'Home'; st.rerun()

    kpi_map = {
        "Comercial": ["Ventas vs Costos", "Market Share", "Ticket Promedio", "Churn Rate"],
        "Capital Humano": ["Productividad", "Costo Laboral", "Ausentismo", "Capacitación"],
        "Logística": ["Stock vs Quiebre", "Lead Time", "Flete/Venta", "Rotación"]
    }

    tabs = st.tabs(kpi_map[cat])
    for i, kpi in enumerate(kpi_map[cat]):
        with tabs[i]:
            st.markdown(f"### Métrica: {kpi}")
            c1, c2 = st.columns([2, 1])
            with c1:
                if i % 2 == 0: st.plotly_chart(chart_dual_line(), use_container_width=True)
                else: st.plotly_chart(chart_multi_donut(), use_container_width=True)
            with c2:
                intel = KPI_INTELLIGENCE.get(kpi, KPI_INTELLIGENCE["Ventas vs Costos"])
                st.markdown(f'<div class="cx-card" style="padding:15px;"><p class="label-cx">DIAGNÓSTICO</p><p>{intel["detalle"]}</p></div>', unsafe_allow_html=True)

            st.markdown("#### Registro Maestro de Auditoría (1000 Registros)")
            st.dataframe(get_massive_data(), height=400, use_container_width=True)

# ==============================================================================
# 8. ORQUESTADOR
# ==============================================================================

def main():
    inject_cx_industrial_design()
    if st.session_state.view == 'Home':
        render_home()
    else:
        render_category()

if __name__ == "__main__":
    main()