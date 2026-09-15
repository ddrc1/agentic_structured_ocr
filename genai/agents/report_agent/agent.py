import base64
import pymupdf
from dotenv import load_dotenv

# from langchain_openai import ChatOpenAI
# from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.messages import SystemMessage, HumanMessage, AnyMessage
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import END
from langgraph.types import Command

from genai.agents.report_agent.schemas import ReportAgentSchema
from genai.agents.report_agent.prompt import prompt

load_dotenv()


model: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
    model="gemma-4-31b-it",
    temperature=0
)

agent: CompiledStateGraph = create_agent(
    name="report_agent",
    model=model,
    response_format=ReportAgentSchema   
)

# def pdf_para_imagens_base64(caminho: str) -> list[str]:
#     doc = pymupdf.open(caminho)
#     imagens = []
#     for pagina in doc:
#         pix = pagina.get_pixmap(dpi=150)
#         imagens.append(base64.b64encode(pix.tobytes("png")).decode())
#     return imagens


async def report_agent(state: dict) -> Command:
    print(state["current_file"])
    with open(file=state["current_file"], mode="rb") as f:
        file: bytes = f.read()

    encoded_content: bytes = base64.b64encode(file)
    messages: list[AnyMessage] = [
        SystemMessage(content=prompt),
        # HumanMessage(content=[
        #     {"type": "text", "text": "Classifique a imagem."},
        #     {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{pdf_para_imagens_base64(state["current_file"])[0]}"}}
        # ])
        HumanMessage(content=[{"type": "file", "base64": encoded_content, "mime_type": "application/pdf"}])
    ]

    model_response: dict = await agent.ainvoke(input={"messages": messages})
    structured_response: ReportAgentSchema = model_response["structured_response"]
    print(structured_response.model_dump_json(indent=4))

    return Command(
        goto=END
    )