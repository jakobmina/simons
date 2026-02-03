/**
 * Metriplectic Core Engine v1.0
 * Calibrated with C# Mobile H7 Constants.
 */

export const H7_MODULO = 7;
export const GOLDEN_PHASE = 0.3674234614174767;
export const PHI = (1 + Math.sqrt(5)) / 2;

export const GoldenOperator = {
    compute: (n) => {
        return Math.cos(Math.PI * n) * Math.cos(Math.PI * PHI * n);
    }
};

export const PhysicsEngine = {
    calculateMetriplecticEnergy: (n) => {
        const center = 3.5;
        const distance = Math.abs(n - center);
        if (distance === 2.5) return 0.4783;
        if (distance === 1.5) return 0.4609;
        if (distance === 0.5) return 0.4513;
        return 0.4600;
    },

    calculateBerryPhase: (n, momento) => {
        const basePhase = (2 * Math.PI * momento) / H7_MODULO;
        const scfrCorrection = GOLDEN_PHASE * (n <= 3 ? 1 : -1);
        return basePhase + scfrCorrection;
    }
};

export class QuantumLayer {
    constructor(n_inputs, n_qubits) {
        this.n_inputs = n_inputs;
        this.n_qubits = n_qubits;
        this.theta = Array.from({ length: n_qubits }, () => 
            Array.from({ length: n_inputs }, () => Math.random() * 2 * Math.PI)
        );
        this.phi = Array.from({ length: n_qubits }, () => 
            Array.from({ length: n_inputs }, () => Math.random() * 2 * Math.PI)
        );
    }

    forward(x) {
        // Simplified dot product for simulation
        const rho = this.theta.map((row, i) => {
            let sumY = 0;
            let sumZ = 0;
            for (let j = 0; j < x.length; j++) {
                sumY += row[j] * x[j];
                sumZ += this.phi[i][j] * x[j];
            }
            // Probabilidad de colapso |psi_1|^2
            return Math.pow(Math.sin(sumY / 2.0), 2);
        });
        return rho;
    }
}

export class MetriplecticQLSTMCell {
    constructor(n_inputs, n_hidden, step_n = 0) {
        this.n_inputs = n_inputs;
        this.n_hidden = n_hidden;
        this.step_n = step_n;
        this.S_potential = 0.1;

        this.gate_f = new QuantumLayer(n_inputs + n_hidden, n_hidden);
        this.gate_i = new QuantumLayer(n_inputs + n_hidden, n_hidden);
        this.gate_c = new QuantumLayer(n_inputs + n_hidden, n_hidden);
        this.gate_o = new QuantumLayer(n_inputs + n_hidden, n_hidden);
    }

    computeLagrangian(psi) {
        const L_symp = 0.5 * psi.reduce((acc, val) => acc + val * val, 0);
        const L_metr = this.S_potential * psi.reduce((acc, val) => acc + Math.pow(Math.log(val + 1e-10), 2), 0);
        return { L_symp, L_metr };
    }

    forward(x, h_prev, c_prev) {
        const On = GoldenOperator.compute(this.step_n);
        const combined = [...x, ...h_prev];

        const f_gate = this.gate_f.forward(combined);
        const i_gate = this.gate_i.forward(combined);
        const c_tilde = this.gate_c.forward(combined);
        const o_gate = this.gate_o.forward(combined);

        const dissipation = c_prev.map(v => this.S_potential * On * v);
        
        const c_next = c_prev.map((v, i) => {
            let val = f_gate[i] * v + i_gate[i] * c_tilde[i] - dissipation[i];
            return Math.min(Math.max(val, 0.01), 0.99); // Regla 1.3
        });

        const h_next = o_gate.map((v, i) => v * Math.tanh(c_next[i]));

        this.step_n++;
        return { h_next, c_next, On };
    }
}
