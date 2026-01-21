# Build Ticket Analyzer Model Node

**Goal:** Create a model node that uses Claude to analyze Jira ticket data and extract key testing information. This teaches you how to integrate LLMs into LangGraph nodes.

**Files to create/modify:**
- `components/nodes/model_nodes/ticket_analyzer.py`
- `components/state_schemas/base_schemas.py` (update)
- `tests/unit/test_ticket_analyzer.py`

---

## Checklist

### Setup & Planning
- [x] Review the jira_fetcher node to understand the basic node pattern
- [x] Understand: Model nodes follow the same pattern but include LLM calls
- [x] Read about ChatAnthropic in LangChain docs (I can fetch this for you)
- [x] Decide what the analyzer should extract from tickets (test scenarios, acceptance criteria, edge cases)

### Update State Schema
- [x] Open `components/state_schemas/base_schemas.py`
- [x] Add a new field to `JiraTicketState` for analysis results
- [x] Mark it as `NotRequired` (since jira_fetcher doesn't populate it)
- [x] Decide on structure: dict with keys like `test_scenarios`, `edge_cases`, `acceptance_criteria`

Example:
```python
class JiraTicketState(TypedDict):
    ticket_id: str
    ticket_data: NotRequired[dict]
    analysis: NotRequired[dict]  # Add this
    error: NotRequired[str]
```

### Build the Analyzer Node
- [x] Create `components/nodes/model_nodes/ticket_analyzer.py`
- [x] Import necessary items: `ChatAnthropic`, state schema
- [x] Write the `analyze_ticket()` function with proper type hints
- [x] Extract `ticket_data` from state (check if it exists!)
- [ ] Build a prompt that asks Claude to analyze the ticket
- [ ] Initialize ChatAnthropic with model name
- [ ] Invoke the LLM with your prompt
- [ ] Parse the response into structured data
- [ ] Return dict with analysis results

### Handle Edge Cases
- [x] What if `ticket_data` doesn't exist in state? (return error)
- [ ] What if the LLM call fails? (try/except)
- [x] What if the ticket has no description? (handle gracefully)

### Write Tests
- [ ] Create `tests/unit/test_ticket_analyzer.py`
- [ ] Test: Analyzer with valid ticket data (mock the LLM response)
- [ ] Test: Analyzer without ticket_data in state (should error)
- [ ] Test: Node returns a dict (required for LangGraph)
- [ ] Run tests: `pytest tests/unit/test_ticket_analyzer.py`

### Integration Testing
- [ ] Update `examples/simple_graph.py` to include both nodes
- [ ] Add ticket_analyzer node to the graph
- [ ] Connect edges: START → jira_fetcher → ticket_analyzer → END
- [ ] Run and verify both nodes execute in sequence
- [ ] Check final state has both `ticket_data` and `analysis`

### Study & Experiment
- [ ] Run with different ticket IDs, observe different analyses
- [ ] Try breaking things: remove ticket_data from state, see error handling
- [ ] Compare to deterministic node: what's different about model nodes?
- [ ] Understand: LLM responses are non-deterministic (run twice, different results)

---

## Key Concepts to Learn

**Model Nodes vs Deterministic Nodes:**
- **Deterministic:** Same input → same output (jira_fetcher)
- **Model nodes:** Same input → *potentially different* output (LLM)
- Both follow the same state in → dict out pattern

**ChatAnthropic:**
- LangChain's wrapper for Claude API
- Takes model name, temperature, other config
- `.invoke()` method sends prompt, returns response
- Response has `.content` attribute with the text

**Prompt Engineering for Structured Output:**
- Be specific about what you want
- Ask for specific format (bullet points, JSON, etc.)
- Include examples if needed
- For production: use Structured Output (we'll learn later)

**Error Handling in Model Nodes:**
- LLM calls can fail (API errors, rate limits, timeouts)
- Always wrap in try/except
- Return error dict, don't crash the graph

---

## Example Prompt Template

```python
prompt = f"""Analyze this Jira ticket and extract testing information.

Ticket: {ticket_data['key']}
Summary: {ticket_data['summary']}
Description: {ticket_data['description']}

Please identify:
1. Key test scenarios to verify
2. Edge cases to consider
3. Acceptance criteria

Format as clear bullet points."""
```

---

## Expected State Flow

**After jira_fetcher:**
```python
{
    'ticket_id': 'PROJ-123',
    'ticket_data': { ... }
}
```

**After ticket_analyzer:**
```python
{
    'ticket_id': 'PROJ-123',
    'ticket_data': { ... },
    'analysis': {
        'test_scenarios': [...],
        'edge_cases': [...],
        'acceptance_criteria': [...]
    }
}
```

---

## Testing Strategy

**For model nodes, you'll mock the LLM:**

```python
from unittest.mock import Mock, patch

def test_analyze_ticket():
    # Mock the LLM response
    mock_llm = Mock()
    mock_llm.invoke.return_value.content = "Test scenarios:\n- Login works\n- Handles invalid credentials"

    # Test with mocked LLM
    # (We'll cover mocking in detail when you write tests)
```

**Why mock?**
- Tests run fast (no API calls)
- Tests are deterministic (no random LLM responses)
- Tests don't cost money (no API usage)
- Can test error conditions easily

---

## Things That Will Trip You Up

1. **Forgetting to check if ticket_data exists:** Always use `state.get("ticket_data")` and handle None
2. **Not handling LLM errors:** Wrap the `.invoke()` in try/except
3. **Parsing LLM output:** LLMs return strings, you need to structure them (simple parsing for now, structured output later)
4. **API keys:** You'll need `ANTHROPIC_API_KEY` in your environment or `.env` file

---

## Study Points (After It Works)

- [ ] What makes a model node different from a deterministic node?
- [ ] Why do we mock LLM calls in tests?
- [ ] What happens if the LLM returns unexpected format?
- [ ] How would you improve the prompt to get more consistent output?
- [ ] What's the difference between `.invoke()` and `.stream()`?
- [ ] When would you use structured output vs parsing strings?

---

## Next Steps After Completion

Once this works:
1. Update your simple_graph.py to run both nodes in sequence
2. See the full pipeline: fetch → analyze → results
3. Learn about structured output for more reliable LLM responses
4. Add more sophisticated analysis (complexity estimation, risk assessment)

---

## Resources

Ask me to fetch LangChain docs on:
- ChatAnthropic usage
- Structured output with Pydantic
- Prompt templates
- Error handling in chains

---

**Status:** In Progress (50% complete)
**Last Updated:** 2026-01-02
**Estimated time:** 1-2 hours (including reading, coding, testing)
**Difficulty:** Intermediate - introduces LLM integration
**Prerequisites:** ✅ Completed "Build First LangGraph Workflow"

---

## Current Progress Notes

**Completed (lines 1-17 in ticket_analyzer.py):**
- ✅ File created with proper imports
- ✅ Function signature defined correctly
- ✅ Ticket data extraction with error handling
- ✅ Individual field extraction (summary, description, priority) with defaults
- ✅ State schema updated with `analysis` and `ticket_summary` fields

**Next Steps:**
1. Build the prompt using extracted data
2. Initialize ChatAnthropic (model: "claude-sonnet-4-5-20250929")
3. Wrap LLM call in try/except
4. Parse response into structured dict
5. Return `{"analysis": {...}}` to merge into state
