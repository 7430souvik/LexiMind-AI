from pydantic import BaseModel


class AnalysisResponse(BaseModel):
    summary: str
    important_clauses: list[str]
    risks: list[str]
    obligations: list[str]
    missing_terms: list[str]