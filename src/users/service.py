
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..auth import config, exceptions
from . import crud, schemas

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)

async def get_current_user(db: Session, security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    try:
        payload = jwt.decode(token, config.SECRET_KEY, config.JWT_ALGORITHM)
        payload_email = payload.get("email")
        payload_scope = payload.get("scope")

        token_data = schemas.JWTTokenData(email=payload_email, scopes=payload_scope)

    except (InvalidTokenError, ValidationError):
        raise exceptions.credentials_exception("Could not validate credentials", authenticate_value)

    for scope in security_scopes.scopes:
        if scope is not token_data.scope:
            raise exceptions.credentials_exception("User doesn't have enough privilege", authenticate_value)
        
    return crud.get_user_by_email(db=db, email=token_data.email)