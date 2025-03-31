from langchain_google_vertexai import ChatVertexAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode


@tool
def check_tfl(start: str, end: str) -> str:
    """call the TfL API to get a route given a start point and an end point. 
    currently this is a dummy function that always returns "nya"."""
    return "take the bus 69 from {} to {}.".format(start, end)

SYSTEM_PROMPT = """You are a helpful London travel assistant. 
When a user asks about travel between locations in London, ALWAYS use the check_tfl tool to find route information.
Do not make up routes or transit information - only provide information returned by the tool.
If the user's query is not about travel directions, respond normally without using the tool."""


model_with_tools = ChatVertexAI(model_name="gemini-2.0-flash-001", system_message=SystemMessage(SYSTEM_PROMPT)).bind_tools([check_tfl])

response = model_with_tools.invoke("how do i get from canada water to london bridge")

model_with_tools.invoke("hiiii")
