from app.domains.users.models.user_language import UserLanguage


class UserLanguagesRepository:
    model_name = "User language"
    def __init__(self, session):
        self.session = session

    def create(self, item: UserLanguage):
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item
