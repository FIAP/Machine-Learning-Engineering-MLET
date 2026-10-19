#!/usr/bin/env python3
"""Atualiza o índice de fases/módulos/aulas no README.md."""
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
START = "<!-- INDEX:START -->"
END = "<!-- INDEX:END -->"
PHASE_PREFIX = "Fase"


def natural_key(path: Path):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", path.name)]


def subdirs(path: Path):
    return sorted(
        (d for d in path.iterdir() if d.is_dir() and not d.name.startswith(".")),
        key=natural_key,
    )


def url(path: Path) -> str:
    return "./" + quote(path.relative_to(ROOT).as_posix())


def build_index() -> str:
    out = []
    phases = [p for p in subdirs(ROOT) if p.name.startswith(PHASE_PREFIX)]
    for phase in phases:
        out.append(f"## [{phase.name}]({url(phase)})")
        for module in subdirs(phase):
            out.append(f"- [{module.name}]({url(module)})")
            lessons = sorted(
                (c for c in module.iterdir()
                 if (c.is_dir() and not c.name.startswith("."))
                 or (c.suffix == ".md" and c.name.lower() != "readme.md")),
                key=natural_key,
            )
            for lesson in lessons:
                name = lesson.stem if lesson.is_file() else lesson.name
                out.append(f"  - [{name}]({url(lesson)})")
        out.append("")
    return "\n".join(out)


def main():
    content = README.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(content):
        raise SystemExit(f"Marcadores {START} / {END} não encontrados no README.")

    block = f"{START}\n\n{build_index()}\n{END}"
    new_content = pattern.sub(lambda _: block, content)
    if new_content != content:
        README.write_text(new_content, encoding="utf-8")
        print("README atualizado.")
    else:
        print("Índice já está em dia.")


if __name__ == "__main__":
    main()