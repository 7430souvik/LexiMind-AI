from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import EmbeddingService


class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    def retrieve_chunks(
        self,
        db: Session,
        document_id: int,
        question: str,
        limit: int = 5,
    ) -> list[DocumentChunk]:
        """
        Retrieve the most semantically similar chunks
        from a document using pgvector cosine similarity.
        """

        question_embedding = self.embedding_service.embed_text(
            question
        )

        chunks = (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id == document_id
            )
            .order_by(
                DocumentChunk.embedding.cosine_distance(
                    question_embedding
                )
            )
            .limit(limit)
            .all()
        )

        return chunks