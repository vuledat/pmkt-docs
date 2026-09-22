"""Synchronize PMKT skills from .claude to .agents; stdlib-only, no deletion."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(base):
    result = {}
    if base.is_symlink() or base.resolve() != base.absolute():
        raise ValueError(f"Linked skill root is not supported: {base}")
    if not base.exists():
        return result
    for folder in sorted(base.iterdir()):
        if not folder.is_dir():
            continue  # archives beside skill directories are not skill resources
        if folder.is_symlink() or folder.resolve() != folder.absolute():
            raise ValueError(f"Linked skill directory is not supported: {folder}")
        if not (folder / "SKILL.md").is_file():
            raise ValueError(f"Missing SKILL.md: {folder}")
        for path in sorted(folder.rglob("*")):
            if path.is_symlink() or path.resolve() != path.absolute():
                raise ValueError(f"Resource escapes skill root: {path}")
            if path.is_file():
                result[path.relative_to(base).as_posix()] = path.read_bytes()
    return result


def validate(files):
    problems = []
    for name, data in files.items():
        if not name.endswith(".md"):
            continue
        text = data.decode("utf-8-sig")
        folder = name.split("/")[0]
        if name == f"{folder}/SKILL.md":
            front = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|$)", text, re.S)
            if not front:
                problems.append(f"Invalid frontmatter: {name}")
                continue
            title = re.search(r"^name:\s*(.+)$", front[1], re.M)
            description = re.search(r"^description:\s*\S.+$", front[1], re.M)
            if not title or title[1].strip() != folder or not re.fullmatch(r"[a-z0-9-]{1,63}", folder):
                problems.append(f"Invalid skill name: {name}")
            if not description:
                problems.append(f"Missing description: {name}")
        # PMKT uses skill-root-relative code references and Markdown links.
        for ref in re.findall(r"(?:references|scripts|assets)/[\w./-]+\.[\w]+", text):
            if f"{folder}/{ref}" not in files:
                problems.append(f"Missing resource: {name} -> {ref}")
    return sorted(set(problems))


def synchronize(root, write=False, adopt=False):
    root = root.resolve()
    source = inventory(root / ".claude/skills")
    target_root = root / ".agents/skills"
    target = inventory(target_root)
    manifest = target_root / ".pmkt-sync.json"
    if manifest.is_symlink():
        raise ValueError("Manifest must not be a symlink")
    if not source:
        raise ValueError("No source skills")
    problems = validate(source)
    extra = sorted(set(target) - set(source))
    problems.extend(f"Unmanaged target resource (preserved): {p}" for p in extra)
    changed = sorted(p for p in source if source[p] != target.get(p))
    expected = {p: digest(data) for p, data in source.items()}
    previous = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else None
    if previous is not None and (not isinstance(previous, dict) or previous.get("version") != 1
                                 or not isinstance(previous.get("files"), dict)):
        raise ValueError("Invalid sync manifest")
    if write:
        for p in changed:
            if p not in target:
                continue
            old = previous.get("files", {}).get(p) if previous else None
            if old != digest(target[p]) and not (previous is None and adopt):
                problems.append(f"Local target edit; reconcile with source first: {p}")
    if problems:
        return 1, problems
    if not write:
        messages = [f"DRIFT {p}" for p in changed]
        if previous != {"version": 1, "files": expected}:
            messages.append("DRIFT sync manifest")
        return (1, messages) if messages else (0, [f"OK: {len(source)} resources synchronized"])
    target_root.mkdir(parents=True, exist_ok=True)
    for p in changed:
        out = target_root / p
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(source[p])
    manifest.write_text(json.dumps({"version": 1, "files": expected}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0, [f"OK: wrote {len(changed)} resources; {len(expected)} managed"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument("--adopt-source", action="store_true", help="First migration only, after reviewing both copies")
    args = parser.parse_args()
    if args.adopt_source and not args.write:
        parser.error("--adopt-source requires --write")
    try:
        status, messages = synchronize(Path(__file__).resolve().parents[2], args.write, args.adopt_source)
    except (OSError, ValueError, UnicodeError) as exc:
        status, messages = 1, [str(exc)]
    for message in messages:
        print(message)
    return status


if __name__ == "__main__":
    sys.exit(main())
