from app.logger import logger
from app.services.github_client_service import GithubClientService
from app.utils.github_processor import normalize_repo, normalize_user


class GithubInfoService:

    def __init__(self) -> None:
        self.github_client = GithubClientService()
        logger.debug("GithubInfoService initialized")

    async def extract(self, username: str):
        logger.debug(f"Extracting GitHub data for user: {username}")

        user_raw = await self.github_client.get_user(username)
        logger.debug("User raw data fetched")

        repos_raw = await self.github_client.get_repos(username)
        logger.debug(f"Fetched {len(repos_raw)} repositories")

        user = normalize_user(user_raw)
        logger.debug("User normalized")

        main_readme = await self.github_client.get_readme(username, username)
        user["readme"] = main_readme
        logger.debug("User README processed")

        repos = []
        for repo in repos_raw:
            repo_data = await self._process_single_repo(username, repo)
            repos.append(repo_data)
            logger.debug(f"Processed repo: {repo_data['name']}")

        user["top_languages"] = self._compute_top_languages(repos)
        logger.debug("Top languages computed")

        logger.debug("Extraction process completed")
        return {"user": user, "repos": repos}

    async def _process_single_repo(self, username: str, repo: dict):
        repo_data = normalize_repo(repo)
        name = repo_data["name"]
        logger.debug(f"Processing repo: {name}")

        readme = await self.github_client.get_readme(username, name)
        logger.debug(f"README fetched for repo: {name}")

        languages = await self.github_client.get_repo_languages(username, name)
        logger.debug(f"Languages fetched for repo: {name}")

        branches = await self.github_client.get_branches(username, name)
        logger.debug(f"Branches fetched for repo: {name}")

        commit_count = await self.github_client.get_commit_count(username, name)
        logger.debug(f"Commit count fetched for repo: {name}")

        repo_data["readme"] = readme
        repo_data["languages"] = languages
        repo_data["branches"] = [b["name"] for b in branches]
        repo_data["commit_count"] = commit_count

        logger.debug(f"Repo processed: {name}")
        return repo_data

    def _compute_top_languages(self, repos: list):
        logger.debug("Computing total language usage")

        totals = {}
        for repo in repos:
            languages = repo.get("languages", {})
            for lang, value in languages.items():
                totals[lang] = totals.get(lang, 0) + value

        sorted_langs = dict(
            sorted(totals.items(), key=lambda item: item[1], reverse=True)
        )

        logger.debug("Language usage sorted")
        return sorted_langs
