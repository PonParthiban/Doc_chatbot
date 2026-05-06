"""
RAG Engine module
Handles document loading, index building, persistence, and querying
"""

import logging
from pathlib import Path
from typing import List, Tuple, Optional

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI

from config import Config

logger = logging.getLogger(__name__)


class RAGEngine:
    """RAG (Retrieval-Augmented Generation) Engine with index persistence"""

    def __init__(self):
        """Initialize RAG engine with configuration"""
        self.config = Config
        self.index: Optional[VectorStoreIndex] = None
        self.query_engine = None
        self._setup_llm_and_embeddings()

    def _setup_llm_and_embeddings(self):
        """Configure LLM and embedding models"""
        logger.info("Setting up LLM and embedding models...")

        # Configure LLM (HuggingFace Inference API)
        Settings.llm = HuggingFaceInferenceAPI(
            model_name=self.config.MODEL_ID,
            token=self.config.HF_TOKEN,
            max_new_tokens=self.config.LLM_MAX_TOKENS,
            temperature=self.config.LLM_TEMPERATURE,
        )

        # Configure Embedding Model (runs locally for efficiency)
        Settings.embed_model = HuggingFaceEmbedding(
            model_name=self.config.EMBEDDING_MODEL
        )

        logger.info(f"✓ LLM: {self.config.MODEL_ID}")
        logger.info(f"✓ Embedding: {self.config.EMBEDDING_MODEL}")

    def _load_documents(self) -> List:
        """Load PDF documents from data directory"""
        logger.info(f"Loading documents from {self.config.DATA_DIR}...")
        
        reader = SimpleDirectoryReader(
            input_dir=str(self.config.DATA_DIR),
            required_exts=[".pdf"],
            recursive=True,
        )
        docs = reader.load_data()
        logger.info(f"✓ Loaded {len(docs)} documents")
        return docs

    def _build_index(self, docs: List) -> VectorStoreIndex:
        """Build vector index from documents using semantic chunking"""
        logger.info("Building vector index with semantic chunking...")

        # Create semantic node parser
        parser = SemanticSplitterNodeParser(
            embed_model=Settings.embed_model,
            breakpoint_percentile_threshold=self.config.BREAKPOINT_PERCENTILE_THRESHOLD,
        )
        nodes = parser.get_nodes_from_documents(docs)
        logger.info(f"✓ Created {len(nodes)} semantic chunks")

        # Build and persist index
        index = VectorStoreIndex(nodes)
        index.storage_context.persist(str(self.config.STORAGE_DIR))
        logger.info(f"✓ Index persisted to {self.config.STORAGE_DIR}")

        return index

    def _load_or_build_index(self) -> VectorStoreIndex:
        """Load existing index or build new one"""
        index_path = self.config.STORAGE_DIR / "docstore.json"

        # Try to load existing index
        if index_path.exists():
            try:
                logger.info(f"Loading existing index from {self.config.STORAGE_DIR}...")
                storage_context = StorageContext.from_defaults(
                    persist_dir=str(self.config.STORAGE_DIR)
                )
                index = load_index_from_storage(storage_context)
                logger.info("✓ Index loaded successfully")
                return index
            except Exception as e:
                logger.warning(f"Failed to load existing index: {e}. Rebuilding...")

        # Build new index
        docs = self._load_documents()
        if not docs:
            raise ValueError(f"No documents found in {self.config.DATA_DIR}")
        
        return self._build_index(docs)

    def initialize(self):
        """Initialize RAG engine (called on startup)"""
        logger.info("=" * 60)
        logger.info("Initializing RAG Engine...")
        logger.info("=" * 60)

        try:
            self.index = self._load_or_build_index()
            self.query_engine = self.index.as_query_engine(
                similarity_top_k=self.config.SIMILARITY_TOP_K,
                response_mode="compact",
            )
            logger.info("=" * 60)
            logger.info("✓ RAG Engine initialized successfully!")
            logger.info("=" * 60)
        except Exception as e:
            logger.error(f"Failed to initialize RAG Engine: {e}", exc_info=True)
            raise

    def query(self, question: str) -> Tuple[str, List[dict]]:
        """
        Query the RAG engine
        
        Args:
            question: User question
            
        Returns:
            Tuple of (answer, sources) where sources is list of dicts with 'file' and 'score'
        """
        if not self.query_engine:
            raise RuntimeError("RAG Engine not initialized. Call initialize() first.")

        logger.info(f"Query: {question}")

        try:
            response = self.query_engine.query(question)
            
            # Extract answer
            answer = str(response)

            # Extract sources with scores
            sources = []
            if response.source_nodes:
                for node in response.source_nodes:
                    file_name = node.metadata.get("file_name", "Unknown")
                    score = float(node.score) if node.score is not None else 0.0
                    sources.append({"file": file_name, "score": score})

            logger.info(f"✓ Query successful. Sources: {len(sources)}")
            return answer, sources

        except Exception as e:
            logger.error(f"Query failed: {e}", exc_info=True)
            raise


# Global RAG engine instance
_rag_engine = None


def get_rag_engine() -> RAGEngine:
    """Get or create RAG engine instance (singleton)"""
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine()
    return _rag_engine


def initialize_rag_engine():
    """Initialize RAG engine on startup"""
    engine = get_rag_engine()
    engine.initialize()
