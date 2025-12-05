from fastapi import UploadFile, File
from PIL import Image
import io
import pytesseract
import httpx
import json

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
