
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, PydanticObjectId


class UserBase(BaseModel):
    pass

class UserCredentials(UserBase):
    email: str 
    password: str 

class UserProfile(UserBase):
    id: PydanticObjectId | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str

class User(UserProfile, UserCredentials):
    pass

class UserRepository(AbstractRepository[User]):
    class Meta:
        collection_name = "users"

    def create_user(self, user: User):
        if(not self.find_one_by({"email" : user.email}) is None):
            return False
        self.save(user)
        return True
        