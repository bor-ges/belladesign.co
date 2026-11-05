#!/usr/bin/env python3
"""
Baixa a imagem de capa (og:image) de cada projeto do Behance e salva em img/covers/<id>.<ext>.
Rode no SEU computador, na pasta do site:

    python3 fetch-covers.py

Requer apenas Python 3 (sem instalar nada). Se o Behance bloquear algum projeto,
o script avisa e você salva a capa manualmente (botão direito > Salvar imagem)
com o nome indicado, por exemplo img/covers/zago.jpg. A página reconhece
jpg, png, webp e jpeg automaticamente.
"""
import os
import re
import sys
import urllib.request

PROJECTS = {
    "zago": "https://www.behance.net/gallery/178060809/Restaurante-Zago-Sushi",
    "revista": "https://www.behance.net/gallery/200900381/Revista-Fabio-Palacio-Pr-Candidato-a-Prefeito-SCS",
    "rayane": "https://www.behance.net/gallery/211009413/Vereadora-Rayane-Braga-Eleicoes-Municipais-2024",
    "rpg": "https://www.behance.net/gallery/212211577/RPG-UMA-AVENTURA-NA-BIOLOGIA-Livro-do-Jogador",
    "prata": "https://www.behance.net/gallery/221808221/Prata-Digital-Bank",
    "guara": "https://www.behance.net/gallery/225782847/Projeto-Prefeitura-Guaratingueta",
    "solaris": "https://www.behance.net/gallery/231946441/Identidade-Visual-Solaris-Esttica",
    "sonhar": "https://www.behance.net/gallery/234122895/Branding-Espaco-Sonhar-Fono-e-Psicologia-Infantil",
    "netinho": "https://www.behance.net/gallery/254953601/Campanha-2026-Deputado-Federal-Netinho-de-Paula",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}
EXT = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "covers")


def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=30)


def find_cover(html):
    for pattern in (
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
    ):
        m = re.search(pattern, html, re.I)
        if m:
            return m.group(1).replace("&amp;", "&")
    return None


def main():
    os.makedirs(OUT, exist_ok=True)
    falhas = []
    for pid, url in PROJECTS.items():
        try:
            html = get(url).read().decode("utf-8", "ignore")
            img = find_cover(html)
            if not img:
                raise RuntimeError("capa (og:image) não encontrada na página")
            resp = get(img)
            ext = EXT.get(resp.headers.get_content_type(), "jpg")
            dest = os.path.join(OUT, f"{pid}.{ext}")
            with open(dest, "wb") as f:
                f.write(resp.read())
            print(f"ok     {pid:8} -> img/covers/{pid}.{ext}")
        except Exception as e:  # noqa: BLE001
            falhas.append(pid)
            print(f"falhou {pid:8} ({e}). Salve manualmente em img/covers/{pid}.jpg")
    if falhas:
        print("\nProjetos para salvar manualmente:", ", ".join(falhas))
        sys.exit(1)
    print("\nPronto. Abra o index.html e confira as capas.")


if __name__ == "__main__":
    main()
