
import jwt, os

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from ..db import db

from ..models.user import User, UserProfile, UserRepository
from ..models.auth import Token

from ..dependencies.auth import get_user_by_credentials

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
async def login(user: Annotated[UserProfile, Depends(get_user_by_credentials)]) -> Token:
    model = user.model_dump()
    model['id'] = str(model['id'])

    tkn = jwt.encode(model, key=SECRET_KEY, algorithm=ALGORITHM)
    return {"access" : tkn}


@router.post("/sign-up")
async def sign_up(user: User) -> Token:
    repo = UserRepository(db)
    user.password = pwd_context.hash(user.password)
    if(not repo.create_user(user)):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="User with given email already exists"
        )
    
    model = UserProfile(**user.model_dump()).model_dump()
    model['id'] = str(model['id'])

    tkn = jwt.encode(model, key=SECRET_KEY, algorithm=ALGORITHM)
    return {'access' : tkn}

