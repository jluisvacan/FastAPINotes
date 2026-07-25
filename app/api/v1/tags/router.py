from fastapi import APIRouter, status, HTTPException, Query
from fastapi.params import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.v1.tags.schemas import TagPublic, TagCreate, TagUpdate
from app.core.db import get_db
from app.core.security import get_current_user, require_admin, require_user, require_editor
from app.api.v1.tags.repository import TagRepository
from app.models import UserORM

router = APIRouter(prefix="/tags", tags=["tags"])



@router.get("", response_model=dict)
def list_tags(
    page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=100),
        order_by: str = Query("id", pattern="^(id|name)$"),
        direction: str = Query("asc", pattern="^(asc|desc)$"),
        search: str | None = Query(None),
        db: Session = Depends(get_db)
):

    repository = TagRepository(db)
    return repository.list_tags(page=page, per_page=per_page, order_by=order_by, direction=direction, search=search)

@router.post("", response_model=TagPublic, response_description="Post creato OK", status_code=status.HTTP_201_CREATED)
def create_tag(tag: TagCreate, db: Session = Depends(get_db), _editor: UserORM = Depends(require_editor)):

    repository = TagRepository(db)

    try:
        tag_create = repository.create_tag(name = tag.name)
        db.commit()
        db.refresh(tag_create)
        return tag_create
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear el tag")


@router.put("{/tag_id}", response_model=TagPublic, response_description="Post update OK", status_code=status.HTTP_200_OK)
def update_tag(
        tag_id: int,
        payload: TagUpdate,
        db: Session = Depends(get_db),
        _editor: UserORM = Depends(require_editor)
):
    repository = TagRepository(db)

    tag = repository.update(tag_id, name=payload.name)

    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.commit()
    return TagPublic.model_validate(tag)




@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
        tag_id: int,
        db: Session = Depends(get_db),
        _admin: UserORM = Depends(require_admin)
):
    repository = TagRepository(db)

    tag = repository.delete(tag_id)

    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.commit()

    return None


@router.get("/popular/top")
def get_most_popular(
        db: Session = Depends(get_db),
        _user: UserORM = Depends(require_user),
):
    repository = TagRepository(db)
    row = repository.most_popular()

    if not row:
        raise HTTPException(status_code=404, detail="Tag not found")

    return row