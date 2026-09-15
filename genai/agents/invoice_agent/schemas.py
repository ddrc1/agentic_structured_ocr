from pydantic import BaseModel, Field


class Item(BaseModel):
    descricao: str = Field(description="Descrição do item")
    quantidade: int = Field(description="Quantidade do item")
    valor: float = Field(description="Valor do item")


class InvoiceAgentSchema(BaseModel):
    fornecedor: str = Field(description="Fornecedor da nota fiscal")
    cnpj: str = Field(description="CNPJ do fornecedor")
    items: list[Item] = Field(description="Lista de itens da nota fiscal")
    valor_total: float = Field(description="Valor total da nota fiscal")