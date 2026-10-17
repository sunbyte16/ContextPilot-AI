from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.all_models import User, Memory, AuditEvent
from app.schemas.memory import MemoryCreate, MemoryUpdate, MemoryResponse
from app.security.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=List[MemoryResponse])
def list_memories(
    category: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Memory).filter(Memory.user_id == current_user.id)
    if category:
        query = query.filter(Memory.category == category.upper())
    if search:
        query = query.filter(
            (Memory.title.ilike(f"%{search}%")) | (Memory.content.ilike(f"%{search}%"))
        )
    return query.order_by(Memory.is_pinned.desc(), Memory.updated_at.desc()).all()


@router.post("/", response_model=MemoryResponse)
def create_memory(
    mem_in: MemoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mem = Memory(
        user_id=current_user.id,
        category=mem_in.category.upper(),
        title=mem_in.title,
        content=mem_in.content,
        source_reference=mem_in.source_reference,
        is_pinned=mem_in.is_pinned or False
    )
    db.add(mem)

    audit = AuditEvent(
        user_id=current_user.id,
        event_type="MEMORY_MUTATED",
        resource_type="memory",
        action="create_memory",
        details={"title": mem.title, "category": mem.category}
    )
    db.add(audit)
    db.commit()
    db.refresh(mem)
    return mem


@router.put("/{memory_id}", response_model=MemoryResponse)
def update_memory(
    memory_id: str,
    mem_in: MemoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mem = db.query(Memory).filter(
        Memory.id == memory_id,
        Memory.user_id == current_user.id
    ).first()
    if not mem:
        raise HTTPException(status_code=404, detail="Memory not found")

    if mem_in.title is not None:
        mem.title = mem_in.title
    if mem_in.content is not None:
        mem.content = mem_in.content
    if mem_in.category is not None:
        mem.category = mem_in.category.upper()
    if mem_in.is_pinned is not None:
        mem.is_pinned = mem_in.is_pinned

    db.commit()
    db.refresh(mem)
    return mem


@router.delete("/{memory_id}")
def delete_memory(
    memory_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mem = db.query(Memory).filter(
        Memory.id == memory_id,
        Memory.user_id == current_user.id
    ).first()
    if not mem:
        raise HTTPException(status_code=404, detail="Memory not found")

    db.delete(mem)

    audit = AuditEvent(
        user_id=current_user.id,
        event_type="MEMORY_MUTATED",
        resource_type="memory",
        action="delete_memory",
        details={"title": mem.title}
    )
    db.add(audit)
    db.commit()
    return {"message": "Memory deleted successfully"}


@router.delete("/")
def clear_all_memories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    count = db.query(Memory).filter(Memory.user_id == current_user.id).delete()
    audit = AuditEvent(
        user_id=current_user.id,
        event_type="MEMORY_MUTATED",
        resource_type="memory",
        action="clear_all_memories",
        details={"deleted_count": count}
    )
    db.add(audit)
    db.commit()
    return {"message": f"Cleared {count} memory records successfully."}
