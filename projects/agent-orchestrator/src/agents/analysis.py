"""
Analysis Agent
Performs data analysis, pattern recognition, and insight generation.
"""

import json
from typing import Dict, List, Any
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from ..state import AgentState


class AnalysisAgent:
    """Agent specialized in analytical reasoning and insight generation."""
    
    def __init__(self, model: str = "gpt-4"):
        self.llm = ChatOpenAI(model=model, temperature=0.1)
        
        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert analysis agent. Provide deep, data-driven insights.

Your analysis should include:
1. Key patterns and trends identified
2. Root cause analysis (if applicable)
3. Implications and recommendations
4. Confidence level for each insight
5. Alternative interpretations considered

Be rigorous, objective, and thorough."""),
            ("human", "Data/Topic: {topic}\n\nContext: {context}\n\nAnalysis Focus: {focus}"),
        ])
    
    def analyze(self, state: AgentState) -> Dict:
        """Perform analysis."""
        query = state["messages"][0].content if state["messages"] else ""
        
        # Gather context from other agents if available
        context_parts = []
        if state.get("research_results"):
            context_parts.append("Research: " + str(state["research_results"])[:500])
        if state.get("code_results"):
            context_parts.append("Code: " + str(state["code_results"])[:500])
        
        context = "\n".join(context_parts) if context_parts else "No additional context"
        
        chain = self.analysis_prompt | self.llm
        response = chain.invoke({
            "topic": query,
            "context": context,
            "focus": "Comprehensive analysis with actionable insights"
        })
        
        return {
            "analysis_results": {
                "insights": response.content,
                "confidence": "high",
                "timestamp": datetime.now().isoformat(),
            },
            "messages": state["messages"] + [
                ("assistant", f"Analysis complete: {response.content[:200]}...")
            ]
        }
