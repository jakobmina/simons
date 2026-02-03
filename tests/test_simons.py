import pytest
import numpy as np
import math
from simons_complete import AnalizadorSimetriaDinamica, MetriplecticMomentumOracle, AlgoritmoSimonCuantico

def test_analizador_simetria_h7():
    analizador = AnalizadorSimetriaDinamica()
    lista_n = [1, 6, 2, 5]
    analisis = analizador.analizar_lista_n(lista_n, s=7)
    
    assert len(analisis) == 4
    for a in analisis:
        # Conservación H=7
        assert a['momento'] + a['complemento_H7'] == 7
        # Fase de Berry en rango [0, 2pi)
        assert 0 <= a['fase_berry_rad'] < 2 * math.pi

def test_metriplectic_oracle_21():
    oracle = MetriplecticMomentumOracle(s=7, n_bits=3)
    
    # Estados 2-1
    assert oracle.evaluar_momento(1) == (1, 0)
    assert oracle.evaluar_momento(6) == (0, 1)
    assert oracle.evaluar_momento(0) == (0, 0)
    
    # Simetría f(x) = f(x ^ 7)
    # x ^ 7 es equivalente a NOT x, o 7-x en 3 bits
    for x in range(8):
        assert oracle.evaluar(x) == oracle.evaluar(x ^ 7)

def test_simon_algorithm_recovery():
    # Usamos s=7 y n_bits=3
    oracle = MetriplecticMomentumOracle(s=7, n_bits=3)
    simon = AlgoritmoSimonCuantico(oracle, num_mediciones=50)
    
    s_est, meds, conf = simon.ejecutar_completo()
    
    # Verificamos que las mediciones cumplen y * s = 0 (mod 2)
    for y in meds:
        if y != 0:
            prod = bin(y & 7).count('1') % 2
            assert prod == 0
            
    # El estimado debería ser 7 si las mediciones son variadas
    # (A veces puede fallar por aleatoriedad, pero con 50 mediciones es probable)
    assert s_est == 7

def test_metriplectic_energy():
    oracle = MetriplecticMomentumOracle(s=7, n_bits=3)
    # H = H_symp + S_metr
    # H_symp es constante (7/14 = 0.5)
    # S_metr varía con el momento
    e1 = oracle.aplicar_metriplectica(1)
    e3 = oracle.aplicar_metriplectica(3)
    
    # Las energías deben ser positivas y finitas
    assert 0 < e1 < 1
    assert 0 < e3 < 1
    assert e1 != e3
