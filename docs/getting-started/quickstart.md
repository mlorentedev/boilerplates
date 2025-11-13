# Quick Start Guide

Get started with the boilerplates repository in under 5 minutes.

## Installation

### Option 1: Direct Clone

```bash
# Clone the repository
git clone https://github.com/mlorentedev/boilerplates.git
cd boilerplates

# Install dependencies
make setup

# Install the bp CLI tool
make install-cli

# Verify installation
bp --version
```

### Option 2: Using Docker

```bash
# Pull the Docker image
docker pull ghcr.io/mlorentedev/boilerplates:latest

# Run the documentation server
docker run -p 8000:8000 ghcr.io/mlorentedev/boilerplates:latest

# Access documentation at http://localhost:8000
```

### Option 3: Direct CLI Installation

```bash
# Download and install bp CLI directly
curl -fsSL https://raw.githubusercontent.com/mlorentedev/boilerplates/main/scripts/install-bp.sh | bash

# Or using wget
wget -qO- https://raw.githubusercontent.com/mlorentedev/boilerplates/main/scripts/install-bp.sh | bash

# Verify installation
bp --version
```

## First Steps

### 1. Explore Available Templates

```bash
# List all available templates
bp list

# Search for specific templates
bp search "kubernetes"

# Show details of a template
bp show spring-boot-api
```

### 2. Generate Your First Project

```bash
# Create a Spring Boot microservice
bp new spring-boot-api my-awesome-api

# Navigate to the project
cd my-awesome-api

# Run the project
./mvnw spring-boot:run
```

### 3. Browse Documentation

```bash
# Start the documentation server
make docs-serve

# Or using bp CLI
bp web

# Documentation will be available at http://localhost:8000
```

### 4. Search Documentation

Use the search bar (++ctrl+k++ or ++cmd+k++) to find anything instantly:

- Type partial words: `k8s ing` finds Kubernetes Ingress
- Use categories: `terraform aws` finds AWS Terraform templates
- Search commands: `docker ps` finds Docker commands
- Find snippets: `postgres` finds PostgreSQL configurations

## Common Use Cases

### Deploy a Microservice to Kubernetes

```bash
# 1. Generate Spring Boot microservice
bp new spring-boot-api user-service

# 2. Build Docker image
cd user-service
docker build -t user-service:latest .

# 3. Generate Kubernetes manifests
bp new k8s-deployment user-service

# 4. Deploy to Kubernetes
kubectl apply -f k8s/
```

### Setup Infrastructure with Terraform

```bash
# 1. Generate Terraform AWS infrastructure
bp new terraform-aws my-infrastructure

# 2. Configure variables
cd my-infrastructure
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# 3. Deploy infrastructure
terraform init
terraform plan
terraform apply
```

### Setup Development Environment

```bash
# 1. Generate Docker Compose stack
bp new docker-compose-dev dev-stack

# 2. Start services
cd dev-stack
docker-compose up -d

# 3. Check services
docker-compose ps

# Services available:
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
# - PgAdmin: localhost:8080
```

### Automate Server Setup with Ansible

```bash
# 1. Configure inventory
cat > inventory.ini <<EOF
[servers]
server1 ansible_host=192.168.1.10
server2 ansible_host=192.168.1.11
EOF

# 2. Copy SSH key
bp copy ansible-ssh-key > add-ssh-key.yml

# 3. Run playbook
ansible-playbook -i inventory.ini add-ssh-key.yml
```

## CLI Tips

### Fuzzy Search

The `bp` CLI uses fuzzy search - you don't need exact matches:

```bash
# All of these find the same Spring Boot template:
bp search "spring boot"
bp search "spr boot"
bp search "sb api"
```

### Recent Templates

```bash
# Show recently used templates
bp recent

# Use a recent template again
bp recent 1  # Use the most recent template
```

### Favorites

```bash
# Add a template to favorites
bp favorite add spring-boot-api

# List favorites
bp favorite list

# Generate from favorite
bp favorite use spring-boot-api my-new-service
```

### Copy to Clipboard

```bash
# Copy a snippet directly to clipboard
bp copy docker-compose-postgres

# Then paste where needed
# Ctrl+V or Cmd+V
```

## Shell Integration

### Bash

Add to `~/.bashrc`:

```bash
# bp CLI autocomplete
eval "$(bp completion bash)"

# Aliases
alias bps='bp search'
alias bpn='bp new'
alias bpw='bp web'
```

### Zsh

Add to `~/.zshrc`:

```bash
# bp CLI autocomplete
eval "$(bp completion zsh)"

# Aliases
alias bps='bp search'
alias bpn='bp new'
alias bpw='bp web'
```

### Fish

Add to `~/.config/fish/config.fish`:

```fish
# bp CLI autocomplete
bp completion fish | source

# Aliases
alias bps='bp search'
alias bpn='bp new'
alias bpw='bp web'
```

## IDE Integration

### VS Code

Install the Boilerplates extension:

```bash
code --install-extension mlorentedev.boilerplates-snippets
```

Features:
- Snippet suggestions
- Template generation from command palette
- Inline documentation
- Syntax highlighting

### IntelliJ IDEA

1. Open Settings > Plugins
2. Search for "Boilerplates"
3. Install and restart

### Vim/Neovim

Add to your config:

```vim
" ~/.vimrc or ~/.config/nvim/init.vim
Plug 'mlorentedev/boilerplates.vim'

" Keybindings
nnoremap <leader>bs :BpSearch<CR>
nnoremap <leader>bn :BpNew<CR>
nnoremap <leader>bc :BpCopy<CR>
```

## Next Steps

- [Read CLI Usage Guide](cli-usage.md) for advanced commands
- [Learn Search Tips](search-tips.md) for efficient searching
- [Browse Templates](../terraform/index.md) to see what's available
- [Check Cheatsheets](../cheatsheets/index.md) for quick reference

## Troubleshooting

### bp command not found

```bash
# Check if bp is in PATH
which bp

# If not found, install again
make install-cli

# Or add to PATH manually
export PATH="$PATH:$HOME/.local/bin"
```

### Documentation not loading

```bash
# Check if mkdocs is installed
mkdocs --version

# Install if needed
pip install mkdocs-material

# Start server
make docs-serve
```

### Search not working

```bash
# Rebuild search index
make docs-build

# Clear cache
rm -rf site/

# Rebuild and serve
make docs-serve
```

## Getting Help

- Check the [CLI Usage Guide](cli-usage.md)
- Read [Search Tips](search-tips.md)
- Visit [GitHub Issues](https://github.com/mlorentedev/boilerplates/issues)
- Join our [Discord Community](https://discord.gg/boilerplates)

---

**Ready to start?** Try: `bp search "getting started"`
