"""Diretivas e roles reStructuredText para os componentes do dsgovbr-bootstraped.

Ative em ``conf.py``::

    extensions = ["dsgovbr_sphinx_theme.componentes"]

Cada diretiva/role gera o markup público do Bootstrap 5.3 (``.alert``, ``.card``,
``.accordion``...), que o CSS do `dsgovbr-bootstraped
<https://github.com/abrasileirado/dsgovbr-bootstraped>`_ estiliza no padrão do
GOV.BR DS. O CSS e o ``bootstrap.bundle`` (JS) são empacotados no tema e só são
carregados quando esta extensão está ativa.

Em construtores que não são HTML (LaTeX, texto, man...), os componentes viram
apenas o conteúdo textual: as tags e o comportamento interativo são omitidos.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any, ClassVar

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.states import Inliner
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective

from . import __version__

PREFIXO = "br-"

VARIANTES = ("primary", "secondary", "success", "danger", "warning", "info", "light", "dark")
VARIANTES_BOTAO = (*VARIANTES, "link", *(f"outline-{v}" for v in VARIANTES))

_ALVO_RE = re.compile(r"^(?P<texto>.+?)\s*<(?P<alvo>[^<>]+)>$", re.DOTALL)


# --------------------------------------------------------------------- nós


class ComponenteBloco(nodes.General, nodes.Element):
    """Elemento HTML em bloco (``<div>``, ``<nav>``, ``<button>``...)."""


class ComponenteInline(nodes.Inline, nodes.TextElement):
    """Elemento HTML em linha (``<span>``, ``<a>``, ``<button>``...)."""


def _eh_componente(no: nodes.Node, classe_css: str) -> bool:
    return isinstance(no, (ComponenteBloco, ComponenteInline)) and classe_css in no["classes"]


def _atributos(node: nodes.Element) -> dict[str, Any]:
    attrs = dict(node.get("br_attrs", {}))
    if "id" in attrs:
        attrs["ids"] = [attrs.pop("id")]
    return attrs


def _visit_html(self: Any, node: nodes.Element) -> None:
    tag = node["br_tag"]
    self.body.append(self.starttag(node, tag, "", **_atributos(node)))


def _depart_html(self: Any, node: nodes.Element) -> None:
    self.body.append(f"</{node['br_tag']}>")


def _ignorar(self: Any, node: nodes.Element) -> None:
    """Outros construtores: só o conteúdo dos filhos é escrito."""


def el(
    tag: str,
    classes: str | Iterable[str] = (),
    *filhos: nodes.Node,
    inline: bool = False,
    **attrs: str,
) -> nodes.Element:
    """Cria um nó de componente.

    Atributos com hífen (``data-bs-toggle``, ``aria-label``) são passados com
    ``_`` no nome: ``data_bs_toggle="collapse"``.
    """
    # Conteúdo só de texto/inline precisa de um nó TextElement: o tradutor HTML do
    # Sphinx exige isso para <a> (reference) fora de parágrafo.
    so_inline = bool(filhos) and all(isinstance(f, (nodes.Inline, nodes.Text)) for f in filhos)
    classe = ComponenteInline if inline or so_inline else ComponenteBloco
    node = classe()
    node["br_tag"] = tag
    node["br_attrs"] = {k.replace("_", "-"): v for k, v in attrs.items()}
    node["classes"] = classes.split() if isinstance(classes, str) else list(classes)
    node.extend(filhos)
    return node


def texto(conteudo: str, tag: str = "span", classes: str = "", **attrs: str) -> nodes.Element:
    return el(tag, classes, nodes.Text(conteudo), inline=True, **attrs)


# ------------------------------------------------------------ validadores


def _escolha(*opcoes: str) -> Callable[[str | None], str]:
    def validar(valor: str | None) -> str:
        return directives.choice(valor, opcoes)

    return validar


def _inteiro(minimo: int, maximo: int) -> Callable[[str | None], int]:
    def validar(valor: str | None) -> int:
        numero = directives.nonnegative_int(valor)
        if not minimo <= numero <= maximo:
            raise ValueError(f"deve estar entre {minimo} e {maximo} (recebido: {numero})")
        return numero

    return validar


# ------------------------------------------------------------ base


class BaseComponente(SphinxDirective):
    """Base comum: opção ``:class:`` e geração de ids únicos por página."""

    has_content = True
    option_spec: ClassVar[dict[str, Callable[[str | None], Any]]] = {
        "class": directives.class_option,
    }

    def novo_id(self, tipo: str) -> str:
        return f"br-{tipo}-{self.env.new_serialno('dsgovbr-componente')}"

    def classes_extra(self) -> list[str]:
        return list(self.options.get("class", []))

    def conteudo(self, destino: nodes.Element) -> nodes.Element:
        self.state.nested_parse(self.content, self.content_offset, destino)
        return destino

    def exigir_conteudo(self) -> None:
        if not self.content:
            raise self.error(f'A diretiva "{self.name}" exige conteúdo.')

    def lista(self, nome_lista: str = "lista") -> nodes.Element:
        """Faz o parse do conteúdo e devolve a única lista (com marcadores ou numerada)."""
        self.exigir_conteudo()
        temp = nodes.container()
        self.conteudo(temp)
        listas = [
            n for n in temp.children if isinstance(n, (nodes.bullet_list, nodes.enumerated_list))
        ]
        if len(listas) != 1 or len(temp.children) != 1:
            raise self.error(
                f'A diretiva "{self.name}" espera como conteúdo apenas uma {nome_lista} '
                '("- item" ou "#. item").'
            )
        return listas[0]

    @staticmethod
    def conteudo_item(item: nodes.list_item) -> list[nodes.Node]:
        """Conteúdo de um item de lista, sem o ``<p>`` quando há um só parágrafo."""
        if len(item.children) == 1 and isinstance(item[0], nodes.paragraph):
            return list(item[0].children)
        return list(item.children)

    @staticmethod
    def links(no: nodes.Node) -> list[nodes.reference]:
        return list(no.findall(nodes.reference))


# ------------------------------------------------------------ alerta


class Alerta(BaseComponente):
    """``.. br-alerta:: [variante]`` — componente *Alert* (``.alert``)."""

    optional_arguments = 1
    option_spec = {
        **BaseComponente.option_spec,
        "titulo": directives.unchanged,
        "fechavel": directives.flag,
    }

    def run(self) -> list[nodes.Node]:
        self.exigir_conteudo()
        variante = directives.choice(self.arguments[0], VARIANTES) if self.arguments else "info"
        classes = ["alert", f"alert-{variante}", *self.classes_extra()]
        fechavel = "fechavel" in self.options
        if fechavel:
            classes += ["alert-dismissible", "fade", "show"]
        alerta = el("div", classes, role="alert")
        if self.options.get("titulo"):
            alerta += texto(self.options["titulo"], "p", "alert-heading fw-semibold mb-1")
        self.conteudo(alerta)
        if fechavel:
            alerta += el(
                "button", "btn-close", type="button", data_bs_dismiss="alert", aria_label="Fechar"
            )
        return [alerta]


# ------------------------------------------------------------ card(s)


class Card(BaseComponente):
    """``.. br-card:: [título]`` — componente *Card* (``.card``)."""

    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        **BaseComponente.option_spec,
        "subtitulo": directives.unchanged,
        "imagem": directives.uri,
        "alt": directives.unchanged,
        "cabecalho": directives.unchanged,
        "rodape": directives.unchanged,
        "link": directives.uri,
        "link-texto": directives.unchanged,
    }

    def run(self) -> list[nodes.Node]:
        card = el("div", ["card", "h-100", *self.classes_extra()])
        if self.options.get("cabecalho"):
            card += texto(self.options["cabecalho"], "div", "card-header")
        if self.options.get("imagem"):
            card += nodes.image(
                uri=self.options["imagem"],
                alt=self.options.get("alt", ""),
                classes=["card-img-top"],
            )
        corpo = el("div", "card-body")
        if self.arguments:
            corpo += texto(self.arguments[0], "h3", "card-title h5")
        if self.options.get("subtitulo"):
            corpo += texto(self.options["subtitulo"], "p", "card-subtitle mb-2 text-body-secondary")
        self.conteudo(corpo)
        if self.options.get("link"):
            corpo += texto(
                self.options.get("link-texto") or "Saiba mais",
                "a",
                "btn btn-primary",
                href=self.options["link"],
            )
        card += corpo
        if self.options.get("rodape"):
            card += texto(self.options["rodape"], "div", "card-footer text-body-secondary")
        return [card]


class Cards(BaseComponente):
    """``.. br-cards::`` — grade responsiva de ``br-card``."""

    option_spec = {**BaseComponente.option_spec, "colunas": _inteiro(1, 6)}

    def run(self) -> list[nodes.Node]:
        self.exigir_conteudo()
        colunas = self.options.get("colunas", 3)
        grade = el(
            "div",
            ["row", "row-cols-1", f"row-cols-md-{colunas}", "g-3", "mb-3", *self.classes_extra()],
        )
        temp = self.conteudo(nodes.container())
        for filho in list(temp.children):
            grade += el("div", "col", filho.deepcopy())
        return [grade]


# ------------------------------------------------------------ acordeão


class Acordeao(BaseComponente):
    """``.. br-acordeao::`` — componente *Accordion*; itens com ``br-acordeao-item``."""

    option_spec = {
        **BaseComponente.option_spec,
        "sempre-aberto": directives.flag,
        "flush": directives.flag,
    }

    def run(self) -> list[nodes.Node]:
        self.exigir_conteudo()
        acordeao_id = self.novo_id("acordeao")
        classes = ["accordion", "mb-3", *self.classes_extra()]
        if "flush" in self.options:
            classes.append("accordion-flush")
        acordeao = el("div", classes, id=acordeao_id)
        temp = self.conteudo(nodes.container())
        for filho in temp.children:
            if not _eh_componente(filho, "accordion-item"):
                raise self.error('"br-acordeao" aceita apenas diretivas "br-acordeao-item".')
            if "sempre-aberto" not in self.options:
                for painel in filho.findall(ComponenteBloco):
                    if _eh_componente(painel, "accordion-collapse"):
                        painel["br_attrs"]["data-bs-parent"] = f"#{acordeao_id}"
            acordeao += filho.deepcopy()
        return [acordeao]


class AcordeaoItem(BaseComponente):
    """``.. br-acordeao-item:: título``."""

    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {**BaseComponente.option_spec, "aberto": directives.flag}

    def run(self) -> list[nodes.Node]:
        aberto = "aberto" in self.options
        painel_id = self.novo_id("acordeao-painel")
        botao = texto(
            self.arguments[0],
            "button",
            "accordion-button" + ("" if aberto else " collapsed"),
            type="button",
            data_bs_toggle="collapse",
            data_bs_target=f"#{painel_id}",
            aria_expanded="true" if aberto else "false",
            aria_controls=painel_id,
        )
        corpo = self.conteudo(el("div", "accordion-body"))
        painel = el(
            "div", "accordion-collapse collapse" + (" show" if aberto else ""), corpo, id=painel_id
        )
        item = el(
            "div",
            ["accordion-item", *self.classes_extra()],
            el("h3", "accordion-header", botao),
            painel,
        )
        return [item]


# ------------------------------------------------------------ abas


class Abas(BaseComponente):
    """``.. br-abas::`` — componente *Navs & tabs*; abas com ``br-aba``."""

    option_spec = {**BaseComponente.option_spec, "estilo": _escolha("tabs", "pills", "underline")}

    def run(self) -> list[nodes.Node]:
        self.exigir_conteudo()
        temp = self.conteudo(nodes.container())
        paineis = list(temp.children)
        if not paineis or not all(_eh_componente(p, "tab-pane") for p in paineis):
            raise self.error('"br-abas" aceita apenas diretivas "br-aba".')
        if not any(p.get("br_ativa") for p in paineis):
            paineis[0]["br_ativa"] = True
        estilo = self.options.get("estilo", "tabs")
        nav = el("ul", f"nav nav-{estilo}", role="tablist")
        conteudo = el("div", "tab-content pt-3")
        for painel in paineis:
            painel = painel.deepcopy()
            ativo = bool(painel.get("br_ativa"))
            painel_id = painel["br_attrs"]["id"]
            botao_id = f"{painel_id}-aba"
            nav += el(
                "li",
                "nav-item",
                texto(
                    painel["br_titulo"],
                    "button",
                    "nav-link" + (" active" if ativo else ""),
                    id=botao_id,
                    type="button",
                    role="tab",
                    data_bs_toggle="tab",
                    data_bs_target=f"#{painel_id}",
                    aria_controls=painel_id,
                    aria_selected="true" if ativo else "false",
                ),
                role="presentation",
            )
            painel["br_attrs"]["aria-labelledby"] = botao_id
            if ativo:
                painel["classes"] += ["show", "active"]
            conteudo += painel
        return [el("div", ["mb-3", *self.classes_extra()], nav, conteudo)]


class Aba(BaseComponente):
    """``.. br-aba:: título``."""

    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {**BaseComponente.option_spec, "ativa": directives.flag}

    def run(self) -> list[nodes.Node]:
        painel = el(
            "div",
            ["tab-pane", "fade", *self.classes_extra()],
            id=self.novo_id("aba"),
            role="tabpanel",
            tabindex="0",
        )
        painel["br_titulo"] = self.arguments[0]
        painel["br_ativa"] = "ativa" in self.options
        return [self.conteudo(painel)]


# ------------------------------------------------------------ collapse


class Recolhivel(BaseComponente):
    """``.. br-recolhivel:: texto do botão`` — componente *Collapse*."""

    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        **BaseComponente.option_spec,
        "aberto": directives.flag,
        "variante": _escolha(*VARIANTES_BOTAO),
    }

    def run(self) -> list[nodes.Node]:
        self.exigir_conteudo()
        aberto = "aberto" in self.options
        alvo = self.novo_id("recolhivel")
        botao = texto(
            self.arguments[0],
            "button",
            f"btn btn-{self.options.get('variante', 'secondary')} mb-2",
            type="button",
            data_bs_toggle="collapse",
            data_bs_target=f"#{alvo}",
            aria_expanded="true" if aberto else "false",
            aria_controls=alvo,
        )
        painel = el("div", "collapse" + (" show" if aberto else ""), id=alvo)
        painel += self.conteudo(el("div", "card card-body"))
        return [el("div", ["mb-3", *self.classes_extra()], el("p", "", botao), painel)]


# ------------------------------------------------------------ progresso / spinner / placeholder


class Progresso(BaseComponente):
    """``.. br-progresso:: valor`` — componente *Progress* (0 a 100)."""

    has_content = False
    required_arguments = 1
    option_spec = {
        **BaseComponente.option_spec,
        "variante": _escolha(*VARIANTES),
        "rotulo": directives.unchanged,
        "mostrar-valor": directives.flag,
        "listrado": directives.flag,
        "animado": directives.flag,
    }

    def run(self) -> list[nodes.Node]:
        try:
            valor = _inteiro(0, 100)(self.arguments[0])
        except ValueError as erro:
            raise self.error(f'"br-progresso": valor {erro}.') from erro
        classes = ["progress-bar"]
        if "variante" in self.options:
            classes.append(f"bg-{self.options['variante']}")
        if "listrado" in self.options or "animado" in self.options:
            classes.append("progress-bar-striped")
        if "animado" in self.options:
            classes.append("progress-bar-animated")
        barra = el("div", classes, style=f"width: {valor}%")
        if "mostrar-valor" in self.options:
            barra += nodes.Text(f"{valor}%")
        rotulo = self.options.get("rotulo") or f"Progresso: {valor}%"
        return [
            el(
                "div",
                ["progress", "mb-3", *self.classes_extra()],
                barra,
                role="progressbar",
                aria_label=rotulo,
                aria_valuenow=str(valor),
                aria_valuemin="0",
                aria_valuemax="100",
            )
        ]


class Spinner(BaseComponente):
    """``.. br-spinner::`` — componente *Spinner*."""

    has_content = False
    option_spec = {
        **BaseComponente.option_spec,
        "tipo": _escolha("border", "grow"),
        "variante": _escolha(*VARIANTES),
        "pequeno": directives.flag,
        "rotulo": directives.unchanged,
    }

    def run(self) -> list[nodes.Node]:
        tipo = self.options.get("tipo", "border")
        classes = [f"spinner-{tipo}", *self.classes_extra()]
        if "variante" in self.options:
            classes.append(f"text-{self.options['variante']}")
        if "pequeno" in self.options:
            classes.append(f"spinner-{tipo}-sm")
        rotulo = texto(self.options.get("rotulo") or "Carregando...", "span", "visually-hidden")
        return [el("div", "mb-3", el("div", classes, rotulo, role="status"))]


class Placeholder(BaseComponente):
    """``.. br-placeholder::`` — componente *Placeholders* (linhas de carregamento)."""

    has_content = False
    option_spec = {
        **BaseComponente.option_spec,
        "linhas": _inteiro(1, 12),
        "animacao": _escolha("glow", "wave"),
    }

    def run(self) -> list[nodes.Node]:
        larguras = (7, 4, 9, 6, 8, 5, 10, 3, 11, 6, 8, 4)
        bloco = el("p", ["mb-3", *self.classes_extra()], aria_hidden="true")
        if "animacao" in self.options:
            bloco["classes"].append(f"placeholder-{self.options['animacao']}")
        for indice in range(self.options.get("linhas", 3)):
            bloco += el("span", f"placeholder col-{larguras[indice]} me-1", inline=True)
        return [bloco]


# ------------------------------------------------------------ listas


class ListaGrupo(BaseComponente):
    """``.. br-lista::`` — componente *List group* a partir de uma lista reST."""

    option_spec = {
        **BaseComponente.option_spec,
        "flush": directives.flag,
        "ativo": directives.positive_int,
    }

    def run(self) -> list[nodes.Node]:
        lista = self.lista()
        lista["classes"] += ["list-group", "mb-3", *self.classes_extra()]
        if isinstance(lista, nodes.enumerated_list):
            lista["classes"].append("list-group-numbered")
        if "flush" in self.options:
            lista["classes"].append("list-group-flush")
        for indice, item in enumerate(lista.children, start=1):
            item["classes"].append("list-group-item")
            if indice == self.options.get("ativo"):
                item["classes"].append("active")
        return [lista]


class Breadcrumb(BaseComponente):
    """``.. br-breadcrumb::`` — componente *Breadcrumb*; o último item é a página atual."""

    def run(self) -> list[nodes.Node]:
        lista = self.lista()
        ol = el("ol", ["breadcrumb", *self.classes_extra()])
        itens = list(lista.children)
        for indice, item in enumerate(itens):
            atual = indice == len(itens) - 1
            li = el(
                "li", "breadcrumb-item" + (" active" if atual else ""), *self.conteudo_item(item)
            )
            if atual:
                li["br_attrs"]["aria-current"] = "page"
            ol += li
        return [el("nav", "", ol, aria_label="breadcrumb")]


class Paginacao(BaseComponente):
    """``.. br-paginacao::`` — componente *Pagination*; cada item é um link."""

    option_spec = {
        **BaseComponente.option_spec,
        "atual": directives.positive_int,
        "tamanho": _escolha("sm", "lg"),
        "rotulo": directives.unchanged,
    }

    def run(self) -> list[nodes.Node]:
        lista = self.lista()
        classes = ["pagination", *self.classes_extra()]
        if "tamanho" in self.options:
            classes.append(f"pagination-{self.options['tamanho']}")
        ul = el("ul", classes)
        for indice, item in enumerate(lista.children, start=1):
            conteudo = self.conteudo_item(item)
            atual = indice == self.options.get("atual")
            refs = [n for n in conteudo if isinstance(n, nodes.reference)]
            for ref in refs:
                ref["classes"].append("page-link")
            if not refs:
                conteudo = [el("span", "page-link", *conteudo, inline=True)]
            li = el("li", "page-item" + (" active" if atual else ""), *conteudo, inline=True)
            if atual:
                li["br_attrs"]["aria-current"] = "page"
            ul += li
        return [el("nav", "", ul, aria_label=self.options.get("rotulo") or "Paginação")]


class Dropdown(BaseComponente):
    """``.. br-dropdown:: texto do botão`` — componente *Dropdown*; itens em lista de links."""

    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {**BaseComponente.option_spec, "variante": _escolha(*VARIANTES_BOTAO)}

    def run(self) -> list[nodes.Node]:
        lista = self.lista("lista de links")
        botao = texto(
            self.arguments[0],
            "button",
            f"btn btn-{self.options.get('variante', 'primary')} dropdown-toggle",
            type="button",
            data_bs_toggle="dropdown",
            aria_expanded="false",
        )
        menu = el("ul", "dropdown-menu")
        for item in lista.children:
            conteudo = self.conteudo_item(item)
            for ref in self.links(item):
                ref["classes"].append("dropdown-item")
            if any(isinstance(n, nodes.reference) for n in conteudo):
                menu += el("li", "", *conteudo)
            else:
                menu += el("li", "", el("span", "dropdown-item-text", *conteudo, inline=True))
        return [el("div", ["dropdown", "mb-3", *self.classes_extra()], botao, menu)]


class Navbar(BaseComponente):
    """``.. br-navbar:: marca`` — componente *Navbar* (demonstrativo, dentro do conteúdo)."""

    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {**BaseComponente.option_spec, "link": directives.uri}

    def run(self) -> list[nodes.Node]:
        lista = self.lista("lista de links")
        alvo = self.novo_id("navbar")
        marca = texto(self.arguments[0], "a", "navbar-brand", href=self.options.get("link", "#"))
        alternar = el(
            "button",
            "navbar-toggler",
            el("span", "navbar-toggler-icon", inline=True),
            type="button",
            data_bs_toggle="collapse",
            data_bs_target=f"#{alvo}",
            aria_controls=alvo,
            aria_expanded="false",
            aria_label="Alternar navegação",
        )
        ul = el("ul", "navbar-nav")
        for item in lista.children:
            for ref in self.links(item):
                ref["classes"].append("nav-link")
            ul += el("li", "nav-item", *self.conteudo_item(item))
        recolhivel = el("div", "collapse navbar-collapse", ul, id=alvo)
        container = el("div", "container-fluid", marca, alternar, recolhivel)
        return [
            el(
                "nav",
                ["navbar", "navbar-expand-lg", "bg-body-tertiary", "mb-3", *self.classes_extra()],
                container,
            )
        ]


# ------------------------------------------------------------ sobreposições


class Modal(BaseComponente):
    """``.. br-modal:: título`` — componente *Modal* com botão para abrir."""

    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        **BaseComponente.option_spec,
        "botao": directives.unchanged,
        "variante": _escolha(*VARIANTES_BOTAO),
        "tamanho": _escolha("sm", "lg", "xl"),
        "centralizado": directives.flag,
    }

    def run(self) -> list[nodes.Node]:
        self.exigir_conteudo()
        modal_id = self.novo_id("modal")
        titulo_id = f"{modal_id}-titulo"
        abrir = texto(
            self.options.get("botao") or self.arguments[0],
            "button",
            f"btn btn-{self.options.get('variante', 'primary')}",
            type="button",
            data_bs_toggle="modal",
            data_bs_target=f"#{modal_id}",
        )
        classes_dialogo = ["modal-dialog"]
        if "tamanho" in self.options:
            classes_dialogo.append(f"modal-{self.options['tamanho']}")
        if "centralizado" in self.options:
            classes_dialogo.append("modal-dialog-centered")
        cabecalho = el(
            "div",
            "modal-header",
            texto(self.arguments[0], "h2", "modal-title fs-5", id=titulo_id),
            el("button", "btn-close", type="button", data_bs_dismiss="modal", aria_label="Fechar"),
        )
        corpo = self.conteudo(el("div", "modal-body"))
        rodape = el(
            "div",
            "modal-footer",
            texto("Fechar", "button", "btn btn-secondary", type="button", data_bs_dismiss="modal"),
        )
        modal = el(
            "div",
            ["modal", "fade", *self.classes_extra()],
            el("div", classes_dialogo, el("div", "modal-content", cabecalho, corpo, rodape)),
            id=modal_id,
            tabindex="-1",
            aria_labelledby=titulo_id,
            aria_hidden="true",
        )
        return [el("p", "", abrir), modal]


class Offcanvas(BaseComponente):
    """``.. br-offcanvas:: título`` — componente *Offcanvas* com botão para abrir."""

    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        **BaseComponente.option_spec,
        "botao": directives.unchanged,
        "variante": _escolha(*VARIANTES_BOTAO),
        "lado": _escolha("start", "end", "top", "bottom"),
    }

    def run(self) -> list[nodes.Node]:
        self.exigir_conteudo()
        painel_id = self.novo_id("offcanvas")
        titulo_id = f"{painel_id}-titulo"
        abrir = texto(
            self.options.get("botao") or self.arguments[0],
            "button",
            f"btn btn-{self.options.get('variante', 'primary')}",
            type="button",
            data_bs_toggle="offcanvas",
            data_bs_target=f"#{painel_id}",
            aria_controls=painel_id,
        )
        cabecalho = el(
            "div",
            "offcanvas-header",
            texto(self.arguments[0], "h2", "offcanvas-title fs-5", id=titulo_id),
            el(
                "button",
                "btn-close",
                type="button",
                data_bs_dismiss="offcanvas",
                aria_label="Fechar",
            ),
        )
        painel = el(
            "div",
            ["offcanvas", f"offcanvas-{self.options.get('lado', 'end')}", *self.classes_extra()],
            cabecalho,
            self.conteudo(el("div", "offcanvas-body")),
            id=painel_id,
            tabindex="-1",
            aria_labelledby=titulo_id,
        )
        return [el("p", "", abrir), painel]


class Toast(BaseComponente):
    """``.. br-toast:: título`` — componente *Toast*, exibido de forma estática."""

    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {**BaseComponente.option_spec, "detalhe": directives.unchanged}

    def run(self) -> list[nodes.Node]:
        self.exigir_conteudo()
        cabecalho = el("div", "toast-header", texto(self.arguments[0], "strong", "me-auto"))
        if self.options.get("detalhe"):
            cabecalho += texto(self.options["detalhe"], "small", "text-body-secondary")
        cabecalho += el(
            "button", "btn-close", type="button", data_bs_dismiss="toast", aria_label="Fechar"
        )
        toast = el(
            "div",
            ["toast", "show", "mb-3", *self.classes_extra()],
            cabecalho,
            self.conteudo(el("div", "toast-body")),
            role="status",
            aria_live="polite",
            aria_atomic="true",
        )
        return [toast]


# ------------------------------------------------------------ carrossel


class Carrossel(BaseComponente):
    """``.. br-carrossel::`` — componente *Carousel*; slides com ``br-carrossel-item``."""

    option_spec = {
        **BaseComponente.option_spec,
        "indicadores": directives.flag,
        "automatico": directives.flag,
    }

    def run(self) -> list[nodes.Node]:
        self.exigir_conteudo()
        carrossel_id = self.novo_id("carrossel")
        temp = self.conteudo(nodes.container())
        slides = list(temp.children)
        if not slides or not all(_eh_componente(s, "carousel-item") for s in slides):
            raise self.error('"br-carrossel" aceita apenas diretivas "br-carrossel-item".')
        attrs: dict[str, str] = {"id": carrossel_id}
        if "automatico" in self.options:
            attrs["data_bs_ride"] = "carousel"
        carrossel = el("div", ["carousel", "slide", "mb-3", *self.classes_extra()], **attrs)
        if "indicadores" in self.options:
            indicadores = el("div", "carousel-indicators")
            for indice in range(len(slides)):
                botao_attrs = {
                    "type": "button",
                    "data_bs_target": f"#{carrossel_id}",
                    "data_bs_slide_to": str(indice),
                    "aria_label": f"Slide {indice + 1}",
                }
                if indice == 0:
                    botao_attrs["aria_current"] = "true"
                indicadores += el("button", "active" if indice == 0 else "", **botao_attrs)
            carrossel += indicadores
        interno = el("div", "carousel-inner")
        for indice, slide in enumerate(slides):
            slide = slide.deepcopy()
            if indice == 0:
                slide["classes"].append("active")
            interno += slide
        carrossel += interno
        for direcao, rotulo in (("prev", "Anterior"), ("next", "Próximo")):
            carrossel += el(
                "button",
                f"carousel-control-{direcao}",
                el("span", f"carousel-control-{direcao}-icon", inline=True, aria_hidden="true"),
                texto(rotulo, "span", "visually-hidden"),
                type="button",
                data_bs_target=f"#{carrossel_id}",
                data_bs_slide=direcao,
            )
        return [carrossel]


class CarrosselItem(BaseComponente):
    """``.. br-carrossel-item:: caminho/da/imagem.png`` — o conteúdo vira a legenda."""

    required_arguments = 1
    option_spec = {**BaseComponente.option_spec, "alt": directives.unchanged}

    def run(self) -> list[nodes.Node]:
        imagem = nodes.image(
            uri=directives.uri(self.arguments[0]),
            alt=self.options.get("alt", ""),
            classes=["d-block", "w-100"],
        )
        slide = el("div", ["carousel-item", *self.classes_extra()], imagem)
        if self.content:
            slide += self.conteudo(el("div", "carousel-caption d-none d-md-block"))
        return [slide]


# ------------------------------------------------------------ agrupadores


class GrupoBotoes(BaseComponente):
    """``.. br-grupo-botoes::`` — componente *Button group*; use os roles ``:br-botao-*:``."""

    option_spec = {
        **BaseComponente.option_spec,
        "rotulo": directives.unchanged,
        "tamanho": _escolha("sm", "lg"),
        "vertical": directives.flag,
    }

    def run(self) -> list[nodes.Node]:
        self.exigir_conteudo()
        temp = self.conteudo(nodes.container())
        filhos: list[nodes.Node] = []
        for filho in temp.children:
            if isinstance(filho, nodes.paragraph):
                filhos += [
                    n for n in filho.children if not (isinstance(n, nodes.Text) and not n.strip())
                ]
            else:
                filhos.append(filho)
        classes = [
            "btn-group-vertical" if "vertical" in self.options else "btn-group",
            *self.classes_extra(),
        ]
        if "tamanho" in self.options:
            classes.append(f"btn-group-{self.options['tamanho']}")
        grupo = el(
            "div",
            classes,
            *filhos,
            role="group",
            aria_label=self.options.get("rotulo") or "Grupo de botões",
        )
        return [el("div", "mb-3", grupo)]


class Bloco(BaseComponente):
    """``.. br-bloco:: classes`` — ``<div>`` com classes utilitárias do Bootstrap."""

    required_arguments = 1
    final_argument_whitespace = True

    def run(self) -> list[nodes.Node]:
        self.exigir_conteudo()
        return [self.conteudo(el("div", [*self.arguments[0].split(), *self.classes_extra()]))]


# --------------------------------------------------------------------- roles


def _separar(texto_role: str) -> tuple[str, str | None]:
    """``"Texto <alvo>"`` -> ("Texto", "alvo"); sem ``<...>`` -> (texto, None)."""
    casamento = _ALVO_RE.match(texto_role.strip())
    if casamento:
        return casamento["texto"].strip(), casamento["alvo"].strip()
    return texto_role.strip(), None


RoleRetorno = tuple[list[nodes.Node], list[nodes.system_message]]


def _role_badge(variante: str) -> Callable[..., RoleRetorno]:
    def role(
        name: str,
        rawtext: str,
        text: str,
        lineno: int,
        inliner: Inliner,
        options: dict[str, Any] | None = None,
        content: list[str] | None = None,
    ) -> RoleRetorno:
        classes = f"badge text-bg-{variante}"
        return [texto(text, "span", classes)], []

    return role


def _role_botao(variante: str) -> Callable[..., RoleRetorno]:
    def role(
        name: str,
        rawtext: str,
        text: str,
        lineno: int,
        inliner: Inliner,
        options: dict[str, Any] | None = None,
        content: list[str] | None = None,
    ) -> RoleRetorno:
        rotulo, alvo = _separar(text)
        classes = f"btn btn-{variante}"
        if alvo:
            return [texto(rotulo, "a", classes, href=alvo, role="button")], []
        return [texto(rotulo, "button", classes, type="button")], []

    return role


def role_tooltip(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: dict[str, Any] | None = None,
    content: list[str] | None = None,
) -> RoleRetorno:
    """``:br-tooltip:`texto <dica>``` — componente *Tooltip*."""
    rotulo, dica = _separar(text)
    if not dica:
        msg = inliner.reporter.error(f'":{name}:" espera "texto <dica>": {text!r}', line=lineno)
        return [inliner.problematic(rawtext, rawtext, msg)], [msg]
    no = texto(
        rotulo,
        "span",
        "text-decoration-underline",
        tabindex="0",
        data_bs_toggle="tooltip",
        data_bs_title=dica,
    )
    return [no], []


def role_popover(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: dict[str, Any] | None = None,
    content: list[str] | None = None,
) -> RoleRetorno:
    """``:br-popover:`texto <conteúdo>``` — componente *Popover*."""
    rotulo, conteudo = _separar(text)
    if not conteudo:
        msg = inliner.reporter.error(f'":{name}:" espera "texto <conteúdo>": {text!r}', line=lineno)
        return [inliner.problematic(rawtext, rawtext, msg)], [msg]
    no = texto(
        rotulo,
        "button",
        "btn btn-link p-0 align-baseline",
        type="button",
        data_bs_toggle="popover",
        data_bs_trigger="focus",
        data_bs_content=conteudo,
    )
    return [no], []


def role_botao_fechar(
    name: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: Inliner,
    options: dict[str, Any] | None = None,
    content: list[str] | None = None,
) -> RoleRetorno:
    """``:br-botao-fechar:`rótulo``` — componente *Close button* (demonstrativo)."""
    return [
        el("button", "btn-close", type="button", aria_label=text.strip() or "Fechar", inline=True)
    ], []


# --------------------------------------------------------------------- registro

DIRETIVAS: dict[str, type[SphinxDirective]] = {
    "alerta": Alerta,
    "card": Card,
    "cards": Cards,
    "acordeao": Acordeao,
    "acordeao-item": AcordeaoItem,
    "abas": Abas,
    "aba": Aba,
    "recolhivel": Recolhivel,
    "progresso": Progresso,
    "spinner": Spinner,
    "placeholder": Placeholder,
    "lista": ListaGrupo,
    "breadcrumb": Breadcrumb,
    "paginacao": Paginacao,
    "dropdown": Dropdown,
    "navbar": Navbar,
    "modal": Modal,
    "offcanvas": Offcanvas,
    "toast": Toast,
    "carrossel": Carrossel,
    "carrossel-item": CarrosselItem,
    "grupo-botoes": GrupoBotoes,
    "bloco": Bloco,
}


def _registrar_roles(app: Sphinx) -> None:
    app.add_role(f"{PREFIXO}badge", _role_badge("primary"))
    app.add_role(f"{PREFIXO}botao", _role_botao("primary"))
    for variante in VARIANTES:
        app.add_role(f"{PREFIXO}badge-{variante}", _role_badge(variante))
    for variante in VARIANTES_BOTAO:
        app.add_role(f"{PREFIXO}botao-{variante}", _role_botao(variante))
    app.add_role(f"{PREFIXO}tooltip", role_tooltip)
    app.add_role(f"{PREFIXO}popover", role_popover)
    app.add_role(f"{PREFIXO}botao-fechar", role_botao_fechar)


STATIC_DIR = Path(__file__).resolve().parent / "componentes_static"


def _adicionar_static(app: Sphinx) -> None:
    """Publica CSS/JS do vendor em ``_static/`` com qualquer tema HTML."""
    caminho = str(STATIC_DIR)
    if caminho not in app.config.html_static_path:
        app.config.html_static_path.insert(0, caminho)


def setup(app: Sphinx) -> dict[str, Any]:
    app.connect("builder-inited", _adicionar_static)
    visitantes_html = (_visit_html, _depart_html)
    outros = (_ignorar, _ignorar)
    for no in (ComponenteBloco, ComponenteInline):
        app.add_node(
            no, html=visitantes_html, latex=outros, text=outros, man=outros, texinfo=outros
        )
    for nome, diretiva in DIRETIVAS.items():
        app.add_directive(f"{PREFIXO}{nome}", diretiva)
    _registrar_roles(app)
    # Antes do CSS do tema (prioridade 200): o tema sobrepõe o reboot do Bootstrap.
    app.add_css_file("vendor/dsgovbr-bootstraped/dsgovbr-bootstraped.min.css", priority=150)
    app.add_js_file(
        "vendor/bootstrap/bootstrap.bundle.min.js", priority=150, loading_method="defer"
    )
    return {"version": __version__, "parallel_read_safe": True, "parallel_write_safe": True}
