import numpy as np
from typing import List, Tuple, Dict, Any

class VietorisRipsAnalysis:
    """
    Análisis de Topología Algebraica: Complejo de Vietoris-Rips.
    Se enfoca en el 1-esqueleto (grafo de proximidad).
    """
    def __init__(self, epsilon: float = 0.5):
        self.epsilon = epsilon

    def compute_proximity_graph(self, points: np.ndarray) -> np.ndarray:
        """
        Construye la matriz de adyacencia del 1-esqueleto.
        A[i,j] = 1 si dist(p_i, p_j) <= epsilon. (Regla 2.2 distancias)
        """
        n = len(points)
        adj = np.zeros((n, n), dtype=int)
        
        # Cálculo optimizado con numpy
        # dists[i,j] = sqrt(sum((p_i - p_j)^2))
        dists = np.sqrt(np.sum((points[:, np.newaxis, :] - points[np.newaxis, :, :])**2, axis=2))
        
        adj = (dists <= self.epsilon).astype(int)
        np.fill_diagonal(adj, 0) # Sin auto-lazos para el grafo de proximidad
        
        return adj

    def get_edges(self, adj: np.ndarray) -> List[Tuple[int, int]]:
        """Extrae la lista de aristas a partir de la matriz de adyacencia."""
        edges = []
        n = len(adj)
        for i in range(n):
            for j in range(i + 1, n):
                if adj[i, j] == 1:
                    edges.append((i, j))
        return edges
