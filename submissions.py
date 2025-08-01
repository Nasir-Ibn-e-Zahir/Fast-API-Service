from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import os

router = APIRouter()

PDF_FOLDER_BASE = "../edu_pilot/public/pdf_files"

class SubmissionItem(BaseModel):
    id: str
    name: str

class SubmissionRequest(BaseModel):
    submissionIds: List[SubmissionItem]

@router.post("/get-user-files")
async def get_user_files(data: SubmissionRequest):
    result = []

    for item in data.submissionIds:
        sub_id = item.id
        sub_name = item.name
        folder_path = os.path.join(PDF_FOLDER_BASE, sub_id)
        if os.path.exists(folder_path):
            files = [
                f for f in os.listdir(folder_path)
                if f.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg', '.webp'))
            ]
            result.append({
                "submissionName": sub_name,
                "submissionId": sub_id,
                "files": [f"/pdf_files/{sub_id}/{file}" for file in files]
            })

    return {"submissions": result}
