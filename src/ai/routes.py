from fastapi import APIRouter, Depends, UploadFile, File
from .services import medical_image_analysis

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