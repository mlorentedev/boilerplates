#!/usr/bin/env bash
#
# Installation script for bp CLI tool
# Usage: curl -fsSL https://raw.githubusercontent.com/mlorentedev/boilerplates/main/scripts/install-bp.sh | bash
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/bin}"
REPO_URL="https://github.com/mlorentedev/boilerplates.git"
REPO_DIR="$HOME/.local/share/boilerplates"

echo "========================================="
echo "  bp CLI Tool Installer"
echo "========================================="
echo ""

# Check dependencies
echo "Checking dependencies..."

check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 found"
        return 0
    else
        echo -e "${RED}✗${NC} $1 not found"
        return 1
    fi
}

MISSING_DEPS=0

check_command "python3" || MISSING_DEPS=1
check_command "git" || MISSING_DEPS=1

# fzf is optional but recommended
if ! check_command "fzf"; then
    echo -e "${YELLOW}  fzf is recommended for interactive search${NC}"
    echo "  Install: https://github.com/junegunn/fzf#installation"
fi

if [ $MISSING_DEPS -eq 1 ]; then
    echo -e "\n${RED}Error: Missing required dependencies${NC}"
    echo "Please install missing dependencies and try again"
    exit 1
fi

echo ""
echo "Installing bp CLI..."

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$HOME/.config/bp"
mkdir -p "$HOME/.cache/bp"

# Clone or update repository
if [ -d "$REPO_DIR" ]; then
    echo "Updating repository..."
    cd "$REPO_DIR"
    git pull origin main
else
    echo "Cloning repository..."
    git clone "$REPO_URL" "$REPO_DIR"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
cd "$REPO_DIR"
pip3 install --user -q -r requirements.txt

# Make bp executable
chmod +x "$REPO_DIR/cli/bp"

# Create symlink
echo "Creating symlink..."
ln -sf "$REPO_DIR/cli/bp" "$INSTALL_DIR/bp"

# Check if INSTALL_DIR is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo -e "${YELLOW}Warning: $INSTALL_DIR is not in your PATH${NC}"
    echo "Add this to your shell configuration file (~/.bashrc, ~/.zshrc, etc.):"
    echo ""
    echo "  export PATH=\"\$PATH:$INSTALL_DIR\""
    echo ""
fi

# Generate shell completion
echo "Generating shell completions..."
SHELL_NAME=$(basename "$SHELL")

case "$SHELL_NAME" in
    bash)
        mkdir -p "$HOME/.bash_completion.d"
        "$INSTALL_DIR/bp" completion bash > "$HOME/.bash_completion.d/bp" 2>/dev/null || true
        echo "  Add to ~/.bashrc: source ~/.bash_completion.d/bp"
        ;;
    zsh)
        mkdir -p "$HOME/.zsh_completion.d"
        "$INSTALL_DIR/bp" completion zsh > "$HOME/.zsh_completion.d/_bp" 2>/dev/null || true
        echo "  Add to ~/.zshrc: fpath=(~/.zsh_completion.d \$fpath)"
        ;;
    fish)
        mkdir -p "$HOME/.config/fish/completions"
        "$INSTALL_DIR/bp" completion fish > "$HOME/.config/fish/completions/bp.fish" 2>/dev/null || true
        ;;
esac

# Build search index
echo "Building search index..."
cd "$REPO_DIR"
python3 -c "from cli.utils.search import build_search_index; build_search_index()" 2>/dev/null || echo "  (will be built on first use)"

# Create initial config
if [ ! -f "$HOME/.config/bp/config.yaml" ]; then
    echo "Creating default configuration..."
    cat > "$HOME/.config/bp/config.yaml" <<'EOF'
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
EOF
fi

# Create snippets
echo "Creating snippet database..."
cd "$REPO_DIR"
python3 -c "from cli.utils.snippets import create_snippet_database; create_snippet_database()" 2>/dev/null || true

echo ""
echo -e "${GREEN}========================================="
echo "  Installation Complete!"
echo "=========================================${NC}"
echo ""
echo "Verify installation:"
echo "  $ bp --version"
echo ""
echo "Get started:"
echo "  $ bp search \"getting started\""
echo "  $ bp web"
echo "  $ bp list"
echo ""
echo "Documentation: https://mlorentedev.github.io/boilerplates"
echo ""
