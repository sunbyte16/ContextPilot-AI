# Amazon Bedrock Developer & Agent Architecture Guide

## 1. Introduction
Amazon Bedrock is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies like AI21 Labs, Anthropic, Cohere, Meta, Mistral AI, Stability AI, and Amazon through a single API.

## 2. Agentic Task Decomposition
In ContextPilot AI, Amazon Bedrock is used as an intelligent reasoning and planning engine. The system passes user objectives and available registered tools to Bedrock, which generates structured, ordered execution plans with input parameter validation.

## 3. Human-In-The-Loop Security Policies
To ensure production safety:
- **Autonomous Safe Tools**: Pure mathematical calculations, server time querying, and document retrieval can execute autonomously.
- **Consequential Operations**: Data exports, database mutations, and notifications that affect external systems require explicit human approval via server-side gates.

## 4. Grounded Retrieval-Augmented Generation (RAG)
When users pose questions regarding indexed documents, the agent retrieves verbatim text passages and computes relevance rankings. If the indexed content does not contain sufficient evidence to answer the user's inquiry, the agent explicitly reports that evidence is insufficient, adhering to verifiable AI principles.
