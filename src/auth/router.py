from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from . import constants, schemas, service


router = APIRouter(
    prefix = "",
    tags = ["auth"],
)

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    #authenticate user
    user = service.authenticate_user(entered_email=form_data.username, entered_password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    #create access token
    access_token_expire_duration = timedelta(days=constants.ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = service.create_access_token(
        payload = {"email": form_data.username, "scope": user.status},
        expires_delta = access_token_expire_duration
    )

    return schemas.Token(access_token=access_token, token_type="bearer")