from fastapi import APIRouter, HTTPException, Depends
from src.auth.schemas import RegisterModel, LoginModel
from src.supabase_client import supabase
from src.dependencies import get_current_user

router = APIRouter()

@router.post("/register")
async def register(user: RegisterModel):
    resp = supabase.auth.sign_up({
        "email": user.email,
        "password": user.password
    })

    if not resp.user:
        raise HTTPException(status_code=400, detail="Не удалось создать пользователя")

    return {"message": "Пользователь зарегистрирован. Подтвердите email."}


@router.post("/login")
async def login(user: LoginModel):
    resp = supabase.auth.sign_in_with_password({
        "email": user.email,
        "password": user.password
    })

    if not resp.session:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    return {"access_token": resp.session.access_token}


# --- Пример защищённого роутера ---
@router.get("/protected")
async def protected_route(user=Depends(get_current_user)):
    return {"message": f"Привет, {user.email}!", "user_id": user.id}
