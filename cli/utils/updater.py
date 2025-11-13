"""Update functionality"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).parent.parent.parent.absolute()


def check_updates() -> Optional[str]:
    """Check for updates"""
    try:
        # Fetch latest version from git
        result = subprocess.run(
            ['git', 'fetch', '--tags'],
            cwd=REPO_ROOT,
            capture_output=True
        )

        # Get latest tag
        result = subprocess.run(
            ['git', 'describe', '--tags', '--abbrev=0', 'origin/main'],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return result.stdout.strip()

        return None

    except Exception:
        return None


def update_cli(version: Optional[str] = None):
    """Update CLI"""
    try:
        # Pull latest changes
        if version:
            subprocess.run(
                ['git', 'checkout', version],
                cwd=REPO_ROOT,
                check=True
            )
        else:
            subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                cwd=REPO_ROOT,
                check=True
            )

    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to update CLI: {e}")


def update_templates():
    """Update templates"""
    try:
        # Pull latest changes
        subprocess.run(
            ['git', 'pull', 'origin', 'main'],
            cwd=REPO_ROOT,
            check=True
        )

    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to update templates: {e}")
