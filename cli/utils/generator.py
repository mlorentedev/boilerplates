"""Project generation from templates"""

import shutil
import os
from pathlib import Path
from typing import Dict, Optional, List
import yaml
import json
import re

from .templates import get_template_path, get_template_files


def generate_project(template: str, name: str, output_dir: str = '.',
                    vars_file: Optional[str] = None, interactive: bool = False,
                    dry_run: bool = False, force: bool = False) -> Dict:
    """Generate a project from a template"""

    # Get template path
    template_path = get_template_path(template)

    if not template_path or not template_path.exists():
        raise ValueError(f"Template not found: {template}")

    # Prepare output directory
    output_path = Path(output_dir) / name

    if output_path.exists() and not force:
        raise ValueError(f"Directory already exists: {output_path}")

    # Load variables
    variables = {
        'project_name': name,
        'project_name_snake': name.replace('-', '_'),
        'project_name_camel': ''.join(word.capitalize() for word in name.split('-')),
    }

    # Load from vars file
    if vars_file:
        with open(vars_file, 'r') as f:
            if vars_file.endswith('.yaml') or vars_file.endswith('.yml'):
                file_vars = yaml.safe_load(f)
            else:
                file_vars = json.load(f)
            variables.update(file_vars)

    # Interactive mode
    if interactive:
        variables.update(prompt_for_variables(template))

    # Get template files
    template_files = get_template_files(template)

    result = {
        'template': template,
        'name': name,
        'output': str(output_path),
        'files': [],
        'files_created': 0,
        'next_steps': []
    }

    if dry_run:
        # Just list what would be created
        for file_path in template_files:
            rel_path = file_path.relative_to(template_path)
            dest_path = output_path / rel_path
            result['files'].append(str(dest_path))
        return result

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    # Copy and process template files
    for file_path in template_files:
        rel_path = file_path.relative_to(template_path)
        dest_path = output_path / rel_path

        # Create parent directories
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Read file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Process template variables
            content = process_template_vars(content, variables)

            # Process filename
            dest_path_str = str(dest_path)
            for key, value in variables.items():
                dest_path_str = dest_path_str.replace(f'{{{{{key}}}}}', value)
            dest_path = Path(dest_path_str)

            # Write file
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(content)

            result['files'].append(str(dest_path))
            result['files_created'] += 1

        except UnicodeDecodeError:
            # Binary file, just copy
            shutil.copy2(file_path, dest_path)
            result['files'].append(str(dest_path))
            result['files_created'] += 1

    # Add next steps based on template type
    result['next_steps'] = generate_next_steps(template, name, output_path)

    return result


def process_template_vars(content: str, variables: Dict) -> str:
    """Process template variables in content"""
    for key, value in variables.items():
        # Replace {{variable}} with value
        content = content.replace(f'{{{{{key}}}}}', str(value))

    return content


def prompt_for_variables(template: str) -> Dict:
    """Prompt user for template variables"""
    import click

    variables = {}

    # Common variables
    prompts = {
        'description': 'Project description',
        'author': 'Author name',
        'email': 'Author email',
        'version': 'Version',
        'license': 'License',
    }

    # Template-specific prompts
    if 'spring' in template.lower():
        prompts.update({
            'group_id': 'Maven group ID',
            'artifact_id': 'Maven artifact ID',
            'java_version': 'Java version',
            'spring_boot_version': 'Spring Boot version',
        })
    elif 'terraform' in template.lower():
        prompts.update({
            'region': 'AWS/Azure region',
            'environment': 'Environment (dev/staging/prod)',
        })
    elif 'kubernetes' in template.lower():
        prompts.update({
            'namespace': 'Kubernetes namespace',
            'replicas': 'Number of replicas',
        })

    click.echo("\nEnter template variables (press Enter for default):\n")

    for key, prompt_text in prompts.items():
        value = click.prompt(prompt_text, default='', show_default=False)
        if value:
            variables[key] = value

    return variables


def generate_next_steps(template: str, name: str, output_path: Path) -> List[str]:
    """Generate next steps based on template type"""
    steps = []

    if 'spring' in template.lower():
        steps.extend([
            f"cd {name}",
            "./mvnw clean install",
            "./mvnw spring-boot:run",
            "Visit http://localhost:8080"
        ])
    elif 'terraform' in template.lower():
        steps.extend([
            f"cd {name}",
            "terraform init",
            "terraform plan",
            "terraform apply"
        ])
    elif 'kubernetes' in template.lower():
        steps.extend([
            f"cd {name}",
            "kubectl apply -f .",
            "kubectl get pods"
        ])
    elif 'docker' in template.lower():
        steps.extend([
            f"cd {name}",
            "docker-compose up -d",
            "docker-compose ps"
        ])
    elif 'ansible' in template.lower():
        steps.extend([
            f"cd {name}",
            "ansible-playbook -i inventory.ini playbook.yml"
        ])
    else:
        steps.extend([
            f"cd {name}",
            "# Follow the README.md for instructions"
        ])

    return steps
