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

# Documentation targets
docs: ## Generate documentation
	@echo "Generating documentation..."
	@for dir in terraform/*/; do \
		if [ -f "$$dir/provider.tf" ] || [ -f "$$dir/main.tf" ]; then \
			echo "Generating docs for $$dir"; \
			(cd "$$dir" && terraform-docs markdown table . > README.md); \
		fi; \
	done

# Release targets
release: ## Create a new release
	@echo "Creating release..."
	@echo "Current version: $$(git describe --tags --abbrev=0 2>/dev/null || echo 'No tags found')"
	@echo "Please create a new tag manually: git tag -a v1.0.0 -m 'Release v1.0.0'"