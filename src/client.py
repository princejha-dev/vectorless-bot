import os
from dotenv import load_dotenv
from pageindex import PageIndexClient
from groq import Groq

load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# The doc_id of Academic Regulations 2025 PDF
DOC_ID = "pi-cmnllmkvt0kzg01qp2ajbsdcb"

# Clients
pi_client = PageIndexClient(api_key=PAGEINDEX_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)
