from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import Optional
from pathlib import Path

from Executor_openFOAM.executor.core import status_types

router = APIRouter(prefix="/remote_ctrl/sim", tags=["experiment-config-file"])

class FileUploadMeta(BaseModel):
    checksum: Optional[str] = None


@router.post("/experiment/{experiment_uuid}/config/{module_name}/file/{filename}")
def config_file(
    experiment_uuid: str,
    module_name: str,
    filename: str,
    meta: FileUploadMeta = None,
    file: UploadFile = File(...)
):
    
    if Path(file).suffix != ".stl":
        return {"status": status_types.ModuleStatus.TERMINATED.value}
    
    # Deposit .stl file in the experiment directory
    pass

    return {"status":status_types.ModuleStatus.PROPOSED.value}