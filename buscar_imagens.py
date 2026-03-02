#!/usr/bin/env python3
"""
Busca a primeira imagem de cada item da lista de presentes no Mercado Livre
e salva em img/produtos/.
"""
import urllib.request
import urllib.parse
import json
import os
import re
import time

OUTDIR = "img/produtos"
os.makedirs(OUTDIR, exist_ok=True)

ITEMS = [
    ("facas-tabua",          "bloco facas tábua bambu cozinha"),
    ("pratos-ceramica",      "jogo pratos cerâmica 6 pessoas fosco"),
    ("talheres-inox",        "jogo talheres inox cabo madeira 24 peças"),
    ("copos-vidro",          "jogo copos vidro canelado 12 unidades"),
    ("mixer-processador",    "mixer processador alimentos 800w"),
    ("potes-hermeticos",     "kit potes herméticos vidro tampa bambu"),
    ("organizador-gaveta",   "organizador gaveta talheres bambu"),
    ("porta-utensilios",     "porta utensílios bambu kit silicone cozinha"),
    ("tacas-verdes",         "taças verdes vidro oliva 6 unidades"),
    ("canecas-verdes",       "canecas verdes cerâmica poá kit 4"),
    ("chaleira-vintage",     "chaleira fogão estilo vintage retrô"),
    ("formas-forno",         "jogo formas forno cerâmica branca 3 peças"),
    ("boleira-cupula",       "boleira cúpula base bambu bolo"),
    ("sousplat-junco",       "sousplat junco natural 6 unidades"),
    ("panos-prato",          "panos de prato algodão kit 6"),
    ("porta-temperos",       "porta temperos giratório bambu frascos vidro"),
    ("jogo-cama-queen",      "jogo cama queen 300 fios percal algodão"),
    ("toalhas-banho",        "jogo toalhas banho verde bege kit 8 peças"),
    ("travesseiros",         "par travesseiros fibra siliconada"),
    ("espelho-decorativo",   "espelho parede decorativo moldura madeira"),
    ("tapete-sala",          "tapete sala pelo curto neutro 2x1.5m"),
    ("organizadores-verde",  "kit organizadores empilháveis verde geladeira"),
    ("geladeira",            "geladeira frost free 2 portas 400L"),
    ("cama-casal",           "cama casal base box colchão espuma"),
    ("cadeira-ergonomica",   "cadeira escritório ergonômica regulável"),
]

def search_ml(query):
    q = urllib.parse.quote(query)
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={q}&limit=3"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    results = data.get("results", [])
    for item in results:
        thumb = item.get("thumbnail", "")
        if thumb:
            # Converte thumbnail para imagem grande full
            # Ex: https://http2.mlstatic.com/D_NQ_NP_XXXXX-MLB...-O.jpg
            # -> https://http2.mlstatic.com/D_Q_NP_XXXXX-MLB...-F.webp
            full = re.sub(r"-[A-Z]\.jpg$", "-F.webp", thumb)
            full = re.sub(r"_NQ_NP_", "_Q_NP_", full)
            return full
    return None

def download(url, dest):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.mercadolivre.com.br/"
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        data = r.read()
    if len(data) < 2000:
        return False
    with open(dest, "wb") as f:
        f.write(data)
    return True

results = {}
for slug, query in ITEMS:
    dest = os.path.join(OUTDIR, f"{slug}.webp")
    print(f"[{slug}] buscando...", end=" ", flush=True)
    try:
        img_url = search_ml(query)
        if not img_url:
            print("NENHUM resultado")
            results[slug] = False
            continue
        ok = download(img_url, dest)
        if ok:
            size = os.path.getsize(dest)
            print(f"OK ({size//1024}KB) <- {img_url}")
            results[slug] = True
        else:
            print(f"FALHA no download ({img_url})")
            results[slug] = False
    except Exception as e:
        print(f"ERRO: {e}")
        results[slug] = False
    time.sleep(0.3)

print("\n=== RESUMO ===")
ok_count = sum(1 for v in results.values() if v)
print(f"{ok_count}/{len(ITEMS)} imagens baixadas com sucesso")
for slug, ok in results.items():
    print(f"  {'✓' if ok else '✗'} {slug}")
