Configuração
============

Todas as opções vão em ``html_theme_options`` no ``conf.py``:

.. code-block:: python

   html_theme_options = {
       "project_name": "Meu Projeto",
       "tagline": "Documentação",
       "logo": "logo.svg",              # arquivo em html_static_path
       "github_url": "https://github.com/org/repo",
       "navigation_links": "Início|index, PyPI|https://pypi.org/project/x/",
   }

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Opção
     - Padrão
     - Descrição
   * - ``project_name``
     - ``project``
     - Nome no cabeçalho e no rodapé.
   * - ``tagline``
     - vazio
     - Texto curto ao lado do nome (oculto em telas pequenas).
   * - ``logo``
     - vazio
     - Imagem em ``html_static_path``. Também aceita ``html_logo``.
   * - ``logo_height``
     - ``40px``
     - Altura do logotipo.
   * - ``navigation_links``
     - vazio
     - Links do cabeçalho: ``"Título|destino, Outro|https://..."``. Destinos sem
       ``http`` são nomes de documento (``index``, ``guia/uso``).
   * - ``github_url`` / ``github_repo``
     - vazio
     - Repositório; ``github_repo`` (``org/repo``) é deduzido da URL se omitido.
   * - ``github_version``
     - ``main``
     - Branch usada no link "Editar no GitHub".
   * - ``doc_path``
     - ``docs/``
     - Pasta da documentação dentro do repositório.
   * - ``show_edit_on_github``
     - ``True``
     - Mostra o botão "Editar no GitHub" quando há repositório configurado.
   * - ``primary_color``
     - ``#1351b4``
     - Cor interativa (links, destaques). Mantenha contraste AA.
   * - ``enable_dark_mode``
     - ``True``
     - Botão de modo escuro; respeita ``prefers-color-scheme`` e guarda a escolha.
   * - ``show_disclaimer``
     - ``True``
     - Faixa "projeto não oficial" abaixo do cabeçalho.
   * - ``disclaimer_text``
     - texto padrão
     - Substitui o texto da faixa.
   * - ``footer_text``
     - vazio
     - Parágrafo extra no rodapé.
   * - ``globaltoc_maxdepth``
     - ``3``
     - Profundidade do menu lateral.

.. important::

   O tema é **não oficial**. Não use logotipos ou marcas do Governo Federal sem
   autorização; a faixa de aviso existe para deixar isso claro ao leitor.
