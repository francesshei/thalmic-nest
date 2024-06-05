import numpy as np
import matplotlib.pyplot as plt

# Model parameters for TC neuron
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

# Input current (example)
I_stim = 100  # Stimulus current (pA)

# Initialize variables
V_m = E_L * np.ones(len(time))  # Membrane potential (mV)
w = np.zeros(len(time))  # Adaptation variable (pA)
last_spike_time = -np.inf  # Last spike time

# Simulate the model
for i in range(1, len(time)):
    if (time[i] - last_spike_time) > t_ref:
        # Update the adaptation and membrane potential
        w[i] = w[i-1] + (a * (V_m[i-1] - E_L) - w[i-1]) / tau_w * dt
        V_m[i] = V_m[i-1] + (dt / C_m) * (-g_L * (V_m[i-1] - E_L) + g_L * Delta_T * np.exp((V_m[i-1] - V_th) / Delta_T) + w[i-1] + I_stim)
        
        # Spike condition
        if V_m[i] >= V_th:
            V_m[i-1] = 0  # Add a spike to the plot
            V_m[i] = V_reset  # Reset membrane potential
            w[i] += b  # Increase adaptation current
            last_spike_time = time[i]

# Plot the membrane potential
plt.plot(time, V_m)
plt.title('AdEx Neuron Model')
plt.xlabel('Time (ms)')
plt.ylabel('Membrane Potential (mV)')
plt.show()
