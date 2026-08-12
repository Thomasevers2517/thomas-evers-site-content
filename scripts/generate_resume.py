#!/usr/bin/env python3
"""Generate resume.tex from the same JSON files used by thomas-evers.me."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def tex(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "×": r"$\times$",
        "–": "--",
        "—": "---",
    }
    return "".join(replacements.get(char, char) for char in value)


def main() -> None:
    profile = load("profile.json")
    items = load("resume.json")
    skills = load("skills.json")
    research = load("research.json")
    links = {link["label"].lower(): link["href"] for link in profile["links"]}
    email = links.get("email", "").removeprefix("mailto:")

    rows = []
    for item in items:
        details = item.get("details") or [item["description"]]
        bullets = "\n".join(r"\item " + tex(detail) for detail in details)
        rows.append(
            r"\entry{%s}{%s}{%s}{%s}" % (
                tex(item["period"]), tex(item["title"]),
                tex(item["organization"]), bullets,
            )
        )

    skill_rows = "\n".join(
        r"\skill{%s}{%s}" % (tex(skill["title"]), tex(skill["description"]))
        for skill in skills
    )
    research_rows = "\n".join(
        r"\entry{%s}{%s}{Research}{\item %s \item %s}" % (
            tex(item["meta"]), tex(item["title"]),
            tex(item["description"]), tex(item["note"]),
        )
        for item in research
    )

    document = r'''\documentclass[10pt,a4paper]{article}
\usepackage[margin=1.35cm]{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{xcolor}
\usepackage{titlesec}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\definecolor{accent}{HTML}{1E4D73}
\titleformat{\section}{\large\bfseries\color{accent}}{}{0pt}{}[\vspace{-0.45em}\rule{\linewidth}{0.35pt}]
\titlespacing*{\section}{0pt}{0.8em}{0.45em}
\newcommand{\entry}[4]{%
  \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lr}
    \textbf{#2} & \textit{#1}\\
    \textit{#3} &
  \end{tabular*}
  \vspace{-0.7em}
  \begin{itemize}[leftmargin=1.25em,itemsep=0.05em,topsep=0.25em]
    #4
  \end{itemize}
}
\newcommand{\skill}[2]{\textbf{#1}: #2\\[0.2em]}
\begin{document}
\begin{center}
  {\LARGE\bfseries %%NAME%%}\\[0.35em]
  %%EMAIL%% $\cdot$
  \href{%%GITHUB%%}{GitHub} $\cdot$
  \href{%%LINKEDIN%%}{LinkedIn} $\cdot$
  \href{https://thomas-evers.me}{thomas-evers.me}
\end{center}

\vspace{-0.4em}
%%INTRO%%

\section{Research}
%%RESEARCH%%

\section{Education and Experience}
%%ENTRIES%%

\section{Skills}
%%SKILLS%%

\end{document}
'''
    document = (document
        .replace("%%NAME%%", tex(profile["name"]))
        .replace("%%EMAIL%%", tex(email))
        .replace("%%GITHUB%%", links.get("github", ""))
        .replace("%%LINKEDIN%%", links.get("linkedin", ""))
        .replace("%%INTRO%%", tex(profile["introduction"]))
        .replace("%%RESEARCH%%", research_rows)
        .replace("%%ENTRIES%%", "\n".join(rows))
        .replace("%%SKILLS%%", skill_rows))
    (ROOT / "resume.tex").write_text(document, encoding="utf-8")


if __name__ == "__main__":
    main()
