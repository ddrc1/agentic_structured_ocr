from typing import TypedDict, Annotated
import operator
from langgraph.graph import MessagesState


class ExtractionState(TypedDict):
    current_filepath: str
    encoded_content: str


class GraphState(MessagesState):
    file_paths: list[str]
    contract_outputs: Annotated[list[dict], operator.add] # output do grafo
    report_outputs: Annotated[list[dict], operator.add] # output do grafo
    invoice_outputs: Annotated[list[dict], operator.add] # output do grafo
    errors: Annotated[list[str], operator.add]