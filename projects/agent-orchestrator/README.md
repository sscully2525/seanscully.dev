# Multi-Agent Orchestrator

A LangGraph-powered system that coordinates multiple specialized AI agents to solve complex tasks.

## Architecture

```
User Query → Router Agent → [Research Agent | Code Agent | Analysis Agent]
                              ↓
                        Synthesizer Agent
                              ↓
                        Final Response
```

## Features

- **Router Agent**: Intelligently routes queries to specialized agents
- **Research Agent**: Web search and information gathering
- **Code Agent**: Python code generation and execution
- **Analysis Agent**: Data analysis and visualization
- **Synthesizer**: Combines outputs into coherent responses
- **Memory**: Conversation history and context preservation

## Tech Stack

- LangGraph for agent orchestration
- OpenAI GPT-4 for agent reasoning
- FastAPI for the API layer
- Redis for state persistence
