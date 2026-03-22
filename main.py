#!/usr/bin/env python3

import re
import shutil
import argparse
from pathlib import Path

INCLUDE_RE = re.compile(r'@include\("([^"]+)"\)')
MAX_DEPTH = 32

def is_partial(path: Path) -> bool:
    return any(part.startswith("_") for part in path.parts)


def process_file(src_file: Path, stack: list[Path], depth: int) -> str:
    if depth > MAX_DEPTH:
        raise RecursionError(
            f"Max include depth ({MAX_DEPTH}) exceeded.\n"
            f"Include chain: {' -> '.join(str(p) for p in stack)}"
        )

    if src_file in stack:
        chain = " -> ".join(str(p) for p in stack) + f" -> {src_file}"
        raise ValueError(f"Circular include detected:\n  {chain}")

    if not src_file.exists():
        includer = stack[-1] if stack else None
        location = f" (included from {includer})" if includer else ""
        raise FileNotFoundError(f"Include not found: {src_file}{location}")

    lines = src_file.read_text(encoding="utf-8").splitlines(keepends=True)
    out = []

    for lineno, line in enumerate(lines, start=1):
        match = INCLUDE_RE.search(line)
        if match:
            include_path = src_file.parent / match.group(1)
            include_path = include_path.resolve()
            try:
                included = process_file(include_path, stack + [src_file], depth + 1)
            except FileNotFoundError as e:
                raise FileNotFoundError(
                    f"{src_file}:{lineno}: {e}"
                ) from None
            indent = line[: len(line) - len(line.lstrip())]
            if indent:
                included = "\n".join(indent + l for l in included.splitlines())
            out.append(included)
        else:
            out.append(line.rstrip("\n"))

    return "\n".join(out)


def build(src: Path, out: Path):
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    processed = 0
    copied = 0
    skipped = 0

    for src_file in sorted(src.rglob("*")):
        if not src_file.is_file():
            continue

        rel = src_file.relative_to(src)

        if is_partial(rel):
            skipped += 1
            continue

        dest = out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)

        if src_file.suffix.lower() == ".html":
            try:
                result = process_file(src_file.resolve(), stack=[], depth=0)
            except (FileNotFoundError, ValueError, RecursionError) as e:
                print(f"  error  {rel}\n         {e}")
                continue
            dest.write_text(result, encoding="utf-8")
            print(f"  build  {rel}")
            processed += 1
        else:
            shutil.copy2(src_file, dest)
            print(f"  copy   {rel}")
            copied += 1

    print(
        f"\nDone. {processed} built, {copied} copied, {skipped} partial(s) skipped."
    )


def main():
    parser = argparse.ArgumentParser(
        description="htmlpp - simple HTML preprocessor"
    )
    parser.add_argument(
        "--src", default="src", type=Path, metavar="DIR",
        help="Source directory (default: src)"
    )
    parser.add_argument(
        "--out", default="dist", type=Path, metavar="DIR",
        help="Output directory (default: dist)"
    )
    args = parser.parse_args()

    src = args.src.resolve()
    out = args.out.resolve()

    if not src.exists():
        parser.error(f"Source directory not found: {src}")
    if not src.is_dir():
        parser.error(f"Source path is not a directory: {src}")

    print(f"htmlpp: {src} -> {out}\n")
    build(src, out)

if __name__ == "__main__":
    main()