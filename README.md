# DevOps Boilerplates with Fast Searchable Documentation

A comprehensive collection of production-ready templates and boilerplates for DevOps, infrastructure, and software development. Features a powerful CLI tool with fast search capabilities and extensive documentation.

## Features

- **Fast Search**: Find any template or documentation in under 100ms
- **CLI Tool**: Powerful `bp` command-line tool with fuzzy search integration
- **Comprehensive Documentation**: Detailed docs for all templates with MkDocs Material
- **Production-Ready**: All templates are tested and follow best practices
- **Multiple Categories**: Terraform, Kubernetes, Docker Compose, Ansible, and more
- **Copy-Paste Ready**: All code snippets are validated and ready to use

## Quick Start

### Installation

```bash
# One-line installation
curl -fsSL https://raw.githubusercontent.com/mlorentedev/boilerplates/main/scripts/install-bp.sh | bash

# Or clone and setup manually
git clone https://github.com/mlorentedev/boilerplates.git
cd boilerplates
make dev-setup
```

### Using the CLI

```bash
# Search for templates
bp search "kubernetes ingress"

# List templates by category
bp list terraform

# Generate a new project
bp new spring-boot-api my-service

# Open documentation
bp web

# Copy a snippet
bp copy docker-compose-postgres
```

### Browse Documentation

```bash
# Start documentation server
make docs-serve

# Open http://localhost:8000
```

## Available Templates

### Infrastructure as Code

**Terraform** - AWS, Azure, DigitalOcean, Proxmox, Kubernetes, Helm

**Kubernetes** - ArgoCD, Cert Manager, Nginx Ingress, Prometheus, Sealed Secrets, Longhorn, Velero

### Application Services

**Docker Compose** - Databases, Monitoring, CI/CD, Networking stacks

**Microservices** - Spring Boot and Quarkus templates with Docker and Kubernetes configs

### Automation

**Ansible** - Server setup, Docker installation, Kubernetes deployment, Security hardening

**GitHub Actions** - Deployment workflows and CI/CD pipelines

## bp CLI Tool

The `bp` CLI provides fast access to all templates and documentation.

### Main Commands

```bash
bp search <query>              # Search documentation and templates
bp find <category> <query>     # Search within a category
bp list [category]             # List available templates
bp show <template>             # Show template documentation
bp new <template> <name>       # Generate new project from template
bp copy <snippet>              # Copy snippet to clipboard
bp web                         # Open documentation in browser
bp recent                      # Show recently used items
```

### Search Performance

All search queries complete in under 100ms. Typical performance:

```
Query: 'kubernetes' - 5 results in 0.85ms
Query: 'docker postgres' - 5 results in 0.67ms
Query: 'terraform aws' - 5 results in 0.59ms
```

## Documentation

Complete documentation is available locally via:

```bash
make docs-serve
```

Quick links:
- [Getting Started](docs/getting-started/quickstart.md)
- [CLI Usage Guide](docs/getting-started/cli-usage.md)
- [Search Tips](docs/getting-started/search-tips.md)
- [Terraform Guide](docs/terraform/index.md)
- [Kubernetes Guide](docs/kubernetes/index.md)

## Development

### Prerequisites

- Python 3.8+
- Git
- fzf (optional, for interactive search)

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Setup development tools
make dev-setup

# Run tests
make test-all

# Serve documentation
make docs-serve
```

## Project Structure

```
boilerplates/
├── cli/                    # bp CLI tool
├── docs/                   # MkDocs documentation
├── snippets/               # Code snippet database
├── terraform/              # Terraform templates
├── kubernetes/             # Kubernetes manifests
├── docker-compose/         # Docker Compose files
├── ansible/                # Ansible playbooks
├── github-actions/         # GitHub Actions workflows
├── scripts/                # Installation scripts
├── Makefile                # Build automation
├── mkdocs.yml              # Documentation config
└── requirements.txt        # Python dependencies
```

## Contributing

Contributions are welcome. Please fork the repository and create a pull request with your changes or reach out directly.

Ensure all templates include:
- Working code/configuration
- Documentation
- Usage examples

## Resources

- **Repository**: [github.com/mlorentedev/boilerplates](https://github.com/mlorentedev/boilerplates)
- **Personal Site**: [mlorente.dev](https://mlorente.dev)
- **Dotfiles**: [github.com/mlorentedev/dotfiles](https://github.com/mlorentedev/dotfiles)
- **Cheatsheets**: [github.com/mlorentedev/cheat-sheets](https://github.com/mlorentedev/cheat-sheets)

## License

MIT License - see LICENSE file for details
