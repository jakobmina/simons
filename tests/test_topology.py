import pytest
import numpy as np
from psimon.analysis.topology import VietorisRipsAnalysis

def test_proximity_graph_trivial():
    vr = VietorisRipsAnalysis(epsilon=1.5)
    points = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [2, 0, 0]
    ])
    adj = vr.compute_proximity_graph(points)
    
    # [0,1] dist=1 <= 1.5 -> True
    # [0,2] dist=2 > 1.5 -> False
    # [1,2] dist=1 <= 1.5 -> True
    assert adj[0, 1] == 1
    assert adj[0, 2] == 0
    assert adj[1, 2] == 1
    assert adj[1, 0] == 1
    assert np.all(np.diag(adj) == 0)

def test_get_edges():
    vr = VietorisRipsAnalysis(epsilon=1.5)
    adj = np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ])
    edges = vr.get_edges(adj)
    assert len(edges) == 2
    assert (0, 1) in edges
    assert (1, 2) in edges

def test_proximity_graph_zero_epsilon():
    vr = VietorisRipsAnalysis(epsilon=0)
    points = np.random.rand(10, 3)
    adj = vr.compute_proximity_graph(points)
    assert np.all(adj == 0)
