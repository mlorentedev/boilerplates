# Microservices Templates

Production-ready microservice templates for Java Spring Boot and Quarkus frameworks.

## Available Templates

### Spring Boot
Complete Spring Boot microservice with:
- RESTful API endpoints
- OpenAPI/Swagger documentation
- Database integration (JPA)
- Docker and Kubernetes deployment
- Health checks and metrics
- Security configuration
- Testing setup

[View Spring Boot Documentation](spring-boot.md)

### Quarkus
Supersonic Subatomic Java microservice with:
- JAX-RS endpoints
- Native compilation support
- OpenAPI documentation
- Database integration (Panache)
- Docker and Kubernetes deployment
- Health and metrics
- GraalVM native image

[View Quarkus Documentation](quarkus.md)

## Features

All templates include:
- Dockerfile for containerization
- Kubernetes manifests
- CI/CD pipeline examples
- Integration tests
- Monitoring setup
- Documentation

## Quick Start

```bash
# Generate new microservice
bp new spring-boot-api my-service

# Build and run
cd my-service
./mvnw spring-boot:run

# Build Docker image
docker build -t my-service:latest .

# Deploy to Kubernetes
kubectl apply -f k8s/
```

## Related Resources

- [Docker Documentation](../docker-compose/index.md)
- [Kubernetes Documentation](../kubernetes/index.md)
