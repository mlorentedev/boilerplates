"""Cheatsheet generation"""

from pathlib import Path
from typing import Optional
import subprocess

REPO_ROOT = Path(__file__).parent.parent.parent.absolute()
DOCS_DIR = REPO_ROOT / "docs"


def generate_cheatsheet(topic: str, format: str = 'md',
                       output: Optional[str] = None,
                       style: str = 'light',
                       size: str = 'a4') -> Optional[str]:
    """Generate a cheatsheet for a topic"""

    # Find cheatsheet file
    cheatsheet_file = DOCS_DIR / 'cheatsheets' / f'{topic}.md'

    if not cheatsheet_file.exists():
        # Try to find in topic directory
        cheatsheet_file = DOCS_DIR / topic / 'cheatsheet.md'

    if not cheatsheet_file.exists():
        raise ValueError(f"Cheatsheet not found for topic: {topic}")

    # Determine output file
    if not output:
        output = f'{topic}-cheatsheet.{format}'

    output_path = Path(output)

    # Generate based on format
    if format == 'md':
        # Just copy the markdown file
        import shutil
        shutil.copy(cheatsheet_file, output_path)
        return str(output_path)

    elif format == 'html':
        # Convert to HTML using pandoc
        try:
            subprocess.run(
                ['pandoc', str(cheatsheet_file), '-o', str(output_path),
                 '--standalone', '--self-contained'],
                check=True
            )
            return str(output_path)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise Exception("pandoc is required for HTML generation")

    elif format == 'pdf':
        # Convert to PDF using pandoc
        try:
            subprocess.run(
                ['pandoc', str(cheatsheet_file), '-o', str(output_path),
                 '--pdf-engine=xelatex', f'-V', f'papersize={size}'],
                check=True
            )
            return str(output_path)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise Exception("pandoc and xelatex are required for PDF generation")

    elif format == 'png':
        # Convert to PNG (requires imagemagick)
        # First convert to HTML, then to PNG
        try:
            html_file = output_path.with_suffix('.html')
            subprocess.run(
                ['pandoc', str(cheatsheet_file), '-o', str(html_file),
                 '--standalone', '--self-contained'],
                check=True
            )

            subprocess.run(
                ['convert', '-density', '300', str(html_file), str(output_path)],
                check=True
            )

            html_file.unlink()  # Clean up HTML file
            return str(output_path)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise Exception("pandoc and imagemagick are required for PNG generation")

    else:
        raise ValueError(f"Unknown format: {format}")
