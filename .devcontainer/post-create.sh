#!/bin/bash
set -e

echo "Setting up development environment..."

# Update package lists
sudo apt-get update

# Install additional tools
sudo apt-get install -y \
    vim \
    jq \
    yq \
    tree \
    htop \
    curl \
    wget \
    unzip \
    git \
    make \
    build-essential

# Install Ansible
pip3 install --user ansible ansible-lint

# Install pre-commit
pip3 install --user pre-commit

# Install Checkov for security scanning
pip3 install --user checkov

# Install tflint for Terraform linting
curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash

# Install kubectl (if not already installed)
if ! command -v kubectl &> /dev/null; then
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    rm kubectl
fi

# Install Docker Compose (if not already installed)
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Set up git hooks
if [ -f .pre-commit-config.yaml ]; then
    pre-commit install --install-hooks
    pre-commit install --hook-type commit-msg
fi

# Create useful aliases
cat >> ~/.bashrc << 'EOF'

# Useful aliases for infrastructure work
alias tf='terraform'
alias k='kubectl'
alias dc='docker-compose'
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Kubernetes aliases
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kgd='kubectl get deployments'
alias kdp='kubectl describe pod'
alias kds='kubectl describe service'
alias kdd='kubectl describe deployment'

# Docker aliases
alias dps='docker ps'
alias dpa='docker ps -a'
alias di='docker images'
alias drmi='docker rmi'
alias drmf='docker rm -f'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline'
alias gd='git diff'
EOF

echo "Development environment setup complete!"
echo "Available tools:"
echo "  - Terraform $(terraform version --json | jq -r .terraform_version)"
echo "  - Ansible $(ansible --version | head -1)"
echo "  - Docker $(docker --version)"
echo "  - kubectl $(kubectl version --client --short 2>/dev/null || echo 'Not configured')"
echo "  - Pre-commit $(pre-commit --version)"