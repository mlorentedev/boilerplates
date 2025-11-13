"""Template management utilities"""

from pathlib import Path
from typing import Optional, List, Dict
import os

from .search import load_search_index

REPO_ROOT = Path(__file__).parent.parent.parent.absolute()
DOCS_DIR = REPO_ROOT / "docs"


def show_template(template_name: str, raw: bool = False, preview: bool = False) -> Optional[str]:
    """Show template documentation"""
    index = load_search_index()

    # Find template
    template = None
    for t in index['templates']:
        if t['name'] == template_name or t['name'].replace('-', '_') == template_name:
            template = t
            break

    if not template:
        # Try to find in documents
        for doc in index['documents']:
            if doc['title'].lower() == template_name.lower() or \
               Path(doc['path']).stem == template_name:
                # Read and return document
                try:
                    with open(doc['full_path'], 'r', encoding='utf-8') as f:
                        content = f.read()

                    if raw:
                        return content
                    elif preview:
                        # Return first 500 chars
                        return content[:500] + '...'
                    else:
                        return content
                except Exception as e:
                    return f"Error reading template: {e}"

        return None

    # Check if documentation exists for template
    doc_path = DOCS_DIR / template['category'] / f"{template['name']}.md"

    if doc_path.exists():
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if raw:
                return content
            elif preview:
                return content[:500] + '...'
            else:
                return content
        except Exception as e:
            return f"Error reading documentation: {e}"

    # Fallback: show basic info
    info = f"# {template['name']}\n\n"
    info += f"Category: {template['category']}\n"
    info += f"Path: {template['path']}\n\n"
    info += f"Template directory at: {template['full_path']}\n"

    return info


def list_templates(category: Optional[str] = None, tag: Optional[str] = None) -> List[Dict]:
    """List available templates"""
    index = load_search_index()

    templates = []

    for template in index['templates']:
        if category and template['category'] != category:
            continue

        templates.append({
            'name': template['name'],
            'category': template['category'],
            'path': template['path'],
            'type': 'template'
        })

    # Also include documented templates
    for doc in index['documents']:
        if category and doc['category'] != category:
            continue

        if tag and tag not in doc.get('tags', []):
            continue

        # Only include docs that look like templates
        if 'template' in doc['title'].lower() or \
           'boilerplate' in doc['title'].lower():
            templates.append({
                'name': doc['title'],
                'category': doc['category'],
                'path': doc['path'],
                'type': 'documentation'
            })

    return templates


def get_template_path(template_name: str) -> Optional[Path]:
    """Get the filesystem path for a template"""
    index = load_search_index()

    for template in index['templates']:
        if template['name'] == template_name or \
           template['name'].replace('-', '_') == template_name:
            return Path(template['full_path'])

    return None


def get_template_files(template_name: str) -> List[Path]:
    """Get all files in a template directory"""
    template_path = get_template_path(template_name)

    if not template_path or not template_path.exists():
        return []

    files = []
    for item in template_path.rglob('*'):
        if item.is_file():
            files.append(item)

    return files


def template_exists(template_name: str) -> bool:
    """Check if a template exists"""
    return get_template_path(template_name) is not None
