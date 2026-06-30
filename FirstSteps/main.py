import os
from datetime import datetime
from fastapi import FastAPI, Query, Body, HTTPException, Path, status, Depends
from fastapi.params import Depends
from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict
from typing import Optional, List, Union, Literal
from math import ceil
from sqlalchemy import create_engine, Integer, String, Text, DateTime, select, func, UniqueConstraint, ForeignKey, \
    Table, Column
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column, relationship, selectinload, joinedload
from dotenv import load_dotenv

#Definir la coneccion a SQL

##Cargar el .emv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///FirstSteps\\blog.db")

#
engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

#Configuraciones para sqlite
engine = create_engine(DATABASE_URL, echo=True, future=True, **engine_kwargs)

#crear una sesion por cada request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)

# Modelo de BD de SQLAlchemist
class Base(DeclarativeBase):
    pass

#tabla intermedia para relacion muchos a muchos
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True ),
        Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True )

)


#Clase que representa la tabla authors en SQLAlchemist
class AuthorORM(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100),unique=True, index=True)

    # relacion con tabla POST. relacion uno (autor) a muchos (posts)
    posts: Mapped[List["PostORM"]] = relationship(back_populates="author")


#tabnlla intermedia


class TagORM(Base):
    __tablename__ = "tags"

    # Relacion uno post a muchas etiquetas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, index=True)

    posts: Mapped[List["PostORM"]] = relationship(secondary=post_tags, back_populates="tags", lazy="selectin")

#Clase que representa la tabla post en SQLAlchemist
class PostORM(Base):
    __tablename__ = "posts"
    __table_args__ = (UniqueConstraint("title", name="posts_unique"),)
    #Mapped define el tipo de dato que tiene la columna
    #mapped_column permite definir los detalles del atributo
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    #Llave foranea
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("authors.id"))
    author: Mapped[Optional["AuthorORM"]] = relationship(back_populates="posts")

    tags: Mapped[List["TagORM"]] = relationship(
        secondary=post_tags,
        back_populates="posts",
        lazy="selectin",
        passive_deletes=True,
    )
Base.metadata.create_all(bind=engine) #crear tablas en caso de que no existan en DEV

#Iniciar sesion en DB
def get_db():
    db = SessionLocal()
    try:
        #yield, como return pero sin terminar la funcion
        yield db
    finally:
        db.close()



#Se instancia fastAPI
app = FastAPI(title="Mini Blog")

# BLOG_POST = [
#     {"id": 1, "title": "Hola con FastAPI", "content": "Mi primer post con FastAPI"},
#     {"id": 2, "title": "FastAPI", "content": "Mi segundo post con FastAPI", "tags": [{"name": "Python", "name": "FastAPI"}]},
#     {"id": 3, "title": "Bye FastAPI", "content": "Mi tercer post con FastAPI"},
#     {"id": 4, "title": "Hola con FastAPI", "content": "Mi primer post con FastAPI"},
#     {"id": 5, "title": "FastAPI", "content": "Mi segundo post con FastAPI"},
#     {"id": 6, "title": "Bye FastAPI", "content": "Mi tercer post con FastAPI", "tags": [{"name": "Python", "name": "FastAPI"}]},
#     {"id": 7, "title": "Hola con FastAPI", "content": "Mi primer post con FastAPI"},
#     {"id": 8, "title": "FastAPI", "content": "Mi segundo post con FastAPI"},
#     {"id": 9, "title": "Bye FastAPI", "content": "Mi tercer post con FastAPI"},
#     {"id": 10, "title": "Hola con FastAPI", "content": "Mi primer post con FastAPI"},
#     {"id": 11, "title": "FastAPI", "content": "Mi segundo post con FastAPI", "tags": [{"name": "Python", "name": "FastAPI"}]},
#     {"id": 12, "title": "Bye FastAPI", "content": "Mi tercer post con FastAPI"},
#     {"id": 13, "title": "Hola con FastAPI", "content": "Mi primer post con FastAPI"},
#     {"id": 14, "title": "FastAPI", "content": "Mi segundo post con FastAPI"},
#     {"id": 15, "title": "Bye FastAPI", "content": "Mi tercer post con FastAPI"},
#     {"id": 16, "title": "Hola con FastAPI", "content": "Mi primer post con FastAPI"},
#     {"id": 17, "title": "FastAPI", "content": "Mi segundo post con FastAPI"},
#     {"id": 18, "title": "Bye FastAPI", "content": "Mi tercer post con FastAPI"},
#     {"id": 19, "title": "Hola con FastAPI", "content": "Mi primer post con FastAPI"},
#     {"id": 20, "title": "FastAPI", "content": "Mi segundo post con FastAPI"}
# ]

class Tag(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Nombre de etiqueta"
    )

    model_config = ConfigDict(from_attributes=True)

class Author(BaseModel):
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

#estructura definida para cada recurso (post)
class PostBase(BaseModel):
    title: str
    content: str
    tags: Optional[List[Tag]] =  Field(default_factory=list)
    author: Optional[Author] = None

    model_config = ConfigDict(from_attributes=True)

class PostCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Titulo del post (minimo 3 caracteres, maximo 50)",
        examples=["Mi primer FastAPI"]
    )
    content: Optional[str] = Field(
        default="Contenido default",
        min_length=10,
        description="Contenido del post (minimo 10 caracteres)",
        examples=["Contenido valida con mas de 10 caracteres"]
    )
    #validaciones anidadas
    tags: Optional[List[Tag]] = Field(default_factory=list)
    author: Optional[Author] = None

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=50)
    content: Optional[str] = None

class PostPublic(PostBase):
    id: int
    #model_config sirve para que Pydantic entienda que la clase es un objeto de SQLAchemy
    model_config = ConfigDict(from_attributes=True)

class PostSummary(BaseModel):
    id: int
    title: str

    #validar objetos, no solo diccionarios
    model_config = ConfigDict(from_attributes=True)


class PostUpdate(BaseModel):
    title: str
    content: Optional[str] = None


class PaginatedPost(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
    order_by: Literal["id", "title"]
    direction: Literal["desc", "asc"]
    search: Optional[str] = None
    items: List[PostPublic]



#Mediante los 2 decoradores se accede a las validaciones personalizadas
#define el campo a validar
@field_validator("title")
#Permite manipular los valores a nivel de clase
@classmethod
def not_allowed_title(cls, value:str) -> str:
    ban_list = ["spam", "bot"]
    title_list = value.split(" ")
    for element in title_list:
        for post in ban_list:
            if post == element.lower():
                raise ValueError(f"El titulo no puede contener la palabra {element}")
    return value


#se ejecuta el servidor de fastapi
# fastapi dev .\main.py
#Con uvicorn
# uvicorn main:app --reload --port 8000
@app.get("/")
def home():
    return {"message": "Bienvenido a Mini Blog por Luis"}


##### GET ######
#al agregar response_model=List se define que se espera una lista de objetos PostPublic
@app.get("/posts", response_model=PaginatedPost)
#query param define como se quiere traer al recurso
def list_posts(
    text: Optional[str] = Query(
        default=None,
        deprecated=True,    #permite notifica via swagger que un query param dejara de funcionar proximamente
        description="Parametro obsoleto, usa 'query o search' en su lugar"
    ),

    query: Optional[str] = Query(
        default=None,
        description="Texto para buscar por titulo",
        alias="search", #personalizacion del parametro en URL
        min_length=3, #caracteres minimos en query
        max_length=50, #caracteres maximos en query
        pattern=r"^[\w\sáéíóúÁÉÍÓÚüÜ-]+$" #patrones de busqueda que cumplan ccon regex definido
    ),
    #paginacion
    per_page: int = Query(
        10,
        ge=1,
        le=50,
        description="Limite de resultados [1-50]"
    ),
    #offset desde que elemento se comienza a paginar
    page: int = Query(
        1, ge=1,description="Numero de pagina(mayor o igual a 1)"
    ),
    order_by: Literal["id", "title"] = Query(
        "id", description="Campo de orden"
    ),
    direction: Literal["desc", "asc"] = Query(
        "asc", description="Direccion de orden"
    ),
    db: Session = Depends(get_db)
):

    results = select(PostORM)

    query = query or text

    if query:
        results = results.where(PostORM.title.ilike(f"%{query}%"))
        # results = [post for post in results if query.lower() in post["title"].lower()]

    total = db.scalar(select(func.count()).select_from(results.subquery())) or 0
    # total = len(results)
    total_pages = ceil(total/per_page) if total > 0 else 0

    current_page = 1 if total_pages == 0 else min(page, total_pages)


    if order_by == "id":
        order_col = PostORM.id
    else:
        order_col = func.lower(PostORM.title)

    results = results.order_by(order_col.asc()  if direction == "asc" else order_col.desc())
    #results = sorted(results, key=lambda post: post[order_by], reverse=(direction == "desc"))

    if total_pages == 0:
        items: List[PostORM] = []
    else:
        start = (current_page - 1) * per_page
        items = db.execute(results.limit(per_page).offset(start)).scalars().all()
        # items = results[start:start + per_page]

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


##### GET ######
#El orden de los endpoint es importante y afecta en FastAPI
@app.get("/posts/by-tags", response_model=List[PostPublic])
def filter_by_tags(
    tags: List[str] = Query(
        ...,
        min_length=1,
        description="Etiquetas. Ejemplo: ?tags=phyton"
    ),
    db: Session = Depends(get_db)
):
    #Con BD
    #Normalizar tags
    normalized_tags_name = [tag.strip().lower() for tag in tags if tag.strip()]

    if not normalized_tags_name:
        return []

    #optimizar llamado de tags
    post_list = (
        select(PostORM)
        .options(
            selectinload(PostORM.tags),
            joinedload(PostORM.author),
        ).where(PostORM.tags.any(func.lower(TagORM.name).in_(normalized_tags_name)))
        .order_by(PostORM.id.asc())
    )

    posts = db.execute(post_list).scalars().all()

    return posts


    #sin bd
    # tags_lower = [tag.lower() for tag in tags]
    #
    # return [
    #     post for post in BLOG_POST if any(tag["name"].lower() in tags_lower for tag in post.get("tags", []))
    # ]


##### GET ######
#path param define el curso exacto que se necesita
#Union permite evaluar que la respuesta cumpla con varios modelos, adaptandose a la respuesta
@app.get("/posts/{post_id}", response_model=Union[PostPublic, PostSummary], response_description="Post encontrado")
def get_post(post_id: int = Path(
    #validaciones en el path (URL)
    ..., #obligatorio
    ge=1, #greater or equal
    title="ID del post",
    description="Identificador de la post, debe ser mayor a 1",
    example=1
), include_content: bool = Query(default=True, description="Incluir o no el contenido"), db: Session = Depends(get_db)):

    #con db
    post_find = select(PostORM).where(PostORM.id == post_id)
    post = db.execute(post_find).scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")

    if include_content:
        return PostPublic.model_validate(post, from_attributes=True)

    return PostSummary.model_validate(post, from_attributes=True)

    #sin db
    # for post in BLOG_POST:
    #     if post["id"] == post_id:
    #         if not include_content:
    #             return {"id": post["id"], "title": post["title"]}
    #         return post
    #return HTTPException(status_code=404, detail="Post no encontrado")


##### POST ######
@app.post("/posts", response_model=PostPublic, response_description="Post creado OK", status_code=status.HTTP_201_CREATED)
    #metodo condicionando a que cumpla con la estructura que establece la clase Post
    #model_dump transforma de objeto a diccionario
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    ##Flujo con BD
    author_obj = None
    if post.author:
        author_obj = db.execute(
            #conmsulta
            select(AuthorORM).where(AuthorORM.email == post.author.email)
        ).scalar_one_or_none()


        if not author_obj:
            author_obj = AuthorORM(name=post.author.name, email=post.author.email)
            db.add(author_obj)
            db.flush()

    new_post = PostORM(title=post.title, content=post.content, author=author_obj)

    for tag in post.tags:
        tag_obj = db.execute(
            select(TagORM).where(TagORM.name.ilike(tag.name))
        ).scalar_one_or_none()
        if not tag_obj:
            tag_obj = TagORM(name=tag.name)
            db.add(tag_obj)
            db.flush()

        new_post.tags.append(tag_obj)

    try:
        #Se marca la insercion a DB
        db.add(new_post)
        #$confirmar la informacion
        db.commit()
        #traer los valores metadata como created_at, id
        db.refresh(new_post)
        return new_post
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Titulo existente")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear post")

    ##Flujo sin BD
    # new_id = (BLOG_POST[-1]["id"] + 1) if BLOG_POST else 1
    # new_post = {"id": new_id,
    #             "title": post.title,
    #             "content": post.content,
    #             "tags": [tag.model_dump() for tag in post.tags],
    #             "author": post.author.model_dump() if post.author else None
    #             }
    # BLOG_POST.append(new_post)
    # return new_post


##### PUT ######
@app.put("/posts/{post_id}", response_model=PostPublic, response_description="Post actualizado", response_model_exclude_none=True)
def update_post(post_id: int, data: PostUpdate, db: Session = Depends(get_db)):
   #con BD
   post = db.get(PostORM, post_id)
   if not post:
       raise HTTPException(status_code=404, detail="Post no encontrado")
   updates = data.model_dump(exclude_unset=True)

   for key, value in updates.items():
       setattr(post, key, value)

   db.add(post)
   db.commit()
   db.refresh(post)
   return post

   #sin BD
    # for post in BLOG_POST:
    #     if post["id"] == post_id:
    #         playload = data.model_dump(exclude_unset=True)
    #         if "title" in playload: post["title"] = playload["title"]
    #         if "content" in playload: post["content"] = playload["content"]
    #         return post
    # #Indicar http code esperado
    #raise HTTPException(status_code=404, detail="Post no encontrado")

##### DELETE ######
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):

    #con BD
    post = db.get(PostORM, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")

    db.delete(post)
    db.commit()

    return

    #sin BD
    # for index, post in enumerate(BLOG_POST):
    #     if post["id"] == post_id:
    #         BLOG_POST.pop(index)
    #         return
    #raise HTTPException(status_code=404, detail="Post no encontrado")


