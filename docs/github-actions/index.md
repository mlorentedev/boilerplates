# GitHub Actions Workflows

CI/CD workflows for automated testing, deployment, and integration with various platforms.

## Available Workflows

### Deployment
- **SSH/SCP**: Secure file transfer and remote execution
- **Kubectl**: Kubernetes deployments
- **Azure DevOps**: Azure pipeline integration
- **GitLab CI**: GitLab pipeline integration

[View Documentation](ssh-scp.md)

## Quick Start

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: make test
```

## Related Resources

- [GitHub Actions Cheatsheet](cheatsheet.md)
