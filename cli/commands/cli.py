#!/usr/bin/env python3
"""
Main CLI interface for bp tool
"""

import click
import os
import sys
import json
import subprocess
from pathlib import Path

# Get the repository root directory
REPO_ROOT = Path(__file__).parent.parent.parent.absolute()
BP_HOME = REPO_ROOT
DOCS_DIR = BP_HOME / "docs"
CONFIG_DIR = Path.home() / ".config" / "bp"
CACHE_DIR = Path.home() / ".cache" / "bp"
CONFIG_FILE = CONFIG_DIR / "config.yaml"

# Version
VERSION = "1.0.0"

# Ensure directories exist
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)


@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True, help='Show version')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.option('--quiet', '-q', is_flag=True, help='Suppress output')
@click.pass_context
def main(ctx, version, verbose, quiet):
    """bp - Fast searchable boilerplates and documentation system"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['quiet'] = quiet

    if version:
        click.echo(f"bp version {VERSION}")
        sys.exit(0)

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
@click.argument('query', nargs=-1, required=False)
@click.option('--category', '-c', help='Filter by category')
@click.option('--tag', '-t', help='Filter by tag')
@click.option('--limit', '-l', default=20, help='Limit results')
@click.option('--recent', is_flag=True, help='Search recent history')
@click.option('--history', is_flag=True, help='Show search history')
@click.pass_context
def search(ctx, query, category, tag, limit, recent, history):
    """Search through all documentation and snippets"""
    from utils.search import search_docs, search_history, save_search

    if history:
        results = search_history()
        if results:
            click.echo("Recent searches:")
            for i, result in enumerate(results[:limit], 1):
                click.echo(f"  {i}. {result['query']} ({result['timestamp']})")
        else:
            click.echo("No search history found")
        return

    query_str = ' '.join(query) if query else ''

    if not query_str and not ctx.obj.get('quiet'):
        # Interactive mode with fzf
        try:
            from utils.fzf import interactive_search
            result = interactive_search(category=category, tag=tag)
            if result:
                click.echo(result)
        except ImportError:
            click.echo("Error: fzf is required for interactive search", err=True)
            click.echo("Install fzf: https://github.com/junegunn/fzf", err=True)
            sys.exit(1)
        return

    # Perform search
    results = search_docs(query_str, category=category, tag=tag, limit=limit)

    if not results:
        click.echo(f"No results found for: {query_str}")
        return

    # Save search to history
    save_search(query_str)

    # Display results
    if not ctx.obj.get('quiet'):
        click.echo(f"Found {len(results)} results:\n")

    for i, result in enumerate(results, 1):
        if ctx.obj.get('quiet'):
            click.echo(result['path'])
        else:
            click.echo(f"{i}. {result['title']}")
            click.echo(f"   Category: {result.get('category', 'N/A')}")
            click.echo(f"   Path: {result['path']}")
            if result.get('snippet'):
                click.echo(f"   {result['snippet']}")
            click.echo()


@main.command()
@click.argument('category')
@click.argument('query', nargs=-1, required=False)
@click.option('--limit', '-l', default=20, help='Limit results')
@click.pass_context
def find(ctx, category, query, limit):
    """Search within a specific category"""
    from utils.search import search_docs

    # Map category aliases
    category_map = {
        'tf': 'terraform',
        'k8s': 'kubernetes',
        'dk': 'docker',
        'ans': 'ansible',
        'gh': 'github-actions'
    }

    category = category_map.get(category, category)
    query_str = ' '.join(query) if query else ''

    if not query_str:
        # List category contents
        from utils.search import list_category
        results = list_category(category)
    else:
        # Search within category
        results = search_docs(query_str, category=category, limit=limit)

    if not results:
        click.echo(f"No results found in {category}")
        return

    if not ctx.obj.get('quiet'):
        click.echo(f"Found {len(results)} results in {category}:\n")

    for i, result in enumerate(results, 1):
        if ctx.obj.get('quiet'):
            click.echo(result['path'])
        else:
            click.echo(f"{i}. {result['title']}")
            click.echo(f"   {result.get('description', '')}")
            click.echo()


@main.command()
@click.argument('template')
@click.option('--raw', is_flag=True, help='Show raw markdown')
@click.option('--preview', is_flag=True, help='Show preview only')
@click.option('--copy', is_flag=True, help='Copy to clipboard')
def show(template, raw, preview, copy):
    """Display documentation for a specific template"""
    from utils.templates import show_template

    content = show_template(template, raw=raw, preview=preview)

    if content:
        if copy:
            try:
                import pyperclip
                pyperclip.copy(content)
                click.echo("Content copied to clipboard!")
            except ImportError:
                click.echo("Error: pyperclip required for clipboard support", err=True)
                sys.exit(1)
        else:
            click.echo(content)
    else:
        click.echo(f"Template not found: {template}", err=True)
        sys.exit(1)


@main.command()
@click.argument('category', required=False)
@click.option('--tag', '-t', help='Filter by tag')
@click.option('--format', '-f', default='table', type=click.Choice(['table', 'json', 'yaml']))
@click.option('--tree', is_flag=True, help='Show as tree structure')
def list(category, tag, format, tree):
    """List all available templates"""
    from utils.templates import list_templates

    templates = list_templates(category=category, tag=tag)

    if not templates:
        click.echo("No templates found")
        return

    if format == 'json':
        click.echo(json.dumps(templates, indent=2))
    elif format == 'yaml':
        import yaml
        click.echo(yaml.dump(templates, default_flow_style=False))
    elif tree:
        from utils.display import display_tree
        display_tree(templates)
    else:
        from utils.display import display_table
        display_table(templates)


@main.command()
@click.argument('template')
@click.argument('name')
@click.option('--output', '-o', default='.', help='Output directory')
@click.option('--vars', '-v', type=click.Path(exists=True), help='Variables file')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode')
@click.option('--dry-run', is_flag=True, help='Show what would be generated')
@click.option('--force', '-f', is_flag=True, help='Overwrite existing files')
def new(template, name, output, vars, interactive, dry_run, force):
    """Generate a new project from a template"""
    from utils.generator import generate_project

    try:
        result = generate_project(
            template=template,
            name=name,
            output_dir=output,
            vars_file=vars,
            interactive=interactive,
            dry_run=dry_run,
            force=force
        )

        if dry_run:
            click.echo("Dry run - would create:")
            for file in result['files']:
                click.echo(f"  {file}")
        else:
            click.echo(f"✓ Generated {template} as '{name}' in {output}")
            click.echo(f"  Created {result['files_created']} files")
            if result.get('next_steps'):
                click.echo("\nNext steps:")
                for step in result['next_steps']:
                    click.echo(f"  • {step}")

    except Exception as e:
        click.echo(f"Error generating project: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('snippet')
@click.option('--preview', is_flag=True, help='Preview before copying')
@click.option('--edit', is_flag=True, help='Edit before copying')
@click.option('--format', '-f', default='raw', type=click.Choice(['raw', 'json', 'yaml']))
def copy(snippet, preview, edit, format):
    """Copy a snippet to clipboard"""
    from utils.snippets import get_snippet

    content = get_snippet(snippet, format=format)

    if not content:
        click.echo(f"Snippet not found: {snippet}", err=True)
        sys.exit(1)

    if preview:
        click.echo("Preview:")
        click.echo("=" * 50)
        click.echo(content)
        click.echo("=" * 50)

        if not click.confirm("Copy to clipboard?"):
            return

    if edit:
        import tempfile
        import subprocess

        editor = os.getenv('EDITOR', 'vim')
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            subprocess.run([editor, temp_file], check=True)
            with open(temp_file, 'r') as f:
                content = f.read()
        finally:
            os.unlink(temp_file)

    try:
        import pyperclip
        pyperclip.copy(content)
        click.echo(f"✓ Copied {snippet} to clipboard")
    except ImportError:
        # Fallback to xclip or pbcopy
        try:
            if sys.platform == 'darwin':
                subprocess.run(['pbcopy'], input=content.encode(), check=True)
            else:
                subprocess.run(['xclip', '-selection', 'clipboard'], input=content.encode(), check=True)
            click.echo(f"✓ Copied {snippet} to clipboard")
        except (subprocess.CalledProcessError, FileNotFoundError):
            click.echo("Error: Could not copy to clipboard", err=True)
            click.echo("Install pyperclip: pip install pyperclip", err=True)
            sys.exit(1)


@main.command()
@click.argument('page', required=False)
@click.option('--port', '-p', default=8000, help='Server port')
@click.option('--no-open', is_flag=True, help="Don't open browser")
@click.option('--build', is_flag=True, help='Build before serving')
def web(page, port, no_open, build):
    """Open documentation in web browser"""
    import subprocess
    import time
    import webbrowser

    os.chdir(REPO_ROOT)

    if build:
        click.echo("Building documentation...")
        subprocess.run(['mkdocs', 'build'], check=True)

    click.echo(f"Starting documentation server on port {port}...")

    # Start mkdocs server in background
    process = subprocess.Popen(
        ['mkdocs', 'serve', '-a', f'0.0.0.0:{port}'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for server to start
    time.sleep(2)

    url = f'http://localhost:{port}'
    if page:
        url += f'/{page}/'

    if not no_open:
        click.echo(f"Opening {url}")
        webbrowser.open(url)
    else:
        click.echo(f"Documentation available at {url}")

    try:
        # Keep server running
        click.echo("Press Ctrl+C to stop the server")
        process.wait()
    except KeyboardInterrupt:
        click.echo("\nStopping server...")
        process.terminate()
        process.wait()


@main.command()
@click.argument('topic')
@click.option('--format', '-f', default='md', type=click.Choice(['pdf', 'png', 'md', 'html']))
@click.option('--output', '-o', help='Output file')
@click.option('--style', '-s', default='light', type=click.Choice(['light', 'dark']))
@click.option('--size', '-z', default='a4', type=click.Choice(['a4', 'letter', 'a5']))
def cheatsheet(topic, format, output, style, size):
    """Generate a cheatsheet for a topic"""
    from utils.cheatsheet import generate_cheatsheet

    try:
        result = generate_cheatsheet(
            topic=topic,
            format=format,
            output=output,
            style=style,
            size=size
        )

        if result:
            click.echo(f"✓ Generated {topic} cheatsheet: {result}")
        else:
            click.echo(f"Error generating cheatsheet for {topic}", err=True)
            sys.exit(1)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('n', required=False, type=int)
@click.option('--limit', '-l', default=10, help='Show last n items')
@click.option('--type', '-t', type=click.Choice(['search', 'template', 'all']), default='all')
@click.option('--clear', is_flag=True, help='Clear recent history')
def recent(n, limit, type, clear):
    """Show recently used templates and searches"""
    from utils.history import get_recent, clear_history

    if clear:
        clear_history(type)
        click.echo(f"✓ Cleared {type} history")
        return

    items = get_recent(type=type, limit=n or limit)

    if not items:
        click.echo("No recent items found")
        return

    click.echo(f"Recent {type}:\n")
    for i, item in enumerate(items, 1):
        click.echo(f"{i}. {item['name']} ({item['timestamp']})")
        if item.get('description'):
            click.echo(f"   {item['description']}")
        click.echo()


@main.command()
@click.argument('action')
@click.argument('template', required=False)
@click.argument('name', required=False)
def favorite(action, template, name):
    """Manage favorite templates"""
    from utils.favorites import add_favorite, remove_favorite, list_favorites, use_favorite

    if action == 'add':
        if not template:
            click.echo("Error: template required", err=True)
            sys.exit(1)
        add_favorite(template)
        click.echo(f"✓ Added {template} to favorites")

    elif action == 'remove':
        if not template:
            click.echo("Error: template required", err=True)
            sys.exit(1)
        remove_favorite(template)
        click.echo(f"✓ Removed {template} from favorites")

    elif action == 'list':
        favorites = list_favorites()
        if favorites:
            click.echo("Favorites:")
            for i, fav in enumerate(favorites, 1):
                click.echo(f"  {i}. {fav}")
        else:
            click.echo("No favorites yet")

    elif action == 'use':
        if not template or not name:
            click.echo("Error: template and name required", err=True)
            sys.exit(1)
        use_favorite(template, name)

    else:
        click.echo(f"Unknown action: {action}", err=True)
        click.echo("Valid actions: add, remove, list, use")
        sys.exit(1)


@main.command()
@click.argument('action')
def cache(action):
    """Manage search cache and index"""
    from utils.cache import clear_cache, rebuild_index, show_stats, clean_cache

    if action == 'clear':
        clear_cache()
        click.echo("✓ Cache cleared")

    elif action == 'rebuild':
        click.echo("Rebuilding search index...")
        rebuild_index()
        click.echo("✓ Index rebuilt")

    elif action == 'stats':
        stats = show_stats()
        click.echo("Cache statistics:")
        for key, value in stats.items():
            click.echo(f"  {key}: {value}")

    elif action == 'clean':
        clean_cache()
        click.echo("✓ Old cache files removed")

    else:
        click.echo(f"Unknown action: {action}", err=True)
        click.echo("Valid actions: clear, rebuild, stats, clean")
        sys.exit(1)


@main.command()
@click.argument('shell', type=click.Choice(['bash', 'zsh', 'fish', 'powershell']))
def completion(shell):
    """Generate shell completion script"""
    # This would be implemented with click's completion support
    click.echo(f"# Completion script for {shell}")
    click.echo("# Add this to your shell configuration file")

    if shell == 'bash':
        click.echo('eval "$(_BP_COMPLETE=bash_source bp)"')
    elif shell == 'zsh':
        click.echo('eval "$(_BP_COMPLETE=zsh_source bp)"')
    elif shell == 'fish':
        click.echo('_BP_COMPLETE=fish_source bp | source')
    elif shell == 'powershell':
        click.echo('Register-ArgumentCompleter -Native -CommandName bp -ScriptBlock {')
        click.echo('    param($wordToComplete, $commandAst, $cursorPosition)')
        click.echo('    $env:_BP_COMPLETE="powershell_complete" bp $commandAst.CommandElements[1..$commandAst.CommandElements.Count] | ForEach-Object {')
        click.echo('        [System.Management.Automation.CompletionResult]::new($_.Split(",")[0], $_.Split(",")[1], "ParameterValue", $_.Split(",")[1])')
        click.echo('    }')
        click.echo('}')


@main.command()
@click.option('--check', is_flag=True, help='Check for updates')
@click.option('--version', help='Update to specific version')
@click.option('--templates', is_flag=True, help='Update only templates')
@click.option('--cli', is_flag=True, help='Update only CLI')
def update(check, version, templates, cli):
    """Update bp CLI and templates"""
    from utils.updater import check_updates, update_cli, update_templates

    if check:
        latest = check_updates()
        if latest:
            click.echo(f"New version available: {latest}")
            click.echo("Run 'bp update' to update")
        else:
            click.echo("You're up to date!")
        return

    try:
        if templates or (not cli and not templates):
            click.echo("Updating templates...")
            update_templates()
            click.echo("✓ Templates updated")

        if cli or (not cli and not templates):
            click.echo("Updating CLI...")
            update_cli(version)
            click.echo("✓ CLI updated")

        click.echo("\n✓ Update complete!")

    except Exception as e:
        click.echo(f"Error updating: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--check', is_flag=True, help='Check for newer version')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed version info')
def version(check, verbose):
    """Show version information"""
    click.echo(f"bp version {VERSION}")

    if verbose:
        click.echo(f"Repository: {REPO_ROOT}")
        click.echo(f"Config: {CONFIG_FILE}")
        click.echo(f"Cache: {CACHE_DIR}")
        click.echo(f"Python: {sys.version}")

    if check:
        from utils.updater import check_updates
        latest = check_updates()
        if latest and latest != VERSION:
            click.echo(f"\nNew version available: {latest}")
            click.echo("Run 'bp update' to update")
        else:
            click.echo("\nYou're up to date!")


if __name__ == '__main__':
    main()
