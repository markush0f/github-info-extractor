import argparse
import asyncio
from pathlib import Path
from extractor.extractor import GitHubExtractor
from extractor.exporter import save_json, save_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="GitHub username")
    args = parser.parse_args()

    async def wrapper():
        extractor = GitHubExtractor()
        result = await extractor.extract(args.username)

        user_output_dir = Path("output/user")
        projects_output_dir = Path("output/projects")

        save_json(result["user"], str(user_output_dir / "user.json"))

        user_readme = result["user"].get("readme")
        if user_readme:
            save_text(user_readme, str(user_output_dir / "readme.md"))

        for repo in result["repos"]:
            repo_dir = projects_output_dir / repo["name"]
            save_json(repo, str(repo_dir / "info.json"))

            readme = repo.get("readme")
            if readme:
                save_text(readme, str(repo_dir / "readme.md"))

        print("Extraction completed.")

    asyncio.run(wrapper())


if __name__ == "__main__":
    main()


# python3 main.py markush0f
