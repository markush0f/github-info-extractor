from pydantic import BaseModel
from typing import List, Union
import uuid

class SaveProjectLanguagesRequest(BaseModel):
    user_id: uuid.UUID
    projects: Union[str, List[uuid.UUID]] 
