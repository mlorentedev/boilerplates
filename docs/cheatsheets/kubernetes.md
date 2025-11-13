# Kubernetes Cheatsheet

Essential kubectl commands and Kubernetes operations.

## Cluster Management

```bash
# Cluster info
kubectl cluster-info
kubectl version
kubectl api-resources

# Node management
kubectl get nodes
kubectl describe node <node>
kubectl top nodes
kubectl cordon <node>
kubectl uncordon <node>
kubectl drain <node>
```

## Pod Management

```bash
# List pods
kubectl get pods
kubectl get pods -n <namespace>
kubectl get pods -o wide
kubectl get pods --all-namespaces

# Describe pod
kubectl describe pod <pod>

# Pod logs
kubectl logs <pod>
kubectl logs -f <pod>
kubectl logs <pod> -c <container>
kubectl logs <pod> --previous

# Execute commands
kubectl exec -it <pod> -- /bin/bash
kubectl exec <pod> -- <command>

# Port forwarding
kubectl port-forward <pod> 8080:80
```

## Deployment Management

```bash
# Create deployment
kubectl create deployment <name> --image=<image>

# List deployments
kubectl get deployments

# Scale deployment
kubectl scale deployment <name> --replicas=3

# Update image
kubectl set image deployment/<name> <container>=<image>

# Rollout management
kubectl rollout status deployment/<name>
kubectl rollout history deployment/<name>
kubectl rollout undo deployment/<name>
kubectl rollout restart deployment/<name>
```

## Service Management

```bash
# List services
kubectl get services
kubectl get svc

# Describe service
kubectl describe service <service>

# Expose deployment
kubectl expose deployment <name> --port=80 --type=LoadBalancer
```

## Namespace Management

```bash
# List namespaces
kubectl get namespaces
kubectl get ns

# Create namespace
kubectl create namespace <name>

# Delete namespace
kubectl delete namespace <name>

# Set default namespace
kubectl config set-context --current --namespace=<name>
```

## ConfigMap and Secrets

```bash
# ConfigMaps
kubectl create configmap <name> --from-literal=key=value
kubectl create configmap <name> --from-file=<file>
kubectl get configmaps
kubectl describe configmap <name>

# Secrets
kubectl create secret generic <name> --from-literal=key=value
kubectl create secret generic <name> --from-file=<file>
kubectl get secrets
kubectl describe secret <name>
```

## Resource Management

```bash
# Apply manifests
kubectl apply -f <file>
kubectl apply -f <directory>
kubectl apply -k <kustomize-dir>

# Delete resources
kubectl delete -f <file>
kubectl delete pod <pod>
kubectl delete deployment <deployment>

# Get all resources
kubectl get all
kubectl get all -n <namespace>

# Label management
kubectl label pod <pod> env=prod
kubectl label pod <pod> env-

# Annotation management
kubectl annotate pod <pod> description="text"
```

## Debugging

```bash
# Describe resources
kubectl describe <resource> <name>

# View events
kubectl get events
kubectl get events --sort-by='.lastTimestamp'

# Resource usage
kubectl top pods
kubectl top nodes

# Debug pod
kubectl run -it --rm debug --image=busybox --restart=Never -- sh

# Copy files
kubectl cp <pod>:/path/to/file /local/path
kubectl cp /local/path <pod>:/path/to/file
```

## Context and Config

```bash
# View config
kubectl config view

# Get contexts
kubectl config get-contexts

# Switch context
kubectl config use-context <context>

# Set namespace
kubectl config set-context --current --namespace=<namespace>
```

## Resource Shortcuts

```bash
po    # pods
svc   # services
deploy # deployments
rs    # replicasets
sts   # statefulsets
ds    # daemonsets
ing   # ingresses
cm    # configmaps
ns    # namespaces
pv    # persistentvolumes
pvc   # persistentvolumeclaims
```

## Common Tasks

### Create Resources
```bash
kubectl run nginx --image=nginx
kubectl create deployment nginx --image=nginx
kubectl expose pod nginx --port=80 --name=nginx-service
```

### Update Resources
```bash
kubectl edit deployment <name>
kubectl patch deployment <name> -p '{"spec":{"replicas":5}}'
kubectl set image deployment/<name> container=image:tag
```

### Scale Resources
```bash
kubectl scale deployment <name> --replicas=3
kubectl autoscale deployment <name> --min=2 --max=10 --cpu-percent=80
```

### Resource Monitoring
```bash
kubectl get pods --watch
kubectl logs -f <pod>
kubectl top pods
kubectl top nodes
```

## Tips

### Output Formats
```bash
kubectl get pods -o wide
kubectl get pods -o yaml
kubectl get pods -o json
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
```

### Filtering
```bash
kubectl get pods --field-selector status.phase=Running
kubectl get pods -l app=nginx
kubectl get pods -l 'env in (prod,staging)'
```

### Dry Run
```bash
kubectl run nginx --image=nginx --dry-run=client -o yaml > pod.yaml
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml
```
