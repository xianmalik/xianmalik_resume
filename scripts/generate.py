#!/usr/bin/env python3
"""
Minimal YAML → TeX generator. Reads data/*.yml and writes sections/*.tex.
No-op if data directory or files are missing, or if PyYAML is unavailable.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except Exception:
    sys.exit(0)

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
SECTIONS_DIR = REPO_ROOT / "sections"

if not DATA_DIR.exists() or not SECTIONS_DIR.exists():
    sys.exit(0)


def read_yaml(filename: str):
    path = DATA_DIR / filename
    if not path.exists():
        return None
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def latex_escape(s: str) -> str:
    return (
        str(s)
        .replace("\\", "\\textbackslash{}")
        .replace("%", "\\%")
        .replace("&", "\\&")
        .replace("#", "\\#")
        .replace("_", "\\_")
        .replace("{", "\\{")
        .replace("}", "\\}")
        .replace("$", "\\$")
    )


def gen_summary(data):
    if not data or not data.get("summary"):
        return None
    return (
        "\\cvsection{ABOUT ME}\n\n"
        "\\begin{cvparagraph}\n"
        f"  {data['summary']}\n"
        "\\end{cvparagraph}\n"
    )


def gen_experience(data):
    if not data or not isinstance(data.get("positions"), list):
        return None

    chunks = []
    for p in data["positions"]:
        bullets = "\n".join(
            f"                \\item {{{latex_escape(t)}}}" for t in p.get("items", [])
        )
        chunks.append(
            "    \\cventry\n"
            f"        {{{latex_escape(p.get('title', ''))}}}\n"
            f"        {{{latex_escape(p.get('company', ''))}}}\n"
            f"        {{{latex_escape(p.get('location', ''))}}}\n"
            f"        {{{latex_escape(p.get('dates', ''))}}}\n"
            "        {\n"
            "            \\begin{cvitems}\n"
            f"{bullets}\n"
            "            \\end{cvitems}\n"
            "        }"
        )

    body = "\n\n".join(chunks)
    tex = (
        "\\cvsection{PROFESSIONAL EXPERIENCE}\n\n"
        "\\begin{cventries}\n\n"
        f"{body}\n\n"
        "\\end{cventries}\n"
    )

    internships = data.get("internships")
    if isinstance(internships, list) and internships:
        ichunks = []
        for p in internships:
            bullets = "\n".join(
                f"                \\item {{{latex_escape(t)}}}" for t in p.get("items", [])
            )
            ichunks.append(
                "    \\cventry\n"
                f"        {{{latex_escape(p.get('title', ''))}}}\n"
                f"        {{{latex_escape(p.get('company', ''))}}}\n"
                f"        {{{latex_escape(p.get('location', ''))}}}\n"
                f"        {{{latex_escape(p.get('dates', ''))}}}\n"
                "        {\n"
                "            \\begin{cvitems}\n"
                f"{bullets}\n"
                "            \\end{cvitems}\n"
                "        }"
            )
        ibody = "\n\n".join(ichunks)
        tex += (
            "\n\\cvsection{INTERNSHIPS}\n\n"
            "\\begin{cventries}\n\n"
            f"{ibody}\n\n"
            "\\end{cventries}\n"
        )

    return tex


def gen_education(data):
    if not data or not isinstance(data.get("schools"), list):
        return None

    chunks = []
    for s in data["schools"]:
        bullets = "\n".join(
            f"        \\item {{{latex_escape(t)}}}" for t in s.get("items", [])
        )
        chunks.append(
            "  \\cventry\n"
            f"    {{{latex_escape(s.get('degree', ''))}}} \n"
            f"    {{{latex_escape(s.get('institution', ''))}}} \n"
            f"    {{{latex_escape(s.get('location', ''))}}} \n"
            f"    {{{latex_escape(s.get('dates', ''))}}} \n"
            "    {\n"
            "      \\begin{cvitems}\n"
            f"{bullets}\n"
            "      \\end{cvitems}\n"
            "    }"
        )

    body = "\n\n".join(chunks)
    return (
        "\\cvsection{EDUCATION}\n\n"
        "\\begin{cventries}\n\n"
        f"{body}\n\n"
        "\\end{cventries}\n"
    )


def gen_projects(data):
    if not data or not isinstance(data.get("projects"), list):
        return None

    chunks = []
    for p in data["projects"]:
        bullets = "\n".join(
            f"        \\item {{{latex_escape(t)}}}" for t in p.get("items", [])
        )
        tech = latex_escape(", ".join(p.get("tech", [])))
        url = p.get("url")
        url_label = p.get("urlLabel") or url or ""
        url_tex = f"\\href{{{url}}}{{{latex_escape(url_label)}}}" if url else ""
        chunks.append(
            "  \\cvproject\n"
            f"    {{{latex_escape(p.get('name', ''))}}}\n"
            f"    {{{latex_escape(p.get('subtitle', ''))}}}\n"
            "    {\n"
            "      \\begin{cvitems}\n"
            f"{bullets}\n"
            "      \\end{cvitems}\n"
            "    }\n"
            f"    {{{tech}}}\n"
            f"    {{{url_tex}}}"
        )

    body = "\n\n".join(chunks)
    return (
        "\\cvsection{PROJECTS}\n\n"
        "\\begin{cventries}\n\n"
        f"{body}\n\n"
        "\\end{cventries}\n"
    )


def gen_skills(data):
    if not data or not isinstance(data.get("skills"), list):
        return None
    rows = "\n".join(
        f"        \\cvskill {{{latex_escape(s.get('category', ''))}}} {{{latex_escape(', '.join(s.get('items', [])))}}}"
        for s in data["skills"]
    )
    return (
        "\\cvsection{SKILLS}\n"
        "    \\begin{cvskills}\n"
        f"{rows}\n"
        "\\end{cvskills}\n"
    )


def gen_languages(data):
    if not data or not isinstance(data.get("languages"), list):
        return None
    rows = "\n\n".join(
        "  \\cvskill\n    {" + latex_escape(item.get("name", "")) + "}\n    {" + latex_escape(item.get("level", "")) + "}"
        for item in data["languages"]
    )
    return (
        "\\cvsection{LANGUAGES}\n\n"
        "\\begin{cvskills}\n\n"
        f"{rows}\n\n"
        "\\end{cvskills}\n"
    )


summary = read_yaml("00-summary.yml")
experience = read_yaml("10-experience.yml")
projects = read_yaml("30-projects.yml")
skills = read_yaml("40-skills.yml")
education = read_yaml("20-education.yml")
languages = read_yaml("50-languages.yml")

outputs = {
    "00-summary.tex": gen_summary(summary),
    "10-experience.tex": gen_experience(experience),
    "20-projects.tex": gen_projects(projects),
    "30-skills.tex": gen_skills(skills),
    "50-education.tex": gen_education(education),
    "60-languages.tex": gen_languages(languages),
}

for filename, content in outputs.items():
    if content:
        write_file(SECTIONS_DIR / filename, content)

sys.exit(0)

