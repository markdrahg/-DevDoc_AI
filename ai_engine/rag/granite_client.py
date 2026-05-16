import os
from dotenv import load_dotenv
from typing import Any
from ibm_watsonx_ai.foundation_models import Model

load_dotenv()


class GraniteClient:

    def __init__(self) -> None:
        self.model = Model(
            model_id="ibm/granite-8b-code-instruct",
            credentials={
                "apikey": os.getenv("IBM_API_KEY"),
                "url": os.getenv("IBM_URL"),
            },
            project_id=os.getenv("IBM_PROJECT_ID"),
        )

    def generate(self, prompt: str) -> str:
        try:
            response: Any = self.model.generate(
                prompt=prompt,
                params={
                    "max_new_tokens": 800,
                    "temperature": 0.3
                }
            )

            return response["results"][0]["generated_text"]

        except Exception as e:
            return f"Error: {str(e)}"