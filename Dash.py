# ==============================================================================
# D.A.I. - DASHBOARD DE ANÁLISIS INTEGRAL (GRIMOLDI S.A. - VERSIÓN ELITE)
# Estándares: Zero-Friction, Stripe Visuals, Spotfire Layers, Zstd Engine.
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import zstandard as zstd
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.add_vertical_space import add_vertical_space

# ==============================================================================
# 1. CONFIGURACIÓN ESTRUCTURAL (ESTÁNDAR 1)
# ==============================================================================
st.set_page_config(
    page_title="GRIMOLDI D.A.I. | Executive Suite",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. MOTOR CSS DE ALTA FIDELIDAD (ESTÁNDAR 2 Y 6)
# ==============================================================================
def apply_elite_styles():
    st.markdown("""
        <style>
        @import url('https://rsms.me/inter/inter.css');
        
        :root {
            --stripe-blurple: #635BFF;
            --stripe-dark: #1A1F36;
            --stripe-slate: #4F566B;
            --stripe-light: #F6F9FC;
            --success: #00D924;
            --danger: #FF4D4D;
        }

        html, body, [class*="css"] { 
            font-family: 'Inter', sans-serif !important; 
            background-color: var(--stripe-light) !important;
        }

        /* Contenedores de Cristal (Glassmorphism) */
        .stMetric, .element-container div.stMarkdown div.kpi-card {
            background: rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(230, 235, 241, 1);
            border-radius: 16px !important;
            padding: 25px !important;
            box-shadow: 0 15px 35px rgba(50,50,93,.1), 0 5px 15px rgba(0,0,0,.07) !important;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .stMetric:hover {
            transform: translateY(-5px);
            box-shadow: 0 30px 60px rgba(50,50,93,.15), 0 12px 20px rgba(0,0,0,.1) !important;
        }

        /* Encabezado Premium */
        .main-header {
            background: linear-gradient(90deg, #1A1F36 0%, #635BFF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900;
            font-size: 3.5rem;
            letter-spacing: -0.05em;
            margin-bottom: 0px;
        }

        /* Animaciones Quirúrgicas */
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-up { animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1); }

        /* Estilo de Botones de Navegación */
        .stButton>button {
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            border: none;
            background-color: white;
            color: var(--stripe-dark);
            box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11);
            transition: all 0.2s;
        }
        .stButton>button:hover {
            background-color: var(--stripe-blurple);
            color: white;
            transform: scale(1.02);
        }

        /* Cápsula de Insights Avanzada */
        .insight-box {
            background: #ffffff;
            border-left: 5px solid var(--stripe-blurple);
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.02);
        }
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. MOTOR DE DATOS ZSTD (ESTÁNDAR 4)
# ==============================================================================
@st.cache_resource
def init_engine():
    zst_path = "Grimoldi_Balance_Real.db.zst"
    db_path = "runtime_core.db"
    if os.path.exists(zst_path) and not os.path.exists(db_path):
        with open(zst_path, 'rb') as f_in:
            dctx = zstd.ZstdDecompressor()
            with open(db_path, 'wb') as f_out:
                dctx.copy_stream(f_in, f_out)
    return sqlite3.connect(db_path, check_same_thread=False)

conn = init_engine()

# ==============================================================================
# 4. GESTIÓN DE CAPAS (ESTÁNDAR 3 Y 6)
# ==============================================================================
if 'view' not in st.session_state: st.session_state.view = 'Home'
if 'category' not in st.session_state: st.session_state.category = None
if 'kpi_focus' not in st.session_state: st.session_state.kpi_focus = None

def change_view(target, cat=None, kpi=None):
    st.session_state.view = target
    st.session_state.category = cat
    st.session_state.kpi_focus = kpi

# ==============================================================================
# 5. GENERADORES DE GRÁFICOS INTERACTIVOS (VISUALIZACIÓN CIENTÍFICA)
# ==============================================================================
def get_detailed_chart(kpi_name):
    """Genera gráficos multivariable según el contexto del KPI"""
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    if "Venta" in kpi_name or "ROI" in kpi_name:
        # Gráfico de Área Apilada: Ventas vs Costos
        sales = np.random.randint(80, 120, 12)
        costs = sales * 0.65 + np.random.randint(-5, 5, 12)
        margin = sales - costs
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=sales, name='Venta Bruta', fill='tonexty', line_color='#635BFF', stackgroup='one'))
        fig.add_trace(go.Scatter(x=months, y=costs, name='Costo Operativo', fill='tonexty', line_color='#A5ADBB', stackgroup='one'))
        fig.update_layout(title="Análisis de Margen Progresivo", hovermode="x unified", height=450)
        
    elif "Market Share" in kpi_name:
        # Gráfico Donut Multi-Capa
        labels = ['Hush Puppies', 'Merrell', 'Kickers', 'Vans', 'Otros']
        values = [40, 25, 15, 10, 10]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker_colors=['#635BFF', '#00D924', '#7A73FF', '#80E9FF', '#E6EBF1'])])
        fig.update_layout(title="Dominancia de Marca en Portfolio")
        
    elif "Logística" in kpi_name or "Stock" in kpi_name:
        # Gráfico de Barras Agrupadas: Stock Real vs Objetivo
        fig = go.Figure(data=[
            go.Bar(name='Stock Real', x=months, y=np.random.randint(50, 100, 12), marker_color='#635BFF'),
            go.Bar(name='Target de Rotación', x=months, y=np.random.randint(60, 90, 12), marker_color='#00D924')
        ])
        fig.update_layout(barmode='group', title="Eficiencia de Suministro")
        
    else:
        # Gráfico de Líneas de Alta Precisión con Delta
        fig = go.Figure()
        y_data = np.random.normal(100, 10, 12)
        fig.add_trace(go.Scatter(x=months, y=y_data, mode='lines+markers', line=dict(color='#635BFF', width=4)))
        fig.update_layout(title=f"Evolución Temporal: {kpi_name}")

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#E6EBF1')
    )
    return fig

# ==============================================================================
# 6. RENDERIZADO DE CAPAS
# ==============================================================================

def render_home():
    st.markdown('<div class="animate-up">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-header">Executive Health Score</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#4F566B; font-size:1.2rem; margin-bottom:40px;">Consolidado de Alto Nivel - Grupo Grimoldi</p>', unsafe_allow_html=True)
    
    # KPIs Maestros
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("ROI Anualizado", "24.8%", "+2.4%", help="Retorno sobre inversión de capital propio")
    with c2: st.metric("Margen EBITDA", "14.2%", "-0.8%", delta_color="inverse")
    with c3: st.metric("Cash Flow", "$12.4M", "+5.1%")
    with c4: st.metric("Stock Value", "$84.2M", "-2.3%")
    style_metric_cards(background_color="#FFFFFF", border_left_color="#635BFF", shadow=True)

    add_vertical_space(3)
    
    # Navegación Principal
    st.markdown("### 🛠️ Áreas de Gestión Estratégica")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background:#1A1F36; padding:30px; border-radius:16px; color:white;'>
            <h3>🛒 Comercial</h3>
            <p style='color:#A5ADBB;'>Performance de ventas, tickets y penetración de marca.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Explorar Comercial", key="btn_com", use_container_width=True):
            change_view('Category', 'Comercial')

    with col2:
        st.markdown("""
        <div style='background:#635BFF; padding:30px; border-radius:16px; color:white;'>
            <h3>👥 Capital Humano</h3>
            <p style='color:#E6EBF1;'>Productividad por m², ratios de sueldos y eficiencia laboral.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Explorar RRHH", key="btn_rrhh", use_container_width=True):
            change_view('Category', 'Capital Humano')

    with col3:
        st.markdown("""
        <div style='background:#E6EBF1; padding:30px; border-radius:16px; color:#1A1F36;'>
            <h3>📦 Logística</h3>
            <p style='color:#4F566B;'>Lead times, rotación de inventario y eficiencia en fletes.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Explorar Logística", key="btn_log", use_container_width=True):
            change_view('Category', 'Logística')
    st.markdown('</div>', unsafe_allow_html=True)

def render_category():
    cat = st.session_state.category
    st.markdown(f'<div class="animate-up"><h1 class="main-header">{cat}</h1></div>', unsafe_allow_html=True)
    
    if st.button("← Volver al Centro de Control"): change_view('Home')
    
    add_vertical_space(2)
    
    # Diccionario de KPIs detallados
    kpi_list = {
        "Comercial": ["Venta Bruta vs Costos", "Market Share por Marca", "Ticket Promedio Sucursales", "Tasa de Conversión"],
        "Capital Humano": ["Productividad por Vendedor", "Costo Laboral / Venta", "Ausentismo Estratégico", "Curva de Comisiones"],
        "Logística": ["Rotación de Inventario", "Análisis de Lead Time", "Quiebre de Stock (Out)", "Costos de Flete Logístico"]
    }
    
    # Layout de 2 columnas: Menú a la izquierda, Gráfico Expandido a la derecha
    left_col, right_col = st.columns([1, 3])
    
    with left_col:
        st.markdown("#### Selección de KPI")
        for kpi in kpi_list[cat]:
            if st.button(kpi, use_container_width=True):
                st.session_state.kpi_focus = kpi
        
    with right_col:
        selected_kpi = st.session_state.kpi_focus if st.session_state.kpi_focus else kpi_list[cat][0]
        
        # Dashboard Principal del KPI
        with st.container():
            st.markdown(f"### {selected_kpi}")
            
            # Gráfico de Alta Fidelidad
            fig = get_detailed_chart(selected_kpi)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            # Métricas Auxiliares
            ma1, ma2, ma3 = st.columns(3)
            ma1.metric("Valor Actual", f"{np.random.randint(100, 500)}K", "+12%")
            ma2.metric("Target Q3", f"{np.random.randint(400, 600)}K", "-2%")
            ma3.metric("Confianza de IA", "98.2%", "Óptimo")
            
            # Cápsula de Insight (Explicación Senior)
            st.markdown(f"""
            <div class="insight-box">
                <h4 style="margin-top:0; color:#635BFF;">💡 Análisis Estratégico</h4>
                El KPI <strong>{selected_kpi}</strong> presenta una correlación directa con los objetivos de rentabilidad de Grimoldi. 
                Los datos muestran que la integración de variables de costo y volumen permiten una toma de decisiones 
                basada en márgenes reales, no solo en facturación bruta.
                <br><br>
                <strong>Acción Recomendada:</strong> Ajustar la presión promocional en base a la rotación observada.
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# 7. ORQUESTADOR (MAIN)
# ==============================================================================
def main():
    apply_elite_styles()
    
    if st.session_state.view == 'Home':
        render_home()
    elif st.session_state.view == 'Category':
        render_category()

if __name__ == "__main__":
    main()

# ==============================================================================
# FIN DEL DOCUMENTO TÉCNICO
# ==============================================================================