# qascaffold
Proyectos base de pruebas automatizadas.

---

# QA Automation Templates

Repositorio de templates reutilizables para proyectos de automatización QA.

Su responsabilidad es publicar templates versionados por ramas y definir un contrato estable que los consumidores (por ejemplo, un CLI) puedan interpretar.

## Cómo se identifica un template

Cada template vive en una rama cuyo nombre sigue:

`{language}-{framework}-{type}`

Ejemplos:
- `python-pytest-api`
- `python-appium-mobile`
- `typescript-playwright-e2e`

Cada rama de template debe contener un archivo `template.yaml` en su raíz. El nombre de la rama y los campos del manifiesto deben coincidir.

## Contenido de `master`

`master` contiene:
- Convenciones y especificación.
- Esquema JSON para validar `template.yaml`.
- Registros de tecnologías permitidas y el inventario `registry/templates.yaml`.
- Validador, listado de templates y workflow de GitHub Actions.
- Ejemplos de manifiestos.

Los proyectos de automatización viven en ramas individuales. Esas ramas no incluyen el código de `master`. No se fusionan en `master`: el registro de la rama se actualiza aquí y la rama se publica por separado.

## Crear un template

1. Lee `AGENTS.md`, `BRANCH_CONVENTION.md` y `TEMPLATE_SPEC.md`.
2. Comprueba que la combinación está permitida en `registry/`.
3. Crea una rama con el formato establecido y solo el proyecto de pruebas en su raíz.
4. Añade `template.yaml`, `README.md` y `.gitignore`.
5. En `master`, añade la rama a `registry/templates.yaml` con su lenguaje, framework y tipo.
6. Desde `master`, ejecuta `python scripts/validate_template.py --branch <nombre-de-rama>`.

## Validación local

Requiere Python 3.11+ y ejecutarse desde `master`:

```bash
python -m pip install -r scripts/requirements.txt
python scripts/list_templates.py
python scripts/validate_template.py
```

`list_templates.py` muestra los frameworks que ya tienen una rama publicada. `validate_template.py` descarga las ramas de origin y comprueba cada entrada de `registry/templates.yaml`. Para una sola rama:

```bash
python scripts/validate_template.py --branch python-pytest-api
```

`--no-fetch` usa las referencias que ya están en el clon.

## Contrato para consumidores

Los consumidores deben:
1. Resolver la rama por su nombre exacto.
2. Descargar el contenido de esa rama.
3. Leer `template.yaml` desde la raíz.
4. Validar que `template.id` y `technology` coincidan con el nombre de rama.
5. Rechazar el template si el manifiesto no cumple el contrato.

No se debe inferir la configuración del template analizando archivos arbitrarios ni depender de IA para interpretar su estructura.
