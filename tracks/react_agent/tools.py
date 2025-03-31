"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function (as an example)

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

from typing import Any, Callable, List, Optional, cast

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg
from typing_extensions import Annotated

from tracks.react_agent.configuration import Configuration


def check_tfl(start: str, end: str) -> str:
    """call the TfL API to get a route given a start point and an end point.
    currently this is a dummy function that always returns "nya"."""
    return "take the bus 69 from {} to {}.".format(start, end)


TOOLS: List[Callable[..., Any]] = [check_tfl]
