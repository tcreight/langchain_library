# Build First LangGraph Workflow

**Goal:** Create a simple end-to-end LangGraph that uses the jira_fetcher node to understand how nodes connect and state flows through a graph.

**File to create:** `examples/simple_graph.py`

---

## Checklist

### Setup & Understanding
- [ ] Review the jira_fetcher node (`components/nodes/deterministic_nodes/jira_fetcher.py`)
- [ ] Review the state schema (`components/state_schemas/base_schemas.py`)
- [ ] Understand: Nodes take state → return dict → LangGraph merges into state

### Build the Graph (Code Along)
- [ ] Import required LangGraph components (`StateGraph`, `START`, `END`)
- [ ] Import the `jira_fetcher` node and `JiraTicketState` schema
- [ ] Create a `StateGraph` instance with the state schema
- [ ] Add the jira_fetcher node to the graph
- [ ] Add edges: START → jira_fetcher → END
- [ ] Compile the graph

### Run the Graph
- [ ] Create initial state with a ticket_id
- [ ] Invoke the graph with the initial state
- [ ] Print the final state to see the ticket_data
- [ ] Run with different ticket IDs (PROJ-123, PROJ-456, unknown ticket)

### Test & Understand
- [ ] Run the example: `python examples/simple_graph.py`
- [ ] Verify the output shows fetched ticket data
- [ ] Understand what LangGraph did (executed node, merged state)
- [ ] Experiment: Try running with invalid state (see error handling)

### Study Points (After It Works)
- [ ] What does `StateGraph` do?
- [ ] What does `.compile()` return? (A runnable graph)
- [ ] How does state flow from START → node → END?
- [ ] What happens if a node returns an error dict?
- [ ] How would you add a second node after jira_fetcher?

---

## Key Concepts to Learn

**StateGraph:** The container that holds your nodes and edges
- Takes a state schema (TypedDict) as input
- Manages state updates as the graph executes

**Nodes:** Functions that transform state
- Added with `graph.add_node("name", function)`
- Must match the state schema signature

**Edges:** Define execution order
- `add_edge(source, destination)` - Always go from source to destination
- START and END are special built-in nodes

**Compile:** Converts the graph definition into an executable
- Returns a "Runnable" you can invoke
- This is when LangGraph validates your graph structure

**Invoke:** Execute the graph
- Pass initial state as input
- Graph runs through nodes following edges
- Returns final state after all nodes execute

---

## Expected Output

When you run this, you should see something like:
```
=== Simple LangGraph Example ===

Initial state:
{'ticket_id': 'PROJ-123'}

Final state after graph execution:
{
  'ticket_id': 'PROJ-123',
  'ticket_data': {
    'key': 'PROJ-123',
    'summary': 'Add user authentication to login page',
    'status': 'In Progress',
    'priority': 'High',
    ...
  }
}
```

---

## Next Steps After Completion

Once this works and you understand it:
1. Build a model node (ticket_analyzer) that uses Claude
2. Add it to this graph as a second step
3. Create a 2-node pipeline: fetch → analyze

---

## Notes

- This is intentionally simple (1 node) to focus on understanding LangGraph mechanics
- You're building the foundation - every complex graph uses these same patterns
- If you get stuck, refer to `examples/basic_jira_fetcher.py` to see the node in isolation
- The pattern is: build the graph → compile → invoke → get results

---

**Status:** Not started
**Estimated time:** 30-45 minutes (including running and experimenting)
**Difficulty:** Beginner - this is your first graph!
