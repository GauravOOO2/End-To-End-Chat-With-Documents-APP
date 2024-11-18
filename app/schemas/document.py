from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentBase(BaseModel):
    file_name: str
    file_url: Optional[str] = None
    parsed_content: str
    metadata: Optional[dict] = None  # Logical name remains metadata
    uploaded_at: datetime

    class Config:
        orm_mode = True
