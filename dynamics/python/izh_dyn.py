import numpy as np
import matplotlib.pyplot as plt

# Izhikevich model parameters
a = 0.02
b = 0.2
c = -65
d = 8
V_peak = 30  # Spike cutoff value

# Refractory period
t_ref = 2.5  # Refractory period (ms)

# Simulation parameters
T = 1000  # Total time to simulate (ms)
dt = 0.1  # Time step (ms)
time = np.arange(0, T+dt, dt)

# Input currents for bifurcation analysis
I_stim_values = [10, 15]  # Example stimulus currents (pA)

# Initialize plot
fig, ax = plt.subplots(figsize=(12, 7))

# Plot nullclines and trajectories for each I_stim value
for I_stim in I_stim_values:
    # Initialize variables for simulation
    V = c * np.ones(len(time))  # Membrane potential (mV)
    u = b * V  # Recovery variable
    last_spike_time = -np.inf  # Initialize last spike time to negative infinity

    # Simulate the model
    for i in range(1, len(time)):
        # Check if outside refractory period
        if (time[i] - last_spike_time) > t_ref:
            V[i] = V[i-1] + dt * (0.04 * V[i-1]**2 + 5 * V[i-1] + 140 - u[i-1] + I_stim)
            u[i] = u[i-1] + dt * a * (b * V[i-1] - u[i-1])

        if V[i] >= V_peak:
            V[i-1] = V_peak  # Spike cutoff
            V[i] = c  # Reset membrane potential
            u[i] += d  # Reset recovery variable
            last_spike_time = time[i]  # Update last spike time


    plt.plot(V, u, label='Trajectory for I_stim = {:.2f}'.format(I_stim), linewidth=0.5)
    V_nullcline = np.linspace(c, V_peak, 1000)
    u_V_nullcline = 0.04 * V_nullcline**2 + 5 * V_nullcline + 140 - I_stim
    plt.plot(V_nullcline, u_V_nullcline, 'r--', label='V-nullcline for I_stim = {:.2f}'.format(I_stim))
    u_nullcline = b * V_nullcline
    plt.plot(V_nullcline, u_nullcline, 'g--', label='u-nullcline for I_stim = {:.2f}'.format(I_stim))

plt.title('Phase Plot with Nullclines for Two I_stim Values')
plt.xlabel('Membrane Potential V (mV)')
plt.ylabel('Recovery Variable u')
plt.legend()
plt.show()

