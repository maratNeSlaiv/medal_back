from fastapi import APIRouter, Depends, UploadFile, File
import os
from dotenv import load_dotenv
from src.core_functions import require_user
from .services import medical_image_analysis

load_dotenv()
WEB_CLIENT_ID = os.environ.get("WEB_CLIENT_ID")

router = APIRouter(
    prefix="/ai",
    tags=["ai"]
)

@router.post("/process-image")
async def process_image(
    file: UploadFile = File(...),
    # user=Depends(require_user)
):
    summary = await medical_image_analysis(file)
    return {"result": summary}