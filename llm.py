from dotenv import load_dotenv
from langchain_ollama import ChatOllama
import os

# Load environment variables
load_dotenv()

llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL"),
    base_url=os.getenv("OLLAMA_BASE_URL"),
    temperature=float(os.getenv("TEMPERATURE", 0))
)