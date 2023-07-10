import nest
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pynestml.frontend.pynestml_frontend import generate_nest_target

plt.style.use("dark_background")


SPIKE_TIMES = np.array(
    [
        4.6,
        18.1,
        20.1,
        20.6,
        20.9,
        24.3,
        26.2,
        27.2,
        27.8,
        31.1,
        31.2,
        31.3,
        32.3,
        33.2,
        33.6,
        36.2,
        36.8,
        37.5,
        37.9,
        38.3,
        41.9,
        42.0,
        43.4,
        44.6,
        44.9,
        45.1,
        45.2,
        45.7,
        46.4,
        46.6,
        47.2,
        47.3,
        47.6,
        48.7,
    ]
)

# Reproducing the two-neuron experiment:
# 1- Creat the simulation nodes and connect them

# pylint:disable=no-member

# pylint: disable=no-member
GENERATE_MODULE = False

if GENERATE_MODULE:
    # Generate the neccesary code for NEST and install the module
    NEST_SIMULATOR_INSTALL_LOCATION = nest.ll_api.sli_func("statusdict/prefix ::")
    generate_nest_target(
        input_path="../nestml/models/thalamic_adex.nestml",
        target_path="/tmp/thalamic_adex",
        module_name="thalamic_adex_module",
        logging_level="ERROR",
        codegen_opts={"nest_path": NEST_SIMULATOR_INSTALL_LOCATION},
    )

nest.Install("thalamic_adex_module")


nest.ResetKernel()
nest.SetKernelStatus({"resolution": 0.1})

# Create the AdEX model
neurons = nest.Create("aeif_cond", n=2)

tc_df = pd.read_excel("params.xlsx", sheet_name="TC")
tc_params = {p: v for p, v in zip(tc_df["parameter"].values, tc_df["value"].values)}
neurons[0].set(tc_params)

re_df = pd.read_excel("params.xlsx", sheet_name="RE")
re_params = {p: v for p, v in zip(re_df["parameter"].values, re_df["value"].values)}
neurons[1].set(re_params)


# Create the recording devices
tc_multimeter = nest.Create("multimeter")
tc_multimeter.set(record_from=["V_m"])

re_multimeter = nest.Create("multimeter")
re_multimeter.set(record_from=["V_m"])

spike_gen = nest.Create("spike_generator", params={"spike_times": SPIKE_TIMES})

spikerecorder = nest.Create("spike_recorder")

# Connect the nodes
# TC - RE
nest.Connect(neurons[0], neurons[1], syn_spec={"weight": 7930, "delay": 1.0})
# RE - TC
nest.Connect(neurons[1], neurons[0], syn_spec={"weight": -150000.0, "delay": 1.0})
# Ext - TC
nest.Connect(spike_gen, neurons[0], syn_spec={"weight": 45.0})


nest.Connect(tc_multimeter, neurons[0])
nest.Connect(re_multimeter, neurons[1])

nest.Simulate(5000)


# Plot data
fig, ax = plt.subplots(nrows=1)
ax.plot(
    tc_multimeter.get("events")["times"],
    tc_multimeter.get("events")["V_m"],
    color="#E62314",
)
ax.plot(
    re_multimeter.get("events")["times"],
    re_multimeter.get("events")["V_m"],
    color="#1e2b61",
)
plt.show()
