import requests
from pytest_bdd import parsers, scenario, then, when


@scenario("charmander.feature", "Consultar el recurso público de Charmander")
def test_consultar_charmander() -> None:
    pass


@when(parsers.parse('se consulta el pokemon "{name}"'), target_fixture="pokemon_response")
def consultar_pokemon(name: str, pokeapi_base_url: str) -> requests.Response:
    return requests.get(f"{pokeapi_base_url}/pokemon/{name}", timeout=30)


@then(parsers.parse("la respuesta tiene estado {status:d}"))
def la_respuesta_tiene_estado(pokemon_response: requests.Response, status: int) -> None:
    assert pokemon_response.status_code == status


@then(parsers.parse('el nombre es "{name}"'))
def el_nombre_es(pokemon_response: requests.Response, name: str) -> None:
    assert pokemon_response.json()["name"] == name


@then(parsers.parse("el id es {pokemon_id:d}"))
def el_id_es(pokemon_response: requests.Response, pokemon_id: int) -> None:
    assert pokemon_response.json()["id"] == pokemon_id


@then(parsers.parse('los tipos incluyen "{pokemon_type}"'))
def los_tipos_incluyen(pokemon_response: requests.Response, pokemon_type: str) -> None:
    type_names = {slot["type"]["name"] for slot in pokemon_response.json()["types"]}
    assert pokemon_type in type_names
