# Multi-Agent Orchestrator

A production-grade system for coordinating specialized AI agents using LangGraph.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│   User      │────▶│   Router    │────▶│  Specialized    │
│   Query     │     │   Agent     │     │    Agents       │
└─────────────┘     └─────────────┘     └─────────────────┘
                                               │
                         ┌─────────────────────┘
                         ▼
                  ┌─────────────┐
                  │ Synthesizer │────▶ Final Response
                  └─────────────┘
```

## Project Structure

```
agent-orchestrator/
├── src/
│   ├── __init__.py
│   ├── state.py              # State management
│   ├── orchestrator.py       # Main graph definition
│   ├── agents/
│   │   ├── router.py         # Routing logic
│   │   ├── research.py       # Research agent
│   │   ├── code.py           # Code generation agent
│   │   ├── analysis.py       # Analysis agent
│   │   └── synthesizer.py    # Response synthesis
│   ├── memory/
│   │   └── conversation.py   # Redis-backed memory
│   └── tools/
│       └── search.py         # Search utilities
├── ui/
│   └── app.py                # Streamlit interface
├── tests/
├── requirements.txt
└── README.md
```

## Features

- **Intelligent Routing**: Router agent analyzes queries and delegates to specialized agents
- **Multi-Agent Coordination**: Research, Code, Analysis, Math, and Creative agents
- **State Management**: Persistent conversation state with Redis
- **Streaming Execution**: Real-time updates as agents execute
- **Synthesis Layer**: Combines multi-agent outputs into coherent responses

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=your_key
export REDIS_URL=redis://localhost:6379

# Run Streamlit UI
streamlit run ui/app.py

# Or use programmatically
from src.orchestrator import AgentOrchestrator

orch = AgentOrchestrator()
result = orch.invoke("Explain quantum computing and write a Python simulation")
print(result["response"])
```

## Agent Capabilities

| Agent | Purpose | Tools |
|-------|---------|-------|
| Research | Information gathering | Web search, APIs |
| Code | Programming tasks | Code execution, linting |
| Analysis | Data insights | Statistical analysis |
| Math | Calculations | Symbolic math |
| Creative | Content generation | Style transfer |

## Configuration

Environment variables:
- `OPENAI_API_KEY`: OpenAI API key
- `REDIS_URL`: Redis connection URL
- `MODEL_NAME`: LLM model (default: gpt-4)
