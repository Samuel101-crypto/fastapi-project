from fastapi import FastAPI
from .router import post, user, auth
from .database import create_tables
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.on_event("startup")
def create_db_and_tables():
    create_tables()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup logic here")
    yield  # This allows the app to run
    print("Shutdown logic here")


@app.get("/")
def root():
    return {"message": "default message"}




