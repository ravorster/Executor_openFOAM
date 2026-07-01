from logging import config
import threading
import time
import CCUS_CFD_execution_software.OpenFOAMCaseDirectory as OpenFOAMCaseDirectory
import CCUS_CFD_execution_software.OpenFOAMSimulation as OpenFOAMSimulation
import CCUS_CFD_execution_software.ParameterizedStructureBuild as ParameterizedStructureBuild
import CCUS_CFD_execution_software.OpenFOAMPostProcess as OpenFOAMPostProcess
from Executor_openFOAM.executor.core import status_types

# In-memory experiment table
EXPERIMENTS = {}   # { uuid: {"status": "Q"} }
# Executor-defined modules
MODULES = [
     "OpenFOAMCaseDirectory", 
     "ParameterizedStructureBuild", 
     "OpenFOAMSimulation", 
     "OpenFOAMPostProcess"
     ]
# Persistent experiment definition file
EDF = dict()

def simulate_experiment(exp_uuid: str):
    try:
        print("SIM START", exp_uuid)
        exp = EXPERIMENTS[exp_uuid]
        print("EXP FOUND:", exp)

        # time.sleep(3)
        exp["status"] = status_types.ExperimentStatus.RUNNING.value
        print("SET TO R")

        # Create OpenFOAM working directory
        module = "OpenFOAMCaseDirectory"
        exp["modules"][module]["status"] = status_types.ExperimentStatus.RUNNING.value
        print("RUNNING", module)
        print(OpenFOAMCaseDirectory.create_openfoam_case_dummy())
        exp["modules"][module]["status"] = status_types.ExperimentStatus.COMPLETED.value
        print("COMPLETED", module)
        
        # Put .stl in OpenFOAM working directory
        module = "ParameterizedStructureBuild"
        exp["modules"][module]["status"] = status_types.ExperimentStatus.RUNNING.value
        print("RUNNING", module)
        print(ParameterizedStructureBuild.parameterized_structure_build_dummy())
        exp["modules"][module]["status"] = status_types.ExperimentStatus.COMPLETED.value
        print("COMPLETED", module)

        # Run OpenFOAM simulation
        module = "OpenFOAMSimulation"
        exp["modules"][module]["status"] = status_types.ExperimentStatus.RUNNING.value
        print("RUNNING", module)
        print(OpenFOAMSimulation.openFOAM_dummy())
        exp["modules"][module]["status"] = status_types.ExperimentStatus.COMPLETED.value
        print("COMPLETED", module)

        # Do post-processing
        module = "OpenFOAMPostProcess"
        exp["modules"][module]["status"] = status_types.ExperimentStatus.RUNNING.value
        print("RUNNING", module)
        print(OpenFOAMPostProcess.openFOAM_postprocess_dummy())
        exp["modules"][module]["status"] = status_types.ExperimentStatus.COMPLETED.value
        print("COMPLETED", module)

        exp["status"] = status_types.ExperimentStatus.COMPLETED.value
        print("EXP COMPLETE")

    except Exception as e:
        print("SIM ERROR:", e)


def run(exp,m):
    config = exp["config"].get(m, {})
    if "x" in config:
            exp["modules"][m]["output"] = {"x_plus_one": config["x"] + 1}
    else:
        exp["modules"][m]["output"] = {"x_plus_one": None}

def start_experiment(exp_uuid: str):
    t = threading.Thread(target=simulate_experiment, args=(exp_uuid,))
    t.start()
