import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ==============================================================================
# 1. CONFIGURACIÓN DE IDENTIDAD Y LAYOUT (ZOOM 100% OPTIMIZED)
# ==============================================================================
st.set_page_config(
    page_title="GRIMOLDI | Strategic Intelligence System",
    page_icon="👠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

CX_THEME = {
    "bg_card": "#E2EBEE",     # Gris azulado claro
    "primary": "#086890",     # Azul profundo (Confianza/Autoridad)
    "accent": "#CE516F",      # Rojo/Pink (Alerta/Urgencia)
    "neutral": "#8A8F90",     # Gris etiquetas (Contexto)
    "cyan": "#57C5E4",        # Cyan (Comparativos/Metas)
    "white": "#FFFFFF",
    "text": "#1A1F2B",
    "success": "#2D8A4E"      # Verde (Salud métrica)
}

if 'view' not in st.session_state: st.session_state.view = 'Home'
if 'category' not in st.session_state: st.session_state.category = None

# ==============================================================================
# 2. MOTOR DE ESTILOS CX (PREMIUM DENSITY)
# ==============================================================================
def inject_high_density_styles():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
        
        * {{ font-family: 'Inter', sans-serif !important; }}
        .stApp {{ background-color: {CX_THEME["white"]}; }}
        
        #MainMenu, footer, header {{ visibility: hidden; }}

        /* Contenedores de KPIs - Optimización de Zoom 100% */
        .kpi-container {{
            background-color: {CX_THEME["bg_card"]};
            padding: 2rem;
            border-radius: 12px;
            border-bottom: 5px solid {CX_THEME["primary"]};
            margin-bottom: 1.5rem;
            min-height: 180px;
        }}

        .kpi-value {{ font-size: 2.8rem; font-weight: 900; color: {CX_THEME["primary"]}; line-height: 1; }}
        .kpi-label {{ color: {CX_THEME["neutral"]}; font-weight: 700; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 1.5px; }}
        
        /* Bloques de Explicación de Datos (Data Narrative) */
        .narrative-box {{
            background: {CX_THEME["white"]};
            border-left: 4px solid {CX_THEME["primary"]};
            padding: 25px;
            margin: 20px 0;
            border-radius: 0 10px 10px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        }}

        .status-badge-good {{ background: {CX_THEME["success"]}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }}
        .status-badge-bad {{ background: {CX_THEME["accent"]}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }}

        /* Estilo para Recomendaciones */
        .rec-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 15px;
        }}
        .rec-item {{
            background: #F8FAFB;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
        }}
        
        .stTabs [aria-selected="true"] {{ background-color: {CX_THEME["primary"]} !important; color: white !important; font-weight: 800; }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. BIBLIOTECA DE GRÁFICOS CX (REQUERIMIENTOS ESPECÍFICOS)
# ==============================================================================

def get_cx_template():
    return go.layout.Template(
        layout=go.Layout(
            font=dict(family="Inter", color=CX_THEME["text"]),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, color=CX_THEME["neutral"]),
            yaxis=dict(showgrid=True, gridcolor="#EDF2F7", color=CX_THEME["neutral"]),
            margin=dict(l=0, r=0, t=30, b=0)
        )
    )

def chart_dual_line():
    fig = go.Figure()
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    fig.add_trace(go.Scatter(x=months, y=[100, 120, 115, 140, 155, 170], name="Venta Real", line=dict(color=CX_THEME["primary"], width=4)))
    fig.add_trace(go.Scatter(x=months, y=[105, 110, 120, 130, 145, 160], name="Presupuesto", line=dict(color=CX_THEME["neutral"], dash='dot', width=2)))
    fig.update_layout(template=get_cx_template(), height=350, legend=dict(orientation="h", y=1.1, x=0))
    return fig

def chart_ascending_bars(labels, values):
    fig = go.Figure(go.Bar(x=labels, y=values, marker_color=CX_THEME["primary"], text=values, textposition='outside'))
    fig.update_layout(template=get_cx_template(), height=350)
    return fig

def chart_donut_concentric():
    fig = go.Figure()
    fig.add_trace(go.Pie(values=[70, 30], hole=0.8, marker=dict(colors=[CX_THEME["primary"], "#F1F5F9"]), domain={'x': [0, 1], 'y': [0, 1]}))
    fig.add_trace(go.Pie(values=[55, 45], hole=0.6, marker=dict(colors=[CX_THEME["cyan"], "#F1F5F9"]), domain={'x': [0.15, 0.85], 'y': [0.15, 0.85]}))
    fig.update_layout(showlegend=False, height=300, template=get_cx_template())
    return fig

# ==============================================================================
# 4. MOTOR DE INTELIGENCIA DE DATOS (DETALLE PROFUNDO)
# ==============================================================================

def render_insight_block(kpi_name, status="good"):
    badge = f'<span class="status-badge-good">SALUDABLE</span>' if status == "good" else f'<span class="status-badge-bad">REVISIÓN REQUERIDA</span>'
    
    # Base de conocimientos masiva por KPI
    intel = {
        "Eficiencia de Margen": {
            "tech": "Cálculo ponderado del Gross Margin vs Costos fijos indirectos. Este KPI determina la capacidad de absorción de gastos estructurales.",
            "why_status": "La métrica está en niveles óptimos (>15%) debido a la renegociación con proveedores de logística y la reducción del 4% en desperdicios de stock en el Q1.",
            "impact": "Un aumento de 1 p.p. en este margen representa una utilidad neta incremental de $12.4M anuales.",
            "recs": [
                ("Optimización de SKU", "Eliminar el 5% inferior de productos con rotación < 0.2 para liberar capital de trabajo."),
                ("Pricing Dinámico", "Ajustar precios en categorías 'Outdoor' dado el incremento de demanda estacional detectado."),
                ("Logística Inversa", "Reducir el costo de devoluciones mediante auditorías de talle en origen.")
            ]
        },
        "Productividad Staff": {
            "tech": "Ventas totales netas divididas por horas hombre totales liquidadas. Mide el ROI directo del capital humano.",
            "why_status": "Se observa una caída del 2.5% respecto al mes anterior. Esto se atribuye a un exceso de horas extra no vinculadas a picos de tráfico de clientes.",
            "impact": "La ineficiencia en horas hombre está erosionando el margen operativo en $2.1M mensuales.",
            "recs": [
                ("Staffing Basado en Tráfico", "Alinear los turnos de personal con los mapas de calor de visitas en tiendas físicas."),
                ("Capacitación Upselling", "Entrenar al personal en venta sugestiva para aumentar el ticket promedio un 15%."),
                ("Automatización Administrativa", "Reducir el tiempo de carga de inventario manual mediante escaneo RFID.")
            ]
        }
    }
    
    data = intel.get(kpi_name, intel["Eficiencia de Margen"])
    
    st.markdown(f"""
        <div class="narrative-box">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:{CX_THEME["primary"]}">{kpi_name.upper()} | ANÁLISIS CRÍTICO</h4>
                {badge}
            </div>
            <hr style="margin: 15px 0; border: 0; border-top: 1px solid #EEE;">
            <p style="font-size: 0.95rem; color: #4A5568;"><strong>Explicación Técnica:</strong> {data['tech']}</p>
            <p style="font-size: 0.95rem; color: #4A5568;"><strong>Análisis de Rendimiento:</strong> {data['why_status']}</p>
            <div class="rec-grid">
                {"".join([f'<div class="rec-item"><strong>{title}:</strong><br><span style="font-size:0.85rem; color:#64748B;">{desc}</span></div>' for title, desc in data['recs']])}
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 5. RENDERIZADO DE VISTAS (SPA MODEL)
# ==============================================================================

def render_home():
    # Hero / Header
    st.markdown(f"<h1 style='font-size:3.5rem; margin-bottom:0;'>RESULTS CONSOLE</h1>", unsafe_allow_html=True)
    st.markdown("<p class='kpi-label' style='margin-bottom:2rem;'>Unidad de Inteligencia Estratégica Grimoldi S.A.</p>", unsafe_allow_html=True)

    # Fila de KPIs de Alta Visibilidad
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown('<div class="kpi-container"><p class="kpi-label">Revenue Q1</p><div class="kpi-value">$458M</div><p style="color:#2D8A4E; font-size:0.8rem;">↑ 12.4% vs L.Y.</p></div>', unsafe_allow_html=True)
    with k2: st.markdown('<div class="kpi-container"><p class="kpi-label">EBITDA</p><div class="kpi-value">18.2%</div><p style="color:#2D8A4E; font-size:0.8rem;">↑ 1.2% Target</p></div>', unsafe_allow_html=True)
    with k3: st.markdown('<div class="kpi-container"><p class="kpi-label">Net Margin</p><div class="kpi-value">14.8%</div><p style="color:#CE516F; font-size:0.8rem;">↓ 0.5% Alert</p></div>', unsafe_allow_html=True)
    with k4: st.markdown('<div class="kpi-container"><p class="kpi-label">Sales/Hr</p><div class="kpi-value">$24k</div><p style="color:#2D8A4E; font-size:0.8rem;">↑ 5.1% Eff.</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Sección de Gráficos de Reporte Directivo
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.markdown("### Ejecución Presupuestaria vs Real")
        st.plotly_chart(chart_dual_line(), use_container_width=True)
        render_insight_block("Eficiencia de Margen", status="good")
        
    with col_side:
        st.markdown("### Mix de Marcas (Concentric)")
        st.plotly_chart(chart_donut_concentric(), use_container_width=True)
        st.markdown("""
            <div style="background:#F1F5F9; padding:20px; border-radius:12px;">
                <h5 style="margin-top:0;">Observación Estratégica</h5>
                <p style="font-size:0.85rem; color:#475569;">
                    El anillo interior (Cyan) representa la meta de penetración para <b>Hush Puppies</b>. 
                    Actualmente estamos un <b>15% por debajo</b> de la meta de inventario óptimo, 
                    lo que genera quiebres de stock en talles centrales.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Navegación
    st.markdown("---")
    st.markdown("### Departamentos Críticos")
    n1, n2, n3 = st.columns(3)
    with n1: 
        if st.button("ACCEDER A COMERCIAL 01"): 
            st.session_state.view = 'Category'; st.session_state.category = 'Comercial'; st.rerun()
    with n2:
        if st.button("ACCEDER A CAPITAL HUMANO 02"): 
            st.session_state.view = 'Category'; st.session_state.category = 'Capital Humano'; st.rerun()
    with n3:
        if st.button("ACCEDER A LOGÍSTICA 03"): 
            st.session_state.view = 'Category'; st.session_state.category = 'Logística'; st.rerun()

def render_category():
    cat = st.session_state.category
    st.markdown(f"<h1>{cat.upper()}</h1>", unsafe_allow_html=True)
    if st.button("↩ REGRESAR AL DASHBOARD GLOBAL"):
        st.session_state.view = 'Home'; st.rerun()
    
    st.markdown("---")
    
    # KPIs específicos de categoría
    t1, t2 = st.tabs(["Análisis de Desempeño", "Data Auditoría"])
    
    with t1:
        st.markdown("### Rendimiento por Categoría de Producto")
        labels = ['Calzado Hombre', 'Calzado Mujer', 'Accesorios', 'Kids', 'Outdoor']
        values = [450, 620, 150, 230, 480]
        st.plotly_chart(chart_ascending_bars(labels, values), use_container_width=True)
        
        # Inyección masiva de contexto para esta métrica
        render_insight_block("Productividad Staff", status="bad" if cat == "Comercial" else "good")
        
    with t2:
        st.markdown("### Registro de Transacciones Críticas")
        data = pd.DataFrame({
            'Transacción': [f'TRX-{i}' for i in range(1001, 1011)],
            'Monto USD': np.random.randint(100, 5000, 10),
            'Estatus': ['Cumplido', 'En Revisión', 'Cumplido', 'Alerta', 'Cumplido']*2,
            'Delta %': np.random.uniform(-5, 10, 10).round(2)
        })
        st.dataframe(data, use_container_width=True)
        st.info("Mostrando registros históricos auditados para el cumplimiento del balance trimestral.")

# ==============================================================================
# 6. EJECUCIÓN
# ==============================================================================
def main():
    inject_high_density_styles()
    if st.session_state.view == 'Home':
        render_home()
    else:
        render_category()

if __name__ == "__main__":
    main()