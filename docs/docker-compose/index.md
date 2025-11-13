# Docker Compose Templates

Ready-to-use Docker Compose configurations for databases, monitoring, CI/CD, and development environments.

## Categories

### Databases
- **PostgreSQL**: Production-ready PostgreSQL with persistent storage
- **MariaDB**: MariaDB database with automatic backups
- **MongoDB**: MongoDB replica set configuration
- **Redis**: Redis with persistence and clustering options

[View Database Documentation](databases.md)

### Monitoring
- **Prometheus**: Complete monitoring stack with exporters
- **Grafana**: Visualization and dashboards
- **Loki**: Log aggregation system
- **Alertmanager**: Alert management and routing

[View Monitoring Documentation](monitoring.md)

### CI/CD
- **Jenkins**: Automated CI/CD server
- **GitLab**: Complete DevOps platform
- **SonarQube**: Code quality and security scanner

[View CI/CD Documentation](cicd.md)

### Networking
- **Traefik**: Reverse proxy and load balancer
- **Nginx Proxy Manager**: Web-based proxy management
- **Nginx**: High-performance web server

[View Networking Documentation](networking.md)

## Quick Start

```bash
# Navigate to template directory
cd docker-compose/postgres

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes
docker-compose down -v
```

## Common Patterns

### Environment Variables

```yaml
version: '3.8'
services:
  app:
    image: myapp:latest
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - API_KEY=${API_KEY}
    env_file:
      - .env
```

### Volumes

```yaml
volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
```

### Networks

```yaml
networks:
  frontend:
  backend:
```

## Related Resources

- [Docker Cheatsheet](../cheatsheets/docker.md)
- [Docker Snippets](../snippets/docker.md)
