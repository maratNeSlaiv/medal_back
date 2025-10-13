from fastapi import APIRouter, HTTPException
from src.schemas import (
    UserCreate, UserLogin, UserRead, TokenResponse,
    ForgotPasswordRequest, ResetPasswordRequest
)
from src.supabase_client import supabase

router = APIRouter()


@router.post("/register", response_model=UserRead)
def register(user: UserCreate):
    try:
        res = supabase.auth.admin.create_user({
            "email": user.email,
            "password": user.password
        })
        created_user = res.user
        return UserRead(id=created_user.id, email=created_user.email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    res = supabase.auth.sign_in_with_password({
        "email": user.email,
        "password": user.password
    })
    if res.user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=res.session.access_token)


@router.post("/forgot-password")
def forgot_password(req: ForgotPasswordRequest):
    try:
        supabase.auth.reset_password_for_email(req.email)
        return {"message": "Password reset email sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reset-password")
def reset_password(req: ResetPasswordRequest):
    try:
        supabase.auth.update_user(
            {"password": req.new_password},
            access_token=req.access_token
        )
        return {"message": "Password updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
