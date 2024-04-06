import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient

from main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[TestClient, None]:
    """Create an instance of the test client for each test case."""
    host, port = "127.0.0.1", "38000"
    scope = {"client": (host, port)}

    async with TestClient(app, scope=scope) as client:
        yield client
