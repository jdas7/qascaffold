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

## Contenido de `main`

`main` contiene:
- Convenciones y especificación.
- Esquema JSON para validar `template.yaml`.
- Registros de tecnologías permitidas.
- Validador y workflow de GitHub Actions.
- Ejemplos de manifiestos.

Los proyectos de automatización se publican en ramas individuales, no en `main`.

## Crear un template

1. Lee `AGENTS.md`, `BRANCH_CONVENTION.md` y `TEMPLATE_SPEC.md`.
2. Comprueba que la combinación está permitida en `registry/`.
3. Crea una rama con el formato establecido.
4. Construye un proyecto funcional en la raíz de esa rama.
5. Añade `template.yaml` y `README.md`.
6. Ejecuta `python scripts/validate_template.py --branch <nombre-de-rama>`.
7. Abre un Pull Request hacia `main` siguiendo `CONTRIBUTING.md`.

## Validación local

Requiere Python 3.11+:

```bash
python -m pip install -r scripts/requirements.txt
python scripts/validate_template.py --branch python-pytest-api
```

El validador debe ejecutarse desde una copia local de la rama que se quiere validar. Para validación CI, el workflow descarga la rama origen del Pull Request y ejecuta el mismo validador.

## Contrato para consumidores

Los consumidores deben:
1. Resolver la rama por su nombre exacto.
2. Descargar el contenido de esa rama.
3. Leer `template.yaml` desde la raíz.
4. Validar que `template.id` y `technology` coincidan con el nombre de rama.
5. Rechazar el template si el manifiesto no cumple el contrato.

No se debe inferir la configuración del template analizando archivos arbitrarios ni depender de IA para interpretar su estructura.
