from pydantic import BaseModel, Field
from typing import Optional

class RecipeRequest(BaseModel):
    dish_name: str = Field(..., description="Name of the dish")
    purpose: Optional[str] = Field(None, description="Purpose of the recipe, e.g., 'weight loss'")
    servings: Optional[int] = Field(None, description="Number of servings")
    cuisine: Optional[str] = Field(None, description="Cuisine type")
    dietary_restrictions: Optional[str] = Field(None, description="Dietary restrictions")
    max_cook_time: Optional[int] = Field(None, description="Maximum cooking time in minutes")
    include_macros: Optional[bool] = Field(False, description="Include macros (protein, carbs, fats)")

class RecipeResponse(BaseModel):
    ingredients: list[str]
    steps: list[str]
    time_minutes: Optional[int]
    servings: Optional[int]
    macros: Optional[dict]

class RecipeWithImageResponse(BaseModel):
    dish_name: str
    recipe: RecipeResponse
    image_url: Optional[str]
