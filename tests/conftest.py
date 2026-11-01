import os

import pytest

DEFAULT_POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"


@pytest.fixture(scope="session")
def pokeapi_base_url() -> str:
    configured = os.environ.get("POKEAPI_BASE_URL", DEFAULT_POKEAPI_BASE_URL)
    return configured.rstrip("/")
