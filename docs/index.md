# DevOps Boilerplates & Quick Reference

Welcome to the comprehensive, searchable documentation for DevOps templates, boilerplates, and quick reference guides. This repository contains production-ready templates for Terraform, Kubernetes, Docker Compose, Ansible, and more.

## :rocket: Quick Start

Get started in under 3 minutes:

=== "Install CLI"

    ```bash
    # Clone the repository
    git clone https://github.com/mlorentedev/boilerplates.git
    cd boilerplates

    # Install the bp CLI
    make install-cli

    # Search for templates
    bp search "spring boot"
    ```

=== "Browse Docs"

    ```bash
    # Start local documentation server
    make docs-serve

    # Open in browser
    open http://localhost:8000
    ```

=== "Generate Template"

    ```bash
    # Generate a new Spring Boot microservice
    bp new spring-boot-api my-service

    # Generate Terraform infrastructure
    bp new terraform-aws my-infra
    ```

## :mag: Fast Search

**Search for anything in < 100ms:** Use the search bar above (++ctrl+k++ or ++cmd+k++) to instantly find templates, commands, configurations, or troubleshooting guides.

Popular searches:

- [Docker Compose PostgreSQL](docker-compose/databases.md#postgresql)
- [Kubernetes Ingress](kubernetes/nginx-ingress.md)
- [Terraform AWS VPC](terraform/aws.md#vpc)
- [Ansible SSH Keys](ansible/ubuntu.md#ssh-keys)
- [Spring Boot Template](microservices/spring-boot.md)

## :books: Documentation Categories

<div class="grid cards" markdown>

-   :material-terraform:{ .lg .middle } __Terraform__

    ---

    Infrastructure as Code templates for AWS, Azure, DigitalOcean, Proxmox, and Kubernetes

    [:octicons-arrow-right-24: Terraform Docs](terraform/index.md)

-   :material-kubernetes:{ .lg .middle } __Kubernetes__

    ---

    Production-ready Kubernetes manifests for ArgoCD, Prometheus, Ingress, and more

    [:octicons-arrow-right-24: Kubernetes Docs](kubernetes/index.md)

-   :material-docker:{ .lg .middle } __Docker Compose__

    ---

    Complete Docker Compose stacks for databases, monitoring, CI/CD, and development

    [:octicons-arrow-right-24: Docker Compose Docs](docker-compose/index.md)

-   :material-ansible:{ .lg .middle } __Ansible__

    ---

    Automation playbooks for Ubuntu, Docker, Kubernetes, monitoring, and security

    [:octicons-arrow-right-24: Ansible Docs](ansible/index.md)

-   :material-github:{ .lg .middle } __GitHub Actions__

    ---

    CI/CD workflows for deployment, testing, and automation

    [:octicons-arrow-right-24: GitHub Actions Docs](github-actions/index.md)

-   :material-application:{ .lg .middle } __Microservices__

    ---

    Spring Boot and Quarkus microservice templates with Docker and Kubernetes

    [:octicons-arrow-right-24: Microservices Docs](microservices/index.md)

</div>

## :zap: Quick Commands

The `bp` CLI provides instant access to templates and documentation:

| Command | Description |
|---------|-------------|
| `bp search <query>` | Fuzzy search through all docs and snippets |
| `bp find <topic>` | Search specific category (terraform, k8s, docker, ansible) |
| `bp show <template>` | Display template documentation |
| `bp copy <snippet>` | Copy snippet to clipboard |
| `bp new <template> <name>` | Generate project from template |
| `bp web` | Open documentation in browser |
| `bp cheatsheet <topic>` | Generate PDF quick reference |
| `bp list` | List all available templates |
| `bp recent` | Show recently used templates |

## :fire: Popular Templates

### Infrastructure

- **[AWS VPC with EKS](terraform/aws.md#eks-cluster)** - Complete AWS infrastructure with VPC, EKS, and RDS
- **[Azure AKS Stack](terraform/azure.md#aks-cluster)** - Azure Kubernetes Service with networking and storage
- **[DigitalOcean K8s](terraform/digitalocean.md#kubernetes)** - DigitalOcean Kubernetes cluster with volumes

### Kubernetes

- **[ArgoCD GitOps](kubernetes/argocd.md)** - Complete GitOps setup with ArgoCD
- **[Prometheus Stack](kubernetes/prometheus-operator.md)** - Full observability with Prometheus, Grafana, and Alertmanager
- **[Nginx Ingress](kubernetes/nginx-ingress.md)** - Production-ready ingress controller with TLS

### Development

- **[Spring Boot API](microservices/spring-boot.md)** - RESTful API with OpenAPI, Docker, and Kubernetes
- **[PostgreSQL + Redis](docker-compose/databases.md)** - Development database stack
- **[Jenkins CI/CD](docker-compose/cicd.md)** - Complete CI/CD environment

### Automation

- **[Ubuntu Server Setup](ansible/ubuntu.md)** - Complete Ubuntu server provisioning
- **[Docker Installation](ansible/docker.md)** - Docker and Docker Compose setup
- **[Kubernetes Deployment](ansible/kubernetes.md)** - K8s cluster deployment and configuration

## :clipboard: Cheatsheets

Quick reference cards for common operations:

- [Docker Cheatsheet](cheatsheets/docker.md) - Essential Docker commands
- [Kubernetes Cheatsheet](cheatsheets/kubernetes.md) - kubectl and K8s operations
- [Terraform Cheatsheet](cheatsheets/terraform.md) - Terraform workflow and commands
- [Ansible Cheatsheet](cheatsheets/ansible.md) - Playbook execution and modules
- [Git Cheatsheet](cheatsheets/git.md) - Git workflows and commands

## :material-code-braces: Snippets Database

Browse copy-paste ready configurations:

- [Docker Snippets](snippets/docker.md) - Dockerfiles, compose files, networking
- [Kubernetes Snippets](snippets/kubernetes.md) - Deployments, services, ingress
- [Terraform Snippets](snippets/terraform.md) - Modules, providers, resources
- [Ansible Snippets](snippets/ansible.md) - Tasks, playbooks, roles
- [Bash Snippets](snippets/bash.md) - Shell scripts and one-liners

## :bulb: Features

### Instant Search
- **< 100ms response time** for any query
- Full-text search across all documentation
- Search suggestions and autocomplete
- Bilingual support (English/Spanish)
- Search result highlighting

### Copy-Paste Ready
- All code snippets have copy buttons
- Syntax highlighting for all languages
- Validated and tested configurations
- Related content suggestions

### Offline Capable
- Complete documentation works offline
- Cached search index
- No external dependencies
- Fast local development server

### Developer Friendly
- CLI tool with fuzzy search
- IDE integration (VS Code snippets)
- Terminal UI for browsing
- Shell autocomplete
- Git hooks for validation

## :hammer_and_wrench: Development

### Prerequisites

```bash
# Install dependencies
pip install mkdocs-material mkdocs-minify-plugin mkdocs-git-revision-date-localized-plugin
pip install mkdocs-awesome-pages-plugin

# Or use the Makefile
make setup
```

### Local Development

```bash
# Start documentation server with live reload
make docs-serve

# Build static documentation
make docs-build

# Run tests
make test

# Validate all templates
make validate
```

### Contributing

Contributions are welcome! Please see our [contributing guidelines](about.md#contributing) for details.

## :link: Resources

- [GitHub Repository](https://github.com/mlorentedev/boilerplates)
- [Personal Blog](https://mlorente.dev)
- [Dotfiles](https://github.com/mlorentedev/dotfiles)
- [Cheatsheets Collection](https://github.com/mlorentedev/cheat-sheets)

## :star: Support

If you find these templates useful:

- Star the repository on GitHub
- Share with your team
- Report issues or suggest improvements
- Contribute templates or documentation

---

**Last updated**: {{ git_revision_date_localized }}
