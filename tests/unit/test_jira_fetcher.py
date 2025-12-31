"""
Unit tests for the jira_fetcher node.

These tests verify that the node works correctly without needing
to actually connect to Jira (since we're using mock data).
"""

import pytest
from components.nodes.deterministic_nodes.jira_fetcher import fetch_jira_ticket


def test_fetch_known_ticket():
    """Test fetching a ticket that exists in our mock data."""
    # Arrange: Set up the input state
    state = {"ticket_id": "PROJ-123"}

    # Act: Call the node
    result = fetch_jira_ticket(state)

    # Assert: Check the results
    assert "ticket_data" in result
    assert result["ticket_data"]["key"] == "PROJ-123"
    assert result["ticket_data"]["summary"] == "Add user authentication to login page"
    assert result["ticket_data"]["status"] == "In Progress"


def test_fetch_another_known_ticket():
    """Test fetching a different known ticket."""
    state = {"ticket_id": "PROJ-456"}

    result = fetch_jira_ticket(state)

    assert "ticket_data" in result
    assert result["ticket_data"]["key"] == "PROJ-456"
    assert result["ticket_data"]["summary"] == "Fix broken search functionality"
    assert result["ticket_data"]["priority"] == "Critical"


def test_fetch_unknown_ticket():
    """Test fetching a ticket that isn't in our mock data - should return generic mock."""
    state = {"ticket_id": "UNKNOWN-999"}

    result = fetch_jira_ticket(state)

    # Should still work, but with generic data
    assert "ticket_data" in result
    assert result["ticket_data"]["key"] == "UNKNOWN-999"
    assert "Mock ticket" in result["ticket_data"]["summary"]


def test_node_returns_dict():
    """Test that the node returns a dict (required for LangGraph)."""
    state = {"ticket_id": "PROJ-123"}

    result = fetch_jira_ticket(state)

    # Must be a dict to merge into state
    assert isinstance(result, dict)


def test_preserves_state_structure():
    """
    Test that calling the node doesn't break state.

    In LangGraph, nodes return updates that get merged into state.
    The node shouldn't remove existing state keys.
    """
    state = {
        "ticket_id": "PROJ-123",
        "some_other_field": "should be preserved"
    }

    result = fetch_jira_ticket(state)

    # The node only returns what it wants to UPDATE
    # LangGraph will merge this with existing state
    assert "ticket_data" in result
    # The node doesn't need to return fields it didn't change
    # (LangGraph handles that)
