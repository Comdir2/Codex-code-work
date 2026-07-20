#!/usr/bin/env python3
"""Validate the repository's portable skill structure without dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


EXPECTED_SKILL_NAME = "code-work"
CHECKOUT_REVISION = "9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0"
SERVICE_REQUEST_URL = (
    "https://github.com/Comdir2/Codex-engineering-guardrails/issues/new"
    "?template=service-request.yml"
)
REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "README.md",
    "README.ru.md",
    "SERVICES.md",
    "CHANGELOG.md",
    "LICENSE",
    ".github/workflows/validate.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
)
SERVICE_LINK_FILES = ("README.md", "README.ru.md", "SERVICES.md")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
MARKDOWN_REFERENCE_RE = re.compile(r"(?m)^ {0,3}\[[^\]]+\]:\s*(\S+)")


def _parse_restricted_yaml_scalar(
    raw_value: str, path: Path, number: int, errors: list[str]
) -> str:
    """Parse the deliberately small scalar subset used by repository metadata."""

    value = raw_value.strip()
    if not value:
        errors.append(f"{path.as_posix()}:{number}: scalar value must be non-empty")
        return ""
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            errors.append(f"{path.as_posix()}:{number}: invalid double-quoted scalar")
            return ""
        if not isinstance(parsed, str):
            errors.append(f"{path.as_posix()}:{number}: quoted scalar must be a string")
            return ""
        return parsed
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            errors.append(f"{path.as_posix()}:{number}: invalid single-quoted scalar")
            return ""
        interior = value[1:-1]
        if "'" in interior.replace("''", ""):
            errors.append(f"{path.as_posix()}:{number}: invalid single-quoted scalar")
            return ""
        return interior.replace("''", "'")
    if value[0] in "-?:,[]{}#&*!|>'\"%@`" or any(ch in value for ch in "[]{}'\""):
        errors.append(f"{path.as_posix()}:{number}: unsupported or malformed plain scalar")
        return ""
    if ": " in value or " #" in value:
        errors.append(f"{path.as_posix()}:{number}: ambiguous plain scalar")
        return ""
    return value


def _parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, [f"{path.name}: YAML frontmatter must start on the first line"]

    try:
        closing = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration:
        return {}, [f"{path.name}: YAML frontmatter has no closing delimiter"]

    metadata: dict[str, str] = {}
    for number, line in enumerate(lines[1:closing], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[:1].isspace() or ":" not in line:
            errors.append(f"{path.name}:{number}: unsupported frontmatter entry")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in metadata:
            errors.append(f"{path.name}:{number}: duplicate frontmatter key {key!r}")
            continue
        metadata[key] = _parse_restricted_yaml_scalar(value, path, number, errors)

    if not any(line.strip().startswith("# ") for line in lines[closing + 1 :]):
        errors.append(f"{path.name}: skill body must contain a top-level heading")
    return metadata, errors


def _parse_agent_interface(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    if not any(line.strip() == "interface:" for line in lines):
        return {}, [f"{path.as_posix()}: missing interface mapping"]

    interface: dict[str, str] = {}
    field_re = re.compile(r"^  ([A-Za-z_][A-Za-z0-9_]*):\s*(.*?)\s*$")
    for number, line in enumerate(lines, start=1):
        match = field_re.match(line)
        if not match:
            continue
        key, value = match.groups()
        if key in interface:
            errors.append(f"{path.as_posix()}:{number}: duplicate interface field {key!r}")
            continue
        interface[key] = _parse_restricted_yaml_scalar(value, path, number, errors)
    return interface, errors


def _markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0] if target else ""


def _validate_local_links(root: Path) -> list[str]:
    errors: list[str] = []
    for document in sorted(root.rglob("*.md")):
        if ".git" in document.parts:
            continue
        text = document.read_text(encoding="utf-8")
        targets = [match.group(1) for match in MARKDOWN_LINK_RE.finditer(text)]
        targets.extend(match.group(1) for match in MARKDOWN_REFERENCE_RE.finditer(text))
        for raw_target in targets:
            target = _markdown_target(raw_target)
            if not target or target.startswith("#") or target.startswith("//"):
                continue
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            relative_target = unquote(parsed.path)
            if not relative_target:
                continue
            resolved = (document.parent / relative_target).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                errors.append(
                    f"{document.relative_to(root)}: local link escapes repository: {target}"
                )
                continue
            if not resolved.exists():
                errors.append(
                    f"{document.relative_to(root)}: missing local link target: {target}"
                )
    return errors


def _validate_workflow(root: Path) -> list[str]:
    errors: list[str] = []
    path = root / ".github/workflows/validate.yml"
    if not path.is_file():
        return errors
    workflow = path.read_text(encoding="utf-8")
    checkout_revisions = re.findall(r"uses:\s*actions/checkout@([^\s#]+)", workflow)
    if checkout_revisions != [CHECKOUT_REVISION]:
        errors.append(
            ".github/workflows/validate.yml: checkout must use the single reviewed revision "
            f"{CHECKOUT_REVISION}"
        )
    if "persist-credentials: false" not in workflow:
        errors.append(".github/workflows/validate.yml: checkout credentials must not persist")
    if "pull_request_target:" in workflow:
        errors.append(".github/workflows/validate.yml: pull_request_target is forbidden")
    if not re.search(r"(?m)^permissions:\s*\n  contents: read\s*$", workflow):
        errors.append(".github/workflows/validate.yml: contents permission must be read-only")
    return errors


def validate_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).is_file():
            errors.append(f"missing required file: {relative_path}")
    if errors:
        return errors

    metadata, frontmatter_errors = _parse_frontmatter(root / "SKILL.md")
    errors.extend(frontmatter_errors)
    if metadata.get("name") != EXPECTED_SKILL_NAME:
        errors.append(
            f"SKILL.md: name must be {EXPECTED_SKILL_NAME!r}, got {metadata.get('name')!r}"
        )
    if not metadata.get("description"):
        errors.append("SKILL.md: description must be non-empty")

    interface, interface_errors = _parse_agent_interface(root / "agents/openai.yaml")
    errors.extend(interface_errors)
    for field in ("display_name", "short_description", "default_prompt"):
        if not interface.get(field):
            errors.append(f"agents/openai.yaml: interface.{field} must be non-empty")
    if f"${EXPECTED_SKILL_NAME}" not in interface.get("default_prompt", ""):
        errors.append(
            f"agents/openai.yaml: default_prompt must mention ${EXPECTED_SKILL_NAME}"
        )

    for relative_path in SERVICE_LINK_FILES:
        text = (root / relative_path).read_text(encoding="utf-8")
        if SERVICE_REQUEST_URL not in text:
            errors.append(f"{relative_path}: missing central service-request link")

    errors.extend(_validate_local_links(root))
    errors.extend(_validate_workflow(root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the parent of this script directory)",
    )
    args = parser.parse_args()
    errors = validate_repository(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print("Validation passed: required files, metadata, service links, and local links are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
