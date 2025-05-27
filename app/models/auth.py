from pydantic import BaseModel

class Token(BaseModel):
    access: str
    
class UserCredentials(BaseModel):
    email: str | None = None
    password: str | None = None