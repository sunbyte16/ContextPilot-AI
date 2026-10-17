from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class BaseLLMProvider(ABC):
    provider_id: str
    name: str

    @abstractmethod
    def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        context_memories: Optional[List[Dict[str, Any]]] = None,
        retrieved_documents: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Generates conversational response, citation links, and intent."""
        pass

    @abstractmethod
    def generate_plan(
        self,
        objective: str,
        available_tools: List[Dict[str, Any]],
        context_memories: Optional[List[Dict[str, Any]]] = None,
        retrieved_documents: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Generates a structured multi-step plan with tool mappings and risk analysis."""
        pass

    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        """Tests provider connectivity and returns diagnostic information."""
        pass
