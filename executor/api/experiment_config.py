from calendar import c

from fastapi import APIRouter
from pydantic import BaseModel, RootModel
from typing import Dict
import json
from Executor_openFOAM.executor.api import module_status
from Executor_openFOAM.executor.core import status_types
from core.runtime import EXPERIMENTS, MODULES, EDF
# MODULES = ["OpenFOAMCaseDirectory", "ParameterizedStructureBuild", "OpenFOAMSimulation", "OpenFOAMPostProcess"]

router = APIRouter(prefix="/remote_ctrl/sim", tags=["experiment-config"])

class ConfigInputs(RootModel[Dict]):
    pass


@router.post("/experiment/{experiment_uuid}/config/{module_name}")
def config_inputs(experiment_uuid: str, module_name: str, payload: ConfigInputs):
    # Value Validation/Setting
    
    # Valid values
    match module_name:
        case "OpenFOAMCaseDirectory":
            valid_inputs = ["case_directory"]
        case "ParameterizedStructureBuild":
            valid_inputs = [
                "create_structure",
                "type",
                "scale",
                "cell_size_min",
                "cell_size_max",
                "density",
                "z_rotation",
                "y_rotation",
                "x_rotation"
            ]
        case "OpenFOAMSimulation":
            valid_inputs = [
                "stl_file_name",
                "gyroid_x",
                "gyroid_yz",
                "tube_ID",
                "inlet_x",
                "outlet_x",
                "center_buffer_factor",
                "stl_buffer_factor",
                "cel",
                "grading",
                "addLayers"
            ]
        case "OpenFOAMPostProcess":
            valid_inputs = ["timeout"]

    
    load = payload.model_dump()
    for key in load.keys:
        if key not in valid_inputs:
            return {
                    "status": status_types.ModuleStatus.TERMINATED.value,
                    "msg": f"invalid input: {key}"
                    }
        else:
            pass
    
    writepath = router.prefix + f"/experiment/{experiment_uuid}/edf.json"

    return {"status":status_types.ModuleStatus.PROPOSED.value}