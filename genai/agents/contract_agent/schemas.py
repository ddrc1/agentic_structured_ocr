from pydantic import BaseModel, Field


class ContractAgentSchema(BaseModel):
    contratante: str = Field(description="Tomador do serviço")
    contratado: str = Field(description="Fornecedor do serviço")
    objeto_contrato: str = Field(description="Descrição do serviço contratado")
    data_inicio: str = Field(description="Data de início do contrato. Formato: DD/MM/YYYY")
    data_final: str = Field(description="Data de término do contrato. Formato: DD/MM/YYYY")
    valor_mensal: float = Field(description="Valor mensal do contrato")