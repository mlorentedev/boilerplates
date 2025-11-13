# Boilerplates Makefile

.PHONY: help setup test lint security clean docker-build terraform-plan ansible-check

# Default target
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

setup: ## Set up development environment
	@echo "Setting up development environment..."
	pip install --user pre-commit ansible-lint checkov
	pre-commit install --install-hooks
	pre-commit install --hook-type commit-msg

test: ## Run all tests
	@echo "Running tests..."
	@make terraform-validate
	@make ansible-check
	@make docker-compose-validate

lint: ## Run linting tools
	@echo "Running pre-commit hooks..."
	pre-commit run --all-files

security: ## Run security scans
	@echo "Running security scans..."
	checkov -d . --framework terraform,kubernetes,dockerfile,ansible
	# Add more security tools as needed

clean: ## Clean up temporary files
	@echo "Cleaning up..."
	find . -name "*.tfstate" -delete
	find . -name "*.tfstate.backup" -delete
	find . -name ".terraform" -type d -exec rm -rf {} + 2>/dev/null || true
	docker system prune -f

# Docker Compose targets
docker-compose-validate: ## Validate all Docker Compose files
	@echo "Validating Docker Compose files..."
	@for dir in docker-compose/*/; do \
		if [ -f "$$dir/compose.yaml" ]; then \
			echo "Validating $$dir/compose.yaml"; \
			docker-compose -f "$$dir/compose.yaml" config > /dev/null; \
		fi; \
	done

docker-build: ## Build all Docker Compose services
	@echo "Building Docker Compose services..."
	@for dir in docker-compose/*/; do \
		if [ -f "$$dir/compose.yaml" ]; then \
			echo "Building services in $$dir"; \
			docker-compose -f "$$dir/compose.yaml" build; \
		fi; \
	done

# Terraform targets
terraform-init: ## Initialize all Terraform configurations
	@echo "Initializing Terraform configurations..."
	@for dir in terraform/*/; do \
		if [ -f "$$dir/provider.tf" ] || [ -f "$$dir/main.tf" ]; then \
			echo "Initializing $$dir"; \
			(cd "$$dir" && terraform init); \
		fi; \
	done

terraform-validate: ## Validate all Terraform configurations
	@echo "Validating Terraform configurations..."
	@for dir in terraform/*/; do \
		if [ -f "$$dir/provider.tf" ] || [ -f "$$dir/main.tf" ]; then \
			echo "Validating $$dir"; \
			(cd "$$dir" && terraform fmt -check && terraform validate); \
		fi; \
	done

terraform-plan: terraform-init ## Plan all Terraform configurations
	@echo "Planning Terraform configurations..."
	@for dir in terraform/*/; do \
		if [ -f "$$dir/provider.tf" ] || [ -f "$$dir/main.tf" ]; then \
			echo "Planning $$dir"; \
			(cd "$$dir" && terraform plan); \
		fi; \
	done

terraform-fmt: ## Format all Terraform files
	@echo "Formatting Terraform files..."
	terraform fmt -recursive .

# Ansible targets
ansible-check: ## Check Ansible playbook syntax
	@echo "Checking Ansible playbooks..."
	@find ansible/ -name "*.yaml" -o -name "*.yml" | while read file; do \
		echo "Checking $$file"; \
		ansible-playbook --syntax-check "$$file" || exit 1; \
	done

ansible-lint: ## Lint Ansible playbooks
	@echo "Linting Ansible playbooks..."
	@find ansible/ -name "*.yaml" -o -name "*.yml" | xargs ansible-lint

# Kubernetes targets
k8s-validate: ## Validate Kubernetes manifests
	@echo "Validating Kubernetes manifests..."
	@find kubernetes/ -name "*.yaml" -o -name "*.yml" | while read file; do \
		echo "Validating $$file"; \
		kubectl --dry-run=client apply -f "$$file" || exit 1; \
	done

# bp CLI targets
install-cli: ## Install bp CLI tool
	@echo "Installing bp CLI..."
	@bash scripts/install-bp.sh

bp-test: ## Test bp CLI functionality
	@echo "Testing bp CLI..."
	@./cli/bp --version
	@./cli/bp list | head -5
	@echo "CLI is working"

# Documentation targets
docs: ## Generate documentation
	@echo "Generating documentation..."
	@for dir in terraform/*/; do \
		if [ -f "$$dir/provider.tf" ] || [ -f "$$dir/main.tf" ]; then \
			echo "Generating docs for $$dir"; \
			(cd "$$dir" && terraform-docs markdown table . > README.md); \
		fi; \
	done

docs-build: ## Build MkDocs documentation
	@echo "Building documentation..."
	mkdocs build

docs-serve: ## Serve documentation locally
	@echo "Starting documentation server..."
	@echo "Documentation will be available at http://localhost:8000"
	mkdocs serve

docs-deploy: ## Deploy documentation to GitHub Pages
	@echo "Deploying documentation..."
	mkdocs gh-deploy --force

docs-validate: ## Validate documentation links
	@echo "Validating documentation..."
	@find docs/ -name "*.md" -type f | while read file; do \
		echo "Checking $$file"; \
		grep -oP '\[.*?\]\(\K[^)]+' "$$file" | while read link; do \
			if [[ $$link == http* ]]; then \
				curl -s -o /dev/null -w "%{http_code} $$link\n" "$$link" | grep -v "^200" && echo "Broken: $$link in $$file" || true; \
			fi; \
		done; \
	done

# Search index targets
search-index: ## Build search index
	@echo "Building search index..."
	@python3 -c "from cli.utils.search import build_search_index; build_search_index()"

search-test: ## Test search performance
	@echo "Testing search performance..."
	@python3 cli/utils/search.py

# Snippet targets
snippets-create: ## Create initial snippet database
	@echo "Creating snippet database..."
	@python3 -c "from cli.utils.snippets import create_snippet_database; create_snippet_database()"

snippets-list: ## List all snippets
	@echo "Available snippets:"
	@python3 -c "from cli.utils.snippets import list_snippets; import json; print(json.dumps(list_snippets(), indent=2))"

# Testing targets
test-all: test docs-validate search-test ## Run all tests including documentation and search

test-cli: ## Test CLI commands
	@echo "Testing CLI commands..."
	@./cli/bp --version
	@./cli/bp list terraform
	@./cli/bp cache stats
	@echo "All CLI tests passed"

# Performance targets
benchmark: ## Run performance benchmarks
	@echo "Running performance benchmarks..."
	@echo "Search performance:"
	@python3 cli/utils/search.py
	@echo ""
	@echo "Cache statistics:"
	@./cli/bp cache stats

# Development targets
dev-setup: setup ## Complete development setup
	@echo "Installing Python dependencies..."
	pip3 install --user -r requirements.txt
	@echo "Installing CLI..."
	@make install-cli
	@echo "Building search index..."
	@make search-index
	@echo "Creating snippets..."
	@make snippets-create
	@echo "Development environment ready"

# Clean targets
clean-all: clean ## Clean everything including cache and docs
	@echo "Cleaning all generated files..."
	rm -rf site/
	rm -rf .cache/
	rm -rf ~/.cache/bp/
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete

# Release targets
release: ## Create a new release
	@echo "Creating release..."
	@echo "Current version: $$(git describe --tags --abbrev=0 2>/dev/null || echo 'No tags found')"
	@echo "Please create a new tag manually: git tag -a v1.0.0 -m 'Release v1.0.0'"

# Validate everything
validate: lint test-all docs-validate ## Validate everything
	@echo "All validation passed"