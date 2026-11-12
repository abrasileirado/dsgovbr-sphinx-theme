Instalação
==========

Requisitos: Python 3.10+ e Sphinx 7.3+.

Pelo PyPI:

.. code-block:: bash

   pip install dsgovbr-sphinx-theme

A versão do tema segue ``X.Y.Z.n``: ``X.Y.Z`` é a versão do GOV.BR DS em que ele se
baseia e ``n`` é a revisão do tema (veja :doc:`desenvolvimento`). Para acompanhar
só as revisões de um mesmo DS, fixe ``dsgovbr-sphinx-theme~=3.7.0.0``.

Direto do GitHub (versão fixa por tag):

.. code-block:: bash

   pip install "dsgovbr-sphinx-theme @ git+https://github.com/abrasileirado/dsgovbr-sphinx-theme@v3.7.0.0"

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
