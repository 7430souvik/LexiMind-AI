import os
import shutil
import uuid

from fastapi import UploadFile
from sqlalchemy.orm  import Session

from app.models.document import Document
from app.models.user import User

class DocumentService:

    def upload_document(
        self,
        file: UploadFile,
        current_user: User,
        db: Session,
    ) -> Document:

        file_extension = file.filename.split(".")[-1]

        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        upload_dir = "uploads"

        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(
            upload_dir,
            unique_filename,
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size = os.path.getsize(file_path)

        document = Document(
            title=file.filename,
            filename=unique_filename,
            file_path=file_path,
            file_size=file_size,
            status="uploaded",
            owner_id=current_user.id,
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

