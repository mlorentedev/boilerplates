# Kubernetes Templates

Production-ready Kubernetes manifests for common applications and platform services. All templates follow Kubernetes best practices and are tested for reliability.

## Available Templates

### Platform Services

#### ArgoCD
GitOps continuous delivery tool for Kubernetes.

[View ArgoCD Documentation](argocd.md)

- Complete ArgoCD installation
- Application definitions
- Repository configurations
- RBAC policies
- Ingress setup

#### Cert Manager
Automatic SSL/TLS certificate management.

[View Cert Manager Documentation](cert-manager.md)

- ClusterIssuers for Let's Encrypt
- Certificate resources
- DNS01 and HTTP01 challenges
- Wildcard certificates

#### Nginx Ingress
Production ingress controller for routing traffic.

[View Nginx Ingress Documentation](nginx-ingress.md)

- Controller deployment
- Ingress class configuration
- TLS termination
- Rate limiting
- Authentication

#### Traefik
Modern reverse proxy and load balancer.

[View Traefik Documentation](traefik.md)

- IngressRoute definitions
- Middleware configuration
- TLS setup
- Dashboard access

### Monitoring and Observability

#### Prometheus Operator
Complete monitoring stack with Prometheus, Grafana, and Alertmanager.

[View Prometheus Documentation](prometheus-operator.md)

- Prometheus server
- Grafana dashboards
- Alertmanager rules
- ServiceMonitors
- Recording rules

### Storage

#### Longhorn
Distributed block storage for Kubernetes.

[View Longhorn Documentation](longhorn.md)

- StorageClass definitions
- Volume snapshots
- Backup configurations
- Recovery procedures

### Security

#### Sealed Secrets
Encrypt secrets for safe git storage.

[View Sealed Secrets Documentation](sealed-secrets.md)

- Controller installation
- Secret sealing
- Namespace scoping
- Key rotation

#### External Secrets
Sync secrets from external providers.

[View External Secrets Documentation](external-secrets.md)

- SecretStore configuration
- ExternalSecret resources
- AWS Secrets Manager integration
- Azure Key Vault integration

### Authentication

#### Authentik
Identity provider and SSO platform.

[View Authentik Documentation](authentik.md)

- Authentik deployment
- LDAP provider
- OAuth2/OIDC configuration
- Application proxies

### Backup

#### Velero
Backup and restore Kubernetes resources.

[View Velero Documentation](velero.md)

- Backup schedules
- Restore procedures
- Volume snapshots
- Migration between clusters

## Quick Start

### Prerequisites

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify connection
kubectl cluster-info
kubectl get nodes
```

### Applying Templates

```bash
# Apply a single resource
kubectl apply -f deployment.yaml

# Apply all resources in a directory
kubectl apply -f kubernetes/nginx-ingress/

# Apply with kustomize
kubectl apply -k overlays/production/
```

### Namespace Management

```bash
# Create namespace
kubectl create namespace production

# Apply to specific namespace
kubectl apply -f deployment.yaml -n production

# Set default namespace
kubectl config set-context --current --namespace=production
```

## Template Structure

Each template directory contains:

```
template-name/
├── namespace.yaml          # Namespace definition
├── deployment.yaml         # Application deployment
├── service.yaml           # Service definition
├── ingress.yaml           # Ingress rules
├── configmap.yaml         # Configuration
├── secret.yaml.example    # Secret template
├── hpa.yaml              # Horizontal Pod Autoscaler
├── pdb.yaml              # Pod Disruption Budget
└── README.md             # Template documentation
```

## Best Practices

### Resource Management

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Health Checks

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Security Context

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000
  capabilities:
    drop:
      - ALL
  readOnlyRootFilesystem: true
```

### Pod Disruption Budgets

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: myapp
```

## Common Tasks

### Debugging

```bash
# View pod logs
kubectl logs <pod-name>
kubectl logs -f <pod-name>
kubectl logs <pod-name> --previous

# Execute commands in pod
kubectl exec -it <pod-name> -- /bin/sh

# Port forwarding
kubectl port-forward <pod-name> 8080:80

# Describe resources
kubectl describe pod <pod-name>
kubectl describe node <node-name>
```

### Scaling

```bash
# Manual scaling
kubectl scale deployment myapp --replicas=5

# Autoscaling
kubectl autoscale deployment myapp --min=2 --max=10 --cpu-percent=80
```

### Updates

```bash
# Rolling update
kubectl set image deployment/myapp myapp=myapp:v2

# Rollback
kubectl rollout undo deployment/myapp

# Check rollout status
kubectl rollout status deployment/myapp

# View rollout history
kubectl rollout history deployment/myapp
```

### Resource Management

```bash
# View resource usage
kubectl top nodes
kubectl top pods

# Get all resources
kubectl get all

# Delete resources
kubectl delete -f deployment.yaml
kubectl delete deployment myapp
```

## Configuration Management

### ConfigMaps

```bash
# Create from literal
kubectl create configmap myconfig --from-literal=key=value

# Create from file
kubectl create configmap myconfig --from-file=config.properties

# Use in pod
env:
  - name: CONFIG_KEY
    valueFrom:
      configMapKeyRef:
        name: myconfig
        key: key
```

### Secrets

```bash
# Create secret
kubectl create secret generic mysecret --from-literal=password=secret123

# Create from file
kubectl create secret generic mysecret --from-file=./secret.txt

# Use in pod
env:
  - name: PASSWORD
    valueFrom:
      secretKeyRef:
        name: mysecret
        key: password
```

## Networking

### Services

```yaml
# ClusterIP (internal)
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8080
  selector:
    app: myapp
```

```yaml
# LoadBalancer (external)
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8080
  selector:
    app: myapp
```

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: backend
```

## Monitoring

### Metrics

```bash
# Install metrics server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# View metrics
kubectl top nodes
kubectl top pods -n default
```

### Logging

```bash
# View logs
kubectl logs -l app=myapp
kubectl logs -f deployment/myapp

# Stream logs from multiple pods
stern myapp
```

## Troubleshooting

### Pod Issues

```bash
# Pod not starting
kubectl describe pod <pod-name>
kubectl logs <pod-name>

# Image pull errors
kubectl describe pod <pod-name> | grep -A 5 Events

# Resource constraints
kubectl top pod <pod-name>
```

### Network Issues

```bash
# Test connectivity
kubectl run -it --rm debug --image=busybox --restart=Never -- sh
wget -O- http://service-name

# DNS resolution
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup service-name
```

### Certificate Issues

```bash
# Check cert-manager logs
kubectl logs -n cert-manager deploy/cert-manager

# Describe certificate
kubectl describe certificate my-cert
```

## Security

### RBAC

```bash
# Create service account
kubectl create serviceaccount myapp

# Create role
kubectl create role pod-reader --verb=get,list,watch --resource=pods

# Bind role to service account
kubectl create rolebinding myapp-binding --role=pod-reader --serviceaccount=default:myapp
```

### Pod Security

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
  containers:
    - name: app
      image: myapp:latest
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop:
            - ALL
        readOnlyRootFilesystem: true
```

## Related Resources

- [Kubernetes Cheatsheet](cheatsheet.md)
- [Helm Charts](#)
- [Kubectl Quick Reference](#)

## Support

For issues or questions:

- Review Kubernetes official documentation
- Check template README files
- Open an issue on GitHub
