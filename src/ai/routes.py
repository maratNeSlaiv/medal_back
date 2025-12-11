from fastapi import APIRouter, Depends, UploadFile, File
from .services import medical_image_analysis, skin_lesion_classification
from .schemas import SkinLesionPredictionResponse
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/ai",
    tags=["ai"]
)

@router.post("/process-image")
async def process_image(
    file: UploadFile = File(...),
    # user=Depends(require_user)
    ):
    print("We received medical image analysis request")
    summary = await medical_image_analysis(file)
    print(summary)
    return {"summary": summary}

@router.post("/skin_lesion", response_model=SkinLesionPredictionResponse)
async def skin_lesion(
    file: UploadFile = File(...),
    # user=Depends(require_user)
    ):
    try:
        predicted_class, confidence = await skin_lesion_classification(file)
        return SkinLesionPredictionResponse(predicted_class=predicted_class, confidence=confidence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))