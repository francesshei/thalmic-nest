import numpy as np
import matplotlib.pyplot as plt

# Model parameters for TC and RE neurons
C_m = 1000  # membrane capacitance (pF)
g_L = 50  # leak conductance (nS)
E_L = -60  # resting potential (mV)
Delta_T = 2.5  # slope factor (mV)
V_th = -50  # spike threshold (mV)
V_reset = -60  # reset potential (mV)
t_ref = 2.5  # refractory period (ms)
tau_w = 600  # adaptation time constant for TC (ms)
a_tc = 200  # subthreshold adaptation for TC (nS)
a_re = 400  # subthreshold adaptation for RE (nS)
b_tc = 0  # spike-triggered adaptation for TC (pA)
b_re = 20  # spike-triggered adaptation for RE (pA)
tau_decay_exc = 5  # synaptic decay time constant excitatory synapse (ms)
tau_rise_exc = 0.4  # synaptic rise time constant excitatory synapse (ms)
tau_decay_inh = 20  # synaptic decay time constant for inhibitory synapse (ms)
tau_rise_inh = 0.4  # synaptic rise time constant inhibitory synapse (ms)
g_tc_re = -50  # synaptic strength from TC to RE (nS)
g_re_tc = 500  # synaptic strength from RE to TC (nS)
E_L_exc = -80 # reversal potential of the synapse (mV)
E_L_inh = 0 # reversal potential of the synapse (mV)

# simulation parameters
T = 3000  # simulation time (ms)
dt = 0.1  # time step for the simulation (ms)
time = np.arange(0, T+dt, dt)

# Initialize variables
I_stim_tc_values = [100, 200, 300, 400, 500]  # Different stimulus current values for TC
fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(20, 10))  # 2 rows, 5 columns

for idx, I_stim_tc in enumerate(I_stim_tc_values):
    # Reset variables for each simulation
    V_m_tc = E_L * np.ones(len(time))
    w_tc = np.zeros(len(time))
    V_m_re = E_L * np.ones(len(time))
    w_re = np.zeros(len(time))
    last_spike_time_tc = -np.inf
    last_spike_time_re = -np.inf
    S_tc_re = np.zeros(len(time))
    S_re_tc = np.zeros(len(time))

    # simulating the model
    for i in range(1, len(time)):
        
        t_since_last_spike_re = time[i] - last_spike_time_re + 1e-3  # 1 ms delay for TC
        t_since_last_spike_tc = time[i] - last_spike_time_tc + 1e-3  # 1 ms delay for RE
        
        S_tc_re[i] = S_tc_re[i-1] * np.exp(-t_since_last_spike_tc / tau_decay_exc) + (1 - S_tc_re[i-1]) * np.exp(-t_since_last_spike_tc / tau_rise_exc) # synaptic conductance for tc to re
        S_re_tc[i] = S_re_tc[i-1] * np.exp(-t_since_last_spike_re / tau_decay_inh) + (1 - S_re_tc[i-1]) * np.exp(-t_since_last_spike_re / tau_rise_inh) # synaptic conductance for re to tc

        # TC neuron update
        if (time[i] - last_spike_time_tc) > t_ref:
            w_tc[i] = w_tc[i-1] + (a_tc * (V_m_tc[i-1] - E_L) - w_tc[i-1]) / tau_w * dt
            V_m_tc[i] = V_m_tc[i-1] + (dt / C_m) * (-g_L * (V_m_tc[i-1] - E_L) + g_L * Delta_T * np.exp((V_m_tc[i-1] - V_th) / Delta_T) + w_tc[i-1] - g_re_tc * S_re_tc[i] * (V_m_tc[i-1] - E_L_inh) + I_stim_tc)
            if V_m_tc[i] >= V_th:
                V_m_tc[i] = V_reset
                w_tc[i] += b_tc
                last_spike_time_tc = time[i]


        #  RE neuron update
        if (time[i] - last_spike_time_re) > t_ref:
            w_re[i] = w_re[i-1] + (a_re * (V_m_re[i-1] - E_L) - w_re[i-1]) / tau_w * dt
            V_m_re[i] = V_m_re[i-1] + (dt / C_m) * (-g_L * (V_m_re[i-1] - E_L) + g_L * Delta_T * np.exp((V_m_re[i-1] - V_th) / Delta_T) + w_re[i-1] - g_tc_re * S_tc_re[i] * (V_m_re[i-1] - E_L_exc))
            if V_m_re[i] >= V_th:
                V_m_re[i] = V_reset
                w_re[i] += b_re
                last_spike_time_re = time[i]
    
    # Plot V_m_tc for the current I_stim_tc
    # Plot V_m_tc for the current I_stim_tc on the first row
    axes[0, idx].plot(time, V_m_tc, 'b', label=f'I_stim_tc = {I_stim_tc} pA')  # 'b' for blue color
    axes[0, idx].set_title(f'V_m_tc (I_stim_tc = {I_stim_tc} pA)')
    axes[0, idx].set_xlabel('Time (ms)')
    axes[0, idx].set_ylabel('V_m_tc (mV)')
    axes[0, idx].legend()

    # Plot V_m_re for the current I_stim_tc on the second row
    axes[1, idx].plot(time, V_m_re, 'r', label=f'I_stim_tc = {I_stim_tc} pA')  # 'r' for red color
    axes[1, idx].set_title(f'V_m_re (I_stim_tc = {I_stim_tc} pA)')
    axes[1, idx].set_xlabel('Time (ms)')
    axes[1, idx].set_ylabel('V_m_re (mV)')
    axes[1, idx].legend()

plt.tight_layout()
plt.show()