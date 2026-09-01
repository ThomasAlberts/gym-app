from sqlalchemy.orm import Session
from config import settings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from prompts import INITIAL_PROMPT

class AIGenerator:

    @classmethod
    def _get_llm(cls):
        return ChatOpenAI(model="gpt-4-turbo")

    @classmethod
    def generate_exercise_suggestion(cls, response: str):
        instance = cls._get_llm()
        exercise_suggestion_format = "stop hier format van hoe je je response wil ontvangen"

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                INITIAL_PROMPT
            ),
            (
                "human",
                f"zet hier de input van gebruiker"
            )
        ]).partial(format_instructions=exercise_suggestion_format)

        raw_response = instance.invoke(prompt.invoke({}))

        response_text = raw_response
        if hasattr(raw_response, "content"):
            response_text = raw_response.content

        # voeg code toe als je de text wil opslaan in een chat of iets
        # of parse de text / geef structuur op een bepaalde manier

        return response_text