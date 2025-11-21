import base64

import httpx

from .github_client import GitHubClient
from .logger import logger

class GitHubReader:
    def __init__(self):
        self.client = GitHubClient()

    async def get_user(self, username: str):
        logger.info(f"Reading user: {username}")
        return await self.client.get_json(f"/users/{username}")

    async def get_repos(self, username: str):
        logger.info(f"Reading repositories for: {username}")
        return await self.client.get_json(f"/users/{username}/repos")

    async def get_repo_languages(self, username: str, repo: str):
        logger.info(f"Reading languages for repo: {repo}")
        return await self.client.get_json(f"/repos/{username}/{repo}/languages")

    async def get_readme(self, username: str, repo: str):
        logger.info(f"Decoding README for repo: {repo}")
        raw = await self.client.get_readme_raw(username, repo)
        if not raw:
            return None
        try:
            return base64.b64decode(raw).decode("utf-8", errors="ignore")
        except Exception as e:
            logger.error(f"Error decoding README for repo {repo}: {e}")
            return None
        
    async def get_branches(self, username: str, repo: str):
        return await self.client.get_json(f"/repos/{username}/{repo}/branches")

    async def get_commit_count(self, username: str, repo: str):
        endpoint = f"/repos/{username}/{repo}/commits?per_page=1"
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.client.base_url}{endpoint}", headers=self.client.headers)

            if response.status_code == 409:
                return 0

            response.raise_for_status()

            link = response.headers.get("Link", None)
            if not link:
                return 1

            parts = link.split(",")
            for part in parts:
                if 'rel="last"' in part:
                    url = part.split(";")[0].strip("<>")
                    query = url.split("?")[1]
                    params = query.split("&")
                    for p in params:
                        if p.startswith("page="):
                            return int(p.replace("page=", ""))

            return 1
        
    async def get_user_commits(self, username: str, repo_owner: str, repo: str):
        return await self.client.get_json(
            f"/repos/{repo_owner}/{repo}/commits?author={username}"
        )

    async def get_commit_detail(self, repo_owner: str, repo: str, sha: str):
        return await self.client.get_json(
            f"/repos/{repo_owner}/{repo}/commits/{sha}"
        )


