from pydantic import BaseModel


class Document(BaseModel):
    doc_ext: str
    doc_content: str
    doc_id: int
    doc_qr_text: str
    api_key: str


class DocumentResponse(BaseModel):
    detail: str
