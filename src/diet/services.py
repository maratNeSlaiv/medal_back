import requests
from PIL import Image
from io import BytesIO
import re
import json
from src.settings import UNSPLASH_URL, LLM_API_URL, UNSPLASH_ACCESS_KEY

def build_prompt(
    dish_name: str,
    purpose: str = None,
    servings: int = None,
    cuisine: str = None,
    dietary_restrictions: str = None,
    max_cook_time: int = None,
    include_macros: bool = True
) -> str:
    """Construct a dynamic prompt for the LLM."""
    prompt_lines = [f'Generate a recipe for "{dish_name}".']

    if purpose:
        prompt_lines.append(f"Purpose: {purpose}.")
    if servings:
        prompt_lines.append(f"Number of servings: {servings}.")
    if cuisine:
        prompt_lines.append(f"Cuisine: {cuisine}.")
    if dietary_restrictions:
        prompt_lines.append(f"Dietary restrictions: {dietary_restrictions}.")
    if max_cook_time:
        prompt_lines.append(f"Max cooking time: {max_cook_time} minutes.")
    if include_macros:
        prompt_lines.append("Include approximate macros (protein, carbs, fats).")

    prompt_lines.append(
        "Follow this format strictly:\n"
        "Ingredients:\n- item (quantity)\n"
        "Steps:\n1. Step one\n2. Step two\n"
        "Time: X minutes\nServings: X\nMacros: protein Xg, carbs Xg, fats Xg"
    )
    return "\n".join(prompt_lines)

def call_llm_api(prompt: str) -> str:
    """Send the prompt to the LLM API, log raw response, and return the text."""
    response = requests.post(LLM_API_URL, headers={"Content-Type": "application/json"}, json={"message": prompt})
    
    try:
        result = response.json()
    except json.JSONDecodeError:
        print(f"[LLM RAW RESPONSE]: {response.text}")
        return f"Error: invalid JSON response from AI API: {response.text}"

    if result.get("status") == "success":
        raw_text = result["response"]
        print(f"[LLM RAW RESPONSE]: {raw_text}")
        return raw_text
    else:
        print(f"[LLM RAW RESPONSE]: {result}")
        raise RuntimeError(f"LLM API error: {result.get('error')}")

def extract_recipe_adaptive(text: str) -> dict:
    """Adaptive parser for LLM-generated recipes. Extracts ingredients, steps, time, servings, macros."""
    recipe = {}

    # --- Ingredients ---
    ing_match = re.search(
        r"(?:\*+)?ingredients(?:\*+)?\s*:\s*(.*?)(?=\n(?:\*+)?steps(?:\*+)?\s*:|\Z)", 
        text, re.S | re.I
    )
    ingredients = []
    if ing_match:
        for line in ing_match.group(1).splitlines():
            line = line.strip()
            if not line:
                continue
            line = re.sub(r"^[\-\*\•\s]+", "", line)
            if line:
                ingredients.append(line)
    recipe["ingredients"] = ingredients

    # --- Steps ---
    steps_match = re.search(
        r"(?:\*+)?steps(?:\*+)?\s*:\s*(.*?)(?=\n(?:\*+)?time|"
        r"\n(?:\*+)?servings|"
        r"\n(?:\*+)?macros|\Z)", 
        text, re.S | re.I
    )
    steps = []
    if steps_match:
        for line in steps_match.group(1).splitlines():
            line = line.strip()
            if not line:
                continue
            line = re.sub(r"^\d+[\.\)\-]?\s*", "", line)
            if line:
                steps.append(line)
    recipe["steps"] = steps

    # --- Time ---
    time_match = re.search(
        r"(?:\*+)?(?:time|total time)(?:\*+)?\s*:\s*(\d+)", text, re.I
    )
    recipe["time_minutes"] = int(time_match.group(1)) if time_match else None

    # --- Servings ---
    servings_match = re.search(
        r"(?:\*+)?servings(?:\*+)?\s*:\s*(\d+)", text, re.I
    )
    recipe["servings"] = int(servings_match.group(1)) if servings_match else None

    # --- Macros ---
    macros_match = re.search(
        r"(?:\*+)?macros(?:\*+)?\s*:\s*"
        r"protein\s*(\d+)g\s*,?\s*"
        r"carbs\s*(\d+)g\s*,?\s*"
        r"fats\s*(\d+)g", text, re.I
    )
    if macros_match:
        recipe["macros"] = {
            "protein": int(macros_match.group(1)),
            "carbs": int(macros_match.group(2)),
            "fats": int(macros_match.group(3))
        }
    else:
        macro_alt = re.findall(r"(?:protein|carbs|fats)\s*(\d+)g", text, re.I)
        if len(macro_alt) == 3:
            recipe["macros"] = {"protein": int(macro_alt[0]), "carbs": int(macro_alt[1]), "fats": int(macro_alt[2])}
        else:
            recipe["macros"] = None

    return recipe

def generate_recipe(
    dish_name: str,
    purpose: str = None,
    servings: int = None,
    cuisine: str = None,
    dietary_restrictions: str = None,
    max_cook_time: int = None,
    include_macros: bool = None
) -> dict:
    """Main function: generates a structured recipe for a single dish."""
    prompt = build_prompt(dish_name, purpose, servings, cuisine, dietary_restrictions, max_cook_time, include_macros)
    raw_text = call_llm_api(prompt)
    recipe = extract_recipe_adaptive(raw_text)
    return recipe

def get_dish_image_url(dish_name: str) -> str | None:
    """
    Fetches a dish image URL from Unsplash.
    Returns None if no image is found.
    """
    params = {
        "query": dish_name,
        "per_page": 1,
        "client_id": UNSPLASH_ACCESS_KEY
    }
    response = requests.get(UNSPLASH_URL, params=params).json()
    
    if response.get('results'):
        return response['results'][0]['urls']['regular']
    else:
        print(f"Image for '{dish_name}' not found.")
        return "https://cdn-icons-png.freepik.com/512/1046/1046874.png"
