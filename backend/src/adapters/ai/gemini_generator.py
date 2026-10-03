# backend/src/adapters/ai/gemini_generator.py
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.src.domain.errors import AiGenerationFailed


class GeminiTextGenerator:
    def __init__(self, api_key: str, model: str = "gemini-flash-latest"):
        self._llm = ChatGoogleGenerativeAI(model=model, google_api_key=api_key)

    def generate(self, prompt: str) -> str:
        try:
            content = self._llm.invoke(prompt).content
        except Exception as e:
            raise AiGenerationFailed(str(e)) from e
        if isinstance(content, list):
            content = "".join(
                p.get("text", "") if isinstance(p, dict) else str(p) for p in content
            )
        return content