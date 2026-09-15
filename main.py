from glob import glob
import pandas as pd
import asyncio
import time
from pathlib import Path
from langgraph.graph.state import CompiledStateGraph
from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

from genai.graph import compile

load_dotenv()
langfuse: Langfuse = Langfuse(
    timeout=600,
    flush_at=20,
    flush_interval=5
)
langfuse_handler = CallbackHandler()

files: list[str] = glob("./data/raw/*")

async def main():
    start: float = time.time()
    try:
        graph: CompiledStateGraph = compile()
        outputs: list[dict] = await graph.ainvoke(
            input={"file_paths": files},
            config={"callbacks": [langfuse_handler]},
        )

        print(outputs["errors"])
        Path("./data/processed").mkdir(parents=True, exist_ok=True)

        contract_outputs_df: pd.DataFrame = pd.DataFrame(outputs["contract_outputs"])
        contract_outputs_df.to_csv("./data/processed/contract_outputs.csv", index=False)

        report_outputs_df: pd.DataFrame = pd.DataFrame(outputs["report_outputs"])
        report_outputs_df.to_csv("./data/processed/report_outputs.csv", index=False)

        invoice_outputs_df: pd.DataFrame = pd.DataFrame(outputs["invoice_outputs"])
        invoice_outputs_df.to_csv("./data/processed/invoice_outputs.csv", index=False)

        end: float = time.time()
        print(f"Tempo total: {end - start} s")
    finally:
        langfuse.flush()
        langfuse.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
