"""Testes de build: o tema e a extensão de componentes geram o HTML esperado."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest
from sphinx.application import Sphinx

from dsgovbr_sphinx_theme import _edit_excluido, _parse_links, _parse_patterns, get_html_theme_path

CONF_BASE = """
project = "Projeto Teste"
html_theme = "dsgovbr_sphinx_theme"
html_theme_options = {{
    "github_url": "https://github.com/org/repo",
    "navigation_links": "Guia|guia, Site|https://exemplo.gov.br",
}}
extensions = [{extensoes}]
"""


def construir(tmp_path: Path, paginas: dict[str, str], extensoes: str = "") -> tuple[Path, str]:
    src = tmp_path / "src"
    src.mkdir()
    (src / "conf.py").write_text(CONF_BASE.format(extensoes=extensoes), encoding="utf-8")
    for nome, conteudo in paginas.items():
        (src / f"{nome}.rst").write_text(textwrap.dedent(conteudo), encoding="utf-8")
    out = tmp_path / "out"
    avisos: list[str] = []

    class Coletor:
        def write(self, texto: str) -> None:
            avisos.append(texto)

        def flush(self) -> None:
            pass

    app = Sphinx(
        str(src),
        str(src),
        str(out),
        str(tmp_path / "doctrees"),
        "html",
        status=None,
        warning=Coletor(),
        freshenv=True,
    )
    app.build()
    # Vários builds no mesmo processo re-registram nós/diretivas do próprio Sphinx.
    linhas = "".join(avisos).splitlines()
    return out, "\n".join(linha for linha in linhas if "already registered" not in linha)


INDEX = """
Início
======

.. toctree::

   guia

.. note:: Um aviso.
"""

GUIA = """
Guia
====

Texto.
"""


def test_caminho_do_tema_tem_theme_toml() -> None:
    assert (Path(get_html_theme_path()) / "theme.toml").is_file()


def test_parse_links() -> None:
    assert _parse_links("A|a, B|https://b") == [("A", "a"), ("B", "https://b")]
    assert _parse_links([("A", "a"), {"title": "B", "url": "b"}]) == [("A", "a"), ("B", "b")]
    assert _parse_links("") == []
    with pytest.raises(ValueError, match="sem destino"):
        _parse_links("Sem destino")


def test_layout_do_tema(tmp_path: Path) -> None:
    out, avisos = construir(tmp_path, {"index": INDEX, "guia": GUIA})
    assert "WARNING" not in avisos, avisos
    html = (out / "guia.html").read_text(encoding="utf-8")
    assert 'class="dsgovbr-header"' in html
    assert 'class="dsgovbr-breadcrumb"' in html
    assert "https://github.com/org/repo/edit/main/docs/guia.rst" in html
    assert 'href="https://exemplo.gov.br"' in html
    assert "Projeto comunitário e não oficial" in html
    assert (out / "_static" / "css" / "dsgovbr-sphinx-theme.css").is_file()
    assert (out / "_static" / "fonts" / "rawline" / "rawline-400.woff2").is_file()
    # sem a extensão, o Bootstrap não é carregado
    assert "bootstrap.bundle.min.js" not in html


COMPONENTES = """
Componentes
===========

.. br-alerta:: success
   :titulo: Ok
   :fechavel:

   Feito.

:br-badge-danger:`Erro` :br-botao:`Ir <https://exemplo.gov.br>`
:br-tooltip:`CPF <Cadastro>`

.. br-acordeao::

   .. br-acordeao-item:: Pergunta
      :aberto:

      Resposta.

.. br-abas::

   .. br-aba:: Um

      Primeiro.

   .. br-aba:: Dois

      Segundo.

.. br-paginacao::
   :atual: 1

   - `1 <#>`__
   - `2 <#>`__

.. br-breadcrumb::

   - `Início <#>`__
   - Atual

.. br-modal:: Título do modal

   Corpo.

.. br-progresso:: 40
"""


EXT = '"dsgovbr_sphinx_theme.componentes"'


def test_componentes(tmp_path: Path) -> None:
    out, avisos = construir(tmp_path, {"index": COMPONENTES}, extensoes=EXT)
    assert "WARNING" not in avisos, avisos
    html = (out / "index.html").read_text(encoding="utf-8")
    assert 'class="alert alert-success alert-dismissible fade show"' in html
    assert 'data-bs-dismiss="alert"' in html
    assert 'class="badge text-bg-danger"' in html
    assert 'class="btn btn-primary" href="https://exemplo.gov.br"' in html
    assert 'data-bs-toggle="tooltip"' in html
    assert 'class="accordion-button"' in html
    assert 'data-bs-parent="#br-acordeao-' in html
    assert 'class="nav-link active"' in html
    assert 'class="tab-pane fade show active"' in html
    assert "page-link" in html and 'aria-current="page"' in html
    assert 'class="breadcrumb-item active"' in html
    assert 'data-bs-toggle="modal"' in html
    assert 'aria-valuenow="40"' in html
    assert "bootstrap.bundle.min.js" in html
    vendor = out / "_static" / "vendor"
    assert (vendor / "dsgovbr-bootstraped" / "dsgovbr-bootstraped.min.css").is_file()


def test_componente_mal_usado_gera_erro(tmp_path: Path) -> None:
    pagina = """
    Erro
    ====

    .. br-abas::

       Texto solto.
    """
    _, avisos = construir(tmp_path, {"index": pagina}, extensoes=EXT)
    assert '"br-abas" aceita apenas diretivas "br-aba"' in avisos


def test_valor_de_progresso_invalido(tmp_path: Path) -> None:
    pagina = """
    Erro
    ====

    .. br-progresso:: 150
    """
    _, avisos = construir(tmp_path, {"index": pagina}, extensoes=EXT)
    assert "entre 0 e 100" in avisos


def test_parse_patterns_e_exclusao() -> None:
    assert _parse_patterns("api/*, gerado") == ["api/*", "gerado"]
    assert _parse_patterns(["api/*"]) == ["api/*"]
    assert _parse_patterns("") == []
    assert _edit_excluido("api/dsgovbr.menus", ["api/*"])
    assert not _edit_excluido("guia", ["api/*"])


def test_edit_on_github_exclude(tmp_path: Path) -> None:
    src = tmp_path / "src"
    (src / "api").mkdir(parents=True)
    conf = (
        'html_theme = "dsgovbr_sphinx_theme"\n'
        'html_theme_options = {"github_url": "https://github.com/org/repo",'
        ' "edit_on_github_exclude": "api/*"}\n'
    )
    (src / "conf.py").write_text(conf, encoding="utf-8")
    index = "Início\n======\n\n.. toctree::\n\n   api/mod\n"
    (src / "index.rst").write_text(index, encoding="utf-8")
    (src / "api" / "mod.rst").write_text("Mod\n===\n", encoding="utf-8")
    out = tmp_path / "out"
    app = Sphinx(str(src), str(src), str(out), str(tmp_path / "dt"), "html", status=None)
    app.build()
    assert "Editar no GitHub" in (out / "index.html").read_text(encoding="utf-8")
    assert "Editar no GitHub" not in (out / "api" / "mod.html").read_text(encoding="utf-8")
