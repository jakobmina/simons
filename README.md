# ALGORITMO DE SIMON CUÁNTICO MEJORADO - PAQUETE COMPLETO

 ═══════════════════════════════════════════════════════════════════════════════
║          ALGORITMO DE SIMON CUÁNTICO MEJORADO - PAQUETE COMPLETO            ║
║                    Versión 2.3 - Febrero 2025                               ║
╚═════════════════════════════════════════════════════════════════════════════╝

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

✨ CARACTERÍSTICAS PRINCIPALES:

✓ MANDATO METRIPLÉTICO: Competencia entre términos conservativos y disipativos ($H = H_{symp} + S_{metr}$).
✓ CONSERVACIÓN H7: Los estados complementarios siempre suman 7 ($s=111$).
✓ FASE DE BERRY: Cálculo geométrico con corrección $GOLDEN\_PHASE \approx 0.3674$.
✓ ESTADOS 2-1: Distinción de estados de salida según el momento (1,0) vs (0,1).
✓ SALIDA TABULAR: Reporte detallado de métricas físicas y cuánticas.

🔬 VALIDACIÓN SEGÚN TRES NIVELES DE CORRESPONDENCIA:

NIVEL 1 (Isomorfismo Matemático):
  ✓ Ecuación de Simon: f(x ⊕ 7) = f(x)
  ✓ Período s=7: Coincide con el complemento aritmético en 3 bits.

NIVEL 2 (Isomorfismo Dimensional):
  ✓ Momento p: ℝ → [0, 7]
  ✓ Energía Metriplética: [0, 1] (Normalizada)

NIVEL 3 (Isomorfismo Físico):
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

═══════════════════════════════════════════════════════════════════════════════

Versión: 2.3
Fecha: Febrero 2, 2025
Autor: jakobmina Jacobo Tlacaelel Mina Rodriguez Smpsys QuoreMind
Licencia: MIT

═══════════════════════════════════════════════════════════════════════════════
