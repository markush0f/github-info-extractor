import uuid
from fastapi import APIRouter, HTTPException
from app.domains.users import service
from app.infrastructure.github.github_info_service import GithubInfoService
from app.domains.users.languages_service import UserLanguagesService
from app.domains.users.service import UserService
from app.domains.users.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User)
def create_user(
    username: str,
    name: str,
    bio: str,
    avatar_url: str,
    github_username: str,
):
    service = UserService()
    return service.create_user(username, name, bio, avatar_url, github_username)


@router.get("/", response_model=list[User])
def list_users():
    service = UserService()
    return service.list_users()


@router.get("/{user_id}", response_model=User)
def get_user(user_id: str):
    service = UserService()
    return service.get_user(user_id)


@router.get("/github/info/{username}")
async def extract_info_github(username: str):
    user_service = UserService()
    github_service = GithubInfoService()

    internal_user = user_service.get_user_by_github(username)
    if not internal_user:
        raise HTTPException(404, "Internal user not found")

    return await github_service.extract(
        username=username, internal_user_id=str(internal_user.id)
    )

@router.post("/{user_id}/languages/save")
def save_user_languages(user_id: str):
    user_service = UserService()
    if not user_service.get_user_by_id(id=user_id):
        raise HTTPException(404, "Internal user not found")
    
    service = UserLanguagesService()
    result = service.save_user_languages(uuid.UUID(user_id))
    return {"saved": len(result)}