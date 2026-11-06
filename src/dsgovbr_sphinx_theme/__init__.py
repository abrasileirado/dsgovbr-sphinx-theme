"""Tema Sphinx comunitário e não oficial inspirado no Design System GOV.BR (DSGovBR)."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

try:
    __version__ = version("dsgovbr-sphinx-theme")
except PackageNotFoundError:  # pragma: no cover - execução a partir do código-fonte
    __version__ = "0.0.0"

THEME_NAME = "dsgovbr_sphinx_theme"


def get_html_theme_path() -> str:
    """Retorna o diretório do tema (o que contém ``theme.toml``).

    Mantido para quem ainda usa ``html_theme_path``; com o pacote instalado o
    Sphinx encontra o tema pelo *entry point* ``sphinx.html_themes``.
    """
    return str(Path(__file__).resolve().parent)


def _parse_links(raw: Any) -> list[tuple[str, str]]:
    """Converte ``navigation_links`` em pares (título, destino).

    Aceita lista de pares/dicionários ou a string ``"Título|destino, Outro|url"``.
    """
    if not raw:
        return []
    links: list[tuple[str, str]] = []
    if isinstance(raw, str):
        for item in raw.split(","):
            if not item.strip():
                continue
            title, _, target = item.partition("|")
            if not target.strip():
                raise ValueError(
                    f"[{THEME_NAME}] navigation_links: item {item.strip()!r} sem destino; "
                    "use 'Título|destino'."
                )
            links.append((title.strip(), target.strip()))
        return links
    for item in raw:
        if isinstance(item, dict):
            links.append((str(item["title"]), str(item["url"])))
        else:
            title, target = item
            links.append((str(title), str(target)))
    return links


def _html_page_context(
    app: Any, pagename: str, templatename: str, context: dict[str, Any], doctree: Any
) -> None:
    """Expõe ``dsgovbr_navigation_links`` já normalizado para os templates."""
    options = context.get("theme_navigation_links")
    context["dsgovbr_navigation_links"] = _parse_links(options)


def setup(app: Any) -> dict[str, Any]:
    """Registra o tema no Sphinx."""
    app.add_html_theme(THEME_NAME, get_html_theme_path())
    app.connect("html-page-context", _html_page_context)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
