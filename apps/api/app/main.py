from fastapi import FastAPI

from .routers.products import router as products_router


app = FastAPI(
    title="OpsPilot API",
    description="AI-powered operational intelligence platform",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(products_router)