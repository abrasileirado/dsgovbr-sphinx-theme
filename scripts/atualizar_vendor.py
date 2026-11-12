"""Copia os assets do dsgovbr-bootstrapped (já compilado) para o pacote do tema.

Uso:
    python scripts/atualizar_vendor.py ../dsgovbr_bootstrapped
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
VENDOR = RAIZ / "src" / "dsgovbr_sphinx_theme" / "componentes_static" / "vendor"
NOTICES = RAIZ / "THIRD_PARTY_NOTICES.md"


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    origem = Path(argv[0]).resolve()
    arquivos = {
        origem / "dist" / "dsgovbr-bootstrapped.min.css": VENDOR / "dsgovbr-bootstrapped",
        origem / "LICENSE": VENDOR / "dsgovbr-bootstrapped",
        origem / "vendor/bootstrap/dist/js/bootstrap.bundle.min.js": VENDOR / "bootstrap",
        origem / "vendor/bootstrap/LICENSE": VENDOR / "bootstrap",
    }
    faltando = [str(a) for a in arquivos if not a.is_file()]
    if faltando:
        print(
            "erro: arquivos não encontrados (rode `npm run build` e "
            "`git submodule update --init` no dsgovbr-bootstrapped):\n  " + "\n  ".join(faltando),
            file=sys.stderr,
        )
        return 1

    for arquivo, destino in arquivos.items():
        destino.mkdir(parents=True, exist_ok=True)
        shutil.copy2(arquivo, destino / arquivo.name)
        print(f"copiado: {arquivo.name} -> {destino.relative_to(RAIZ)}")

    versao_ds = json.loads((origem / "package.json").read_text(encoding="utf-8"))["version"]
    bundle = VENDOR / "bootstrap" / "bootstrap.bundle.min.js"
    cabecalho_bs = bundle.read_text(encoding="utf-8")[:200]
    casamento = re.search(r"Bootstrap v(\d+\.\d+\.\d+)", cabecalho_bs)
    if not casamento:
        print("erro: versão do Bootstrap não encontrada no cabeçalho do bundle", file=sys.stderr)
        return 1
    texto = NOTICES.read_text(encoding="utf-8")
    texto = re.sub(r"(dsgovbr-bootstrapped \*\*v)[\d.]+", rf"\g<1>{versao_ds}", texto)
    texto = re.sub(r"(Bootstrap \*\*v)[\d.]+", rf"\g<1>{casamento[1]}", texto)
    NOTICES.write_text(texto, encoding="utf-8")
    print(f"THIRD_PARTY_NOTICES.md: dsgovbr-bootstrapped v{versao_ds}, Bootstrap v{casamento[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
