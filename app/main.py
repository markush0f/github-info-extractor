from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.domains.users.router import router as user_router
from app.domains.projects.router import router as project_router
from app.domains.entities.router import router as entity_router
from app.domains.embeddings.router import router as embedding_router

app = FastAPI()


@app.get("/health")
def health():
    return JSONResponse(content={"status": "ok"}, status_code=200)


app.include_router(user_router)
app.include_router(project_router)
app.include_router(entity_router)
app.include_router(embedding_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)
