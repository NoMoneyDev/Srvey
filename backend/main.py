from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database_manager import DatabaseManager
from routes.user import router as user_router
from routes.auth import router as auth_router
from routes.survey import router as survey_router
from routes.question import router as question_router
from routes.response import router as response_router
from routes.answer import router as answer_router
from routes.analytics import router as analytics_router
from routes.admin import router as admin_router
from middleware import LoggingMiddleware
from logger import app_logger, debug_logger
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv
from models import User, Survey, Question, Response, Answer
import os


MONGODB_URI = os.getenv('DB_CONNECTION_STRING', 'mongodb://admin:password@localhost:27017')


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware (after CORS so it runs last in the chain)
app.add_middleware(LoggingMiddleware)


@app.on_event("startup")
async def startup():
    app_logger.info("Starting up Srvey backend...")
    
    client = AsyncIOMotorClient(MONGODB_URI)
    database = client["local"]

    await init_beanie(
        database=database,
        document_models=[User, Survey, Question, Response, Answer]
    )
    
    app_logger.info("✅ Database connection established")

    db_manager = DatabaseManager(client=client, db=database)
    app.state.db = db_manager
    
    app_logger.info("✅ Srvey backend started successfully")


@app.on_event("shutdown")
async def shutdown():
    app_logger.info("Shutting down Srvey backend...")


@app.get("/")
async def root():
    debug_logger.debug("Root endpoint accessed")
    return {"message": "Hello World"}


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(survey_router)
app.include_router(question_router)
app.include_router(response_router)
app.include_router(answer_router)
app.include_router(analytics_router)
app.include_router(admin_router)


if __name__ == "__main__":
    import uvicorn
    app_logger.info("Starting uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)