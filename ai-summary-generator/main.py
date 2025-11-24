import os

from extract_data import list_projects, load_project_data
from summarizer import summarize_project, save_summary
from extract_data import save_languages_data, get_projects_languages

BASE_PATH = "../output/projects"
SUMMARY_PATH = "../output/summaries"
LANGUAGES_PATH = "../output/languages"

if __name__ == "__main__":
    project_paths = list_projects(BASE_PATH)

    for project_path in project_paths:
        project_name = os.path.basename(project_path)
        content = load_project_data(project_path)

        summary = summarize_project(content, "gpt-4o-mini")
        languages = get_projects_languages(project_path)

        save_summary(project_name, summary, SUMMARY_PATH)
        save_languages_data(project_name, languages, LANGUAGES_PATH)
        print(f"Summary generated for: {project_name}")
