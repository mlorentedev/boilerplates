"""History and recent items tracking"""

import json
import time
from pathlib import Path
from typing import List, Dict

CACHE_DIR = Path.home() / ".cache" / "bp"
HISTORY_FILE = CACHE_DIR / "history.json"

CACHE_DIR.mkdir(parents=True, exist_ok=True)


def add_to_history(item_type: str, name: str, description: str = ''):
    """Add item to history"""
    history = load_history()

    # Add new item
    history.insert(0, {
        'type': item_type,
        'name': name,
        'description': description,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'unix_timestamp': time.time()
    })

    # Keep only last 100 items
    history = history[:100]

    # Save history
    save_history(history)


def load_history() -> List[Dict]:
    """Load history from file"""
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return []


def save_history(history: List[Dict]):
    """Save history to file"""
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save history: {e}")


def get_recent(type: str = 'all', limit: int = 10) -> List[Dict]:
    """Get recent items"""
    history = load_history()

    if type != 'all':
        history = [item for item in history if item['type'] == type]

    return history[:limit]


def clear_history(type: str = 'all'):
    """Clear history"""
    if type == 'all':
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()
    else:
        history = load_history()
        history = [item for item in history if item['type'] != type]
        save_history(history)
