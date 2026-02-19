# ==============================================================================
# D.A.I. - GRIMOLDI LUXURY EDITION (INTEGRATED INTELLIGENCE)
# Sistema de Inteligencia de Negocios - Grado Directorio
# Estándares: Trailblaze Aesthetic + Deep Analytics + Actionable Insights
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import zstandard as zstd
import os
import plotly.graph_objects as go
from datetime import datetime

# ==============================================================================
# 1. CONFIGURACIÓN ESTRUCTURAL
# ==============================================================================
st.set_page_config(
    page_title="GRIMOLDI | Strategic Intelligence",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'view' not in st.session_state: st.session_state.view = 'Home'
if 'category' not in st.session_state: st.session_state.category = None

# ==============================================================================
# 2. MOTOR VISUAL TRAILBLAZE (CSS EXPANDIDO)
# ==============================================================================
def inject_trailblaze_vibe():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
        
        :root {
            --bg-deep: #0A0A0A;
            --accent-gold: #D4AF37;
            --text-main: #FFFFFF;
            --text-dim: #A0A0A0;
            --card-bg: #161616;
            --border-glow: rgba(212, 175, 55, 0.2);
        }

        .stApp { background-color: var(--bg-deep) !important; color: var(--text-main) !important; }
        #MainMenu, footer, header { visibility: hidden; }

        .hero-container {
            padding: 80px 50px;
            background: linear-gradient(90deg, #0A0A0A 0%, #1a1a1a 100%);
            border-bottom: 1px solid #333;
            margin-bottom: 40px;
        }
        
        .hero-title {
            font-family: 'Inter', sans-serif; font-weight: 900; font-size: 5rem;
            line-height: 1; letter-spacing: -2px; margin-bottom: 20px;
            background: linear-gradient(to right, #FFFFFF, var(--accent-gold));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }

        .metric-card-custom {
            background: var(--card-bg); border: 1px solid #333;
            border-radius: 4px; padding: 40px 30px; transition: all 0.4s ease;
        }
        
        .metric-card-custom:hover {
            border-color: var(--accent-gold); box-shadow: 0 0 30px var(--border-glow);
        }

        .metric-label {
            color: var(--accent-gold); text-transform: uppercase;
            font-weight: 700; letter-spacing: 2px; font-size: 0.8rem; margin-bottom: 15px;
        }

        .metric-value { font-size: 3.5rem; font-weight: 900; color: #FFF; }

        .stButton>button {
            background-color: transparent !important; color: var(--text-main) !important;
            border: 2px solid var(--accent-gold) !important; border-radius: 0px !important;
            padding: 1.5rem 2rem !important; font-weight: 700 !important;
            text-transform: uppercase !important; letter-spacing: 2px !important; width: 100%;
        }

        .stButton>button:hover { background-color: var(--accent-gold) !important; color: #000 !important; }

        /* Contenedores de Inteligencia */
        .tech-box {
            background: #111; border-left: 2px solid var(--accent-gold);
            padding: 25px; margin-top: 20px; border-radius: 0 8px 8px 0;
        }
        
        .rec-box {
            background: rgba(212, 175, 55, 0.05); border: 1px dashed var(--accent-gold);
            padding: 25px; margin-top: 20px; border-radius: 8px;
        }

        .stTabs [data-baseweb="tab"] { color: var(--text-dim); }
        .stTabs [aria-selected="true"] { color: var(--accent-gold) !important; }
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. MOTOR DE DATOS & INTELIGENCIA DE NEGOCIO
# ==============================================================================
def get_kpi_intelligence(kpi_name):
    """Retorna la explicación técnica y recomendaciones para cada KPI."""
    intel = {
        "Ventas vs Costos": {
            "tech": "Análisis de dispersión temporal entre ingresos brutos y egresos operativos (OPEX + COGS). Mide la eficiencia del flujo de caja.",
            "recs": ["Optimizar la cadena de suministro para reducir COGS en un 3%.", "Revisar contratos de servicios fijos para aplanar la curva de OPEX.", "Implementar Dynamic Pricing en picos de demanda."]
        },
        "Market Share por Marca": {
            "tech": "Distribución porcentual del volumen de ventas capturado por cada marca del portafolio. Detecta canibalización interna.",
            "recs": ["Reforzar marketing en marcas con margen > 20%.", "Identificar marcas nicho para expansión de puntos de venta.", "Descontinuar SKUs de baja rotación en marcas 'Otros'."]
        },
        "Ticket Promedio": {
            "tech": "Valor medio de transacción por cliente. Indica la efectividad de las estrategias de up-selling y cross-selling.",
            "recs": ["Implementar bundles (combos) de calzado + accesorios.", "Capacitar fuerza de venta en técnicas de sugerencia premium.", "Ajustar umbral de envío gratis para incentivar mayor compra."]
        },
        "Productividad": {
            "tech": "Ratio de ventas logradas por hora hombre/vendedor. Mide la eficiencia del capital humano en el salón de ventas.",
            "recs": ["Gamificar objetivos diarios para motivar al staff.", "Redistribuir personal según mapas de calor de tráfico en tienda.", "Automatizar tareas administrativas para liberar tiempo de venta."]
        },
        "Rotación de Inventario": {
            "tech": "Frecuencia con la que el stock se renueva totalmente. Un ratio alto indica agilidad; uno bajo, capital inmovilizado.",
            "recs": ["Liquidación agresiva de stock estancado (+180 días).", "Sincronizar pedidos con previsiones meteorológicas.", "Mejorar la precisión del picking para evitar devoluciones."]
        }
        # Fallback genérico para otros KPIs
    }
    default = {
        "tech": "Visualización multivariable del rendimiento operativo mensual frente a objetivos estratégicos establecidos por el directorio.",
        "recs": ["Realizar auditoría de procesos en los puntos críticos detectados.", "Ajustar el presupuesto del próximo trimestre según esta tendencia.", "Escalar las mejores prácticas de las unidades líderes."]
    }
    return intel.get(kpi_name, default)

# ==============================================================================
# 4. COMPONENTES GRÁFICOS RECUPERADOS Y MEJORADOS
# ==============================================================================
def draw_integrated_chart(kpi_name):
    months = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']
    fig = go.Figure()
    
    # Lógica de renderizado según el tipo de KPI recuperado
    if "Ventas" in kpi_name:
        y1 = np.random.randint(150, 250, 12)
        y2 = y1 * 0.6 + np.random.randint(5, 15, 12)
        fig.add_trace(go.Scatter(x=months, y=y1, name='VENTAS', line=dict(color='#FFF', width=4), fill='tozeroy'))
        fig.add_trace(go.Scatter(x=months, y=y2, name='COSTOS', line=dict(color='#D4AF37', width=2, dash='dot')))
    
    elif "Market Share" in kpi_name or "Marca" in kpi_name:
        labels = ['Hush Puppies', 'Merrell', 'Kickers', 'Vans', 'Otros']
        fig.add_trace(go.Pie(labels=labels, values=[35, 25, 15, 15, 10], hole=0.6, marker=dict(colors=['#D4AF37', '#FFF', '#555', '#222', '#888'])))
    
    elif "Stock" in kpi_name or "Quiebre" in kpi_name:
        fig.add_trace(go.Bar(x=months, y=np.random.randint(70, 100, 12), name='STOCK', marker_color='#D4AF37'))
        fig.add_trace(go.Bar(x=months, y=np.random.randint(5, 15, 12), name='QUIEBRE', marker_color='#FF4D00'))
        fig.update_layout(barmode='stack')
        
    else: # Lineal estándar para el resto
        fig.add_trace(go.Scatter(x=months, y=np.random.normal(100, 15, 12), mode='lines+markers', line=dict(color='#D4AF37', width=3)))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#A0A0A0'), showlegend=True,
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#222')
    )
    return fig

# ==============================================================================
# 5. RENDERIZADO DE CAPAS
# ==============================================================================

def render_home():
    st.markdown("""
        <div class="hero-container">
            <div class="metric-label">Grimoldi S.A. | Executive Intelligence</div>
            <h1 class="hero-title">RESULTS<br>IN RESIDENCE.</h1>
            <p style="font-size: 1.5rem; color: #A0A0A0; max-width: 600px;">
                Dashboard de alta fidelidad. Recuperación total de KPIs operativos bajo el nuevo estándar visual de directorio.
            </p>
        </div>
    """, unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1: 
        st.markdown('<div class="metric-card-custom"><div class="metric-label">ROI GLOBAL</div><div class="metric-value">28.4%</div><div style="color:#00D924">+3.2% ↑</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="metric-card-custom"><div class="metric-label">EBITDA</div><div class="metric-value">$18.2M</div><div style="color:#00D924">+5.4% ↑</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="metric-card-custom"><div class="metric-label">LIQUIDEZ</div><div class="metric-value">1.65</div><div style="color:#FF4D00">-0.1% ↓</div></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for i, (label, view) in enumerate([("01. COMERCIAL", "Comercial"), ("02. CAPITAL HUMANO", "Capital Humano"), ("03. LOGÍSTICA", "Logística")]):
        with [c1, c2, c3][i]:
            if st.button(label):
                st.session_state.view = 'Category'
                st.session_state.category = view
                st.rerun()

def render_category():
    cat = st.session_state.category
    
    # Navegación Superior
    col_t, col_b = st.columns([4, 1])
    with col_t: st.markdown(f"<h1 style='font-weight:900; font-size:4rem;'>{cat.upper()}</h1>", unsafe_allow_html=True)
    with col_b: 
        if st.button("CLOSE X"):
            st.session_state.view = 'Home'
            st.rerun()

    # Recuperación de los 4 KPIs por categoría
    kpis_config = {
        "Comercial": ["Ventas vs Costos", "Market Share por Marca", "Ticket Promedio", "Tasa de Conversión"],
        "Capital Humano": ["Productividad", "Ratio Payroll/Ventas", "Ausentismo", "Rotación"],
        "Logística": ["Rotación de Inventario", "Lead Time Distribución", "Flete sobre Venta", "Stock vs Quiebre"]
    }

    tabs = st.tabs(kpis_config[cat])
    
    for i, kpi_name in enumerate(kpis_config[cat]):
        with tabs[i]:
            st.markdown(f"<h2 style='color:#FFF; margin-top:30px;'>{kpi_name}</h2>", unsafe_allow_html=True)
            
            # Layout: Gráfico Principal
            st.plotly_chart(draw_integrated_chart(kpi_name), use_container_width=True)
            
            # Bloques de Inteligencia solicitados
            intel = get_kpi_intelligence(kpi_name)
            
            col_inf1, col_inf2 = st.columns(2)
            with col_inf1:
                st.markdown(f"""
                    <div class="tech-box">
                        <h4 style="color:var(--accent-gold); margin-top:0;">🔍 EXPLICACIÓN TÉCNICA</h4>
                        <p style="color:var(--text-dim); font-size:0.95rem;">{intel['tech']}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_inf2:
                recs_html = "".join([f"<li>{r}</li>" for r in intel['recs']])
                st.markdown(f"""
                    <div class="rec-box">
                        <h4 style="color:var(--accent-gold); margin-top:0;">💡 RECOMENDACIONES ESTRATÉGICAS</h4>
                        <ul style="color:var(--text-main); font-size:0.95rem; padding-left:20px;">
                            {recs_html}
                        </ul>
                    </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# 6. ORQUESTADOR
# ==============================================================================
def main():
    inject_trailblaze_vibe()
    if st.session_state.view == 'Home':
        render_home()
    else:
        render_category()

if __name__ == "__main__":
    main()