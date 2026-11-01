# Python Pytest API

Plantilla de pruebas de API con Python, Pytest y Requests. El ejemplo consulta el recurso público de Charmander en PokeAPI.

## Requisitos

- Python 3.11 o superior.
- Acceso de red a PokeAPI durante la ejecución de las pruebas.

## Instalación

```bash
python -m pip install -r requirements.txt
```

## Configuración

La URL base se lee de la variable de entorno `POKEAPI_BASE_URL`. Si no está definida, las pruebas usan `https://pokeapi.co/api/v2`.

Copia el ejemplo y ajústalo si necesitas otro host:

```bash
copy .env.example .env
```

En PowerShell, carga la variable antes de ejecutar Pytest:

```powershell
Get-Content .env | ForEach-Object {
  if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
    Set-Item -Path "Env:$($Matches[1].Trim())" -Value $Matches[2].Trim()
  }
}
```

No guardes secretos en el repositorio. `.env` está ignorado por Git.

## Ejecutar las pruebas

```bash
pytest
```

El ejemplo solicita `GET {POKEAPI_BASE_URL}/pokemon/charmander` y comprueba que la respuesta sea 200, que el nombre sea `charmander`, que el id sea `4` y que el tipo incluya `fire`.

## Añadir pruebas

Coloca nuevos módulos en `tests/` con nombres `test_*.py`. Reutiliza el fixture `pokeapi_base_url` definido en `tests/conftest.py` para no fijar el host dentro de cada prueba.

## Limitaciones

Las pruebas dependen del servicio público de PokeAPI. Si el servicio no responde, la ejecución falla. Este ejemplo no autentica peticiones ni cubre otros recursos de la API.
