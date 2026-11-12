Desenvolvimento
===============

.. code-block:: bash

   git clone git@github.com:abrasileirado/dsgovbr-sphinx-theme.git
   cd dsgovbr-sphinx-theme
   uv venv && uv pip install -e ".[dev]"
   uv run pytest
   uv run ruff check .
   uv run sphinx-build -W -b html docs docs/_build/html

Versionamento
-------------

A versão do pacote segue ``X.Y.Z.n``: ``X.Y.Z`` é a versão do GOV.BR DS
(``govbr-ds-core``) em que o tema se baseia e ``n`` é a revisão do próprio tema
para aquela versão do DS (começa em ``0``). Exemplo: ``3.7.0.0``, ``3.7.0.1``.
As versões ``0.1.x`` e ``0.2.0`` são anteriores a este esquema.

Estrutura
---------

- ``src/dsgovbr_sphinx_theme/``: templates (``layout.html``, menu e breadcrumb),
  ``theme.toml`` e ``static/`` (CSS, JS e fonte Rawline).
- ``src/dsgovbr_sphinx_theme/componentes.py``: extensão com as diretivas ``br-*``.
- ``src/dsgovbr_sphinx_theme/componentes_static/vendor/``: CSS do
  dsgovbr-bootstrapped e ``bootstrap.bundle.min.js``, copiados sem modificação.

Atualizar os assets do dsgovbr-bootstrapped
-------------------------------------------

Com o dsgovbr-bootstrapped compilado ao lado (``npm run build``):

.. code-block:: bash

   python scripts/atualizar_vendor.py ../dsgovbr_bootstrapped

O script copia ``dist/dsgovbr-bootstrapped.min.css`` e
``vendor/bootstrap/dist/js/bootstrap.bundle.min.js`` e atualiza as versões em
``THIRD_PARTY_NOTICES.md``.

Versão e publicação
-------------------

A versão fica em ``pyproject.toml``. Criar a tag ``vX.Y.Z`` dispara o workflow de
release, que publica no PyPI por *Trusted Publishing*.
