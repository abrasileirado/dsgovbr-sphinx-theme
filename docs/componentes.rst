Componentes (diretivas reST)
============================

A extensão ``dsgovbr_sphinx_theme.componentes`` registra diretivas ``.. br-*::`` e
roles ``:br-*:`` que geram o markup público do Bootstrap 5.3. O CSS do
`dsgovbr-bootstraped <https://abrasileirado.github.io/dsgovbr-bootstraped/>`_
estiliza esse markup no padrão do GOV.BR DS.

.. code-block:: python

   # conf.py
   extensions = ["dsgovbr_sphinx_theme.componentes"]

A extensão publica o CSS do dsgovbr-bootstraped e o ``bootstrap.bundle.min.js``
(comportamento de acordeão, abas, modal...). Funciona com qualquer tema HTML,
mas foi pensada para o ``dsgovbr_sphinx_theme``.

.. note::

   Toda diretiva aceita ``:class:`` para acrescentar classes (ex.: utilitárias do
   Bootstrap). Em saídas que não são HTML (PDF/LaTeX, texto), só o conteúdo textual
   é mantido. O status de cada componente (Estável, Limitado, Não suportado) segue a
   `matriz de compatibilidade do dsgovbr-bootstraped
   <https://abrasileirado.github.io/dsgovbr-bootstraped/requisitos.html>`_.

Alerta
------

``.. br-alerta:: [primary|secondary|success|danger|warning|info|light|dark]`` —
padrão ``info``. Opções: ``:titulo:``, ``:fechavel:``.

.. code-block:: rst

   .. br-alerta:: success
      :titulo: Tudo certo

      Operação concluída com **sucesso**.

.. br-alerta:: success
   :titulo: Tudo certo

   Operação concluída com **sucesso**.

.. br-alerta:: danger
   :fechavel:

   Erro ao processar a solicitação.

Badge e botão (roles)
---------------------

``:br-badge:`` e ``:br-badge-<variante>:``; ``:br-botao:`` e
``:br-botao-<variante>:`` (variantes, ``link`` e ``outline-<variante>``). Com
``Texto <url>`` o botão vira link.

.. code-block:: rst

   :br-badge:`Novo` :br-badge-success:`Estável` :br-badge-warning:`Limitado`

   :br-botao:`Primário` :br-botao-outline-primary:`Secundário`
   :br-botao-link:`Saiba mais <https://www.gov.br/ds/>`

:br-badge:`Novo` :br-badge-success:`Estável` :br-badge-warning:`Limitado`

:br-botao:`Primário` :br-botao-outline-primary:`Secundário`
:br-botao-link:`Saiba mais <https://www.gov.br/ds/>`

Grupo de botões
---------------

``.. br-grupo-botoes::`` — opções ``:rotulo:``, ``:tamanho: sm|lg``, ``:vertical:``.

.. code-block:: rst

   .. br-grupo-botoes::
      :rotulo: Alinhamento

      :br-botao-outline-primary:`Esquerda` :br-botao-outline-primary:`Centro`
      :br-botao-outline-primary:`Direita`

.. br-grupo-botoes::
   :rotulo: Alinhamento

   :br-botao-outline-primary:`Esquerda` :br-botao-outline-primary:`Centro`
   :br-botao-outline-primary:`Direita`

Botão de fechar
---------------

``:br-botao-fechar:`rótulo``` — o texto vira o ``aria-label``:
:br-botao-fechar:`Fechar aviso`

Tooltip e popover
-----------------

.. code-block:: rst

   Passe o mouse em :br-tooltip:`CPF <Cadastro de Pessoas Físicas>` ou clique em
   :br-popover:`gov.br <Conta única de acesso a serviços digitais>`.

Passe o mouse em :br-tooltip:`CPF <Cadastro de Pessoas Físicas>` ou clique em
:br-popover:`gov.br <Conta única de acesso a serviços digitais>`.

Card e grade de cards
---------------------

``.. br-card:: [título]`` — opções ``:subtitulo:``, ``:imagem:``, ``:alt:``,
``:cabecalho:``, ``:rodape:``, ``:link:``, ``:link-texto:``.
``.. br-cards::`` organiza cards em grade (``:colunas:`` de 1 a 6, padrão 3).

.. code-block:: rst

   .. br-cards::
      :colunas: 2

      .. br-card:: Instalação
         :link: instalacao.html
         :link-texto: Instalar

         Instale pelo PyPI e ative no ``conf.py``.

      .. br-card:: Configuração
         :rodape: Atualizado em 2026

         Ajuste cores, logo e links.

.. br-cards::
   :colunas: 2

   .. br-card:: Instalação
      :link: instalacao.html
      :link-texto: Instalar

      Instale pelo PyPI e ative no ``conf.py``.

   .. br-card:: Configuração
      :rodape: Atualizado em 2026

      Ajuste cores, logo e links.

Acordeão
--------

``.. br-acordeao::`` com ``.. br-acordeao-item:: título`` (``:aberto:``). Opções do
acordeão: ``:sempre-aberto:`` (itens independentes) e ``:flush:``.

.. code-block:: rst

   .. br-acordeao::

      .. br-acordeao-item:: O que é o GOV.BR DS?
         :aberto:

         O Padrão Digital de Governo.

      .. br-acordeao-item:: Este tema é oficial?

         Não. É um projeto comunitário.

.. br-acordeao::

   .. br-acordeao-item:: O que é o GOV.BR DS?
      :aberto:

      O Padrão Digital de Governo.

   .. br-acordeao-item:: Este tema é oficial?

      Não. É um projeto comunitário.

Abas
----

``.. br-abas::`` com ``.. br-aba:: título`` (``:ativa:``). Opção ``:estilo:
tabs|pills|underline``.

.. code-block:: rst

   .. br-abas::

      .. br-aba:: pip

         .. code-block:: bash

            pip install dsgovbr-sphinx-theme

      .. br-aba:: uv

         .. code-block:: bash

            uv add dsgovbr-sphinx-theme

.. br-abas::

   .. br-aba:: pip

      .. code-block:: bash

         pip install dsgovbr-sphinx-theme

   .. br-aba:: uv

      .. code-block:: bash

         uv add dsgovbr-sphinx-theme

Recolhível (collapse)
---------------------

``.. br-recolhivel:: texto do botão`` — opções ``:aberto:``, ``:variante:``.

.. br-recolhivel:: Mostrar detalhes

   Conteúdo exibido ao clicar no botão.

Lista (list group)
------------------

``.. br-lista::`` sobre uma lista reST (numerada com ``#.``). Opções ``:flush:`` e
``:ativo: N``.

.. code-block:: rst

   .. br-lista::
      :ativo: 1

      - Primeiro item
      - Segundo item
      - Terceiro item

.. br-lista::
   :ativo: 1

   - Primeiro item
   - Segundo item
   - Terceiro item

Breadcrumb
----------

``.. br-breadcrumb::`` — o último item é a página atual.

.. code-block:: rst

   .. br-breadcrumb::

      - `Início <index.html>`_
      - `Guia <instalacao.html>`_
      - Componentes

.. br-breadcrumb::

   - `Início <index.html>`_
   - `Guia <instalacao.html>`_
   - Componentes

Paginação
---------

``.. br-paginacao::`` — opções ``:atual: N``, ``:tamanho: sm|lg``, ``:rotulo:``.

.. br-paginacao::
   :atual: 2

   - `1 <#>`_
   - `2 <#>`_
   - `3 <#>`_

Dropdown
--------

``.. br-dropdown:: texto do botão`` sobre uma lista de links; opção ``:variante:``.

.. br-dropdown:: Versões
   :variante: outline-primary

   - `Estável <https://pypi.org/project/dsgovbr-sphinx-theme/>`_
   - `Código-fonte <https://github.com/abrasileirado/dsgovbr-sphinx-theme>`_

Navbar
------

``.. br-navbar:: marca`` sobre uma lista de links (demonstrativo dentro da página);
opção ``:link:`` para a marca.

.. br-navbar:: Meu sistema

   - `Início <#>`__
   - `Serviços <#>`__
   - `Contato <#>`__

Modal e offcanvas
-----------------

``.. br-modal:: título`` — opções ``:botao:``, ``:variante:``, ``:tamanho:
sm|lg|xl``, ``:centralizado:``. ``.. br-offcanvas:: título`` — opções ``:botao:``,
``:variante:``, ``:lado: start|end|top|bottom``.

.. code-block:: rst

   .. br-modal:: Confirmação
      :botao: Abrir modal

      Deseja continuar?

.. br-modal:: Confirmação
   :botao: Abrir modal

   Deseja continuar?

.. br-offcanvas:: Filtros
   :botao: Abrir painel lateral
   :variante: outline-primary

   Conteúdo do painel.

Toast
-----

``.. br-toast:: título`` — exibido de forma estática; opção ``:detalhe:``.

.. br-toast:: Notificação
   :detalhe: agora

   Documento salvo.

Progresso, spinner e placeholder
--------------------------------

.. code-block:: rst

   .. br-progresso:: 60
      :mostrar-valor:

   .. br-spinner::
      :variante: primary

   .. br-placeholder::
      :linhas: 3
      :animacao: glow

.. br-progresso:: 60
   :mostrar-valor:

.. br-progresso:: 35
   :variante: success
   :listrado:

.. br-spinner::
   :variante: primary

.. br-placeholder::
   :linhas: 3
   :animacao: glow

Carrossel
---------

``.. br-carrossel::`` com ``.. br-carrossel-item:: imagem`` (``:alt:``; o conteúdo
vira a legenda). Opções ``:indicadores:`` e ``:automatico:``.

.. code-block:: rst

   .. br-carrossel::
      :indicadores:

      .. br-carrossel-item:: _static/slide-1.svg
         :alt: Primeiro slide

         Primeiro slide

      .. br-carrossel-item:: _static/slide-2.svg
         :alt: Segundo slide

.. br-carrossel::
   :indicadores:

   .. br-carrossel-item:: _static/slide-1.svg
      :alt: Primeiro slide

      Primeiro slide

   .. br-carrossel-item:: _static/slide-2.svg
      :alt: Segundo slide

Bloco com classes utilitárias
-----------------------------

``.. br-bloco:: classes`` — ``<div>`` com as classes informadas (helpers e
utilitários do Bootstrap).

.. code-block:: rst

   .. br-bloco:: p-3 mb-3 border rounded bg-body-tertiary

      Caixa com borda e espaçamento.

.. br-bloco:: p-3 mb-3 border rounded bg-body-tertiary

   Caixa com borda e espaçamento.

Fora do escopo
--------------

*Scrollspy* e formulários não têm diretiva: dependem da página inteira ou de
interação que não faz sentido em documentação estática. Para formulários de
exemplo, use ``.. raw:: html`` com as classes do Bootstrap.
