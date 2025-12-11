from pydantic import BaseModel

class SkinLesionPredictionResponse(BaseModel):
    predicted_class: str
    confidence: float