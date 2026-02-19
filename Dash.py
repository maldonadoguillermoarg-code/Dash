import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ==============================================================================
# 1. CONSTANTES DE IDENTIDAD DE MARCA (CX THEME)
# ==============================================================================
CX_THEME = {
    "bg_card": "#E2EBEE",
    "primary": "#086890",
    "accent": "#CE516F",
    "neutral": "#8A8F90",
    "cyan": "#57C5E4",
    "text": "#1A1F2B",
    "white": "#FFFFFF"
}

# Template Global de Plotly (Senior Spec)
CX_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Inter, sans-serif", color=CX_THEME["text"]),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=False, zeroline=False, color=CX_THEME["neutral"]),
        yaxis=dict(showgrid=True, gridcolor="#D1D9DB", zeroline=False, color=CX_THEME["neutral"]),
        hoverlabel=dict(bgcolor=CX_THEME["white"], font_size=12, font_family="Inter")
    )
)

# ==============================================================================
# 2. MOTOR DE RENDERIZADO VISUAL (COMPONETIZACIÓN)
# ==============================================================================

def inject_cx_styles():
    st.markdown(f"""
        <style>
        @import url('https://rsms.me/inter/inter.css');
        html, body, [class*="css"] {{ font-family: 'Inter', sans-serif !important; background-color: {CX_THEME["white"]}; }}
        .stApp {{ background-color: {CX_THEME["white"]}; }}
        
        /* Metric Cards CX */
        .metric-cx {{
            background-color: {CX_THEME["bg_card"]};
            border-radius: 12px;
            padding: 25px;
            border-bottom: 4px solid {CX_THEME["primary"]};
        }}
        
        /* Progress Indicator */
        .progress-bg {{ background: #D1D9DB; border-radius: 10px; height: 10px; width: 100%; }}
        .progress-fill {{ background: {CX_THEME["primary"]}; border-radius: 10px; height: 10px; }}
        
        .stButton>button {{
            background-color: {CX_THEME["primary"]} !important; color: white !important;
            border: none !important; border-radius: 8px !important; padding: 12px !important;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- FÁBRICA DE GRÁFICOS CX ---

def chart_multi_donut():
    fig = go.Figure()
    fig.add_trace(go.Pie(values=[40, 60], hole=0.8, marker=dict(colors=[CX_THEME["primary"], CX_THEME["bg_card"]]), domain={'x': [0, 1], 'y': [0, 1]}))
    fig.add_trace(go.Pie(values=[25, 75], hole=0.6, marker=dict(colors=[CX_THEME["accent"], CX_THEME["bg_card"]]), domain={'x': [0.1, 0.9], 'y': [0.1, 0.9]}))
    fig.update_layout(showlegend=False, template=CX_TEMPLATE, height=300)
    return fig

def chart_stacked_area():
    x = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=[20, 35, 30, 45, 40, 55], fill='tozeroy', 
                             fillcolor='rgba(87, 197, 228, 0.2)', line=dict(color=CX_THEME["cyan"], width=3)))
    fig.update_layout(template=CX_TEMPLATE, height=300)
    return fig

def chart_rounded_bar():
    fig = go.Figure(go.Bar(x=['T1', 'T2', 'T3', 'T4'], y=[450, 600, 550, 700], 
                           marker=dict(color=CX_THEME["primary"]), width=0.5))
    fig.update_layout(template=CX_TEMPLATE, height=300)
    return fig

def chart_stepped():
    fig = go.Figure(go.Scatter(x=[1, 2, 3, 4, 5], y=[10, 15, 15, 25, 20], line_shape='hv', 
                               line=dict(color=CX_THEME["accent"], width=3)))
    fig.update_layout(template=CX_TEMPLATE, height=300)
    return fig

def chart_dual_line():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(10)), y=np.random.randint(10,20,10), mode='lines+markers', name='Real', line=dict(color=CX_THEME["primary"])))
    fig.add_trace(go.Scatter(x=list(range(10)), y=np.random.randint(10,20,10), mode='lines', name='Target', line=dict(color=CX_THEME["neutral"], dash='dot')))
    fig.update_layout(template=CX_TEMPLATE, height=300)
    return fig

def chart_gauge(value):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = value,
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': CX_THEME["primary"]}},
        title = {'text': "Eficiencia %", 'font': {'size': 14}}
    ))
    fig.update_layout(template=CX_TEMPLATE, height=250)
    return fig

# ==============================================================================
# 3. ORQUESTACIÓN DE VISTAS
# ==============================================================================

def render_cx_home():
    st.markdown(f"<h1 style='color:{CX_THEME["primary"]}; font-weight:800;'>Executive Reporting CX</h1>", unsafe_allow_html=True)
    
    # KPIs con Progress Indicators (Req 3.5)
    cols = st.columns(4)
    metrics = [("Ventas", 85), ("Margen", 62), ("Stock", 40), ("RRHH", 90)]
    for i, (label, val) in enumerate(metrics):
        with cols[i]:
            st.markdown(f"""
                <div class="metric-cx">
                    <p style="color:{CX_THEME["neutral"]}; margin:0;">{label}</p>
                    <h2 style="margin:0;">{val}%</h2>
                    <div class="progress-bg"><div class="progress-fill" style="width:{val}%"></div></div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Galería de Componentes CX Solicitados
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Multi-Donut Concentric (Market Share)")
        st.plotly_chart(chart_multi_donut(), use_container_width=True)
        
        st.subheader("Stacked Area (Tendencia)")
        st.plotly_chart(chart_stacked_area(), use_container_width=True)

    with col_right:
        st.subheader("Ascending Bar Series (Desempeño)")
        fig_asc = px.bar(x=['A', 'B', 'C', 'D'], y=[10, 25, 45, 80], text_auto=True)
        fig_asc.update_traces(marker_color=CX_THEME["primary"])
        fig_asc.update_layout(template=CX_TEMPLATE, height=300)
        st.plotly_chart(fig_asc, use_container_width=True)
        
        st.subheader("Dual-Line Graph with Markers")
        st.plotly_chart(chart_dual_line(), use_container_width=True)

def render_deep_dive():
    cat = st.session_state.category
    st.markdown(f"<h2 style='color:{CX_THEME["primary"]}'>{cat} | Deep Dive</h2>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Métricas de Cambio de Estado (Stepped)**")
        st.plotly_chart(chart_stepped(), use_container_width=True)
    with c2:
        st.write("**Indicador Gauge de KPI**")
        st.plotly_chart(chart_gauge(78), use_container_width=True)
    
    if st.button("↩ Volver"):
        st.session_state.view = 'Home'
        st.rerun()

def main():
    inject_cx_styles()
    if 'view' not in st.session_state: st.session_state.view = 'Home'
    
    if st.session_state.view == 'Home':
        render_cx_home()
        if st.button("IR A DETALLE COMERCIAL"):
            st.session_state.view = 'Detail'
            st.session_state.category = 'Comercial'
            st.rerun()
    else:
        render_deep_dive()

if __name__ == "__main__":
    main()