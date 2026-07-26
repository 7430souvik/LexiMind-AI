from sqlalchemy.orm import Session

from app.schemas.chat import ChatResponse
from app.services.llm_service import LLMService
from app.services.retrieval_services import RetrievalService


class ChatService:

    def __init__(self):
        self.retrieval = RetrievalService()
        self.llm = LLMService()

    def ask_question(
        self,
        db: Session,
        document_id: int,
        question: str,
    ) -> ChatResponse:

        chunks = self.retrieval.retrieve_chunks(
            db=db,
            document_id=document_id,
            question=question,
        )

        context = "\n\n".join(
            chunk.content
            for chunk in chunks
        )

        answer = self.llm.answer_question(
            context=context,
            question=question,
        )

        return ChatResponse(
            answer=answer,
            sources=[
                f"Chunk {chunk.chunk_index}"
                for chunk in chunks
            ],
        )