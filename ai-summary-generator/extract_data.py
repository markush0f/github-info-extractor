import os
import json


def check_projects(base_path: str):
    if not os.path.exists(base_path):
        raise FileNotFoundError(f"Base path {base_path} does not exist")
    print(f"Base path {base_path} exists")


def load_project_data(project_path: str):
    json_path = os.path.join(project_path, "info.json")
    readme_file = os.path.join(project_path, "readme.md")

    collected = ""

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found at {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)
        collected += normalize_json(json_data)

    if os.path.exists(readme_file):
        with open(readme_file, "r", encoding="utf-8") as f:
            collected += normalize_readme(f.read())

    return collected


def list_projects(base_path: str):
    return [
        os.path.join(base_path, folder)
        for folder in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, folder))
    ]


def normalize_json(data: dict):
    text = "PROJECT METADATA:\n"
    for key, value in data.items():
        text += f"- {key}: {value}\n"
    text += "\n"
    return text


def normalize_readme(content: str):
    text = "README CONTENT:\n"
    text += content.strip() + "\n\n"
    return text


def get_projects_languages(project_path: str):
    json_path = os.path.join(project_path, "info.json")

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found at {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    languages_data = data.get("languages", {})

    languages = [
        {"language": lang, "bytes": count} for lang, count in languages_data.items()
    ]

    total_bytes = sum(languages_data.values()) if languages_data else 0
    for item in languages:
        item["percentage"] = (
            (item["bytes"] / total_bytes * 100) if total_bytes > 0 else 0
        )

    return languages


def save_languages_data(project_name: str, languages: list, output_path: str):
    os.makedirs(output_path, exist_ok=True)
    file_path = os.path.join(output_path, f"{project_name}_languages.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(languages, f, indent=4)
