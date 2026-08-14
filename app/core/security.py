import os
from datetime import timedelta, timezone, datetime
from typing import Optional, Literal

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt import PyJWTError
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.models import UserORM

from app.api.v1.auth.repository import UserRepository



password_hash = PasswordHash.recommended()
#los tokens se obtienen del endpoint definido
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autenticado",
        headers={"WWW-Authenticate": "Bearer"}
    )




def raise_expire_token():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expirado",
        headers={"WWW-Authenticate": "Bearer"}
    )




def raise_forbidden():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permisos suficientes"
    )


def invalid_credentials():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales invalidas"
    )


def decode_token(token: str) -> dict:
    payload = jwt.decode(token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

    return payload


# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     expire = datetime.now(tz=timezone.utc) + (expires_delta or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     token = jwt.encode(payload=to_encode, key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
#
#     return token

def create_access_token(sub: str, minutes: int | None = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes or settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {
            "sub": sub,
            "exp": expire
        },
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )


async def get_current_user(db: Session = Depends(get_db),
                           token: str = Depends(oauth2_scheme)) -> UserORM:

    try:
        payload = decode_token(token)
        sub: Optional[str] = payload.get("sub")
        if not sub:
            # manejo de errores como variable
            raise credentials_exc

        user_id = int(sub)

    except ExpiredSignatureError:
        # manejo de errores como funcion
        raise raise_expire_token()
    except InvalidTokenError:
        # manejo de errores explicito
        raise HTTPException(status_code=401, detail="Token Invalido")
    except PyJWTError:
        raise invalid_credentials()

    user = db.get(UserORM, user_id)

    if not user or not user.is_active:
        raise invalid_credentials()

    return user


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)



def require_role(min_role: Literal["user", "editor", "admin"]):
    order = {"user": 0, "editor": 1, "admin": 2}

    def evaluation(user: UserORM = Depends(get_current_user)) -> UserORM:
        if order[user.role] < order[min_role]:
            raise raise_forbidden()
        return user

    return evaluation



async def auth2_token(form: OAuth2PasswordRequestForm =Depends(), db: Session = Depends(get_db)):
    repository = UserRepository(db)
    user = repository.get_by_email(form.username)
    if not user or not verify_password(form.password, user.hash_password):
        raise invalid_credentials()
    token = create_access_token(sub=str(user.id))
    return {"access_token": token, "token_type": "bearer"}

require_user = require_role("user")
require_editor = require_role("editor")
require_admin = require_role("admin")