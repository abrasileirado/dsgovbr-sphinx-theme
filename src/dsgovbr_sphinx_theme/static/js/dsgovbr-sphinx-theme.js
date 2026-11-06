/* dsgovbr-sphinx-theme: modo escuro, menu móvel e botão "Copiar" nos blocos de código. */
(function () {
  "use strict";

  var CHAVE_MODO = "dsgovbr-sphinx-modo";
  var raiz = document.documentElement;

  function iniciarModo() {
    var botao = document.querySelector(".dsgovbr-modo");
    if (!botao) {
      return;
    }
    function sincronizar() {
      var escuro = raiz.getAttribute("data-modo") === "escuro";
      botao.setAttribute("aria-pressed", escuro ? "true" : "false");
      botao.setAttribute("aria-label", escuro ? "Ativar modo claro" : "Ativar modo escuro");
    }
    botao.addEventListener("click", function () {
      var escuro = raiz.getAttribute("data-modo") !== "escuro";
      if (escuro) {
        raiz.setAttribute("data-modo", "escuro");
        raiz.setAttribute("data-bs-theme", "dark");
      } else {
        raiz.removeAttribute("data-modo");
        raiz.removeAttribute("data-bs-theme");
      }
      try {
        localStorage.setItem(CHAVE_MODO, escuro ? "escuro" : "claro");
      } catch (e) {
        /* sem localStorage: a escolha vale só para esta página */
      }
      sincronizar();
    });
    sincronizar();
  }

  function iniciarMenu() {
    var menu = document.getElementById("dsgovbr-menu");
    var abrir = document.querySelector(".dsgovbr-menu-toggle");
    var fechar = document.querySelector(".dsgovbr-menu-close");
    var fundo = document.querySelector(".dsgovbr-menu-scrim");
    if (!menu || !abrir) {
      return;
    }
    function definir(aberto) {
      menu.classList.toggle("is-aberto", aberto);
      abrir.setAttribute("aria-expanded", aberto ? "true" : "false");
      if (fundo) {
        fundo.hidden = !aberto;
      }
      if (aberto) {
        var link = menu.querySelector("a, button");
        if (link) {
          link.focus();
        }
      } else {
        abrir.focus();
      }
    }
    abrir.addEventListener("click", function () { definir(true); });
    if (fechar) {
      fechar.addEventListener("click", function () { definir(false); });
    }
    if (fundo) {
      fundo.addEventListener("click", function () { definir(false); });
    }
    document.addEventListener("keydown", function (evento) {
      if (evento.key === "Escape" && menu.classList.contains("is-aberto")) {
        definir(false);
      }
    });
  }

  function iniciarCopiar() {
    if (!navigator.clipboard) {
      return;
    }
    document.querySelectorAll("div.highlight").forEach(function (bloco) {
      var pre = bloco.querySelector("pre");
      if (!pre) {
        return;
      }
      var botao = document.createElement("button");
      botao.type = "button";
      botao.className = "dsgovbr-copy";
      botao.textContent = "Copiar";
      botao.setAttribute("aria-label", "Copiar código");
      botao.addEventListener("click", function () {
        navigator.clipboard.writeText(pre.innerText.replace(/\n$/, "")).then(
          function () { botao.textContent = "Copiado!"; },
          function () { botao.textContent = "Falhou"; }
        ).then(function () {
          setTimeout(function () { botao.textContent = "Copiar"; }, 2000);
        });
      });
      bloco.appendChild(botao);
    });
  }

  /* Tooltips e popovers do Bootstrap são opt-in: só existem com a extensão
     dsgovbr_sphinx_theme.componentes (que carrega o bootstrap.bundle). */
  function iniciarBootstrap() {
    var bs = window.bootstrap;
    if (!bs) {
      return;
    }
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
      bs.Tooltip.getOrCreateInstance(el);
    });
    document.querySelectorAll('[data-bs-toggle="popover"]').forEach(function (el) {
      bs.Popover.getOrCreateInstance(el);
    });
  }

  function iniciar() {
    iniciarModo();
    iniciarMenu();
    iniciarCopiar();
    iniciarBootstrap();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciar);
  } else {
    iniciar();
  }
})();
