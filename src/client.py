import os
from dotenv import load_dotenv
from pageindex import PageIndexClient
from google import genai

load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# The doc_id of your already-uploaded PDF
DOC_ID = "pi-cmnle3q4m0hxq01qps355ctgo"

# Clients
pi_client = PageIndexClient(api_key=PAGEINDEX_API_KEY)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)
