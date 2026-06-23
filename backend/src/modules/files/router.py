from fastapi import APIRouter, Depends, status

from src.modules.files.facades.delete_file import delete_file
from src.modules.files.facades.get_file import get_file
from src.modules.files.facades.upload_files import upload_files
from src.modules.files.schemas import FileInfoResponse, FileUploadResponse

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_endpoint(result: FileUploadResponse = Depends(upload_files)):
    return result


@router.get("/{file_id}", response_model=FileInfoResponse)
async def get_endpoint(result: FileInfoResponse = Depends(get_file)):
    return result


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_endpoint(_: None = Depends(delete_file)):
    return None
