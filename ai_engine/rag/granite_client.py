import os
from dotenv import load_dotenv
from shared.utils import log
from ibm_watsonx_ai.foundation_models import ModelInference

# Load environment variables
load_dotenv()


class GraniteClient:

    def __init__(self):
        self.api_key = os.getenv("IBM_API_KEY")
        self.project_id = os.getenv("IBM_PROJECT_ID")
        self.url = os.getenv("IBM_URL")

        # VALIDATION
        if not self.api_key or not self.project_id or not self.url:
            raise ValueError(
                "Missing IBM credentials. Please check your .env file:\n"
                "IBM_API_KEY, IBM_PROJECT_ID, IBM_URL"
            )

        try:
            self.model = ModelInference(
                model_id="ibm/granite-8b-code-instruct",
                credentials={
                    "apikey": self.api_key,
                    "url": self.url
                },
                project_id=self.project_id
            )
        except Exception as e:
            log(f"Failed to initialize Granite model: {e}")
            raise

    def generate(self, prompt: str):
        try:
            response = self.model.generate_text(prompt=prompt)
            return response
        except Exception as e:
            log(f"LLM generation failed: {e}")
            return "Error generating response."