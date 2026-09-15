from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from genai.graph_state import GraphState, ExtractionState
from genai.common_nodes.parallel_sender import parallel_sender_node
from genai.agents.classification_agent.agent import classification_agent
from genai.agents.report_agent.agent import report_agent
from genai.agents.contract_agent.agent import contract_agent
from genai.agents.invoice_agent.agent import invoice_agent

def _sub_graph() -> CompiledStateGraph:
    graph: StateGraph = StateGraph(ExtractionState)

    graph.add_node(
        node="classification_agent",
        action=classification_agent,
        destinations=("report_agent", "contract_agent", "invoice_agent"),
    )  # type: ignore
    graph.add_node(node="report_agent", action=report_agent)  # type: ignore
    graph.add_node(node="contract_agent", action=contract_agent)  # type: ignore
    graph.add_node(node="invoice_agent", action=invoice_agent)  # type: ignore

    graph.add_edge(START, "classification_agent")

    return graph.compile(name="extraction_subgraph")


def compile() -> CompiledStateGraph:
    graph: StateGraph = StateGraph(GraphState)

    graph.add_node(node="extraction_subgraph", action=_sub_graph())  # type: ignore

    graph.add_conditional_edges(START, path=parallel_sender_node, path_map=["extraction_subgraph"])

    return graph.compile(name="content_extractor")