"""
RAG Service for GitHub Profile Chat
Implements Retrieval Augmented Generation without external LLM dependencies.
"""
import math
import re
import asyncio
from typing import List, Dict, Tuple, Optional
from collections import Counter

from app.services.github_service import github_service

class SimpleVectorStore:
    """
    A lightweight in-memory vector store using TF-IDF / Cosine Similarity
    """
    def __init__(self):
        self.documents: List[Dict] = []
        self.vocabulary: Dict[str, int] = {}
        self.vectors: List[Dict[int, int]] = []

    def add_documents(self, docs: List[Dict]):
        """
        Add documents to the store.
        Each doc should be: {"content": str, "metadata": dict}
        """
        self.documents.extend(docs)
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b\w+\b', text.lower())

    def _build_index(self):
        # Build vocabulary
        all_words = []
        for doc in self.documents:
            tokens = self._tokenize(doc["content"])
            all_words.extend(tokens)

        # Simple frequency filter could go here
        unique_words = sorted(list(set(all_words)))
        self.vocabulary = {word: idx for idx, word in enumerate(unique_words)}

        # Build vectors (Bag of Words)
        self.vectors = []
        for doc in self.documents:
            tokens = self._tokenize(doc["content"])
            vec = Counter(tokens)
            # Convert to sparse vector {index: count}
            sparse_vec = {self.vocabulary[word]: count for word, count in vec.items() if word in self.vocabulary}
            self.vectors.append(sparse_vec)

    def similarity(self, query: str, top_k: int = 3) -> List[Tuple[Dict, float]]:
        """Find most similar documents to query"""
        query_tokens = self._tokenize(query)
        query_vec = Counter(query_tokens)
        query_sparse = {self.vocabulary[word]: count for word, count in query_vec.items() if word in self.vocabulary}

        if not query_sparse:
            return []

        scores = []
        query_norm = math.sqrt(sum(c**2 for c in query_sparse.values()))

        for i, doc_vec in enumerate(self.vectors):
            dot_product = sum(query_sparse.get(idx, 0) * count for idx, count in doc_vec.items())
            doc_norm = math.sqrt(sum(c**2 for c in doc_vec.values()))

            if doc_norm == 0 or query_norm == 0:
                score = 0.0
            else:
                score = dot_product / (query_norm * doc_norm)

            scores.append((self.documents[i], score))

        # Sort by score desc
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


class RAGService:
    """Service for RAG Chat"""

    async def index_user_data(self, username: str) -> SimpleVectorStore:
        """Fetch and index user repositories"""
        store = SimpleVectorStore()

        # 1. Fetch Repositories
        # Limit to 10 to avoid hitting rate limits too hard
        # 'stars' sort is not valid for user repos endpoint, using 'updated'
        repos = await github_service.get_user_repositories(
            username, sort="updated", per_page=10
        )

        # Sort client-side by stars to get most relevant
        # Note: repos is a list of Repository objects, not dicts
        repos.sort(key=lambda r: r.stars, reverse=True)

        documents = []
        readme_tasks = []

        for repo in repos:
            # Add repo description
            content = f"Repository: {repo.name}\n"
            content += f"Description: {repo.description or 'No description'}\n"
            content += f"Language: {repo.language}\n"
            content += f"Topics: {', '.join(repo.topics)}\n"

            documents.append({
                "content": content,
                "metadata": {"source": repo.name, "type": "meta"}
            })

            # Queue README fetch for starred repos
            if repo.stars > 0:
                readme_tasks.append((repo.name, github_service.get_readme_content(username, repo.name)))

        # Concurrent fetch
        if readme_tasks:
            # Extract tasks from tuples
            tasks = [t[1] for t in readme_tasks]
            results = await asyncio.gather(*tasks)

            for (repo_name, _), readme in zip(readme_tasks, results):
                if readme:
                    truncated_readme = readme[:1000]
                    documents.append({
                        "content": f"README for {repo_name}:\n{truncated_readme}",
                        "metadata": {"source": repo_name, "type": "readme"}
                    })

        store.add_documents(documents)
        return store

    def generate_response(self, query: str, retrieved_docs: List[Tuple[Dict, float]]) -> str:
        """
        Simulate LLM generation using templates based on retrieved context.
        """
        if not retrieved_docs or retrieved_docs[0][1] < 0.1:
            return "I couldn't find specific information in the user's repositories matching your query. They might not have public code related to that topic."

        context_str = "\n\n".join([doc["content"] for doc, score in retrieved_docs])
        sources = list(set([doc["metadata"]["source"] for doc, score in retrieved_docs]))

        # Determine intent (simple keyword matching)
        query_lower = query.lower()

        if any(w in query_lower for w in ["what", "does", "project", "repo"]):
            return f"Based on the analysis of {', '.join(sources)}, here is what I found:\n\n{retrieved_docs[0][0]['content']}\n\nThis project appears to be relevant to your question about '{query}'."

        elif any(w in query_lower for w in ["language", "stack", "tech"]):
            return f"Looking at the code in {', '.join(sources)}, the user primarily uses technologies mentioned in these contexts:\n\n{context_str}"

        else:
            return f"I found some relevant information in {', '.join(sources)}:\n\n{retrieved_docs[0][0]['content']}\n...and {len(retrieved_docs)-1} other contexts."

rag_service = RAGService()
