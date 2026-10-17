from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class BaseTool(ABC):
    tool_id: str
    name: str
    description: str
    version: str = "1.0.0"
    permission_level: str = "user"  # user, admin
    risk_level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
    requires_approval: bool = False
    implementation_type: str = "local"  # local, external, simulated
    timeout_seconds: int = 30

    @abstractmethod
    def get_input_schema(self) -> Dict[str, Any]:
        """Returns JSON schema for input arguments"""
        pass

    @abstractmethod
    def get_output_schema(self) -> Dict[str, Any]:
        """Returns JSON schema for outputs"""
        pass

    @abstractmethod
    def execute(self, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Executes the tool with validated arguments"""
        pass

    def to_metadata(self, last_executed_at: Optional[datetime] = None) -> Dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "input_schema": self.get_input_schema(),
            "output_schema": self.get_output_schema(),
            "permission_level": self.permission_level,
            "risk_level": self.risk_level,
            "requires_approval": self.requires_approval,
            "is_available": True,
            "implementation_type": self.implementation_type,
            "last_executed_at": last_executed_at,
        }
