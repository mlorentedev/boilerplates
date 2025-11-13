# Contributing to DevOps Boilerplates

Thank you for your interest in contributing to this project. This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- fzf (optional, for interactive search)
- Docker (for testing Docker Compose templates)
- Terraform (for testing Terraform templates)
- kubectl (for testing Kubernetes templates)
- Ansible (for testing Ansible playbooks)

### Development Setup

```bash
# Clone the repository
git clone https://github.com/mlorentedev/boilerplates.git
cd boilerplates

# Install dependencies
pip install -r requirements.txt

# Setup development environment
make dev-setup

# Run tests
make test-all
```

## How to Contribute

### Reporting Issues

When reporting issues, please include:

- Clear description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots if applicable

### Suggesting Enhancements

For feature requests or enhancements:

- Check if the feature already exists
- Describe the use case
- Explain why it would be useful
- Provide examples if possible

### Pull Requests

1. Fork the repository
2. Create a feature branch from main
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a pull request

#### PR Requirements

- Follow the existing code style
- Add tests for new features
- Update documentation
- Ensure all tests pass
- Keep commits focused and atomic
- Use conventional commit messages

#### Commit Message Format

```
type: subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

Examples:
```
feat: add Terraform module for AWS EKS
fix: resolve search performance issue
docs: update Kubernetes installation guide
```

## Development Guidelines

### Code Style

**Python:**
- Follow PEP 8 guidelines
- Maximum line length: 120 characters
- Use meaningful variable names
- Add docstrings to functions and classes
- Format code with Black: `black cli/`

**Markdown:**
- Use ATX-style headers (`#` instead of underlines)
- Keep lines under 120 characters where possible
- Use code blocks with language identifiers
- Include examples for commands

**YAML:**
- Use 2 spaces for indentation
- Quote strings when necessary
- Validate with yamllint

### Testing

All contributions must include appropriate tests:

```bash
# Run all tests
make test-all

# Run specific tests
make test-cli
make search-test
make docs-validate

# Run benchmarks
make benchmark
```

### Documentation

For any new features or templates:

1. Add documentation in the `docs/` directory
2. Update relevant index pages
3. Add examples and usage instructions
4. Include troubleshooting tips
5. Update README.md if needed

### Adding Templates

When adding new templates:

1. Create template files in appropriate directory
2. Add comprehensive documentation
3. Include usage examples
4. Add to search index
5. Create snippet if applicable
6. Test thoroughly

Example structure:
```
terraform/new-module/
├── main.tf
├── variables.tf
├── outputs.tf
├── README.md
└── examples/
    └── basic/
```

Documentation:
```
docs/terraform/new-module.md
```

### Search Index

After adding new documentation:

```bash
# Rebuild search index
make search-index

# Test search
./cli/bp search "new feature"
```

### Performance Requirements

- Search queries must complete in under 100ms
- Index build should complete in under 1 second
- Documentation pages should load quickly
- CLI commands should respond instantly

## Testing Guidelines

### Unit Tests

Write unit tests for:
- CLI commands
- Utility functions
- Search functionality
- Template generation

### Integration Tests

Test complete workflows:
- Documentation generation
- Template usage
- Search functionality
- CLI workflows

### Performance Tests

Verify performance requirements:
- Search speed
- Index build time
- Documentation build time

## Code Review Process

All pull requests will be reviewed for:

1. **Functionality**: Does it work as intended?
2. **Tests**: Are there adequate tests?
3. **Documentation**: Is it well documented?
4. **Code Quality**: Is the code clean and maintainable?
5. **Performance**: Does it meet performance requirements?
6. **Security**: Are there any security concerns?

## CI/CD Pipeline

All PRs must pass:

- CLI tests
- Documentation tests
- Template validation
- Code quality checks
- Security scans
- Performance tests

The CI/CD pipeline runs automatically on every PR.

## Release Process

Releases are created by maintainers:

1. Update version numbers
2. Update CHANGELOG
3. Create git tag
4. Push tag to trigger release workflow
5. Verify release artifacts

## Getting Help

If you need help:

- Check existing documentation
- Search closed issues
- Ask in discussions
- Contact maintainers

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue for any questions about contributing.

Thank you for contributing!
