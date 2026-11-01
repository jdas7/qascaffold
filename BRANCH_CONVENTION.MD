# Branch Convention

## Canonical format

Every template branch must use exactly three lowercase, hyphen-separated segments:

`{language}-{framework}-{type}`

Example: `python-pytest-api`

## Segment definitions

1. `language`: programming language, using a value from `registry/languages.yaml`.
2. `framework`: primary automation framework or tool identifier, using a value from `registry/frameworks.yaml`.
3. `type`: automation category, using a value from `registry/test-types.yaml`.

## Naming rules

- Use lowercase ASCII letters and digits only inside each segment.
- Use a single hyphen between segments.
- Exactly three segments are required.
- No spaces, underscores, slashes, versions, or descriptive suffixes.
- Do not put framework versions in branch names.
- Branch names are stable identifiers. A template's release version belongs in `template.yaml`.

## Examples

Valid:
- `python-pytest-api`
- `python-appium-mobile`
- `java-restassured-api`
- `java-appium-mobile`
- `typescript-playwright-e2e`

Invalid:
- `Python-Pytest-API`
- `python_pytest_api`
- `python-pytest`
- `python-pytest-api-v2`
- `python-pytest-mobile-e2e`

## Combination validity

A syntactically valid name is not automatically a supported template. The language/framework/type combination must be explicitly allowed in `registry/frameworks.yaml`.

## Main branch

`main` is reserved for repository governance: documentation, schemas, registries, scripts, and CI configuration. Do not publish a runnable template in `main`.
