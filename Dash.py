import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ==============================================================================
# 1. CX BRAND IDENTITY & GLOBAL CONFIG
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
# 2. CUSTOM CSS ENGINE (REFACTOR UI/UX)
# ==============================================================================
def inject_cx_industrial_design():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        
        * {{ font-family: 'Inter', sans-serif !important; }}
        .stApp {{ background-color: {CX_THEME["white"]}; }}
        
        /* Ocultar basura nativa */
        #MainMenu, footer, header {{ visibility: hidden; }}

        /* CX Cards */
        .cx-card {{
            background-color: {CX_THEME["bg_card"]};
            padding: 30px;
            border-radius: 16px;
            border-left: 6px solid {CX_THEME["primary"]};
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }}

        /* Progress Bars Personalizadas */
        .pg-container {{ background: #D1D9DB; border-radius: 20px; height: 12px; margin: 10px 0; overflow: hidden; }}
        .pg-bar {{ background: {CX_THEME["primary"]}; height: 100%; border-radius: 20px; transition: width 0.8s ease-in-out; }}

        /* Tabs CX */
        .stTabs [data-baseweb="tab-list"] {{ gap: 24px; }}
        .stTabs [data-baseweb="tab"] {{
            padding: 10px 20px; background-color: {CX_THEME["bg_card"]};
            border-radius: 8px 8px 0 0; color: {CX_THEME["neutral"]};
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {CX_THEME["primary"]} !important; color: white !important;
        }}

        /* Tipografía */
        h1, h2, h3 {{ color: {CX_THEME["primary"]}; font-weight: 800 !important; }}
        .label-cx {{ color: {CX_THEME["neutral"]}; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }}
        
        /* Tablas */
        .styled-table {{ width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 0.9em; min-width: 400px; }}
        .styled-table thead tr {{ background-color: {CX_THEME["primary"]}; color: #ffffff; text-align: left; }}
        .styled-table th, .styled-table td {{ padding: 12px 15px; border-bottom: 1px solid #dddddd; }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. COMPONENTES DE VISUALIZACIÓN CX (REQUERIMIENTOS ESPECÍFICOS)
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

def chart_multi_donut(values1=[60, 40], values2=[45, 55], labels=["Real", "Gap"]):
    fig = go.Figure()
    fig.add_trace(go.Pie(values=values1, hole=0.8, marker=dict(colors=[CX_THEME["primary"], "#D1D9DB"]), domain={'x': [0, 1], 'y': [0, 1]}))
    fig.add_trace(go.Pie(values=values2, hole=0.6, marker=dict(colors=[CX_THEME["accent"], "#E2EBEE"]), domain={'x': [0.15, 0.85], 'y': [0.15, 0.85]}))
    fig.update_layout(showlegend=False, height=250, template=get_cx_template())
    return fig

def chart_stacked_area(data_y):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=data_y, fill='tozeroy', fillcolor='rgba(87, 197, 228, 0.2)', 
                             line=dict(color=CX_THEME["cyan"], width=4), mode='lines'))
    fig.update_layout(template=get_cx_template(), height=300)
    return fig

def chart_rounded_bar(x, y):
    fig = go.Figure(go.Bar(x=x, y=y, marker=dict(color=CX_THEME["primary"], line_width=0), width=0.6))
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

# ==============================================================================
# 4. LÓGICA DE NEGOCIO E INTELIGENCIA (RECOVERY DATA)
# ==============================================================================

KPI_INTEL = {
    "Ventas vs Costos": {
        "desc": "Correlación entre facturación bruta y erosión de margen por costos fijos/variables.",
        "recs": ["Revisar matriz de precios", "Optimizar costos de flete", "Estrategia de Cross-selling"],
        "tech": "Cálculo basado en SQL real-time vs Proyección Zstd."
    },
    "Market Share": {
        "desc": "Cuota de mercado relativa por unidad de negocio.",
        "recs": ["Incentivar marcas B", "Analizar competencia regional"],
        "tech": "Datos normalizados de auditoría externa."
    }
}

# ==============================================================================
# 5. VISTA HOME (EXECUTIVE DASHBOARD)
# ==============================================================================

def render_home():
    st.markdown("<h1>SISTEMA DE ANÁLISIS INTEGRAL (D.A.I.)</h1>", unsafe_allow_html=True)
    st.markdown("<p class='label-cx'>Consolidado Estratégico Grimoldi S.A. | Q1 2026</p>", unsafe_allow_html=True)

    # KPIs Principales con Progress Indicators (CX Req)
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
    
    # Grid de Navegación y Gráficos Resumen
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
        st.write("**Gauge de Eficiencia de Red**")
        st.plotly_chart(chart_radial_gauge(74), use_container_width=True)

    with c_right:
        st.write("**Performance Histórica (Stacked Area CX)**")
        st.plotly_chart(chart_stacked_area([10, 25, 20, 45, 38, 55, 60]), use_container_width=True)

# ==============================================================================
# 6. VISTA CATEGORÍA (DEEP DIVE + RECOVERY DATA)
# ==============================================================================

def render_category():
    cat = st.session_state.category
    st.markdown(f"<h2>EXPLORACIÓN: {cat.upper()}</h2>", unsafe_allow_html=True)
    
    if st.button("↩ VOLVER AL PANEL GLOBAL"):
        st.session_state.view = 'Home'; st.rerun()

    kpi_list = {
        "Comercial": ["Ventas vs Costos", "Market Share", "Ticket Promedio", "Tasa de Conversión"],
        "Capital Humano": ["Productividad", "Costo Laboral", "Ausentismo", "Rotación"],
        "Logística": ["Stock vs Quiebre", "Lead Time", "Flete sobre Venta", "Rotación Inv"]
    }

    tabs = st.tabs(kpi_list[cat])
    
    for i, kpi in enumerate(kpi_list[cat]):
        with tabs[i]:
            st.markdown(f"### {kpi}")
            
            # Layout Multivariable
            g1, g2 = st.columns([2, 1])
            
            with g1:
                if i == 0: st.plotly_chart(chart_rounded_bar(['E','F','M','A','M'], [40,55,45,70,65]), use_container_width=True)
                elif i == 1: st.plotly_chart(chart_multi_donut(), use_container_width=True)
                else: st.plotly_chart(chart_stepped([5,10,10,15,12,20]), use_container_width=True)
            
            with g2:
                # Recuperación de tablas y descripciones
                st.markdown(f"""
                    <div style="background:#f9f9f9; padding:15px; border-radius:10px;">
                        <p class="label-cx">ANATOMÍA DEL KPI</p>
                        <p><strong>Definición:</strong> {KPI_INTEL.get(kpi, KPI_INTEL["Ventas vs Costos"])["desc"]}</p>
                        <p><strong>Técnica:</strong> {KPI_INTEL.get(kpi, KPI_INTEL["Ventas vs Costos"])["tech"]}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("#### Recomendaciones")
                for r in KPI_INTEL.get(kpi, KPI_INTEL["Ventas vs Costos"])["recs"]:
                    st.write(f"• {r}")

            # Tabla de Datos Crudos (Recovery)
            st.markdown("#### Detalle de Transacciones Recientes")
            df_sim = pd.DataFrame({
                'Fecha': pd.date_range(start='2026-01-01', periods=5),
                'ID': ['GR-01', 'GR-02', 'GR-03', 'GR-04', 'GR-05'],
                'Valor': [np.random.randint(100,500) for _ in range(5)],
                'Estado': ['Aprobado', 'Aprobado', 'Pendiente', 'Aprobado', 'Revisión']
            })
            st.table(df_sim)

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