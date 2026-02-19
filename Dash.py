import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ==============================================================================
# 1. CX BRAND IDENTITY & GLOBAL CONFIG (ZOOM 100% OPTIMIZED)
# ==============================================================================
st.set_page_config(page_title="GRIMOLDI CX | Intelligence", layout="wide", initial_sidebar_state="collapsed")

CX_THEME = {
    "bg_card": "#E2EBEE",     # Gris azulado claro
    "primary": "#086890",     # Azul profundo
    "accent": "#CE516F",      # Rojo/Pink Alerta
    "neutral": "#8A8F90",     # Gris etiquetas
    "cyan": "#57C5E4",        # Cyan comparativo
    "white": "#FFFFFF",
    "text": "#1A1F2B"
}

if 'view' not in st.session_state: st.session_state.view = 'Home'
if 'category' not in st.session_state: st.session_state.category = None

# ==============================================================================
# 2. CUSTOM CSS ENGINE (CONSERVANDO TU VISUAL ORIGINAL)
# ==============================================================================
def inject_cx_industrial_design():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        
        * {{ font-family: 'Inter', sans-serif !important; }}
        .stApp {{ background-color: {CX_THEME["white"]}; }}
        
        #MainMenu, footer, header {{ visibility: hidden; }}

        /* CX Cards - Optimización para Zoom 100% */
        .cx-card {{
            background-color: {CX_THEME["bg_card"]};
            padding: 30px;
            border-radius: 16px;
            border-left: 6px solid {CX_THEME["primary"]};
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }}

        /* Progress Bars */
        .pg-container {{ background: #D1D9DB; border-radius: 20px; height: 12px; margin: 10px 0; overflow: hidden; }}
        .pg-bar {{ background: {CX_THEME["primary"]}; height: 100%; border-radius: 20px; transition: width 0.8s ease-in-out; }}

        /* Tipografía */
        h1, h2, h3 {{ color: {CX_THEME["primary"]}; font-weight: 800 !important; }}
        .label-cx {{ color: {CX_THEME["neutral"]}; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }}
        
        /* Bloques de Explicación Detallada */
        .data-explanation {{
            background: #F8FAFB;
            border: 1px solid #D1D9DB;
            padding: 20px;
            border-radius: 12px;
            margin: 15px 0;
            font-size: 0.95rem;
            color: {CX_THEME["text"]};
            line-height: 1.6;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. COMPONENTES DE VISUALIZACIÓN (RESTAURADOS Y COMPLETOS)
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

def chart_multi_donut():
    fig = go.Figure()
    fig.add_trace(go.Pie(values=[60, 40], hole=0.8, marker=dict(colors=[CX_THEME["primary"], "#D1D9DB"]), domain={'x': [0, 1], 'y': [0, 1]}))
    fig.add_trace(go.Pie(values=[45, 55], hole=0.6, marker=dict(colors=[CX_THEME["accent"], "#E2EBEE"]), domain={'x': [0.15, 0.85], 'y': [0.15, 0.85]}))
    fig.update_layout(showlegend=False, height=250, template=get_cx_template())
    return fig

def chart_stacked_area(data_y):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=data_y, fill='tozeroy', fillcolor='rgba(87, 197, 228, 0.2)', 
                             line=dict(color=CX_THEME["cyan"], width=4), mode='lines'))
    fig.update_layout(template=get_cx_template(), height=300)
    return fig

def chart_rounded_bar(x, y):
    fig = go.Figure(go.Bar(x=x, y=y, marker=dict(color=CX_THEME["primary"]), width=0.6))
    fig.update_layout(template=get_cx_template(), height=300)
    return fig

def chart_stepped(y):
    fig = go.Figure(go.Scatter(y=y, line_shape='hv', line=dict(color=CX_THEME["accent"], width=4)))
    fig.update_layout(template=get_cx_template(), height=300)
    return fig

def chart_radial_gauge(val):
    fig = go.Figure(go.Indicator(mode="gauge+number", value=val, 
                                 gauge={'bar': {'color': CX_THEME["primary"]}, 'axis': {'range': [0, 100]}}))
    fig.update_layout(height=200, template=get_cx_template())
    return fig

def chart_dual_line():
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=[20, 35, 45, 30, 55], name="Real", line=dict(color=CX_THEME["primary"], width=4)))
    fig.add_trace(go.Scatter(y=[25, 30, 40, 35, 50], name="Target", line=dict(color=CX_THEME["neutral"], dash='dot')))
    fig.update_layout(template=get_cx_template(), height=300)
    return fig

# ==============================================================================
# 4. DATA ENGINE (1000 FILAS DE AUDITORÍA)
# ==============================================================================

@st.cache_data
def get_massive_audit_data():
    base = datetime(2026, 1, 1)
    return pd.DataFrame({
        'Fecha': [base + timedelta(hours=i) for i in range(1000)],
        'ID_Transaccion': [f'GR-{10000+i}' for i in range(1000)],
        'Local': np.random.choice(["Unicenter", "Florida", "Abasto", "E-Comm", "Rosario"], 1000),
        'Monto_Neto': np.random.uniform(5000, 75000, 1000).round(2),
        'Estado': np.random.choice(["Validado", "Pendiente", "Error"], 1000)
    })

# ==============================================================================
# 5. VISTA HOME (EXECUTIVE DASHBOARD)
# ==============================================================================

def render_home():
    st.markdown("<h1>SISTEMA DE ANÁLISIS INTEGRAL (D.A.I.)</h1>", unsafe_allow_html=True)
    st.markdown("<p class='label-cx'>Consolidado Estratégico Grimoldi S.A. | Q1 2026</p>", unsafe_allow_html=True)

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
    
    c_left, c_right = st.columns([1, 2])
    with c_left:
        st.subheader("Unidades Estratégicas")
        if st.button("🛒 ÁREA COMERCIAL", use_container_width=True):
            st.session_state.view = 'Category'; st.session_state.category = 'Comercial'; st.rerun()
        if st.button("👥 CAPITAL HUMANO", use_container_width=True):
            st.session_state.view = 'Category'; st.session_state.category = 'Capital Humano'; st.rerun()
        if st.button("📦 EFICIENCIA LOGÍSTICA", use_container_width=True):
            st.session_state.view = 'Category'; st.session_state.category = 'Logística'; st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("**Monitor de Cambio de Estado (Stepped Chart)**")
        st.plotly_chart(chart_stepped([10, 10, 25, 25, 40, 35]), use_container_width=True)

    with c_right:
        st.write("**Performance Histórica (Stacked Area CX)**")
        st.plotly_chart(chart_stacked_area([10, 25, 20, 45, 38, 55, 60]), use_container_width=True)
        st.markdown("""
            <div class="data-explanation">
                <strong>Análisis de la Métrica:</strong> El crecimiento proyectado para el cierre del Q1 indica una estabilización del 15% mensual. 
                <b>¿Por qué está bien?</b> La optimización de los canales digitales ha compensado la caída de tráfico en tiendas físicas. 
                <b>¿Por qué está mal?</b> El costo de adquisición por cliente ha subido un 4%, erosionando el margen neto.
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 6. VISTA CATEGORÍA (DEEP DIVE + RECOVERY DATA)
# ==============================================================================

def render_category():
    cat = st.session_state.category
    st.markdown(f"<h2>EXPLORACIÓN: {cat.upper()}</h2>", unsafe_allow_html=True)
    if st.button("↩ VOLVER AL PANEL GLOBAL"):
        st.session_state.view = 'Home'; st.rerun()

    tabs = st.tabs(["Dashboard de Rendimiento", "Auditoría de Datos", "Recomendaciones Directivas"])
    
    with tabs[0]:
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Distribución Relativa (Multi-Donut)**")
            st.plotly_chart(chart_multi_donut(), use_container_width=True)
        with c2:
            st.write("**Tendencia vs Target (Dual Line)**")
            st.plotly_chart(chart_dual_line(), use_container_width=True)

    with tabs[1]:
        st.markdown("#### Registro Maestro de Transacciones (1000 Filas)")
        st.dataframe(get_massive_audit_data(), height=450, use_container_width=True)

    with tabs[2]:
        st.markdown(f"""
            <div class="cx-card">
                <h3>Plan de Acción para {cat}</h3>
                <p>1. <b>Optimización de Costos:</b> Reducir en un 5% el desperdicio operativo mediante auditorías cruzadas.</p>
                <p>2. <b>Capacitación:</b> Implementar el nuevo protocolo CX en todas las sucursales del Nodo Sur.</p>
                <p>3. <b>Tecnología:</b> Migrar los procesos de conciliación al motor Zstd para reducir el lag de datos de 24h a 1h.</p>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 7. MAIN ORCHESTRATOR
# ==============================================================================

def main():
    inject_cx_industrial_design()
    if st.session_state.view == 'Home':
        render_home()
    else:
        render_category()

if __name__ == "__main__":
    main()