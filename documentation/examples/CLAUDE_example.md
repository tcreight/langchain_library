# CLAUDE.md

<!-- HUMAN-ONLY NOTES - Claude, please ignore:

PURPOSE: This file instructs Claude Code on how to work with this codebase. It's read automatically
by Claude Code when working in this repository, making every session consistent.

METHODOLOGY: Keep this file updated as the project evolves. When you discover patterns that work
well or common mistakes to avoid, add them here. This becomes institutional knowledge.

MAINTENANCE TIPS:
- Update "Current Project Status" section as you complete major milestones
- Add new patterns to "Code Patterns Reference" as they emerge
- Keep "Developer Context" accurate - if your skill level changes, update it
- This is a living document - don't be afraid to refactor it as you learn
- You can also direct Claude to updated this document as you go. Be specific about what should be updated.

-->

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<!-- HUMAN-ONLY: This section sets expectations and establishes the learning-first philosophy.
Update as project goals evolve. The "make the user study" instruction is critical - it ensures
Claude doesn't just write all the code for you. -->

## Project Overview

Building a reusable library of plug-and-play LangChain/LangGraph components to quickly assemble specialized agents and workflows for QA automation, with potential for third-party clients. In addition, this project is a learning experience. Write minimal applicable code, prefer examples, explanations and references to documentation. Make the user study!

**Core Goal:** Minimize custom work per agent by having battle-tested building blocks ready to compose.

<!-- HUMAN-ONLY: Developer Context is THE most important section for Claude's behavior.
This tells Claude who you are, your skill level, and how to communicate with you.

WHEN TO UPDATE:
- Your Python skills improve → update "Skill Level"
- You change roles → update "Role"
- You discover communication preferences → update "Work Style" or "Notes for Claude Code"

This section directly affects how Claude explains concepts, structures code, and provides feedback. -->

## Developer Context

### Background
- **Role:** QA Specialist, transitioning into development
- **Skill Level:** Python beginner ("baby control flow worm"), comfortable with basic scripting
- **Experience:** Tech-savvy, homelab enthusiast, tool-building mindset
- **Work Style:** Ex-military background, appreciates direct communication and practical solutions

### Notes for Claude Code
- **Assume Python beginner level:** Explain non-obvious patterns, avoid overly clever code
- **Favor clarity over brevity:** Readable code > clever one-liners
- **Provide context for errors:** Explain what went wrong and how to fix it
- **Use type hints:** They help with understanding and catch errors early
- **Comment non-obvious logic:** Why, not just what
- **Start simple:** Don't over-engineer on first pass
- **Test incrementally:** Small working pieces > big broken system

<!-- HUMAN-ONLY: Commands section is your quick reference for common operations.

METHODOLOGY: Add new commands as you discover useful workflows. This saves Claude from having to
explain basic commands every session.

MAINTENANCE: When you add new test files, update the examples. If you change your testing approach
(e.g., add pytest plugins), document the new commands here. -->

## Commands

### Setup
```bash
# Install dependencies (including dev dependencies)
pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov

# Run a specific test file
pytest tests/unit/test_jira_fetcher.py

# Run a specific test function
pytest tests/unit/test_jira_fetcher.py::test_fetch_known_ticket
```

### Running Examples
```bash
# Run the basic Jira fetcher example
python examples/basic_jira_fetcher.py
```

<!-- HUMAN-ONLY: Architecture section defines the foundational patterns and structure.
- MODIFY THIS SECTION TO FIT YOUR PROJECT! The architecture section shown is specific to THIS project.

PURPOSE: This is the "how we build things" reference. Every node, state schema, and workflow
should follow these patterns.

METHODOLOGY:
- Core Concepts: The fundamental LangGraph pattern (state in → dict out)
- Component Library Structure: Where files go and why
- Node Categories: The three types of nodes and when to use each
- State Schema Pattern: How to structure TypedDicts for type safety

CRITICAL: When you create new node types or discover better patterns, update this section.
This ensures consistency across all components. -->

## Architecture

### Core Concepts

This library follows the **LangGraph node pattern** where:
1. **Nodes** are functions that take `state` as input (a TypedDict)
2. Nodes return a `dict` containing updates to merge into state
3. LangGraph automatically merges the returned dict into the state
4. State schemas are defined using TypedDict for type safety

### Component Library Structure
<!--
- I recommend letting Claude come up with the file structure based on your project description.
- It's easy enough to make changes once the scaffold is in place.
 -->

```
langchain-component-library/
├── components/
│   ├── nodes/
│   │   ├── model_nodes/          # LLM calls with structured output
│   │   ├── deterministic_nodes/  # API calls, data transforms, no LLM
│   │   └── agent_nodes/          # Reasoning loops with tool access
│   ├── subgraphs/                # Reusable mini-workflows
│   ├── tools/                    # Tool implementations
│   └── state_schemas/            # Shared state definitions
├── patterns/                     # Multi-agent patterns (router, subagent, etc.)
├── utils/                        # Retry policies, prompts, validation
└── tests/
    ├── unit/
    ├── integration/
    └── fixtures/
```

### Node Categories

**Deterministic Nodes** (`components/nodes/deterministic_nodes/`):
- No LLM calls, just data operations
- Examples: API calls, data validation, transformations, vector search
- Pattern: Extract from state → Do work → Return updates

**Model Nodes** (`components/nodes/model_nodes/`):
- Use LLMs for single-purpose tasks
- Examples: Intent classification, query rewriting, response generation
- Typically use structured output for reliability

**Agent Nodes** (`components/nodes/agent_nodes/`):
- Use LLMs with reasoning loops and tools
- Examples: ReAct agents, tool-calling agents, plan-execute agents
- Can make multiple LLM calls and use external tools

### State Schema Pattern

All state schemas use TypedDict with:
- Required fields: Inputs the node expects to exist
- `NotRequired` fields: Outputs the node will populate or optional fields
- This makes data flow through the graph explicit and type-safe

Example:
```python
class JiraTicketState(TypedDict):
    ticket_id: str                      # Input (required)
    ticket_data: NotRequired[dict]      # Output (node populates this)
    error: NotRequired[str]             # Optional error info
```

<!-- HUMAN-ONLY: Architecture Principles guide high-level design decisions.

WHEN TO USE:
- "When to Split Projects" → deciding if a new feature needs a separate repo
- "Key Design Patterns" → choosing how to structure new components

These principles prevent over-engineering early on and provide structure as the project grows.
Update these as you learn from real usage. -->

### Architecture Principles

#### When to Split Projects
**Create separate projects when:**
- Different execution triggers (event sources, schedules)
- Independent scaling needs (different resource profiles)
- Different failure domains (blast radius containment)
- No shared runtime state (only shared output artifacts)
- Different teams/ownership

**Keep as subgraphs when:**
- Sequential execution with shared state
- Tight coupling (can't test one without the other)
- Shared configuration and dependencies
- Single logical workflow with distinct phases

**Integration Point:** Separate projects share data via shared storage/APIs, not runtime state.

#### Key Design Patterns

**Interface-First Design**
```python
from typing import TypedDict, Protocol

class NodeInterface(Protocol):
    """All nodes must follow this interface"""
    def __call__(self, state: TypedDict) -> dict:
        """Returns dict to update state"""
        ...
```

**Configuration Over Code**
Use YAML/JSON configs for component parameters rather than hardcoding.

**Granular Nodes for Observability**
- Smaller nodes = more checkpoints = easier debugging
- Each external service call = separate node
- Trade-off: More nodes vs less re-execution on failure

<!-- HUMAN-ONLY: Technology Choices documents the "why" behind tech stack decisions.

PURPOSE: When you're six months in and wondering "why did I choose Python over TypeScript?",
this section has the answer. It also helps future contributors understand the rationale.

MAINTENANCE: If you add new core libraries (e.g., a different vector store), add them here
with rationale. This prevents decision fatigue in future sessions. -->

## Technology Choices

### Language: Python
**Rationale:**
- Best LangChain/LangGraph support (features land here first)
- Larger community, more examples
- Better for learning (more forgiving than TypeScript)
- Stronger integration ecosystem
- Good for workflow automation use case

**TypeScript considered but deprioritized:**
- Slightly behind on features
- Better for web-facing/edge deployments (not primary use case)
- Compile-time type safety nice-to-have, not critical

### Core Libraries
- **LangChain/LangGraph:** Agent orchestration and workflows
- **Anthropic API:** Claude Sonnet 4.5 for LLM calls
- **Vector Store:** Chroma (local, persistent) for development
- **Embeddings:** OpenAI text-embedding-3-small

<!-- HUMAN-ONLY: Code Patterns Reference is your copy-paste library.

PURPOSE: These are proven patterns that work. When implementing new nodes, start here.

METHODOLOGY:
- Each pattern is a complete, working example
- Copy the pattern, modify for your use case
- If you discover a new pattern that gets reused 3+ times, add it here

MAINTENANCE: As patterns evolve (e.g., you add better error handling), update the examples.
Keep them simple and focused on one concept each. -->

## Code Patterns Reference

### Pattern 1: Basic Node
```python
def my_node(state: StateType) -> dict:
    """Nodes always return a dict to update state."""
    # 1. Get what you need from state
    input_data = state["some_key"]

    # 2. Do something
    result = process(input_data)

    # 3. Return updates
    return {"output_key": result}
```

### Pattern 2: API Call Node
```python
def call_external_api(state: StateType) -> dict:
    """Pattern for calling external APIs."""
    try:
        response = requests.post(
            "https://api.example.com/endpoint",
            json={"data": state["input"]},
            timeout=30
        )
        response.raise_for_status()
        return {"result": response.json()}
    except requests.RequestException as e:
        print(f"API call failed: {e}")
        return {"error": str(e)}
```

### Pattern 3: LLM Call
```python
def ask_llm(state: StateType) -> dict:
    """Pattern for LLM calls."""
    llm = ChatAnthropic(model="claude-sonnet-4-20250514")

    prompt = f"""
    Task: {state["task_description"]}
    Data: {state["data"]}

    Respond with clear, actionable output.
    """

    response = llm.invoke(prompt)
    return {"llm_output": response.content}
```

### Pattern 4: Conditional Router
```python
def route_decision(state: StateType) -> str:
    """Decide which node to go to next."""
    if state["needs_human_review"]:
        return "human_review_node"
    elif state["error"]:
        return "error_handler_node"
    else:
        return "continue_workflow_node"

workflow.add_conditional_edges(
    "decision_node",
    route_decision,
    {
        "human_review_node": "human_review_node",
        "error_handler_node": "error_handler_node",
        "continue_workflow_node": "continue_workflow_node"
    }
)
```

<!-- HUMAN-ONLY: RAG Pipeline Implementation provides the step-by-step process for building
retrieval-augmented generation systems.

WHEN TO USE: When you need to build features that search/retrieve from documentation, tickets,
or other text sources before generating responses.

NOTE: This is more advanced than basic node patterns. Don't worry about this until you need
to implement search/retrieval features. -->

## RAG Pipeline Implementation

### Five-Step Process
1. **Load Documents:** Use appropriate loaders (WebBaseLoader, PyPDFLoader, ConfluenceLoader)
2. **Chunk Documents:** RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
3. **Embed & Store:** OpenAIEmbeddings + Chroma vector store
4. **Create Retriever:** `vector_store.as_retriever(search_kwargs={"k": 5})`
5. **Connect to Generation:** 2-step RAG (simple) or Agentic RAG (flexible)

### RAG Architectures

**2-Step RAG (Fast, Predictable):**
- Always retrieve → always generate
- Single LLM call per query
- Good for simple, predictable queries

**Agentic RAG (Smart, Flexible):**
- LLM decides when to retrieve
- Can chain multiple searches
- More LLM calls but better results for complex queries

<!-- HUMAN-ONLY: Common Pitfalls is your "learn from my mistakes" section.

PURPOSE: These are errors you've made or will make. Keeping them documented prevents repeat mistakes.

METHODOLOGY: When you encounter a bug that took >30 minutes to fix, add it here. Include:
1. What went wrong
2. How to avoid it
3. Example of the correct approach (if helpful)

This section grows with experience - it's more valuable after 6 months than after 6 days. -->

## Common Pitfalls to Avoid

1. **State mutations:** Always return new dicts, never mutate state directly
2. **Missing return dicts:** Nodes must return `dict`, not raw values
3. **No None handling:** Always check `state.get("key")` and handle missing values
4. **Poor chunking:** Test chunk sizes for your specific content
5. **Ignoring metadata:** Use source, timestamp for filtering/context
6. **Over-engineering:** Start simple, iterate based on real usage

<!-- HUMAN-ONLY: Development Workflow defines your build → test → iterate cycle.

PURPOSE: This is your reminder to stay pragmatic. It's easy to get caught up in "perfect code."
This workflow keeps you moving forward.

NOTE: The 5-step process here reflects the ex-military "bias toward action" preference. If you
find a different workflow works better for you, update it. Just keep it simple and actionable. -->

## Development Workflow

1. **Write code that works** (don't worry about elegance)
2. **Run it, fix errors, repeat**
3. **Make it slightly better** (add error handling, logging)
4. **Ship it, use it, find what breaks**
5. **Fix what breaks, add features**

### Testing Strategy
- Unit tests for individual nodes (mock external calls)
- Integration tests for full pipelines (use fixtures)
- Create test fixtures for common scenarios (failed APIs, malformed outputs, edge cases)

**Testing Philosophy:**
- Tests verify nodes work correctly in isolation before composing them into graphs
- Use the actual node functions (no mocking of nodes themselves)
- Mock external dependencies (APIs, databases) when present
- Verify state updates are correct
- Check edge cases and error handling

<!-- HUMAN-ONLY: Integration Points documents external systems and APIs.

PURPOSE: Quick reference for what integrations are available and how to use them.

MAINTENANCE: As you add new integrations (Slack, email, databases), add them here with:
- What it connects to
- Which library/SDK to use
- Link to docs or MCP server if available

This prevents "how do I connect to X again?" questions in every session. -->

## Integration Points

### Atlassian Tools
- Jira API: `atlassian-python-api` library
- Confluence: Document loaders and MCP servers available
- Zephyr Scale: API integration for test cycle management

### Data Flow Between Projects
- Use shared database or blob storage for artifacts
- API endpoints for cross-project communication
- No shared runtime state between separate deployments

<!-- HUMAN-ONLY: Component Reusability Guidelines ensure your library stays modular.

PURPOSE: These guidelines keep components independent and composable. Following them means:
- New workflows can reuse existing nodes
- You can share components with other projects
- Future you won't hate past you for tight coupling

METHODOLOGY: Before creating a new component, check these guidelines. After creating one,
verify it meets these standards. This is especially important as the library grows. -->

## Component Reusability Guidelines

**Make components reusable by:**
- Clear, well-defined interfaces (input/output schemas)
- Configuration via parameters, not hardcoding
- Independent testability
- Single responsibility per component
- Documentation: purpose, dependencies, breaking changes

**Version and document:**
- Keep CHANGELOG.md for major components
- Semantic versioning
- Document breaking changes clearly

<!-- HUMAN-ONLY: Current Project Status is the MOST FREQUENTLY UPDATED section.

PURPOSE: This tells Claude (and future you) what's done, what's in progress, and what's next.

CRITICAL MAINTENANCE:
- Update this after every major milestone (completed node, working pipeline, etc.)
- Keep "Next Steps / Current Focus" accurate - Claude uses this to understand priorities
- When files are no longer "empty placeholders", update that note
- Add new reference implementations as you build them

This section ensures every Claude Code session starts with accurate context. Update it often! -->

## Current Project Status

- Most files are currently empty placeholders - the project is in early scaffolding phase
- The `jira_fetcher` node (components/nodes/deterministic_nodes/jira_fetcher.py) is the reference implementation showing the full pattern
- When implementing new nodes, follow the pattern in the jira_fetcher implementation
- All components use mock data for learning purposes; replace with real integrations in production

### Next Steps / Current Focus

Building QA Documentation Pipeline with:
1. Jira ticket fetching and analysis
2. Test case generation
3. Zephyr Scale integration
4. Start simple (single ticket → analysis → output)
5. Add structure (proper LangGraph nodes)
6. Connect to real APIs
7. Iterate based on usage
