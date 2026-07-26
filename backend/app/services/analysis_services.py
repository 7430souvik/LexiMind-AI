from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_analysis import DocumentAnalysis
from app.models.document_chunk import DocumentChunk
from app.schemas.analysis import AnalysisResponse
from app.services.pdf_service import extract_text_from_pdf
from app.services.text_chunker import chunk_text
from app.services.llm_service import LLMService
from app.services.embedding_service import EmbeddingService


class AnalysisService:
    def __init__(self):
        self.llm = LLMService()
        self.embedding_service = EmbeddingService()

    def analyze_document(
    self,
    db: Session,
    document: Document,
    ) -> AnalysisResponse:

        try:
            print("1. Status -> processing")
            document.status = "processing"
            db.commit()

            print("2. Extract text")
            text = extract_text_from_pdf(document.file_path)

            print("3. Chunk")
            chunks = chunk_text(text)
            print(f"Chunks: {len(chunks)}")

            analyses: list[AnalysisResponse] = []

            # Process each chunk
            for index, chunk in enumerate(chunks):

                print(f"Chunk {index + 1}/{len(chunks)}")

                embedding = self.embedding_service.embed_text(chunk)

                chunk_record = DocumentChunk(
                    document_id=document.id,
                    chunk_index=index,
                    content=chunk,
                    embedding=embedding,
                )

                db.add(chunk_record)
                db.flush()

                analysis = self.llm.analyze_chunk(chunk)
                analyses.append(analysis)

            print("4. Finished chunk loop")

            final_analysis = self.merge_analyses(analyses)

            print("5. Merge complete")

            # Prevent duplicate analysis rows
            existing_analysis = (
                db.query(DocumentAnalysis)
                .filter(
                    DocumentAnalysis.document_id == document.id
                )
                .first()
            )

            if existing_analysis:
                existing_analysis.model_name = "llama-3.3-70b-versatile"
                existing_analysis.analysis = final_analysis.model_dump()
            else:
                analysis_record = DocumentAnalysis(
                    document_id=document.id,
                    model_name="llama-3.3-70b-versatile",
                    analysis=final_analysis.model_dump(),
                )
                db.add(analysis_record)

            print("6. Saving analysis")

            document.status = "completed"

            db.commit()

            print("7. Commit complete")

            return final_analysis

        except Exception as e:
            import traceback

            traceback.print_exc()

            document.status = "failed"
            db.commit()

            print("Analysis failed:", e)

            raise
    def merge_analyses(
        self,
        analyses: list[AnalysisResponse],
    ) -> AnalysisResponse:

        summary = "\n\n".join(
            analysis.summary
            for analysis in analyses
        )

        important_clauses = []
        risks = []
        obligations = []
        missing_terms = []

        for analysis in analyses:
            important_clauses.extend(analysis.important_clauses)
            risks.extend(analysis.risks)
            obligations.extend(analysis.obligations)
            missing_terms.extend(analysis.missing_terms)

        return AnalysisResponse(
            summary=summary,
            important_clauses=list(set(important_clauses)),
            risks=list(set(risks)),
            obligations=list(set(obligations)),
            missing_terms=list(set(missing_terms)),
        )