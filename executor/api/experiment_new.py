from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from core.runtime import EXPERIMENTS, MODULES, EDF
import json

router = APIRouter(prefix="/remote_ctrl/sim", tags=["experiment-new"])

class NewExperimentRequest(BaseModel):
    experiment_name: str
    campaign_name: str
    experiment_uuid: UUID
    exp_exec_fingerprint: UUID
    base_index: Optional[int] = None


@router.post("/experiment/new", status_code=201)
def experiment_new(payload: NewExperimentRequest):
    EXPERIMENTS[str(payload.experiment_uuid)] = {"status": "P",
        "modules": {m: {"status": "P"} for m in MODULES},
         "config": {} } 
    create_edf(EDF)
    return {
        "id": str(payload.experiment_uuid),
        "experiment_definition": json.dumps(EDF)
    }

def create_edf(EDF) -> dict:
    EDF = {
        "meta":{
            "experiment_uuid": "",
            "filename": "edf.json"
        },
        "module_data": {
            "OpenFOAMCaseDirectory": {
                "case_directory": ""
            },
            "OpenFOAMSimulation":{            
                "mesh":{
                    "blockMeshDict":{
                        "gyroid_x": 0.014,
                        "gyroid_yz": 0.014,
                        "tube_ID": 0.022,
                        "inlet_x": -0.036,
                        "outlet_x": 0.072,
                        "center_buffer_factor": 0.4,
                        "stl_buffer_factor": 0.01,
                        "cel": 0.0008,
                        "grading": 1
                    },
                    "snappyHexMeshDict":{
                        "addLayers": False
                    },
                    "stl_file_name": "parameterized_structure.stl"
                },
                "solver":{},
                "control":{}
            },
            "ParameterizedStructureBuild":{
                "meta":{
                    "module_name": "tpms"
                },
                "create_structure": True,
                "module_data":{
                    "tpms":{
                        "type": "gyroid",
                        "scale": 0.014,
                        "cell_size_min": 0.214,
                        "cell_size_max": 0.857,
                        "density": 0.2,
                        "z_rotation": 0,
                        "y_rotation": 0,
                        "x_rotation": 0
                    }
                }
            },
            "OpenFOAMPostProcess":{
                "timeout": 86400
            }
        }
    }