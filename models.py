"""
Pydantic models for API request/response validation
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """Request schema for /ask endpoint"""

    question: str = Field(..., min_length=1, max_length=1000, description="The question to ask")

    class Config:
        json_schema_extra = {
            "example": {"question": "What are the main topics covered in the documents?"}
        }


class SourceMetadata(BaseModel):
    """Source document metadata in response"""

    file: str = Field(..., description="Source file name")
    score: float = Field(..., ge=0.0, le=1.0, description="Relevance score (0-1)")

    class Config:
        json_schema_extra = {"example": {"file": "document.pdf", "score": 0.95}}


class AskResponse(BaseModel):
    """Response schema for /ask endpoint"""

    answer: str = Field(..., description="Generated answer from RAG pipeline")
    sources: List[SourceMetadata] = Field(default_factory=list, description="Source documents")

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "The documents cover machine learning, deep learning, and NLP.",
                "sources": [
                    {"file": "ml_guide.pdf", "score": 0.98},
                    {"file": "deep_learning.pdf", "score": 0.94},
                ],
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema"""

    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")

    class Config:
        json_schema_extra = {"example": {"detail": "Invalid question", "error_code": "INVALID_INPUT"}}
