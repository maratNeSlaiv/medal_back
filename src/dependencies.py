from fastapi import HTTPException, Header
from src.supabase_client import supabase

async def get_current_user(authorization: str = Header(...)):
    # Берём токен из заголовка
    token = authorization.split("Bearer ")[-1]
    
    # Проверяем токен через Supabase Auth
    user_resp = supabase.auth.get_user(token)
    
    if not user_resp or not user_resp.user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Возвращаем объект пользователя для endpoint
    return user_resp.user
