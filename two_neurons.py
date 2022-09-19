import nest
import matplotlib.pyplot as plt
import pandas as pd

nest.ResetKernel()

# Create the AdEX model
neurons = nest.Create("aeif_cond_exp", n=2)

tc_df = pd.read_excel('params.xlsx', sheet_name="TC")
tc_params = {p: v for p,v in zip(tc_df['parameter'].values, tc_df['value'].values)}
neurons[0].set(tc_params)

re_df = pd.read_excel('params.xlsx', sheet_name="RE")
re_params = {p: v for p,v in zip(re_df['parameter'].values, re_df['value'].values)}
neurons[1].set(re_params)

dc_current = nest.Create("dc_generator")
dc_current.set({"start":1200.0, "stop":1600.0, "amplitude": -1250.})

# Create the recording devices
multimeter = nest.Create("multimeter")
multimeter.set(record_from=["V_m"])

spikerecorder = nest.Create("spike_recorder")

# TODO: implement a proper neuron model in NESTML