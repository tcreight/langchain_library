"""
Model node for analyzing Jira tickets with Claude.

This is a MODEL NODE - it uses an LLM for a specific task (analyzing tickets).
Compare to jira_fetcher (deterministic node) which just fetches data without AI.

Pattern for model nodes:
1. Extract data from state
2. Build a prompt for the LLM
3. Call the LLM (wrapped in try/except)
4. Parse the response
5. Return structured data

Status: IN PROGRESS (stops at line 17 - needs LLM call implementation)
"""

from langchain_anthropic import ChatAnthropic
from components.state_schemas.base_schemas import JiraTicketState


def analyze_ticket(state: JiraTicketState) -> dict:
    

    """
    LangGraph node that analyzes Jira tickets using Claude.

    Takes ticket data from state, sends it to Claude for analysis,
    and returns structured test scenarios and acceptance criteria.

    Args:
        state: JiraTicketState containing ticket_data from jira_fetcher

    Returns:
        dict with 'analysis' key containing test scenarios, edge cases, etc.
        OR dict with 'error' key if something goes wrong
    """

    # Step 1: Extract ticket data from state
    # Always use .get() to safely handle missing keys
    ticket_data = state.get("ticket_data")
    if not ticket_data:
        return {"error": "No ticket data available. Run jira_fetcher first."}

    # Step 2: Extract individual fields with fallbacks
    # Using .get() with defaults prevents KeyError if fields are missing
    summary = ticket_data.get("summary", "no summary")
    description = ticket_data.get("description", "no description")
    priority = ticket_data.get("priority", "no priority")

    # TODO: Step 3: Build the prompt for Claude
    # TODO: Step 4: Initialize ChatAnthropic
    # TODO: Step 5: Call LLM (with try/except!)
    # TODO: Step 6: Parse response into structured dict
    # TODO: Step 7: Return {"analysis": {...}}