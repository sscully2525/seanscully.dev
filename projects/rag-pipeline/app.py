from typing import List, Dict, Tuple
import numpy as np
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rank_bm25 import BM25Okapi
import re

class AdvancedRAGPipeline:
    """Production RAG with query rewriting, hybrid search, and reranking"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        
        # Document store
        self.documents: List[Document] = []
        self.doc_embeddings: np.ndarray = None
        
        # BM25 index
        self.bm25 = None
        self.tokenized_docs = []
        
    def add_documents(self, texts: List[str], metadatas: List[Dict] = None):
        """Add documents to the index"""
        if metadatas is None:
            metadatas = [{} for _ in texts]
            
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        
        for text, meta in zip(texts, metadatas):
            chunks = text_splitter.split_text(text)
            for i, chunk in enumerate(chunks):
                self.documents.append(Document(
                    page_content=chunk,
                    metadata={**meta, "chunk_index": i}
                ))
        
        # Build vector index
        texts = [doc.page_content for doc in self.documents]
        self.doc_embeddings = np.array(self.embeddings.embed_documents(texts))
        
        # Build BM25 index
        self.tokenized_docs = [self._tokenize(t) for t in texts]
        self.bm25 = BM25Okapi(self.tokenized_docs)
        
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization for BM25"""
        return re.findall(r'\b\w+\b', text.lower())
    
    def rewrite_query(self, query: str) -> str:
        """Expand query for better retrieval"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Rewrite the user query to improve retrieval.
            Expand abbreviations, add synonyms, and clarify intent.
            Return ONLY the rewritten query, no explanation."""),
            ("human", "Query: {query}")
        ])
        
        chain = prompt | self.llm
        result = chain.invoke({"query": query})
        return result.content.strip()
    
    def vector_search(self, query: str, k: int = 10) -> List[Tuple[int, float]]:
        """Dense retrieval using embeddings"""
        query_embed = np.array(self.embeddings.embed_query(query))
        
        # Cosine similarity
        similarities = np.dot(self.doc_embeddings, query_embed) / (
            np.linalg.norm(self.doc_embeddings, axis=1) * np.linalg.norm(query_embed)
        )
        
        # Get top k
        top_indices = np.argsort(similarities)[::-1][:k]
        return [(int(idx), float(similarities[idx])) for idx in top_indices]
    
    def keyword_search(self, query: str, k: int = 10) -> List[Tuple[int, float]]:
        """Sparse retrieval using BM25"""
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top k
        top_indices = np.argsort(scores)[::-1][:k]
        return [(int(idx), float(scores[idx])) for idx in top_indices]
    
    def reciprocal_rank_fusion(
        self,
        vector_results: List[Tuple[int, float]],
        keyword_results: List[Tuple[int, float]],
        k: float = 60.0
    ) -> List[int]:
        """Merge results using RRF"""
        scores = {}
        
        # Add vector scores
        for rank, (doc_id, _) in enumerate(vector_results):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
        
        # Add keyword scores
        for rank, (doc_id, _) in enumerate(keyword_results):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
        
        # Sort by score
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [doc_id for doc_id, _ in sorted_docs]
    
    def rerank(self, query: str, doc_indices: List[int]) -> List[int]:
        """Cross-encoder reranking (simplified - would use dedicated model)"""
        # In production: use cross-encoder like BAAI/bge-reranker-large
        # For demo: use LLM to score relevance
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Rate the relevance of each document to the query.
            Return a JSON object with doc indices as keys and scores (0-10) as values."""),
            ("human", "Query: {query}\n\nDocuments:\n{docs}")
        ])
        
        docs_text = "\n".join([
            f"[{i}] {self.documents[idx].page_content[:200]}..."
            for i, idx in enumerate(doc_indices[:5])  # Rerank top 5
        ])
        
        chain = prompt | self.llm
        # Simplified: return original order for demo
        return doc_indices
    
    def query(self, query: str, top_k: int = 5) -> Dict:
        """End-to-end RAG query"""
        # Rewrite query
        rewritten = self.rewrite_query(query)
        
        # Hybrid retrieval
        vector_results = self.vector_search(rewritten, k=10)
        keyword_results = self.keyword_search(rewritten, k=10)
        
        # Fusion
        fused = self.reciprocal_rank_fusion(vector_results, keyword_results)
        
        # Rerank
        reranked = self.rerank(rewritten, fused)
        
        # Get top documents
        context_docs = [self.documents[i] for i in reranked[:top_k]]
        context = "\n\n".join([
            f"[Source {i+1}] {doc.page_content}"
            for i, doc in enumerate(context_docs)
        ])
        
        # Generate response
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Answer the question using only the provided context.
            Cite sources using [Source X] format. If unsure, say so."""),
            ("human", "Context:\n{context}\n\nQuestion: {query}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"context": context, "query": query})
        
        return {
            "query": query,
            "rewritten": rewritten,
            "response": response.content,
            "sources": [
                {"content": doc.page_content[:150] + "...", "metadata": doc.metadata}
                for doc in context_docs
            ],
            "retrieval_stats": {
                "vector_hits": len(vector_results),
                "keyword_hits": len(keyword_results),
                "fused_candidates": len(fused)
            }
        }

# Demo
if __name__ == "__main__":
    # Sample documents
    docs = [
        """LangGraph is a library for building stateful, multi-actor applications with LLMs.
        It provides a graph-based approach to orchestrating AI workflows.""",
        
        """Retrieval-Augmented Generation (RAG) combines information retrieval with text generation.
        It allows LLMs to access external knowledge and reduce hallucinations.""",
        
        """Vector databases store embeddings for semantic search. Popular options include
        Pinecone, Weaviate, Chroma, and pgvector for PostgreSQL.""",
        
        """BM25 is a ranking function used in information retrieval. It's based on
        probabilistic retrieval frameworks and considers term frequency and document length.""",
        
        """Query rewriting improves retrieval by expanding abbreviations and adding synonyms.
        It helps bridge the gap between user queries and document vocabulary."""
    ]
    
    # Initialize pipeline
    rag = AdvancedRAGPipeline()
    rag.add_documents(docs)
    
    # Test queries
    test_queries = [
        "What is LangGraph used for?",
        "How does RAG work?",
        "Tell me about vector search"
    ]
    
    for q in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {q}")
        print('='*60)
        
        result = rag.query(q)
        print(f"\nRewritten: {result['rewritten']}")
        print(f"\nResponse: {result['response']}")
        print(f"\nSources used: {len(result['sources'])}")
