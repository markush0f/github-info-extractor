from .reader import GitHubReader
from .processor import normalize_user, normalize_repo
from .logger import logger

class GitHubExtractor:
    def __init__(self):
        self.reader = GitHubReader()

    async def extract(self, username: str):
        user_raw = await self.reader.get_user(username)
        repos_raw = await self.reader.get_repos(username)

        user = normalize_user(user_raw)

        main_readme = await self.reader.get_readme(username, username)
        user["readme"] = main_readme

        repos = []
        for repo in repos_raw:
            repo_data = normalize_repo(repo)
            name = repo_data["name"]

            readme = await self.reader.get_readme(username, name)
            languages = await self.reader.get_repo_languages(username, name)

            repo_data["readme"] = readme
            repo_data["languages"] = languages
            repos.append(repo_data)

        return {
            "user": user,
            "repos": repos
        }

