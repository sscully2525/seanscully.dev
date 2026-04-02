"""
Research Agent
Gathers information from various sources to answer queries.
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools import DuckDuckGoSearchRun

from ..state import AgentState


class ResearchAgent:
    """Agent specialized in information gathering and research."""
    
    def __init__(self, model: str = "gpt-4"):
        self.llm = ChatOpenAI(model=model, temperature=0.1)
        self.search_tool = DuckDuckGoSearchRun()
        
        self.research_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a research agent. Gather comprehensive information about the topic.
            
Use the search results provided to formulate a detailed, accurate response.
Include specific facts, figures, and sources where possible.
Structure your response clearly with:
1. Key findings
2. Supporting details
3. Sources consulted

Be thorough but concise."""),
            ("human", "Query: {query}\n\nSearch Results:\n{search_results}"),
        ])
    
    def _search(self, query: str, num_results: int = 5) -> str:
        """Perform web search."""
        try:
            results = self.search_tool.run(query)
            return results
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def research(self, state: AgentState) -> Dict:
        """Execute research task."""
        # Get the original query
        query = state["messages"][0].content if state["messages"] else ""
        
        # Perform search
        search_results = self._search(query)
        
        # Generate research response
        chain = self.research_prompt | self.llm
        response = chain.invoke({
            "query": query,
            "search_results": search_results
        })
        
        return {
            "research_results": {
                "findings": response.content,
                "sources": search_results[:500],  # Truncated
                "timestamp": datetime.now().isoformat(),
            },
            "messages": state["messages"] + [
                ("assistant", f"Research findings: {response.content[:200]}...")
            ]
        }
