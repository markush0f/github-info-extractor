from fastapi import HTTPException
from uuid import UUID


class RecordFinder:
    def __init__(self, repo):
        self.repo = repo

    def find_or_404(self, record_id: UUID):
        record = self.repo.get_by_id(record_id)
        if not record:
            raise HTTPException(
                status_code=404, detail=f"{self.repo.model_name} not found"
            )
        return record
