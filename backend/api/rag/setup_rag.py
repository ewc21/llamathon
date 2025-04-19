# setup_rag.py
from llama_stack_client import LlamaStackClient
from llama_stack_client import Document
import uuid
from pathlib import Path
import httpx

client = LlamaStackClient(base_url="http://localhost:8321", timeout=httpx.Timeout(60.0, read=30.0))

# Pick the embed model
embed_model = client.models.list()[0]
embedding_model = embed_model.identifier

vector_db_id = "nutrition-rag"

client.vector_dbs.register(vector_db_id=vector_db_id, embedding_model=embedding_model)

# Load local .txt docs
docs_path = Path("backend/rag/docs")
documents = [
    Document(
        document_id=f"doc-{i}",
        content=doc.read_text(),
        mime_type="text/plain",
        metadata={}
    )
    for i, doc in enumerate(docs_path.glob("*.txt"))
]

# Insert chunks
client.tool_runtime.rag_tool.insert(
    documents=documents,
    vector_db_id=vector_db_id,
    chunk_size_in_tokens=512,
)

print("✅ RAG vector DB setup complete:", vector_db_id)
