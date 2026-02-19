# ==============================================================================
# D.A.I. - DASHBOARD DE ANÁLISIS INTEGRAL (GRIMOLDI S.A.)
# Arquitectura: Navegación de Profundidad (Spotfire) + UI Zero-Friction (Stripe)
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import zstandard as zstd
import os
import plotly.graph_objects as go
import time

# ==============================================================================
# 1. CONFIGURACIÓN CORE Y ESTÁNDAR ZERO-FRICTION
# ==============================================================================
st.set_page_config(
    page_title="D.A.I. | Grimoldi",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. INYECCIÓN CSS AVANZADA (ESTÁNDAR STRIPE DESIGN SYSTEM & MICRO-ANIMATIONS)
# ==============================================================================
def inject_custom_css():
    st.markdown("""
        <style>
        /* Tipografía Inter (Estándar Apple/Stripe) */
        @import url('https://rsms.me/inter/inter.css');
        html, body, [class*="css"] { 
            font-family: 'Inter', sans-serif !important; 
            background-color: #F6F9FC !important; /* Fondo Stripe */
        }

        /* Ocultar elementos nativos de Streamlit para efecto SPA */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Animación Fade-In (Sexto Estándar) */
        @keyframes fadeInRise {
            0% { opacity: 0; transform: translateY(15px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .fade-in { animation: fadeInRise 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }

        /* Tarjetas de KPI (Stripe Cards) */
        .kpi-card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px rgba(50, 50, 93, 0.05), 0 1px 3px rgba(0, 0, 0, 0.03);
            border: 1px solid #e6ebf1;
            transition: all 0.2s ease;
        }
        .kpi-card:hover {
            box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
            transform: translateY(-2px);
        }
        
        /* Tipografías de la Tarjeta */
        .kpi-title { color: #4F566B; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }
        .kpi-value { color: #1A1F36; font-size: 2.2rem; font-weight: 800; line-height: 1.1; margin-bottom: 4px; }
        .kpi-delta-positive { color: #00D924; font-size: 0.9rem; font-weight: 600; }
        .kpi-delta-negative { color: #E25950; font-size: 0.9rem; font-weight: 600; }
        .kpi-context { color: #697386; font-size: 0.85rem; margin-top: 12px; border-top: 1px solid #e6ebf1; padding-top: 12px;}

        /* Encabezado Principal */
        .main-header { color: #1A1F36; font-weight: 900; font-size: 2.8rem; letter-spacing: -0.03em; margin-bottom: 0px; }
        .sub-header { color: #697386; font-weight: 400; font-size: 1.1rem; margin-bottom: 30px; }

        /* Cápsula de Insights (El Auditor) */
        .insight-capsule {
            background: linear-gradient(135deg, #f8f9fa 0%, #eef1f5 100%);
            border-left: 4px solid #635BFF;
            padding: 16px 20px;
            border-radius: 0 8px 8px 0;
            color: #3C4257;
            font-size: 0.95rem;
            line-height: 1.5;
            margin-top: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. MOTOR DE DATOS ZSTD / SQL (ESTÁNDAR 4)
# ==============================================================================
@st.cache_resource(show_spinner="Descomprimiendo Motor Zstd...")
def init_database():
    zst_file = "Grimoldi_Balance_Real.db.zst"
    db_file = "temp_grimoldi_runtime.db"
    
    # Proceso de descompresión en memoria temporal
    if os.path.exists(zst_file) and not os.path.exists(db_file):
        try:
            with open(zst_file, 'rb') as compressed:
                dctx = zstd.ZstdDecompressor()
                with open(db_file, 'wb') as uncompressed:
                    dctx.copy_stream(compressed, uncompressed)
        except Exception as e:
            st.error(f"Error Crítico en el Motor Zstd: {e}")
            return None
            
    # Conexión SQLite
    if os.path.exists(db_file):
        return sqlite3.connect(db_file, check_same_thread=False)
    return None

conn = init_database()

# ==============================================================================
# 4. DICCIONARIO DE MÉTRICAS Y ESTADO (ESTÁNDAR 5 y 6)
# ==============================================================================
def init_session_state():
    if 'layer' not in st.session_state:
        st.session_state.layer = 'home' # Capas: 'home', 'category'
    if 'current_category' not in st.session_state:
        st.session_state.current_category = None
    if 'current_kpi' not in st.session_state:
        st.session_state.current_kpi = None

init_session_state()

# Diccionario Balanced Scorecard Grimoldi
KPI_DICT = {
    "Comercial": ["Venta Bruta vs Obj", "UPT (Units/Ticket)", "Market Share", "Ticket Promedio", "Devoluciones"],
    "Capital Humano": ["Venta x Vendedor", "Ratio Costo Laboral", "Dotación vs m²", "Rotación Mensual", "Comisiones"],
    "Logística": ["Rotación de Inventario", "Lead Time", "Quiebre de Stock", "Costo Logístico", "Salud de Almacén"]
}

# Funciones de Navegación de Estado (SPA)
def nav_to_category(cat_name):
    st.session_state.layer = 'category'
    st.session_state.current_category = cat_name
    st.session_state.current_kpi = KPI_DICT[cat_name][0] # Selecciona el primero por defecto (Spotfire)

def nav_to_kpi(kpi_name):
    st.session_state.current_kpi = kpi_name

def nav_home():
    st.session_state.layer = 'home'
    st.session_state.current_category = None
    st.session_state.current_kpi = None

# ==============================================================================
# 5. COMPONENTES DE UI Y GRÁFICOS (ESTÉTICA ELITE)
# ==============================================================================
def render_kpi_card(title, value, delta_pct, context, positive_is_good=True):
    delta_class = "kpi-delta-positive" if (delta_pct >= 0 and positive_is_good) else "kpi-delta-negative"
    sign = "+" if delta_pct > 0 else ""
    
    html = f"""
    <div class="kpi-card fade-in">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="{delta_class}">{sign}{delta_pct}% vs mes anterior</div>
        <div class="kpi-context">{context}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def generate_elite_chart(kpi_name):
    # Generación de datos simulados de alta fidelidad para el gráfico (Plotly)
    # En producción real, esto hace un pd.read_sql sobre 'conn'
    np.random.seed(len(kpi_name))
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    valores = np.cumsum(np.random.randn(12) * 10 + 100)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=meses, y=valores,
        mode='lines+markers',
        line=dict(color='#635BFF', width=4, shape='spline'), # Stripe Blurple + Spline suave
        marker=dict(size=8, color='#F6F9FC', line=dict(width=2, color='#635BFF')),
        fill='tozeroy',
        fillcolor='rgba(99, 91, 255, 0.1)'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(showgrid=False, zeroline=False, color='#697386'),
        yaxis=dict(showgrid=True, gridcolor='#e6ebf1', gridwidth=1, zeroline=False, color='#697386'),
        height=350,
        hovermode="x unified"
    )
    return fig

# ==============================================================================
# 6. CAPA 0: SALUD FINANCIERA (THE BIG PICTURE)
# ==============================================================================
def render_layer_home():
    st.markdown('<div class="fade-in"><h1 class="main-header">D.A.I. Grimoldi</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Dashboard de Análisis Integral • Panel de Salud Corporativa</p></div>', unsafe_allow_html=True)
    
    # --- The Golden Metrics (Salud Financiera) ---
    st.markdown("### 🩺 Signos Vitales (Q3 - 2026)")
    col1, col2, col3, col4 = st.columns(4)
    with col1: render_kpi_card("ROI Global", "18.4%", 2.1, "Eficiencia de capital en temporada")
    with col2: render_kpi_card("Margen Neto", "12.2%", -0.5, "Afectado por costos logísticos", False)
    with col3: render_kpi_card("Punto de Equilibrio", "$45.2M", 1.2, "Cubierto al día 18 del mes")
    with col4: render_kpi_card("EBITDA", "$12.8M", 4.3, "Salud operativa pura")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # --- Categorías Zero-Friction (Navegación) ---
    st.markdown("### 🧭 Exploración de Áreas")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button("🛒 Comercial\n(Ventas, UPT, Market Share)", use_container_width=True): nav_to_category("Comercial")
    with c2:
        if st.button("👥 Capital Humano\n(Productividad, Payroll, Rotación)", use_container_width=True): nav_to_category("Capital Humano")
    with c3:
        if st.button("📦 Logística\n(Inventario, Lead Time, Fletes)", use_container_width=True): nav_to_category("Logística")

# ==============================================================================
# 7. CAPA 1 & 2: NAVEGACIÓN SPOTFIRE (EL FOCO TOTAL)
# ==============================================================================
def render_layer_category():
    cat = st.session_state.current_category
    kpi_actual = st.session_state.current_kpi
    
    # Header de Navegación
    col_back, col_title, _ = st.columns([1, 4, 1])
    with col_back:
        if st.button("← Volver al Home"): nav_home()
    with col_title:
        st.markdown(f"<h2 style='color:#1A1F36; margin-top:0;'>Área {cat}</h2>", unsafe_allow_html=True)
    
    st.divider()
    
    # Menú Superior Spotfire (Los 5 KPIs)
    cols = st.columns(5)
    for i, kpi in enumerate(KPI_DICT[cat]):
        with cols[i]:
            # Resaltar el KPI seleccionado
            tipo = "primary" if kpi == kpi_actual else "secondary"
            if st.button(kpi, use_container_width=True, type=tipo):
                nav_to_kpi(kpi)
                st.rerun()

    # --- La Lupa (Vista de KPI Individual) ---
    st.markdown(f"<div class='fade-in'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#4F566B; margin-top:20px;'>Foco: {kpi_actual}</h3>", unsafe_allow_html=True)
    
    g_col1, g_col2 = st.columns([7, 3]) # 70% Gráfico, 30% Datos duros
    
    with g_col1:
        # El Gráfico (Estándar 2)
        fig = generate_elite_chart(kpi_actual)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
    with g_col2:
        # El Número Grande y el Insight (Estándar 5)
        st.markdown(f"<h1 style='font-size:4rem; color:#1A1F36; line-height:1;'>14.2K</h1>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='color:#00D924;'>+8.4% vs T-1</h4>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="insight-capsule">
            <strong>Auditoría de IA:</strong><br>
            La métrica de '{kpi_actual}' muestra una tendencia alcista sostenida. 
            Recomendamos mantener la estrategia actual, ya que impacta positivamente en el flujo de caja del próximo trimestre.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 8. ORQUESTADOR PRINCIPAL (MAIN LOOP)
# ==============================================================================
def main():
    inject_custom_css()
    
    if st.session_state.layer == 'home':
        render_layer_home()
    elif st.session_state.layer == 'category':
        render_layer_category()

if __name__ == "__main__":
    main()
    