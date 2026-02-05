import pytest
import numpy as np
from simon_h7.simulation.tripartite import TripartiteMetriplecticSystem

def test_tripartite_stability():
    """Verifica que el sistema alcanza un estado estable con input estándar."""
    sys = TripartiteMetriplecticSystem(input_val=5)
    state = sys.run_tripartite_task()
    
    assert state.is_stable is True
    assert state.output_a == 6
    assert state.output_b == (5 ^ 7) + 1
    assert state.l_symp > 0
    assert state.l_metr < 0

def test_berry_phase_accumulation():
    """Verifica que la fase de Berry se actualiza correctamente."""
    sys = TripartiteMetriplecticSystem(input_val=10)
    initial_phase = sys.state.berry_phase
    state = sys.run_tripartite_task()
    
    # La fase de Berry debe haber cambiado
    assert state.berry_phase != initial_phase

def test_decoherence_detection():
    """Simula una falla de simetría y verifica que se detecta decoherencia."""
    sys = TripartiteMetriplecticSystem(input_val=5)
    
    # Ejecutamos hilos manualmente para inyectar error
    sys.thread_particle()
    sys.thread_mirror()
    
    # Inyectamos "ruido" en el canal espejo
    sys.state.output_b = 1234 
    
    # El hilo de coherencia debe detectar la falla
    sys.thread_coherence()
    
    assert sys.state.is_stable is False
    assert sys.state.l_metr == 0.0 # En decoherencia el término métrico muere

def test_golden_operator_modulation():
    """Verifica que el operador áureo modula psi correctamente."""
    sys = TripartiteMetriplecticSystem(input_val=5)
    sys.run_tripartite_task()
    
    assert len(sys.state.psi) == 200
    assert np.all(np.abs(sys.state.psi) <= 1.0) # Modulado por cosenos
