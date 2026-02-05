import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from simon_h7.core.metriplectic import MetriplecticH7System
from simon_h7.analysis.topology import VietorisRipsAnalysis
from simon_h7.core.algorithm import AnalizadorSimetriaDinamica

# Configuración de la página Premium
st.set_page_config(
    page_title="Simon H7: Metriplectic Holography",
page_icon="🔆",
    layout="wide",
)

# Estilo Personalizado (Glassmorphism & Dark Mode)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1c24 100%);
    }
    h1 {
        color: #00d4ff;
        font-family: 'Outfit', sans-serif;
        text-align: center;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔆 SIMON H7: HOLOGRAFÍA METRIPLÉCTICA")
st.markdown("---")

# Sidebar - Controles
with st.sidebar:
    st.header("🎛 Configuración Dinámica")
    steps = st.slider("Pasos de Simulación (n)", 100, 5000, 1000)
    delta = st.slider("Parámetro Delta (Estabilidad)", 0.0, 1.0, 0.1)
    phi_custom = st.number_input("Razón Áurea (φ)", value=1.61803398875, format="%.10f")
    
    st.markdown("---")
    st.header("🕸 Topología (Vietoris-Rips)")
    epsilon = st.slider("Radio Epsilon (ε)", 0.05, 1.0, 0.3)
    
    st.markdown("---")
    st.info("Regla 1.3: No se permiten sistemas puramente conservativos ni puramente disipativos.")

# Instanciar y Simular
system = MetriplecticH7System(phi_golden=phi_custom, delta=delta)
data = system.evolve_state(n_steps=steps)

# Layout de Dashboard
col1, col2 = st.columns([1, 1])

with col1:
    # 1. Diagnóstico Metriplético: Competencia entre L_symp y L_metr
    st.subheader("📊 Diagnóstico Metriplético (Regla 3.3)")
    fig_diag = go.Figure()
    fig_diag.add_trace(go.Scatter(x=data['n'], y=data['H_term'], name="Simpléctico (H)", line=dict(color='#00d4ff', width=2)))
    fig_diag.add_trace(go.Scatter(x=data['n'], y=data['S_term'], name="Métrico (S)", line=dict(color='#ff4b4b', width=2, dash='dash')))
    fig_diag.update_layout(
        template="plotly_dark",
        margin=dict(l=20, r=20, t=30, b=20),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_diag, use_container_width=True)

    # 2. Esfera de Bloch
    st.subheader("🌐 Trayectoria en Esfera de Bloch")
    fig_bloch = go.Figure()
    # Esfera base
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:15j]
    x_s = np.cos(u)*np.sin(v)
    y_s = np.sin(u)*np.sin(v)
    z_s = np.cos(v)
    fig_bloch.add_trace(go.Surface(x=x_s, y=y_s, z=z_s, opacity=0.1, showscale=False, hoverinfo='skip'))
    # Trayectoria
    fig_bloch.add_trace(go.Scatter3d(
        x=data['x_bloch'], y=data['y_bloch'], z=data['z_bloch'],
        mode='lines',
        line=dict(color='cyan', width=4),
        name='Evolución H7'
    ))
    fig_bloch.update_layout(template="plotly_dark", height=500, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_bloch, use_container_width=True)

with col2:
    # 3. Holograma Cuántico (CGH)
    st.subheader("🌀 Holograma Cuántico (CGH 3D)")
    # Simulamos la proyección CGH basada en rho
    res = 50
    X, Y = np.meshgrid(np.linspace(-2, 2, res), np.linspace(-2, 2, res))
    rho_cgh = np.sqrt(X**2 + Y**2)
    # Modulación por el operador áureo proyectado
    Z = np.sin(rho_cgh * phi_custom) * np.cos(rho_cgh * np.pi) * data['O_n'].mean()
    
    fig_cgh = go.Figure(data=[go.Surface(z=Z, colorscale='Viridis')])
    fig_cgh.update_layout(template="plotly_dark", height=450, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_cgh, use_container_width=True)

    # 4. Métricas de Lagrangiano
    st.subheader("📐 Invariantes del Sistema")
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric("Lagrangiano Simpléctico ($L_{symp}$)", f"{data['L_symp']:.4f}")
    with m_col2:
        st.metric("Lagrangiano Métrico ($L_{metr}$)", f"{data['L_metr']:.4f}")
    
    st.metric("📏 Coherence (Euclidean)", f"{data['dist_coherence']:.6f}", delta=f"{delta:.2f} Δ", delta_color="inverse")
    st.metric("🧬 Statistical Depth (Mahalanobis)", f"{data['dist_mahalanobis']:.4f}", help="Métricas de dispersión y correlación de la trayectoria")
    
    st.markdown("""
    <div class="metric-card">
        <b>Ecuación de Evolución:</b><br>
        <i>dψ = {ψ, H}dt + [ψ, S]dt</i><br><br>
        La fase es gobernada por la simetría Hamiltoniana, mientras que la amplitud 
        relaja hacia el atractor áureo definido por el potencial de disipación.
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# NUEVA SECCIÓN: PROCESO TRIPARTITO (2da CUANTIZACIÓN)
# ---------------------------------------------------------
st.markdown("---")
st.header("🧬 PROCESO TRIPARTITO: 2da CUANTIZACIÓN")

from simon_h7.simulation.tripartite import TripartiteMetriplecticSystem

# Ejecutar simulación tripartita
tri_sys = TripartiteMetriplecticSystem(input_val=int(steps % 255)) # Usamos steps como semilla
tri_data = tri_sys.run_tripartite_task()

t_col1, t_col2, t_col3 = st.columns(3)

with t_col1:
    st.markdown("#### Hilo A: Partícula")
    st.write(f"**Output A:** `{tri_data.output_a}`")
    st.progress(1.0 if tri_data.output_a > 0 else 0.0)
    st.caption("Evolución Simpléctica Unitaria")

with t_col2:
    st.markdown("#### Hilo B: Espejo")
    st.write(f"**Output B:** `{tri_data.output_b}`")
    st.progress(1.0 if tri_data.output_b > 0 else 0.0)
    st.caption("Simetría Topológica XOR-Simon")

with t_col3:
    st.markdown("#### Hilo C: Coherencia")
    status = "✅ ESTABLE" if tri_data.is_stable else "❌ DECOHERENCIA"
    st.write(f"**Estado:** {status}")
    st.write(f"**Fase de Berry:** `{tri_data.berry_phase:.6f}`")
    st.caption("Segunda Cuantización / Operador Métrico")

# Graficar Historia de la Coherencia (Simulada para visualización)
st.subheader("🔄 Convergencia del Atractor Métrico")
n_tri = np.arange(len(tri_data.rho)) if len(tri_data.rho) > 0 else np.arange(100)
fig_tri = go.Figure()
fig_tri.add_trace(go.Scatter(
    x=n_tri, 
    y=tri_data.v if len(tri_data.v) > 0 else np.zeros(100), 
    name="Flujo de Información (v)",
    line=dict(color='#00ff41', width=1)
))
fig_tri.update_layout(template="plotly_dark", height=300, margin=dict(l=20, r=20, t=10, b=20))
st.plotly_chart(fig_tri, use_container_width=True)

# ---------------------------------------------------------
# NUEVA SECCIÓN: TOPOLOGÍA DE VIETORIS-RIPS
# ---------------------------------------------------------
st.markdown("---")
st.header("🕸 TOPOLOGÍA DEL ESPACIO DE ESTADOS (VIETORIS-RIPS)")

# Extraer puntos de la esfera de Bloch (muestreo para no saturar el grafo)
indices = np.linspace(0, steps-1, min(steps, 100), dtype=int)
bloch_points = np.vstack([data['x_bloch'][indices], data['y_bloch'][indices], data['z_bloch'][indices]]).T

# Analizar topología
vr = VietorisRipsAnalysis(epsilon=epsilon)
adj = vr.compute_proximity_graph(bloch_points)
edges = vr.get_edges(adj)

# Obtener quiralidad para colorear nodos
analizador = AnalizadorSimetriaDinamica()
quiralidades = [analizador.calcular_quiralidad(analizador.calcular_paridad(i), analizador.calcular_quasiperiodo(i, phi_custom)) for i in indices]

# Graficar Grafo de Proximidad 3D
fig_vr = go.Figure()

# Dibujar aristas
for i, j in edges:
    fig_vr.add_trace(go.Scatter3d(
        x=[bloch_points[i, 0], bloch_points[j, 0]],
        y=[bloch_points[i, 1], bloch_points[j, 1]],
        z=[bloch_points[i, 2], bloch_points[j, 2]],
        mode='lines',
        line=dict(color='rgba(255,255,255,0.2)', width=1),
        hoverinfo='skip',
        showlegend=False
    ))

# Dibujar nodos
fig_vr.add_trace(go.Scatter3d(
    x=bloch_points[:, 0],
    y=bloch_points[:, 1],
    z=bloch_points[:, 2],
    mode='markers',
    marker=dict(
        size=6,
        color=quiralidades,
        colorscale='Hot',
        opacity=0.8,
        colorbar=dict(title="Quiralidad", thickness=15, len=0.5)
    ),
    text=[f"Paso {i}" for i in indices],
    name="Vértices (Estados)"
))

fig_vr.update_layout(
    template="plotly_dark",
    height=600,
    scene=dict(
        xaxis=dict(title='X Bloch'),
        yaxis=dict(title='Y Bloch'),
        zaxis=dict(title='Z Bloch'),
        aspectmode='cube'
    ),
    margin=dict(l=0, r=0, t=30, b=0)
)
st.plotly_chart(fig_vr, use_container_width=True)
st.caption(f"Grafo de proximidad con ε={epsilon}. Los nodos se conectan si su distancia en la esfera de Bloch es menor que el radio. Coloreados por Quiralidad (Regla 1.1).")

# Footer
st.markdown("---")
st.markdown("Developed with Metriplectic Rigor by Antigravity AI")
