from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth_routes import router as auth_router
from app.routes.book_routes import router as book_router
from app.routes.user_routes import router as user_router
from app.routes.issue_routes import router as issue_router
from app.routes.stats_routes import router as stats_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(book_router, prefix="/books", tags=["Books"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(issue_router, prefix="/issues", tags=["Issues"])
app.include_router(stats_router, prefix="/stats", tags=["Stats"])


@app.get("/")
def home():
    return {"message": "Library Management System API is running!"}
