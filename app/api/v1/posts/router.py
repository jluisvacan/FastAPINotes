from math import ceil
from typing import Optional, List, Union, Literal, Annotated
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status, UploadFile, File
from app.core.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models import UserORM
from .schemas import PostPublic, PaginatedPost, PostUpdate, PostBase, PostSummary, PostCreate
from .repository import PostRepository
from app.core.security import oauth2_scheme, get_current_user, require_user, require_editor, require_admin
from app.services.file_storage import save_image
import time
import asyncio
import threading

router = APIRouter(prefix="/posts", tags=["posts"])

def get_fake_user():
    return {"username": "luis", "role": "admin"}

#funcion con dependencia, necesita resolver la dependencia para ejecutarse
@router.get("/me")
def read_me(user: dict = Depends(get_fake_user)):
    return {"user": user}

# #funcion sincrona
# @router.get("/sync")
# def sync_endpoint():
#     print("SYNC theread: ", threading.current_thread().name)
#     time.sleep(5)
#     return {"message": "Funcion sincrona termino"}
#
# #la palabra reservada async define una fyncion asincrona
# #await espera una respuesta
# @router.get("/async")
# async def sync_endpoint():
#     print("ASYNC theread: ", threading.current_thread().name)
#     await asyncio.sleep(5)
#     return {"message": "Funcion asincrona termino"}



@router.get("", response_model=PaginatedPost, response_description="Listado de posts")
def list_posts(
    text: Optional[str] = Query(
        default=None,
        deprecated=True,
        description="Parametro obsoleto, usa 'query o search' en su lugar"
    ),

    query: Optional[str] = Query(
        default=None,
        description="Texto para buscar por titulo",
        alias="search",
        min_length=3,
        max_length=50,
        pattern=r"^[\w\sáéíóúÁÉÍÓÚüÜ-]+$"
    ),
    per_page: int = Query(
        10,
        ge=1,
        le=50,
        description="Limite de resultados [1-50]"
    ),

    page: int = Query(
        1, ge=1,description="Numero de pagina(mayor o igual a 1)"
    ),
    order_by: Literal["id", "title"] = Query(
        "id", description="Campo de orden"
    ),
    direction: Literal["asc", "desc"] = Query(
        "asc", description="Direccion de orden"
    ),
    db: Session = Depends(get_db)
    ):

    repository = PostRepository(db)

    query = query or text

    total, items = repository.search(query, order_by, direction, page, per_page, )

    total_pages = ceil(total / per_page) if total > 0 else 0
    current_page = 1 if total_pages == 0 else min(page, total_pages)

    has_prev = current_page > 1
    has_next = current_page < total_pages if total_pages> 0 else False

    return PaginatedPost(
        page=current_page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        has_prev=has_prev,
        has_next=has_next,
        order_by=order_by,
        direction=direction,
        search=query,
        items=items
    )


@router.get("/by-tags", response_model=List[PostPublic])
def filter_by_tags(
        tags: List[str] = Query(
            ...,
            min_length=1,
            description="Etiquetas. Ejemplo: ?tags=phyton"
        ),
        db: Session = Depends(get_db)
):
    repository = PostRepository(db)

    return repository.by_tags(tags)



@router.get("/{post_id}", response_model=Union[PostPublic, PostSummary], response_description="Post encontrado")
def get_post(post_id: int = Path(
    ...,
    ge=1,
    title="ID del post",
    description="Identificador de la post, debe ser mayor a 1",
    example=1
), include_content: bool = Query(default=True, description="Incluir o no el contenido"),
        db: Session = Depends(get_db)):

    repository = PostRepository(db)
    post = repository.get(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")

    if include_content:
        return PostPublic.model_validate(post, from_attributes=True)

    return PostSummary.model_validate(post, from_attributes=True)



@router.post("", response_model=PostPublic, response_description="Post creado OK", status_code=status.HTTP_201_CREATED)
def create_post(post: Annotated[PostCreate, Depends(PostCreate.as_form)], image: Optional[UploadFile] = File(None),db: Session = Depends(get_db), _user: UserORM = Depends(require_user)):

    repository = PostRepository(db)
    saved = None

    try:
        if image is not None:
            saved = save_image(image)

        image_url = saved["url"] if saved else None

        post = repository.create_post(
            title=post.title,
            content=post.content,
            author=_user,
            category_id=post.category_id,
            tags=[tag.model_dump() for tag in post.tags],
            image_url=image_url
        )
        db.commit()
        db.refresh(post)
        return post
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Titulo existente")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear post")


@router.put("/{post_id}", response_model=PostPublic, response_description="Post actualizado", response_model_exclude_none=True)
def update_post(post_id: int, data: PostUpdate, db: Session = Depends(get_db), _editor: UserORM = Depends(require_editor)):

    repository = PostRepository(db)

    post = repository.get(post_id)

    if not post:
       raise HTTPException(status_code=404, detail="Post no encontrado")

    try:
        updates = data.model_dump(exclude_unset=True)
        post = repository.update_post(post, updates)
        db.commit()
        db.refresh(post)
        return post
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al actualizar post")




@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), _admin: UserORM = Depends(require_admin)):

    repository = PostRepository(db)

    post = repository.get(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")

    try:
        repository.delete(post)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al eliminar post")



@router.get("/secure")
def secure_endpoint(token: str = Depends(oauth2_scheme)):
    return {"message": "Acceso con token", "token recibido": token}