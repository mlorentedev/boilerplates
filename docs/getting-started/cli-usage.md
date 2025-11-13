# CLI Usage Guide

Complete reference for the `bp` command-line tool.

## Installation

See the [Installation Guide](installation.md) for detailed installation instructions.

## Global Options

```bash
bp [global options] <command> [command options] [arguments...]
```

| Option | Description |
|--------|-------------|
| `--version, -v` | Show version information |
| `--help, -h` | Show help |
| `--verbose` | Enable verbose output |
| `--quiet, -q` | Suppress output |
| `--config <file>` | Use custom config file |
| `--no-color` | Disable colored output |

## Commands

### search

Search through all documentation and snippets.

```bash
bp search [options] <query>
```

**Options:**

| Option | Description |
|--------|-------------|
| `--category, -c <cat>` | Filter by category (terraform, k8s, docker, ansible) |
| `--tag, -t <tag>` | Filter by tag |
| `--limit, -l <n>` | Limit results to n items (default: 20) |
| `--lang <lang>` | Search language (en, es) |
| `--recent` | Search recent history |
| `--history` | Show search history |
| `--multi` | Multi-select mode |

**Examples:**

```bash
# Basic search
bp search "kubernetes ingress"

# Category filtered search
bp search -c k8s "ingress"

# Tag filtered search
bp search -t monitoring "prometheus"

# Limit results
bp search -l 5 "docker"

# Interactive search with fzf
bp search

# Search with preview
bp search "terraform" --preview
```

### find

Search within a specific category.

```bash
bp find <category> [options] <query>
```

**Categories:**
- `terraform` or `tf`
- `kubernetes` or `k8s`
- `docker` or `dk`
- `ansible` or `ans`
- `github-actions` or `gh`

**Examples:**

```bash
# Find in Terraform
bp find terraform "aws vpc"
bp find tf "eks cluster"

# Find in Kubernetes
bp find kubernetes "ingress"
bp find k8s "deployment"

# Find in Docker
bp find docker "compose postgres"
bp find dk "network"

# Find in Ansible
bp find ansible "ubuntu setup"
bp find ans "docker install"
```

### show

Display documentation for a specific template.

```bash
bp show [options] <template>
```

**Options:**

| Option | Description |
|--------|-------------|
| `--raw` | Show raw markdown |
| `--preview` | Show preview only |
| `--copy` | Copy content to clipboard |

**Examples:**

```bash
# Show template documentation
bp show spring-boot-api

# Show with raw markdown
bp show --raw kubernetes-deployment

# Preview template
bp show --preview terraform-aws-vpc

# Show and copy to clipboard
bp show --copy docker-compose-postgres
```

### list

List all available templates.

```bash
bp list [options] [category]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--category, -c <cat>` | Filter by category |
| `--tag, -t <tag>` | Filter by tag |
| `--format, -f <fmt>` | Output format (table, json, yaml) |
| `--tree` | Show as tree structure |

**Examples:**

```bash
# List all templates
bp list

# List by category
bp list terraform
bp list -c k8s

# List by tag
bp list -t database

# Output as JSON
bp list -f json

# Show as tree
bp list --tree
```

### new

Generate a new project from a template.

```bash
bp new [options] <template> <name>
```

**Options:**

| Option | Description |
|--------|-------------|
| `--output, -o <dir>` | Output directory (default: current) |
| `--vars, -v <file>` | Variables file (YAML/JSON) |
| `--interactive, -i` | Interactive mode (prompts for variables) |
| `--dry-run` | Show what would be generated |
| `--force, -f` | Overwrite existing files |

**Examples:**

```bash
# Generate Spring Boot microservice
bp new spring-boot-api my-service

# Generate with custom output directory
bp new -o ./projects spring-boot-api my-service

# Generate with variables file
bp new -v vars.yaml terraform-aws-vpc my-vpc

# Interactive mode
bp new -i kubernetes-deployment my-app

# Dry run
bp new --dry-run spring-boot-api my-service

# Force overwrite
bp new -f spring-boot-api my-service
```

### copy

Copy a snippet to clipboard.

```bash
bp copy [options] <snippet>
```

**Options:**

| Option | Description |
|--------|-------------|
| `--preview` | Preview before copying |
| `--edit` | Edit before copying |
| `--format, -f <fmt>` | Output format (raw, json, yaml) |

**Examples:**

```bash
# Copy snippet
bp copy docker-compose-postgres

# Preview before copying
bp copy --preview kubernetes-deployment

# Edit before copying
bp copy --edit terraform-vpc

# Copy as JSON
bp copy -f json spring-boot-config
```

### web

Open documentation in web browser.

```bash
bp web [options] [page]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--port, -p <port>` | Server port (default: 8000) |
| `--no-open` | Don't open browser |
| `--build` | Build before serving |

**Examples:**

```bash
# Open documentation
bp web

# Open specific page
bp web terraform/aws

# Use custom port
bp web -p 8080

# Build and serve
bp web --build

# Start server without opening browser
bp web --no-open
```

### cheatsheet

Generate a cheatsheet for a topic.

```bash
bp cheatsheet [options] <topic>
```

**Options:**

| Option | Description |
|--------|-------------|
| `--format, -f <fmt>` | Output format (pdf, png, md, html) |
| `--output, -o <file>` | Output file |
| `--style, -s <style>` | Style theme (light, dark) |
| `--size, -z <size>` | Page size (a4, letter, a5) |

**Examples:**

```bash
# Generate Docker cheatsheet
bp cheatsheet docker

# Generate as PDF
bp cheatsheet -f pdf kubernetes

# Custom output file
bp cheatsheet -o k8s-cheat.pdf kubernetes

# Dark theme
bp cheatsheet -s dark docker

# Letter size
bp cheatsheet -z letter terraform
```

### recent

Show recently used templates and searches.

```bash
bp recent [options] [n]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--limit, -l <n>` | Show last n items (default: 10) |
| `--type, -t <type>` | Filter by type (search, template, all) |
| `--clear` | Clear recent history |

**Examples:**

```bash
# Show recent items
bp recent

# Show last 5 items
bp recent 5
bp recent -l 5

# Show only recent searches
bp recent -t search

# Show only recent templates
bp recent -t template

# Use most recent template
bp recent 1

# Clear history
bp recent --clear
```

### favorite

Manage favorite templates.

```bash
bp favorite <action> [template]
```

**Actions:**
- `add <template>` - Add to favorites
- `remove <template>` - Remove from favorites
- `list` - List all favorites
- `use <template> <name>` - Use favorite to create project

**Examples:**

```bash
# Add to favorites
bp favorite add spring-boot-api

# Remove from favorites
bp favorite remove spring-boot-api

# List favorites
bp favorite list

# Use favorite
bp favorite use spring-boot-api my-service
```

### cache

Manage search cache and index.

```bash
bp cache <action>
```

**Actions:**
- `clear` - Clear cache
- `rebuild` - Rebuild search index
- `stats` - Show cache statistics
- `clean` - Remove old cache files

**Examples:**

```bash
# Clear cache
bp cache clear

# Rebuild search index
bp cache rebuild

# Show statistics
bp cache stats

# Clean old files
bp cache clean
```

### config

Manage configuration.

```bash
bp config <action> [key] [value]
```

**Actions:**
- `get <key>` - Get configuration value
- `set <key> <value>` - Set configuration value
- `list` - List all configuration
- `reset` - Reset to defaults
- `edit` - Open config file in editor

**Examples:**

```bash
# Get configuration
bp config get editor

# Set configuration
bp config set editor "code"

# List all configuration
bp config list

# Reset to defaults
bp config reset

# Edit config file
bp config edit
```

### completion

Generate shell completion script.

```bash
bp completion <shell>
```

**Supported shells:**
- `bash`
- `zsh`
- `fish`
- `powershell`

**Examples:**

```bash
# Generate Bash completion
bp completion bash > /etc/bash_completion.d/bp

# Generate Zsh completion
bp completion zsh > /usr/local/share/zsh/site-functions/_bp

# Generate Fish completion
bp completion fish > ~/.config/fish/completions/bp.fish

# Generate PowerShell completion
bp completion powershell > $PROFILE
```

### update

Update bp CLI and templates.

```bash
bp update [options]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--check` | Check for updates without installing |
| `--version <ver>` | Update to specific version |
| `--templates` | Update only templates |
| `--cli` | Update only CLI |

**Examples:**

```bash
# Update everything
bp update

# Check for updates
bp update --check

# Update to specific version
bp update --version v1.5.0

# Update only templates
bp update --templates

# Update only CLI
bp update --cli
```

### version

Show version information.

```bash
bp version [options]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--check` | Check for newer version |
| `--verbose, -v` | Show detailed version info |

**Examples:**

```bash
# Show version
bp version

# Check for updates
bp version --check

# Show detailed version info
bp version -v
```

## Configuration

### Config File Location

The configuration file is located at:

- Linux/macOS: `~/.config/bp/config.yaml`
- Windows: `%APPDATA%\bp\config.yaml`

### Config File Format

```yaml
# Default editor for 'bp config edit' and 'bp copy --edit'
editor: vim

# Default output directory for 'bp new'
output_dir: ./

# Enable colored output
color: true

# Search settings
search:
  limit: 20
  category: all
  fuzzy: true

# Cache settings
cache:
  enabled: true
  ttl: 3600  # 1 hour

# Web server settings
web:
  port: 8000
  auto_open: true

# Favorites
favorites:
  - spring-boot-api
  - terraform-aws-vpc
  - kubernetes-deployment

# Recent limit
recent_limit: 10
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `BP_CONFIG` | Custom config file path |
| `BP_CACHE_DIR` | Custom cache directory |
| `BP_EDITOR` | Default editor |
| `BP_OUTPUT_DIR` | Default output directory |
| `BP_NO_COLOR` | Disable colored output |

## Examples

### Complete Workflows

#### 1. Deploy Microservice to Kubernetes

```bash
# Search for Spring Boot template
bp search "spring boot"

# Generate project
bp new spring-boot-api user-service

# Build and test
cd user-service
./mvnw clean package

# Find Kubernetes deployment template
bp find k8s "deployment"

# Generate Kubernetes manifests
bp new k8s-deployment user-service

# Deploy
kubectl apply -f k8s/
```

#### 2. Setup Infrastructure with Terraform

```bash
# List Terraform templates
bp list terraform

# Show AWS VPC template
bp show terraform-aws-vpc

# Generate infrastructure
bp new -i terraform-aws-vpc my-infrastructure

# Deploy
cd my-infrastructure
terraform init
terraform plan
terraform apply
```

#### 3. Create Development Environment

```bash
# Find Docker Compose stack
bp find docker "dev stack"

# Generate stack
bp new docker-compose-dev dev-env

# Start services
cd dev-env
docker-compose up -d

# Check status
docker-compose ps
```

## Tips & Tricks

### Use Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias bps='bp search'
alias bpf='bp find'
alias bpn='bp new'
alias bpc='bp copy'
alias bpl='bp list'
alias bpw='bp web'
```

### Pipe to Other Commands

```bash
# Copy snippet and save to file
bp copy docker-compose-postgres > docker-compose.yml

# Search and pipe to grep
bp search "kubernetes" | grep ingress

# List templates and count
bp list | wc -l
```

### Use with Watch

```bash
# Monitor documentation changes
watch -n 5 bp recent

# Monitor search results
watch -n 10 bp search "monitoring"
```

### Combine Commands

```bash
# Search, copy, and create file
bp copy $(bp search "dockerfile java" | head -1) > Dockerfile

# Find and generate in one line
bp new $(bp search "spring boot" | head -1) my-service
```

## Troubleshooting

### Command Not Found

```bash
# Check installation
which bp

# Reinstall
make install-cli

# Add to PATH
export PATH="$PATH:$HOME/.local/bin"
```

### Slow Performance

```bash
# Rebuild cache
bp cache rebuild

# Clear old cache
bp cache clean

# Check cache stats
bp cache stats
```

### Search Not Working

```bash
# Rebuild search index
bp cache rebuild

# Check search settings
bp config list

# Try with verbose mode
bp --verbose search "test"
```

## Getting Help

```bash
# General help
bp --help

# Command-specific help
bp search --help
bp new --help
bp copy --help

# Show examples
bp <command> --examples

# Show version
bp version -v
```

## Next Steps

- [Learn Search Tips](search-tips.md) for efficient searching
- [Browse Templates](../terraform/index.md) to see available templates
- [Check Cheatsheets](../cheatsheets/index.md) for quick reference

---

**Need help?** Run `bp --help` or visit the [GitHub repository](https://github.com/mlorentedev/boilerplates).
