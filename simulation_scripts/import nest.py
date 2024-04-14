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
