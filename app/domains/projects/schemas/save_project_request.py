from pydantic import BaseModel
from typing import Union, List

class SaveProjectsRequest(BaseModel):
    projects: Union[str, List[str]]  # "all" or ["repo1", "repo2"]
