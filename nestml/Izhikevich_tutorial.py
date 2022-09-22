import matplotlib.pyplot as plt
import nest
import numpy as np
import os

from pynestml.frontend.pynestml_frontend import generate_nest_target

# Generate the neccesary code for NEST and install the module
#NEST_SIMULATOR_INSTALL_LOCATION = nest.ll_api.sli_func("statusdict/prefix ::")
#generate_nest_target(input_path="/Users/ju/Desktop/neuro/thalamic-nest/nestml/models/izhikevich_tutorial.nestml",
#                     target_path="/tmp/nestml-component",
#                     logging_level="ERROR",
#                     codegen_opts={"nest_path": NEST_SIMULATOR_INSTALL_LOCATION})

nest.Install("nestmlmodule")

# Reset NEST kernel
nest.set_verbosity("M_WARNING")
nest.ResetKernel()

# Create nodes
neuron = nest.Create("izhikevich_tutorial")
voltmeter = nest.Create("voltmeter")
# Set voltmeter params
voltmeter.set({"record_from": ["v", "u"]})
nest.Connect(voltmeter, neuron)
# Create and set DC generator node
cgs = nest.Create('dc_generator')
cgs.set({"amplitude": 25.})
nest.Connect(cgs, neuron)
# Create spike recorder node and connect to neuron
sr = nest.Create("spike_recorder")
nest.Connect(neuron, sr)
# Simulate the neuron
nest.Simulate(250.)
# Read data 
spike_times = nest.GetStatus(sr, keys='events')[0]['times']
# Plot data
fig, ax = plt.subplots(nrows=2)
ax[0].plot(voltmeter.get("events")["times"], voltmeter.get("events")["v"])
ax[1].plot(voltmeter.get("events")["times"], voltmeter.get("events")["u"])
ax[0].scatter(spike_times, 30 * np.ones_like(spike_times), marker="d", c="orange", alpha=.8, zorder=99)
for _ax in ax:
    _ax.grid(True)
ax[0].set_ylabel("v [mV]")
ax[1].set_ylabel("u")
ax[-1].set_xlabel("Time [ms]")
plt.show()