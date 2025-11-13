# Terraform Templates

Infrastructure as Code templates for multiple cloud providers and platforms. These templates follow best practices and are production-ready.

## Available Providers

### AWS
Complete infrastructure setups for Amazon Web Services including VPC, EKS, RDS, and more.

[View AWS Documentation](aws.md)

**Key Templates:**
- VPC with public/private subnets
- EKS cluster with node groups
- RDS databases (PostgreSQL, MySQL)
- S3 buckets with policies
- IAM roles and policies
- Route53 DNS management
- CloudFront distributions
- Lambda functions

### Azure
Microsoft Azure infrastructure including AKS, Virtual Networks, and managed databases.

[View Azure Documentation](azure.md)

**Key Templates:**
- Resource groups
- Virtual Networks
- AKS clusters
- Azure SQL databases
- Storage accounts
- Azure Functions
- Application Gateway

### DigitalOcean
Simple and cost-effective cloud infrastructure on DigitalOcean.

[View DigitalOcean Documentation](digitalocean.md)

**Key Templates:**
- Droplets
- Kubernetes clusters
- Managed databases
- Load balancers
- Spaces (object storage)
- Firewalls

### Proxmox
On-premises virtualization platform templates.

[View Proxmox Documentation](proxmox.md)

**Key Templates:**
- VM creation
- LXC containers
- Storage configuration
- Network setup

### Kubernetes
Kubernetes resource management using Terraform.

[View Kubernetes Documentation](kubernetes.md)

**Key Templates:**
- Namespaces
- Deployments
- Services
- Ingress resources
- ConfigMaps and Secrets
- PersistentVolumeClaims

### Helm
Helm chart deployments via Terraform.

[View Helm Documentation](helm.md)

**Key Templates:**
- Chart releases
- Value overrides
- Multi-environment setups

## Quick Start

### Prerequisites

```bash
# Install Terraform
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install terraform

# macOS
brew install terraform

# Verify installation
terraform --version
```

### Basic Usage

```bash
# Navigate to template directory
cd terraform/aws

# Initialize Terraform
terraform init

# Review planned changes
terraform plan

# Apply changes
terraform apply

# Destroy resources
terraform destroy
```

### Configuration

Create a `terraform.tfvars` file with your variables:

```hcl
# terraform.tfvars
region = "us-east-1"
environment = "production"
project_name = "my-project"
```

## Best Practices

### State Management

Always use remote state for production:

```hcl
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Variable Management

Use variable files for different environments:

```bash
# Development
terraform apply -var-file="dev.tfvars"

# Production
terraform apply -var-file="prod.tfvars"
```

### Module Organization

```
terraform/
├── modules/
│   ├── vpc/
│   ├── eks/
│   └── rds/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
└── main.tf
```

## Common Commands

```bash
# Format code
terraform fmt -recursive

# Validate configuration
terraform validate

# Show current state
terraform show

# List resources
terraform state list

# Import existing resource
terraform import aws_instance.example i-1234567890abcdef0

# Refresh state
terraform refresh

# Output values
terraform output

# Generate dependency graph
terraform graph | dot -Tpng > graph.png
```

## Troubleshooting

### State Lock Issues

```bash
# Force unlock (use with caution)
terraform force-unlock LOCK_ID
```

### Provider Issues

```bash
# Clear provider cache
rm -rf .terraform/
terraform init -upgrade
```

### Debugging

```bash
# Enable debug logging
export TF_LOG=DEBUG
terraform apply

# Save logs to file
export TF_LOG_PATH=./terraform.log
```

## Security Considerations

- Never commit sensitive data to version control
- Use encrypted remote state
- Implement least privilege IAM policies
- Enable MFA for destructive operations
- Use Terraform Cloud for team collaboration
- Regular security audits with tools like checkov

```bash
# Security scan
checkov -d .

# Terraform plan with security checks
tfsec .
```

## Testing

```bash
# Install terraform-compliance
pip install terraform-compliance

# Run compliance tests
terraform-compliance -f compliance/ -p plan.out
```

## Documentation Generation

```bash
# Install terraform-docs
brew install terraform-docs

# Generate documentation
terraform-docs markdown table . > README.md
```

## Related Resources

- [Terraform Cheatsheet](cheatsheet.md)
- [AWS Templates](aws.md)
- [Azure Templates](azure.md)
- [Best Practices Guide](#)

## Support

For issues or questions:

- Check existing templates in the repository
- Review Terraform official documentation
- Open an issue on GitHub
