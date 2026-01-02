"""
Simple LangGraph workflow example.

This is your first graph! It demonstrates the core LangGraph pattern:
1. Define a state schema (JiraTicketState)
2. Create a StateGraph with that schema
3. Add nodes (functions that process state)
4. Connect nodes with edges (define execution flow)
5. Compile and run

This example uses just one node (jira_fetcher), but you can chain
multiple nodes together by adding more edges.

Run with: python examples/simple_graph.py
"""

from langgraph.graph import StateGraph, START, END
from components.nodes.deterministic_nodes.jira_fetcher import fetch_jira_ticket
from components.state_schemas.base_schemas import JiraTicketState


# Step 1: Create a StateGraph with your state schema
# This tells LangGraph what shape your data will have
builder = StateGraph(JiraTicketState)

# Step 2: Add nodes (functions that process state)
# The node name is auto-detected from the function name
builder.add_node(fetch_jira_ticket)

# Step 3: Define the execution flow with edges
# START → fetch_jira_ticket → END means:
#   1. Graph starts
#   2. Runs fetch_jira_ticket node
#   3. Graph ends
builder.add_edge(START, "fetch_jira_ticket")
builder.add_edge("fetch_jira_ticket", END)

# Step 4: Compile the graph into a runnable
# This validates your graph structure and prepares it for execution
graph = builder.compile()

print("=== Initial State ===")
# Create the starting state with just a ticket_id
# The jira_fetcher node will add ticket_data to the state
initial_state = {"ticket_id": "PROJ-456"}
print(initial_state)

print("\n=== Running Graph ===")
# Invoke the graph with initial state
# The graph will:
#   1. Start with initial_state
#   2. Run fetch_jira_ticket node
#   3. Merge the node's return value into state
#   4. Return the final state
result = graph.invoke(initial_state)

print("\n=== Final State ===")
# Now result contains both the original ticket_id AND the new ticket_data
# that the jira_fetcher node added
print(f"Ticket: {result['ticket_data']['key']}")
print(f"Summary: {result['ticket_data']['summary']}")
print(f"Status: {result['ticket_data']['status']}")

print("\n=== Graph Visualization (Mermaid) ===")
# This shows the structure of your graph as a diagram
# You can paste this into a Mermaid viewer to see a visual representation
print(graph.get_graph().draw_mermaid())
