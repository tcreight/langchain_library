"""
Unit tests for ticket_analyzer node.

PYTEST BASICS:
- Each test is a function that starts with "test_"
- pytest automatically finds and runs these functions
- Use "assert" to check if something is true
- If assert fails, the test fails
- Tests should be independent (don't rely on each other)

MOCKING BASICS:
- We mock the LLM so tests don't actually call the API
- Why? Fast, free, deterministic, and works offline
- We use unittest.mock.patch to replace the real LLM with a fake one
"""

import pytest
from unittest.mock import Mock, patch
from components.nodes.model_nodes.ticket_analyzer import analyze_ticket
from components.state_schemas.base_schemas import JiraTicketState


# ========================================
# TEST 1: Successful analysis with valid data
# ========================================
@patch("components.nodes.model_nodes.ticket_analyzer.ChatAnthropic")
def test_analyze_ticket_success(mock_chat_class):
    """
    Test that analyze_ticket works correctly with valid ticket data.

    This is the "happy path" test - everything works as expected.

    HOW MOCKING WORKS HERE:
    1. @patch replaces ChatAnthropic class with a mock
    2. When analyze_ticket creates ChatAnthropic(), it gets our mock instead
    3. We control what the mock returns, so no real API call happens
    """

    # Step 1: Create a mock LLM response
    # This is what we PRETEND Claude returns
    mock_llm_instance = Mock()
    mock_response = Mock()
    mock_response.content = """
    ## Test Cases
    - Verify login with valid credentials
    - Verify error message on invalid password

    ## Edge Cases
    - Empty username field
    - SQL injection attempts

    ## Acceptance Criteria
    - PASS: User logs in within 2 seconds

    ## Risk Areas
    - Authentication service dependency

    ## Questions for Team
    1. Should we support multi-device login?
    """

    # Wire up the mock: when llm.invoke() is called, return our mock response
    mock_llm_instance.invoke.return_value = mock_response

    # When ChatAnthropic() is instantiated, return our mock instance
    mock_chat_class.return_value = mock_llm_instance

    # Step 2: Create fake state with ticket data
    # This mimics what jira_fetcher would have added to the state
    test_state: JiraTicketState = {
        "ticket_id": "PROJ-123",
        "ticket_data": {
            "key": "PROJ-123",
            "summary": "Fix login bug",
            "description": "Users can't log in with special characters in password",
            "priority": "High"
        }
    }

    # Step 3: Call the function we're testing
    result = analyze_ticket(test_state)

    # Step 4: Assert (check) that the results are what we expect
    # This is where we verify the node works correctly

    # Check that result is a dict (required for LangGraph nodes)
    assert isinstance(result, dict), "Node must return a dict"

    # Check that result has "analysis" key
    assert "analysis" in result, "Result should contain 'analysis' key"

    # Check that analysis has the structure we expect
    assert "raw_output" in result["analysis"], "Analysis should have raw_output"
    assert "ticket_id" in result["analysis"], "Analysis should have ticket_id"

    # Check that the mock LLM was actually called
    mock_llm_instance.invoke.assert_called_once()

    # Check that the ticket_id is preserved
    assert result["analysis"]["ticket_id"] == "PROJ-123"

    # Check that we got the mocked content back
    assert "Test Cases" in result["analysis"]["raw_output"]


# ========================================
# TEST 2: Missing ticket data (error case)
# ========================================
def test_analyze_ticket_missing_data():
    """
    Test that analyze_ticket handles missing ticket_data gracefully.

    This tests error handling - what happens when something goes wrong?

    NO MOCKING NEEDED: This test doesn't reach the LLM call because
    it should fail early when it checks for ticket_data.
    """

    # Create state WITHOUT ticket_data
    test_state: JiraTicketState = {
        "ticket_id": "PROJ-999"
        # Note: no "ticket_data" key!
    }

    # Call the function
    result = analyze_ticket(test_state)

    # Assert that we got an error, not a crash
    assert isinstance(result, dict), "Should still return a dict"
    assert "error" in result, "Should return error when ticket_data is missing"
    assert "No ticket data" in result["error"], "Error message should be descriptive"


# ========================================
# TEST 3: LLM API call fails (network error, rate limit, etc.)
# ========================================
@patch("components.nodes.model_nodes.ticket_analyzer.ChatAnthropic")
def test_analyze_ticket_llm_failure(mock_chat_class):
    """
    Test that analyze_ticket handles LLM failures gracefully.

    This tests what happens when the API call throws an exception.
    """

    # Step 1: Make the mock LLM raise an exception when invoked
    mock_llm_instance = Mock()
    mock_llm_instance.invoke.side_effect = Exception("API rate limit exceeded")
    mock_chat_class.return_value = mock_llm_instance

    # Step 2: Create valid test state
    test_state: JiraTicketState = {
        "ticket_id": "PROJ-456",
        "ticket_data": {
            "key": "PROJ-456",
            "summary": "Test ticket",
            "description": "Test description",
            "priority": "Medium"
        }
    }

    # Step 3: Call the function
    result = analyze_ticket(test_state)

    # Step 4: Assert that we got an error, not a crash
    assert isinstance(result, dict), "Should return dict even on error"
    assert "error" in result, "Should return error when LLM fails"
    assert "LLM call failed" in result["error"], "Error should mention LLM failure"


# ========================================
# TEST 4: Verify return type is always dict
# ========================================
@patch("components.nodes.model_nodes.ticket_analyzer.ChatAnthropic")
def test_node_always_returns_dict(mock_chat_class):
    """
    Test that the node ALWAYS returns a dict.

    This is critical for LangGraph - nodes MUST return dict.
    """

    # Mock the LLM
    mock_llm_instance = Mock()
    mock_response = Mock()
    mock_response.content = "Some analysis output"
    mock_llm_instance.invoke.return_value = mock_response
    mock_chat_class.return_value = mock_llm_instance

    # Test with valid data
    test_state: JiraTicketState = {
        "ticket_id": "PROJ-789",
        "ticket_data": {
            "key": "PROJ-789",
            "summary": "Test",
            "description": "Test",
            "priority": "Low"
        }
    }

    result = analyze_ticket(test_state)

    # The critical assertion
    assert isinstance(result, dict), "Node must ALWAYS return a dict for LangGraph"


# ========================================
# TEST 5: Verify ticket fields with defaults work
# ========================================
@patch("components.nodes.model_nodes.ticket_analyzer.ChatAnthropic")
def test_analyze_ticket_missing_fields(mock_chat_class):
    """
    Test that analyze_ticket handles missing fields in ticket_data.

    What if ticket_data exists but some fields are missing?
    The node should use defaults and not crash.
    """

    # Mock the LLM
    mock_llm_instance = Mock()
    mock_response = Mock()
    mock_response.content = "Analysis with minimal data"
    mock_llm_instance.invoke.return_value = mock_response
    mock_chat_class.return_value = mock_llm_instance

    # Create state with minimal ticket_data (missing description, priority, etc.)
    test_state: JiraTicketState = {
        "ticket_id": "PROJ-MIN",
        "ticket_data": {
            "key": "PROJ-MIN"
            # Note: missing summary, description, priority
        }
    }

    # Should not crash
    result = analyze_ticket(test_state)

    # Should still work
    assert isinstance(result, dict)
    assert "analysis" in result

    # Verify the LLM was called (meaning it got past field extraction)
    mock_llm_instance.invoke.assert_called_once()
