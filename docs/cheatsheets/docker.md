# Docker Cheatsheet

Quick reference for Docker commands and operations.

## Container Management

```bash
# List containers
docker ps                    # Running containers
docker ps -a                # All containers

# Start/stop containers
docker start <container>
docker stop <container>
docker restart <container>

# Remove containers
docker rm <container>
docker rm -f <container>    # Force remove
docker container prune      # Remove all stopped

# Execute commands
docker exec -it <container> /bin/bash
docker exec <container> <command>

# View logs
docker logs <container>
docker logs -f <container>     # Follow logs
docker logs --tail 100 <container>
```

## Image Management

```bash
# List images
docker images
docker image ls

# Pull/push images
docker pull <image>:<tag>
docker push <image>:<tag>

# Build images
docker build -t <name>:<tag> .
docker build -f Dockerfile.prod -t <name>:<tag> .

# Remove images
docker rmi <image>
docker image prune          # Remove dangling images
docker image prune -a      # Remove all unused images
```

## Docker Compose

```bash
# Start services
docker-compose up
docker-compose up -d        # Detached mode
docker-compose up --build   # Rebuild images

# Stop services
docker-compose stop
docker-compose down
docker-compose down -v      # Remove volumes

# View logs
docker-compose logs
docker-compose logs -f <service>

# Execute commands
docker-compose exec <service> /bin/bash

# Scale services
docker-compose up -d --scale <service>=3
```

## Network Management

```bash
# List networks
docker network ls

# Create network
docker network create <name>

# Connect container
docker network connect <network> <container>

# Inspect network
docker network inspect <network>
```

## Volume Management

```bash
# List volumes
docker volume ls

# Create volume
docker volume create <name>

# Remove volumes
docker volume rm <name>
docker volume prune         # Remove unused volumes

# Inspect volume
docker volume inspect <name>
```

## System Management

```bash
# System info
docker info
docker version

# Disk usage
docker system df

# Clean up
docker system prune         # Remove unused data
docker system prune -a     # Remove all unused data
docker system prune --volumes  # Include volumes

# Resource usage
docker stats
docker stats <container>
```

## Dockerfile Best Practices

```dockerfile
# Multi-stage build
FROM node:16 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:16-alpine
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY package*.json ./
RUN npm install --production
CMD ["node", "dist/index.js"]
```

## Common Patterns

### Environment Variables
```bash
docker run -e VAR=value <image>
docker run --env-file .env <image>
```

### Port Mapping
```bash
docker run -p 8080:80 <image>
docker run -p 127.0.0.1:8080:80 <image>
```

### Volume Mounting
```bash
docker run -v /host/path:/container/path <image>
docker run -v volume_name:/container/path <image>
```

### Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost/ || exit 1
```

## Troubleshooting

```bash
# Inspect container
docker inspect <container>

# Check container processes
docker top <container>

# View container changes
docker diff <container>

# Export/import
docker export <container> > container.tar
docker import container.tar <image>

# Save/load images
docker save <image> > image.tar
docker load < image.tar
```
