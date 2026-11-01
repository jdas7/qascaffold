## Registry change

- Template branch:
- Language:
- Framework:
- Test type:

## Checklist

- [ ] `registry/templates.yaml` lists the branch on `master`.
- [ ] Language, framework, and type are allowed by the registries.
- [ ] The template branch contains only the test project.
- [ ] `python scripts/validate_template.py --branch <name> --no-fetch` passed from `master`.
- [ ] This pull request does not merge the template project into `master`.
