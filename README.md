# LangChain Component Library

> **A note from the developer:**
> This project is not designed for production. This is my journey to relearning Python and getting started with LangChain and LangGraph. It is designed to help me and other noobs figure out how things work. Any contributions should be focused around making learning opportunities rather than trying to complete the project. I will do my best to keep things in a mostly working state but, this still VERY in dev as of
1/1/2026.

## What This Is

A learning-focused library of reusable LangChain/LangGraph components for building QA automation agents and workflows. Think of it as:
- **A learning playground** for Python beginners getting into AI/LLM development
- **Building blocks** you can snap together to create specialized agents
- **Reference implementations** showing how LangGraph nodes, state schemas, and workflows actually work
- **Documentation that teaches** rather than just describing

## Who This Is For

- **Python beginners** comfortable with basic scripting but new to LangChain/LangGraph
- **QA engineers** transitioning into development and automation
- **Anyone learning AI agent development** who wants working examples, not just theory
- **People who prefer learning by building** real, useful tools

## Quick Start

### Prerequisites
- Python 3.10+
- Basic understanding of Python (functions, dictionaries, type hints helpful but not required)
- An Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com)). Or any
LLM provider, I just happened to use Claude for this.

### Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/langchain_library.git
   cd langchain_library
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   # If pip install -e ".[dev]" fails, use PYTHONPATH workaround:
   export PYTHONPATH=/path/to/langchain_library:$PYTHONPATH
   pip install langchain langgraph langchain-anthropic pytest
   ```

4. **Set up your API key:**
   ```bash
   # Create a .env file or export directly:
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

5. **Run your first example:**
   ```bash
   python examples/simple_graph.py
   ```

## Learning Path

This project follows a structured learning path. Start here:

### 1. Understand the Basics
- Read `documentation/examples/CLAUDE.md` to understand the architecture and patterns
- Look at `components/nodes/deterministic_nodes/jira_fetcher.py` - this is the reference implementation

### 2. Build Your First Graph
- Follow `documentation/learning_guides/Build First LangGraph Workflow.md`
- This walks you through creating a simple graph that fetches and displays data
- You'll learn: StateGraph, nodes, edges, invoke

### 3. Add an LLM Node
- Follow `documentation/learning_guides/Build Ticket Analyzer Model Node.md`
- This teaches you how to integrate Claude into a node
- You'll learn: ChatAnthropic, prompts, LLM calls, mocking for tests

### 4. Build Your Own Components
- Start creating your own nodes for your use cases
- Reference the patterns in `CLAUDE.md`
- Test as you go (see `tests/` directory for examples)

## Project Structure

```
langchain_library/
├── components/               # Reusable building blocks
│   ├── nodes/
│   │   ├── deterministic_nodes/   # No LLM, just logic (API calls, transforms)
│   │   ├── model_nodes/           # Single-purpose LLM calls
│   │   └── agent_nodes/           # LLM with reasoning loops and tools
│   ├── state_schemas/        # TypedDict definitions for state flow
│   ├── subgraphs/            # Reusable mini-workflows
│   └── tools/                # Tool implementations for agents
├── documentation/
│   ├── examples/             # Example configurations and guides
│   │   └── CLAUDE.md         # **START HERE** - Project guide for Claude Code
│   └── learning_guides/      # Step-by-step learning checklists
├── examples/                 # Runnable example scripts
│   ├── simple_graph.py       # Your first graph (fetcher only)
│   └── basic_jira_fetcher.py # Standalone node example
├── tests/
│   ├── unit/                 # Test individual nodes
│   └── integration/          # Test full workflows
├── patterns/                 # Multi-agent patterns (future)
└── utils/                    # Shared utilities (future)
```

## Key Concepts

### The LangGraph Node Pattern

Every node in this library follows the same pattern:

```python
def my_node(state: StateType) -> dict:
    """Node that does something with state."""
    # 1. Extract what you need from state
    input_data = state["some_key"]

    # 2. Do your work
    result = process(input_data)

    # 3. Return updates (LangGraph merges this into state)
    return {"output_key": result}
```

### Three Types of Nodes

1. **Deterministic Nodes** - No LLM, predictable output
   - Example: API calls, data validation, transformations

2. **Model Nodes** - Single-purpose LLM calls
   - Example: Classify intent, rewrite query, extract info

3. **Agent Nodes** - LLM with reasoning and tools
   - Example: ReAct agent, plan-execute agent

### State Flow

State is a TypedDict that flows through your graph:
- **Required fields**: What the node expects to exist
- **NotRequired fields**: What the node will populate

```python
class JiraTicketState(TypedDict):
    ticket_id: str                      # Input (required)
    ticket_data: NotRequired[dict]      # Output (node populates)
    analysis: NotRequired[dict]         # Output (analyzer populates)
    error: NotRequired[str]             # Optional error info
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_jira_fetcher.py

# Run with coverage
pytest --cov
```

## Using with Claude Code

This repository is optimized for use with [Claude Code](https://claude.ai/code). The `CLAUDE.md` file tells Claude how to work with this codebase, maintaining consistent behavior across sessions.

**Key features:**
- Claude knows your skill level (Python beginner)
- Claude provides explanations, not just code
- Claude follows the established patterns
- Claude makes you learn by doing

## Contributing

Contributions are welcome, but remember: **this is a learning project**.

### Good Contributions:
- ✅ More learning guides/checklists
- ✅ Better explanations in code comments
- ✅ Example workflows for common use cases
- ✅ Beginner-friendly documentation improvements
- ✅ Tests that demonstrate concepts clearly

### Not-So-Good Contributions:
- ❌ "Production-ready" enterprise features
- ❌ Overly clever code that beginners can't understand
- ❌ Removing comments/explanations to make code more concise
- ❌ Advanced optimizations that obscure the learning value

### How to Contribute:
1. Fork the repo
2. Create a branch (`git checkout -b feature/your-learning-guide`)
3. Make your changes (focus on teaching value)
4. Test it works
5. Submit a PR explaining what learners will gain

## Current Status

**Completed:**
- ✅ Project scaffolding
- ✅ `jira_fetcher` deterministic node (reference implementation)
- ✅ `JiraTicketState` schema
- ✅ First graph workflow (`simple_graph.py`)
- ✅ Learning guide: Build First LangGraph Workflow

**In Progress:**
- 🚧 `ticket_analyzer` model node (LLM integration)
- 🚧 Learning guide: Build Ticket Analyzer Model Node

**Next Up:**
- Test case generation node
- Zephyr Scale integration
- Multi-node pipeline example

## Resources

- [LangChain Documentation](https://python.langchain.com/docs/introduction/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- `documentation/examples/CLAUDE.md` - Your primary reference guide

## License

GPL-3.0 - See LICENSE file for details

## Questions or Issues?

- Check the learning guides in `documentation/learning_guides/`
- Review patterns in `documentation/examples/CLAUDE.md`
- Look at working examples in `examples/` and `tests/`
- Open an issue if you're stuck we're all learning and I'm happy to help research.

---

**Remember:** The goal isn't to build the perfect library. The goal is to learn how LangChain, LangGraph, and AI agents work by building real, useful things. Start simple, make mistakes, learn from them, and iterate.
