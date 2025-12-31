from langgraph.graph import StateGraph, START, END 
from components.nodes.deterministic_nodes.jira_fetcher import fetch_jira_ticket
from components.state_schemas.base_schemas import JiraTicketState


builder = StateGraph(JiraTicketState)
builder.add_node(fetch_jira_ticket)
builder.add_edge(START, "fetch_jira_ticket")
builder.add_edge("fetch_jira_ticket", END)
graph = builder.compile()

print("=== Initial State ===")
initial_state = {"ticket_id": "PROJ-456"}
print(initial_state)

print("\n=== Running Graph ===")
result = graph.invoke(initial_state)

print("\n=== Final State ===")
print(f"Ticket: {result['ticket_data']['key']}")
print(f"Summary: {result['ticket_data']['summary']}")
print(f"Status: {result['ticket_data']['status']}")

# Visualize graph
app = graph
print(app.get_graph().draw_mermaid())
