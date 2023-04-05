import logging

from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.settings import settings

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

app = FastAPI(title=settings.project_name, version=settings.app_version, debug=settings.debug,
              description=settings.project_description)

app.include_router(api_router, prefix=settings.app_v1_prefix)

if __name__ == "__main__":
    import uvicorn

    logging.info("Initializing server...")
    logging.info("Starting server at http://localhost:8000")
    logging.info("Swagger UI available at http://localhost:8000/docs")

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
