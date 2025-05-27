
import jwt, os
from passlib.context import CryptContext

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated
from pydantic_mongo import PydanticObjectId

from ..db import db
from ..models.auth import Token
from ..models.user import UserProfile, UserCredentials, UserRepository


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_credentials(credentials: UserCredentials) -> UserProfile:
    repo = UserRepository(db)
    user = repo.find_one_by(query={"email" : credentials.email})
    
    if(user is None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User is not found"
        )
    
    if(not pwd_context.verify(credentials.password, user.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    user = repo.to_model(user)
    
    return UserProfile(**user.model_dump())

async def get_user_by_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]) -> UserProfile:
  
    try:
        user = jwt.decode(jwt=credentials.credentials, key=SECRET_KEY, algorithms=[ALGORITHM])

    except jwt.exceptions.DecodeError as e:
        print(e) 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user