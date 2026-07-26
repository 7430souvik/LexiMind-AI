import json

class PromptService:

    @staticmethod
    def legal_analysis_prompt(document: str) -> str:

        schema = {
            "summary": "",
            "important_clauses": [],
            "risks": [],
            "obligations": [],
            "missing_terms": []
        }

        return f"""
You are an expert legal assistant.

Analyze the following legal document.

Return ONLY valid JSON.

The JSON must match this schema:

{json.dumps(schema, indent=2)}

Document:

{document}
"""