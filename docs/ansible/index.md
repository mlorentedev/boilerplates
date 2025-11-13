# Ansible Playbooks

Automation playbooks for server provisioning, configuration management, and deployment tasks.

## Categories

### Ubuntu
- System setup and hardening
- SSH key management
- Package installation
- User management

[View Ubuntu Documentation](ubuntu.md)

### Docker
- Docker installation
- Docker Compose setup
- Registry configuration
- Certificate management

[View Docker Documentation](docker.md)

### Kubernetes
- Cluster setup
- Node configuration
- Application deployment

[View Kubernetes Documentation](kubernetes.md)

### Monitoring
- Prometheus setup
- Node exporter installation
- Alertmanager configuration

[View Monitoring Documentation](monitoring.md)

### Security
- Firewall configuration
- Fail2ban setup
- Security auditing

[View Security Documentation](security.md)

### Storage
- NFS server setup
- Mount configurations
- Backup automation

[View Storage Documentation](storage.md)

### Database
- PostgreSQL installation
- Backup automation
- Replication setup

[View Database Documentation](database.md)

## Quick Start

```bash
# Create inventory
cat > inventory.ini <<EOF
[servers]
server1 ansible_host=192.168.1.10
server2 ansible_host=192.168.1.11
EOF

# Run playbook
ansible-playbook -i inventory.ini playbook.yml

# Check syntax
ansible-playbook --syntax-check playbook.yml

# Dry run
ansible-playbook --check -i inventory.ini playbook.yml
```

## Related Resources

- [Ansible Cheatsheet](cheatsheet.md)
- [Ansible Snippets](../snippets/ansible.md)
