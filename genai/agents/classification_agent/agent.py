import base64
import pymupdf
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.messages import SystemMessage, HumanMessage, AnyMessage
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import END
from langgraph.types import Command

from genai.agents.classification_agent.schemas import ClassificationAgentSchema
from genai.middlewares.structured_response_retry import StructuredResponseRetryMiddleware
from genai.agents.classification_agent.prompt import prompt

load_dotenv()


# model: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
#     model="gemma-4-26b-a4b-it",
#     temperature=0
# )

model: ChatOpenAI = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0,
    timeout=60,
    max_retries=3
)

agent: CompiledStateGraph = create_agent(
    name="classification_agent",
    model=model,
    middleware=[StructuredResponseRetryMiddleware(schema=ClassificationAgentSchema, max_retries=3)],
    response_format=ClassificationAgentSchema   
)

# def pdf_para_imagens_base64(caminho: str) -> list[str]:
#     doc = pymupdf.open(caminho)
#     imagens = []
#     for pagina in doc:
#         pix = pagina.get_pixmap(dpi=150)
#         imagens.append(base64.b64encode(pix.tobytes("png")).decode())
#     return imagens


async def classification_agent(state: dict) -> Command:
    with open(file=state["current_filepath"], mode="rb") as f:
        file: bytes = f.read()

    encoded_content: str = base64.b64encode(file).decode("ascii")
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

    model_response: dict = await agent.ainvoke(input={"messages": messages})
    structured_response: ClassificationAgentSchema = model_response["structured_response"]

    goto: str
    errors: list[str] = []
    graph: str | None = None
    classification: str = structured_response.classification
    if classification == "contract":
        goto = "contract_agent"
    elif classification == "report":
        goto = "report_agent"
    elif classification == "invoice":
        goto = "invoice_agent"
    else:
        goto = END
        graph = Command.PARENT
        errors.append(f"Arquivo {state['current_filepath']} sem tipo definido. Opções possíveis: Contrato, relatório e nota fiscal / recibo")
    
    return Command(
        goto=goto,
        graph=graph,
        update={
            "encoded_content": encoded_content,
            "errors": errors
        }
    )
