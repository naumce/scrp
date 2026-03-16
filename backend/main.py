import argparse
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from db.database import init_db
from routers import projects as projects_router
from routers import search as search_router
from routers import businesses as businesses_router
from routers import enrichment as enrichment_router
from routers import export as export_router
from routers import settings as settings_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Local Biz Scraper API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(projects_router.router)
app.include_router(search_router.router)
app.include_router(businesses_router.router)
app.include_router(enrichment_router.router)
app.include_router(export_router.router)
app.include_router(settings_router.router)


@app.get("/health")
async def health():
    return {"status": "ok"}


def main():
    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=settings.port)
    parser.add_argument("--host", type=str, default=settings.host)
    parser.add_argument("--db-path", type=str, default=settings.db_path)
    args = parser.parse_args()

    settings.db_path = args.db_path

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
