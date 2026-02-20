import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ==============================================================================
# 1. CX BRAND IDENTITY & GLOBAL CONFIG - MONOCHROME EDITION
# ==============================================================================
st.set_page_config(
    page_title="GRIMOLDI CX | Monochrome System", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Paleta en Blanco y Negro
CX_THEME = {
    "bg_card": "#F2F2F2",
    "primary": "#000000",   # Negro Puro
    "accent": "#444444",    # Gris Oscuro
    "neutral": "#888888",   # Gris Medio
    "light": "#D1D1D1",     # Gris Claro
    "white": "#FFFFFF",
    "text": "#000000",
    "success": "#333333"
}

MONEY_VALUATION = {
    "REVENUE_TARGET": 1250000000.00,
    "OPEX_LIMIT": 450000000.00,
    "MARKET_CAP_EST": 8500000000.00,
    "TASA_CONVERSION_ARS": 1050.00
}

if 'view' not in st.session_state: st.session_state.view = 'Home'
if 'category' not in st.session_state: st.session_state.category = None

# ==============================================================================
# 2. CUSTOM CSS ENGINE - MINIMALIST
# ==============================================================================
def inject_cx_industrial_design():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        * {{ font-family: 'Inter', sans-serif !important; }}
        .stApp {{ background-color: {CX_THEME["white"]}; }}
        #MainMenu, footer, header {{ visibility: hidden; }}
        .cx-card {{
            background-color: {CX_THEME["bg_card"]};
            padding: 30px;
            border-radius: 0px; /* Bordes rectos para look más minimalista */
            border-left: 8px solid {CX_THEME["primary"]};
            margin-bottom: 20px;
            box-shadow: none;
            border-top: 1px solid #E0E0E0;
            border-right: 1px solid #E0E0E0;
            border-bottom: 1px solid #E0E0E0;
        }}
        .pg-container {{ background: {CX_THEME["light"]}; border-radius: 0px; height: 8px; margin: 10px 0; overflow: hidden; }}
        .pg-bar {{ background: {CX_THEME["primary"]}; height: 100%; transition: width 0.8s ease-in-out; }}
        h1, h2, h3 {{ color: {CX_THEME["primary"]}; font-weight: 800 !important; letter-spacing: -1px; }}
        .label-cx {{ color: {CX_THEME["neutral"]}; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; }}
        .data-explanation {{
            background: #FFFFFF;
            border: 1px solid {CX_THEME["primary"]};
            padding: 20px;
            margin: 15px 0;
            font-size: 0.95rem;
            color: {CX_THEME["text"]};
        }}
        .money-badge {{
            background: {CX_THEME["primary"]};
            color: white;
            padding: 4px 10px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 10px;
        }}
        /* Estilo para botones B&N */
        .stButton>button {{
            border-radius: 0px;
            background-color: white;
            color: black;
            border: 2px solid black;
            font-weight: 700;
            transition: 0.3s;
        }}
        .stButton>button:hover {{
            background-color: black;
            color: white;
            border: 2px solid black;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. VISUALIZATION COMPONENTS - MONOCHROME
# ==============================================================================
def get_cx_template():
    return go.layout.Template(
        layout=go.Layout(
            font=dict(family="Inter", color=CX_THEME["text"]),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, zeroline=True, zerolinecolor="#000", color=CX_THEME["primary"]),
            yaxis=dict(showgrid=True, gridcolor="#E0E0E0", zeroline=False, color=CX_THEME["primary"]),
            margin=dict(l=10, r=10, t=30, b=10)
        )
    )

def chart_multi_donut(v1, v2):
    fig = go.Figure()
    fig.add_trace(go.Pie(values=[v1, 100-v1], hole=0.8, marker=dict(colors=[CX_THEME["primary"], CX_THEME["light"]]), domain={'x': [0, 1], 'y': [0, 1]}))
    fig.add_trace(go.Pie(values=[v2, 100-v2], hole=0.6, marker=dict(colors=[CX_THEME["accent"], CX_THEME["bg_card"]]), domain={'x': [0.15, 0.85], 'y': [0.15, 0.85]}))
    fig.update_layout(showlegend=False, height=250, template=get_cx_template())
    return fig

def chart_stacked_area(data_y):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=data_y, fill='tozeroy', fillcolor='rgba(0, 0, 0, 0.1)', line=dict(color=CX_THEME["primary"], width=3), mode='lines'))
    fig.update_layout(template=get_cx_template(), height=300)
    return fig

def chart_rounded_bar(x, y):
    fig = go.Figure(go.Bar(x=x, y=y, marker=dict(color=CX_THEME["primary"]), width=0.5))
    fig.update_layout(template=get_cx_template(), height=300)
    return fig

def chart_stepped(y):
    fig = go.Figure(go.Scatter(y=y, line_shape='hv', line=dict(color=CX_THEME["primary"], width=3)))
    fig.update_layout(template=get_cx_template(), height=300)
    return fig

def chart_radial_gauge(val):
    fig = go.Figure(go.Indicator(mode="gauge+number", value=val, 
                                 gauge={'bar': {'color': CX_THEME["primary"]}, 
                                        'axis': {'range': [0, 100]},
                                        'bgcolor': "white",
                                        'bordercolor': "black"}))
    fig.update_layout(height=200, template=get_cx_template())
    return fig

def chart_dual_line(y1, y2):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=y1, name="Real", line=dict(color=CX_THEME["primary"], width=3)))
    fig.add_trace(go.Scatter(y=y2, name="Target", line=dict(color=CX_THEME["neutral"], dash='dot')))
    fig.update_layout(template=get_cx_template(), height=300)
    return fig

# [El resto de las funciones: get_massive_audit_data, KPI_MASTER_LOGIC, get_money_explanation permanecen igual]
@st.cache_data
def get_massive_audit_data():
    base = datetime(2026, 1, 1)
    return pd.DataFrame({
        'Fecha': [base + timedelta(hours=i) for i in range(1000)],
        'ID_TX': [f'GR-{10000+i}' for i in range(1000)],
        'Local': np.random.choice(["Unicenter", "Florida", "Abasto", "E-Comm", "Rosario", "Córdoba", "Mendoza", "Palermo"], 1000),
        'Monto_Neto': np.random.uniform(5000, 85000, 1000).round(2),
        'Costo_OP': np.random.uniform(2000, 30000, 1000).round(2),
        'Lead_Time_H': np.random.randint(12, 72, 1000),
        'Satisfaccion': np.random.randint(1, 100, 1000),
        'Estado': np.random.choice(["Validado", "Pendiente", "Error"], 1000, p=[0.85, 0.1, 0.05])
    })

KPI_MASTER_LOGIC = {
    "Comercial": {
        "Ventas vs Costos": {"money": f"${(MONEY_VALUATION['REVENUE_TARGET'] * 0.12):,.0f}", "relacion": "Eficiencia marginal del capital.", "formula": "Revenue - Costs", "impacto": "Alto"},
        "Market Share": {"money": "22%", "relacion": "Posicionamiento en Malls.", "formula": "Grimoldi / Total Sector", "impacto": "Estratégico"},
        "Ticket Promedio": {"money": "$92,450", "relacion": "Efectividad de up-selling.", "formula": "Total Revenue / N Transacciones", "impacto": "Medio"},
        "Tasa de Conversión": {"money": "8.2%", "relacion": "Eficiencia del embudo.", "formula": "(Tickets / Tráfico) * 100", "impacto": "Crítico"}
    },
    "Capital Humano": {
        "Productividad": {"money": "$45k/H", "relacion": "Retorno inversión capacitación.", "formula": "Venta / Horas Hombre", "impacto": "Operativo"},
        "Costo Laboral": {"money": "18%", "relacion": "Peso sobre margen bruto.", "formula": "Nómina / Venta Neta", "impacto": "Financiero"},
        "Ausentismo": {"money": "4.1%", "relacion": "Costo de oportunidad.", "formula": "Horas Perdidas / Plan", "impacto": "Bajo"},
        "Rotación": {"money": "12%", "relacion": "Pérdida de know-how.", "formula": "Bajas / Dotación", "impacto": "Cultura"}
    },
    "Logística": {
        "Stock vs Quiebre": {"money": "7.4%", "relacion": "Venta perdida por talles.", "formula": "No Satisfecha / Demanda", "impacto": "Crítico"},
        "Lead Time": {"money": "3.5 D", "relacion": "Velocidad CD a Sucursal.", "formula": "Recepción - Pedido", "impacto": "Servicio"},
        "Flete sobre Venta": {"money": "4.5%", "relacion": "Erosión logística.", "formula": "Costo Flete / Venta", "impacto": "Margen"},
        "Rotación Inv": {"money": "2.8x", "relacion": "Salud del inventario.", "formula": "CMV / Inventario", "impacto": "Liquidez"}
    }
}

def get_money_explanation(kpi_name, value):
    base = MONEY_VALUATION['REVENUE_TARGET']
    impacto_cash = (value / 100) * base
    return f"Impacto de ${impacto_cash:,.2f} ARS en el balance actual."

# ==============================================================================
# 5. RENDER FUNCTIONS - MONOCHROME UI
# ==============================================================================
def render_home():
    inject_cx_industrial_design()
    st.markdown("<h1>SISTEMA DE ANÁLISIS (D.A.I.)</h1>", unsafe_allow_html=True)
    st.markdown("<p class='label-cx'>Consolidado Estratégico Grimoldi S.A. | Monochrome V3</p>", unsafe_allow_html=True)
    
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown(f'<div class="cx-card"><p class="label-cx">ROI OPERATIVO</p><h2>28.4%</h2><span class="money-badge">$355M</span><div class="pg-container"><div class="pg-bar" style="width:75%"></div></div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="cx-card"><p class="label-cx">MARGEN NETO</p><h2>14.8%</h2><span class="money-badge">$185M</span><div class="pg-container"><div class="pg-bar" style="width:45%"></div></div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="cx-card"><p class="label-cx">EBITDA M$</p><h2>18.2</h2><span class="money-badge">$227M</span><div class="pg-container"><div class="pg-bar" style="width:90%"></div></div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="cx-card"><p class="label-cx">STOCK HEALTH</p><h2>82.0%</h2><span class="money-badge">$1.02B</span><div class="pg-container"><div class="pg-bar" style="width:82%"></div></div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    c_left, c_right = st.columns([1, 2])
    with c_left:
        st.subheader("Unidades")
        if st.button("🛒 COMERCIAL", key="btn_comercial", use_container_width=True): st.session_state.view = 'Category'; st.session_state.category = 'Comercial'; st.rerun()
        if st.button("👥 CAPITAL HUMANO", key="btn_rrhh", use_container_width=True): st.session_state.view = 'Category'; st.session_state.category = 'Capital Humano'; st.rerun()
        if st.button("📦 LOGÍSTICA", key="btn_logistica", use_container_width=True): st.session_state.view = 'Category'; st.session_state.category = 'Logística'; st.rerun()
        st.plotly_chart(chart_stepped([10, 10, 25, 25, 40, 35]), use_container_width=True)
    with c_right:
        st.write("**Performance Histórica (Trend)**")
        st.plotly_chart(chart_stacked_area([120, 250, 200, 450, 380, 550, 600]), use_container_width=True)
        st.markdown(f'<div class="data-explanation"><strong>Nota:</strong> {get_money_explanation("Revenue", 15)}</div>', unsafe_allow_html=True)

def render_category():
    inject_cx_industrial_design()
    cat = st.session_state.category
    st.markdown(f"<h2>EXPLORACIÓN: {cat.upper()}</h2>", unsafe_allow_html=True)
    if st.button("↩ VOLVER AL PANEL"): st.session_state.view = 'Home'; st.rerun()
    
    kpis = list(KPI_MASTER_LOGIC[cat].keys())
    tabs = st.tabs(kpis + ["Auditoría"])
    for i, kpi in enumerate(kpis):
        with tabs[i]:
            intel = KPI_MASTER_LOGIC[cat][kpi]
            c1, c2 = st.columns([2, 1])
            with c1:
                if i == 0: st.plotly_chart(chart_dual_line([30, 45, 55, 40], [35, 40, 50, 55]), use_container_width=True, key=f"cat_dual_{cat}_{i}")
                elif i == 1: st.plotly_chart(chart_multi_donut(65, 45), use_container_width=True, key=f"cat_donut_{cat}_{i}")
                elif i == 2: st.plotly_chart(chart_rounded_bar(["A", "B", "C", "D"], [80, 45, 90, 60]), use_container_width=True, key=f"cat_bar_{cat}_{i}")
                else: st.plotly_chart(chart_radial_gauge(78), use_container_width=True, key=f"cat_gauge_{cat}_{i}")
                
                st.markdown(f"""
                <div class="data-explanation">
                    <strong>DATOS: {kpi.upper()}</strong><br>
                    <b>Impacto:</b> {intel["money"]} | <b>Lógica:</b> {intel["formula"]}
                </div>
                """, unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="cx-card"><p class="label-cx">ESTADO</p><h2>{intel["money"]}</h2><hr><p class="label-cx">IMPACTO</p><p>{intel["impacto"]}</p></div>', unsafe_allow_html=True)

def main():
    if st.session_state.view == 'Home': render_home()
    elif st.session_state.view == 'Category': render_category()
    elif st.session_state.view == 'Specialized': st.write("Módulo en construcción")

if __name__ == "__main__":
    main()