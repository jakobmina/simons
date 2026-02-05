import pytest
import numpy as np
from simon_h7_metriplectic import MetriplecticH7System

@pytest.fixture
def h7_system():
    return MetriplecticH7System()

def test_golden_operator_range(h7_system):
    """Regla 2.1: El operador áureo debe estar en el rango [-1, 1]"""
    n = np.arange(100)
    O_n = h7_system.golden_operator(n)
    assert np.all(O_n >= -1.0)
    assert np.all(O_n <= 1.0)

def test_metriplectic_competition(h7_system):
    """Regla 1.3: Prohibición de singularidades (Competencia detectada)"""
    data = h7_system.evolve_state(n_steps=100)
    
    # Ambos términos deben coexistir y ser distintos de cero
    assert not np.allclose(data['H_term'], 0)
    assert not np.allclose(data['S_term'], 0)
    
    # El término métrico debe mostrar relajación (disminuir en promedio)
    assert data['S_term'][-1] < data['S_term'][0]

def test_lagrangian_balance(h7_system):
    """Regla 3.1: Existencia de componentes L_symp y L_metr"""
    data = h7_system.evolve_state(n_steps=100)
    
    # Verificamos que los valores sean finitos y numéricamente estables
    assert np.isfinite(data['L_symp'])
    assert np.isfinite(data['L_metr'])
    
    # No deben ser cero si hay evolución
    assert abs(data['L_symp']) > 1e-10
    assert abs(data['L_metr']) > 1e-10

def test_bloch_normalization(h7_system):
    """Verificar que la trayectoria de Bloch se mantenga en la superficie"""
    data = h7_system.evolve_state(n_steps=100)
    norms = np.sqrt(data['x_bloch']**2 + data['y_bloch']**2 + data['z_bloch']**2)
    assert np.allclose(norms, 1.0, atol=1e-7)

def test_nomenclatura_metriplectica(h7_system):
    """Regla 3.2: Verificar nombres de variables físicas"""
    data = h7_system.evolve_state(n_steps=10)
    assert 'psi' in data
    assert 'rho' in data
    assert 'v' in data
    
    # rho debe ser una densidad de probabilidad real (positiva y suma 1)
    assert np.all(data['rho'] >= 0)
    assert np.isclose(np.sum(data['rho']), 1.0)
