from fastapi import APIRouter
from pydantic import BaseModel
import os

router = APIRouter()

PDF_FOLDER_BASE = "../edu_pilot/public/pdf_files"

class SubmissionRequest(BaseModel):
    submissionIds: list[str]

@router.post("/get-user-files")
async def get_user_files(data: SubmissionRequest):
    result = []

    for sub_id in data.submissionIds:
        folder_path = os.path.join(PDF_FOLDER_BASE, sub_id)
        if os.path.exists(folder_path):
            files = [
                f for f in os.listdir(folder_path)
                if f.endswith(".pdf") or f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
            ]
            result.append({
                "submissionId": sub_id,
                "files": [f"/pdf_files/{sub_id}/{file}" for file in files]
            })

    print(result)
    return {"submissions": result}
    