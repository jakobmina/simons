import numpy as np
import math
from dataclasses import dataclass
from typing import Tuple

@dataclass
class MetriplecticH7System:
    """
    Sistema Dinámico Cuántico Simon H7 según el Mandato Metriplético.
    
    Regla 1.1 (Simpléctica): Hamiltoniano H para evolución unitaria.
    Regla 1.2 (Métrica): Potencial S para relajación y estabilidad.
    Regla 2.1 (Fondo Estructurado): Operador Áureo O_n.
    Regla 3.2 (Nomenclatura): psi, rho, v.
    """
    phi_golden: float = (1 + math.sqrt(5)) / 2
    delta: float = 0.1  # Parámetro de estabilidad
    
    def golden_operator(self, n: np.ndarray) -> np.ndarray:
        """
        O_n = cos(π n) * cos(π φ n)
        Modulación fundamental del vacío estructurado.
        """
        return np.cos(np.pi * n) * np.cos(np.pi * self.phi_golden * n)

    def compute_lagrangian(self, psi: np.ndarray, H: float, S: float) -> Tuple[float, float]:
        """
        Regla 3.1: Devuelve L_symp y L_metr.
        """
        # L_symp: Basado en la energía conservativa (Hamiltoniano)
        L_symp = np.sum(np.abs(psi)**2 * H)
        
        # L_metr: Basado en la entropía/disipación (Potencial de Relajación)
        L_metr = -np.sum(np.abs(psi)**2 * S)
        
        return float(L_symp), float(L_metr)

    def evolve_state(self, n_steps: int = 1000) -> dict:
        """
        Simula la evolución del campo psi bajo la competencia Metriplética.
        """
        n = np.arange(n_steps)
        O_n = self.golden_operator(n)
        
        # psi: Campo de orden modulado por el operador áureo
        psi = np.exp(1j * (n * self.phi_golden + self.delta * n**2)) * O_n
        
        # rho: Densidad de probabilidad (Métrica)
        rho = np.abs(psi)**2
        rho /= (np.sum(rho) + 1e-15)
        
        # v: Flujo de información/velocidad
        v = np.gradient(np.angle(psi))
        
        # Dinámica Metriplética
        # d_symp = {u, H} -> Término conservativo (fase)
        # d_metr = [u, S] -> Término disipativo (amplitud/relajación)
        H_term = np.cos(n / self.phi_golden) # Simpléctico (Oscilatorio)
        S_term = np.exp(-n / (10 * self.phi_golden)) # Métrico (Relajación)
        
        L_s, L_m = self.compute_lagrangian(psi, H_term.mean(), S_term.mean())
        
        # Bloch Coordinates para visualización
        # Mapeo de psi a la esfera de Bloch (segmentado por n)
        # Simplificamos para la trayectoria
        x_bloch = 2 * np.real(psi * np.conj(psi * 0.5)) # Proyección simplificada
        y_bloch = 2 * np.imag(psi * np.conj(psi * 0.5))
        z_bloch = np.abs(psi)**2 - np.abs(psi * 0.5)**2
        
        # Normalización Bloch
        norm_b = np.sqrt(x_bloch**2 + y_bloch**2 + z_bloch**2 + 1e-15)
        x_bloch /= norm_b
        y_bloch /= norm_b
        z_bloch /= norm_b

        return {
            "n": n,
            "psi": psi,
            "rho": rho,
            "v": v,
            "O_n": O_n,
            "H_term": H_term,
            "S_term": S_term,
            "L_symp": L_s,
            "L_metr": L_m,
            "x_bloch": x_bloch,
            "y_bloch": y_bloch,
            "z_bloch": z_bloch
        }
