# Thomas Evers — website and résumé

This is the single source of truth for [thomas-evers.me](https://thomas-evers.me) and the PDF résumé.

## Edit your content

Use GitHub's pencil button to edit one of these files and commit the change:

- [`about.md`](about.md) — About me
- [`profile.json`](profile.json) — name, introduction, links, and PDF link
- [`resume.json`](resume.json) — education and experience
- [`skills.json`](skills.json) — skills
- [`research.json`](research.json) — papers and research

Website changes appear after a refresh, usually within a minute. Changes to résumé, profile, skills, or research data also trigger GitHub Actions, which regenerates `resume.tex`, builds `resume.pdf`, and publishes it as the repository's latest release.

## PDF and LaTeX

- [Download the latest generated PDF](https://github.com/Thomasevers2517/thomas-evers-site-content/releases/latest/download/resume.pdf)
- [`resume.tex`](resume.tex) is generated; do not edit it directly.
- [`scripts/generate_resume.py`](scripts/generate_resume.py) controls the LaTeX layout.
- [Build history](../../actions/workflows/build-resume.yml)

JSON punctuation matters. Edit the text between quotes and keep the surrounding quotes, commas, brackets, and braces.
