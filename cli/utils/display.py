"""Display utilities"""

from typing import List, Dict


def display_table(items: List[Dict]):
    """Display items as a table"""
    if not items:
        print("No items to display")
        return

    # Calculate column widths
    headers = ['Name', 'Category', 'Type']
    rows = []

    for item in items:
        rows.append([
            item.get('name', 'N/A'),
            item.get('category', 'N/A'),
            item.get('type', 'N/A')
        ])

    # Calculate widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    # Print header
    header_line = ' | '.join(h.ljust(w) for h, w in zip(headers, widths))
    print(header_line)
    print('-' * len(header_line))

    # Print rows
    for row in rows:
        row_line = ' | '.join(str(cell).ljust(w) for cell, w in zip(row, widths))
        print(row_line)


def display_tree(items: List[Dict], indent: int = 0):
    """Display items as a tree"""
    # Group by category
    categories = {}
    for item in items:
        category = item.get('category', 'Other')
        if category not in categories:
            categories[category] = []
        categories[category].append(item)

    # Print tree
    for category, category_items in sorted(categories.items()):
        print(' ' * indent + f'📁 {category}')
        for item in category_items:
            print(' ' * (indent + 2) + f'└─ {item.get("name", "N/A")}')


def format_size(bytes: int) -> str:
    """Format bytes as human-readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024
    return f"{bytes:.1f} TB"


def format_time(seconds: float) -> str:
    """Format seconds as human-readable time"""
    if seconds < 0.001:
        return f"{seconds*1000000:.0f}μs"
    elif seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"
