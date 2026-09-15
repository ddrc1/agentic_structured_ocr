from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from genai.graph_state import GraphState
from genai.common_nodes.parallel_sender import parallel_sender_node
from genai.agents.classification_agent.agent import classification_agent
from genai.agents.report_agent.agent import report_agent

def compile() -> CompiledStateGraph:
    graph: StateGraph = StateGraph(GraphState)

    graph.add_node(node="classification_agent", action=classification_agent)  # type: ignore
    graph.add_node(node="report_agent", action=report_agent)  # type: ignore

    graph.add_conditional_edges(START, path=parallel_sender_node)

    return graph.compile(name="content_extractor")