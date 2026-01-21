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

Status: COMPLETE
"""

from textwrap import dedent
from langchain_anthropic import ChatAnthropic
from components.state_schemas.base_schemas import JiraTicketState


SYSTEM_PROMPT = dedent("""
    You are a quality assurance analyst reviewing Jira tickets.

    Your goal: Identify what needs to be tested and what questions need answers.

    Provide your analysis in this EXACT format:

    ## Test Cases (3-7 items)
    List specific, actionable test scenarios focusing on functionality and usability.
    Each test case should describe WHAT to verify, not detailed steps.

    Example format:
    - Verify user can log in with valid username and password
    - Verify appropriate error message displays when password is incorrect
    - Verify "Forgot Password" link redirects to password reset page

    ## Edge Cases (2-5 items)
    Identify boundary conditions, error states, and unusual inputs to test.

    Example format:
    - Empty username/password fields
    - SQL injection attempts in login fields
    - Session timeout during active use

    ## Acceptance Criteria
    If the ticket includes acceptance criteria, write: "See ticket description"
    If the ticket LACKS acceptance criteria, provide 3-5 clear PASS/FAIL statements.

    Example format:
    - PASS: User successfully logs in with valid credentials within 2 seconds
    - PASS: System displays specific error for invalid credentials
    - PASS: User session persists for 30 minutes of inactivity

    ## Risk Areas (2-4 items)
    Identify what could go wrong, integration points, dependencies, and user impact.

    Example format:
    - Authentication service dependency - failure blocks all logins
    - Password reset email delivery - spam filters may block
    - Concurrent login sessions - may cause data conflicts

    ## Questions for Team (3-5 items, prioritized)
    Ask critical questions to clarify requirements, edge cases, or missing information.
    Prioritize by importance - most critical first.

    Example format:
    1. Should users be able to log in from multiple devices simultaneously?
    2. What is the password complexity requirement?
    3. How should the system handle accounts locked due to failed login attempts?

    Keep each item concise (1-2 sentences max).
""").strip()


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
    ticket_key = ticket_data.get("key", "UNKNOWN")

    # Step 3: Build the full prompt with ticket data
    prompt = f"""{SYSTEM_PROMPT}

TICKET TO ANALYZE:
ID: {ticket_key}
Priority: {priority}
Summary: {summary}
Description: {description}

Provide your analysis:"""

    # Step 4: Initialize ChatAnthropic
    # temperature=0.3 keeps responses fairly consistent but not robotic
    # timeout=30 prevents hanging if API is slow
    llm = ChatAnthropic(
        model_name="claude-sonnet-4-5-20250929",
        temperature=0.3,
        timeout=30,
        stop=None
    )

    # Step 5: Call LLM with error handling
    # Why try/except? API calls can fail for many reasons:
    # - Network issues
    # - Rate limits
    # - Invalid API key
    # - Timeout
    # We don't want the whole graph to crash, so we catch errors gracefully
    try:
        response = llm.invoke(prompt)
        analysis_text = response.content

    except Exception as e:
        # If anything goes wrong, return an error dict
        # The graph will continue but the error will be in the state
        return {"error": f"LLM call failed: {str(e)}"}

    # Step 6: Parse response into structured dict
    # For now, we're storing the raw markdown response
    # Later, you could parse this into structured fields (test_scenarios, edge_cases, etc.)
    # but that's over-engineering for v1 - the markdown format is already structured
    return {
        "analysis": {
            "raw_output": analysis_text,
            "ticket_id": ticket_key
        }
    }
