from fastapi import APIRouter, File, UploadFile, Depends
from src.dependencies import get_current_user
# from src.analyze.utils import extract_text, analyze_text

router = APIRouter()

@router.post("/pdf")
async def analyze_pdf(file: UploadFile = File(...), user=Depends(get_current_user)):
    # читаем PDF и делаем OCR
    # text = await extract_text(file)
    # summary, recommendations = analyze_text(text)
    
    # # сохраняем результат в Supabase
    # from src.supabase_client import supabase
    # pdf_url = f"user_uploads/{user.id}/{file.filename}"
    # supabase.storage.from_("medical_pdfs").upload(pdf_url, file.file)
    # supabase.table("analyses").insert({
    #     "user_id": user.id,
    #     "pdf_url": pdf_url,
    #     "summary": summary,
    #     "recommendations": recommendations
    # }).execute()
    
    # return {"summary": summary, "recommendations": recommendations}
    return {"response" : "100"}
