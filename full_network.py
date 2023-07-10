import nest
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from pynestml.frontend.pynestml_frontend import generate_nest_target

plt.style.use("dark_background")

GAP_JUNCTIONS = True

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

# pylint: disable=no-member
GENERATE_MODULE = False

if GENERATE_MODULE:
    # Generate the neccesary code for NEST and install the module
    NEST_SIMULATOR_INSTALL_LOCATION = nest.ll_api.sli_func("statusdict/prefix ::")
    generate_nest_target(
        input_path="nestml/models/thalamic_adex.nestml",
        target_path="/tmp/thalamic_adex",
        module_name="thalamic_adex_module",
        logging_level="ERROR",
        codegen_opts={"nest_path": NEST_SIMULATOR_INSTALL_LOCATION},
    )

nest.Install("thalamic_adex_module")
nest.ResetKernel()

# Create the AdEX models and set their parameters
tc_neurons = nest.Create("aeif_cond", n=250)
re_neurons = nest.Create("aeif_cond", n=250)


tc_df = pd.read_excel("params.xlsx", sheet_name="TC")
tc_params = {p: v for p, v in zip(tc_df["parameter"].values, tc_df["value"].values)}
tc_neurons.set(tc_params)
tc_neurons.tau_decay_inh = 10.0

re_df = pd.read_excel("params.xlsx", sheet_name="RE")
re_params = {p: v for p, v in zip(re_df["parameter"].values, re_df["value"].values)}
re_neurons.set(re_params)
re_neurons.tau_decay_inh = 10.0


# Connect the network
tc_re_conn = {"rule": "pairwise_bernoulli", "p": 0.01}
tc_re_syn = {"weight": 200, "delay": 1.0}

re_re_conn = {"rule": "pairwise_bernoulli", "p": 0.04}
re_re_syn = {"weight": 300, "delay": 1.0}

re_tc_conn = {"rule": "pairwise_bernoulli", "p": 0.04}
re_tc_syn = {"weight": 300, "delay": 1.0}

# Create the recording devices
tc_multimeter = nest.Create("multimeter")
tc_multimeter.set(record_from=["V_m"])

re_multimeter = nest.Create("multimeter")
re_multimeter.set(record_from=["V_m"])

tc_recorder = nest.Create("spike_recorder")
re_recorder = nest.Create("spike_recorder")

# External stimulation
spike_gen = nest.Create("spike_generator", params={"spike_times": SPIKE_TIMES})

# Connect the nodes
# TC - RE
nest.Connect(tc_neurons, re_neurons, conn_spec=tc_re_conn, syn_spec=tc_re_syn)
# RE - TC
nest.Connect(re_neurons, tc_neurons, conn_spec=re_tc_conn, syn_spec=re_tc_syn)
# RE - RE
if GAP_JUNCTIONS:
    g = nx.watts_strogatz_graph(250, 10, 0.25, seed=None)
    A = nx.adjacency_matrix(g).todense()
    for i, pre in enumerate(re_neurons):
        # Extract the weights column.
        weights = A[:, i]
        # To only connect pairs with a nonzero weight, we use array indexing
        # to extract the weights and post-synaptic neurons.
        nonzero_indices = np.where(weights != 0)[0]
        weights = weights[nonzero_indices]
        post = re_neurons[nonzero_indices]
        # Generate an array of node IDs for the column of the weight
        # matrix, with length based on the number of nonzero
        # elements. The array's dtype must be an integer.
        pre_array = np.ones(len(nonzero_indices), dtype=int) * pre.get("global_id")
        re_re_syn = {
            "weight": np.array([300] * len(weights)),
            "delay": np.array([1.0] * len(weights)),
        }
        # nest.Connect() automatically converts post to a NumPy array
        # because pre_array contains multiple identical node IDs. When
        # also specifying a one_to_one connection rule, the arrays of
        # node IDs can then be connected.
        nest.Connect(pre_array, post, conn_spec="one_to_one", syn_spec=re_re_syn)


else:
    nest.Connect(re_neurons, tc_neurons, conn_spec=re_re_conn, syn_spec=re_re_syn)


# Ext - TC
nest.Connect(spike_gen, tc_neurons[:5], syn_spec={"weight": 40.0})
nest.Connect(tc_neurons, tc_recorder)
nest.Connect(re_neurons, re_recorder)


nest.Connect(tc_multimeter, tc_neurons[10])
nest.Connect(re_multimeter, re_neurons[10])


nest.Simulate(5000)

# nest.raster_plot.from_device(tc_recorder, hist=True)
# nest.raster_plot.from_device(re_recorder, hist=True)
# plt.show()


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
