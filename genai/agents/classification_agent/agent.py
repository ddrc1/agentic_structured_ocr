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

from genai.agents.classification_agent.schemas import ClassificationAgentSchema
from genai.agents.classification_agent.prompt import prompt

load_dotenv()


model: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
    model="gemma-4-26b-a4b-it",
    temperature=0
)

agent: CompiledStateGraph = create_agent(
    name="classification_agent",
    model=model,
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
    structured_response: ClassificationAgentSchema = model_response["structured_response"]

    goto: str
    errors: list[str] = []
    classification: str = structured_response.classification
    if classification == "contract":
        goto = "contract_agent"
    elif classification == "report":
        goto = "report_agent"
    elif classification == "tax_receipt":
        goto = "tax_receipt_agent"
    else:
        goto = END
        errors.append(f"Arquivo {state["current_file"]} sem tipo definido. Opções possíveis: Contrato, relatório e nota fiscal / recibo")
    
    print(goto)
    return Command(
        goto=goto,
        update={
            "errors": errors
        }
    )


#  File "d:\Projetos\Python\teste_franq\.venv\Lib\site-packages\langgraph\_internal\_runnable.py", line 522, in ainvoke
#     ret = await self.afunc(*args, **kwargs)
#           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "D:\Projetos\Python\teste_franq\genai\agents\report_agent\agent.py", line 41, in report_agent
#     print(state["current_file"])
#           ~~~~~^^^^^^^^^^^^^^^^
# KeyError: 'current_file'
# During task with name 'report_agent' and id '27085be0-ba6f-6c46-d3ee-b44019a3d2e0'