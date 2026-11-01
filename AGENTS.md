# Agent Instructions — QA Automation Templates

## Purpose and scope

This repository stores reusable QA automation project templates and the rules required to publish them.

## Before making changes

Read:

- `BRANCH_CONVENTION.md`
- `TEMPLATE_SPEC.md`
- `CONTRIBUTING.md`
- Relevant files under `registry/`
- `schemas/template.schema.json`

## Creating a template branch

1. Identify the requested language, framework, and test type.
2. Verify that each value exists in the registries.
3. Verify that the combination is explicitly allowed by `registry/frameworks.yaml`.
4. Construct the exact branch name: `{language}-{framework}-{type}`.
5. Check that the branch does not already exist. Never overwrite an existing template without explicit approval.
6. Create the branch from the approved base and add the complete project at its root.
7. Add `template.yaml` at the repository root.
8. Ensure `template.id` equals the branch name.
9. Ensure `technology.language`, `technology.framework`, and `technology.type` match the three branch segments.
10. Add a useful `README.md` with setup, configuration, and execution instructions.
11. Run the validator and relevant project tests before proposing publication.

## Git safety

- Never commit template project files directly to `main`.
- Never delete, rename, force-push, or overwrite an existing template branch without explicit approval.
- Do not change unrelated template branches.
- Do not put credentials, tokens, private keys, or real environment secrets in templates.
- Use placeholders and provide `.env.example` where configuration is needed.
- Do not claim a template is validated unless validation was actually run.

## Template quality

A template must be a usable starting project, not merely a collection of empty folders.
Include at least one representative test, dependency declaration, configuration example, and clear run instructions.
Avoid embedding customer-specific URLs, accounts, test data, or secrets.

## Change reporting

When finished, report:

- Branch name.
- Language, framework, and test type.
- Files added or changed.
- Validation commands executed and their actual results.
- Any known limitations.
