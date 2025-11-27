from app.logger import logger
from app.services.github_client_service import GithubClientService
from app.utils.github_processor import normalize_repo, normalize_user
from app.utils.file_writer import save_json, save_text


class GithubInfoService:

    def __init__(self) -> None:
        self.github_client = GithubClientService()

    async def extract(self, username: str, internal_user_id: str | None = None):
        logger.debug(f"Extracting GitHub data for user: {username}")

        user_raw = await self.github_client.get_user(username)
        repos_raw = await self.github_client.get_repos(username)

        user = normalize_user(user_raw)
        user["github_username"] = username
        user["id"] = internal_user_id  # Internal user id injected from router

        main_readme = await self.github_client.get_readme(username, username)
        user["readme"] = main_readme

        repos = []
        for repo in repos_raw:
            repo_data = await self._process_single_repo(username, repo)

            # Attach internal user id to repo
            repo_data["user_id"] = internal_user_id

            repos.append(repo_data)

        top_languages = self._compute_top_languages(repos)
        user["top_languages"] = top_languages

        # Save user
        save_json(user, "output/user/user.json")
        if main_readme:
            save_text(main_readme, "output/user/readme.md")

        # Save languages
        save_json(top_languages, "output/languages/top_languages.json")

        # Save repos
        for repo in repos:
            name = repo["name"]
            base = f"output/projects/{name}"

            save_json(repo, f"{base}/repo.json")

            if repo.get("readme"):
                save_text(repo["readme"], f"{base}/readme.md")

            save_json(repo.get("languages", {}), f"{base}/languages.json")

        return {"user": user, "repos": repos}


    async def _process_single_repo(self, username: str, repo: dict):
        repo_data = normalize_repo(repo)
        name = repo_data["name"]

        readme = await self.github_client.get_readme(username, name)
        languages = await self.github_client.get_repo_languages(username, name)
        branches = await self.github_client.get_branches(username, name)
        commit_count = await self.github_client.get_commit_count(username, name)

        repo_data["readme"] = readme
        repo_data["languages"] = languages
        repo_data["branches"] = [b["name"] for b in branches]
        repo_data["commit_count"] = commit_count

        return repo_data

    def _compute_top_languages(self, repos: list):
        totals = {}
        for repo in repos:
            languages = repo.get("languages", {})
            for lang, value in languages.items():
                totals[lang] = totals.get(lang, 0) + value

        sorted_langs = dict(
            sorted(totals.items(), key=lambda item: item[1], reverse=True)
        )
        return sorted_langs
