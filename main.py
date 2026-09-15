from glob import glob
import asyncio
from langgraph.graph.state import CompiledStateGraph

from genai.graph import compile


files: list[str] = glob("./data/raw/*")[:1]

async def main():
    graph: CompiledStateGraph = compile()
    await graph.ainvoke(input={"file_paths": files})


if __name__ == "__main__":
    asyncio.run(main())
