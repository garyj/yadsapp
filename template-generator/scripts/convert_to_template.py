#!/usr/bin/env python3
"""
Convert the Django project to a template that can be used with django-admin startproject --template
"""

import os
import shutil
from pathlib import Path

# Files and directories to exclude from the template
EXCLUDE_PATTERNS = [
    '.git',
    '.github',
    '__pycache__',
    '*.pyc',
    '.pytest_cache',
    'node_modules',
    '.venv',
    'venv',
    'logs',
    'tmp',
    'static/dist',
    'media',
    '.env',
    '.env.local',
    '.ruff_cache',
    'template-generator',  # Don't include the template generator itself
    'template-output',  # Don't include the output directory
    'README.md',  # Root README.md is for this repo, not the template
]

# Directory and file renames
RENAMES = {
    'src/yads': 'src/project_name',
}


def should_exclude(path: Path, exclude_patterns: list) -> bool:
    """Check if a path should be excluded based on patterns. Explicit allows .gitkeep files."""
    path_str = str(path)
    if path.name in {'.gitkeep', '.gitignore'}:
        return False
    for pattern in exclude_patterns:
        if pattern in path_str or path.name == pattern:
            return True
        if pattern.startswith('*.') and path.name.endswith(pattern[1:]):
            return True
    return False


def replace_content(content: str, replacements: dict) -> str:
    """Replace content with template variables."""
    for old, new in replacements.items():
        content = content.replace(old, new)
    return content


def copy_and_convert_file(src: Path, dest: Path, replacements: dict) -> None:
    """Copy a file and apply template conversions."""
    dest.parent.mkdir(parents=True, exist_ok=True)

    if src.suffix in ['.py', '.toml', '.json', '.js', '.md', '.yml', '.yaml', '.html', '.css'] or src.name in [
        'justfile',
        'Dockerfile',
        'entrypoint',
        'start',
    ]:
        # Text files - apply replacements
        try:
            with src.open(encoding='utf-8') as f:
                content = f.read()

            content = replace_content(content, replacements)

            with dest.open('w', encoding='utf-8') as f:
                f.write(content)
        except UnicodeDecodeError:
            # If file can't be decoded as text, copy as binary
            shutil.copy2(src, dest)
    else:
        # Binary files - copy as-is
        shutil.copy2(src, dest)


def main() -> None:
    """Main conversion function."""
    source_dir = Path()
    output_dir = Path('template-output')

    # Clean output directory
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()

    # Content replacements
    replacements = {
        'yads': '{{ project_name }}',
    }

    # Walk through source directory
    for root, dirs, files in os.walk(source_dir):
        root_path = Path(root)

        # Skip excluded directories
        dirs[:] = [d for d in dirs if not should_exclude(root_path / d, EXCLUDE_PATTERNS)]

        for file in files:
            src_file = root_path / file

            # Skip excluded files
            if should_exclude(src_file, EXCLUDE_PATTERNS):
                continue

            # Calculate relative path
            rel_path = src_file.relative_to(source_dir)

            # Apply renames to path
            dest_path_str = str(rel_path)
            for old_path, new_path in RENAMES.items():
                dest_path_str = dest_path_str.replace(old_path, new_path)

            dest_file = output_dir / dest_path_str

            # Copy and convert file
            copy_and_convert_file(src_file, dest_file, replacements)

    # Copy template files from template-generator/template-files/
    template_files_dir = Path('template-generator/template-files')

    # Copy README.md (DO NOT replace content)
    src_readme = template_files_dir / 'README.md'
    if src_readme.exists():
        shutil.copy2(src_readme, output_dir / 'README.md')

    # Copy .env.example with replacements
    src_env = template_files_dir / '.env.example'
    if src_env.exists():
        with src_env.open(encoding='utf-8') as f:
            env_content = f.read()
        env_content = replace_content(env_content, replacements)
        with (output_dir / '.env.example').open('w', encoding='utf-8') as f:
            f.write(env_content)

    # Copy the .github directory with replacements
    src_github = template_files_dir / '.github'
    if src_github.exists():
        dest_github = output_dir / '.github'
        for root, _dirs, files in os.walk(src_github):
            root_path = Path(root)

            for file in files:
                src_file = root_path / file
                # Calculate relative path from .github directory
                rel_path = src_file.relative_to(src_github)
                dest_file = dest_github / rel_path

                # Copy and convert file with replacements
                copy_and_convert_file(src_file, dest_file, replacements)

    print(f'✅ Django template created in {output_dir}')
    print('\nTemplate structure:')
    for root, _dirs, files in os.walk(output_dir):
        level = root.replace(str(output_dir), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{Path(root).name}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')


if __name__ == '__main__':
    main()
