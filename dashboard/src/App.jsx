import React, { useState, useEffect, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { Activity, Zap, Shield, Cpu, Play, RefreshCw, Layers } from 'lucide-react';
import { motion as Motion } from 'framer-motion';
import {
  MetriplecticQLSTMCell,
  GoldenOperator,
  PhysicsEngine,
  GOLDEN_PHASE
} from './metriplectic_core';
import './App.css';

const App = () => {
  const [history, setHistory] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [cellState, setCellState] = useState({ h: [0, 0, 0, 0], c: [0, 0, 0, 0], On: 0, Ls: 0, Lm: 0 });

  const cellRef = useRef(new MetriplecticQLSTMCell(2, 4));
  const timerRef = useRef(null);

  const resetSimulation = () => {
    setIsRunning(false);
    if (timerRef.current) clearInterval(timerRef.current);
    cellRef.current = new MetriplecticQLSTMCell(2, 4);
    setHistory([]);
    setCurrentStep(0);
    setCellState({ h: [0, 0, 0, 0], c: [0, 0, 0, 0], On: 0, Ls: 0, Lm: 0 });
  };

  const stepSimulation = () => {
    const input = [Math.random() * 0.5, Math.random() * 0.5];
    const { h_next, c_next, On } = cellRef.current.forward(input, cellState.h, cellState.c);
    const { L_symp, L_metr } = cellRef.current.computeLagrangian(c_next);

    const newState = {
      h: h_next,
      c: c_next,
      On: On,
      Ls: L_symp,
      Lm: L_metr,
      step: cellRef.current.step_n
    };

    setCellState(newState);
    setHistory(prev => [...prev.slice(-19), newState]); // Keep last 20 steps
    setCurrentStep(prev => prev + 1);
  };

  const toggleSimulation = () => {
    if (isRunning) {
      clearInterval(timerRef.current);
    } else {
      timerRef.current = setInterval(stepSimulation, 800);
    }
    setIsRunning(!isRunning);
  };

  useEffect(() => {
    return () => clearInterval(timerRef.current);
  }, []);

  return (
    <div className="dashboard-container">
      <Motion.header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="header"
      >
        <div className="header-top" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1 className="title">m-QLSTM Dashboard</h1>
          <div className="glass-pill">EL MANDATO METRIPLÉCTICO</div>
        </div>
        <p className="subtitle">Quantum LSTM Evolution & Metriplectic Dynamics (H7 Optimized)</p>
      </Motion.header>

      <div className="controls">
        <button onClick={toggleSimulation}>
          {isRunning ? <Zap size={18} /> : <Play size={18} />}
          {isRunning ? 'Pause Engine' : 'Start Evolution'}
        </button>
        <button onClick={resetSimulation} style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)' }}>
          <RefreshCw size={18} />
          Reset
        </button>
      </div>

      <div className="stats-grid">
        <StatCard
          label="Symplectic Energy (H)"
          value={cellState.Ls.toFixed(4)}
          icon={<Cpu size={20} color="#4facfe" />}
          color="#4facfe"
        />
        <StatCard
          label="Metric Potential (S)"
          value={cellState.Lm.toFixed(4)}
          icon={<Activity size={20} color="#00f2fe" />}
          color="#00f2fe"
        />
        <StatCard
          label="Golden Operator (On)"
          value={cellState.On.toFixed(4)}
          icon={<Layers size={20} color="#ff9a9e" />}
          color="#ff9a9e"
        />
        <StatCard
          label="Step Count"
          value={currentStep}
          icon={<Shield size={20} color="#a18cd1" />}
          color="#a18cd1"
        />
      </div>

      <div className="stats-grid" style={{ gridTemplateColumns: '1fr' }}>
        <Motion.div
          className="glass-card"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <h3 className="stat-label">Lagrangian Dynamics: L_symp vs L_metr</h3>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={history}>
                <defs>
                  <linearGradient id="colorLs" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#4facfe" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#4facfe" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorLm" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#00f2fe" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#00f2fe" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="step" hide />
                <YAxis hide domain={[0, 'auto']} />
                <Tooltip
                  contentStyle={{ background: 'rgba(12,12,14,0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '10px' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Area type="monotone" dataKey="Ls" stroke="#4facfe" fillOpacity={1} fill="url(#colorLs)" name="Symplectic" />
                <Area type="monotone" dataKey="Lm" stroke="#00f2fe" fillOpacity={1} fill="url(#colorLm)" name="Metric" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Motion.div>
      </div>

      <div className="glass-card footer-info">
        <h3 className="stat-label">Physics Internal State (H7 Calibration)</h3>
        <div className="data-table-container">
          <table>
            <thead>
              <tr>
                <th>Parameter</th>
                <th>Reference (C#)</th>
                <th>Current Value</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Berry Phase Offset</td>
                <td>{GOLDEN_PHASE.toFixed(6)}</td>
                <td className="highlight">{(GOLDEN_PHASE * (currentStep % 2 === 0 ? 1 : -1)).toFixed(6)} <span style={{ fontSize: '0.7rem', opacity: 0.5 }}>rad</span></td>
              </tr>
              <tr>
                <td>Metriplectic Attractor</td>
                <td>0.4600</td>
                <td className="highlight">{PhysicsEngine.calculateMetriplecticEnergy(currentStep % 7).toFixed(4)} <span style={{ fontSize: '0.7rem', opacity: 0.5 }}>J</span></td>
              </tr>
              <tr>
                <td>Hidden Entropy (v)</td>
                <td>-</td>
                <td className="highlight">{Math.abs(cellState.h.reduce((a, b) => a + b, 0)).toFixed(4)} <span style={{ fontSize: '0.7rem', opacity: 0.5 }}>bits</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ label, value, icon, color }) => (
  <Motion.div
    className="glass-card stat-card"
    whileHover={{ scale: 1.02 }}
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
  >
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <span className="stat-label">{label}</span>
      {icon}
    </div>
    <span className="stat-value" style={{ color: color }}>{value}</span>
  </Motion.div>
);

export default App;
