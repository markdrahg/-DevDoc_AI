from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from ai_engine.database.db import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    repo_id = Column(String)
    file_path = Column(String)
    content = Column(Text)

    chunks = relationship("Chunk", back_populates="document")


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)
    repo_id = Column(String)
    document_id = Column(Integer, ForeignKey("documents.id"))
    content = Column(Text)
    embedding = Column(Text)

    document = relationship("Document", back_populates="chunks")