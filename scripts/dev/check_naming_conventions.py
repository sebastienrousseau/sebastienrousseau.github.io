#!/usr/bin/env python3
"""Enforces repository naming conventions on all git-tracked source files."""

import subprocess
import sys
from pathlib import Path

# Root-level uppercase files that comply with industry standard conventions
# and platform-specific integrations.
ALLOWED_ROOT_UPPERCASE = {
    # Main repository documentation entrypoint, standard across all code hubs
    "README.md",
    # Auto-detected by GitHub Security Advisories tab and security alerts
    "SECURITY.md",
    # Canonical license declaration file name
    "LICENSE",
    # Historical log of repository release notes
    "CHANGELOG.md",
    # Operational instructions for environment staging and deployments
    "DEPLOY.md",
    # Default Makefile target entrypoint for GNU Make toolchain orchestration
    "Makefile",
}


def validate_directory_part(part: str, file_path: str) -> bool:
    """Validates that a directory name complies with lowercase conventions."""
    # Hidden/dot config directories are exempted from naming checks as they
    # contain standard config payloads. E.g., .github/ for CI workflows and
    # .well-known/ for RFC-defined protocols (WKD keys, security contacts).
    if part.startswith("."):
        return True

    # SSG source directories starting with underscore (e.g. _layouts, _posts)
    # must be lowercase.
    clean_part = part[1:] if part.startswith("_") else part

    # Must be lowercase and kebab-case/snake_case
    if not clean_part.islower() or any(char.isupper() for char in clean_part):
        print(
            f"Directory naming violation: '{part}' in '{file_path}' contains uppercase characters or is not lowercase."
        )
        return False
    return True


def validate_python_name(name: str, file_path: str) -> bool:
    """Checks if a python file name is strict snake_case."""
    clean_name = name[:-3]
    if clean_name.startswith("_"):
        clean_name = clean_name[1:]
    if not clean_name.islower() or "-" in clean_name:
        print(f"Python file naming violation: '{file_path}' must be strict snake_case.")
        return False
    return True


def validate_shell_name(name: str, file_path: str) -> bool:
    """Checks if a shell script file name is strict kebab-case."""
    clean_name = name[:-3]
    if not clean_name.islower() or "_" in clean_name:
        print(f"Shell script naming violation: '{file_path}' must be strict kebab-case.")
        return False
    return True


def validate_js_name(name: str, ext: str, file_path: str) -> bool:
    """Checks if a javascript file name is lowercase."""
    clean_name = name[: name.find(ext)]
    if any(char.isupper() for char in clean_name):
        print(f"JavaScript file naming violation: '{file_path}' must be lowercase.")
        return False
    return True


def validate_markdown_name(name: str, path: Path, file_path: str) -> bool:
    """Checks if a markdown file name is lowercase (except for README and MANIFEST)."""
    if len(path.parent.parts) > 0:
        clean_name = name[:-3]
        # Allow standard uppercase names within subdirectories:
        # - README: explain directory structure and domain scope to developers
        # - MANIFEST: package catalogs, static file listings, or translations maps
        if clean_name in ("README", "MANIFEST"):
            return True
        if any(char.isupper() for char in clean_name):
            print(f"Markdown file naming violation: '{file_path}' must be lowercase.")
            return False
    return True


def validate_file_name(path: Path, file_path: str) -> bool:
    """Validates that a file name complies with extension-specific casing rules."""
    name = path.name
    ext = path.suffix.lower()

    # Root files exceptions
    if len(path.parent.parts) == 0 and name in ALLOWED_ROOT_UPPERCASE:
        return True

    if ext == ".py":
        return validate_python_name(name, file_path)
    if ext == ".sh":
        return validate_shell_name(name, file_path)
    if ext in (".js", ".mjs"):
        return validate_js_name(name, ext, file_path)
    if ext == ".md":
        return validate_markdown_name(name, path, file_path)

    return True


def check_naming_conventions() -> bool:
    """Gathers all tracked files and runs validation checks on directories and names."""
    try:
        output = subprocess.check_output(["git", "ls-files"], text=True)
    except subprocess.SubprocessError as e:
        print(f"Error calling git ls-files: {e}")
        return False

    files = output.splitlines()
    failed = False

    for file_path in files:
        path = Path(file_path)

        # Skip checking compiled deployment output directory
        if path.parts and path.parts[0] == "docs":
            continue

        # 1. Check directory segment casing
        for part in path.parent.parts:
            if not validate_directory_part(part, file_path):
                failed = True

        # 2. Check file name casing and pattern matching
        if not validate_file_name(path, file_path):
            failed = True

    return not failed


if __name__ == "__main__":
    success = check_naming_conventions()
    if not success:
        print("\nNaming convention check FAILED.")
        sys.exit(1)
    print("All naming conventions passed.")
    sys.exit(0)
