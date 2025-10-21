from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from fastapi import APIRouter, HTTPException
from src.schemas import (
    UserCreate, UserLogin, UserRead, TokenResponse,
    ForgotPasswordRequest, ResetPasswordRequest, GoogleAuthRequest
)
from src.supabase_client import supabase
from supabase_auth.errors import AuthApiError
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
load_dotenv()
WEB_CLIENT_ID = os.environ.get("WEB_CLIENT_ID")

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
        if "already been registered" in str(e):
            return JSONResponse(
                status_code=409,
                content={"message": "Email has already been registered"}
            )
        else:
            raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
    except AuthApiError as e:
        print(e)
        if "Invalid login credentials" in str(e):
            return JSONResponse(
                status_code=401,
                content={"message": "Invalid email or password"}
            )
        elif "Email not confirmed" in str(e):
            return JSONResponse(
                status_code=401,
                content={"message": "Email is not confirmed."}
            )
        else:
            raise HTTPException(status_code=500, detail="Authentication failed")

    if not res.user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return TokenResponse(access_token=res.session.access_token)


@router.post("/forgot-password")
def forgot_password(req: ForgotPasswordRequest):
    try:
        supabase.auth.reset_password_for_email(req.email)
        return JSONResponse(
                status_code=200,
                content={"message": "Password reset email sent"}
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reset-password")
def reset_password(req: ResetPasswordRequest):
    try:
        supabase.auth.update_user(
            {"password": req.new_password},
            access_token=req.access_token
        )
        return JSONResponse(
                status_code=200,
                content={"message": "Password updated successfully"}
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/google")
async def google_login(body: GoogleAuthRequest):
    try:
        # Google token check
        idinfo = id_token.verify_oauth2_token(
            body.idToken, grequests.Request(), WEB_CLIENT_ID
        )
        email = idinfo.get("email")

        if not email:
            return JSONResponse(
                status_code=400,
                content={"message": "Email is required"}
            )

        # Search for user in Supabase Auth
        user_resp = supabase.auth.admin.list_users({"email": email})
        users = user_resp.data

        if users:
            user = users[0]
        else:
            # Create new user
            new_user_resp = supabase.auth.admin.create_user({
                "email": email,
                "email_confirm": True
            })
            user = new_user_resp.user

        return {"success": True, "user": user}

    except ValueError:
        return JSONResponse(
                status_code=400,
                content={"message": "Invalid ID token"}
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))