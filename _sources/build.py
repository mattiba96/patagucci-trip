import re

DIR = "/Users/mattiabacileri/Library/Mobile Documents/com~apple~CloudDocs/progetti/patagucci trip /"
SRC_DIR = DIR + "_sources/"

import json

DESTS = [
    {"file": "islanda-trip.html", "suf": "is", "flag": "🇮🇸", "name": "Islanda", "stato": "confermato"},
    {"file": "corea-trip.html", "suf": "kr", "flag": "🇰🇷🇹🇼🇭🇰", "name": "Corea, Taiwan e Hong Kong", "stato": "confermato"},
    # Non e' una meta: e' la pagina che le cerca. Sta in fondo al selettore.
    {"file": "prossimo.html", "suf": "nx", "flag": "❓", "name": "Quale sarà il prossimo?", "stato": "idea"},
]

def extract(tag, content):
    pattern = r'<' + tag + r'(?:\s[^>]*)?>.*?</' + tag + r'>'
    m = re.search(pattern, content, re.DOTALL)
    if not m:
        raise Exception(f"Could not find <{tag}> block")
    return m.group(0)


# ----------------------------------------------------------------------
# Il contesto della chat.
#
# "Chiedi ai Patagucci" (api/chat.js) risponde solo con quello che sul
# sito c'e' scritto davvero. Il testo glielo passiamo da qui, generato
# insieme a index.html: se la pagina cambia, cambia anche cio' che la
# chat sa, senza doversene ricordare.
# ----------------------------------------------------------------------

def testo_da_html(html):
    """Il testo che un lettore vedrebbe, senza markup."""
    for tag in ("script", "style", "svg"):
        html = re.sub(r"<" + tag + r"\b.*?</" + tag + r">", " ", html, flags=re.S | re.I)
    html = re.sub(r"<[^>]+>", "\n", html)
    html = html.replace("&nbsp;", " ").replace("&amp;", "&").replace("&egrave;", "è")
    html = re.sub(r"[ \t]+", " ", html)
    righe, pulite = [l.strip() for l in html.split("\n")], []
    for r in righe:
        # Il marosello di foto in home duplica ogni voce per scorrere
        # all'infinito: la seconda copia non aggiunge niente.
        if r and r not in pulite[-40:]:
            pulite.append(r)
    return "\n".join(pulite)


def dati_da_script(js):
    """Le tabelle della pagina (itinerario, tappe, budget) vivono in JS.

    Senza queste la chat non saprebbe dire cosa si fa il quarto giorno:
    in HTML quelle tabelle sono vuote e vengono riempite dallo script.
    Prendo le sole dichiarazioni di dati, saltando le liste di sole
    coordinate — al modello non dicono nulla e pesano.
    """
    fuori = []
    for m in re.finditer(r"^\s*(?:const|var|let)\s+([A-Za-z_$][\w$]*)\s*=\s*([\[{])", js, re.M):
        i = m.end() - 1
        apri, chiudi = js[i], "]" if js[i] == "[" else "}"
        profondita, j, stringa = 0, i, None
        while j < len(js):
            c = js[j]
            if stringa:
                if c == "\\":
                    j += 2
                    continue
                if c == stringa:
                    stringa = None
            elif c in "\"'`":
                stringa = c
            elif c == apri:
                profondita += 1
            elif c == chiudi:
                profondita -= 1
                if profondita == 0:
                    break
            j += 1
        blocco = js[i:j + 1]
        if len(blocco) < 80:
            continue
        if sum(c.isalpha() for c in blocco) / len(blocco) < 0.35:
            continue
        fuori.append(f"{m.group(1)} = {blocco}")
    return "\n\n".join(fuori)


contesti = {}

blocks = []
scripts = []

for d in DESTS:
    path = SRC_DIR + d["file"]
    with open(path, encoding="utf-8") as f:
        content = f.read()

    ids = sorted(set(re.findall(r'id="([a-zA-Z0-9_-]+)"', content)))
    suf = d["suf"]

    for _id in ids:
        new_id = f"{_id}-{suf}"
        content = content.replace(f'id="{_id}"', f'id="{new_id}"')
        content = content.replace(f"href=\"#{_id}\"", f"href=\"#{new_id}\"")
        content = content.replace(f"getElementById('{_id}')", f"getElementById('{new_id}')")
        content = content.replace(f'getElementById("{_id}")', f'getElementById("{new_id}")')
        content = content.replace(f"querySelector('#{_id} ", f"querySelector('#{new_id} ")
        content = content.replace(f"querySelector('#{_id}')", f"querySelector('#{new_id}')")

    hero = extract("header", content)
    nav = extract("nav", content)
    main = extract("main", content)
    footer = extract("footer", content)
    script_m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    script_body = script_m.group(1)

    dati = dati_da_script("".join(re.findall(r"<script>(.*?)</script>", content, re.S)))
    contesti[d["suf"]] = (
        f"# {d['flag']} {d['name']} — stato: {d['stato']}\n\n"
        + testo_da_html(hero + main)
        + (f"\n\n## Dati della pagina (itinerario, tappe, tratte, budget)\n\n{dati}" if dati else "")
    )

    nav = nav.replace(
        '<a href="index.html" class="home-link">🌍 Tutte le mete</a>',
        '<a href="javascript:void(0)" class="home-link" onclick="showHub()">🌍 Tutte le mete</a>'
    )
    footer = re.sub(
        r'<a href="index\.html" class="home-link">[^<]*</a>',
        '<a href="javascript:void(0)" class="home-link" onclick="showHub()">Patagucci Trips</a>',
        footer
    )

    block = f'''  <div class="destination" id="dest-{suf}" data-dest="{suf}">
{hero}

{nav}

{main}

{footer}
  </div>'''

    blocks.append({"suf": suf, "flag": d["flag"], "name": d["name"], "block": block})
    scripts.append(f"<script>\n// ---- {d['name']} ----\n{script_body}\n</script>")

hub_html = '''  <div class="destination active" id="dest-hub" data-dest="hub">
    <header class="hero" style="min-height:64vh;">
      <div class="bg" style="background-image:linear-gradient(180deg, rgba(10,14,11,0.35) 0%, rgba(10,14,11,0.6) 55%, rgba(10,14,11,0.94) 100%), url('foto/destinazioni/A_land_enclosed_in_Mountains_-_Hunza_Valley.jpg'); background-position:center 55%;"></div>
      <div class="content">
        <h1>Patagucci Trips</h1>
        <p class="tagline">Machu Picchu, il Salar de Uyuni, Rio — lo stesso gruppo, una meta nuova ogni volta. Qui dentro ci sono i viaggi con le date fissate, con lo stesso livello di dettaglio ossessivo.</p>
        <div class="scroll-cue">↓ scegli la meta</div>
      </div>
    </header>

    <main>
      <section class="panel dark" data-nav>
        <div class="inner">
          <h2 class="section-title reveal">🔥 I Patagucci</h2>
          <p class="section-sub reveal">Machu Picchu, il Salar de Uyuni, Rio — e ora l'aurora islandese e i ciliegi coreani. Lo stesso gruppo, una meta nuova ogni volta.</p>
          <div class="crew-grid">
            <div class="crew-card reveal" data-audio="assets/audio/manu.mp3">
              <img src="foto/32909e5a-8870-4ba2-961d-8baf5bc0c7c8.jpeg" alt="Manu, il logistico, compra le maglie" loading="lazy">
              <div class="crew-caption">Manu — il logistico</div>
            </div>
            <div class="crew-card reveal" data-audio="assets/audio/kiki.mp3">
              <img src="foto/843b0e80-020f-46ed-a7f6-561fc189847a.jpeg" alt="Kiki, la meteora pazza" loading="lazy">
              <div class="crew-caption">Kiki — la meteora pazza <span class="crew-check">✔</span></div>
            </div>
            <div class="crew-card reveal" data-audio="assets/audio/mala.mp3">
              <img src="foto/bea8bd31-b2fc-4c45-9557-03044f26a57d.jpeg" alt="Mala, l'enciclopedia vivente, al vulcano Batur" loading="lazy">
              <div class="crew-caption">Mala — l'enciclopedia vivente <span class="crew-check">✔</span></div>
            </div>
            <div class="crew-card reveal" data-audio="assets/audio/bacci.mp3">
              <img src="foto/5624176e-4c77-4989-9af3-245a53408b1d.jpeg" alt="Bacci, il tecnologico" loading="lazy">
              <div class="crew-caption">Bacci — il tecnologico</div>
            </div>
          </div>

          <div class="card reveal" style="margin-top:18px; text-align:center; font-style:italic;">
            <h3 style="margin-top:0; font-style:normal;">📜 I Patagucci</h3>
            <p style="color:#c7c2b6; font-size:0.88rem; line-height:1.7; margin:0; max-width:640px; margin-left:auto; margin-right:auto;">
              Quattro amici, uno zaino e un biglietto di sola andata, ogni volta una meta nuova, ogni volta la stessa combriccola scatenata. Manu è il logistico, con lui il viaggio non si perde mai un colpo, ma senza dieci birre al giorno lo vedi diventare uno sconvolto. Kiki è la meteora pazza, sempre pronta a ripartire, ma toglietele il ceviche e la sentirete ruggire: diventa aggressiva, non capisce più niente, datele pesce crudo o scappate immediatamente. Mala è l'enciclopedia vivente del gruppo intero, sa tutto di ogni posto, storia e sentiero, ma se non prende la bumba prima di coricarsi la notte è tutta un rimbombo, meglio non disturbarsi. Bacci è il tecnologico, con lui non ti perdi in un vicolo, ma portatelo in quota e guardate che spettacolo: trema come una foglia al primo metro guadagnato, e giuro che una volta se l'è quasi fatta sotto, poveraccio. Quattro caratteri diversi, un'unica squadra che parte, i Patagucci vanno per il mondo, sempre dalla stessa parte — e ovunque li porti il prossimo volo o il prossimo passo, tornano a casa con una storia in più da raccontare, senza sosta.
            </p>
          </div>

          <h3 style="color:#fff; margin:32px 0 4px;">📸 Insieme in giro per il mondo</h3>
          <div class="group-marquee reveal">
            <div class="group-marquee-track">
              <div class="group-marquee-item">
                <img src="foto/dd148649-09ef-45bd-8b5e-313dff562db8.jpeg" alt="Il gruppo al completo a Machu Picchu, Perù" loading="lazy">
                <div class="crew-caption">Machu Picchu, Perù</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_1590.JPG" alt="Il gruppo sui binari nel deserto di sale, Bolivia/Cile" loading="lazy">
                <div class="crew-caption">Deserto di sale, Bolivia/Cile</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_7193.JPG" alt="Il gruppo sui binari del treno, Salar de Uyuni, Bolivia" loading="lazy">
                <div class="crew-caption">Salar de Uyuni, Bolivia</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/group-geyser-bolivia.jpeg" alt="Il gruppo tra i fumi dei geyser, Bolivia" loading="lazy">
                <div class="crew-caption">Geyser Sol de Mañana, Bolivia</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/group-altopiano-boliviano.jpeg" alt="Pranzo di gruppo con vista sulla laguna, altopiano boliviano" loading="lazy">
                <div class="crew-caption">Altopiano boliviano</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/group-cusco-peru.jpeg" alt="Il gruppo di notte tra i vicoli di Cusco, Perù" loading="lazy">
                <div class="crew-caption">Cusco, Perù</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_6840.JPG" alt="Al mercato locale, Perù" loading="lazy">
                <div class="crew-caption">Mercato locale, Perù</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/group-van-bolivia.jpeg" alt="In viaggio sul van tra un trasferimento e l'altro, Bolivia" loading="lazy">
                <div class="crew-caption">In viaggio, Bolivia</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/group-notte-ande.jpeg" alt="Il gruppo di notte tra le nuvole, Ande" loading="lazy">
                <div class="crew-caption">Notte in quota, Ande</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_0283.jpeg" alt="Selfie di gruppo sul bus notturno" loading="lazy">
                <div class="crew-caption">Notte in bus, on the road</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_0300.JPG" alt="Sul relitto di un treno al cimitero dei treni di Uyuni, Bolivia" loading="lazy">
                <div class="crew-caption">Cimitero dei treni, Uyuni, Bolivia</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_0343.jpeg" alt="Il gruppo davanti al fuoristrada sul Salar de Uyuni, Bolivia" loading="lazy">
                <div class="crew-caption">Il fuoristrada sul Salar de Uyuni, Bolivia</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_0420.jpeg" alt="Effetto prospettiva con il cappello, Salar de Uyuni" loading="lazy">
                <div class="crew-caption">Giochi di prospettiva, Salar de Uyuni</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_0422.jpeg" alt="Altro effetto prospettiva, Salar de Uyuni" loading="lazy">
                <div class="crew-caption">Ancora prospettiva, Salar de Uyuni</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_0589.jpeg" alt="Il gruppo davanti a una laguna colorata, altopiano boliviano" loading="lazy">
                <div class="crew-caption">Lagune colorate dell'altopiano, Bolivia</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_0683.jpeg" alt="Shopping di souvenir a San Pedro de Atacama, Cile" loading="lazy">
                <div class="crew-caption">Shopping a San Pedro de Atacama, Cile</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_0821.jpeg" alt="Trekking in alta quota tra le montagne, Perù" loading="lazy">
                <div class="crew-caption">Trekking in alta quota, Perù</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_1169.jpeg" alt="Cena di gruppo in un ristorante, Lima, Perù" loading="lazy">
                <div class="crew-caption">Cena gourmet, Lima, Perù</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_2748.JPG" alt="Tra le guglie di roccia della Valle de las Ánimas, La Paz, Bolivia" loading="lazy">
                <div class="crew-caption">Valle de las Ánimas, La Paz, Bolivia</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_3185.JPG" alt="Tramonto accanto al fuoristrada, Salar de Uyuni, Bolivia" loading="lazy">
                <div class="crew-caption">Tramonto sul Salar de Uyuni, Bolivia</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_3759.JPG" alt="Una sera tra amici al ristorante" loading="lazy">
                <div class="crew-caption">Una sera tra amici</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_3979.JPG" alt="Pausa fast food in centro commerciale, Cile" loading="lazy">
                <div class="crew-caption">Pausa fast food, Cile</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_4070.JPG" alt="All'ingresso del Santuario Storico di Machu Picchu, Perù" loading="lazy">
                <div class="crew-caption">Ingresso a Machu Picchu, Perù</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_4089.JPG" alt="Lungo la ferrovia verso Aguas Calientes, Perù" loading="lazy">
                <div class="crew-caption">Lungo i binari di Aguas Calientes, Perù</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_4173.JPG" alt="Il gruppo con la vista classica su Machu Picchu, Perù" loading="lazy">
                <div class="crew-caption">Machu Picchu, la vista classica</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_4746.JPG" alt="Il gruppo alle terrazze saline di Maras, Perù" loading="lazy">
                <div class="crew-caption">Salinas de Maras, Perù</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_4786.JPG" alt="Pausa pranzo in un centro commerciale" loading="lazy">
                <div class="crew-caption">Pausa pranzo in centro commerciale</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_6903.JPG" alt="In viaggio in auto con un cane a bordo" loading="lazy">
                <div class="crew-caption">In viaggio con il cane</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_6970.JPG" alt="Una serata di gruppo a un evento" loading="lazy">
                <div class="crew-caption">Serata a un evento</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/IMG_7186.JPG" alt="Verso la ferrovia del Salar de Uyuni, Bolivia" loading="lazy">
                <div class="crew-caption">Ferrovia di Uyuni, Bolivia</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/group-barbiere.jpeg" alt="Dal barbiere durante il viaggio" loading="lazy">
                <div class="crew-caption">Un taglio di capelli</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/group-notte-strada.jpeg" alt="Passeggiata notturna vicino a un distributore" loading="lazy">
                <div class="crew-caption">Passeggiata notturna, on the road</div>
              </div>
              <div class="group-marquee-item">
                <img src="foto/group-relax-maschere.jpeg" alt="Relax con maschera viso dopo il trekking" loading="lazy">
                <div class="crew-caption">Relax dopo il trek</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/dd148649-09ef-45bd-8b5e-313dff562db8.jpeg" alt="" loading="lazy">
                <div class="crew-caption">Machu Picchu, Perù</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_1590.JPG" alt="" loading="lazy">
                <div class="crew-caption">Deserto di sale, Bolivia/Cile</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_7193.JPG" alt="" loading="lazy">
                <div class="crew-caption">Salar de Uyuni, Bolivia</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/group-geyser-bolivia.jpeg" alt="" loading="lazy">
                <div class="crew-caption">Geyser Sol de Mañana, Bolivia</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/group-altopiano-boliviano.jpeg" alt="" loading="lazy">
                <div class="crew-caption">Altopiano boliviano</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/group-cusco-peru.jpeg" alt="" loading="lazy">
                <div class="crew-caption">Cusco, Perù</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_6840.JPG" alt="" loading="lazy">
                <div class="crew-caption">Mercato locale, Perù</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/group-van-bolivia.jpeg" alt="" loading="lazy">
                <div class="crew-caption">In viaggio, Bolivia</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/group-notte-ande.jpeg" alt="" loading="lazy">
                <div class="crew-caption">Notte in quota, Ande</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_0283.jpeg" alt="" loading="lazy">
                <div class="crew-caption">Notte in bus, on the road</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_0300.JPG" alt="" loading="lazy">
                <div class="crew-caption">Cimitero dei treni, Uyuni, Bolivia</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_0343.jpeg" alt="" loading="lazy">
                <div class="crew-caption">Il fuoristrada sul Salar de Uyuni, Bolivia</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_0420.jpeg" alt="" loading="lazy">
                <div class="crew-caption">Giochi di prospettiva, Salar de Uyuni</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_0422.jpeg" alt="" loading="lazy">
                <div class="crew-caption">Ancora prospettiva, Salar de Uyuni</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_0589.jpeg" alt="" loading="lazy">
                <div class="crew-caption">Lagune colorate dell'altopiano, Bolivia</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_0683.jpeg" alt="" loading="lazy">
                <div class="crew-caption">Shopping a San Pedro de Atacama, Cile</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_0821.jpeg" alt="" loading="lazy">
                <div class="crew-caption">Trekking in alta quota, Perù</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_1169.jpeg" alt="" loading="lazy">
                <div class="crew-caption">Cena gourmet, Lima, Perù</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_2748.JPG" alt="" loading="lazy">
                <div class="crew-caption">Valle de las Ánimas, La Paz, Bolivia</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_3185.JPG" alt="" loading="lazy">
                <div class="crew-caption">Tramonto sul Salar de Uyuni, Bolivia</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_3759.JPG" alt="" loading="lazy">
                <div class="crew-caption">Una sera tra amici</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_3979.JPG" alt="" loading="lazy">
                <div class="crew-caption">Pausa fast food, Cile</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_4070.JPG" alt="" loading="lazy">
                <div class="crew-caption">Ingresso a Machu Picchu, Perù</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_4089.JPG" alt="" loading="lazy">
                <div class="crew-caption">Lungo i binari di Aguas Calientes, Perù</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_4173.JPG" alt="" loading="lazy">
                <div class="crew-caption">Machu Picchu, la vista classica</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_4746.JPG" alt="" loading="lazy">
                <div class="crew-caption">Salinas de Maras, Perù</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_4786.JPG" alt="" loading="lazy">
                <div class="crew-caption">Pausa pranzo in centro commerciale</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_6903.JPG" alt="" loading="lazy">
                <div class="crew-caption">In viaggio con il cane</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_6970.JPG" alt="" loading="lazy">
                <div class="crew-caption">Serata a un evento</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/IMG_7186.JPG" alt="" loading="lazy">
                <div class="crew-caption">Ferrovia di Uyuni, Bolivia</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/group-barbiere.jpeg" alt="" loading="lazy">
                <div class="crew-caption">Un taglio di capelli</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/group-notte-strada.jpeg" alt="" loading="lazy">
                <div class="crew-caption">Passeggiata notturna, on the road</div>
              </div>
              <div class="group-marquee-item" aria-hidden="true">
                <img src="foto/group-relax-maschere.jpeg" alt="" loading="lazy">
                <div class="crew-caption">Relax dopo il trek</div>
              </div>
            </div>
          </div>

          <p class="section-sub reveal" style="margin-top:18px;">Machu Picchu, i geyser boliviani a 5.000 metri, Rio, le notti in bus sull'altopiano — e adesso l'inverno artico e la primavera coreana. Direi che siamo pronti per qualsiasi cosa.</p>
        </div>
      </section>

      <section class="panel" data-nav>
        <div class="inner" style="max-width:1060px;">
          <h2 class="section-title reveal">🌍 Tutte le mete</h2>
          <p class="section-sub reveal">I due viaggi con le date fissate. Ognuno ha la sua pagina: itinerario giorno per giorno, mappa animata, meteo e tutto il resto.</p>

          <div class="trip-grid reveal">
            <a class="trip-card" href="javascript:void(0)" onclick="showDest('is')">
              <img src="foto/destinazioni/is-kirkjufell.jpg" alt="Aurora boreale sul Kirkjufell, Islanda" loading="lazy">
              <div class="overlay"></div>
              <div class="content">
                <div class="flag">🇮🇸</div>
                <div class="title">Islanda</div>
                <div class="meta">2-9 gennaio 2027 · 8 giorni</div>
                <p class="tagline">Aurora, grotte di ghiaccio e la laguna glaciale, con quattro ore di luce al giorno.</p>
              </div>
            </a>

            <a class="trip-card" href="javascript:void(0)" onclick="showDest('kr')">
              <img src="foto/destinazioni/kr-ciliegi.jpg" alt="Ciliegi in fiore in Corea del Sud" loading="lazy">
              <div class="overlay"></div>
              <div class="content">
                <div class="flag">🇰🇷🇹🇼🇭🇰</div>
                <div class="title">Corea, Taiwan e Hong Kong</div>
                <div class="meta">2-18 aprile 2027 · 17 giorni</div>
                <p class="tagline">Seul, Gyeongju e Busan in KTX, il vulcano di Jeju, i ciliegi in fiore, e poi giù a tappe: Taipei e Hong Kong.</p>
              </div>
            </a>
          </div>
        </div>
      </section>

      <section class="panel dark" data-nav>
        <div class="inner">
          <h2 class="section-title reveal">🗺️ Viaggi già fatti</h2>
          <p class="section-sub reveal">Quanto mondo hanno già visto i Patagucci, e dove.</p>

          <div class="mondo-wrap reveal">
            <svg id="mondo" viewBox="0 0 950 620" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Mappamondo con i paesi visitati evidenziati">
<!--MAPPAMONDO-->
            </svg>
            <div class="mondo-stat">
              <div class="ms-box"><span class="ms-num">25<span class="ms-pct">%</span></span><span class="ms-lab">del mondo</span></div>
              <div class="ms-box"><span class="ms-num">49</span><span class="ms-lab">paesi</span></div>
              <div class="ms-box"><span class="ms-num">4</span><span class="ms-lab">continenti</span></div>
            </div>
            <div class="source-note">Il <strong>25%</strong> è 49 paesi sui <strong>195 stati membri dell'ONU</strong>: lo dichiaro perché contando anche territori e regioni autonome verrebbe un numero diverso. Fuori da quel conto ci sono <strong>Taiwan</strong>, <strong>Kosovo</strong>, <strong>Hong Kong</strong>, <strong>Macao</strong>, il <strong>Vaticano</strong>, le <strong>Canarie</strong> (che sono Spagna) e la <strong>Transnistria</strong>, che non sono stati membri ONU ma sono stati visti lo stesso. Bandiera della Transnistria: Wikimedia Commons, pubblico dominio. Mappa: Al MacDonald (@F1LT3R), <a href="https://commons.wikimedia.org/wiki/File:World_map_-_low_resolution.svg" target="_blank" rel="noopener">CC BY-SA 3.0</a>. Hong Kong, Macao, Singapore, Kosovo, San Marino, il Vaticano e le Seychelles sono troppo piccoli per essere colorati a questa scala. Gli elenchi per persona sono ancora parziali: manca tutto Manu.</div>
          </div>

          <h3 style="margin-top:30px;">Chi c'era, viaggio per viaggio</h3>
          <div class="card reveal" style="overflow-x:auto;">
            <table class="hub-table">
              <thead><tr><th>Meta</th><th>Con chi</th></tr></thead>
              <tbody>
                <tr><td>🇵🇪🇧🇴🇨🇱 Perù, Bolivia e Cile</td><td>Tutti insieme</td></tr>
                <tr><td>🇲🇩 Moldavia</td><td>Bacci, Mala, Manu</td></tr>
                <tr><td>🇯🇵 Giappone</td><td>Bacci, Manu, Mala</td></tr>
                <tr><td>🇲🇰🇽🇰 Macedonia del Nord e Kosovo</td><td>Bacci, Manu, Mala</td></tr>
              </tbody>
            </table>
          </div>

          <h3 style="margin-top:30px;">Paese per paese, uno per uno</h3>

          <div class="persona-paesi reveal">
            <div class="pp-nome">🧭 Mala</div>
            <div class="paesi-fatti">
              <span class="paese-fatto"><span class="pf-flag">🇲🇽</span><span class="pf-nome">Messico</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇬🇹</span><span class="pf-nome">Guatemala</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇨🇴</span><span class="pf-nome">Colombia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇧🇴</span><span class="pf-nome">Bolivia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇵🇪</span><span class="pf-nome">Perù</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇨🇱</span><span class="pf-nome">Cile</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇦🇷</span><span class="pf-nome">Argentina</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇺🇸</span><span class="pf-nome">Stati Uniti</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇨🇳</span><span class="pf-nome">Cina</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇭🇰</span><span class="pf-nome">Hong Kong</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇴</span><span class="pf-nome">Macao</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇹🇼</span><span class="pf-nome">Taiwan</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇯🇵</span><span class="pf-nome">Giappone</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇸🇬</span><span class="pf-nome">Singapore</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇾</span><span class="pf-nome">Malesia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇹🇭</span><span class="pf-nome">Thailandia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇮🇩</span><span class="pf-nome">Indonesia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇱🇰</span><span class="pf-nome">Sri Lanka</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇦</span><span class="pf-nome">Marocco</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇪🇸</span><span class="pf-nome">Spagna</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇮🇪</span><span class="pf-nome">Irlanda</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇷🇴</span><span class="pf-nome">Romania</span></span>
              <span class="paese-fatto"><span class="pf-flag"><svg viewBox="0 0 1200 600" width="24" height="12" role="img" aria-label="Bandiera della Transnistria" style="display:block;border-radius:2px;"><path fill="#de0000" d="M0 0h1200v600H0z"/><path fill="#093" d="M0 225h1200v150H0z"/><path fill="gold" d="m150 30-6.735 20.73h-21.797l17.634 12.81-6.736 20.73L150 71.46l17.634 12.812-6.736-20.73 17.633-12.812h-21.796zm0 10.8 4.31 13.267h13.95l-11.285 8.2 4.31 13.266-11.285-8.2-11.285 8.2 4.31-13.267-11.285-8.2h13.95z"/><g fill="gold"><path d="m101.839 138.547 14.93 14.993 14.078-13.945c21.415 22.909 43.877 44.991 65.126 67.988a8.22 8.22 0 0 0 11.603.04 8.168 8.168 0 0 0 .04-11.573c-22.808-21.463-45.687-43.102-68.502-64.644l18.967-18.787-26.388-3.644z"/><path d="M150 90c12.281 6.899 21.606 16.8 27.106 27.15 5.575 10.49 8.025 21.44 8.075 30.197.104 17.953-14.592 32.508-32.593 32.508-9.605 0-18.24-4.143-24.205-10.736l-3.3 2.77a4.931 4.931 0 0 0-5.519 1.412 6.181 6.181 0 0 0-5.069 4.178c-2.48 4.964-6.834 8.857-12.102 10.64-.05.017-.095.039-.139.061-2.436.89-4.877 2.498-6.956 4.58-4.11 4.134-6.117 9.423-4.987 13.135-.111.322-.169.66-.17 1.002a3.107 3.107 0 0 0 4.36 2.838c3.715.835 8.76-1.22 12.706-5.178 2.237-2.25 3.913-4.913 4.735-7.524 1.834-5.228 5.776-9.487 10.782-11.882.12-.058.216-.117.303-.177a6.173 6.173 0 0 0 3.344-4.116c7.678 9.035 19.194 14.804 32.068 15.106 23.612.554 41.261-16.781 42.077-41.709.411-12.545-4.455-28.721-15.545-41.988C176.496 102.127 164.07 93.71 150 90z"/></g></svg></span><span class="pf-nome">Transnistria</span></span>
            </div>
          </div>

          <div class="persona-paesi reveal">
            <div class="pp-nome">💻 Bacci</div>
            <div class="paesi-fatti">
              <span class="paese-fatto"><span class="pf-flag">🇵🇪</span><span class="pf-nome">Perù</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇧🇴</span><span class="pf-nome">Bolivia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇨🇱</span><span class="pf-nome">Cile</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇨🇺</span><span class="pf-nome">Cuba</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇯🇵</span><span class="pf-nome">Giappone</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇹🇭</span><span class="pf-nome">Thailandia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇱🇰</span><span class="pf-nome">Sri Lanka</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇦🇪</span><span class="pf-nome">Emirati Arabi</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇦🇿</span><span class="pf-nome">Azerbaigian</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇹🇳</span><span class="pf-nome">Tunisia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇸🇨</span><span class="pf-nome">Seychelles</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇮🇹</span><span class="pf-nome">Italia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇸🇲</span><span class="pf-nome">San Marino</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇻🇦</span><span class="pf-nome">Vaticano</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇪🇸</span><span class="pf-nome">Spagna</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇮🇨</span><span class="pf-nome">Canarie</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇵🇹</span><span class="pf-nome">Portogallo</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇫🇷</span><span class="pf-nome">Francia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇧🇪</span><span class="pf-nome">Belgio</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇳🇱</span><span class="pf-nome">Paesi Bassi</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇨🇭</span><span class="pf-nome">Svizzera</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇩🇰</span><span class="pf-nome">Danimarca</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇬🇧</span><span class="pf-nome">Regno Unito</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇬🇷</span><span class="pf-nome">Grecia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇭🇷</span><span class="pf-nome">Croazia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇭🇺</span><span class="pf-nome">Ungheria</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇷🇴</span><span class="pf-nome">Romania</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇩</span><span class="pf-nome">Moldavia</span></span>
              <span class="paese-fatto"><span class="pf-flag"><svg viewBox="0 0 1200 600" width="24" height="12" role="img" aria-label="Bandiera della Transnistria" style="display:block;border-radius:2px;"><path fill="#de0000" d="M0 0h1200v600H0z"/><path fill="#093" d="M0 225h1200v150H0z"/><path fill="gold" d="m150 30-6.735 20.73h-21.797l17.634 12.81-6.736 20.73L150 71.46l17.634 12.812-6.736-20.73 17.633-12.812h-21.796zm0 10.8 4.31 13.267h13.95l-11.285 8.2 4.31 13.266-11.285-8.2-11.285 8.2 4.31-13.267-11.285-8.2h13.95z"/><g fill="gold"><path d="m101.839 138.547 14.93 14.993 14.078-13.945c21.415 22.909 43.877 44.991 65.126 67.988a8.22 8.22 0 0 0 11.603.04 8.168 8.168 0 0 0 .04-11.573c-22.808-21.463-45.687-43.102-68.502-64.644l18.967-18.787-26.388-3.644z"/><path d="M150 90c12.281 6.899 21.606 16.8 27.106 27.15 5.575 10.49 8.025 21.44 8.075 30.197.104 17.953-14.592 32.508-32.593 32.508-9.605 0-18.24-4.143-24.205-10.736l-3.3 2.77a4.931 4.931 0 0 0-5.519 1.412 6.181 6.181 0 0 0-5.069 4.178c-2.48 4.964-6.834 8.857-12.102 10.64-.05.017-.095.039-.139.061-2.436.89-4.877 2.498-6.956 4.58-4.11 4.134-6.117 9.423-4.987 13.135-.111.322-.169.66-.17 1.002a3.107 3.107 0 0 0 4.36 2.838c3.715.835 8.76-1.22 12.706-5.178 2.237-2.25 3.913-4.913 4.735-7.524 1.834-5.228 5.776-9.487 10.782-11.882.12-.058.216-.117.303-.177a6.173 6.173 0 0 0 3.344-4.116c7.678 9.035 19.194 14.804 32.068 15.106 23.612.554 41.261-16.781 42.077-41.709.411-12.545-4.455-28.721-15.545-41.988C176.496 102.127 164.07 93.71 150 90z"/></g></svg></span><span class="pf-nome">Transnistria</span></span>
            </div>
          </div>

          <div class="persona-paesi reveal">
            <div class="pp-nome">🌟 Kiki</div>
            <div class="paesi-fatti">
              <span class="paese-fatto"><span class="pf-flag">🇺🇸</span><span class="pf-nome">Stati Uniti</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇽</span><span class="pf-nome">Messico</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇨🇺</span><span class="pf-nome">Cuba</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇧🇸</span><span class="pf-nome">Bahamas</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇧🇷</span><span class="pf-nome">Brasile</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇵🇪</span><span class="pf-nome">Perù</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇧🇴</span><span class="pf-nome">Bolivia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇨🇱</span><span class="pf-nome">Cile</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇯🇵</span><span class="pf-nome">Giappone</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇵🇭</span><span class="pf-nome">Filippine</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇾</span><span class="pf-nome">Malesia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇸🇬</span><span class="pf-nome">Singapore</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇮🇩</span><span class="pf-nome">Indonesia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇻</span><span class="pf-nome">Maldive</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇯🇴</span><span class="pf-nome">Giordania</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇹🇷</span><span class="pf-nome">Turchia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇦</span><span class="pf-nome">Marocco</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇨🇻</span><span class="pf-nome">Capo Verde</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇺</span><span class="pf-nome">Mauritius</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇵🇹</span><span class="pf-nome">Portogallo</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇪🇸</span><span class="pf-nome">Spagna</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇫🇷</span><span class="pf-nome">Francia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇳🇱</span><span class="pf-nome">Paesi Bassi</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇩🇪</span><span class="pf-nome">Germania</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇦🇹</span><span class="pf-nome">Austria</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇨🇭</span><span class="pf-nome">Svizzera</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇭🇷</span><span class="pf-nome">Croazia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇬🇷</span><span class="pf-nome">Grecia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇹</span><span class="pf-nome">Malta</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇬🇧</span><span class="pf-nome">Regno Unito</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇻🇦</span><span class="pf-nome">Vaticano</span></span>
            </div>
          </div>
        </div>
      </section>

    </main>

    <footer>
      Patagucci Trips — quattro amici, uno zaino e la prossima meta sempre aperta.
    </footer>
  </div>'''


# Il mappamondo sta in un file suo: cosi' aggiornare i paesi visitati non
# richiede di toccare questo script.
with open(DIR + "_sources/mappamondo.svg", encoding="utf-8") as _f:
    hub_html = hub_html.replace("<!--MAPPAMONDO-->", _f.read())

destination_blocks = "\n\n".join(b["block"] for b in blocks)

# Il contesto della chat, diviso per scheda.
#
# In un blocco unico la chat, aperta sull'Islanda, rispondeva della
# Corea: aveva tutto sotto gli occhi e della pagina aperta sapeva solo
# per sentito dire. Adesso ogni scheda riceve il proprio viaggio e basta,
# piu' la home e un indice delle altre per sapere dove mandare chi chiede
# d'altro. Costa anche meno: un terzo dei token per domanda.
#
# Finisce in un modulo JS e non in un .txt perche' cosi' Vercel se lo
# porta dentro la funzione da solo, come qualsiasi altra dipendenza.
import datetime

comune = "\n\n".join([
    "# Patagucci Trips",
    f"Contenuto del sito, generato da _sources/build.py il {datetime.date.today().isoformat()}.",
    "Le mete con stato \"confermato\" hanno le date fissate; \"idea\" no.",
    "## 🌍 La home del sito\n\n" + testo_da_html(hub_html),
])

indice = "\n".join(
    f"- {d['flag']} {d['name']} ({d['stato']}) — scheda \"{d['suf']}\""
    for d in DESTS
)

contesto = {"comune": comune, "indice": indice, "schede": contesti}
with open(DIR + "api/contesto.js", "w", encoding="utf-8") as f:
    f.write(
        "// Generato da _sources/build.py insieme a index.html. Non modificare a mano.\n"
        "// Serve a api/chat.js: il contenuto del sito, una voce per scheda.\n"
        "module.exports = " + json.dumps(contesto) + ";\n"
    )
print("Written", DIR + "api/contesto.js",
      "| comune", len(comune),
      "| schede:", ", ".join(f"{k}={len(v)}" for k, v in contesti.items()))

stato_per_suf = {d["suf"]: d["stato"] for d in DESTS}
switcher_buttons = '\n        '.join(
    f'<button class="switch-btn{" confermato" if stato_per_suf[b["suf"]] == "confermato" else ""}"'
    f' data-dest="{b["suf"]}" onclick="showDest(\'{b["suf"]}\')">{b["flag"]} {b["name"]}</button>'
    for b in blocks
)

# ----------------------------------------------------------------------
# "Chiedi ai Patagucci": il pannello di chat.
#
# Sta qui e non in una pagina sorgente perche' e' dell'intero sito, non
# di una meta: il bottone resta in basso a destra ovunque, e la scheda
# aperta viene passata alla funzione come contesto della domanda.
# Il tema (colori, accenti) lo eredita da data-dest come tutto il resto.
# ----------------------------------------------------------------------

chat_css = '''
  .pg-chat .sr-only{
    position:absolute; width:1px; height:1px; padding:0; margin:-1px;
    overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0;
  }
  .pg-chat-fab{
    position:fixed; right:16px; bottom:16px; z-index:500;
    display:flex; align-items:center; gap:9px;
    border:1px solid rgba(var(--accent-rgb),0.5); border-radius:999px;
    background:linear-gradient(180deg,#1d1d1d,#101010); color:var(--accent);
    padding:11px 18px; font-family:var(--font-body); font-size:0.84rem; font-weight:800;
    cursor:pointer; box-shadow:0 10px 28px rgba(0,0,0,0.45);
    transition:transform .18s cubic-bezier(.16,1,.3,1), box-shadow .18s ease, background .5s ease;
  }
  .pg-chat-fab:hover{ transform:translateY(-2px); box-shadow:0 16px 36px rgba(0,0,0,0.5); }
  .pg-chat-fab:focus-visible{ outline:2px solid var(--accent); outline-offset:3px; }
  .pg-chat-fab .pg-fab-icona{ font-size:1.05rem; line-height:1; }
  .pg-chat-fab[aria-expanded="true"]{ opacity:0; pointer-events:none; }

  .pg-chat{
    position:fixed; right:16px; bottom:16px; z-index:501;
    width:min(390px, calc(100vw - 32px)); max-height:min(620px, calc(100vh - 32px));
    display:flex; flex-direction:column; overflow:hidden;
    background:linear-gradient(180deg,#1a1a1a,#101010);
    border:1px solid rgba(var(--accent-rgb),0.28); border-radius:20px;
    box-shadow:0 30px 70px rgba(0,0,0,0.55);
    font-family:var(--font-body);
    animation:pgChatSu .28s cubic-bezier(.16,1,.3,1) both;
  }
  .pg-chat[hidden]{ display:none; }
  @keyframes pgChatSu{ from{ opacity:0; transform:translateY(14px) scale(.98); } to{ opacity:1; transform:none; } }

  .pg-chat-testa{
    display:flex; align-items:center; justify-content:space-between; gap:10px;
    padding:13px 16px; border-bottom:1px solid rgba(255,255,255,0.09);
    background:linear-gradient(180deg, rgba(var(--accent-rgb),0.13), transparent);
  }
  .pg-chat-testa strong{ display:block; color:#fdf9f0; font-size:0.92rem; letter-spacing:0.01em; }
  .pg-chat-dove{ display:block; font-size:0.72rem; color:var(--accent); font-weight:700; margin-top:2px; }
  .pg-chat-testa button{
    border:none; background:rgba(255,255,255,0.07); color:#c7c2b6;
    width:30px; height:30px; border-radius:9px; font-size:0.9rem; cursor:pointer; flex:0 0 auto;
  }
  .pg-chat-testa button:hover{ background:rgba(255,255,255,0.15); color:#fff; }

  .pg-chat-righe{ flex:1 1 auto; overflow-y:auto; padding:16px; display:flex; flex-direction:column; gap:12px; }
  .pg-chat-riga{ max-width:88%; font-size:0.87rem; line-height:1.62; }
  .pg-chat-riga.io{
    align-self:flex-end; background:var(--accent); color:#10100e;
    padding:9px 14px; border-radius:16px 16px 4px 16px; font-weight:600;
  }
  .pg-chat-riga.lei{ align-self:flex-start; color:#e4e0d6; }
  .pg-chat-riga.lei strong{ color:#fdf9f0; }
  .pg-chat-riga.lei a{ color:var(--accent); }
  .pg-chat-riga.lei ul{ margin:6px 0; padding-left:18px; }
  .pg-chat-riga.guasto{ align-self:flex-start; color:#ff9b8a; font-size:0.82rem; }
  .pg-chat-fonti{ margin-top:7px; font-size:0.72rem; line-height:1.6; color:#8d887d; }
  .pg-chat-fonti a{ color:var(--accent); text-decoration:none; border-bottom:1px solid rgba(var(--accent-rgb),0.35); }
  .pg-chat-fonti a:hover{ border-bottom-color:var(--accent); }
  .pg-chat-stato{ align-self:flex-start; font-size:0.78rem; color:var(--accent); opacity:0.85; }
  .pg-chat-riga .pg-cursore{
    display:inline-block; width:7px; height:14px; margin-left:2px; vertical-align:-2px;
    background:var(--accent); animation:pgLampeggia 1s steps(2,start) infinite;
  }
  @keyframes pgLampeggia{ 50%{ opacity:0; } }

  .pg-chat-spunti{ display:flex; flex-wrap:wrap; gap:6px; padding:0 16px 12px; }
  .pg-chat-spunti button{
    border:1px solid rgba(var(--accent-rgb),0.3); background:rgba(var(--accent-rgb),0.08);
    color:var(--accent); padding:6px 12px; border-radius:999px;
    font-size:0.75rem; font-weight:600; font-family:var(--font-body); cursor:pointer;
  }
  .pg-chat-spunti button:hover{ background:rgba(var(--accent-rgb),0.18); }

  .pg-chat-invio{ display:flex; gap:8px; align-items:flex-end; padding:12px 16px; border-top:1px solid rgba(255,255,255,0.09); }
  .pg-chat-invio textarea{
    flex:1 1 auto; resize:none; max-height:120px;
    background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.14); border-radius:12px;
    color:#f2efe7; font-family:var(--font-body); font-size:0.86rem; line-height:1.5; padding:10px 12px;
  }
  .pg-chat-invio textarea::placeholder{ color:#8d887d; }
  .pg-chat-invio textarea:focus{ outline:2px solid var(--accent); outline-offset:0; }
  .pg-chat-invio button{
    flex:0 0 auto; width:40px; height:40px; border:none; border-radius:12px; cursor:pointer;
    background:var(--accent); color:#10100e; font-size:1rem; font-weight:800;
  }
  .pg-chat-invio button:disabled{ opacity:0.4; cursor:not-allowed; }

  @media (max-width:560px){
    .pg-chat{ right:0; left:0; bottom:0; width:100%; max-height:86vh; border-radius:20px 20px 0 0; }
    .pg-chat-fab{ right:12px; bottom:12px; padding:12px 16px; }
    .pg-chat-fab .pg-fab-testo{ display:none; }
  }
  @media (prefers-reduced-motion:reduce){
    .pg-chat{ animation:none; }
    .pg-chat-riga .pg-cursore{ animation:none; }
  }
'''

chat_html = '''
<button class="pg-chat-fab" id="pg-chat-fab" aria-expanded="false" aria-controls="pg-chat">
  <span class="pg-fab-icona" aria-hidden="true">💬</span>
  <span class="pg-fab-testo">Chiedi ai Patagucci</span>
</button>

<section class="pg-chat" id="pg-chat" role="dialog" aria-label="Chiedi ai Patagucci" hidden>
  <header class="pg-chat-testa">
    <div>
      <strong>💬 Chiedi ai Patagucci</strong>
      <span class="pg-chat-dove" id="pg-chat-dove"></span>
    </div>
    <button type="button" id="pg-chat-chiudi" aria-label="Chiudi">✕</button>
  </header>
  <div class="pg-chat-righe" id="pg-chat-righe" aria-live="polite"></div>
  <div class="pg-chat-spunti" id="pg-chat-spunti"></div>
  <form class="pg-chat-invio" id="pg-chat-form">
    <label class="sr-only" for="pg-chat-testo">La tua domanda</label>
    <textarea id="pg-chat-testo" rows="1" maxlength="1500" placeholder="Scrivi una domanda sui viaggi…"></textarea>
    <button type="submit" id="pg-chat-manda" aria-label="Manda la domanda">➤</button>
  </form>
</section>
'''

# Nomi leggibili e spunti di partenza: la chat dice alla funzione quale
# scheda e' aperta, e propone domande che su quella scheda hanno senso.
NOMI_METE = {"hub": "la home"}
NOMI_METE.update({d["suf"]: d["name"] for d in DESTS})

SPUNTI = {
    "hub": ["Serve il visto per queste mete?", "Che vaccinazioni servono?", "Quanto costa l'assicurazione?"],
    "is": ["Quanto costa l'ingresso alla Blue Lagoon?", "Com'è il meteo adesso in Islanda?", "I vulcani sono attivi in questo momento?"],
    "kr": ["Quanto costano i voli in tutto?", "Cosa si fa a Taipei in due giorni?", "Serve il K-ETA per gli italiani?"],
    "nx": ["Dove si vola con poco a gennaio?", "Quali mete sono fuori stagione ad aprile?", "Come funziona la ricerca voli?"],
}

chat_js = '''
// ------------------------------------------------------------------
// "Chiedi ai Patagucci".
// La pagina non sa niente dei viaggi: manda la domanda, lo storico e la
// scheda aperta a /api/chat, che risponde in streaming. Il contenuto del
// sito ce l'ha la funzione, generata insieme a questa pagina.
// ------------------------------------------------------------------
(function(){
  // Servito da Vercel: stessa origine. Aperto in locale col doppio clic
  // o da GitHub Pages: serve l'indirizzo assoluto del deploy.
  var API_REMOTA = 'https://patagucci-trip.vercel.app/api/chat';
  var locale = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
  var API = (location.protocol.indexOf('http') === 0 && (locale || !API_REMOTA)) ? '/api/chat' : API_REMOTA;

  var NOMI = __NOMI__;
  var SPUNTI = __SPUNTI__;
  var CHIAVE_STORICO = 'patagucci-chat-v2';

  var fab = document.getElementById('pg-chat-fab');
  var pannello = document.getElementById('pg-chat');
  var righe = document.getElementById('pg-chat-righe');
  var spunti = document.getElementById('pg-chat-spunti');
  var form = document.getElementById('pg-chat-form');
  var campo = document.getElementById('pg-chat-testo');
  var manda = document.getElementById('pg-chat-manda');
  var dove = document.getElementById('pg-chat-dove');

  // Una conversazione per scheda, non una sola per tutto il sito: le
  // domande sull'Islanda non hanno niente da dire su quelle coreane, e
  // tornando su una scheda si ritrova il discorso lasciato li'.
  var fili = {};
  var inCorso = false;

  try {
    var salvato = sessionStorage.getItem(CHIAVE_STORICO);
    if(salvato) fili = JSON.parse(salvato) || {};
  } catch(e){ fili = {}; }

  function metaAttiva(){ return document.documentElement.getAttribute('data-dest') || 'hub'; }
  function nomeMeta(){ return NOMI[metaAttiva()] || 'la home'; }

  function filo(scheda){
    var k = scheda || metaAttiva();
    if(!fili[k]) fili[k] = [];
    return fili[k];
  }

  function salva(){
    try {
      var corti = {};
      Object.keys(fili).forEach(function(k){ if(fili[k].length) corti[k] = fili[k].slice(-16); });
      sessionStorage.setItem(CHIAVE_STORICO, JSON.stringify(corti));
    } catch(e){}
  }

  // La risposta arriva come testo semplice. Qui si scappa tutto e poi si
  // riaccendono le due sole cose che il modello usa: grassetto e righe.
  function formatta(testo){
    var s = testo.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    s = s.replace(/\\*\\*([^*]+)\\*\\*/g, '<strong>$1</strong>');
    s = s.replace(/\\n/g, '<br>');
    return s;
  }

  function aggiungi(ruolo, testo){
    var el = document.createElement('div');
    el.className = 'pg-chat-riga ' + (ruolo === 'utente' ? 'io' : ruolo === 'guasto' ? 'guasto' : 'lei');
    el.innerHTML = formatta(testo);
    righe.appendChild(el);
    righe.scrollTop = righe.scrollHeight;
    return el;
  }

  // Le pagine citate finiscono sotto la risposta: sono di qualcun altro
  // e chi legge deve poterci andare. Link e titoli arrivano dal modello,
  // quindi niente innerHTML e solo http/https come destinazione.
  function disegnaFonti(el, lista){
    if(!el || !lista || !lista.length) return;
    var box = document.createElement('div');
    box.className = 'pg-chat-fonti';
    box.appendChild(document.createTextNode('Cercato su: '));
    lista.forEach(function(f, i){
      if(!/^https?:\/\//i.test(f.url || '')) return;
      var a = document.createElement('a');
      a.href = f.url;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.textContent = f.titolo || f.url;
      box.appendChild(a);
      if(i < lista.length - 1) box.appendChild(document.createTextNode(' · '));
    });
    el.appendChild(box);
  }

  function disegnaSpunti(){
    var lista = SPUNTI[metaAttiva()] || SPUNTI.hub;
    spunti.innerHTML = '';
    if(filo().length) return;   // gli spunti servono solo a rompere il ghiaccio
    lista.forEach(function(s){
      var b = document.createElement('button');
      b.type = 'button';
      b.textContent = s;
      b.addEventListener('click', function(){ chiedi(s); });
      spunti.appendChild(b);
    });
  }

  function ridisegna(){
    righe.innerHTML = '';
    if(!filo().length){
      aggiungi('assistente', 'Ciao. Il sito lo leggi da solo: io servo per quello che non c\\'è scritto — prezzi d\\'ingresso, orari, meteo di adesso, visti, cosa conviene prenotare. Vado a cercarlo sul web. Stai guardando **' + nomeMeta() + '**.');
    } else {
      filo().forEach(function(m){ disegnaFonti(aggiungi(m.ruolo, m.testo), m.fonti); });
    }
    disegnaSpunti();
  }

  function apri(){
    pannello.hidden = false;
    fab.setAttribute('aria-expanded', 'true');
    dove.textContent = 'stai guardando: ' + nomeMeta();
    ridisegna();
    setTimeout(function(){ campo.focus(); }, 60);
  }

  function chiudi(){
    pannello.hidden = true;
    fab.setAttribute('aria-expanded', 'false');
    fab.focus();
  }

  fab.addEventListener('click', apri);
  document.getElementById('pg-chat-chiudi').addEventListener('click', chiudi);
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape' && !pannello.hidden) chiudi();
  });

  // Cambiando scheda si passa all'altra conversazione: quella lasciata
  // resta dov'era e si ritrova tornando indietro. Se una risposta e'
  // ancora in arrivo non si cambia filo a meta' — finisce nel suo.
  window.addEventListener('destinazione-cambiata', function(){
    if(pannello.hidden) return;
    dove.textContent = 'stai guardando: ' + nomeMeta();
    if(!inCorso) ridisegna();
  });

  campo.addEventListener('input', function(){
    campo.style.height = 'auto';
    campo.style.height = Math.min(campo.scrollHeight, 120) + 'px';
  });
  campo.addEventListener('keydown', function(e){
    if(e.key === 'Enter' && !e.shiftKey){ e.preventDefault(); form.requestSubmit(); }
  });
  form.addEventListener('submit', function(e){
    e.preventDefault();
    chiedi(campo.value);
  });

  function chiedi(domanda){
    domanda = String(domanda || '').trim();
    if(!domanda || inCorso) return;
    // La scheda si fissa adesso: se cambia mentre la risposta arriva,
    // quella risposta appartiene comunque alla conversazione di qui.
    var schedaTurno = metaAttiva();
    var mio = filo(schedaTurno);
    if(!mio.length) righe.innerHTML = '';
    inCorso = true;
    manda.disabled = true;
    campo.value = '';
    campo.style.height = 'auto';
    spunti.innerHTML = '';

    mio.push({ ruolo:'utente', testo: domanda });
    aggiungi('utente', domanda);
    salva();

    var el = aggiungi('assistente', '');
    el.innerHTML = '<span class="pg-cursore"></span>';
    var risposta = '';
    var fontiTurno = null;
    // Mentre cerca sul web non arriva testo per parecchi secondi: senza
    // questa riga sembra piantato.
    var stato = document.createElement('div');
    stato.className = 'pg-chat-riga pg-chat-stato';
    stato.hidden = true;
    righe.appendChild(stato);

    function chiudiTurno(){
      inCorso = false;
      manda.disabled = false;
      campo.focus();
    }

    var taglio = new AbortController();
    var scadenza = setTimeout(function(){ taglio.abort(); }, 60000);

    fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messaggi: mio.slice(-16), meta: NOMI[schedaTurno] || 'la home', scheda: schedaTurno }),
      signal: taglio.signal
    }).then(function(r){
      if(!r.ok || !r.body){
        return r.json().catch(function(){ return {}; }).then(function(d){
          var guasto = new Error(d.errore || 'Non riesco a rispondere adesso. Riprova fra un attimo.');
          guasto.gentile = true;
          throw guasto;
        });
      }
      var lettore = r.body.getReader();
      var decoder = new TextDecoder();
      var resto = '';

      function pezzo(){
        return lettore.read().then(function(res){
          if(res.done){
            clearTimeout(scadenza);
            stato.remove();
            if(risposta){
              mio.push({ ruolo:'assistente', testo: risposta, fonti: fontiTurno || undefined });
              salva();
            }
            chiudiTurno();
            return;
          }
          resto += decoder.decode(res.value, { stream:true });
          var blocchi = resto.split('\\n\\n');
          resto = blocchi.pop();
          blocchi.forEach(function(b){
            var riga = b.split('\\n').filter(function(l){ return l.indexOf('data: ') === 0; })[0];
            if(!riga) return;
            var ev;
            try { ev = JSON.parse(riga.slice(6)); } catch(err){ return; }
            if(ev.t === 'testo'){
              risposta += ev.d;
              stato.hidden = true;
              el.innerHTML = formatta(risposta) + '<span class="pg-cursore"></span>';
              righe.scrollTop = righe.scrollHeight;
            } else if(ev.t === 'stato'){
              stato.textContent = ev.d;
              stato.hidden = false;
              righe.scrollTop = righe.scrollHeight;
            } else if(ev.t === 'fonti'){
              fontiTurno = ev.d;
            } else if(ev.t === 'errore'){
              el.className = 'pg-chat-riga guasto';
              el.textContent = ev.d;
              risposta = '';
            } else if(ev.t === 'fine'){
              stato.hidden = true;
              el.innerHTML = formatta(risposta) + (ev.d && ev.d.troncata ? ' <em>(risposta troncata)</em>' : '');
              disegnaFonti(el, fontiTurno);
            }
          });
          return pezzo();
        });
      }
      return pezzo();
    }).catch(function(err){
      clearTimeout(scadenza);
      el.className = 'pg-chat-riga guasto';
      // Solo i messaggi scritti apposta arrivano a schermo: quelli di
      // rete sono in inglese e non dicono niente a chi legge.
      el.textContent = err.name === 'AbortError'
        ? 'Nessuna risposta entro un minuto. Riprova.'
        : err.gentile ? err.message : 'Non riesco a rispondere adesso. Riprova fra un attimo.';
      chiudiTurno();
    });
  }
})();
'''.replace('__NOMI__', json.dumps(NOMI_METE, ensure_ascii=False)).replace('__SPUNTI__', json.dumps(SPUNTI, ensure_ascii=False))

final_html = f'''<!DOCTYPE html>
<html lang="it" data-dest="hub">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Patagucci Trips</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<style>
  .destination{{ display:none; }}
  .destination.active{{ display:block; animation:destIn .5s cubic-bezier(.16,1,.3,1) both; }}
  @keyframes destIn{{ from{{ opacity:0; transform:translateY(10px); }} to{{ opacity:1; transform:none; }} }}
  /* Una riga sola che scorre, a qualsiasi larghezza.
     Andando a capo occupava 97px gia' a 1280, 138px su tablet e 302px su
     telefono: con la barra delle sezioni sotto restava zero schermo per il
     contenuto. I due margin:auto la tengono centrata quando ci sta e non
     rendono irraggiungibile il primo bottone quando invece scorre. */
  .site-switcher{{
    position:sticky; top:0; z-index:200;
    display:flex; gap:6px; justify-content:flex-start; flex-wrap:nowrap;
    overflow-x:auto; -webkit-overflow-scrolling:touch; scrollbar-width:none;
    background:linear-gradient(180deg, rgba(var(--accent-rgb),0.12), transparent 60%), linear-gradient(180deg,#181818,#0e0e0e);
    padding:10px 12px; box-shadow:0 6px 18px rgba(0,0,0,0.35);
    border-bottom:1px solid rgba(var(--accent-rgb),0.22);
    transition:background .5s ease, border-color .5s ease;
  }}
  .site-switcher::-webkit-scrollbar{{ display:none; }}
  .site-switcher > button:first-child{{ margin-left:auto; }}
  .site-switcher > button:last-child{{ margin-right:auto; }}
  .site-switcher button{{
    flex:0 0 auto; white-space:nowrap;
    border:1px solid transparent; background:rgba(255,255,255,0.06); color:#cfcfcf;
    padding:8px 16px; border-radius:999px; font-size:0.8rem; font-weight:700; cursor:pointer;
    text-transform:uppercase; letter-spacing:0.04em; transition:all .2s cubic-bezier(.16,1,.3,1);
  }}
  .site-switcher button:hover{{ background:rgba(255,255,255,0.14); transform:translateY(-1px); }}
  .site-switcher button.active{{ background:var(--accent); color:#10100e; box-shadow:0 4px 14px rgba(var(--accent-rgb),0.4); }}
  .site-switcher button.home-btn{{ color:var(--accent); border-color:rgba(var(--accent-rgb),0.4); }}
  .site-switcher button.home-btn.active{{ color:#10100e; }}
  @media (max-width:760px){{
    .site-switcher{{ padding:7px 10px; }}
    .site-switcher button{{ padding:10px 13px; font-size:0.72rem; letter-spacing:0.03em; min-height:44px; }}
  }}
{chat_css}
</style>
</head>
<body>

<div class="flagbar" id="flagbar"></div>


<div class="site-switcher" id="site-switcher">
  <button class="home-btn active" data-dest="hub" onclick="showDest('hub')">🌍 Home</button>
  {switcher_buttons}
</div>

{hub_html}

{destination_blocks}

{chat_html}

<script>
var FLAG_BARS = {{
  hub: 'linear-gradient(90deg,#141414 0 50%, #FFCE00 50% 100%)',
  nx: 'linear-gradient(90deg,#FFCE00 0 25%, #2a6b4d 25% 50%, #D21034 50% 75%, #1D2A4D 75% 100%)',
  ug: 'linear-gradient(90deg,#141414 0 33%, #FFCE00 33% 66%, #D21034 66% 100%)',
  pk: 'linear-gradient(90deg,#ffffff 0 25%, #01411C 25% 100%)',
  za: 'linear-gradient(90deg,#DE3831 0 16.6%, #ffffff 16.6% 33.3%, #002395 33.3% 50%, #007A4D 50% 66.6%, #FFB612 66.6% 83.3%, #000000 83.3% 100%)',
  np: 'linear-gradient(90deg,#DC143C 0 25%, #003893 25% 50%, #FF9933 50% 75%, #FFB612 75% 100%)',
  uk: 'linear-gradient(90deg,#0099B5 0 50%, #1EB53A 50% 100%)',
  gl: 'linear-gradient(90deg,#ffffff 0 50%, #C60C30 50% 100%)',
  ge: 'linear-gradient(90deg,#ffffff 0 20%, #DA291C 20% 40%, #ffffff 40% 60%, #DA291C 60% 80%, #ffffff 80% 100%)',
  in: 'linear-gradient(90deg,#FF9933 0 33%, #ffffff 33% 66%, #138808 66% 100%)',
  tz: 'linear-gradient(90deg,#1EB53A 0 30%, #FCD116 30% 40%, #000000 40% 60%, #FCD116 60% 70%, #00A3DD 70% 100%)',
  cx: 'linear-gradient(90deg,#0067C6 0 20%, #ffffff 20% 33%, #002B7F 33% 46%, #CE1126 46% 60%, #ffffff 60% 73%, #D21034 73% 86%, #005293 86% 100%)',
  kr: 'linear-gradient(90deg,#ffffff 0 12%, #CD2E3A 12% 22%, #0047A0 22% 33%, #FE0000 33% 44%, #000095 44% 55%, #ffffff 55% 66%, #DE2910 66% 100%)',
  'kr-kr': 'linear-gradient(90deg,#ffffff 0 32%, #CD2E3A 32% 47%, #0047A0 47% 62%, #ffffff 62% 100%)',
  'kr-tw': 'linear-gradient(90deg,#000095 0 30%, #FE0000 30% 100%)',
  'kr-hk': 'linear-gradient(90deg,#DE2910 0 42%, #ffffff 42% 58%, #DE2910 58% 100%)',
  is: 'linear-gradient(90deg,#02529C 0 30%, #ffffff 30% 38%, #DC1E35 38% 47%, #ffffff 47% 55%, #02529C 55% 100%)'
}};
function showDest(name){{
  document.documentElement.setAttribute('data-dest', name);
  document.documentElement.removeAttribute('data-paese');
  document.querySelectorAll('.destination').forEach(function(el){{ el.classList.remove('active'); }});
  var target = document.getElementById(name === 'hub' ? 'dest-hub' : 'dest-' + name);
  if(target) target.classList.add('active');
  document.querySelectorAll('#site-switcher button').forEach(function(b){{ b.classList.remove('active'); }});
  var btn = document.querySelector('#site-switcher button[data-dest="' + name + '"]');
  if(btn){{
    btn.classList.add('active');
    // Su mobile il selettore e' una riga che scorre: senza questo la meta
    // attiva puo' restare fuori schermo.
    btn.scrollIntoView({{ behavior:'smooth', block:'nearest', inline:'center' }});
  }}
  var flagbar = document.getElementById('flagbar');
  if(flagbar && FLAG_BARS[name]) flagbar.style.background = FLAG_BARS[name];
  window.scrollTo({{ top: 0, left: 0, behavior: 'instant' }});
  target.querySelectorAll('.reveal').forEach(function(el){{ el.classList.add('visible'); }});
  // Fa ripartire da capo le mappe animate della meta appena aperta.
  window.dispatchEvent(new CustomEvent('destinazione-cambiata'));
  if(typeof syncSwitcherHeight === 'function') setTimeout(syncSwitcherHeight, 0);
}}
function showHub(){{ showDest('hub'); }}

// Una meta che attraversa piu' paesi tinge la pagina col paese che si sta
// guardando: la scheda chiama questa passando 'kr-tw', 'kr-hk' e simili,
// oppure niente per tornare alla bandiera unita della meta.
function tingiPaese(paese){{
  var radice = document.documentElement;
  var meta = radice.getAttribute('data-dest');
  if(paese) radice.setAttribute('data-paese', paese);
  else radice.removeAttribute('data-paese');
  var flagbar = document.getElementById('flagbar');
  if(!flagbar) return;
  var chiave = paese ? meta + '-' + paese : meta;
  var sfondo = FLAG_BARS[chiave] || FLAG_BARS[meta];
  if(sfondo) flagbar.style.background = sfondo;
}}

// Le due tab della home: confermati / in programma.
document.querySelectorAll('#trip-tabs .trip-tab').forEach(function(tab){{
  tab.addEventListener('click', function(){{
    var gruppo = tab.getAttribute('data-gruppo');
    document.querySelectorAll('#trip-tabs .trip-tab').forEach(function(t){{
      var attiva = t === tab;
      t.classList.toggle('active', attiva);
      t.setAttribute('aria-selected', attiva ? 'true' : 'false');
    }});
    document.querySelectorAll('.trip-gruppo').forEach(function(g){{
      g.classList.toggle('attivo', g.id === 'gruppo-' + gruppo);
    }});
    // Le card appena mostrate non hanno mai incrociato l'observer.
    document.querySelectorAll('.trip-gruppo.attivo .reveal').forEach(function(el){{
      el.classList.add('visible');
    }});
  }});
}});

function syncSwitcherHeight(){{
  var switcher = document.getElementById('site-switcher');
  if(switcher) document.documentElement.style.setProperty('--switcher-h', switcher.offsetHeight + 'px');
}}
syncSwitcherHeight();
window.addEventListener('resize', syncSwitcherHeight);
window.addEventListener('load', syncSwitcherHeight);

document.querySelectorAll('.crew-card[data-audio]').forEach(function(card){{
  var audio = new Audio(card.getAttribute('data-audio'));
  audio.preload = 'none';
  card.addEventListener('mouseenter', function(){{
    audio.currentTime = 0;
    audio.play().catch(function(){{}});
  }});
  card.addEventListener('mouseleave', function(){{
    audio.pause();
    audio.currentTime = 0;
  }});
}});
</script>

{"".join(scripts)}

<script>
{chat_js}
</script>

</body>
</html>
'''

out_path = DIR + "index.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print("Written", out_path, "length", len(final_html))

# Il sito monta il JavaScript per concatenazione di stringhe: un escape
# sbagliato produce uno script che non parte, e il resto della pagina
# sembra a posto. Qui li controlliamo tutti prima di considerare fatto.
def controlla_javascript(html):
    import re, subprocess, tempfile, os, shutil
    if not shutil.which("node"):
        print("  (node non disponibile: salto il controllo di sintassi JS)")
        return True
    ok = True
    for i, js in enumerate(re.findall(r"<script>(.*?)</script>", html, re.S)):
        f = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8")
        f.write(js); f.close()
        r = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
        os.unlink(f.name)
        if r.returncode:
            ok = False
            righe = [l for l in r.stderr.splitlines() if l.strip()]
            print("  ERRORE di sintassi nello script inline #%d:" % i)
            for l in righe[:4]:
                print("   ", l)
    return ok

if controlla_javascript(final_html):
    print("  JavaScript: sintassi ok")
else:
    raise SystemExit("Build interrotta: JavaScript non valido nella pagina generata.")
