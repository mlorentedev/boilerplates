# Installation Guide

Multiple ways to install the boilerplates system and `bp` CLI tool.

## Quick Install

### One-Line Install (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/mlorentedev/boilerplates/main/scripts/install-bp.sh | bash
```

Or using wget:

```bash
wget -qO- https://raw.githubusercontent.com/mlorentedev/boilerplates/main/scripts/install-bp.sh | bash
```

This will:
- Install the `bp` CLI tool
- Setup shell completion
- Install documentation locally
- Configure defaults

### Verify Installation

```bash
bp --version
bp help
```

## Platform-Specific Installation

### Linux

#### Ubuntu/Debian

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y python3-pip git fzf

# Install bp CLI
curl -fsSL https://raw.githubusercontent.com/mlorentedev/boilerplates/main/scripts/install-bp.sh | bash

# Install shell completion
bp completion bash | sudo tee /etc/bash_completion.d/bp
```

#### Fedora/RHEL/CentOS

```bash
# Install dependencies
sudo dnf install -y python3-pip git fzf

# Install bp CLI
curl -fsSL https://raw.githubusercontent.com/mlorentedev/boilerplates/main/scripts/install-bp.sh | bash

# Install shell completion
bp completion bash | sudo tee /etc/bash_completion.d/bp
```

#### Arch Linux

```bash
# Install dependencies
sudo pacman -S python-pip git fzf

# Install bp CLI
curl -fsSL https://raw.githubusercontent.com/mlorentedev/boilerplates/main/scripts/install-bp.sh | bash

# Install shell completion
bp completion bash | sudo tee /usr/share/bash-completion/completions/bp
```

### macOS

#### Using Homebrew (Recommended)

```bash
# Install dependencies
brew install python3 git fzf

# Install bp CLI
brew tap mlorentedev/tap
brew install bp

# Shell completion is automatically configured
```

#### Manual Installation

```bash
# Install dependencies
brew install python3 git fzf

# Install bp CLI
curl -fsSL https://raw.githubusercontent.com/mlorentedev/boilerplates/main/scripts/install-bp.sh | bash

# Install shell completion (Bash)
bp completion bash > /usr/local/etc/bash_completion.d/bp

# Or for Zsh
bp completion zsh > /usr/local/share/zsh/site-functions/_bp
```

### Windows

#### Using PowerShell

```powershell
# Install using PowerShell script
Invoke-WebRequest -Uri https://raw.githubusercontent.com/mlorentedev/boilerplates/main/scripts/install-bp.ps1 -OutFile install-bp.ps1
.\install-bp.ps1

# Add to PATH
$env:Path += ";$env:LOCALAPPDATA\bp\bin"

# Make permanent
[Environment]::SetEnvironmentVariable("Path", $env:Path, [System.EnvironmentVariableTarget]::User)
```

#### Using WSL (Recommended)

```bash
# Install in WSL Ubuntu
curl -fsSL https://raw.githubusercontent.com/mlorentedev/boilerplates/main/scripts/install-bp.sh | bash

# Use from Windows
wsl bp search "kubernetes"
```

## Manual Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/mlorentedev/boilerplates.git
cd boilerplates

# Install dependencies
pip install -r requirements.txt

# Install bp CLI
make install-cli

# Or manually
sudo cp cli/bp /usr/local/bin/bp
sudo chmod +x /usr/local/bin/bp

# Install shell completion
bp completion bash > ~/.bash_completion.d/bp
source ~/.bash_completion.d/bp
```

### From Release

```bash
# Download latest release
VERSION=$(curl -s https://api.github.com/repos/mlorentedev/boilerplates/releases/latest | grep "tag_name" | cut -d '"' -f 4)
curl -LO "https://github.com/mlorentedev/boilerplates/releases/download/${VERSION}/bp-linux-amd64"

# Install
sudo mv bp-linux-amd64 /usr/local/bin/bp
sudo chmod +x /usr/local/bin/bp

# Verify
bp --version
```

### Using Docker

```bash
# Pull the Docker image
docker pull ghcr.io/mlorentedev/boilerplates:latest

# Create alias for easy use
echo 'alias bp="docker run --rm -it -v \$(pwd):/workspace ghcr.io/mlorentedev/boilerplates:latest bp"' >> ~/.bashrc
source ~/.bashrc

# Use bp command
bp search "kubernetes"
```

### Using Nix

```bash
# Install using Nix
nix-env -iA nixpkgs.bp

# Or using flakes
nix profile install github:mlorentedev/boilerplates#bp
```

## Post-Installation Setup

### Shell Completion

#### Bash

```bash
# Add to ~/.bashrc
bp completion bash > ~/.bash_completion.d/bp
echo 'source ~/.bash_completion.d/bp' >> ~/.bashrc
source ~/.bashrc
```

#### Zsh

```bash
# Add to ~/.zshrc
bp completion zsh > ~/.zsh_completion.d/_bp
echo 'fpath=(~/.zsh_completion.d $fpath)' >> ~/.zshrc
echo 'autoload -Uz compinit && compinit' >> ~/.zshrc
source ~/.zshrc
```

#### Fish

```bash
# Add to Fish configuration
bp completion fish > ~/.config/fish/completions/bp.fish
```

#### PowerShell

```powershell
# Add to PowerShell profile
bp completion powershell >> $PROFILE
. $PROFILE
```

### Environment Variables

Add to your shell configuration file (~/.bashrc, ~/.zshrc, etc.):

```bash
# bp CLI configuration
export BP_CONFIG="$HOME/.config/bp/config.yaml"
export BP_CACHE_DIR="$HOME/.cache/bp"
export BP_EDITOR="vim"  # or code, nano, etc.
export BP_OUTPUT_DIR="$HOME/projects"

# Optional: Disable color output
# export BP_NO_COLOR=1
```

### Configuration File

Create the configuration file:

```bash
mkdir -p ~/.config/bp
cat > ~/.config/bp/config.yaml <<'EOF'
# bp CLI Configuration

editor: vim
output_dir: ./
color: true

search:
  limit: 20
  category: all
  fuzzy: true

cache:
  enabled: true
  ttl: 3600

web:
  port: 8000
  auto_open: true

recent_limit: 10

favorites:
  - spring-boot-api
  - terraform-aws-vpc
  - kubernetes-deployment
EOF
```

### Aliases (Optional but Recommended)

Add convenient aliases to your shell:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias bps='bp search'
alias bpf='bp find'
alias bpn='bp new'
alias bpc='bp copy'
alias bpl='bp list'
alias bpw='bp web'
alias bpr='bp recent'
```

## Dependencies

### Required

- **Python 3.8+**: Core runtime
- **Git**: For cloning templates
- **fzf**: For fuzzy search functionality

### Optional

- **Docker**: For running containerized tools
- **MkDocs Material**: For local documentation
  ```bash
  pip install mkdocs-material
  ```
- **kubectl**: For Kubernetes validation
- **terraform**: For Terraform validation
- **ansible**: For Ansible validation

### Install All Dependencies

#### Linux (Ubuntu/Debian)

```bash
# Core dependencies
sudo apt-get install -y python3-pip git fzf

# Optional dependencies
sudo apt-get install -y docker.io
pip install mkdocs-material ansible-lint

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install terraform
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt-get update && sudo apt-get install terraform
```

#### macOS

```bash
# Core dependencies
brew install python3 git fzf

# Optional dependencies
brew install docker kubectl terraform ansible
pip3 install mkdocs-material ansible-lint
```

## IDE Integration

### VS Code

```bash
# Install VS Code extension
code --install-extension mlorentedev.boilerplates-snippets

# Or search for "Boilerplates" in VS Code Extensions
```

### IntelliJ IDEA

1. Open Settings > Plugins
2. Search for "Boilerplates"
3. Install and restart

### Vim/Neovim

Add to your Vim configuration:

```vim
" For vim-plug
Plug 'mlorentedev/boilerplates.vim'

" For packer.nvim
use 'mlorentedev/boilerplates.nvim'
```

## Updating

### Update bp CLI

```bash
# Update to latest version
bp update

# Or using the installation script
curl -fsSL https://raw.githubusercontent.com/mlorentedev/boilerplates/main/scripts/install-bp.sh | bash

# Check for updates
bp update --check
```

### Update Templates

```bash
# Update templates only
bp update --templates

# Or manually
cd ~/boilerplates
git pull origin main
```

### Update Documentation

```bash
# Rebuild documentation
cd ~/boilerplates
make docs-build

# Or using bp
bp cache rebuild
```

## Uninstallation

### Remove bp CLI

```bash
# Remove binary
sudo rm /usr/local/bin/bp

# Remove configuration
rm -rf ~/.config/bp
rm -rf ~/.cache/bp

# Remove shell completion
rm ~/.bash_completion.d/bp  # Bash
rm ~/.zsh_completion.d/_bp  # Zsh
rm ~/.config/fish/completions/bp.fish  # Fish
```

### Complete Cleanup

```bash
# Run uninstall script
curl -fsSL https://raw.githubusercontent.com/mlorentedev/boilerplates/main/scripts/uninstall-bp.sh | bash

# Or manually
sudo rm /usr/local/bin/bp
rm -rf ~/.config/bp
rm -rf ~/.cache/bp
rm -rf ~/boilerplates  # If you cloned the repo
```

## Troubleshooting

### bp command not found

```bash
# Check if bp is installed
which bp

# Check PATH
echo $PATH

# Add to PATH if needed
export PATH="$PATH:$HOME/.local/bin"
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
```

### Permission denied

```bash
# Make bp executable
sudo chmod +x /usr/local/bin/bp

# Or install in user directory
mkdir -p ~/.local/bin
cp cli/bp ~/.local/bin/
export PATH="$PATH:$HOME/.local/bin"
```

### Python version issues

```bash
# Check Python version
python3 --version

# Install Python 3.8+ if needed
sudo apt-get install python3.8  # Ubuntu/Debian
brew install python@3.8          # macOS
```

### fzf not found

```bash
# Install fzf
sudo apt-get install fzf         # Ubuntu/Debian
brew install fzf                 # macOS
sudo dnf install fzf             # Fedora/RHEL

# Or install from source
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

### Documentation not loading

```bash
# Install MkDocs Material
pip install mkdocs-material

# Build documentation
cd ~/boilerplates
make docs-build

# Serve documentation
make docs-serve
```

## System Requirements

### Minimum Requirements

- **OS**: Linux, macOS, Windows (WSL)
- **RAM**: 512 MB
- **Disk**: 100 MB free space
- **Python**: 3.8 or higher

### Recommended Requirements

- **OS**: Linux, macOS, Windows (WSL2)
- **RAM**: 1 GB or more
- **Disk**: 500 MB free space
- **Python**: 3.10 or higher
- **Terminal**: Support for colors and UTF-8

## Getting Help

- **Documentation**: Run `bp web` to open documentation
- **GitHub Issues**: https://github.com/mlorentedev/boilerplates/issues
- **Discord**: https://discord.gg/boilerplates
- **Email**: support@mlorente.dev

## Next Steps

- [Quick Start Guide](quickstart.md) - Get started in 5 minutes
- [CLI Usage Guide](cli-usage.md) - Learn all commands
- [Search Tips](search-tips.md) - Master the search functionality

---

**Installation complete!** Try: `bp search "getting started"`
