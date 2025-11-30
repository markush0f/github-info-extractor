import uuid
from fastapi import APIRouter, HTTPException
from app.domains.projects.schemas.save_project_languages_request import SaveProjectLanguagesRequest
from app.domains.projects.schemas.save_project_request import SaveProjectsRequest
from app.domains.projects.languages_service import ProjectLanguagesService
from app.domains.projects.service import ProjectService
from app.domains.projects.models.project import Project

router = APIRouter(prefix="/project", tags=["projects"])


@router.post("/", response_model=Project)
def create_project(
    user_id: uuid.UUID,
    repo_name: str,
    description: str,
    stars: int,
    forks: int,
    last_commit: str,
):
    service = ProjectService()
    return service.create_project(
        user_id, repo_name, description, stars, forks, last_commit
    )


@router.get("/", response_model=list[Project])
def list_projects(user_id: str):
    service = ProjectService()
    return service.list_projects(user_id)


@router.get("/{project_id}", response_model=Project)
def get_project(project_id: str):
    service = ProjectService()
    return service.get_project(project_id)


@router.patch("/{project_id}", response_model=Project)
def update_project(project_id: str, **fields):
    service = ProjectService()
    return service.update_project(project_id, **fields)


@router.delete("/{project_id}")
def delete_project(project_id: str):
    service = ProjectService()
    return service.delete_project(project_id)


@router.post("/summarize/all")
def summarize_all_projects():
    service = ProjectService()
    service.summarize_all_projects()


@router.post("/save")
async def save_projects(request: SaveProjectsRequest):

    project_service = ProjectService()

    selection = request.projects

    # Validate selection
    if not isinstance(selection, (str, list)):
        raise HTTPException(
            status_code=400,
            detail="Invalid selection type. Must be 'all' or list of project names.",
        )

    result = project_service.save_projects_to_db(selection)

    return result


@router.post("/single/languages")
def save_single_project_languages(project_id: str):
    service = ProjectLanguagesService()
    result = service.save_single_project_languages(project_id)
    return {
        "saved": len(result),
    }

@router.post("/languages/save")
def save_project_languages(data: SaveProjectLanguagesRequest):
    service = ProjectLanguagesService()
    
    total_saved = service.save_multiple_projects_languages(
        user_id=str(data.user_id),
        selection=data.projects
    )

    return {"total_saved": total_saved}