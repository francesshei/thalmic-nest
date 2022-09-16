import nest
import matplotlib.pyplot as plt
import pandas as pd

nest.ResetKernel()

# Create the AdEX model
neuron = nest.Create("aeif_cond_exp")

# INSPECT VALUES
# To access the model parameters, use: neuron.get() 
# e.g. neuron.get("I_e") or "neuron.I_e"
# SET VALUES
# To set the parameters, directly specify a value:
# neuron.I_e = 376.0 or neuron.set({"I_e": 376.0, "C_m":250.0})
df = pd.read_excel('params.xlsx')
params = {p: v for p,v in zip(df['parameter'].values, df['value'].values)}
#neuron.set({"I_e": 1.0, "C_m": 1000., "g_L": 50., "E_L": -60., 
#            "Delta_T": 2.5, "V_th": -50., "t_ref": 2.5, "tau_w": 600.,
#            "a": 400.0, "b": 20.0})
neuron.set(params)
dc_current = nest.Create("dc_generator")
dc_current.set({"start":1200.0, "stop":1600.0, "amplitude": -1250.})

# Create the recording devices
multimeter = nest.Create("multimeter")
multimeter.set(record_from=["V_m"])

spikerecorder = nest.Create("spike_recorder")

# Connect devices to the neuron model
nest.Connect(multimeter, neuron)
nest.Connect(neuron, spikerecorder)
nest.Connect(dc_current, neuron)

# Run the simulation for 1000.0 ms (1 sec)
nest.Simulate(2500.0)

# Access the multimeter quantities (dictionary)
dmm = multimeter.get()
# Specifically, retrieve the voltage values and the timestamps of recording
Vms = dmm["events"]["V_m"]
ts = dmm["events"]["times"]

# Plot the result
fig, ax = plt.subplots()
ax.plot(ts, Vms)
ax.set_xlim(1000,2500)
ax.set_ylim(-100,0)
plt.show()