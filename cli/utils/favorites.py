"""Favorites management"""

import json
from pathlib import Path
from typing import List

CACHE_DIR = Path.home() / ".cache" / "bp"
FAVORITES_FILE = CACHE_DIR / "favorites.json"

CACHE_DIR.mkdir(parents=True, exist_ok=True)


def load_favorites() -> List[str]:
    """Load favorites from file"""
    if not FAVORITES_FILE.exists():
        return []

    try:
        with open(FAVORITES_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return []


def save_favorites(favorites: List[str]):
    """Save favorites to file"""
    try:
        with open(FAVORITES_FILE, 'w') as f:
            json.dump(favorites, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save favorites: {e}")


def add_favorite(template: str):
    """Add template to favorites"""
    favorites = load_favorites()

    if template not in favorites:
        favorites.append(template)
        save_favorites(favorites)


def remove_favorite(template: str):
    """Remove template from favorites"""
    favorites = load_favorites()

    if template in favorites:
        favorites.remove(template)
        save_favorites(favorites)


def list_favorites() -> List[str]:
    """List all favorites"""
    return load_favorites()


def use_favorite(template: str, name: str):
    """Generate project from favorite template"""
    from .generator import generate_project

    if template not in load_favorites():
        raise ValueError(f"{template} is not in favorites")

    return generate_project(template, name)
