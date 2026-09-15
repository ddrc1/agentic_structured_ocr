from pydantic import BaseModel, Field


class ReportAgentSchema(BaseModel):
    date: str = Field(description="Data do serviço. Formato DD/MM/YYYY")
    responsible_technician: str = Field(description="Nome do técnico responsável")
    equipment: str = Field(description="Equipamento")
    problem_description: str = Field(description="Descrição da ocorrência")
    applied_solution: str = Field(description="Solução aplicada")