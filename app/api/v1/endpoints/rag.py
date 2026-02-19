"""
RAG related endpoints
"""
from fastapi import APIRouter, HTTPException, Body

from app.services.rag_service import rag_service
from app.models.schemas import RAGQueryRequest, RAGResponse

router = APIRouter()

@router.post("/ask", response_model=RAGResponse)
async def ask_github(
    username: str,
    request: RAGQueryRequest = Body(...)
):
    """
    Chat with a GitHub Profile (RAG Demo).
    Retrieves relevant repositories and READMEs to answer questions about the user's code.
    """
    # 1. Index User Data (In a real app, this should be cached or pre-computed)
    try:
        store = await rag_service.index_user_data(username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user data: {str(e)}")

    # 2. Retrieve Relevant Docs
    retrieved = store.similarity(request.query, top_k=3)

    # 3. Generate Answer
    answer = rag_service.generate_response(request.query, retrieved)

    # 4. Format Response
    sources = list(set([doc["metadata"]["source"] for doc, score in retrieved]))
    context_used = [doc["content"][:200] + "..." for doc, score in retrieved]

    return RAGResponse(
        answer=answer,
        sources=sources,
        context_used=context_used
    )
