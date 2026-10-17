import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
from app.core.config import settings
from app.agents.providers.base import BaseLLMProvider


class BedrockProvider(BaseLLMProvider):
    provider_id = "bedrock"
    name = "Amazon Bedrock Runtime Adapter"

    def __init__(self):
        self.region = settings.AWS_REGION
        self.model_id = settings.BEDROCK_MODEL_ID
        self._client = None

    def _get_client(self):
        if self._client is None:
            # Check AWS configuration
            session_kwargs = {"region_name": self.region}
            if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
                session_kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
                session_kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
                if settings.AWS_SESSION_TOKEN:
                    session_kwargs["aws_session_token"] = settings.AWS_SESSION_TOKEN
            
            session = boto3.Session(**session_kwargs)
            self._client = session.client("bedrock-runtime")
        return self._client

    def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        context_memories: Optional[List[Dict[str, Any]]] = None,
        retrieved_documents: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        client = self._get_client()

        # Format messages for AWS Bedrock Converse API
        converse_messages = []
        for m in messages:
            role = "user" if m["role"] == "user" else "assistant"
            converse_messages.append({
                "role": role,
                "content": [{"text": m["content"]}]
            })

        system_prompts = []
        base_system = (
            system_prompt or "You are ContextPilot AI, an intelligent agentic assistant that plans tasks, "
            "uses connected tools, respects human approvals, and delivers verified results."
        )
        if context_memories:
            mem_text = "\n".join([f"- [{m.get('category')}]: {m.get('title')} - {m.get('content')}" for m in context_memories])
            base_system += f"\n\nUser Context Memories:\n{mem_text}"

        system_prompts.append({"text": base_system})

        try:
            response = client.converse(
                modelId=self.model_id,
                messages=converse_messages,
                system=system_prompts,
                inferenceConfig={"maxTokens": 1024, "temperature": 0.2}
            )
            output_msg = response["output"]["message"]["content"][0]["text"]
            usage = response.get("usage", {})

            return {
                "content": output_msg,
                "intent": "chat",
                "is_plan_request": "plan" in output_msg.lower(),
                "citations": [],
                "usage": usage
            }
        except (NoCredentialsError, ClientError, BotoCoreError) as e:
            raise RuntimeError(
                f"Amazon Bedrock API Error: {str(e)}. "
                "Ensure valid AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) and region are set, "
                "or switch to 'Local Demo' provider in Settings."
            )

    def generate_plan(
        self,
        objective: str,
        available_tools: List[Dict[str, Any]],
        context_memories: Optional[List[Dict[str, Any]]] = None,
        retrieved_documents: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        client = self._get_client()

        prompt = (
            f"You are the planning engine of ContextPilot AI. Given the user objective: '{objective}', "
            f"generate an ordered JSON plan utilizing only these registered tools: {[t['tool_id'] for t in available_tools]}.\n"
            "Format your answer strictly as a valid JSON object with keys: "
            "'objective', 'description', 'risk_level' (LOW/MEDIUM/HIGH), 'estimated_complexity' (SIMPLE/STANDARD/COMPLEX), "
            "and 'steps' (list of step objects with step_order, description, tool_name, tool_input, expected_output, risk_level, requires_approval)."
        )

        try:
            response = client.converse(
                modelId=self.model_id,
                messages=[{"role": "user", "content": [{"text": prompt}]}],
                inferenceConfig={"maxTokens": 1500, "temperature": 0.1}
            )
            text_out = response["output"]["message"]["content"][0]["text"]
            # Extract JSON block
            match = re.search(r'\{.*\}', text_out, re.DOTALL)
            if match:
                plan_json = json.loads(match.group(0))
                return plan_json
            raise ValueError("Bedrock model output could not be parsed as JSON plan.")
        except Exception as e:
            raise RuntimeError(f"Bedrock Planning Failure: {str(e)}")

    def test_connection(self) -> Dict[str, Any]:
        start = time.time()
        try:
            client = self._get_client()
            # Test small invocation or list operation
            client.converse(
                modelId=self.model_id,
                messages=[{"role": "user", "content": [{"text": "ping"}]}],
                inferenceConfig={"maxTokens": 5}
            )
            latency = (time.time() - start) * 1000
            return {
                "status": "CONNECTED",
                "is_real": True,
                "provider": "bedrock",
                "latency_ms": round(latency, 1),
                "details": f"Successfully connected to Amazon Bedrock ({self.model_id} in {self.region}).",
                "last_checked": datetime.now(timezone.utc).isoformat()
            }
        except NoCredentialsError:
            return {
                "status": "NOT_CONFIGURED",
                "is_real": False,
                "provider": "bedrock",
                "details": "AWS Credentials not detected in environment or ~/.aws/credentials. Local demo mode is active.",
                "last_checked": datetime.now(timezone.utc).isoformat()
            }
        except ClientError as ce:
            code = ce.response.get("Error", {}).get("Code", "ClientError")
            msg = ce.response.get("Error", {}).get("Message", str(ce))
            return {
                "status": "ERROR",
                "is_real": False,
                "provider": "bedrock",
                "details": f"AWS Bedrock {code}: {msg}",
                "last_checked": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "is_real": False,
                "provider": "bedrock",
                "details": f"Connection test failed: {str(e)}",
                "last_checked": datetime.now(timezone.utc).isoformat()
            }
