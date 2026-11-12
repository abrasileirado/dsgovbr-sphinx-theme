"""Configuração da documentação do próprio dsgovbr-sphinx-theme."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dsgovbr_sphinx_theme import __version__  # noqa: E402

project = "dsgovbr-sphinx-theme"
author = "Kelson da Costa Medeiros"
copyright = "2026, Abrasileirado"  # noqa: A001
release = __version__
language = "pt_BR"

extensions = [
    "sphinx.ext.githubpages",
    "dsgovbr_sphinx_theme.componentes",
]

root_doc = "index"
exclude_patterns = ["_build"]

html_theme = "dsgovbr_sphinx_theme"
html_title = project
html_static_path = ["_static"]
html_theme_options = {
    "tagline": "Tema Sphinx inspirado no GOV.BR DS",
    "github_url": "https://github.com/abrasileirado/dsgovbr-sphinx-theme",
    "navigation_links": (
        "dsgovbr-bootstrapped|https://abrasileirado.github.io/dsgovbr-bootstrapped/, "
        "PyPI|https://pypi.org/project/dsgovbr-sphinx-theme/"
    ),
}
