import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from PIL import Image
import math
import os

# Importar lógica H7 del proyecto
from simons_complete import AnalizadorSimetriaDinamica, MetriplecticMomentumOracle

def run_holography():
    # ======================
    # PARÁMETROS CUASI-PERIÓDICOS (CONTEXTO H7)
    # ======================
    N = 1000
    phi = AnalizadorSimetriaDinamica.PHI
    alpha = 1 / phi
    l = 1.0
    PHI_QUAD = 0.05
    delta = 0.1
    GOLDEN_PHASE = AnalizadorSimetriaDinamica.GOLDEN_PHASE

    n = np.arange(N)
    # Ángulos cuasi-periódicos modulados por la dinámica áurea
    theta_n = 2 * np.pi * (n * alpha) % (2 * np.pi * alpha)

    # ======================
    # PROYECCIÓN HOLOGRÁFICA METRIPLÉCTICA
    # ======================
    # Usamos el oráculo para obtener el perfil de energía metriplética
    oracle = MetriplecticMomentumOracle(s=7, n_bits=3)
    # Simulamos la energía para los N puntos basada en su momento mod 7
    momentos_sim = n % 7
    energias = np.array([oracle.aplicar_metriplectica(int(m)) for m in momentos_sim])

    # Proyección holográfica: amplitud modulada por la energía metriplética
    cos_proj = np.cos(phi * n * l + PHI_QUAD * n**2) * energias
    phase_holo = -np.pi * (n + delta) * (1 + PHI_QUAD)
    amplitude_1 = np.exp(1j * phase_holo) * cos_proj

    # ======================
    # VECTOR DE ESTADO EN BLOCH (EVOLUCIÓN H7)
    # ======================
    psi_0 = cos_proj
    psi_1 = amplitude_1
    norm = np.sqrt(np.abs(psi_0)**2 + np.abs(psi_1)**2)
    psi_0 /= norm + 1e-15
    psi_1 /= norm + 1e-15

    # Coordenadas en esfera de Bloch
    x_bloch = 2 * np.real(psi_0 * np.conj(psi_1))
    y_bloch = 2 * np.imag(psi_0 * np.conj(psi_1))
    z_bloch = np.abs(psi_0)**2 - np.abs(psi_1)**2

    # ======================
    # PARÁMETROS CGH-SLM (ESTRUCTURA DE SIMETRÍA)
    # ======================
    SLM_SIZE = (1080, 1920)
    N_cgh = 51
    phi_cgh = 0.18
    n_cgh = np.arange(N_cgh)
    # Operador de simetría O_n para el holograma
    O_n = (-1)**n_cgh * np.cos(phi_cgh * n_cgh)

    res_y, res_x = SLM_SIZE
    x_cgh = np.linspace(-2, 2, res_x)
    y_cgh = np.linspace(-2, 2, res_y)
    X_cgh, Y_cgh = np.meshgrid(x_cgh, y_cgh)
    rho_cgh = np.sqrt(X_cgh**2 + Y_cgh**2)
    theta_cgh = np.arctan2(Y_cgh, X_cgh)

    m_idx = np.round((N_cgh * theta_cgh) / (2 * np.pi)) % N_cgh
    m_idx = m_idx.astype(int)

    amplitude_cgh = np.abs(O_n[m_idx])
    sign_phase_cgh = np.sign(O_n[m_idx])

    cgh_gray = 127 + 127 * sign_phase_cgh * amplitude_cgh
    cgh_gray = np.clip(cgh_gray, 0, 255).astype(np.uint8)
    mask_cgh = (rho_cgh <= 1.9)
    cgh_gray = cgh_gray * mask_cgh

    # ======================
    # CREAR FIGURA INTERACTIVA (Contexto H7)
    # ======================
    fig = make_subplots(
        rows=2, cols=2,
        specs=[
            [{"type": "scatterpolar"}, {"type": "scatter3d"}],
            [{"type": "surface"}, {"type": "scatter3d"}]
        ],
        subplot_titles=(
            "Ciclo de Fase de Berry - Cuasiperíodo H7",
            "Esfera de Bloch - Trayectoria Metriplética",
            "Holograma Cuántico (CGH) - Superficie 3D",
            "Espacio de Fases: Simon H7 vs Holografía"
        ),
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )

    # 1. Trayectoria Polar (Berry Phase)
    fig.add_trace(
        go.Scatterpolar(
            r=energias, # La energía define el radio efectivo
            theta=np.degrees(theta_n),
            mode='markers',
            marker=dict(size=4, color=n, colorscale='Turbo', showscale=True),
            name='Momentos H7'
        ),
        row=1, col=1
    )

    # 2. Esfera de Bloch
    # Alambres de la esfera
    u_sph, v_sph = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]
    x_sph = np.cos(u_sph)*np.sin(v_sph)
    y_sph = np.sin(u_sph)*np.sin(v_sph)
    z_sph = np.cos(v_sph)
    fig.add_trace(go.Surface(x=x_sph, y=y_sph, z=z_sph, opacity=0.1, showscale=False, hoverinfo='skip'), row=1, col=2)

    fig.add_trace(
        go.Scatter3d(
            x=x_bloch, y=y_bloch, z=z_bloch,
            mode='lines',
            line=dict(color='cyan', width=2),
            name='Evolución Cuántica'
        ),
        row=1, col=2
    )

    # Resaltar los 6 estados del dado H7
    n_h7 = np.arange(1, 7)
    momentos_h7 = n_h7 % 7
    # Mapear n_h7 a índices en el array N=1000 para visualización representativa
    # o simplemente calcular sus puntos específicos de Bloch
    x_h7, y_h7, z_h7 = [], [], []
    for val in n_h7:
        idx = int(val * (N/7)) # Distribución proporcional
        x_h7.append(x_bloch[idx])
        y_h7.append(y_bloch[idx])
        z_h7.append(z_bloch[idx])

    fig.add_trace(
        go.Scatter3d(
            x=x_h7, y=y_h7, z=z_h7,
            mode='markers+text',
            marker=dict(size=8, color='red', symbol='diamond'),
            text=[f"n={v}" for v in n_h7],
            name='Estados H7 (El Dado)'
        ),
        row=1, col=2
    )

    # 3. CGH Surface
    step = 10
    fig.add_trace(
        go.Surface(x=X_cgh[::step,::step], y=Y_cgh[::step,::step], z=cgh_gray[::step,::step], colorscale='Viridis', name='CGH'),
        row=2, col=1
    )

    # 4. Espacio de Fases Combinado
    fig.add_trace(
        go.Scatter3d(x=x_bloch[::5], y=y_bloch[::5], z=z_bloch[::5], mode='markers', marker=dict(size=2, color='cyan', opacity=0.5), name='Trayectoria Bloch'),
        row=2, col=2
    )
    fig.add_trace(
        go.Scatter3d(x=X_cgh[::20,::20].flatten()/2, y=Y_cgh[::20,::20].flatten()/2, z=(cgh_gray[::20,::20].flatten()-127)/127,
                     mode='markers', marker=dict(size=1, color='magenta', opacity=0.3), name='Estructura CGH'),
        row=2, col=2
    )

    # Layout
    fig.update_layout(
        title_text="<b>HOLOGRAFÍA CUÁNTICA METRIPLÉCTICA: SIMON H7</b><br>Perspectiva Unificada de Fase de Berry, Energía y Simetría Áurea",
        height=1000, width=1400, template="plotly_dark"
    )

    # Guardar y Mostrar
    fig.write_html("Simon_H7_Holografia_Interactiva.html")
    print("✓ Archivo generado: Simon_H7_Holografia_Interactiva.html")

    # Fractal Analysis
    def box_count(points, eps):
        grids = np.floor(points / eps).astype(int)
        return len(np.unique(grids, axis=0))

    epsilons = np.logspace(-2, -0.5, 10)
    pts = np.vstack((x_bloch, y_bloch, z_bloch)).T
    boxes = [box_count(pts, eps) for eps in epsilons]
    d_fractal = -np.polyfit(np.log(1/epsilons), np.log(boxes), 1)[0]
    print(f"ANÁLISIS FRACTAL: Dimensión efectiva d ≈ {d_fractal:.3f}")

    # Imagen CGH
    img = Image.fromarray(cgh_gray)
    img.save("Simon_H7_CGH_Pattern.png")
    print("✓ Imagen generada: Simon_H7_CGH_Pattern.png")

    # Info File
    with open("SIMON_H7_VIZ_REPORT.txt", "w", encoding="utf-8") as f:
        f.write(f"REPORTE DE VISUALIZACIÓN H7\n")
        f.write(f"===========================\n")
        f.write(f"Contexto: Algoritmo de Simon Mejorado (H7)\n")
        f.write(f"Dimensión Fractal Bloch: {d_fractal:.4f}\n")
        f.write(f"Constante Áurea PHI: {phi:.6f}\n")
        f.write(f"Fase de Berry (Golden Phase): {GOLDEN_PHASE:.6f} rad\n")
        f.write(f"Puntos Simulados: {N}\n")

if __name__ == '__main__':
    run_holography()
