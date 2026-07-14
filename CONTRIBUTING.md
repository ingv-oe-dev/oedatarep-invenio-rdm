# Contributing to OEDataRep

Thank you for your interest in contributing to OEDataRep.

OEDataRep is developed as an InvenioRDM-based application for the specific
needs of the INGV Osservatorio Etneo. Contributions that improve the project,
its documentation, accessibility, maintainability, or reuse are welcome.

## Before starting

For substantial changes, open or reference a GitHub issue before beginning
implementation. This helps clarify the expected result, avoid duplicated work,
and identify possible dependencies.

Small documentation fixes or clearly scoped maintenance changes may be proposed
directly through a pull request.

Do not include credentials, tokens, personal data, production configuration, or
other sensitive information in issues, commits, or pull requests.

## Development workflow

Changes must be developed on a dedicated branch and proposed through a pull
request targeting `main`.

A typical workflow is:

```console
git switch main
git pull --ff-only
git switch -c <branch-name>
```

Use a short, descriptive branch name. Common prefixes include:

- `feature/` for new functionality;
- `fix/` for bug fixes;
- `docs/` for documentation;
- `chore/` for maintenance and repository tasks.

Examples:

```text
feature/geographic-search
fix/react-leaflet
docs/contribution-guide
chore/update-ci
```

## Making changes

Keep each pull request focused on one logical change.

When applicable:

- follow the existing project structure and coding style;
- update documentation affected by the change;
- add or update tests when suitable tests exist;
- avoid unrelated formatting or refactoring;
- verify that no sensitive or environment-specific information is included;
- consider accessibility when changing user interfaces;
- include screenshots for relevant visual changes.

The exact InvenioRDM version and dependency constraints are defined by the
project dependency files.

## Local validation

Run the checks that are relevant to the change before opening a pull request.

Local development is managed with `invenio-cli`. Refer to the official
InvenioRDM documentation for current requirements and development procedures:

<https://inveniordm.docs.cern.ch/>

At minimum, confirm that the changed area behaves as expected and describe the
validation performed in the pull request.

GitHub Actions performs the repository's required automated checks. A pull
request cannot be merged until the required checks pass.

## Commits

Write clear commit messages that describe the purpose of the change.

Prefixes such as the following are encouraged but not mandatory:

```text
feat:
fix:
docs:
chore:
refactor:
test:
```

Intermediate commits may be used freely while developing a branch. Pull
requests are merged using **Squash and merge**, so the pull request title and
final squash commit message should clearly describe the complete change.

## Pull requests

A pull request should:

- explain what changed and why;
- reference related issues when applicable;
- describe how the change was tested;
- identify relevant impacts or limitations;
- include screenshots for visible interface changes;
- remain focused enough to be reviewed independently.

Before requesting review:

- ensure the branch is up to date with `main`;
- review the complete diff;
- remove debugging code and temporary files;
- verify that required checks pass;
- resolve relevant review conversations.

Direct pushes to `main` are not part of the normal development process.

## Review and merge

Reviewers may request clarification or changes before merge.

All review conversations must be resolved. When the branch is behind `main`,
it must be updated before merge so that the required checks run against the
current base branch.

The repository uses **Squash and merge**. This keeps one logical commit on
`main` for each pull request and maintains a linear project history.

## Reporting bugs

When reporting a bug, include enough information to reproduce and understand
the problem:

- expected behavior;
- actual behavior;
- steps to reproduce;
- relevant environment or version information;
- logs or screenshots, after removing sensitive information.

Search existing issues before opening a new one.

## Proposing enhancements

Enhancement requests should describe:

- the user or operational need;
- the expected result;
- relevant alternatives or existing behavior;
- possible compatibility or maintenance implications.

A comparison with another service may provide useful context, but the issue
should state the underlying OEDataRep requirement rather than only the observed
difference.

## Security

Do not report vulnerabilities, exposed credentials, or other sensitive
security issues through public GitHub issues.

Follow the repository security policy when a private reporting procedure is
available.
