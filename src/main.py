# main.py
from fastapi import FastAPI
from src.auth.routes import router as auth_router

app = FastAPI(title="Medical PDF Analyzer")

# Подключаем роутер auth
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Можно добавить корневой маршрут для теста
@app.get("/")
def root():
    return {"message": "Server is running"}
