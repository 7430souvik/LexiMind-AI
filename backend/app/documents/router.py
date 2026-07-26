import os
import shutil
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.services.llm_service import LLMService

from app.services.pdf_service import extract_text_from_pdf
from app.services.text_chunker import chunk_text
from app.services.document_service import DocumentService
from app.schemas.analysis import AnalysisResponse
from app.models.document_analysis import DocumentAnalysis
from app.services.analysis_services import AnalysisService
from fastapi import BackgroundTasks
from app.services.chat_service import ChatService
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

llm =   LLMService()

document_service = DocumentService()

analysis_service = AnalysisService()

# @router.post("/upload")
# def upload_document(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     if file.content_type != "application/pdf":
#         raise HTTPException(
#             status_code= 400,
#             detail="Only PDF files are allowed",
#         )
    
#     file_extension = file.filename.split(".")[-1]

#     unique_filename = f"{uuid.uuid4()}.{file_extension}"

#     UPLOAD_DIR = "uploads"

#     os.makedirs(UPLOAD_DIR, exist_ok=True)

#     file_path= os.path.join(
#         UPLOAD_DIR,
#         unique_filename,
#     )

#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     file_size = os.path.getsize(file_path)

#     document = Document(
#         title=file.filename,
#         filename= unique_filename,
#         file_path= file_path,
#         file_size= file_size,
#         status="uploaded",
#         owner_id= current_user.id,
#     )

#     db.add(document)
#     db.commit()
#     db.refresh(document)

#     text = extract_text_from_pdf(file_path)

#     chunks = chunk_text(text)

#     if chunks:
#         analysis = llm.analyze_chunk(chunks[0])

#         print("=" * 60)
#         print("LLM OUTPUT")
#         print("=" * 60)
#         print(analysis)
#         print("=" * 60)
#     else:
#         print("No text extracted.")

    
#     return{
#         "message": "Valid PDF received",
#         "filename": file.filename,
#         "generated_filename": unique_filename,
#         "content_type": file.content_type,
#         "file_path": file_path,
#     }

@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed",
        )

    document = document_service.upload_document(
        file=file,
        current_user=current_user,
        db=db,
    )

    return document

@router.get("", response_model=list[DocumentResponse])
def get_documents(
    db: Session = Depends(get_db),
    current_user: User= Depends(get_current_user),

):
    documents=(
        db.query(Document)
        .filter(Document.owner_id == current_user.id)
        .all()
    )
    return documents

@router.get("/{document_id}", response_model= DocumentResponse)
def get_document(
    document_id: int,
    db: Session= Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document= (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.owner_id == current_user.id,


        )
        .first()
    )
    if document is None:
        raise HTTPException(
            status_code=404,
            detail= "Document not found.",
        )
    return document

@router.post("/{document_id}/analyze")
def analyze_document(
    document_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.owner_id == current_user.id,
        )
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    background_tasks.add_task(
    analysis_service.analyze_document,
    db,
    document,
    )

    return {
    "message": "Analysis started",
    "document_id": document.id,
    }

@router.get(
    "/{document_id}/analysis",
    response_model=AnalysisResponse,
)
def get_analysis(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify document ownership
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.owner_id == current_user.id,
        )
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    analysis = (
        db.query(DocumentAnalysis)
        .filter(
            DocumentAnalysis.document_id == document_id
        )
        .first()
    )

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not ready.",
        )

    return AnalysisResponse(**analysis.analysis)

@router.post(
    "/{document_id}/chat",
    response_model=ChatResponse,
)
def chat_with_document(
    document_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.owner_id == current_user.id,
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return ChatService.ask_question(
        db=db,
        document_id=document_id,
        question=request.question,
    )
