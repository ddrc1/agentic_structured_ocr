from typing import TypedDict, Annotated
import operator
from langgraph.graph import MessagesState


class CurrentExtractionState(TypedDict):
    current_file: str


class GraphState(MessagesState):
    file_paths: list[str]
    outputs: Annotated[list[dict], operator.add] # output do grafo
    errors: Annotated[list[str], operator.add]