"""
Note for future me and anyone else that decides to use this project:
    This node is entirely built by Claude Code as an example. That's why it looks pretty. I'll note anything I didn't at least partially write.
"""

"""
Jira ticket fetcher node.

This is a deterministic node - it doesn't use an LLM, just fetches data.
For learning purposes, this uses mock data. In production, you'd replace
the mock_fetch_from_jira() function with real Jira API calls.
"""

from components.state_schemas.base_schemas import JiraTicketState


def mock_fetch_from_jira(ticket_id: str) -> dict:
    """
    Mock function that simulates fetching a ticket from Jira.

    In a real implementation, this would use the Jira API:
    - from atlassian import Jira
    - jira = Jira(url='...', username='...', password='...')
    - return jira.issue(ticket_id)

    Args:
        ticket_id: The Jira ticket key (e.g., "PROJ-123")

    Returns:
        A dictionary containing mock ticket data
    """
    # Simulate different tickets based on ID
    mock_tickets = {
        "PROJ-123": {
            "key": "PROJ-123",
            "summary": "Add user authentication to login page",
            "description": "Users need to be able to log in with username and password. Should validate credentials against database.",
            "status": "In Progress",
            "priority": "High",
            "assignee": "john.doe",
            "created": "2025-01-15T10:30:00Z"
        },
        "PROJ-456": {
            "key": "PROJ-456",
            "summary": "Fix broken search functionality",
            "description": "Search returns no results even when data exists. Appears to be a query bug.",
            "status": "Open",
            "priority": "Critical",
            "assignee": "jane.smith",
            "created": "2025-01-20T14:15:00Z"
        }
    }

    # Return the mock ticket if it exists, otherwise a generic one
    return mock_tickets.get(ticket_id, {
        "key": ticket_id,
        "summary": f"Mock ticket {ticket_id}",
        "description": "This is a mock ticket for testing purposes.",
        "status": "Open",
        "priority": "Medium",
        "assignee": "unassigned",
        "created": "2025-01-01T00:00:00Z"
    })


def fetch_jira_ticket(state: JiraTicketState) -> dict:
    """
    LangGraph node that fetches a Jira ticket and adds it to state.

    This is the key pattern for nodes:
    1. Take state as input (type: JiraTicketState)
    2. Extract what you need from state
    3. Do some work (fetch the ticket)
    4. Return a dict with updates to state

    Args:
        state: The current state containing ticket_id

    Returns:
        A dict containing the ticket_data to merge into state
    """
    # Step 1: Get what we need from state
    ticket_id = state["ticket_id"]

    # Step 2: Do the work (fetch the ticket)
    try:
        ticket_data = mock_fetch_from_jira(ticket_id)

        # Step 3: Return updates to state
        return {"ticket_data": ticket_data}

    except Exception as e:
        # If something goes wrong, return an error
        return {"error": f"Failed to fetch ticket {ticket_id}: {str(e)}"}
