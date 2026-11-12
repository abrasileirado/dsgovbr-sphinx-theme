# dsgovbr-sphinx-theme

> Projeto comunitário, independente e **não oficial**. Não representa nem implica
> homologação ou endosso pelo GOV.BR DS ou pelo Governo Federal.

Tema [Sphinx](https://www.sphinx-doc.org/) com visual inspirado no Padrão Digital de
Governo ([GOV.BR DS](https://www.gov.br/ds/)): fonte Rawline, tokens de cor do GOV.BR DS,
cabeçalho, menu lateral, breadcrumb, avisos (*message*), tabelas e rodapé no estilo dos
componentes do design system, modo escuro e layout responsivo.

Inclui a extensão opcional `dsgovbr_sphinx_theme.componentes`, com diretivas e roles reST
(`.. br-alerta::`, `.. br-card::`, `.. br-acordeao::`, `:br-badge:`...) para usar nos seus
`.rst` os componentes do [dsgovbr-bootstrapped](https://github.com/abrasileirado/dsgovbr-bootstrapped).

Documentação: <https://abrasileirado.github.io/dsgovbr-sphinx-theme/>

## Uso rápido

```bash
pip install dsgovbr-sphinx-theme
```

```python
# docs/conf.py
html_theme = "dsgovbr_sphinx_theme"
extensions = [
    "sphinx.ext.githubpages",
    "dsgovbr_sphinx_theme.componentes",  # opcional: diretivas br-*
]
html_theme_options = {
    "github_url": "https://github.com/org/repo",
    "navigation_links": "PyPI|https://pypi.org/project/x/",
}
```

```rst
.. br-alerta:: warning
   :titulo: Atenção

   Revise os dados antes de continuar.

.. br-abas::

   .. br-aba:: pip

      ``pip install pacote``

   .. br-aba:: uv

      ``uv add pacote``
```

Opções do tema e a lista completa de componentes estão na documentação.

## Desenvolvimento

```bash
uv venv && uv pip install -e ".[dev]"
uv run pytest
uv run ruff check .
uv run sphinx-build -W -b html docs docs/_build/html
```

## Licença

MIT. Fontes e assets de terceiros: ver [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
