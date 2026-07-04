from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TagPublic(BaseModel):
    id : int
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Nombre de etiqueta"
    )

    model_config = ConfigDict(from_attributes=True)

class TagCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Nombre de etiqueta"
    )


class TagUpdate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Nombre de etiqueta"
    )

class TagWithCount(TagPublic):
    uses: int
