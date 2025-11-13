"""Snippet management"""

from pathlib import Path
from typing import Optional, Dict, List
import yaml
import json

REPO_ROOT = Path(__file__).parent.parent.parent.absolute()
SNIPPETS_DIR = REPO_ROOT / "snippets"
CACHE_DIR = Path.home() / ".cache" / "bp"

# Ensure directories exist
SNIPPETS_DIR.mkdir(parents=True, exist_ok=True)


def get_snippet(snippet_name: str, format: str = 'raw') -> Optional[str]:
    """Get a snippet by name"""
    # Load snippet database
    snippets_db = load_snippets()

    # Find snippet
    snippet = snippets_db.get(snippet_name)

    if not snippet:
        # Try fuzzy match
        for key in snippets_db.keys():
            if snippet_name.lower() in key.lower():
                snippet = snippets_db[key]
                break

    if not snippet:
        return None

    # Format output
    if format == 'json':
        return json.dumps(snippet, indent=2)
    elif format == 'yaml':
        return yaml.dump(snippet, default_flow_style=False)
    else:
        # Raw content
        return snippet.get('content', '')


def load_snippets() -> Dict:
    """Load all snippets from YAML files"""
    snippets = {}

    if not SNIPPETS_DIR.exists():
        return snippets

    for yaml_file in SNIPPETS_DIR.glob('**/*.yaml'):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if isinstance(data, dict) and 'snippets' in data:
                for snippet in data['snippets']:
                    name = snippet.get('name')
                    if name:
                        snippets[name] = snippet
            elif isinstance(data, dict):
                # Single snippet file
                name = data.get('name') or yaml_file.stem
                snippets[name] = data

        except Exception as e:
            print(f"Warning: Could not load {yaml_file}: {e}")

    return snippets


def list_snippets(category: Optional[str] = None, tag: Optional[str] = None) -> List[Dict]:
    """List available snippets"""
    snippets_db = load_snippets()

    results = []
    for name, snippet in snippets_db.items():
        if category and snippet.get('category') != category:
            continue

        if tag and tag not in snippet.get('tags', []):
            continue

        results.append({
            'name': name,
            'description': snippet.get('description', ''),
            'category': snippet.get('category', 'general'),
            'tags': snippet.get('tags', [])
        })

    return results


def search_snippets(query: str) -> List[Dict]:
    """Search snippets"""
    snippets_db = load_snippets()
    query_lower = query.lower()

    results = []
    for name, snippet in snippets_db.items():
        score = 0

        # Name match
        if query_lower in name.lower():
            score += 10

        # Description match
        if query_lower in snippet.get('description', '').lower():
            score += 5

        # Content match
        if query_lower in snippet.get('content', '').lower():
            score += 3

        # Tag match
        if query_lower in ' '.join(snippet.get('tags', [])).lower():
            score += 4

        if score > 0:
            results.append({
                'name': name,
                'description': snippet.get('description', ''),
                'category': snippet.get('category', 'general'),
                'score': score
            })

    results.sort(key=lambda x: x['score'], reverse=True)
    return results


def create_snippet_database():
    """Create initial snippet database structure"""
    # Docker snippets
    docker_snippets = {
        'snippets': [
            {
                'name': 'docker-compose-postgres',
                'description': 'PostgreSQL with Docker Compose',
                'category': 'docker',
                'tags': ['docker', 'postgres', 'database'],
                'content': '''version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: {{database_name}}
      POSTGRES_USER: {{database_user}}
      POSTGRES_PASSWORD: {{database_password}}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
'''
            },
            {
                'name': 'dockerfile-java',
                'description': 'Multi-stage Dockerfile for Java applications',
                'category': 'docker',
                'tags': ['docker', 'java', 'dockerfile'],
                'content': '''FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
'''
            }
        ]
    }

    # Save docker snippets
    with open(SNIPPETS_DIR / 'docker.yaml', 'w') as f:
        yaml.dump(docker_snippets, f, default_flow_style=False)

    # Kubernetes snippets
    k8s_snippets = {
        'snippets': [
            {
                'name': 'kubernetes-deployment',
                'description': 'Basic Kubernetes Deployment',
                'category': 'kubernetes',
                'tags': ['kubernetes', 'deployment'],
                'content': '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{app_name}}
  labels:
    app: {{app_name}}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {{app_name}}
  template:
    metadata:
      labels:
        app: {{app_name}}
    spec:
      containers:
      - name: {{app_name}}
        image: {{image_name}}:{{image_tag}}
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
'''
            }
        ]
    }

    with open(SNIPPETS_DIR / 'kubernetes.yaml', 'w') as f:
        yaml.dump(k8s_snippets, f, default_flow_style=False)


if __name__ == '__main__':
    # Create initial snippet database
    create_snippet_database()
    print("✓ Created snippet database")

    # Test snippet retrieval
    snippets = load_snippets()
    print(f"Loaded {len(snippets)} snippets")
