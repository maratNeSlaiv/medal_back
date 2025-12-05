import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

WEB_CLIENT_ID = os.environ.get("WEB_CLIENT_ID")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

UNSPLASH_URL = "https://api.unsplash.com/search/photos"
LLM_API_URL = "https://apifreellm.com/api/chat"
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
