from typing import Literal
from pydantic import BaseModel, Field


class ClassificationAgentSchema(BaseModel):
    classification: Literal["contract", "report", "invoice", "other"] = Field(description="Tipo de arquivo recebido")