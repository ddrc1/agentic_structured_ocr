from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.messages import SystemMessage, HumanMessage, AnyMessage
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import END
from langgraph.types import Command

from genai.agents.report_agent.schemas import ReportAgentSchema
from genai.agents.report_agent.prompt import prompt
from genai.middlewares.structured_response_retry import StructuredResponseRetryMiddleware

load_dotenv()


# model: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
#     model="gemma-4-31b-it",
#     temperature=0
# )

model: ChatOpenAI = ChatOpenAI(
    model="gpt-5.6-luna",
    reasoning={"effort": None, "summary": "auto"},
    timeout=60,
    max_retries=3
)

agent: CompiledStateGraph = create_agent(
    name="report_agent",
    model=model,
    middleware=[StructuredResponseRetryMiddleware(schema=ReportAgentSchema, max_retries=3)],
    response_format=ReportAgentSchema   
)


async def report_agent(state: dict) -> Command:
    encoded_content: str = state["encoded_content"]
    
    messages: list[AnyMessage] = [
        SystemMessage(content=prompt),
        # HumanMessage(content=[
        #     {"type": "text", "text": "Classifique a imagem."},
        #     {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{pdf_para_imagens_base64(state["current_file"])[0]}"}}
        # ])
        HumanMessage(content=[{
            "type": "file",
            "file": {
                "filename": Path(state["current_filepath"]).name,
                "file_data": f"data:application/pdf;base64,{encoded_content}",
            },
        }]),
    ]

    update: dict
    try:
        model_response: dict = await agent.ainvoke(input={"messages": messages})
        structured_response: ReportAgentSchema = model_response["structured_response"]
        output: dict = structured_response.model_dump()
        output["filename"] = Path(state["current_filepath"]).name
        update = {
            "report_outputs": [output]
        }
    except Exception as e:
        error_msg: str = f"Error occurred in file {state['current_filepath']} while invoking report_agent: {e}"
        update={"errors": [error_msg]}
        
    return Command(
        goto=END,
        graph=Command.PARENT,
        update=update
    )