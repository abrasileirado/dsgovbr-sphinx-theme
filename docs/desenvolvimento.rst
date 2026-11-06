Desenvolvimento
===============

.. code-block:: bash

   git clone git@github.com:abrasileirado/dsgovbr-sphinx-theme.git
   cd dsgovbr-sphinx-theme
   uv venv && uv pip install -e ".[dev]"
   uv run pytest
   uv run ruff check .
   uv run sphinx-build -W -b html docs docs/_build/html

Estrutura
---------

- ``src/dsgovbr_sphinx_theme/``: templates (``layout.html``, menu e breadcrumb),
  ``theme.toml`` e ``static/`` (CSS, JS e fonte Rawline).
- ``src/dsgovbr_sphinx_theme/componentes.py``: extensão com as diretivas ``br-*``.
- ``src/dsgovbr_sphinx_theme/componentes_static/vendor/``: CSS do
  dsgovbr-bootstraped e ``bootstrap.bundle.min.js``, copiados sem modificação.

Atualizar os assets do dsgovbr-bootstraped
------------------------------------------

Com o dsgovbr-bootstraped compilado ao lado (``npm run build``):

.. code-block:: bash

   python scripts/atualizar_vendor.py ../dsgovbr_bootstraped

O script copia ``dist/dsgovbr-bootstraped.min.css`` e
``vendor/bootstrap/dist/js/bootstrap.bundle.min.js`` e atualiza as versões em
``THIRD_PARTY_NOTICES.md``.

Versão e publicação
-------------------

A versão fica em ``pyproject.toml``. Criar a tag ``vX.Y.Z`` dispara o workflow de
release, que publica no PyPI por *Trusted Publishing*.
