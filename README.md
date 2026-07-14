# OEDataRep

OEDataRep is the open-access general-purpose research data repository of the
INGV Osservatorio Etneo.

This repository contains the OEDataRep application code and the graphical and
functional customizations developed on top of InvenioRDM for the specific needs
of the INGV Osservatorio Etneo.

- Public service: <https://oedatarep.ct.ingv.it/>
- InvenioRDM documentation: <https://inveniordm.docs.cern.ch/>

## Project status

OEDataRep is a production service under active development.

## Repository scope

This repository contains:

- the application-level configuration required by OEDataRep;
- user-interface and theme customizations;
- custom frontend and backend components;
- application assets and templates;
- local development and container build configuration;
- continuous integration and release workflows.

The repository is intended both as the source code of the OEDataRep
application and as a possible reference or starting point for institutions
implementing similar InvenioRDM customizations.

Some components, assets, configurations, and assumptions are specific to
OEDataRep and the INGV Osservatorio Etneo and may require adaptation before
reuse.

Production infrastructure and deployment-specific configuration are
maintained separately and are not included in this repository.

## Built with InvenioRDM

OEDataRep is based on
[InvenioRDM](https://inveniordm.docs.cern.ch/), an open-source research data
management repository platform.

This repository customizes an InvenioRDM instance rather than replacing the
upstream framework. General installation, architecture, configuration, and
upgrade concepts should therefore be read together with the official
InvenioRDM documentation.

OEDataRep aims to remain aligned with supported InvenioRDM releases. Version
compatibility is defined by the project dependency files and release history.

## Local development

Local development is managed with
[`invenio-cli`](https://inveniordm.docs.cern.ch/reference/cli/).

Refer to the official InvenioRDM documentation for current requirements,
installation, and local development procedures.

## Repository structure

| Path | Purpose |
|---|---|
| `app_data/` | Application data, vocabularies, and initialization resources |
| `assets/` | Frontend assets and source files used during the web build |
| `docker/` | Container-related configuration |
| `site/` | OEDataRep Python package, templates, and application customizations |
| `static/` | Static files served as-is |
| `Dockerfile` | Application image build definition |
| `Pipfile` | Python dependency declarations |
| `Pipfile.lock` | Locked Python dependency graph |
| `docker-compose.yml` | Services used by the local development environment |
| `docker-compose.full.yml` | Full container-based application stack |
| `docker-services.yml` | Shared Docker Compose service definitions |
| `invenio.cfg` | Main Invenio application configuration |
| `.invenio` | Version-controlled `invenio-cli` instance configuration |
| `.github/workflows/` | Continuous integration and release workflows |

## Continuous integration

Pull requests and changes to the default branch are validated through GitHub
Actions.

## Development workflow

Changes are developed on dedicated branches and proposed through pull
requests.

Direct pushes to the default branch are not part of the normal development
process.

## Production deployment

This repository does not contain the complete production deployment
configuration.

Production infrastructure, secrets, environment-specific settings, and
operational deployment procedures are maintained separately.

## Contributing

Contributions may be proposed through GitHub issues and pull requests.

## Security

Do not report vulnerabilities, exposed credentials, or other sensitive
security issues through public GitHub issues.

## License

The source code in this repository is licensed under the GNU General Public
License v3.0. See the [LICENSE](LICENSE) file for details.

Institutional names, logos, trademarks, datasets, and third-party assets may
be subject to separate terms and are not necessarily covered by the software
license.

## Maintainers

OEDataRep is maintained by the OEDataRep development team at the INGV
Osservatorio Etneo.
