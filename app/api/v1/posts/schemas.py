from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict

from typing import Optional, List, Literal


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
    tags: List[Tag] = Field(default_factory=list)
    # author: Optional[Author] = None

    @field_validator("title")
    @classmethod
    def not_allowed_titles(cls, value: str) -> str:
        if "spam" in value.lower():
            raise ValueError("Titulo spam")
        return value

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

class PaginatedPost(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
    order_by: Literal["id", "title"]
    direction: Literal["asc", "desc"]
    search: Optional[str] = None
    items: List[PostPublic]