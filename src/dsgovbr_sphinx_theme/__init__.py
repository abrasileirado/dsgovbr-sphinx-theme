"""Tema Sphinx comunitário e não oficial inspirado no Design System GOV.BR (DSGovBR)."""

from __future__ import annotations

from fnmatch import fnmatchcase
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


def _parse_patterns(raw: Any) -> list[str]:
    """Normaliza ``edit_on_github_exclude``: string separada por vírgula ou lista."""
    if not raw:
        return []
    itens = raw.split(",") if isinstance(raw, str) else raw
    return [str(item).strip() for item in itens if str(item).strip()]


def _edit_excluido(pagename: str, padroes: list[str]) -> bool:
    """True se a página casa com algum padrão glob (ex.: ``api/*``)."""
    return any(fnmatchcase(pagename, padrao) for padrao in padroes)


def _html_page_context(
    app: Any, pagename: str, templatename: str, context: dict[str, Any], doctree: Any
) -> None:
    """Expõe ``dsgovbr_navigation_links`` e ``dsgovbr_edit_excluido`` para os templates."""
    options = context.get("theme_navigation_links")
    context["dsgovbr_navigation_links"] = _parse_links(options)
    padroes = _parse_patterns(context.get("theme_edit_on_github_exclude"))
    context["dsgovbr_edit_excluido"] = _edit_excluido(pagename, padroes)


def setup(app: Any) -> dict[str, Any]:
    """Registra o tema no Sphinx."""
    app.add_html_theme(THEME_NAME, get_html_theme_path())
    app.connect("html-page-context", _html_page_context)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
