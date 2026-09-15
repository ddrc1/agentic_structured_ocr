from typing import Any, Awaitable, Callable

from langchain.agents.middleware import AgentMiddleware
from langchain.agents.middleware.types import ModelRequest, ModelResponse
from langchain_core.messages import HumanMessage
from langgraph.runtime import Runtime
from pydantic import BaseModel


class StructuredResponseRetryMiddleware(AgentMiddleware):
    def __init__(
        self,
        schema: type[BaseModel],
        max_retries: int = 2,
    ):
        super().__init__()
        self.schema_name: str = schema.__name__
        self.max_retries: int = max_retries

    def after_model(self, state: Any, runtime: Runtime) -> None:
        return None

    async def awrap_model_call(self, request: ModelRequest, handler: Callable[[ModelRequest], Awaitable[ModelResponse]]) -> ModelResponse:
        response: ModelResponse = await handler(request)

        for _ in range(self.max_retries):
            if self._is_valid(response=response):
                return response

            request.messages.append(
                HumanMessage(
                    content=f"Chame a ferramenta `{self.schema_name}` com os campos exigidos.",
                    name="structured_response_retry",
                )
            )
            response = await handler(request)

        if self._is_valid(response=response):
            return response

        raise Exception(
            f"`{self.schema_name}` não foi produzido após {self.max_retries} tentativas."
        )

    def _is_valid(self, response: ModelResponse,
    ) -> bool:
        if response.structured_response is not None:
            return True

        last: Any = response.result[-1] if response.result else None

        if last is not None and getattr(last, "tool_calls", None):
            return True

        return False
