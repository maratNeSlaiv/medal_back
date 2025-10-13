from fastapi import FastAPI, Depends
from src.routes import router as auth_router
from src.dependencies import get_current_user
from src.schemas import UserRead

app = FastAPI()

app.include_router(auth_router)

@app.get("/me", response_model=UserRead)
def read_me(current_user: UserRead = Depends(get_current_user)):
    return current_user
