import requests


def test_charmander(pokeapi_base_url: str) -> None:
    response = requests.get(f"{pokeapi_base_url}/pokemon/charmander", timeout=30)

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "charmander"
    assert body["id"] == 4
    type_names = {slot["type"]["name"] for slot in body["types"]}
    assert "fire" in type_names
