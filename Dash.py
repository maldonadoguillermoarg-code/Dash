import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ==============================================================================
# 1. CX BRAND IDENTITY & GLOBAL CONFIG
# ==============================================================================
st.set_page_config(
    page_title="GRIMOLDI CX | Intelligence System v3.0", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

CX_THEME = {
    "bg_card": "#E2EBEE",
    "primary": "#086890",
    "accent": "#CE516F",
    "neutral": "#8A8F90",
    "cyan": "#57C5E4",
    "white": "#FFFFFF",
    "text": "#1A1F2B",
    "success": "#2D8A4E"
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
# 2. CUSTOM CSS ENGINE
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
            border-radius: 16px;
            border-left: 6px solid {CX_THEME["primary"]};
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }}
        .pg-container {{ background: #D1D9DB; border-radius: 20px; height: 12px; margin: 10px 0; overflow: hidden; }}
        .pg-bar {{ background: {CX_THEME["primary"]}; height: 100%; border-radius: 20px; transition: width 0.8s ease-in-out; }}
        h1, h2, h3 {{ color: {CX_THEME["primary"]}; font-weight: 800 !important; }}
        .label-cx {{ color: {CX_THEME["neutral"]}; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }}
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
        .money-badge {{
            background: {CX_THEME["primary"]};
            color: white;
            padding: 4px 12px;
            border-radius: 6px;
            font-weight: 800;
            display: inline-block;
            margin-bottom: 10px;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. COMPONENTES DE VISUALIZACIÓN
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

def chart_multi_donut(v1, v2):
    fig = go.Figure()
    fig.add_trace(go.Pie(values=[v1, 100-v1], hole=0.8, marker=dict(colors=[CX_THEME["primary"], "#D1D9DB"]), domain={'x': [0, 1], 'y': [0, 1]}))
    fig.add_trace(go.Pie(values=[v2, 100-v2], hole=0.6, marker=dict(colors=[CX_THEME["accent"], "#E2EBEE"]), domain={'x': [0.15, 0.85], 'y': [0.15, 0.85]}))
    fig.update_layout(showlegend=False, height=250, template=get_cx_template())
    return fig

def chart_stacked_area(data_y):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=data_y, fill='tozeroy', fillcolor='rgba(87, 197, 228, 0.2)', line=dict(color=CX_THEME["cyan"], width=4), mode='lines'))
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
    fig = go.Figure(go.Indicator(mode="gauge+number", value=val, gauge={'bar': {'color': CX_THEME["primary"]}, 'axis': {'range': [0, 100]}}))
    fig.update_layout(height=200, template=get_cx_template())
    return fig

def chart_dual_line(y1, y2):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=y1, name="Real", line=dict(color=CX_THEME["primary"], width=4)))
    fig.add_trace(go.Scatter(y=y2, name="Target", line=dict(color=CX_THEME["neutral"], dash='dot')))
    fig.update_layout(template=get_cx_template(), height=300)
    return fig

# ==============================================================================
# 4. MASTER DATA ENGINE
# ==============================================================================
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
        "Ventas vs Costos": {
            "money": f"${(MONEY_VALUATION['REVENUE_TARGET'] * 0.12):,.0f}",
            "relacion": "Eficiencia marginal del capital. Afecta directamente al flujo libre de caja.",
            "formula": "Revenue - (COGS + SG&A)", "impacto": "Alto"
        },
        "Market Share": {
            "money": f"${(MONEY_VALUATION['MARKET_CAP_EST'] * 0.22):,.0f}",
            "relacion": "Posicionamiento relativo vs competencia directa en Malls.",
            "formula": "Ventas Grimoldi / Ventas Totales Sector", "impacto": "Estratégico"
        },
        "Ticket Promedio": {
            "money": "$92,450",
            "relacion": "Poder de compra y efectividad de up-selling en puntos de venta.",
            "formula": "Total Revenue / N Transacciones", "impacto": "Medio"
        },
        "Tasa de Conversión": {
            "money": f"${(MONEY_VALUATION['REVENUE_TARGET'] * 0.08):,.0f}",
            "relacion": "Eficiencia del embudo de ventas físico y digital.",
            "formula": "(Tickets / Tráfico) * 100", "impacto": "Crítico"
        }
    },
    "Capital Humano": {
        "Productividad": {
            "money": "$45,000 / H-H",
            "relacion": "Retorno de la inversión en capacitación y protocolos CX.",
            "formula": "Venta Neta / Horas Hombre", "impacto": "Operativo"
        },
        "Costo Laboral": {
            "money": f"${(MONEY_VALUATION['REVENUE_TARGET'] * 0.18):,.0f}",
            "relacion": "Peso de la nómina sobre el margen operativo bruto.",
            "formula": "Nómina Total / Venta Neta", "impacto": "Financiero"
        },
        "Ausentismo": {
            "money": f"${(MONEY_VALUATION['OPEX_LIMIT'] * 0.04):,.0f}",
            "relacion": "Costo de oportunidad por puestos no cubiertos en horas pico.",
            "formula": "Horas Perdidas / Horas Plan", "impacto": "Bajo"
        },
        "Rotación": {
            "money": "$25,000,000 anual",
            "relacion": "Costo de reclutamiento y pérdida de conocimiento institucional.",
            "formula": "Bajas / Promedio Dotación", "impacto": "Cultura"
        }
    },
    "Logística": {
        "Stock vs Quiebre": {
            "money": f"${(MONEY_VALUATION['REVENUE_TARGET'] * 0.07):,.0f}",
            "relacion": "Venta perdida por falta de disponibilidad de talles críticos.",
            "formula": "Demanda No Satisfecha / Demanda Total", "impacto": "Crítico"
        },
        "Lead Time": {
            "money": "3.5 Días Promedio",
            "relacion": "Velocidad de reposición desde el CD a la red de sucursales.",
            "formula": "Fecha Recepción - Fecha Pedido", "impacto": "Servicio"
        },
        "Flete sobre Venta": {
            "money": f"${(MONEY_VALUATION['REVENUE_TARGET'] * 0.045):,.0f}",
            "relacion": "Erosión logística del margen por canal (E-Comm vs Retail).",
            "formula": "Costo Transporte / Venta Neta", "impacto": "Margen"
        },
        "Rotación Inv": {
            "money": "2.8x Anual",
            "relacion": "Salud del inventario y frescura de la colección en salón.",
            "formula": "CMV / Inventario Promedio", "impacto": "Liquidez"
        }
    }
}

def get_money_explanation(kpi_name, value):
    base = MONEY_VALUATION['REVENUE_TARGET']
    impacto_cash = (value / 100) * base
    return f"El {value}% en {kpi_name} representa un impacto de ${impacto_cash:,.2f} ARS en el balance actual."

# ==============================================================================
# 5. RENDER FUNCTIONS (HOME & CATEGORY PRESERVADOS)
# ==============================================================================
def render_home():
    inject_cx_industrial_design()
    st.markdown("<h1>SISTEMA DE ANÁLISIS INTEGRAL (D.A.I.)</h1>", unsafe_allow_html=True)
    st.markdown("<p class='label-cx'>Consolidado Estratégico Grimoldi S.A. | Inteligencia Q1 2026</p>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown(f'<div class="cx-card"><p class="label-cx">ROI OPERATIVO</p><h2>28.4%</h2><span class="money-badge">$355,000,000</span><div class="pg-container"><div class="pg-bar" style="width:75%"></div></div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="cx-card"><p class="label-cx">MARGEN NETO</p><h2>14.8%</h2><span class="money-badge">$185,000,000</span><div class="pg-container"><div class="pg-bar" style="width:45%"></div></div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="cx-card"><p class="label-cx">EBITDA M$</p><h2>18.2</h2><span class="money-badge">$227,500,000</span><div class="pg-container"><div class="pg-bar" style="width:90%"></div></div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="cx-card"><p class="label-cx">STOCK HEALTH</p><h2>82.0%</h2><span class="money-badge">$1,025,000,000</span><div class="pg-container"><div class="pg-bar" style="width:82%"></div></div></div>', unsafe_allow_html=True)
    st.markdown("---")
    c_left, c_right = st.columns([1, 2])
    with c_left:
        st.subheader("Unidades Estratégicas")
        if st.button("🛒 ÁREA COMERCIAL", key="btn_comercial", use_container_width=True): st.session_state.view = 'Category'; st.session_state.category = 'Comercial'; st.rerun()
        if st.button("👥 CAPITAL HUMANO", key="btn_rrhh", use_container_width=True): st.session_state.view = 'Category'; st.session_state.category = 'Capital Humano'; st.rerun()
        if st.button("📦 EFICIENCIA LOGÍSTICA", key="btn_logistica", use_container_width=True): st.session_state.view = 'Category'; st.session_state.category = 'Logística'; st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📊 UNIDADES ESPECIALIZADAS (100 TABLAS)", key="btn_specialized", use_container_width=True): st.session_state.view = 'Specialized'; st.rerun()
        st.write("**Monitor de Cambio de Estado (Stepped)**")
        st.plotly_chart(chart_stepped([10, 10, 25, 25, 40, 35]), use_container_width=True)
    with c_right:
        st.write("**Performance Histórica (Stacked Area CX)**")
        st.plotly_chart(chart_stacked_area([120, 250, 200, 450, 380, 550, 600]), use_container_width=True)
        st.markdown(f'<div class="data-explanation"><strong>Análisis:</strong> {get_money_explanation("Revenue Anual", 15)}</div>', unsafe_allow_html=True)

def render_category():
    inject_cx_industrial_design()
    cat = st.session_state.category
    st.markdown(f"<h2>EXPLORACIÓN: {cat.upper()}</h2>", unsafe_allow_html=True)
    if st.button("↩ VOLVER AL PANEL GLOBAL"): st.session_state.view = 'Home'; st.rerun()
    kpis = list(KPI_MASTER_LOGIC[cat].keys())
    tabs = st.tabs(kpis + ["Auditoría Maestra", "Relaciones Financieras"])
    for i, kpi in enumerate(kpis):
        with tabs[i]:
            intel = KPI_MASTER_LOGIC[cat][kpi]
            c1, c2 = st.columns([2, 1])
            with c1:
                if i == 0: st.plotly_chart(chart_dual_line([30, 45, 55, 40], [35, 40, 50, 55]), use_container_width=True)
                elif i == 1: st.plotly_chart(chart_multi_donut(65, 45), use_container_width=True)
                elif i == 2: st.plotly_chart(chart_rounded_bar(["A", "B", "C", "D"], [80, 45, 90, 60]), use_container_width=True)
                else: st.plotly_chart(chart_radial_gauge(78), use_container_width=True)
            with c2: st.markdown(f'<div class="cx-card"><p class="label-cx">IMPACTO ECONÓMICO</p><h2 style="color:{CX_THEME["accent"]}">{intel["money"]}</h2><hr><p><strong>Relación:</strong> {intel["relacion"]}</p></div>', unsafe_allow_html=True)
    with tabs[4]:
        df = get_massive_audit_data()
        st.dataframe(df, height=500, use_container_width=True)

# ==============================================================================
# 8. ESPECIALIZADA (MODIFICADA SOLO PARA AUTO-COMPLETAR TABLAS)
# ==============================================================================
def render_specialized():
    inject_cx_industrial_design()
    st.markdown("<h2>MÓDULO DE UNIDADES ESPECIALIZADAS</h2>", unsafe_allow_html=True)
    if st.button("↩ VOLVER AL PANEL GLOBAL"): st.session_state.view = 'Home'; st.rerun()

    df_base = get_massive_audit_data()

    unidades = {
        "🛒 COMERCIAL Y VENTAS": ["Ranking de Facturación Bruta por Sucursal", "Tabla de Margen de Contribución por Local", "Matriz de Cumplimiento de Objetivos", "Desglose de Ticket Promedio por Región", "Tabla de Unidades por Ticket (UPT)", "Ranking de Venta por Metro Cuadrado", "Matriz de Medios de Pago", "Tabla de Descuentos Otorgados", "Análisis de Ventas por Franja Horaria", "Ranking de Best Sellers por Local", "Tabla de Slow Movers", "Matriz de Ventas Cruzadas", "Tabla de Devoluciones por Motivo", "Ranking de Clientes VIP", "Tabla de Nuevos Clientes vs. Recurrentes", "Matriz de Ventas por Género y Edad", "Tabla de Performance de Marcas Propias", "Ranking de Locales por Tasa de Conversión", "Tabla de Impacto de Promociones Bancarias", "Matriz de Ventas por Temporada"],
        "👥 CAPITAL HUMANO": ["Ranking de Productividad Individual", "Tabla de Costo Laboral sobre Venta", "Matriz de Ausentismo por Sucursal", "Tabla de Horas Extra por Nodo Logístico", "Ranking de Comisiones a Liquidar", "Tabla de Rotación Temprana", "Matriz de Capacitación CX", "Tabla de Incidencias Disciplinarias", "Ranking de Satisfacción del Cliente", "Tabla de Antigüedad vs. Performance", "Matriz de Costos de ART por Región", "Tabla de Gastos de Viáticos", "Ranking de Líderes de Tienda", "Tabla de Estructura de Dotación", "Matriz de Clima Organizacional", "Tabla de Productividad en Días Festivos", "Ranking de Cumplimiento de Horarios", "Tabla de Inversión en Uniformes", "Matriz de Beneficios vs. Retención", "Tabla de Evolución Salarial Real"],
        "📦 LOGÍSTICA": ["Matriz de Quiebre de Stock", "Ranking de Lead Time CD a Sucursal", "Tabla de Exactitud de Inventario (ERI)", "Matriz de Transferencias Inter-sucursales", "Tabla de Costo de Flete por Par", "Ranking de Proveedores", "Tabla de Calidad de Recepción", "Matriz de Ocupación de Depósito", "Tabla de Antigüedad de Stock", "Ranking de Velocidad de Picking", "Tabla de Siniestros en Transporte", "Matriz de Costo de Almacenamiento", "Tabla de Despacho de E-Commerce (SLA)", "Ranking de Devoluciones Logísticas", "Tabla de Eficiencia de Rutas", "Matriz de Reposición Automática", "Tabla de Gastos de Embalaje", "Ranking de Locales por Error de Inventario", "Tabla de Stock en Tránsito", "Matriz de Consumo Energético en CD"],
        "💰 FINANZAS": ["Matriz de EBITDA consolidado por Local", "Tabla de Gastos Fijos (OPEX)", "Ranking de Impuestos por Jurisdicción", "Tabla de Conciliación Bancaria", "Matriz de Costo Financiero por Tarjeta", "Tabla de Días de Cobro (DSO)", "Ranking de Cuentas por Pagar", "Tabla de Inversión en Marketing", "Matriz de Amortización de Bienes", "Tabla de Seguros y Pólizas", "Ranking de Gastos de Mantenimiento", "Tabla de Flujo de Caja Proyectado", "Matriz de Costo de Capital (WACC)", "Tabla de Margen Bruto por Línea", "Ranking de Sucursales por ROI", "Tabla de Auditoría de Compras Directas", "Matriz de Eficiencia Impositiva", "Tabla de Resultado Financiero (RECPAM)", "Ranking de Rentabilidad por M2 de Vidriera", "Tabla de Provisiones y Reservas"],
        "🌐 E-COMMERCE": ["Embudo de Conversión Web (Funnel)", "Tabla de Costo de Adquisición (CAC)", "Matriz de Tasa de Rebote", "Ranking de Productos buscados sin stock", "Tabla de Tiempo de Carga vs. Ventas", "Matriz de Canales de Origen", "Tabla de Abandono de Carrito", "Ranking de Cupones de Descuento", "Tabla de Ticket Promedio Online vs. Offline", "Matriz de Pick-up in Store", "Tabla de Reseñas y Calificaciones", "Ranking de Dispositivos de Compra", "Tabla de Ubicación de Compras Web", "Matriz de Publicidad en Redes", "Tabla de Tasa de Apertura de Newsletters", "Ranking de Influencers", "Tabla de Re-compras (Retención)", "Matriz de Errores en el Checkout", "Tabla de Costo de Logística Inversa", "Ranking de Cumplimiento de Promesa"]
    }

    tab_units = st.tabs(list(unidades.keys()))
    for idx, (nombre_unidad, tablas) in enumerate(unidades.items()):
        with tab_units[idx]:
            st.subheader(f"Data Master: {nombre_unidad}")
            cols = st.columns(2)
            for i, nombre_tabla in enumerate(tablas):
                with cols[i % 2]:
                    st.markdown(f"**{nombre_tabla}**")
                    
                    # LÓGICA DE AUTO-COMPLETADO BASADA EN DATOS REALES DE AUDITORÍA
                    if "Facturación" in nombre_tabla or "EBITDA" in nombre_tabla or "Margen" in nombre_tabla:
                        df_res = df_base.groupby('Local')['Monto_Neto'].sum().sort_values(ascending=False).reset_index()
                        df_res.columns = ['Local', 'Monto Total ($)']
                    elif "Lead Time" in nombre_tabla:
                        df_res = df_base.groupby('Local')['Lead_Time_H'].mean().reset_index()
                        df_res.columns = ['Local', 'Promedio Horas']
                    elif "Satisfacción" in nombre_tabla or "Performance" in nombre_tabla:
                        df_res = df_base.groupby('Local')['Satisfaccion'].mean().reset_index()
                        df_res.columns = ['Local', 'Score Promedio']
                    elif "Sucursal" in nombre_tabla or "Local" in nombre_tabla:
                        df_res = df_base.groupby('Local').size().reset_index(name='Transacciones')
                    else:
                        # Si no hay match, se mantiene tu "No info" original
                        df_res = pd.DataFrame({"Estado": ["No info"], "Valor": [0], "Detalle": ["Sin datos en base"]})
                    
                    st.dataframe(df_res, use_container_width=True, hide_index=True)
                    st.markdown("---")

def main():
    if st.session_state.view == 'Home': render_home()
    elif st.session_state.view == 'Category': render_category()
    elif st.session_state.view == 'Specialized': render_specialized()

if __name__ == "__main__":
    main()