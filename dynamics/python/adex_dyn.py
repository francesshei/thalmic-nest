import numpy as np
import matplotlib.pyplot as plt

# AdEx model parameters
C_m = 1000  # Membrane capacitance (pF)
g_L = 50  # Leak conductance (nS)
E_L = -60  # Resting potential (mV)
Delta_T = 2.5  # Slope factor (mV)
V_th = -50  # Spike threshold (mV)
V_reset = -60  # Reset potential (mV)
t_ref = 2.5  # Refractory period (ms)
tau_w = 600  # Adaptation time constant (ms)
a = 200  # Subthreshold adaptation (nS)
b = 0  # Spike-triggered adaptation (pA)

# Simulation parameters
T = 1000  # Total time to simulate (ms)
dt = 0.1  # Time step (ms)
time = np.arange(0, T+dt, dt)

# Input currents for bifurcation analysis
I_stim_values = [200, 400]  # Two different stimulus currents (pA)

# Initialize plot
fig, ax = plt.subplots(figsize=(12, 7))

# Plot nullclines and trajectories for each I_stim value
for I_stim in I_stim_values:
    # Initialize variables for simulation
    V_m = E_L * np.ones(len(time))  # Membrane potential (mV)
    w = np.zeros(len(time))  # Adaptation variable (pA)
    last_spike_time = -np.inf  # Last spike time (initialize to negative infinity)

    # Simulate the model
    for i in range(1, len(time)):
        # Check for refractory period
        if (time[i] - last_spike_time) > t_ref:
            # Update the adaptation and membrane potential
            w[i] = w[i-1] + (a * (V_m[i-1] - E_L) - w[i-1]) / tau_w * dt
            V_m[i] = V_m[i-1] + (dt / C_m) * (-g_L * (V_m[i-1] - E_L) + g_L * Delta_T * np.exp((V_m[i-1] - V_th) / Delta_T) + w[i-1] + I_stim)
            
            # Spike condition
            if V_m[i] >= V_th:
                V_m[i-1] = V_th  # Spike cutoff
                V_m[i] = V_reset  # Reset membrane potential
                w[i] += b  # Increase adaptation current
                last_spike_time = time[i]  # Update the last spike time

    plt.plot(V_m, w, label='Trajectory for I_stim = {:.2f}'.format(I_stim), linewidth=0.5)
    V_m_nullcline = np.linspace(E_L, V_th, 1000)
    w_V_m_nullcline = (g_L * (V_m_nullcline - E_L) - g_L * Delta_T * np.exp((V_m_nullcline - V_th) / Delta_T) + I_stim) / a
    plt.plot(V_m_nullcline, w_V_m_nullcline, 'r--', label='V_m-nullcline for I_stim = {:.2f}'.format(I_stim))
    w_nullcline = a * (V_reset - E_L)
    plt.axhline(y=w_nullcline, color='g', linestyle='--', label='w-nullcline')

plt.title('Phase Plot with Nullclines for Two I_stim Values in the AdEx Model')
plt.xlabel('Membrane Potential V_m (mV)')
plt.ylabel('Adaptation Variable w (pA)')
plt.legend()
plt.show()

