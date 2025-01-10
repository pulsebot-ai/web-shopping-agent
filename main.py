from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time
from routers.search import router as search_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Web Shopping Agent",
    description="AI Agent ready for web shopping",
    lifespan=lifespan,
    version="0.0.1",
)

origins = ['*']

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)


@app.get("/heartbeat", tags=["HeartBeat"])
async def heartbeat():
    return {"message": int(time.time())}


# Routes
app.include_router(search_router)
