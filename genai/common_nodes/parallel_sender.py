from langgraph.types import Send

def parallel_sender_node(state: dict) -> list[Send]:
    return [Send(node="classification_agent", arg={"current_file": path}) for path in state["file_paths"]]