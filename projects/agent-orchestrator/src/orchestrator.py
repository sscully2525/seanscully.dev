"""
Main Orchestrator Graph
Defines the LangGraph workflow for multi-agent orchestration.
"""

from typing import Dict, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint import MemorySaver

from .state import AgentState
from .agents.router import RouterAgent
from .agents.research import ResearchAgent
from .agents.code import CodeAgent
from .agents.analysis import AnalysisAgent
from .agents.synthesizer import SynthesizerAgent


class AgentOrchestrator:
    """Main orchestrator coordinating multiple agents."""
    
    def __init__(self):
        self.router = RouterAgent()
        self.research_agent = ResearchAgent()
        self.code_agent = CodeAgent()
        self.analysis_agent = AnalysisAgent()
        self.synthesizer = SynthesizerAgent()
        
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        
        # Initialize graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("router", self._route)
        workflow.add_node("research", self._research)
        workflow.add_node("code", self._code)
        workflow.add_node("analysis", self._analysis)
        workflow.add_node("synthesize", self._synthesize)
        
        # Define edges
        workflow.set_entry_point("router")
        
        # Conditional routing from router
        workflow.add_conditional_edges(
            "router",
            self._should_continue,
            {
                "research": "research",
                "code": "code",
                "analysis": "analysis",
                "synthesize": "synthesize",
                "end": END
            }
        )
        
        # All agents route to synthesizer or end
        workflow.add_edge("research", "synthesize")
        workflow.add_edge("code", "synthesize")
        workflow.add_edge("analysis", "synthesize")
        workflow.add_edge("synthesize", END)
        
        # Compile with checkpointing
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)
    
    def _route(self, state: AgentState) -> Dict:
        """Router node."""
        return self.router.route(state)
    
    def _research(self, state: AgentState) -> Dict:
        """Research agent node."""
        return self.research_agent.research(state)
    
    def _code(self, state: AgentState) -> Dict:
        """Code agent node."""
        return self.code_agent.generate_code(state)
    
    def _analysis(self, state: AgentState) -> Dict:
        """Analysis agent node."""
        return self.analysis_agent.analyze(state)
    
    def _synthesize(self, state: AgentState) -> Dict:
        """Synthesizer node."""
        return self.synthesizer.synthesize(state)
    
    def _should_continue(self, state: AgentState) -> Literal["research", "code", "analysis", "synthesize", "end"]:
        """Determine next step in workflow."""
        next_agent = state.get("next_agent", "synthesize")
        
        if next_agent in ["research", "code", "analysis"]:
            return next_agent
        elif next_agent == "synthesize":
            return "synthesize"
        else:
            return "end"
    
    def invoke(self, query: str, session_id: str = None) -> Dict:
        """Execute the orchestrator on a query."""
        from langchain_core.messages import HumanMessage
        
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "next_agent": "",
            "research_results": {},
            "code_results": {},
            "analysis_results": {},
            "final_response": "",
            "execution_path": [],
            "start_time": "",
            "metadata": {"session_id": session_id}
        }
        
        config = {"configurable": {"thread_id": session_id or "default"}}
        result = self.graph.invoke(initial_state, config)
        
        return {
            "query": query,
            "response": result.get("final_response", "No response generated"),
            "execution_path": result.get("execution_path", []),
            "agent_outputs": {
                "research": result.get("research_results", {}),
                "code": result.get("code_results", {}),
                "analysis": result.get("analysis_results", {})
            }
        }
