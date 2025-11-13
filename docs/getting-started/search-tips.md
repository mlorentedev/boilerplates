# Search Tips & Tricks

Master the search functionality to find anything in < 3 seconds.

## Quick Access

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| ++ctrl+k++ or ++cmd+k++ | Open search |
| ++esc++ | Close search |
| ++up++ / ++down++ | Navigate results |
| ++enter++ | Go to result |
| ++ctrl+n++ / ++ctrl+p++ | Next/previous result |

### CLI Search

```bash
# Basic search
bp search "kubernetes ingress"

# Search with category filter
bp find terraform "aws vpc"

# Interactive search (uses fzf)
bp search

# Search recent history
bp search --recent
```

## Search Syntax

### Basic Search

Simple text search finds partial matches:

```
kubernetes        # Finds all Kubernetes content
docker compose    # Finds Docker Compose content
spring boot       # Finds Spring Boot templates
```

### Exact Phrases

Use quotes for exact matches:

```
"kubectl apply"        # Exact phrase
"docker-compose up"    # Exact command
```

### Boolean Operators

Combine search terms:

```
kubernetes AND ingress     # Must contain both
terraform OR ansible       # Contains either
docker NOT compose        # Contains docker but not compose
```

### Wildcards

Use wildcards for flexible matching:

```
kube*         # kubernetes, kubectl, etc.
*sql          # postgresql, mysql, etc.
spring-*-api  # spring-boot-api, spring-cloud-api, etc.
```

### Category Filters

Prefix search with category:

```
terraform:aws       # Only AWS Terraform templates
k8s:ingress        # Only Kubernetes ingress
ansible:ubuntu     # Only Ubuntu Ansible playbooks
docker:postgres    # Only PostgreSQL Docker configs
```

## Search Strategies

### Finding Templates

**By technology:**
```bash
bp search "spring boot"
bp search "terraform aws"
bp search "kubernetes prometheus"
```

**By purpose:**
```bash
bp search "microservice"
bp search "monitoring stack"
bp search "ci/cd pipeline"
```

**By component:**
```bash
bp search "postgres"
bp search "nginx ingress"
bp search "vpc"
```

### Finding Commands

**Docker commands:**
```bash
bp search "docker ps"
bp search "docker-compose logs"
bp search "build image"
```

**Kubernetes commands:**
```bash
bp search "kubectl get pods"
bp search "apply deployment"
bp search "port forward"
```

**Terraform commands:**
```bash
bp search "terraform plan"
bp search "state management"
bp search "module import"
```

### Finding Snippets

**Configuration snippets:**
```bash
bp search "docker-compose postgres"
bp search "kubernetes deployment"
bp search "terraform vpc"
```

**Code snippets:**
```bash
bp search "dockerfile java"
bp search "helm chart"
bp search "ansible task"
```

### Finding Troubleshooting

**Error messages:**
```bash
bp search "connection refused"
bp search "permission denied"
bp search "image pull error"
```

**Common issues:**
```bash
bp search "troubleshooting kubernetes"
bp search "debug docker"
bp search "terraform state"
```

## Advanced Features

### Fuzzy Search

The search is forgiving - you don't need exact matches:

| You type | Finds |
|----------|-------|
| `k8s` | Kubernetes |
| `tf` | Terraform |
| `ans` | Ansible |
| `dkr` | Docker |
| `spr boot` | Spring Boot |
| `postgre` | PostgreSQL |

### Tag Search

Search by tags:

```bash
# Using web interface
#monitoring     # All monitoring content
#database       # All database content
#security       # All security content

# Using CLI
bp search --tag monitoring
bp search --tag database
```

### Language Toggle

Search in Spanish or English:

```bash
# Web interface automatically detects language

# CLI language selection
bp search "base de datos"    # Spanish
bp search --lang es "kubernetes"

bp search "database"         # English
bp search --lang en "kubernetes"
```

### Recent Searches

```bash
# View recent searches
bp search --history

# Repeat last search
bp search !!

# Repeat specific search
bp search !3  # Repeat 3rd search from history
```

## Search Performance

### Optimization Tips

1. **Use specific terms**: "kubernetes ingress nginx" vs "k8s"
2. **Filter by category**: `bp find terraform "aws"`
3. **Use tags**: `bp search --tag monitoring`
4. **Limit results**: `bp search --limit 10 "docker"`

### Performance Benchmarks

Average search times:

| Search Type | Time |
|-------------|------|
| Simple keyword | < 20ms |
| Multiple terms | < 50ms |
| Complex boolean | < 80ms |
| Full-text | < 100ms |

### Cache

Search results are cached for better performance:

```bash
# Clear search cache
bp cache clear

# Rebuild search index
bp cache rebuild

# Show cache stats
bp cache stats
```

## Search Examples

### Example 1: Find Kubernetes Ingress Config

```bash
# Quick search
bp search "k8s ingress"

# Specific search
bp find kubernetes "nginx ingress"

# With tags
bp search --tag k8s --tag networking "ingress"
```

### Example 2: Find Database Setup

```bash
# General search
bp search "postgresql"

# Docker Compose
bp find docker-compose "postgres"

# Kubernetes
bp find kubernetes "database"

# Terraform
bp find terraform "rds"
```

### Example 3: Find Troubleshooting Guide

```bash
# Error message
bp search "pod crashloopbackoff"

# Problem description
bp search "kubernetes pod not starting"

# Category specific
bp find kubernetes "troubleshooting"
```

### Example 4: Find Related Content

```bash
# Search for main topic
bp search "spring boot"

# Results show related content:
# - Spring Boot template
# - Docker configuration
# - Kubernetes deployment
# - CI/CD pipeline
# - Monitoring setup
```

## CLI Interactive Mode

### Fuzzy Finder (fzf)

Interactive search with preview:

```bash
# Launch interactive search
bp search

# Or with initial query
bp search "kubernetes"

# Navigation:
# - Type to filter
# - Ctrl+N/P for next/previous
# - Enter to select
# - Ctrl+C to cancel
```

### Preview Panel

The fzf interface shows:
- Template name and category
- Description
- Related files
- Quick preview of content

### Multi-Select

Select multiple results:

```bash
# Enable multi-select
bp search --multi

# Navigation:
# - Tab to select/deselect
# - Enter to confirm
# - Ctrl+A to select all
```

## Integration

### Shell Integration

Add to your shell config for instant access:

```bash
# Bash/Zsh: Add to ~/.bashrc or ~/.zshrc
function bps() {
    local result=$(bp search "$@")
    if [ -n "$result" ]; then
        echo "$result"
        echo "$result" | pbcopy  # macOS
        # or: xclip -selection clipboard  # Linux
    fi
}

# Usage
bps "docker postgres"  # Search and copy to clipboard
```

### VS Code Integration

1. Install extension: `mlorentedev.boilerplates-snippets`
2. Use: ++ctrl+shift+p++ > "Boilerplates: Search"
3. Keyboard shortcut: ++ctrl+alt+b++

### Alfred/Ulauncher Integration

Create custom workflow:

```bash
# Alfred Workflow
keyword: bp {query}
script: /usr/local/bin/bp search "{query}"

# Ulauncher Extension
pip install ulauncher-boilerplates
```

## Tips for Speed

### 1. Use Shortcuts

Instead of full commands:

```bash
alias bps='bp search'
alias bpf='bp find'
alias bpc='bp copy'
```

### 2. Remember Common Searches

Create aliases for frequent searches:

```bash
alias bpk8s='bp find kubernetes'
alias bptf='bp find terraform'
alias bpdk='bp find docker'
```

### 3. Use Tab Completion

```bash
bp search ku[TAB]       # Completes to kubernetes
bp find ter[TAB]        # Completes to terraform
```

### 4. Leverage Recent

```bash
bp recent    # Show recent searches
bp recent 1  # Use most recent
```

### 5. Use Favorites

```bash
bp favorite add "kubernetes ingress"
bp favorite use ingress  # Quick access
```

## Troubleshooting Search

### No Results Found

```bash
# Check spelling
bp search "kubernets"  # Wrong
bp search "kubernetes"  # Correct

# Use fuzzy search
bp search "k8s"  # Works

# Try broader terms
bp search "ingress"  # Instead of "nginx-ingress-controller"
```

### Slow Search

```bash
# Rebuild index
bp cache rebuild

# Reduce scope
bp find kubernetes "ingress"  # Instead of bp search "ingress"

# Limit results
bp search --limit 10 "docker"
```

### Wrong Results

```bash
# Use exact phrases
bp search '"kubectl apply"'  # Exact match

# Use category filter
bp find terraform "apply"  # Only Terraform content

# Use tags
bp search --tag k8s "apply"  # Only K8s content
```

## Next Steps

- [Try the Quick Start Guide](quickstart.md)
- [Learn CLI Usage](cli-usage.md)
- [Browse Templates](../terraform/index.md)
- [Check Cheatsheets](../cheatsheets/index.md)

---

**Pro tip**: The more you use search, the better it gets at predicting what you need!
