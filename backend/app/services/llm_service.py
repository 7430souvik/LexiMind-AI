from groq import Groq, APIError
import json
import re

from app.core.config import get_settings
from app.services.prompt_service import PromptService
from app.schemas.analysis import AnalysisResponse


class LLMService:

    def __init__(self):
        settings = get_settings()

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model_name = "llama-3.3-70b-versatile"

    def analyze_chunk(self, chunk: str) -> dict:
        prompt = PromptService.legal_analysis_prompt(chunk)

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": """
    You are an intelligent document analysis assistant.

First determine the document type.

Possible types:
- Resume
- Contract
- Invoice
- Research Paper
- Medical Report
- Legal Agreement
- Other

Then analyze the document appropriately.

Return ONLY valid JSON.

{
  "document_type": "",
  "summary": "",
  "important_points": [],
  "risks": [],
  "obligations": [],
  "missing_information": []
}
    """
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.2,
                max_tokens=1000,
            )
            print("Finish reason:", response.choices[0].finish_reason)

            content = response.choices[0].message.content.strip()

            # Remove markdown fences
            content = (
                content.replace("```json", "")
                .replace("```", "")
                .strip()
            )

            # Extract JSON object
            match = re.search(r"\{.*\}", content, re.DOTALL)

            if not match:
                raise Exception(f"No JSON found:\n{content}")

            json_text = match.group(0)

            data = json.loads(json_text)

            return AnalysisResponse(**data)
        except APIError as e:
            raise Exception(f"Groq API Error: {e}")

        except json.JSONDecodeError as e:
            raise Exception(
                f"Model returned invalid JSON:\n{content}"
            ) from e
        # prompt = PromptService.legal_analysis_prompt(chunk)

        # try:
        #     response = self.client.chat.completions.create(
        #         model="llama-3.3-70b-versatile",
        #         messages=[
        #             {
        #                 "role": "user",
        #                 "content": prompt,
        #             }
        #         ],
        #         temperature=0.2,
        #         max_tokens=1000,
        #     )

        #     content = response.choices[0].message.content

        #     return json.loads(content)

        # except APIError as e:
        #     raise Exception(f"Groq API Error: {e}")

        # except json.JSONDecodeError:
        #     raise Exception("The model did not return valid JSON.")


    def answer_question(
    self,
    context: str,
    question: str,
    ) -> str:

        prompt = f"""
    You are an expert legal AI assistant.

    Answer ONLY using the provided context.

    If the answer cannot be found in the context,
    reply exactly:

    "I couldn't find that information in the document."

    Context:

    {context}

    Question:

    {question}

    Answer:
    """

        completion = self.client.chat.completions.create(
            model=self.model_name,
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return completion.choices[0].message.content.strip()