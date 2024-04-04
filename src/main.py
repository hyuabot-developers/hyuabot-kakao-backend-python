from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import app_configs, settings
from schema.payload import Payload

app = FastAPI(**app_configs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=("DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"),
    allow_headers=settings.CORS_HEADERS,
)


@app.post("/healthcheck", include_in_schema=False)
def healthcheck(_: Payload) -> dict[str, str]:
    return {"status": "ok"}
