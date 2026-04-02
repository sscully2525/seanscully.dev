from typing import TypedDict, Annotated, Sequence
import operator
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import json

# State definition
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str
    research_results: str
    code_results: str
    analysis_results: str

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Router prompt
router_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a router agent. Analyze the user query and decide which specialized agent(s) to invoke.
    
Available agents:
- research: For questions requiring web search, current information, or facts
- code: For programming, data processing, or algorithmic tasks  
- analysis: For data interpretation, insights, or visualization needs
- done: If the query can be answered directly without specialized agents

Respond with a JSON object: {"next": "agent_name", "reason": "explanation"}"""),
    MessagesPlaceholder(variable_name="messages"),
])

# Research agent
research_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a research agent. Gather comprehensive information about the topic.
    Provide detailed findings with sources. Be thorough but concise."""),
    MessagesPlaceholder(variable_name="messages"),
])

# Code agent  
code_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a code agent. Write clean, efficient Python code to solve the problem.
    Include comments and explanation. Return the code and expected output."""),
    MessagesPlaceholder(variable_name="messages"),
])

# Analysis agent
analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an analysis agent. Analyze the provided information deeply.
    Identify patterns, insights, and implications. Be data-driven."""),
    MessagesPlaceholder(variable_name="messages"),
])

# Synthesizer
synthesizer_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a synthesizer agent. Combine outputs from specialized agents into a coherent, helpful response.
    Maintain context from the original query. Be clear and actionable."""),
    ("human", "Original query: {query}\n\nResearch: {research}\n\nCode: {code}\n\nAnalysis: {analysis}"),
])

def router_node(state: AgentState):
    """Route the query to appropriate agents"""
    chain = router_prompt | llm
    response = chain.invoke({"messages": state["messages"]})
    
    try:
        decision = json.loads(response.content)
        return {"next": decision["next"]}
    except:
        return {"next": "done"}

def research_node(state: AgentState):
    """Research agent execution"""
    chain = research_prompt | llm
    response = chain.invoke({"messages": state["messages"]})
    return {
        "research_results": response.content,
        "messages": [AIMessage(content=f"Research: {response.content}")]
    }

def code_node(state: AgentState):
    """Code agent execution"""
    chain = code_prompt | llm
    response = chain.invoke({"messages": state["messages"]})
    return {
        "code_results": response.content,
        "messages": [AIMessage(content=f"Code: {response.content}")]
    }

def analysis_node(state: AgentState):
    """Analysis agent execution"""
    chain = analysis_prompt | llm
    response = chain.invoke({"messages": state["messages"]})
    return {
        "analysis_results": response.content,
        "messages": [AIMessage(content=f"Analysis: {response.content}")]
    }

def synthesizer_node(state: AgentState):
    """Synthesize all agent outputs"""
    query = state["messages"][0].content
    chain = synthesizer_prompt | llm
    response = chain.invoke({
        "query": query,
        "research": state.get("research_results", "N/A"),
        "code": state.get("code_results", "N/A"),
        "analysis": state.get("analysis_results", "N/A")
    })
    return {"messages": [AIMessage(content=response.content)]}

# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("router", router_node)
workflow.add_node("research", research_node)
workflow.add_node("code", code_node)
workflow.add_node("analysis", analysis_node)
workflow.add_node("synthesizer", synthesizer_node)

# Add edges
workflow.set_entry_point("router")

# Conditional routing
workflow.add_conditional_edges(
    "router",
    lambda x: x["next"],
    {
        "research": "research",
        "code": "code", 
        "analysis": "analysis",
        "done": END
    }
)

# All agents go to synthesizer
workflow.add_edge("research", "synthesizer")
workflow.add_edge("code", "synthesizer")
workflow.add_edge("analysis", "synthesizer")

# Synthesizer ends
workflow.add_edge("synthesizer", END)

# Compile
app = workflow.compile()

# Example usage
if __name__ == "__main__":
    # Test the orchestrator
    test_queries = [
        "Analyze the correlation between Tesla stock price and EV market trends",
        "Write a Python function to calculate Fibonacci numbers with memoization",
        "What are the latest developments in quantum computing?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print('='*60)
        
        result = app.invoke({
            "messages": [HumanMessage(content=query)],
            "research_results": "",
            "code_results": "",
            "analysis_results": ""
        })
        
        print(f"\nFinal Response:")
        print(result["messages"][-1].content)
