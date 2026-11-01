# Template Specification

## 1. Purpose

Define the required metadata and minimum quality bar for every template branch.

## 2. Required files

Every template branch must contain at its repository root:

- `template.yaml`: machine-readable metadata contract.
- `README.md`: human-readable setup and usage instructions.
- Dependency declaration appropriate to the language (for example `requirements.txt`, `pyproject.toml`, `pom.xml`, `build.gradle`, or `package.json`).
- At least one representative automated test.
- Configuration example appropriate to the framework.
- `.gitignore`.

Additional directories and files depend on the technology. Do not force every framework into an identical source layout.

## 3. Manifest location and identity

`template.yaml` must be at the root of the branch.

Required top-level properties:
- `schema_version`
- `template`
- `technology`
- `requirements`
- `project`

Identity rules:
- `template.id` must equal the branch name.
- `technology.language` must equal segment 1.
- `technology.framework` must equal segment 2.
- `technology.type` must equal segment 3.

## 4. Manifest format

See `examples/template.yaml` for a complete example and `schemas/template.schema.json` for the authoritative structural schema.

### Fields

- `schema_version`: version of this manifest contract, currently `"1.0"`.
- `template.id`: exact branch identifier.
- `template.name`: readable display name.
- `template.version`: semantic version of the template, independent of the branch name.
- `template.description`: short purpose statement.
- `technology.language`: registered language identifier.
- `technology.framework`: registered framework identifier.
- `technology.type`: registered test type.
- `requirements.runtime`: human-readable runtime constraint.
- `requirements.dependencies`: list of primary dependencies.
- `project.entry_point`: main test directory or entry point.
- `project.install_command`: documented install command.
- `project.test_command`: documented test command.

## 5. README requirements

The template README must explain:
1. What the template is for.
2. Prerequisites and supported runtime.
3. Installation steps.
4. Required environment variables and how to configure them.
5. How to execute tests.
6. How to add or organize tests.
7. Any limitations or external services required.

Never include real secrets. Provide `.env.example` with placeholders when needed.

## 6. Quality requirements

- The project must be executable after following its README.
- Include at least one meaningful example test.
- Pin or constrain dependencies appropriately.
- Keep credentials and environment-specific values outside source code.
- Use deterministic test data where practical.
- Explain any required browser, driver, emulator, device farm, or service setup.
- Do not include generated caches, build output, virtual environments, or local IDE state.

## 7. Compatibility

The language/framework/type combination must be allowed by `registry/frameworks.yaml`. A new combination requires a registry change on `master` before the template branch is published.

Every published branch is also listed in `registry/templates.yaml` with the same language, framework, and type. That inventory stays on `master`. The template branch contains only the test project.

## 8. Validation

Validation runs from `master` with `python scripts/validate_template.py`. The script reads each published branch through git. It does not require the template branch to contain the validator, registries, or schemas.

A template is publishable only when:
- Its branch name is valid.
- Its manifest passes the JSON Schema.
- Branch and manifest identity match.
- The combination is allowed by `registry/frameworks.yaml`.
- The branch is listed in `registry/templates.yaml`.
- Required files exist on that branch.
