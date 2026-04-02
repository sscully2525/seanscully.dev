"""
Synthesizer Agent
Combines outputs from multiple agents into coherent, actionable responses.
"""

import json
from typing import Dict
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from ..state import AgentState


class SynthesizerAgent:
    """Synthesizes multi-agent outputs into final response."""
    
    def __init__(self, model: str = "gpt-4"):
        self.llm = ChatOpenAI(model=model, temperature=0.3)
        
        self.synthesis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a synthesis agent. Combine information from multiple sources into a coherent, actionable response.

Guidelines:
- Integrate insights seamlessly
- Resolve any contradictions
- Maintain factual accuracy
- Structure for clarity and readability
- Include specific details and examples
- Provide clear next steps or recommendations

Your response should feel like a single, unified answer, not a collection of separate pieces."""),
            ("human", """Original Query: {query}

Execution Path: {execution_path}

Research Findings:
{research}

Code Solution:
{code}

Analysis Insights:
{analysis}

Synthesize this into a comprehensive response."""),
        ])
    
    def synthesize(self, state: AgentState) -> Dict:
        """Synthesize all agent outputs."""
        query = state["messages"][0].content if state["messages"] else ""
        
        # Gather all available outputs
        research = state.get("research_results", {}).get("findings", "No research performed")
        code = state.get("code_results", {}).get("solution", "No code generated")
        analysis = state.get("analysis_results", {}).get("insights", "No analysis performed")
        
        chain = self.synthesis_prompt | self.llm
        response = chain.invoke({
            "query": query,
            "execution_path": " → ".join(state.get("execution_path", [])),
            "research": research,
            "code": code,
            "analysis": analysis
        })
        
        return {
            "final_response": response.content,
            "synthesis_metadata": {
                "agents_used": state.get("execution_path", []),
                "timestamp": datetime.now().isoformat(),
            }
        }
