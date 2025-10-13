from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.supabase_client import supabase
from src.schemas import UserRead

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserRead:
    try:
        user_resp = supabase.auth.get_user(token)
        if user_resp.user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return UserRead(id=user_resp.user.id, email=user_resp.user.email)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
