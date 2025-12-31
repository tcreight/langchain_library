#!/usr/bin/env python3
"""
Basic example showing how to use the jira_fetcher node.

This demonstrates the simplest possible use - just calling the node function
directly. In a real workflow, this node would be part of a LangGraph.

Run with: python examples/basic_jira_fetcher.py
"""

from components.nodes.deterministic_nodes.jira_fetcher import fetch_jira_ticket


def main():
    """Demonstrate using the jira_fetcher node."""

    print("=== Jira Fetcher Node Example ===\n")

    # Example 1: Fetch a known ticket
    print("Example 1: Fetching ticket PROJ-123")
    print("-" * 50)

    # Create initial state with just the ticket_id
    state = {"ticket_id": "PROJ-123"}
    print(f"Input state: {state}\n")

    # Call the node - it returns updates to merge into state
    updates = fetch_jira_ticket(state)
    print(f"Node returned: {updates}\n")

    # In LangGraph, the updates would be merged into state automatically
    # For this example, we'll merge manually
    state.update(updates)
    print(f"Final state after merge:")
    print(f"  Ticket ID: {state['ticket_id']}")
    print(f"  Summary: {state['ticket_data']['summary']}")
    print(f"  Status: {state['ticket_data']['status']}")
    print(f"  Priority: {state['ticket_data']['priority']}\n")

    # Example 2: Fetch a different ticket
    print("\nExample 2: Fetching ticket PROJ-456")
    print("-" * 50)

    state2 = {"ticket_id": "PROJ-456"}
    updates2 = fetch_jira_ticket(state2)
    state2.update(updates2)

    print(f"  Summary: {state2['ticket_data']['summary']}")
    print(f"  Priority: {state2['ticket_data']['priority']}\n")

    # Example 3: Fetch an unknown ticket (still works, returns generic data)
    print("\nExample 3: Fetching unknown ticket XYZ-999")
    print("-" * 50)

    state3 = {"ticket_id": "XYZ-999"}
    updates3 = fetch_jira_ticket(state3)
    state3.update(updates3)

    print(f"  Summary: {state3['ticket_data']['summary']}")
    print(f"  (This is generic mock data for unknown tickets)\n")

    print("=== Key Takeaways ===")
    print("1. Nodes take state as input")
    print("2. Nodes return a dict of updates")
    print("3. Updates get merged into state (manually here, automatic in LangGraph)")
    print("4. This pattern works for ALL nodes - deterministic, model, and agent nodes")


if __name__ == "__main__":
    main()
