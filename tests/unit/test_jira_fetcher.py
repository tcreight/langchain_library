"""
Unit tests for the jira_fetcher node.

These tests verify that the node works correctly without needing
to actually connect to Jira (since we're using mock data).

DETERMINISTIC NODE TESTING:
- jira_fetcher is a deterministic node (no LLM, no randomness)
- Same input = same output every time
- No need to mock anything since it already uses mock data
- Tests are simple: check that it returns the expected structure
"""

from components.nodes.deterministic_nodes.jira_fetcher import fetch_jira_ticket


# ========================================
# TEST 1: Fetch known ticket (happy path)
# ========================================
def test_fetch_known_ticket():
    """
    Test fetching a ticket that exists in our mock data.

    This tests the "happy path" - everything works as expected.
    """
    # Arrange: Set up the input state
    # This mimics what the graph would pass to the node
    state = {"ticket_id": "PROJ-123"}

    # Act: Call the node
    result = fetch_jira_ticket(state)

    # Assert: Check the results
    # Verify the node returns expected data structure
    assert "ticket_data" in result, "Result should contain ticket_data"
    assert result["ticket_data"]["key"] == "PROJ-123"
    assert result["ticket_data"]["summary"] == "Add user authentication to login page"
    assert result["ticket_data"]["status"] == "In Progress"


# ========================================
# TEST 2: Fetch different known ticket
# ========================================
def test_fetch_another_known_ticket():
    """
    Test fetching a different known ticket.

    Verifies that the mock data works for multiple tickets.
    """
    state = {"ticket_id": "PROJ-456"}

    result = fetch_jira_ticket(state)

    assert "ticket_data" in result
    assert result["ticket_data"]["key"] == "PROJ-456"
    assert result["ticket_data"]["summary"] == "Fix broken search functionality"
    assert result["ticket_data"]["priority"] == "Critical"


# ========================================
# TEST 3: Fetch unknown ticket (fallback)
# ========================================
def test_fetch_unknown_ticket():
    """
    Test fetching a ticket that isn't in our mock data.

    Should return generic mock data instead of crashing.
    This is graceful degradation - the node always returns something.
    """
    state = {"ticket_id": "UNKNOWN-999"}

    result = fetch_jira_ticket(state)

    # Should still work, but with generic data
    assert "ticket_data" in result
    assert result["ticket_data"]["key"] == "UNKNOWN-999"
    assert "Mock ticket" in result["ticket_data"]["summary"]


# ========================================
# TEST 4: Verify return type (LangGraph contract)
# ========================================
def test_node_returns_dict():
    """
    Test that the node returns a dict (required for LangGraph).

    ALL LangGraph nodes MUST return dict - this is critical!
    """
    state = {"ticket_id": "PROJ-123"}

    result = fetch_jira_ticket(state)

    # Must be a dict to merge into state
    assert isinstance(result, dict), "Node must return dict for LangGraph"


# ========================================
# TEST 5: State preservation (LangGraph behavior)
# ========================================
def test_preserves_state_structure():
    """
    Test that calling the node doesn't break state.

    In LangGraph, nodes return updates that get merged into state.
    The node shouldn't remove existing state keys.

    KEY CONCEPT: Nodes return UPDATES, not full state.
    LangGraph merges the returned dict into existing state.
    """
    # Note: Adding extra field to test that nodes don't break on unexpected state keys
    state = {
        "ticket_id": "PROJ-123",
        "some_other_field": "should be preserved"  # type: ignore
    }

    result = fetch_jira_ticket(state)  # type: ignore

    # The node only returns what it wants to UPDATE
    # LangGraph will merge this with existing state
    assert "ticket_data" in result, "Should add ticket_data to state"

    # The node doesn't need to return fields it didn't change
    # LangGraph handles preserving existing state
    # So it's OK that "some_other_field" is not in result
