from langgraph.types import Send

def parallel_sender_node(state: dict) -> list[Send]:
    return [Send(node="extraction_subgraph", arg={"current_filepath": path}) for path in state["file_paths"]]