import os
import nest
from pynestml.frontend.pynestml_frontend import generate_nest_target

NEST_SIMULATOR_INSTALL_LOCATION = nest.ll_api.sli_func("statusdict/prefix ::")


def load_module(path_to_module=None, module_name="nestmlmodule"):
    if path_to_module is not None:
        generate_nest_target(
            input_path=path_to_module,
            target_path=f"/tmp/{module_name}",
            module_name=module_name,
            suffix="_nestml",
            logging_level="ERROR",  # try "INFO" for more debug information
            codegen_opts={"nest_path": NEST_SIMULATOR_INSTALL_LOCATION},
        )
    # pylint:disable=no-member
    nest.Install(module_name)
