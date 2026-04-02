"""
Agent State Management
Defines the state schema for the multi-agent orchestration graph.
"""

from typing import TypedDict, Annotated, Sequence, List, Dict, Any
import operator
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """State maintained across the agent graph execution."""
    
    # Conversation history
    messages: Annotated[Sequence[BaseMessage], operator.add]
    
    # Routing decision
    next_agent: str
    
    # Agent outputs
    research_results: Dict[str, Any]
    code_results: Dict[str, Any]
    analysis_results: Dict[str, Any]
    
    # Final synthesized response
    final_response: str
    
    # Metadata
    execution_path: List[str]
    start_time: str
    metadata: Dict[str, Any]
