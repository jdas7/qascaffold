# Python Pytest API

Plantilla de pruebas de API con Python, Pytest, pytest-bdd y Requests.

## Requisitos

- Python 3.11 o superior.
- pytest-bdd, instalado con el resto de dependencias.
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
