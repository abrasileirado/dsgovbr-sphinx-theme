Instalação
==========

Requisitos: Python 3.10+ e Sphinx 7.3+.

Pelo PyPI:

.. code-block:: bash

   pip install dsgovbr-sphinx-theme

Direto do GitHub (versão fixa por tag):

.. code-block:: bash

   pip install "dsgovbr-sphinx-theme @ git+https://github.com/abrasileirado/dsgovbr-sphinx-theme@v0.2.0"

No ``docs/conf.py`` do seu projeto:

.. code-block:: python

   html_theme = "dsgovbr_sphinx_theme"

O Sphinx encontra o tema pelo *entry point* ``sphinx.html_themes``; não é preciso
``html_theme_path`` nem listar o tema em ``extensions``.

Para usar também os componentes do dsgovbr-bootstrapped (veja :doc:`componentes`):

.. code-block:: python

   extensions = ["dsgovbr_sphinx_theme.componentes"]

Publicação no GitHub Pages
--------------------------

Inclua ``sphinx.ext.githubpages`` em ``extensions`` para gerar o ``.nojekyll``
(sem ele, o Pages ignora a pasta ``_static/``). Exemplo de workflow:

.. code-block:: yaml

   - run: pip install -r docs/requirements.txt
   - run: sphinx-build -W -b html docs docs/_build/html
   - uses: actions/upload-pages-artifact@v5
     with:
       path: docs/_build/html
