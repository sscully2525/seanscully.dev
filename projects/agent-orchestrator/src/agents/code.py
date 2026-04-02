"""
Code Agent
Handles programming tasks, code generation, and technical problem solving.
"""

import json
import re
from typing import Dict, List, Optional
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from ..state import AgentState


class CodeAgent:
    """Agent specialized in code generation and technical tasks."""
    
    def __init__(self, model: str = "gpt-4"):
        self.llm = ChatOpenAI(model=model, temperature=0.2)
        
        self.code_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert code agent. Write clean, efficient, well-documented code.

Guidelines:
- Use best practices and design patterns
- Include comprehensive comments
- Handle edge cases and errors
- Optimize for readability and performance
- Provide usage examples

Structure your response:
1. Approach explanation
2. Complete code solution
3. Usage examples
4. Complexity analysis (if relevant)"""),
            ("human", "Task: {task}\n\nRequirements:\n{requirements}"),
        ])
    
    def _extract_code(self, text: str) -> List[Dict]:
        """Extract code blocks from markdown."""
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        return [{"language": lang or "text", "code": code} for lang, code in matches]
    
    def generate_code(self, state: AgentState) -> Dict:
        """Generate code solution."""
        query = state["messages"][0].content if state["messages"] else ""
        
        # Determine if there are specific requirements
        requirements = "No specific requirements provided"
        
        chain = self.code_prompt | self.llm
        response = chain.invoke({
            "task": query,
            "requirements": requirements
        })
        
        code_blocks = self._extract_code(response.content)
        
        return {
            "code_results": {
                "solution": response.content,
                "code_blocks": code_blocks,
                "language": code_blocks[0]["language"] if code_blocks else "python",
                "timestamp": datetime.now().isoformat(),
            },
            "messages": state["messages"] + [
                ("assistant", f"Generated code solution with {len(code_blocks)} code blocks")
            ]
        }
