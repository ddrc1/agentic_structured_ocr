from pydantic import BaseModel, Field


class Item(BaseModel):
    descricao: str = Field(description="")
    quantidade: int = Field(description="")
    valor: float = Field(description="")


class NotaFiscal(BaseModel):
    fornecedor: str = Field(description="")
    cnpj: str = Field(description="")
    items: list[Item] = Field(description="")
    #valor total -> ver se é basicamente a soma dos itens ou se tem imposto envolvido
    # se for soma, fazer no proprio python