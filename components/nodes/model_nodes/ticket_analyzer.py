from langchain_anthropic import ChatAnthropic
from components.state_schemas.base_schemas import JiraTicketState


def analyze_ticket(state: JiraTicketState) -> dict:
    """
    LangGraph node that consumes ticket data via state
    and uses LLM to analyze and produce test ideas.
    """

    ticket_data = state.get("ticket_data")
    if not ticket_data:
        return {"error": "No data available."}

    summary = ticket_data.get("summary", "no summary")
    description = ticket_data.get("description", "no description")
    priority = ticket_data.get("priority", "no priority")