import datetime
import json
import os
import traceback

from fastapi import HTTPException, status, UploadFile
import aiofiles
from fastapi.responses import JSONResponse

from configs.database import supabase_connection


class Upload:
    def __init__(self):
        self.supabase_client, self._table = supabase_connection()

    async def upload_data(self, username: str, user_id: str, file: UploadFile, data: str):
        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='username or user_id cannot be null',
            )
        if data:
            data, _ = self.supabase_client.table(self._table).insert({
                'user_id': user_id,
                'data': json.loads(data),
                'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }).execute()
        elif file:
            try:
                contents = await file.read()
                filepath = f"./resources/{file.filename}"
                async with aiofiles.open(filepath, 'wb') as f:
                    await f.write(contents)
                with open(filepath, 'rb') as f:
                    self.supabase_client.storage.from_(username).upload(path=f'{file.filename}', file=f)
                os.remove(filepath)
            except Exception:
                traceback.print_exc()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail='There was an error uploading the file',
                )
            finally:
                await file.close()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "upload data success"},
        )
