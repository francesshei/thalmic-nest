import nest
import matplotlib.pyplot as plt
import pandas as pd
from pynestml.frontend.pynestml_frontend import generate_nest_target

TO_BE_SIMULATED = "TC"

plt.style.use("dark_background")

# pylint: disable=no-member
GENERATE_MODULE = True

if GENERATE_MODULE:
    # Generate the neccesary code for NEST and install the module
    NEST_SIMULATOR_INSTALL_LOCATION = nest.ll_api.sli_func("statusdict/prefix ::")
    generate_nest_target(
        input_path="/home/furkan1/thalamic-nest/mo/models/thalamic_adex.nestml",
        target_path="/tmp/thalamic_adex",
        module_name="thalamic_adex_module",
        logging_level="ERROR",
        codegen_opts={"nest_path": NEST_SIMULATOR_INSTALL_LOCATION},
    )

nest.Install("thalamic_adex_module")


nest.ResetKernel()

# Create the AdEX model
neuron = nest.Create("aeif_cond_adex")

# INSPECT VALUES
# To access the model parameters, use: neuron.get()
# e.g. neuron.get("I_e") or "neuron.I_e"
# SET VALUES
# To set the parameters, directly specify a value:
# neuron.I_e = 376.0 or neuron.set({"I_e": 376.0, "C_m":250.0})

df = pd.read_excel("/home/furkan1/thalamic-nest/simulation_scripts/params.xlsx", sheet_name=TO_BE_SIMULATED)

params = {p: v for p, v in zip(df["parameter"].values, df["value"].values)}
neuron.set(params)
dc_current = nest.Create("dc_generator")
# Change the sign of the amplitude to simulate an hyperpolarizing input
dc_current.set({"start": 1200.0, "stop": 1600.0, "amplitude": 1000.0})
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
ax.set_xlim(1000, 2500)
ax.set_ylim(-100, 0)
plt.show()
