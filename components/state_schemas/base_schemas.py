"""
Base state schemas used across multiple workflows.

These TypedDict classes define the structure of state that flows through
LangGraph nodes. Using typed schemas helps catch errors early and makes
the data flow explicit.

State Schemas are the "contract" for your graph:
- They define what data flows through your nodes
- They make the data flow explicit and type-safe
- They help catch errors at design time, not runtime

Key Pattern:
- Required fields: Data that MUST exist when the graph starts
- NotRequired fields: Data that nodes will ADD as the graph runs
"""

from typing import TypedDict, NotRequired

"""
Note for future me and anyone else that decides to use this project:
    JiraTicketState is entirely built by Claude Code as an example. That's why
    it looks pretty and has instructional comments. I'll note anything I didn't
    at least partially write.
"""


class JiraTicketState(TypedDict):
    """
    State schema for Jira ticket workflows.

    This represents the data that flows through nodes that work with Jira tickets.

    REQUIRED FIELD (no NotRequired):
        ticket_id: Must be provided when starting the graph

    OPTIONAL FIELDS (NotRequired):
        These get added by various nodes as the graph executes:
        - ticket_data: Added by jira_fetcher node
        - analysis: Added by ticket_analyzer node
        - ticket_summary: Added by summary nodes (future)
        - error: Added by any node if something fails

    Example flow:
        Start:  {"ticket_id": "PROJ-123"}
        After jira_fetcher:  {"ticket_id": "PROJ-123", "ticket_data": {...}}
        After analyzer:  {"ticket_id": "PROJ-123", "ticket_data": {...}, "analysis": {...}}
    """
    # Input: The Jira ticket ID/key (e.g., "PROJ-123")
    # This is REQUIRED - you must provide this when starting the workflow
    ticket_id: str

    # Output: The fetched ticket data (populated by jira_fetcher node)
    # NotRequired means this field might not exist initially
    ticket_data: NotRequired[dict]

    # Output: Analysis results from ticket_analyzer node
    # Contains test scenarios, edge cases, acceptance criteria, etc.
    analysis: NotRequired[dict]

    # Output: A concise summary of the ticket (future feature)
    ticket_summary: NotRequired[str]

    # Optional: Error information if something goes wrong in any node
    # Nodes return {"error": "message"} instead of crashing
    error: NotRequired[str]
