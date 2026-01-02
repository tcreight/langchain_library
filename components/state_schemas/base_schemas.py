"""
Base state schemas used across multiple workflows.

These TypedDict classes define the structure of state that flows through
LangGraph nodes. Using typed schemas helps catch errors early and makes
the data flow explicit.
"""

from typing import TypedDict, NotRequired

"""
Note for future me and anyone else that decides to use this project:
    JiraTicketState is entirely built by Claude Code as an example. That's why it looks pretty and has instructional comments. I'll note anything I didn't at least partially write.
"""

class JiraTicketState(TypedDict):
    """
    State schema for Jira ticket workflows.

    This represents the data that flows through nodes that work with Jira tickets.
    """
    # Input: The Jira ticket ID/key (e.g., "PROJ-123")
    ticket_id: str

    # Output: The fetched ticket data (populated by fetcher node)
    # NotRequired means this field might not exist initially
    ticket_data: NotRequired[dict]

    # Optional: Error information if something goes wrong
    error: NotRequired[str]

    # Optional: test case ideas, risk areas, acceptance criteria, etc.
    analysis: NotRequired[dict]
    ticket_summary: NotRequired[str]
