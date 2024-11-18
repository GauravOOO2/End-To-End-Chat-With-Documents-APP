from fastapi import FastAPI
from app.routes.documents import router as documents_router
from app.models.database import Base, engine

# Initialize FastAPI app
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(documents_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Document Management System!"}
