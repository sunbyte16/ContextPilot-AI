from typing import Optional
from app.core.config import settings
from app.agents.providers.base import BaseLLMProvider
from app.agents.providers.local_demo import LocalDemoProvider
from app.agents.providers.bedrock import BedrockProvider


def get_llm_provider(provider_name: Optional[str] = None) -> BaseLLMProvider:
    name = (provider_name or settings.LLM_PROVIDER).lower()
    if name in ["bedrock", "aws-bedrock", "bedrock-claude"]:
        return BedrockProvider()
    return LocalDemoProvider()
