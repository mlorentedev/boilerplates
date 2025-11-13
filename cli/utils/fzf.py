"""
fzf integration for interactive search
Provides fuzzy finding with preview
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional, List, Dict
import json

from .search import load_search_index, search_docs

REPO_ROOT = Path(__file__).parent.parent.parent.absolute()


def check_fzf() -> bool:
    """Check if fzf is installed"""
    try:
        subprocess.run(['fzf', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def interactive_search(category: Optional[str] = None,
                      tag: Optional[str] = None,
                      preview: bool = True) -> Optional[str]:
    """
    Interactive search using fzf
    Returns selected item or None
    """
    if not check_fzf():
        print("Error: fzf not found. Please install fzf:", file=sys.stderr)
        print("  Ubuntu/Debian: sudo apt install fzf", file=sys.stderr)
        print("  macOS: brew install fzf", file=sys.stderr)
        print("  https://github.com/junegunn/fzf#installation", file=sys.stderr)
        return None

    # Load index
    index = load_search_index()

    # Prepare items for fzf
    items = []

    # Add documents
    for doc in index['documents']:
        if category and doc['category'] != category:
            continue
        if tag and tag not in doc.get('tags', []):
            continue

        # Format: "title | category | path"
        item_line = f"{doc['title']} | {doc['category']} | {doc['path']}"
        items.append((item_line, doc))

    # Add templates
    for template in index['templates']:
        if category and template['category'] != category:
            continue

        item_line = f"{template['name']} [Template] | {template['category']} | {template['path']}"
        items.append((item_line, template))

    if not items:
        print("No items found")
        return None

    # Prepare fzf input
    fzf_input = '\n'.join(item[0] for item in items)

    # Build fzf command
    fzf_cmd = [
        'fzf',
        '--ansi',
        '--multi',
        '--reverse',
        '--height=80%',
        '--border',
        '--prompt=Search> ',
        '--header=Search documentation and templates (Tab: select, Enter: open, Esc: cancel)',
        '--preview-window=right:60%:wrap',
    ]

    # Add preview if enabled
    if preview:
        preview_cmd = f'cat {{}}'
        fzf_cmd.extend([
            '--preview',
            f'echo {{}} | cut -d"|" -f3 | xargs -I {{}} cat "{REPO_ROOT}/docs/{{}}" 2>/dev/null || echo "No preview available"'
        ])

    # Add colors
    fzf_cmd.extend([
        '--color=fg:#d0d0d0,bg:#1c1c1c,hl:#5f87af',
        '--color=fg+:#d0d0d0,bg+:#262626,hl+:#5fd7ff',
        '--color=info:#afaf87,prompt:#d7005f,pointer:#af5fff',
        '--color=marker:#87ff00,spinner:#af5fff,header:#87afaf'
    ])

    try:
        # Run fzf
        result = subprocess.run(
            fzf_cmd,
            input=fzf_input.encode(),
            capture_output=True,
            check=True
        )

        selected = result.stdout.decode().strip()

        if selected:
            # Extract path from selection
            path = selected.split('|')[2].strip()
            return path

        return None

    except subprocess.CalledProcessError:
        # User cancelled or error
        return None
    except Exception as e:
        print(f"Error running fzf: {e}", file=sys.stderr)
        return None


def interactive_multi_select(items: List[str],
                            prompt: str = "Select items> ",
                            preview: Optional[str] = None) -> List[str]:
    """
    Multi-select with fzf
    Returns list of selected items
    """
    if not check_fzf():
        return []

    fzf_input = '\n'.join(items)

    fzf_cmd = [
        'fzf',
        '--multi',
        '--reverse',
        '--height=50%',
        '--border',
        f'--prompt={prompt}',
        '--header=Tab: select, Enter: confirm, Esc: cancel',
    ]

    if preview:
        fzf_cmd.extend(['--preview', preview])

    try:
        result = subprocess.run(
            fzf_cmd,
            input=fzf_input.encode(),
            capture_output=True,
            check=True
        )

        selected = result.stdout.decode().strip().split('\n')
        return [s for s in selected if s]

    except subprocess.CalledProcessError:
        return []


def interactive_template_select(category: Optional[str] = None) -> Optional[str]:
    """Select a template interactively"""
    index = load_search_index()

    templates = []
    for template in index['templates']:
        if category and template['category'] != category:
            continue
        templates.append(f"{template['name']} ({template['category']})")

    if not templates:
        print("No templates found")
        return None

    fzf_cmd = [
        'fzf',
        '--reverse',
        '--height=40%',
        '--border',
        '--prompt=Select template> ',
        '--header=Choose a template',
    ]

    try:
        result = subprocess.run(
            fzf_cmd,
            input='\n'.join(templates).encode(),
            capture_output=True,
            check=True
        )

        selected = result.stdout.decode().strip()
        if selected:
            # Extract template name
            template_name = selected.split('(')[0].strip()
            return template_name

        return None

    except subprocess.CalledProcessError:
        return None


def fuzzy_find_file(directory: Path, pattern: str = "*") -> Optional[Path]:
    """Fuzzy find a file in directory"""
    if not check_fzf():
        return None

    try:
        # Use find to list files
        find_result = subprocess.run(
            ['find', str(directory), '-type', 'f', '-name', pattern],
            capture_output=True,
            check=True
        )

        files = find_result.stdout.decode().strip().split('\n')

        if not files or not files[0]:
            return None

        # Make paths relative to directory
        rel_files = [str(Path(f).relative_to(directory)) for f in files]

        # Use fzf to select
        fzf_cmd = [
            'fzf',
            '--reverse',
            '--height=40%',
            '--border',
            '--prompt=Select file> ',
        ]

        result = subprocess.run(
            fzf_cmd,
            input='\n'.join(rel_files).encode(),
            capture_output=True,
            check=True
        )

        selected = result.stdout.decode().strip()
        if selected:
            return directory / selected

        return None

    except subprocess.CalledProcessError:
        return None


def preview_generator(item: Dict) -> str:
    """Generate preview content for an item"""
    lines = []

    lines.append(f"Title: {item.get('title', 'N/A')}")
    lines.append(f"Category: {item.get('category', 'N/A')}")

    if item.get('description'):
        lines.append(f"\nDescription:\n{item['description']}")

    if item.get('tags'):
        lines.append(f"\nTags: {', '.join(item['tags'])}")

    if item.get('content'):
        lines.append(f"\nContent preview:\n{item['content'][:500]}")

    return '\n'.join(lines)


if __name__ == '__main__':
    # Test fzf integration
    print("Testing fzf integration...")

    if check_fzf():
        print("✓ fzf found")

        # Test interactive search
        result = interactive_search()
        if result:
            print(f"Selected: {result}")
        else:
            print("No selection")
    else:
        print("✗ fzf not found")
        sys.exit(1)
