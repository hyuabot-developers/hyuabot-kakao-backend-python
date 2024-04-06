import aiohttp
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import app_configs, settings
from schema.payload import Payload
from schema.response import SimpleTextResponse

app = FastAPI(**app_configs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=("DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"),
    allow_headers=settings.CORS_HEADERS,
)


@app.post("/healthcheck", include_in_schema=False, response_model=SimpleTextResponse)
async def healthcheck(_: Payload) -> dict:
    text = "API 서버 정상"
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{settings.API_URL}/healthcheck") as response:
            if response.status != 200:
                text = "API 서버 비정상"
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text,
                    },
                },
            ],
        },
    }
    return res
