from pydantic import BaseModel, Field


class Contrato(BaseModel):
    contratante: str = Field(description="")
    contratado: str = Field(description="")
    objeto_contrato: str = Field(description="")
    data_vigencia: str = Field(description="")
    valor_mensal: float = Field(description="")