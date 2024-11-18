from sqlalchemy import Column, Integer, String, Text, JSON, TIMESTAMP
from app.models.database import Base
from datetime import datetime

class Document(Base):
    __tablename__ = "documents"  # Table name must match your desired structure

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    file_url = Column(String, nullable=True)
    parsed_content = Column(Text, nullable=False)
    metadata_content = Column(JSON, nullable=True)
    uploaded_at = Column(TIMESTAMP, default=datetime.utcnow)
