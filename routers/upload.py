from fastapi import APIRouter, File, Depends

from typing import Annotated

from fastapi import Form, UploadFile

from services.upload import Upload
from utils.middleware import JWTBearer

router = APIRouter(dependencies=[Depends(JWTBearer())])


@router.post(
    '/',
    description='upload data with various sources',
    name='upload-data',
)
async def upload_data(user_id: str,
                      username: str,
                      data: Annotated[str, Form()] = None,
                      file_b: Annotated[UploadFile, File()] = None):
    upload = Upload()
    response = await upload.upload_data(username, user_id, file_b, data)
    return response
