from fastapi import APIRouter, HTTPException, Depends
from .services import generate_recipe, get_dish_image_url
from .schemas import RecipeRequest, RecipeWithImageResponse
from src.core_functions import require_user

router = APIRouter(
    prefix="/diet",
    tags=["diet"]
)

@router.post("/recipe_with_image", response_model=RecipeWithImageResponse)
async def recipe_with_image_endpoint(
    request: RecipeRequest,
    # user=Depends(require_user),
):
    """
    Generate a recipe and fetch the dish image in a single endpoint.
    """
    try:
        # 1.
        print("We went over here # 1")
        recipe = generate_recipe(
            dish_name=request.dish_name,
            purpose=request.purpose,
            servings=request.servings,
            cuisine=request.cuisine,
            dietary_restrictions=request.dietary_restrictions,
            max_cook_time=request.max_cook_time,
            include_macros=request.include_macros,
        )

        # 2.
        print("We went over it")
        image_url = get_dish_image_url(request.dish_name)

        # 3.
        return RecipeWithImageResponse(
            dish_name=request.dish_name,
            recipe=recipe,
            image_url=image_url,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
