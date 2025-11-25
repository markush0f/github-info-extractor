from app.models.user import User


class GithubInfoService:

    def __init__(self) -> None:
        self.user: User
