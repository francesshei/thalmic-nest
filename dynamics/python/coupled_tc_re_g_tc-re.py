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

E_L_exc = -80 # reversal potential of the synapse (mV)
E_L_inh = 0 # reversal potential of the synapse (mV)

g_tc_re = 50  # synaptic strength from TC to RE (μS)
g_re_tc = 500  # synaptic strength from RE to TC (μS)

# simulation parameters
T = 3000  # simulation time (ms)
dt = 0.1  # time step for the simulation (ms)
time = np.arange(0, T+dt, dt)

# Initialize variables

V_m_tc = E_L * np.ones(len(time))  # membrane potential of TC (mV)
w_tc = np.zeros(len(time))  # adaptation variable of TC (pA)

V_m_re = E_L * np.ones(len(time))  # membrane potential of RE (mV)
w_re = np.zeros(len(time))  # adaptation variable of RE (pA)

last_spike_time_tc = -np.inf  # last spike time of TC
last_spike_time_re = -np.inf  # last spike time of RE

S_tc_re = np.zeros(len(time))  # synaptic conductance from TC to RE
S_re_tc = np.zeros(len(time))  # synaptic conductance from RE to TC


# Define stimulation times and duration
stim_times = [10, 50]  # times of stimulation (ms)
t_stim = 10  # duration of each stimulation (ms)
I_stim_tc = 100 # stimulus current for TC (pA)

def is_stim_time(t, stim_times, t_stim):
    for stim_time in stim_times:
        if stim_time <= t < stim_time + t_stim:
            return True
    return False


g_re_tc_values = [25, 50]

# Create a figure and axes for the plots
fig, axs = plt.subplots(len(g_re_tc_values), 1, figsize=(10, 8))


for idx, g_re_tc in enumerate(g_re_tc_values):
    # Reset the initial conditions for each simulation
    V_m_tc = E_L * np.ones(len(time))  # membrane potential of TC (mV)
    w_tc = np.zeros(len(time))  # adaptation variable of TC (pA)

    V_m_re = E_L * np.ones(len(time))  # membrane potential of RE (mV)
    w_re = np.zeros(len(time))  # adaptation variable of RE (pA)

    last_spike_time_tc = -np.inf  # last spike time of TC
    last_spike_time_re = -np.inf  # last spike time of RE

    S_tc_re = np.zeros(len(time))  # synaptic conductance from TC to RE
    S_re_tc = np.zeros(len(time))  # synaptic conductance from RE to TC


    # simulating the model
    for i in range(1, len(time)):
        
        t_since_last_spike_re = time[i] - last_spike_time_re + 1e-3  # 1 ms delay for TC
        t_since_last_spike_tc = time[i] - last_spike_time_tc + 1e-3  # 1 ms delay for RE
        
        S_tc_re[i] = S_tc_re[i-1] * np.exp(-t_since_last_spike_tc / tau_decay_exc) + (1 - S_tc_re[i-1]) * np.exp(-t_since_last_spike_tc / tau_rise_exc) # synaptic conductance for tc to re
        S_re_tc[i] = S_re_tc[i-1] * np.exp(-t_since_last_spike_re / tau_decay_inh) + (1 - S_re_tc[i-1]) * np.exp(-t_since_last_spike_re / tau_rise_inh) # synaptic conductance for re to tc
        
        I_stim = I_stim_tc if is_stim_time(time[i], stim_times, t_stim) else 0

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

    idx_ms = next(i for i, t in enumerate(time) if t > 2600)

    # Plot the results for the current value of g_re_tc up to 2000 ms
    axs[idx].plot(time[:idx_ms], V_m_re[:idx_ms], label=f'g_re_tc = {g_re_tc}')
    axs[idx].set_title(f'Membrane Potential Over Time for g_re_tc = {g_re_tc}')
    axs[idx].set_xlabel('Time (ms)')
    axs[idx].set_ylabel('Membrane Potential (mV)')
    axs[idx].legend()

# Adjust the layout and show the plots
plt.tight_layout()
plt.show()