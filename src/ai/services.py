from fastapi import UploadFile, File
from PIL import Image
import io
import pytesseract
import httpx
import json
from PIL import Image, UnidentifiedImageError

import torch
from src.model_loader import ModelRegistry

def ocr_image(img: Image.Image) -> str:
    img = img.convert("RGB")
    return pytesseract.image_to_string(img, lang='eng')

async def generate_summary(text: str) -> str:
    if not text.strip():
        return ""
    
    url = "https://apifreellm.com/api/chat"
    headers = {"Content-Type": "application/json"}
    data = {
        "message": f"Analyze the following medical text and summarize the main points:\n{text}"
    }
    
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.post(url, headers=headers, json=data)

            # безопасное преобразование ответа в JSON
            try:
                result = response.json()
            except json.JSONDecodeError:
                return f"Error: invalid JSON response from AI API: {response.text}"

            if result.get("status") == "success":
                return result["response"]
            else:
                return f"Error from AI API: {result.get('error', 'unknown error')}"
        except Exception as e:
            return f"Error calling AI API: {str(e)}"

async def medical_image_analysis(file: UploadFile = File(...)) -> str:
    file_bytes = await file.read()
    img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    extracted_text = ocr_image(img)
    summary = await generate_summary(extracted_text)
    return summary

async def skin_lesion_classification(file: UploadFile) -> tuple[str, float]:
    img_bytes = await file.read()
    if not img_bytes:
        return {"error": "Empty file"}

    try:
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    except (UnidentifiedImageError, OSError) as e:
        return {"error": "Cannot open image, invalid format"}
    
    try:
        inputs = ModelRegistry.melanoma_processor(images=image, return_tensors="pt")
        inputs = {k: v.to(ModelRegistry.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = ModelRegistry.melanoma_model(**inputs)

        logits = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=1)[0]

        predicted_idx = torch.argmax(probabilities).item()
        predicted_class = ModelRegistry.melanoma_model.config.id2label[predicted_idx]
        confidence = probabilities[predicted_idx].item()
        return predicted_class, confidence

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
