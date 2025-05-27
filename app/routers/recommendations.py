

from fastapi import APIRouter, Depends

from pydantic import BaseModel

from ..models.activities import Activity

from ..dependencies.auth import get_user_by_token

from ..llm_modules.recommender import get_recommendations

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
    dependencies=[Depends(get_user_by_token)]
)

class UserPrompt(BaseModel):
    prompt: str

@router.post("/")
async def recommend(prompt: UserPrompt) -> list[Activity]:
    return get_recommendations(prompt)

