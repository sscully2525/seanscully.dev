"""
Router Agent
Intelligently routes user queries to appropriate specialized agents.
"""

import json
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

from ..state import AgentState


class RouterAgent:
    """Routes queries to the most appropriate agent(s)."""
    
    AVAILABLE_AGENTS = {
        "research": "For questions requiring web search, current information, facts, or data gathering",
        "code": "For programming tasks, algorithm design, data processing, or code generation",
        "analysis": "For data interpretation, pattern recognition, insights, or visualization",
        "math": "For mathematical calculations, equations, or numerical reasoning",
        "creative": "For writing, brainstorming, or creative content generation",
    }
    
    def __init__(self, model: str = "gpt-4"):
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an intelligent router agent. Analyze the user query and determine which specialized agent(s) should handle it.

Available agents:
{agent_descriptions}

You can route to multiple agents if the query requires it. Consider:
1. The primary intent of the query
2. Whether multiple capabilities are needed
3. The optimal execution order

Respond with a JSON object:
{{
    "primary_agent": "agent_name",
    "secondary_agents": ["agent_name"],
    "reasoning": "explanation of routing decision",
    "requires_synthesis": true/false
}}"""),
            MessagesPlaceholder(variable_name="messages"),
        ])
    
    def _format_agent_descriptions(self) -> str:
        return "\n".join([f"- {k}: {v}" for k, v in self.AVAILABLE_AGENTS.items()])
    
    def route(self, state: AgentState) -> Dict:
        """Route the query to appropriate agents."""
        chain = self.prompt | self.llm
        
        response = chain.invoke({
            "messages": state["messages"],
            "agent_descriptions": self._format_agent_descriptions()
        })
        
        try:
            decision = json.loads(response.content)
            return {
                "next_agent": decision["primary_agent"],
                "routing_decision": decision,
                "execution_path": [decision["primary_agent"]]
            }
        except json.JSONDecodeError:
            # Fallback to research agent
            return {
                "next_agent": "research",
                "routing_decision": {"reasoning": "Fallback due to parsing error"},
                "execution_path": ["research"]
            }
