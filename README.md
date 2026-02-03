# ALGORITMO DE SIMON CUÁNTICO MEJORADO - PAQUETE COMPLETO

>═══════════════════════════════════════════════════════════════════════════════
>ALGORITMO DE SIMON CUÁNTICO MEJORADO - PAQUETE COMPLETO                        
>Versión 2.3 - Febrero 2025                                                       
>═══════════════════════════════════════════════════════════════════════════════ 

![Quantum Badge](https://img.shields.io/badge/Quantum-Smopsys-black)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-olive)
![License](https://img.shields.io/badge/License-MIT-orange)
![Algorithm](https://img.shields.io/badge/Quantum-Algorithm-darkgrey)

📦 CONTENIDO DEL PAQUETE:

1. main.py
   - Punto de entrada central (CLI).
   - Accede a todas las funcionalidades: `run`, `viz`, `test`, `show`.

2. simons_complete.py
   - Implementación del sistema Metriplético H7.
   - 5 módulos principales:
     - Análisis de Simetría Dinámica (H7 + Fase de Berry + GOLDEN_PHASE)
     - Oráculo de Momento Metriplético (Conservación Hamiltoniana)
     - Algoritmo de Simon (Recuperación de período s=7)
     - Red Neuronal Cuántica (Entrelazamiento y fase)
     - Experimento integrado con salida tabular (Pandas)

3. simon_h7_holography.py
   - Generador de visualización holográfica unificada.
   - Proyecta estados en Bloch y crea patrones CGH.

4. simon_h7_interface.cs
   - Implementación de referencia en C# para AndroidHtmlUi.

5. tests/test_simons.py
   - Suite de pruebas Pytest para validación de H7 y Simon.

🚀 INICIO RÁPIDO:

Configurar entorno:

```bash
python3 -m venv env
./env/bin/pip install numpy pandas pytest plotly Pillow
```

Uso del CLI Central:

```bash
# Ejecutar el experimento completo
./env/bin/python main.py run

# Generar la visualización holográfica
./env/bin/python main.py viz

# Ejecutar tests de validación
./env/bin/python main.py test

# Ver referencia C#
./env/bin/python main.py show
```

## 🔬 COMPARATIVA: QISKIT VS PSIMON

La siguiente tabla contrasta el enfoque estándar de computación cuántica (Qiskit) con nuestro paradigma metriplético (Psimon):

| **Concepto**        | **Qiskit (qc)**                          | **psimon (ps)**                                    |
|---------------------|------------------------------------------|----------------------------------------------------|
| **Core Object**     | `QuantumCircuit`                         | `MetriplecticFlow`                                 |
| **Base de Operación** | Gates (H, CNOT, etc.)                  | `HamiltonianDynamics` ($H_{symp} + S_{metr}$)      |
| **Optimización**    | Transpiler / VQE                         | `BerryPhaseTuning` (Anclaje a $\pi$)               |
| **Resultado**       | Probabilistic Histogram                  | `DeterministicSecret` (100% Confianza)             |
| **Métrica**         | Fidelity / Error Rate                    | `LaminarFlowEntropy` (Meta: 0.0000)                |

### Explicación de Diferencias Clave:

**1. Core Object:**
- **Qiskit** trabaja con circuitos cuánticos discretos compuestos por puertas lógicas
- **Psimon** modela el flujo continuo bajo dinámica Hamiltoniana metriplética

**2. Base de Operación:**
- **Qiskit** usa transformaciones unitarias discretas (H, CNOT, Rz, etc.)
- **Psimon** evoluciona según $H = H_{symp} + S_{metr}$ donde:
  - $H_{symp}$: Término conservativo (simpléctico)
  - $S_{metr}$: Término disipativo (metriplético)

**3. Optimización:**
- **Qiskit** optimiza circuitos mediante transpilación y algoritmos variacionales (VQE)
- **Psimon** ajusta la Fase de Berry mediante GOLDEN_PHASE para anclaje a $\pi$

**4. Resultado:**
- **Qiskit** produce histogramas probabilísticos tras muchas mediciones
- **Psimon** recupera el secreto de forma determinística con 100% de confianza

**5. Métrica:**
- **Qiskit** mide fidelidad cuántica y tasas de error de puertas
- **Psimon** monitorea entropía de flujo laminar (meta: S = 0.0000 bits)

### Ejemplo de Código Comparativo:

```python
# QISKIT: Enfoque tradicional
from qiskit import QuantumCircuit, transpile
qc = QuantumCircuit(3, 3)
qc.h([0, 1, 2])
qc.measure([0, 1, 2], [0, 1, 2])
job = backend.run(transpile(qc, backend), shots=1024)
histogram = job.result().get_counts()  # Probabilístico

# PSIMON: Enfoque metriplético
import psimon as ps
flow = ps.MetriplecticFlow(n_qubits=3, s=7)
flow.apply_hamiltonian_dynamics()
secret = flow.recover_deterministic_secret()  # Determinístico
entropy = flow.measure_laminar_entropy()      # S ≈ 0.0000
```

✨ RECOMENDACIONES Y CARACTERÍSTICAS PRINCIPALES:
```bash
__________________________________________________________________________________________________
||      Librería       | Alias Sugerido |                    Contexto                           ||
══════════════════════════════════════════════════════════════════════════════════════════════════
||      psimon         |      ps        | "Operaciones de oráculo, Hamiltoniano y estados."     ||
||   psimon.holography |      psh       | "Generación de patrones CGH y visualización fractal." ||
|| psimon.metriplectic |      psm       | "Dinámica de energía y entropía (E_Metriplética)."    ||
══════════════════════════════════════════════════════════════════════════════════════════════════
  ==============================================================================================
```
    ✓ MANDATO METRIPLÉTICO: Competencia entre términos conservativos y disipativos ($H = H_{symp} + S_{metr}$).

    ✓ CONSERVACIÓN H7: Los estados complementarios siempre suman 7 ($s=111$).

    ✓ FASE DE BERRY: Cálculo geométrico con corrección $GOLDEN\_PHASE \approx 0.3674$.

    ✓ ESTADOS 2-1: Distinción de estados de salida según el momento (1,0) vs (0,1).

    ✓ SALIDA TABULAR: Reporte detallado de métricas físicas y cuánticas.


🔬 VALIDACIÓN SEGÚN TRES NIVELES DE CORRESPONDENCIA:

>NIVEL 1 (Isomorfismo Matemático):
  
  ✓ Ecuación de Simon: f(x ⊕ 7) = f(x)
  
  ✓ Período s=7: Coincide con el complemento aritmético en 3 bits.

>NIVEL 2 (Isomorfismo Dimensional):
  
  ✓ Momento p: ℝ → [0, 7]
  
  ✓ Energía Metriplética: [0, 1] (Normalizada)

>NIVEL 3 (Isomorfismo Físico):
  
  ✓ Conservación de H: El par entrelazado $(n, 7-n)$ tiene energías simétricas.

  ✓ Fase de Berry: Refleja la topología del ciclo de Hilbert.

📊 SALIDA TÍPICA:

```text
(base) user@user-bash:~/simons$ /home/user/simons/env/bin/python /home/user/simons/simons_complete.py

████████████████████████████████████████████████████████████████████████████████
  SIMON MEJORADO: MOMENTO, FASE DE BERRY Y CONSERVACIÓN H7
████████████████████████████████████████████████████████████████████████████████

[ESTADOS DE MOMENTO ENTRELAZADOS (TABLA H7)]
 n  Momento  Complemento H7 Estado 2-1  E_Metriplética  Fase Berry (rad) Binario |x⟩
 1        1               6     (1, 0)          0.4783            1.2650         001
 2        2               5     (1, 0)          0.4609            2.1626         010
 3        3               4     (1, 0)          0.4513            3.0602         011
 4        4               3     (0, 1)          0.4513            3.2230         100
 5        5               2     (0, 1)          0.4609            4.1206         101
 6        6               1     (0, 1)          0.4783            5.0182         110

[RESULTADO SIMON]
Período Real: 7 (111) | Estimado: 7 (111)
Éxito: ✓ | Confianza: 100.00%

[MÉTRICAS FINALES]
Fase de Berry Promedio: 3.1416 rad
Entropía de Entrelazamiento: -0.0000 bits
```

⚙️ REQUISITOS:

- Python 3.12+ (Recomendado)
- numpy
- pandas
- pytest (para validación)

📚 DOCUMENTACIÓN:

- walkthrough.md: Resumen técnico de la implementación H7.
- simon_h7_interface.cs: Referencia de lógica C#.
- ESPECIFICACIONES_TECNICAS_H7.md: Mapeo completo Python ↔ C#

═══════════════════════════════════════════════════════════════════════════════

Versión: 2.3
Fecha: Febrero 2, 2025
Autor: jakobmina Jacobo Tlacaelel Mina Rodriguez Smpsys QuoreMind
Licencia: MIT

═══════════════════════════════════════════════════════════════════════════════
