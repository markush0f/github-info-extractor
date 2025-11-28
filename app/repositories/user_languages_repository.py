from app.models.user_language import UserLanguage


class UserLanguagesRepository:
    def __init__(self, session):
        self.session = session

    def create(self, item: UserLanguage):
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item
