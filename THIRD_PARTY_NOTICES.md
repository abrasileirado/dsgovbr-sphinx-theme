# Avisos de terceiros

Este pacote redistribui, sem modificação, os arquivos abaixo.

## Fonte Rawline

- Arquivos: `src/dsgovbr_sphinx_theme/static/fonts/rawline/*.woff2` (pesos 300 a 700).
- Origem: CDN do GOV.BR DS (SERPRO),
  `https://cdngovbr-ds.estaleiro.serpro.gov.br/design-system/fonts/rawline/`,
  mesma cópia usada no site do dsgovbr-bootstraped.
- Licença: **SIL Open Font License 1.1** (`OFL.txt` ao lado das fontes;
  copyright "The Raleway Project Authors"; a Rawline deriva da Raleway).
- Motivo da cópia: o CDN não envia `Access-Control-Allow-Origin`, o que impede
  carregar a fonte com SRI.

## dsgovbr-bootstraped

- Arquivo: `src/dsgovbr_sphinx_theme/componentes_static/vendor/dsgovbr-bootstraped/dsgovbr-bootstraped.min.css`
- Versão: dsgovbr-bootstraped **v0.11.0** (inclui Bootstrap 5.3.8 compilado).
- Origem: <https://github.com/abrasileirado/dsgovbr-bootstraped>
- Licença: MIT (`LICENSE` ao lado do arquivo).

## Bootstrap

- Arquivo: `src/dsgovbr_sphinx_theme/componentes_static/vendor/bootstrap/bootstrap.bundle.min.js`
  (inclui Popper).
- Versão: Bootstrap **v5.3.8**.
- Origem: <https://github.com/twbs/bootstrap>
- Licença: MIT (`LICENSE` ao lado do arquivo).

Os dois últimos só são carregados quando a extensão
`dsgovbr_sphinx_theme.componentes` está ativa. Para atualizá-los, veja
`scripts/atualizar_vendor.py`.

Este projeto é comunitário, independente e não oficial; não representa nem implica
endosso pelo GOV.BR DS, pelo Governo Federal ou pelo projeto Bootstrap.
