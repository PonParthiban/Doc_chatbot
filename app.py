"""
FastAPI application for RAG API
Main entry point for the production backend
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from config import Config
from models import AskRequest, AskResponse, SourceMetadata, ErrorResponse
from rag_engine import initialize_rag_engine, get_rag_engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown
    Initialize RAG engine on startup
    """
    logger.info("Application starting...")
    try:
        initialize_rag_engine()
        logger.info("Application ready to handle requests")
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        raise
    
    yield
    
    logger.info("Application shutting down...")


# Create FastAPI app with lifespan
app = FastAPI(
    title="RAG API",
    description="Production-ready RAG backend using LlamaIndex",
    version="1.0.0",
    lifespan=lifespan,
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "RAG API"}


@app.post(
    "/ask",
    response_model=AskResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def ask_question(request: AskRequest) -> AskResponse:
    """
    Query the RAG engine with a question
    
    Args:
        request: AskRequest with 'question' field
        
    Returns:
        AskResponse with 'answer' and 'sources' fields
        
    Raises:
        HTTPException: On validation or processing errors
    """
    try:
        # Get RAG engine
        rag_engine = get_rag_engine()
        
        if not rag_engine.query_engine:
            logger.error("RAG engine not initialized")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="RAG engine not initialized. Please try again later.",
                headers={"X-Error-Code": "ENGINE_NOT_READY"},
            )

        # Query RAG engine
        answer, sources = rag_engine.query(request.question)

        # Build response with source metadata
        source_metadata = [
            SourceMetadata(file=source["file"], score=source["score"])
            for source in sources
        ]

        response = AskResponse(answer=answer, sources=source_metadata)
        logger.info(f"Request processed successfully. Answer length: {len(answer)}")
        return response

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
            headers={"X-Error-Code": "VALIDATION_ERROR"},
        )
    
    except Exception as e:
        logger.error(f"Unexpected error in /ask endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request.",
            headers={"X-Error-Code": "INTERNAL_ERROR"},
        )


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "service": "RAG API",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health",
            "ask": "POST /ask",
            "docs": "GET /docs",
        },
    }


# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with proper formatting"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": exc.headers.get("X-Error-Code", "UNKNOWN") if exc.headers else "UNKNOWN",
        },
    )


# ========================================
# Static Files (Frontend)
# ========================================

# Mount static files directory to serve frontend
# This must be mounted after all other routes to avoid conflicts
current_dir = Path(__file__).parent
static_dir = current_dir

# Check if frontend files exist
if (static_dir / "index.html").exists():
    app.mount(
        "/",
        StaticFiles(directory=str(static_dir), html=True),
        name="static",
    )
    logger.info(f"✓ Static files mounted from {static_dir}")
else:
    logger.warning(f"Frontend files not found in {static_dir}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=Config.API_RELOAD,
        log_level="info",
    )
