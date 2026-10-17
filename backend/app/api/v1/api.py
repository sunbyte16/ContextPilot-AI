from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    conversations,
    tasks,
    tools,
    memory,
    knowledge,
    activity,
    analytics,
    settings,
    demo,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["Conversations"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Agent Tasks & Planning"])
api_router.include_router(tools.router, prefix="/tools", tags=["Tools Registry"])
api_router.include_router(memory.router, prefix="/memory", tags=["Contextual Memory"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["Knowledge & RAG"])
api_router.include_router(activity.router, prefix="/activity", tags=["Activity & Audit"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Execution Analytics"])
api_router.include_router(settings.router, prefix="/settings", tags=["Settings & Integrations"])
api_router.include_router(demo.router, prefix="/demo", tags=["Demo Mode"])
