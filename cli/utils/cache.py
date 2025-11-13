"""Cache management"""

import shutil
import time
from pathlib import Path
from typing import Dict

CACHE_DIR = Path.home() / ".cache" / "bp"

CACHE_DIR.mkdir(parents=True, exist_ok=True)


def clear_cache():
    """Clear all cache"""
    if CACHE_DIR.exists():
        for item in CACHE_DIR.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)


def rebuild_index():
    """Rebuild search index"""
    from .search import build_search_index

    build_search_index()


def show_stats() -> Dict:
    """Show cache statistics"""
    stats = {
        'cache_dir': str(CACHE_DIR),
        'size_mb': 0,
        'files': 0,
        'last_modified': 'N/A'
    }

    if not CACHE_DIR.exists():
        return stats

    total_size = 0
    file_count = 0
    latest_mtime = 0

    for item in CACHE_DIR.rglob('*'):
        if item.is_file():
            file_count += 1
            total_size += item.stat().st_size
            mtime = item.stat().st_mtime
            if mtime > latest_mtime:
                latest_mtime = mtime

    stats['size_mb'] = round(total_size / (1024 * 1024), 2)
    stats['files'] = file_count

    if latest_mtime > 0:
        stats['last_modified'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                              time.localtime(latest_mtime))

    return stats


def clean_cache(max_age_days: int = 7):
    """Remove old cache files"""
    if not CACHE_DIR.exists():
        return

    now = time.time()
    max_age_seconds = max_age_days * 24 * 60 * 60

    for item in CACHE_DIR.rglob('*'):
        if item.is_file():
            age = now - item.stat().st_mtime
            if age > max_age_seconds:
                item.unlink()
