from sqlmodel import Session, select
from app.domains.users.models.user import User


class UserRepository:
    model_name = "User"
    # Stores a session for database operations
    def __init__(self, session: Session):
        self.session = session

    # Saves a user to the database
    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    # Gets a user using its ID
    def get_by_id(self, user_id: str):
        return self.session.get(User, user_id)

    # Gets a user using its username
    def get_by_username(self, username: str):
        statement = select(User).where(User.username == username)
        return self.session.exec(statement).first()

    # Gets all users
    def get_all(self):
        statement = select(User)
        return self.session.exec(statement).all()


    def get_by_github_username(self, github_username: str):
        statement = select(User).where(User.github_username == github_username)
        result = self.session.exec(statement).first()
        return result
