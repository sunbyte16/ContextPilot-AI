import re
from typing import Dict, Any, Optional, List
from app.tools.base import BaseTool


class StructuredSummarizerTool(BaseTool):
    tool_id = "structured_summarizer"
    name = "Structured Summarizer & Synthesizer"
    description = "Generates structured summaries, key takeaways, action items, and risk points from text."
    version = "1.0.0"
    risk_level = "LOW"
    requires_approval = False
    implementation_type = "local"

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text or passages to summarize"
                },
                "max_takeaways": {
                    "type": "integer",
                    "default": 4,
                    "description": "Maximum number of key takeaways"
                }
            },
            "required": ["text"]
        }

    def get_output_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "executive_summary": {"type": "string"},
                "key_takeaways": {"type": "array"},
                "action_items": {"type": "array"},
                "identified_limitations": {"type": "array"},
                "word_count": {"type": "integer"}
            }
        }

    def execute(self, params: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        text = params.get("text", "").strip()
        max_takeaways = params.get("max_takeaways", 4)
        if not text:
            raise ValueError("Input 'text' cannot be empty.")

        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 10]
        words = text.split()
        word_count = len(words)

        # Extractive synthesis
        executive_summary = " ".join(sentences[:2]) if sentences else text[:200]

        # Extract sentences with action keywords or emphasis
        action_keywords = ["must", "should", "need to", "action", "implement", "deploy", "create", "execute"]
        action_items = []
        for s in sentences:
            if any(kw in s.lower() for kw in action_keywords):
                action_items.append(s.strip(" -*#"))
                if len(action_items) >= 3:
                    break
        if not action_items and len(sentences) > 2:
            action_items = [f"Review: {sentences[1]}"]

        takeaways = []
        for s in sentences[:max_takeaways]:
            takeaways.append(s.strip(" -*#"))

        # Detect gaps / limitations
        limitations = []
        if word_count < 30:
            limitations.append("Source text has limited depth; additional context recommended.")
        if "todo" in text.lower() or "tbd" in text.lower():
            limitations.append("Pending placeholder items detected in source text.")

        return {
            "success": True,
            "executive_summary": executive_summary,
            "key_takeaways": takeaways,
            "action_items": action_items,
            "identified_limitations": limitations if limitations else ["No obvious ambiguities detected in the provided excerpt."],
            "word_count": word_count
        }
