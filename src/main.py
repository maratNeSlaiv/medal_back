from fastapi import FastAPI, Depends
from src.auth.routes import router as auth_router
from src.ai.routes import router as ai_router
from src.diet.routes import router as diet_router
from src.core_functions import require_user

app = FastAPI()

app.include_router(auth_router)
app.include_router(ai_router)
app.include_router(diet_router)

@app.get("/me")
def protected_route(user=Depends(require_user)):
    return {"message": f"Hello {user.email}"}