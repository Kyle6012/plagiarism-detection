from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    # This is a placeholder for any startup logic,
    # like creating a database connection pool.
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # This is a placeholder for any shutdown logic,
    # like closing the database connection pool.
    pass
