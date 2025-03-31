from IPython.display import Image, display

from langchain_google_vertexai import ChatVertexAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from langgraph.prebuilt import ToolNode
from langgraph.graph import MessagesState, StateGraph, START, END

from src.external.tfl_api import plan_journey


@tool
def check_tfl(start: str, end: str) -> str:
    """call the TfL API to get a route given a start point and an end point. 
    returns either a list of disambiguation options or a list of journy options."""
    return plan_journey(start, end)


SYSTEM_PROMPT = """You are a helpful London travel assistant. 
When a user asks about travel between locations in London, ALWAYS use the check_tfl tool to find route information.
Do not make up routes or transit information - only provide information returned by the tool.
If the user's query is not about travel directions, respond normally without using the tool."""

tools = [check_tfl]
tool_node = ToolNode(tools)

memory = MemorySaver()
workflow = StateGraph(MessagesState)

model_with_tools = ChatVertexAI(model_name="gemini-2.0-flash-001", system_message=SystemMessage(SYSTEM_PROMPT)).bind_tools(tools)

def call_model(state: MessagesState):
    response = model_with_tools.invoke(state["messages"])
    # We return a list, because this will get added to the existing list
    return {"messages": response}

def should_continue(state: MessagesState):
    """If the last message is a function call, go to action node.
    Otherwise, return END."""
    last_message = state["messages"][-1]
    # If there is no function call, then we finish
    if not last_message.tool_calls:
        return END
    # Otherwise if there is, we continue
    return "action"

workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    ["action", END],
)

workflow.add_edge("action", "agent")
app = workflow.compile(checkpointer=memory)

graph_png = app.get_graph().draw_mermaid_png()
with open("workflow_graph.png", "wb") as f:
    f.write(graph_png)

config = {"configurable": {"thread_id": "2"}}
input_message = HumanMessage(content="how to get from catford to oxford circus?")
for event in app.stream({"messages": [input_message]}, config=config, stream_mode="values"):
    event["messages"][-1].pretty_print()