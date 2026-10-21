import re

DIR = "/Users/mattiabacileri/Library/Mobile Documents/com~apple~CloudDocs/progetti/patagucci trip /"
SRC_DIR = DIR + "_sources/"

import json

DESTS = [
    {"file": "islanda-trip.html", "suf": "is", "flag": "🇮🇸", "name": "Islanda", "stato": "confermato"},
    {"file": "corea-trip.html", "suf": "kr", "flag": "🇰🇷🇧🇳🇸🇬", "name": "Corea, Brunei e Singapore", "stato": "confermato"},
    # "Quale sara' il prossimo?" e' fuori dal sito per scelta del gruppo.
    # La pagina resta in _sources/prossimo.html: per rimetterla in linea
    # basta questa riga.
    # {"file": "prossimo.html", "suf": "nx", "flag": "❓", "name": "Quale sarà il prossimo?", "stato": "idea"},
    # Un viaggio gia' fatto: il diario, ricostruito dalle foto.
    {"file": "perubolivia-trip.html", "suf": "pb", "flag": "🇵🇪🇧🇴🇨🇱", "name": "Perù, Bolivia e Cile", "stato": "fatto"},
]

def extract(tag, content):
    pattern = r'<' + tag + r'(?:\s[^>]*)?>.*?</' + tag + r'>'
    m = re.search(pattern, content, re.DOTALL)
    if not m:
        raise Exception(f"Could not find <{tag}> block")
    return m.group(0)


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
    <header class="hero">
      <div class="bg" role="img" aria-label="Noi quattro a Machu Picchu" style="background-image:url('foto/dd148649-09ef-45bd-8b5e-313dff562db8.jpeg'); background-position:center 40%;"></div>
      <div class="content">
        <h1>Patagucci Trips<svg class="aeroplanino" viewBox="0 0 260 80" aria-hidden="true" focusable="false"><path class="ap-scia" d="M2 78 C 40 78, 84 35.5, 126 30"/><image class="ap-aereo" href="assets/logo/aereo.webp" x="116" y="6" width="140" height="34.8" transform="rotate(-6 186 23.4)"/></svg></h1>
        <p class="tagline">Manu, Kiki, Mala e Bacci. Fra tutti e quattro abbiamo visto 76 paesi in cinque continenti, e il Sud America l'abbiamo girato insieme: diciassette giorni, da La Paz a Lima. Questo è il nostro quaderno: chi siamo, dove siamo stati e dove andiamo.</p>
        <div class="scroll-cue">↓ sfogliamo</div>
      </div>
    </header>

    <main>
      <section class="panel alt" data-nav>
        <div class="inner">
          <h2 class="section-title reveal">🔥 I Patagucci</h2>
          <p class="section-sub reveal">Lo stesso gruppo da sempre, una meta nuova ogni volta. Eccoci.</p>
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

          <div class="card nota-gruppo reveal">
            <h3>I Patagucci</h3>
            <p>
              Quattro amici, uno zaino e un biglietto di sola andata, ogni volta una meta nuova, ogni volta la stessa combriccola scatenata. Manu è il logistico, con lui il viaggio non si perde mai un colpo, ma senza dieci birre al giorno lo vedi diventare uno sconvolto. Kiki è la meteora pazza, sempre pronta a ripartire, ma toglietele il ceviche e la sentirete ruggire: diventa aggressiva, non capisce più niente, datele pesce crudo o scappate immediatamente. Mala è l'enciclopedia vivente del gruppo intero, sa tutto di ogni posto, storia e sentiero, ma se non prende la bumba prima di coricarsi la notte è tutta un rimbombo, meglio non disturbarsi. Bacci è il tecnologico, con lui non ti perdi in un vicolo, ma portatelo in quota e guardate che spettacolo: trema come una foglia al primo metro guadagnato, e giuro che una volta se l'è quasi fatta sotto, poveraccio. Quattro caratteri diversi, un'unica squadra che parte, i Patagucci vanno per il mondo, sempre dalla stessa parte — e ovunque li porti il prossimo volo o il prossimo passo, tornano a casa con una storia in più da raccontare, senza sosta.
            </p>
          </div>

          <h3>Insieme in giro per il mondo</h3>
          <div class="striscia-foto reveal">
            <div class="striscia-foto-binario" id="striscia-foto" tabindex="0" role="region" aria-label="Le foto del gruppo, da scorrere di lato">
              <div class="striscia-foto-item">
                <img src="foto/dd148649-09ef-45bd-8b5e-313dff562db8.jpeg" alt="Il gruppo al completo a Machu Picchu, Perù" loading="lazy">
                <div class="crew-caption">Machu Picchu, Perù</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_1590.JPG" alt="Il gruppo sui binari nel deserto di sale, Bolivia/Cile" loading="lazy">
                <div class="crew-caption">Deserto di sale, Bolivia/Cile</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_7193.JPG" alt="Il gruppo sui binari del treno, Salar de Uyuni, Bolivia" loading="lazy">
                <div class="crew-caption">Salar de Uyuni, Bolivia</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/group-geyser-bolivia.jpeg" alt="Il gruppo tra i fumi dei geyser, Bolivia" loading="lazy">
                <div class="crew-caption">Geyser Sol de Mañana, Bolivia</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/group-altopiano-boliviano.jpeg" alt="Pranzo di gruppo con vista sulla laguna, altopiano boliviano" loading="lazy">
                <div class="crew-caption">Altopiano boliviano</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/group-cusco-peru.jpeg" alt="Il gruppo di notte tra i vicoli di Cusco, Perù" loading="lazy">
                <div class="crew-caption">Cusco, Perù</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_6840.JPG" alt="Al mercato, La Paz, Bolivia" loading="lazy">
                <div class="crew-caption">Al mercato, La Paz, Bolivia</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/group-van-bolivia.jpeg" alt="In viaggio sul van tra un trasferimento e l'altro, Bolivia" loading="lazy">
                <div class="crew-caption">In viaggio, Bolivia</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/group-notte-ande.jpeg" alt="Il gruppo di notte tra le nuvole, Ande" loading="lazy">
                <div class="crew-caption">Notte in quota, Ande</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_0283.jpeg" alt="Selfie di gruppo sul bus notturno" loading="lazy">
                <div class="crew-caption">Notte in bus, on the road</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_0300.JPG" alt="Sul relitto di un treno al cimitero dei treni di Uyuni, Bolivia" loading="lazy">
                <div class="crew-caption">Cimitero dei treni, Uyuni, Bolivia</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_0343.jpeg" alt="Il gruppo davanti al fuoristrada sul Salar de Uyuni, Bolivia" loading="lazy">
                <div class="crew-caption">Il fuoristrada sul Salar de Uyuni, Bolivia</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_0420.jpeg" alt="Effetto prospettiva con il cappello, Salar de Uyuni" loading="lazy">
                <div class="crew-caption">Giochi di prospettiva, Salar de Uyuni</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_0422.jpeg" alt="Altro effetto prospettiva, Salar de Uyuni" loading="lazy">
                <div class="crew-caption">Ancora prospettiva, Salar de Uyuni</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_0589.jpeg" alt="Il gruppo davanti a una laguna colorata, altopiano boliviano" loading="lazy">
                <div class="crew-caption">Lagune colorate dell'altopiano, Bolivia</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_0683.jpeg" alt="Shopping di souvenir a San Pedro de Atacama, Cile" loading="lazy">
                <div class="crew-caption">Shopping a San Pedro de Atacama, Cile</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_0821.jpeg" alt="Trekking in alta quota tra le montagne, Perù" loading="lazy">
                <div class="crew-caption">Trekking in alta quota, Perù</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_1169.jpeg" alt="Cena di gruppo in un ristorante, Lima, Perù" loading="lazy">
                <div class="crew-caption">Cena gourmet, Lima, Perù</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_2748.JPG" alt="Tra le guglie di roccia della Valle de las Ánimas, La Paz, Bolivia" loading="lazy">
                <div class="crew-caption">Valle de las Ánimas, La Paz, Bolivia</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_3185.JPG" alt="Tramonto accanto al fuoristrada, Salar de Uyuni, Bolivia" loading="lazy">
                <div class="crew-caption">Tramonto sul Salar de Uyuni, Bolivia</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_3759.JPG" alt="Una sera tra amici al ristorante" loading="lazy">
                <div class="crew-caption">Una sera tra amici</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_3979.JPG" alt="Pausa fast food in centro commerciale, Cile" loading="lazy">
                <div class="crew-caption">Pausa fast food, Cile</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_4070.JPG" alt="All'ingresso del Santuario Storico di Machu Picchu, Perù" loading="lazy">
                <div class="crew-caption">Ingresso a Machu Picchu, Perù</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_4089.JPG" alt="Lungo la ferrovia verso Aguas Calientes, Perù" loading="lazy">
                <div class="crew-caption">Lungo i binari di Aguas Calientes, Perù</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_4173.JPG" alt="Il gruppo con la vista classica su Machu Picchu, Perù" loading="lazy">
                <div class="crew-caption">Machu Picchu, la vista classica</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_4746.JPG" alt="Il gruppo alle terrazze saline di Maras, Perù" loading="lazy">
                <div class="crew-caption">Salinas de Maras, Perù</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_4786.JPG" alt="La cena di sushi nikkei, Cusco" loading="lazy">
                <div class="crew-caption">Sushi nikkei, Cusco</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_6903.JPG" alt="In viaggio in auto con un cane a bordo" loading="lazy">
                <div class="crew-caption">In viaggio con il cane</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_6970.JPG" alt="Una serata di gruppo a un evento" loading="lazy">
                <div class="crew-caption">Serata a un evento</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/IMG_7186.JPG" alt="Verso la ferrovia del Salar de Uyuni, Bolivia" loading="lazy">
                <div class="crew-caption">Ferrovia di Uyuni, Bolivia</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/group-barbiere.jpeg" alt="Dal barbiere durante il viaggio" loading="lazy">
                <div class="crew-caption">Un taglio di capelli</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/group-notte-strada.jpeg" alt="Passeggiata notturna vicino a un distributore" loading="lazy">
                <div class="crew-caption">Passeggiata notturna, on the road</div>
              </div>
              <div class="striscia-foto-item">
                <img src="foto/group-relax-maschere.jpeg" alt="Relax con maschera viso dopo il trekking" loading="lazy">
                <div class="crew-caption">Relax dopo il trek</div>
              </div>
            </div>
            <button type="button" class="striscia-foto-freccia indietro" aria-controls="striscia-foto" aria-label="Foto precedenti"><svg viewBox="0 0 40 20" aria-hidden="true" focusable="false"><path d="M2 11 C 13 7, 25 13, 36 9 M29 3 L37 9 L30 16"/></svg></button>
            <button type="button" class="striscia-foto-freccia avanti" aria-controls="striscia-foto" aria-label="Foto successive"><svg viewBox="0 0 40 20" aria-hidden="true" focusable="false"><path d="M2 11 C 13 7, 25 13, 36 9 M29 3 L37 9 L30 16"/></svg></button>
          </div>

          <p class="section-sub reveal" style="margin-top:18px;">Machu Picchu, i geyser boliviani a 5.000 metri, Rio, le notti in bus sull'altopiano — e adesso l'inverno artico e la primavera coreana. Direi che siamo pronti per qualsiasi cosa.</p>
        </div>
      </section>

      <section class="panel" data-nav>
        <div class="inner">
          <h2 class="section-title reveal">🗺️ I viaggi fatti</h2>
          <p class="section-sub reveal">Il diario dei viaggi che abbiamo già fatto, e quanto mondo abbiamo visto finora.</p>

          <div class="trip-grid trip-grid-uno reveal">
            <a class="trip-card" href="javascript:void(0)" onclick="showDest('pb')">
              <img src="foto/IMG_4173.JPG" alt="Il gruppo con la vista classica su Machu Picchu" loading="lazy">
              <div class="overlay"></div>
              <div class="content">
                <div class="flag">🇵🇪🇧🇴🇨🇱</div>
                <div class="title">Perù, Bolivia e Cile</div>
                <div class="meta">17 aprile – 3 maggio 2026 · il diario</div>
                <p class="tagline">La Paz, il Salar di Uyuni, l'altopiano fino al Cile, Machu Picchu e Lima, giorno per giorno.</p>
              </div>
            </a>
          </div>

          <div class="mondo-wrap reveal">
            <svg id="mondo" viewBox="0 0 950 620" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Mappamondo con i paesi visitati evidenziati">
<!--MAPPAMONDO-->
            </svg>
            <div class="mondo-stat">
              <div class="ms-box"><span class="ms-num">39<span class="ms-pct">%</span></span><span class="ms-lab">del mondo</span></div>
              <div class="ms-box"><span class="ms-num">76</span><span class="ms-lab">paesi</span></div>
              <div class="ms-box"><span class="ms-num">5</span><span class="ms-lab">continenti</span></div>
            </div>
            <div class="source-note">Il <strong>39%</strong> è 76 paesi sui <strong>195 stati membri dell'ONU</strong>. Contando anche territori e regioni autonome il numero sarebbe diverso: fuori dal conteggio restano <strong>Taiwan</strong>, <strong>Kosovo</strong>, <strong>Hong Kong</strong>, <strong>Macao</strong>, il <strong>Vaticano</strong>, le <strong>Canarie</strong> (che sono Spagna) e la <strong>Transnistria</strong>, che non sono stati membri ONU ma sono stati visti lo stesso. Bandiera della Transnistria: Wikimedia Commons, pubblico dominio. Mappa: Al MacDonald (@F1LT3R), <a href="https://commons.wikimedia.org/wiki/File:World_map_-_low_resolution.svg" target="_blank" rel="noopener">CC BY-SA 3.0</a>. Hong Kong, Macao, Singapore, Kosovo, San Marino, il Vaticano, le Seychelles, il Liechtenstein, il Lussemburgo, Monaco e Vanuatu sono troppo piccoli per essere colorati a questa scala, e la <strong>Lettonia</strong> non è proprio disegnata nella mappa d'origine: nel conteggio ci sono, sulla cartina no.</div>
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
            <div class="pp-nome">Manu <span class="pp-conto">64<span class="pp-conto-lab">paesi</span></span></div>
            <div class="paesi-fatti">
              <span class="paese-fatto"><span class="pf-flag">🇭🇰</span><span class="pf-nome">Hong Kong</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇴</span><span class="pf-nome">Macao</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇹🇼</span><span class="pf-nome">Taiwan</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇨🇳</span><span class="pf-nome">Cina</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇰🇷</span><span class="pf-nome">Corea del Sud</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇯🇵</span><span class="pf-nome">Giappone</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇻🇳</span><span class="pf-nome">Vietnam</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇱🇦</span><span class="pf-nome">Laos</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇰🇭</span><span class="pf-nome">Cambogia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇹🇭</span><span class="pf-nome">Thailandia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇸🇬</span><span class="pf-nome">Singapore</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇾</span><span class="pf-nome">Malesia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇮🇩</span><span class="pf-nome">Indonesia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇵🇭</span><span class="pf-nome">Filippine</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇶🇦</span><span class="pf-nome">Qatar</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇦🇪</span><span class="pf-nome">Emirati Arabi</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇦🇺</span><span class="pf-nome">Australia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇳🇿</span><span class="pf-nome">Nuova Zelanda</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇫🇯</span><span class="pf-nome">Figi</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇻🇺</span><span class="pf-nome">Vanuatu</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇺🇸</span><span class="pf-nome">Stati Uniti</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇽</span><span class="pf-nome">Messico</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇬🇹</span><span class="pf-nome">Guatemala</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇨🇴</span><span class="pf-nome">Colombia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇻🇪</span><span class="pf-nome">Venezuela</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇦🇷</span><span class="pf-nome">Argentina</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇦</span><span class="pf-nome">Marocco</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇪🇬</span><span class="pf-nome">Egitto</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇮🇹</span><span class="pf-nome">Italia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇻🇦</span><span class="pf-nome">Vaticano</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇸🇲</span><span class="pf-nome">San Marino</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇨</span><span class="pf-nome">Monaco</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇱🇮</span><span class="pf-nome">Liechtenstein</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇨🇭</span><span class="pf-nome">Svizzera</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇦🇹</span><span class="pf-nome">Austria</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇩🇪</span><span class="pf-nome">Germania</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇫🇷</span><span class="pf-nome">Francia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇧🇪</span><span class="pf-nome">Belgio</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇱🇺</span><span class="pf-nome">Lussemburgo</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇬🇧</span><span class="pf-nome">Regno Unito</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇮🇪</span><span class="pf-nome">Irlanda</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇵🇹</span><span class="pf-nome">Portogallo</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇬🇷</span><span class="pf-nome">Grecia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇭🇷</span><span class="pf-nome">Croazia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇸🇮</span><span class="pf-nome">Slovenia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇷🇸</span><span class="pf-nome">Serbia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇧🇦</span><span class="pf-nome">Bosnia ed Erzegovina</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇪</span><span class="pf-nome">Montenegro</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇰</span><span class="pf-nome">Macedonia del Nord</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇽🇰</span><span class="pf-nome">Kosovo</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇷🇴</span><span class="pf-nome">Romania</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇩</span><span class="pf-nome">Moldavia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇭🇺</span><span class="pf-nome">Ungheria</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇨🇿</span><span class="pf-nome">Cechia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇸🇰</span><span class="pf-nome">Slovacchia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇵🇱</span><span class="pf-nome">Polonia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇱🇹</span><span class="pf-nome">Lituania</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇱🇻</span><span class="pf-nome">Lettonia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇪🇪</span><span class="pf-nome">Estonia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇫🇮</span><span class="pf-nome">Finlandia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇸🇪</span><span class="pf-nome">Svezia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇳🇴</span><span class="pf-nome">Norvegia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇩🇰</span><span class="pf-nome">Danimarca</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇹🇷</span><span class="pf-nome">Turchia</span></span>
            </div>
          </div>

          <div class="persona-paesi reveal">
            <div class="pp-nome">Mala <span class="pp-conto">26<span class="pp-conto-lab">paesi</span></span></div>
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
              <span class="paese-fatto"><span class="pf-flag">🇲🇩</span><span class="pf-nome">Moldavia</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇰</span><span class="pf-nome">Macedonia del Nord</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇽🇰</span><span class="pf-nome">Kosovo</span></span>
              <span class="paese-fatto"><span class="pf-flag"><svg viewBox="0 0 1200 600" width="24" height="12" role="img" aria-label="Bandiera della Transnistria" style="display:block;border-radius:2px;"><path fill="#de0000" d="M0 0h1200v600H0z"/><path fill="#093" d="M0 225h1200v150H0z"/><path fill="gold" d="m150 30-6.735 20.73h-21.797l17.634 12.81-6.736 20.73L150 71.46l17.634 12.812-6.736-20.73 17.633-12.812h-21.796zm0 10.8 4.31 13.267h13.95l-11.285 8.2 4.31 13.266-11.285-8.2-11.285 8.2 4.31-13.267-11.285-8.2h13.95z"/><g fill="gold"><path d="m101.839 138.547 14.93 14.993 14.078-13.945c21.415 22.909 43.877 44.991 65.126 67.988a8.22 8.22 0 0 0 11.603.04 8.168 8.168 0 0 0 .04-11.573c-22.808-21.463-45.687-43.102-68.502-64.644l18.967-18.787-26.388-3.644z"/><path d="M150 90c12.281 6.899 21.606 16.8 27.106 27.15 5.575 10.49 8.025 21.44 8.075 30.197.104 17.953-14.592 32.508-32.593 32.508-9.605 0-18.24-4.143-24.205-10.736l-3.3 2.77a4.931 4.931 0 0 0-5.519 1.412 6.181 6.181 0 0 0-5.069 4.178c-2.48 4.964-6.834 8.857-12.102 10.64-.05.017-.095.039-.139.061-2.436.89-4.877 2.498-6.956 4.58-4.11 4.134-6.117 9.423-4.987 13.135-.111.322-.169.66-.17 1.002a3.107 3.107 0 0 0 4.36 2.838c3.715.835 8.76-1.22 12.706-5.178 2.237-2.25 3.913-4.913 4.735-7.524 1.834-5.228 5.776-9.487 10.782-11.882.12-.058.216-.117.303-.177a6.173 6.173 0 0 0 3.344-4.116c7.678 9.035 19.194 14.804 32.068 15.106 23.612.554 41.261-16.781 42.077-41.709.411-12.545-4.455-28.721-15.545-41.988C176.496 102.127 164.07 93.71 150 90z"/></g></svg></span><span class="pf-nome">Transnistria</span></span>
            </div>
          </div>

          <div class="persona-paesi reveal">
            <div class="pp-nome">Bacci <span class="pp-conto">31<span class="pp-conto-lab">paesi</span></span></div>
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
              <span class="paese-fatto"><span class="pf-flag">🇲🇰</span><span class="pf-nome">Macedonia del Nord</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇽🇰</span><span class="pf-nome">Kosovo</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇭🇺</span><span class="pf-nome">Ungheria</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇷🇴</span><span class="pf-nome">Romania</span></span>
              <span class="paese-fatto"><span class="pf-flag">🇲🇩</span><span class="pf-nome">Moldavia</span></span>
              <span class="paese-fatto"><span class="pf-flag"><svg viewBox="0 0 1200 600" width="24" height="12" role="img" aria-label="Bandiera della Transnistria" style="display:block;border-radius:2px;"><path fill="#de0000" d="M0 0h1200v600H0z"/><path fill="#093" d="M0 225h1200v150H0z"/><path fill="gold" d="m150 30-6.735 20.73h-21.797l17.634 12.81-6.736 20.73L150 71.46l17.634 12.812-6.736-20.73 17.633-12.812h-21.796zm0 10.8 4.31 13.267h13.95l-11.285 8.2 4.31 13.266-11.285-8.2-11.285 8.2 4.31-13.267-11.285-8.2h13.95z"/><g fill="gold"><path d="m101.839 138.547 14.93 14.993 14.078-13.945c21.415 22.909 43.877 44.991 65.126 67.988a8.22 8.22 0 0 0 11.603.04 8.168 8.168 0 0 0 .04-11.573c-22.808-21.463-45.687-43.102-68.502-64.644l18.967-18.787-26.388-3.644z"/><path d="M150 90c12.281 6.899 21.606 16.8 27.106 27.15 5.575 10.49 8.025 21.44 8.075 30.197.104 17.953-14.592 32.508-32.593 32.508-9.605 0-18.24-4.143-24.205-10.736l-3.3 2.77a4.931 4.931 0 0 0-5.519 1.412 6.181 6.181 0 0 0-5.069 4.178c-2.48 4.964-6.834 8.857-12.102 10.64-.05.017-.095.039-.139.061-2.436.89-4.877 2.498-6.956 4.58-4.11 4.134-6.117 9.423-4.987 13.135-.111.322-.169.66-.17 1.002a3.107 3.107 0 0 0 4.36 2.838c3.715.835 8.76-1.22 12.706-5.178 2.237-2.25 3.913-4.913 4.735-7.524 1.834-5.228 5.776-9.487 10.782-11.882.12-.058.216-.117.303-.177a6.173 6.173 0 0 0 3.344-4.116c7.678 9.035 19.194 14.804 32.068 15.106 23.612.554 41.261-16.781 42.077-41.709.411-12.545-4.455-28.721-15.545-41.988C176.496 102.127 164.07 93.71 150 90z"/></g></svg></span><span class="pf-nome">Transnistria</span></span>
            </div>
          </div>

          <div class="persona-paesi reveal">
            <div class="pp-nome">Kiki <span class="pp-conto">31<span class="pp-conto-lab">paesi</span></span></div>
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

stato_per_suf = {d["suf"]: d["stato"] for d in DESTS}
# Sul telefono le quattro linguette devono starci tutte: nomi corti.
CORTI = {"is": "Islanda", "kr": "Corea", "nx": "Il prossimo?", "pb": "Sudamerica"}
def linguetta(b):
    return (f'<button class="switch-btn{" confermato" if stato_per_suf[b["suf"]] == "confermato" else ""}"'
            f' data-dest="{b["suf"]}" onclick="showDest(\'{b["suf"]}\')"><span class="lungo">{b["name"]}</span><span class="corto">{CORTI.get(b["suf"], b["name"])}</span></button>')

# Le linguette in due gruppi: i viaggi da fare e quelli gia' fatti, con
# un'etichetta scritta a mano davanti a ciascun gruppo.
def gruppo(etichetta, descrizione, elenco):
    if not elenco:
        return ''
    return (f'<div class="sw-gruppo" role="group" aria-label="{descrizione}">'
            f'<span class="sw-etichetta" aria-hidden="true">{etichetta}</span>'
            + ''.join(linguetta(b) for b in elenco) + '</div>')

switcher_buttons = '\n  '.join(filter(None, [
    gruppo("da fare", "Viaggi da fare", [b for b in blocks if stato_per_suf[b["suf"]] != "fatto"]),
    gruppo("fatti", "Viaggi fatti", [b for b in blocks if stato_per_suf[b["suf"]] == "fatto"]),
]))


suffissi_js = json.dumps(["hub"] + [d["suf"] for d in DESTS], ensure_ascii=False)
titoli_js = json.dumps({"hub": "Tutte le mete", **{d["suf"]: d["name"] for d in DESTS}}, ensure_ascii=False)

# ----------------------------------------------------------------------
# La copertina: la schermata d'ingresso.
#
# Il quaderno chiuso, con stampato in copertina il logo dei Patagucci: il
# cielo verde, la banda rossa, le montagne nere con la cresta bianca, la
# scritta e l'aereo Royal Brunico. Il logo viene dal progetto
# "menu cena kiki/logo-animato": cielo, banda e aereo sono i suoi livelli
# (in assets/logo/), montagne, cresta e lettere sono ridisegnate in
# vettoriale dai suoi contorni (_sources/logo/forme.json), cosi' restano
# nitide a qualsiasi grandezza.
#
# All'apertura il logo si stampa da solo, a colpi, come un manifesto: il
# cielo, la banda, le montagne con la cresta, la scritta; poi l'aereo entra
# in volo e compare "Entra" (lo fa il CSS). Premendo "Entra" l'aereo si
# stacca dal logo e vola verso lo schermo, una nuvola bianca copre tutto e
# diventa il foglio a quadretti; lo stesso aereo Royal Brunico rientra da
# sinistra, piccolo, tracciando la scia a pennarello, e si posa accanto al
# titolo della home, dove resta con la sua scia (assets/anima.js).
# La decide lo script in testa alla pagina, prima che si veda qualcosa:
# chi arriva sulla home da zero la trova, chi apre un link a una meta o a
# una sezione va dritto li', e nella stessa scheda la si vede una volta
# sola. Senza JavaScript non compare affatto.
# ----------------------------------------------------------------------
with open(SRC_DIR + "logo/forme.json", encoding="utf-8") as _f:
    LOGO = json.load(_f)


def disegna_logo():
    """Montagne, cresta e lettere del logo come tracciati SVG, in pixel del disegno."""
    W = LOGO["larghezza"]
    # La cresta continua oltre i bordi ripetuta a specchio, come nel logo
    # animato: sugli schermi larghi le montagne non finiscono di colpo.
    lunga = []
    for k in (-1, 0, 1):
        pezzo = [(x + k * W, y) if k % 2 == 0 else ((k + 1) * W - x, y) for x, y in LOGO["linea"]]
        if k % 2:
            pezzo.reverse()
        for x, y in pezzo:
            if not lunga or x - lunga[-1][0] > 0.5:
                lunga.append((x, y))
    n = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")
    tratto = lambda punti: "M" + " L".join(f"{n(x)} {n(y)}" for x, y in punti)
    monti = " ".join(f"{n(x)},{n(y)}" for x, y in lunga) + f" {n(lunga[-1][0])},4000 {n(lunga[0][0])},4000"
    # La cresta si disegna dalla vetta piu' alta verso i due lati.
    vetta = min((i for i, (x, y) in enumerate(lunga) if 0 <= x <= W), key=lambda i: lunga[i][1])
    cresta = (tratto(lunga[vetta::-1]), tratto(lunga[vetta:]))
    # Ogni lettera nel suo riquadro, cosi' puo' spuntare per conto suo.
    lettere = []
    for forme in LOGO["lettere"]:
        punti = [p for forma in forme for p in forma["esterno"]]
        x0, y0 = min(p[0] for p in punti) - 2, min(p[1] for p in punti) - 2
        x1, y1 = max(p[0] for p in punti) + 2, max(p[1] for p in punti) + 2
        d = "".join(tratto(c) + "Z" for forma in forme for c in [forma["esterno"]] + forma["buchi"])
        lettere.append({"d": d, "vb": f"{n(x0)} {n(y0)} {n(x1 - x0)} {n(y1 - y0)}",
                        "stile": f"left:{x0 / W * 100:.3f}%;top:{y0 / LOGO['altezza'] * 100:.3f}%;"
                                 f"width:{(x1 - x0) / W * 100:.3f}%;height:{(y1 - y0) / LOGO['altezza'] * 100:.3f}%"})
    return monti, cresta, lettere


_monti, _cresta, _lettere = disegna_logo()
# Montagne, cresta e lettere stanno in tavole uguali, cosi' ognuna puo'
# muoversi per conto suo nell'intro: montagne e cresta salgono insieme, le
# lettere arrivano dopo, come un timbro.
_TAVOLA = 'viewBox="-1000 360 3672 3640" preserveAspectRatio="none" focusable="false"'

# La canzone dei Patagucci. Parte con la copertina e continua dentro il
# sito; dentro, il tasto in basso a destra la spegne e la riaccende. Sulla
# copertina il tasto non c'e': sta sotto, e si raggiunge solo entrando. Il
# tasto e la canzone vivono fuori dalla copertina, cosi' ci sono anche a
# chi arriva da un link diretto (senza copertina): li' la canzone aspetta
# il tasto, perche' il browser non la lascerebbe partire da sola.
musica_html = """<div class="musica-giro"><button type="button" class="musica" id="musica"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M9 17.4 C 9.2 13, 8.8 9, 9 5.2 L 19.2 2.8 C 19 7, 19.3 11, 19 15.2"/><ellipse cx="6.5" cy="17.6" rx="2.7" ry="2.1"/><ellipse cx="16.6" cy="15.4" rx="2.7" ry="2.1"/></svg><span class="musica-scritta">Accendi la musica</span></button></div>
<script>
  (function(){
    var tasto = document.getElementById('musica');
    var scritta = tasto.querySelector('span');
    // Non la si scarica in anticipo: sono 3,9 MB, e su una rete lenta
    // toglievano la strada agli script del volo. Si comincia a scaricarla
    // solo quando suona.
    var canzone = new Audio();
    canzone.preload = 'none';
    canzone.loop = true;
    canzone.src = 'assets/audio/patagucci-song.mp3';
    // Il tasto dice quello che fa ("Accendi" o "Spegni"): una scritta
    // sola, senza un secondo stato "premuto" che il lettore di schermo
    // annuncerebbe insieme e al contrario.
    function segna(){
      var accesa = !canzone.paused;
      tasto.classList.toggle('accesa', accesa);
      scritta.textContent = accesa ? 'Spegni la musica' : 'Accendi la musica';
    }
    canzone.addEventListener('play', segna);
    canzone.addEventListener('pause', segna);
    function suona(){
      var p = canzone.play();
      if(p && p.then) p.then(segna, segna);
    }
    tasto.addEventListener('click', function(){
      if(canzone.paused) suona(); else canzone.pause();
    });
    window.PatagucciMusica = {
      suona: function(){ if(canzone.paused) suona(); },
      // Mentre parla uno di noi (le foto del gruppo) la canzone si abbassa.
      abbassa: function(si){ canzone.volume = si ? 0.2 : 1; }
    };
  })();
</script>"""

copertina_testa = """<script>
  // Ricaricando si riparte dalla home. L'indirizzo di una meta ("#kr")
  // serve a mandarla a qualcuno e a tornarci con Indietro, non a restarci
  // dopo un aggiornamento. Gira per primo, prima che qualcuno legga
  // l'indirizzo; e la pagina riparte dalla cima, non dal punto della meta.
  (function(){
    try {
      var nav = performance.getEntriesByType && performance.getEntriesByType('navigation')[0];
      var ricarica = nav ? nav.type === 'reload' : (performance.navigation && performance.navigation.type === 1);
      if(!ricarica || !location.hash) return;
      history.replaceState(null, '', location.pathname + location.search);
      if('scrollRestoration' in history) history.scrollRestoration = 'manual';
    } catch(e){}
  })();
</script>
<script>
  (function(){
    var radice = document.documentElement;
    var mostra = !location.hash;
    try { if(sessionStorage.getItem('patagucci-entrato')) mostra = false; } catch(e){}
    if(!mostra) return;
    radice.classList.add('con-copertina');
    // Il logo si stampa da solo all'apertura; con meno movimento e' gia'
    // intero, e "Entra" c'e' da subito.
    if(!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) radice.classList.add('copertina-intro');
  })();
</script>"""

copertina_html = """<div class="copertina" id="copertina" role="dialog" aria-modal="true" aria-labelledby="cp-titolo">
  <div class="cp-anta">
    <p class="sr-only" id="cp-titolo">Patagucci Trips</p>
    <div class="pl" aria-hidden="true">
      <div class="pl-cielo"><img src="assets/logo/cielo.webp" alt="" width="1672" height="941" decoding="async" fetchpriority="high"></div>
      <div class="pl-rossa"><img src="assets/logo/rossa.webp" alt="" width="1672" height="162" decoding="async"></div>
      <div class="pl-terra pl-monti"><svg """ + _TAVOLA + """><polygon points=\"""" + _monti + """\"/></svg></div>
      <div class="pl-terra pl-cresta"><svg """ + _TAVOLA + """><path d=\"""" + _cresta[0] + """\"/><path d=\"""" + _cresta[1] + """\"/></svg></div>
      <div class="pl-lettere">""" + "".join(f'<div class="pl-l" style="{l["stile"]}"><svg viewBox="{l["vb"]}" focusable="false"><path d="{l["d"]}"/></svg></div>' for l in _lettere) + """</div>
      <div class="pl-aereo"><img src="assets/logo/aereo.webp" alt="" width="342" height="85" decoding="async"></div>
    </div>
    <div class="cp-dorso" aria-hidden="true"></div>
    <div class="cp-basso" inert><span class="cp-entra-giro"><button type="button" class="cp-entra" id="cp-entra">Entra <svg viewBox="0 0 40 20" aria-hidden="true" focusable="false"><path d="M2 11 C 13 7, 25 13, 36 9 M29 3 L37 9 L30 16"/></svg></button></span></div>
  </div>
  <div class="cp-foglio" aria-hidden="true"><div class="cp-carta"></div><i class="cp-righe cp-righe-o"></i><i class="cp-righe cp-righe-v"></i></div>
  <div class="cp-volo" aria-hidden="true"><svg focusable="false">
    <defs><mask id="cp-maschera-volo" maskUnits="userSpaceOnUse" x="-1000" y="-1000" width="8000" height="8000"><path class="cp-scopri" pathLength="1"/></mask></defs>
    <path class="cp-scia" mask="url(#cp-maschera-volo)"/>
    <g class="cp-aeroplanino" transform="translate(-300 -300)"><image href="assets/logo/aereo.webp" x="-70" y="-17.4" width="140" height="34.8"/></g>
  </svg></div>
</div>
<script>
  (function(){
    var radice = document.documentElement;
    var copertina = document.getElementById('copertina');
    if(!radice.classList.contains('con-copertina')){ copertina.remove(); return; }

    var entra = document.getElementById('cp-entra');
    var basso = copertina.querySelector('.cp-basso');
    var spenti = [];
    var chiusa = false;
    var daTastiera = false;
    var volo = null, tApri = 0, suRidimensiona = null;

    // ---- L'intro del logo ----
    // La fa il CSS, ma aspetta le immagini del logo: senza, il cielo si
    // "stamperebbe" vuoto. "Entra" diventa premibile, e prende il fuoco,
    // quando ha finito di comparire: fino ad allora e' inerte, cosi' il tab
    // non raggiunge un bottone che ancora non si vede. Aspetta anche, per
    // poco, lo script del volo: su una rete lenta, premendo prima che
    // arrivi, si avrebbe solo la dissolvenza di riserva. Con meno
    // movimento e' tutto pronto da subito.
    var attesa = 0;
    function pronta(){
      if(copertina.classList.contains('pronta')) return;
      if(!window.PatagucciAnima && radice.classList.contains('copertina-intro')){
        attesa = attesa || Date.now();
        if(Date.now() - attesa < 2500){ setTimeout(pronta, 100); return; }
      }
      copertina.classList.add('via', 'pronta');
      basso.inert = false;
      try { entra.focus({ preventScroll:true }); } catch(e){ entra.focus(); }
    }
    if(radice.classList.contains('copertina-intro')){
      // La fine dell'animazione di "Entra" dice quando e' pronta: i tempi
      // stanno solo nel CSS. Il timer e' una rete, se l'animazione non
      // arrivasse alla fine (scheda in secondo piano).
      basso.addEventListener('animationend', function(e){ if(e.animationName === 'cpAppare') pronta(); });
      var parti = function(){
        if(copertina.classList.contains('via')) return;
        copertina.classList.add('via');
        setTimeout(pronta, 5000);
      };
      Promise.all(Array.prototype.map.call(copertina.querySelectorAll('.pl img'), function(img){
        return img.decode ? img.decode().catch(function(){}) : null;
      })).then(parti, parti);
      // se le immagini tardano, l'intro parte comunque
      setTimeout(parti, 1500);
    } else {
      pronta();
    }

    // ---- La canzone dei Patagucci ----
    // Il tasto e la canzone stanno fuori dalla copertina (musica_html,
    // qui sopra): qui la si fa solo partire. Molti browser non
    // lasciano partire un suono da solo: allora parte al primo tocco sulla
    // copertina, anche quello su "Entra", e da li' continua dentro il sito.
    var musica = window.PatagucciMusica;
    function suona(){ if(musica && !chiusa) musica.suona(); }
    // Un tocco sulla copertina accende la canzone, se il browser l'aveva
    // fermata, e porta l'intro alla fine: chi tocca ha gia' voglia di
    // entrare. La tastiera invece non accende niente: chi usa il tab o un
    // lettore di schermo non deve trovarsi la musica sopra la voce, e
    // dentro il sito ha il tasto per accenderla.
    copertina.addEventListener('pointerdown', function(){
      suona();
      if(copertina.classList.contains('via') && !copertina.classList.contains('pronta')){ copertina.classList.add('salta'); pronta(); }
    });

    // Mentre la copertina e' chiusa il resto della pagina non si raggiunge
    // ne' col tab ne' col lettore di schermo. Ogni pezzo si blocca appena
    // il browser lo aggiunge, senza aspettare la fine: su una rete lenta la
    // pagina arriva dopo che "Entra" e' gia' pronto, e il tab ci finirebbe.
    function blocca(el){
      if(el.nodeType !== 1 || el === copertina || el.tagName === 'SCRIPT' || el.inert) return;
      el.inert = true;
      spenti.push(el);
    }
    Array.prototype.forEach.call(document.body.children, blocca);
    var guardia = window.MutationObserver ? new MutationObserver(function(liste){
      liste.forEach(function(l){ Array.prototype.forEach.call(l.addedNodes, blocca); });
    }) : null;
    if(guardia) guardia.observe(document.body, { childList: true });
    // A pagina pronta sono arrivati anche gli script del volo: solo allora
    // parte la canzone.
    document.addEventListener('DOMContentLoaded', function(){
      if(guardia) guardia.disconnect();
      if(chiusa) return;
      Array.prototype.forEach.call(document.body.children, blocca);
      suona();
    });

    function chiudi(){
      if(chiusa) return;
      chiusa = true;
      try { sessionStorage.setItem('patagucci-entrato', '1'); } catch(e){}
      if(guardia) guardia.disconnect();
      spenti.forEach(function(el){ el.inert = false; });
      radice.classList.remove('con-copertina', 'copertina-intro');
      copertina.remove();
      // Niente resta in ascolto per una copertina che non c'e' piu'.
      document.removeEventListener('keydown', suEsc);
      if(suRidimensiona) window.removeEventListener('resize', suRidimensiona);
      // assets/anima.js rimette in osservazione quello che aspettava.
      window.dispatchEvent(new CustomEvent('copertina-chiusa'));
      // Chi e' entrato con la tastiera riparte dal titolo; col mouse o col
      // dito il fuoco torna semplicemente all'inizio della pagina.
      var titolo = daTastiera && document.querySelector('#dest-hub h1');
      if(titolo){
        titolo.setAttribute('tabindex', '-1');
        titolo.addEventListener('blur', function(){ titolo.removeAttribute('tabindex'); }, { once:true });
        try { titolo.focus({ preventScroll:true }); } catch(e){}
      }
    }

    // Saltare il volo: la copertina sfuma in un attimo e sotto la home e'
    // gia' pronta. Il volo ferma i suoi tempi, cosi' niente riparte dopo.
    function salta(){
      if(chiusa || copertina.classList.contains('svanisce')) return;
      if(volo && volo.salta) volo.salta();
      copertina.classList.add('svanisce');
      setTimeout(chiudi, 220);
    }

    function apri(e){
      // Un clic da tastiera (Invio, spazio) ha detail 0; Esc non ha evento.
      var tastiera = !e || e.detail === 0;
      if(copertina.classList.contains('in-volo') || copertina.classList.contains('apri-css')){
        // Un secondo colpo vuol dire "salta", ma non quello di un doppio
        // clic fatto per abitudine: conta solo dopo 0,6 secondi.
        if(Date.now() - tApri > 600) salta();
        return;
      }
      daTastiera = tastiera;
      tApri = Date.now();
      if(window.PatagucciCopertina){
        volo = window.PatagucciCopertina.apri(copertina, chiudi);
        // Se la finestra cambia misura (o il telefono gira) a volo in
        // corso, l'atterraggio calcolato non torna piu': meglio saltare.
        var w = window.innerWidth, h = window.innerHeight;
        suRidimensiona = function(){
          if(Math.abs(window.innerWidth - w) > 40 || Math.abs(window.innerHeight - h) > 40) salta();
        };
        window.addEventListener('resize', suRidimensiona);
        return;
      }
      // Senza Motion (o con meno movimento) la copertina sfuma e basta.
      var meno = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      copertina.classList.add('apri-css');
      setTimeout(chiudi, meno ? 300 : 650);
    }

    // Durante l'intro Esc la fa finire; a copertina pronta entra; durante
    // il volo lo salta.
    function suEsc(e){
      if(chiusa || e.key !== 'Escape') return;
      if(!copertina.classList.contains('pronta')){ copertina.classList.add('salta'); pronta(); }
      else if(copertina.classList.contains('in-volo')) salta();
      else apri();
    }

    entra.addEventListener('click', apri);
    document.addEventListener('keydown', suEsc);
  })();
</script>"""


final_html = f'''<!DOCTYPE html>
<html lang="it" data-dest="hub">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Patagucci Trips</title>
<link rel="icon" href="assets/icona.svg" type="image/svg+xml">
<link rel="icon" href="assets/icona-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/icona-180.png">
{copertina_testa}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Patrick+Hand+SC&family=Atkinson+Hyperlegible+Next:ital,wght@0,400;0,600;0,700;0,800;1,400&family=Atkinson+Hyperlegible+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<!-- Motion (gia' Framer Motion), la versione senza React: il volo della
     copertina, la pagina che si volta, l'evidenziatore, la penna rossa.
     E' una copia del pacchetto ufficiale motion@11.11.17 (dist/motion.js,
     sha256 61b3a38dabf65a31778bc7fa9e71936bfa36ec2f567e50de261b958a3037e84e,
     licenza MIT in assets/vendor/motion-LICENSE.md): servito da qui non
     dipende da un sito esterno e non si puo' alterare per strada. Tutti e
     due gli script stanno in testa, rimandati: si scaricano subito, prima
     delle foto e della canzone, e girano a pagina letta. Se non arrivano,
     assets/anima.js se ne accorge e la pagina resta ferma e intera. -->
<script src="assets/vendor/motion-11.11.17.js" defer fetchpriority="high"></script>
<script src="assets/anima.js" defer fetchpriority="high"></script>
<style>
  .destination{{ display:none; }}
  .destination.active{{ display:block; }}
  /* Le linguette del quaderno: una riga sola che scorre, a qualsiasi
     larghezza. Andando a capo mangiavano un terzo dello schermo sul
     telefono. I due margin:auto la tengono centrata quando ci sta e non
     rendono irraggiungibile la prima linguetta quando invece scorre. */
  .site-switcher{{
    position:sticky; top:0; z-index:200;
    display:flex; gap:4px; justify-content:flex-start; flex-wrap:nowrap;
    overflow-x:auto; -webkit-overflow-scrolling:touch; scrollbar-width:none;
    background:var(--paper) var(--riga-mano) repeat-x 0 100% / 240px 9px;
    padding:9px 12px 12px;
  }}
  .site-switcher::-webkit-scrollbar{{ display:none; }}
  .site-switcher > :first-child{{ margin-left:auto; }}
  .site-switcher > :last-child{{ margin-right:auto; }}
  /* Da fare | fatti: un trattino a matita fra i gruppi, e davanti a
     ciascuno la sua etichetta scritta a mano. */
  .sw-gruppo{{ flex:0 0 auto; display:flex; align-items:center; gap:4px; }}
  .sw-gruppo::before{{
    content:""; flex:0 0 auto; width:2px; height:22px; margin:0 8px 0 6px;
    background:var(--ink-soft); border-radius:2px; transform:rotate(8deg);
  }}
  .sw-etichetta{{ font-family:var(--font-hand); font-size:0.95rem; letter-spacing:0.03em; color:var(--ink-soft); padding:0 2px 0 0; white-space:nowrap; }}
  /* Ogni linguetta ha il suo evidenziatore: un trattino sotto la scritta
     quando e' chiusa, la passata intera dietro le lettere quando e'
     aperta. Il trattino sta sotto, non dietro: il grigio matita sopra
     il rosa scendeva a 3,3:1. */
  .site-switcher button{{
    --dab:#ffe14d;
    flex:0 0 auto; white-space:nowrap; cursor:pointer;
    font-family:var(--font-display); font-size:1.08rem; line-height:1.2; letter-spacing:0.01em;
    color:var(--ink-soft); background-color:transparent; border:0; border-radius:6px;
    padding:8px 13px 9px;
    background-image:var(--evid-grana), linear-gradient(var(--dab), var(--dab));
    background-repeat:no-repeat; background-position:6px 76%, 13px 100%; background-size:0 0, 22px 5px;
    transition:color .2s ease, background-size .4s cubic-bezier(.16,1,.3,1), background-position .4s cubic-bezier(.16,1,.3,1);
  }}
  .site-switcher button[data-dest="is"]{{ --dab:#7deaa0; }}
  .site-switcher button[data-dest="kr"]{{ --dab:#ff92bb; }}
  .site-switcher button[data-dest="nx"]{{ --dab:#6de6d2; }}
  .site-switcher button[data-dest="pb"]{{ --dab:#ffab70; }}
  .site-switcher button:hover{{ color:var(--ink); background-size:0 0, calc(100% - 26px) 5px; }}
  .site-switcher button.active{{ color:var(--ink); background-position:6px 76%, 6px 76%; background-size:calc(100% - 12px) 0.6em, calc(100% - 12px) 0.6em; }}
  .site-switcher .corto{{ display:none; }}
  @media (max-width:760px){{
    .site-switcher{{ padding:6px 8px 10px; }}
    .site-switcher button{{ padding:10px 11px 9px; font-size:1rem; min-height:44px; }}
  }}
  @media (max-width:600px){{
    .site-switcher .lungo{{ display:none; }}
    .site-switcher .corto{{ display:inline; }}
    .site-switcher button{{ padding:10px 6px 9px; }}
    /* Sul telefono tutte le linguette devono stare nello schermo: restano
       i trattini fra i gruppi, le etichette scritte no. */
    .sw-gruppo::before{{ margin:0 4px 0 2px; }}
    .sw-etichetta{{ position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; }}
  }}
</style>
</head>
<body>

{musica_html}

{copertina_html}

<div class="site-switcher" id="site-switcher">
  <button class="home-btn active" data-dest="hub" onclick="showDest('hub')">Home</button>
  {switcher_buttons}
</div>

{hub_html}

{destination_blocks}

<script>
var SUFFISSI = {suffissi_js};
var TITOLI = {titoli_js};
// Il frammento gia' messo in pagina: popstate e hashchange arrivano tutti
// e due per lo stesso salto, e il secondo deve trovarlo gia' fatto.
var ultimoFrammento = null;
var ridottoMovimento = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function showDest(name, daCronologia){{
  var prima = document.documentElement.getAttribute('data-dest');
  var cambia = prima !== name;
  document.documentElement.setAttribute('data-dest', name);
  if(cambia) document.documentElement.removeAttribute('data-paese');
  document.querySelectorAll('.destination').forEach(function(el){{ el.classList.remove('active'); }});
  var target = document.getElementById(name === 'hub' ? 'dest-hub' : 'dest-' + name);
  if(target) target.classList.add('active');
  document.querySelectorAll('#site-switcher button').forEach(function(b){{ b.classList.remove('active'); }});
  var btn = document.querySelector('#site-switcher button[data-dest="' + name + '"]');
  if(btn){{
    btn.classList.add('active');
    // Su mobile il selettore e' una riga che scorre: senza questo la meta
    // attiva puo' restare fuori schermo.
    btn.scrollIntoView({{ behavior: ridottoMovimento ? 'auto' : 'smooth', block:'nearest', inline:'center' }});
  }}
  // Una meta nuova si legge dall'inizio; la linguetta della meta gia'
  // aperta riporta in cima, ma senza voltare pagina.
  window.scrollTo({{ top: 0, left: 0, behavior: 'instant' }});
  target.querySelectorAll('.reveal').forEach(function(el){{ el.classList.add('visible'); }});
  // Un indirizzo per ogni meta: senza questo "guarda i voli" diventa
  // "apri il sito, clicca Corea, scorri fino in fondo", ogni volta.
  document.title = (TITOLI[name] ? TITOLI[name] + ' — ' : '') + 'Patagucci Trips';
  if(!daCronologia){{
    var nuovo = name === 'hub' ? location.pathname : location.pathname + '#' + name;
    if(location.hash.slice(1) !== name) history.pushState({{ meta: name }}, '', nuovo);
  }}
  ultimoFrammento = location.hash;
  // Solo quando la meta cambia davvero: assets/anima.js volta la pagina
  // (in avanti o indietro, secondo l'ordine delle linguette) e le cartine
  // della meta nuova ripartono.
  if(cambia) window.dispatchEvent(new CustomEvent('destinazione-cambiata', {{ detail: {{ da: prima, a: name }} }}));
  if(typeof syncSwitcherHeight === 'function') setTimeout(syncSwitcherHeight, 0);
}}
function showHub(){{ showDest('hub'); }}

// ---- L'indirizzo dice dove sei, e ci si torna ----
// Le sezioni hanno id col suffisso della meta ("#voli-kr"), quindi dal
// frammento si ricava sia la meta sia il punto della pagina.
function metaDaFrammento(frammento){{
  if(!frammento) return null;
  if(SUFFISSI.indexOf(frammento) !== -1) return {{ meta: frammento, sezione: null }};
  var taglio = frammento.lastIndexOf('-');
  if(taglio > 0){{
    var suf = frammento.slice(taglio + 1);
    if(SUFFISSI.indexOf(suf) !== -1) return {{ meta: suf, sezione: frammento }};
  }}
  return null;
}}
function applicaFrammento(daCronologia){{
  // Lo stesso salto annunciato due volte (popstate e poi hashchange): il
  // secondo lo trova gia' fatto e non fa niente.
  if(location.hash === ultimoFrammento) return;
  ultimoFrammento = location.hash;
  var trovato = metaDaFrammento(location.hash.slice(1));
  if(!trovato){{ showDest('hub', true); return; }}
  // Una sezione della meta gia' aperta e' solo un salto dentro la pagina:
  // lo fa il browser, senza voltare pagina e senza passare dalla cima.
  if(trovato.sezione && trovato.meta === document.documentElement.getAttribute('data-dest')) return;
  showDest(trovato.meta, true);
  if(trovato.sezione){{
    var el = document.getElementById(trovato.sezione);
    // Sempre secco: la meta e' appena cambiata, quindi non c'e' niente da
    // seguire con lo sguardo. Scendere piano per ventimila pixel di una
    // pagina che non si stava guardando fa solo perdere l'orientamento.
    if(el) setTimeout(function(){{ el.scrollIntoView({{ behavior:'instant', block:'start' }}); }}, 60);
  }}
}}
window.addEventListener('popstate', function(){{ applicaFrammento(true); }});
window.addEventListener('hashchange', function(){{ applicaFrammento(true); }});
document.addEventListener('DOMContentLoaded', function(){{ if(location.hash) applicaFrammento(false); }});

// Una meta che attraversa piu' paesi tinge la pagina col paese che si sta
// guardando: la scheda chiama questa passando il paese ('bn', 'sg'),
// oppure niente per tornare all'evidenziatore della meta.
function tingiPaese(paese){{
  var radice = document.documentElement;
  if(paese) radice.setAttribute('data-paese', paese);
  else radice.removeAttribute('data-paese');
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
  // Mentre parla, la canzone si abbassa; torna su quando ha finito.
  var abbassa = function(si){{ if(window.PatagucciMusica) window.PatagucciMusica.abbassa(si); }};
  card.addEventListener('mouseenter', function(){{
    audio.currentTime = 0;
    abbassa(true);
    audio.play().catch(function(){{ abbassa(false); }});
  }});
  card.addEventListener('mouseleave', function(){{
    audio.pause();
    audio.currentTime = 0;
    abbassa(false);
  }});
  audio.addEventListener('ended', function(){{ abbassa(false); }});
}});

// La striscia delle foto del gruppo: ferma, si scorre di lato col dito,
// col mouse o con le due frecce disegnate; col tab prende il fuoco e
// scorre con le frecce della tastiera. Una freccia si spegne quando da
// quella parte non c'e' piu' niente.
(function(){{
  var binario = document.getElementById('striscia-foto');
  if(!binario) return;
  var cornice = binario.parentNode;
  var indietro = cornice.querySelector('.striscia-foto-freccia.indietro');
  var avanti = cornice.querySelector('.striscia-foto-freccia.avanti');
  function aggiorna(){{
    var fine = binario.scrollWidth - binario.clientWidth - 2;
    indietro.disabled = binario.scrollLeft <= 2;
    avanti.disabled = fine <= 0 || binario.scrollLeft >= fine;
  }}
  function sposta(verso){{
    binario.scrollBy({{ left: verso * binario.clientWidth * 0.8, behavior: ridottoMovimento ? 'auto' : 'smooth' }});
  }}
  indietro.addEventListener('click', function(){{ sposta(-1); }});
  avanti.addEventListener('click', function(){{ sposta(1); }});
  binario.addEventListener('scroll', aggiorna, {{ passive: true }});
  window.addEventListener('resize', aggiorna);
  window.addEventListener('load', aggiorna);
  // Aprendo il sito su un'altra meta la striscia non ha ancora misure.
  window.addEventListener('destinazione-cambiata', function(){{ setTimeout(aggiorna, 0); }});
  aggiorna();
}})();
</script>

{"".join(scripts)}

</body>
</html>
'''


# ----------------------------------------------------------------------
# Il taccuino.
#
# Le pagine sorgente sono nate per il vecchio stile: titoli con un'emoji
# davanti, foto delle intestazioni scurite per farci stare sopra il
# testo bianco, pannelli "dark" alternati. Invece di riscriverle tutte,
# le aggiusto qui, nel punto dove vengono montate: cosi' valgono anche
# per le mete archiviate, il giorno che tornano in linea.
# ----------------------------------------------------------------------
EVIDENZIA = {"Patagucci Trips": "Patagucci", "Corea, Brunei e Singapore": "Corea", "Quale sarà il prossimo?": "prossimo"}

EMOJI = (r"(?:[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\u2300-\u23FF]"
         r"[\uFE0F\u200D\U0001F3FB-\U0001F3FF]*)+")

def taccuino(html):
    # Nessuna pagina scura: le "dark" diventano pagine coi quadretti del
    # colore del paese. Le vecchie regole section.panel.dark nei <style>
    # delle sorgenti cosi' non trovano piu' niente a cui applicarsi.
    html = html.replace('class="panel dark"', 'class="panel alt"')

    # Titoli di sezione: via l'emoji davanti, e il testo in uno <span>
    # su cui passare l'evidenziatore una riga alla volta.
    def titolo(m):
        testo = re.sub(r"^\s*" + EMOJI + r"\s*", "", m.group(2))
        return f'{m.group(1)}<span class="tt">{testo}</span></h2>'
    html = re.sub(r'(<h2 class="section-title[^"]*"[^>]*>)(.*?)</h2>', titolo, html, flags=re.S)

    # Il titolo della prima pagina di ogni meta: evidenziata una parola
    # sola, quella che conta. Tutte le righe evidenziate non evidenziano
    # niente.
    def titolo_meta(m):
        testo = m.group(2)
        parola = EVIDENZIA.get(testo.strip()) or testo.split()[0].rstrip(",")
        return m.group(1) + testo.replace(parola, f'<span class="tt">{parola}</span>', 1)
    # Solo il testo del titolo: un disegno dentro l'h1 (l'aeroplanino della
    # home) resta fuori dall'evidenziatore.
    html = re.sub(r'(<header class="hero"[^>]*>.*?<h1>)([^<]*)', titolo_meta, html, flags=re.S)

    # Le emoji davanti ai titoletti e ai link per le mappe facevano da
    # icone: via, il testo basta.
    html = re.sub(r'(<h3\b[^>]*>)\s*' + EMOJI + r'\s*', r'\1', html)
    html = re.sub(r'(class="maps-link"[^>]*>)\s*' + EMOJI + r'\s*', r'\1', html)
    html = re.sub(r'((?:id="link-full-route[^"]*"|class="export"|class="qp-secondario")[^>]*>)\s*' + EMOJI + r'\s*', r'\1', html)
    # Alba e tramonto sulla simulazione del sole: scritti, non disegnini.
    html = html.replace('class="sun-label">🌅 ', 'class="sun-label">alba ').replace('class="sun-label">🌇 ', 'class="sun-label">tramonto ')

    # Sulle cartine le tappe erano emoji: diventano puntine a pennarello,
    # un cerchio evidenziato nello stesso punto.
    def puntina(m):
        x, y, corpo = float(m.group(2)), float(m.group(3)), float(m.group(4))
        return f'{m.group(1)}<circle class="pin" cx="{x:g}" cy="{y - corpo * 0.35:g}" r="{corpo * 0.3:g}"/>'
    html = re.sub(r'(<g class="stop-pin[^"]*">\s*)<text x="([\d.]+)" y="([\d.]+)"[^>]*?font-size="([\d.]+)"[^>]*>[^<]*</text>',
                  puntina, html)

    # La foto dell'intestazione adesso e' una polaroid: niente velo scuro.
    html = re.sub(r'(class="bg" style="background-image:)\s*linear-gradient\((?:[^()]|\([^()]*\))*\)\s*,\s*',
                  r'\1', html)

    # Le etichette scritte a mano non hanno l'emoji davanti, e nemmeno
    # il ritorno alla home nelle linguette.
    html = re.sub(r'(<(?:span|a) class="badge[^"]*"[^>]*>)\s*' + EMOJI + r'\s*', r'\1', html)
    html = re.sub(r'(class="home-link"[^>]*>)\s*' + EMOJI + r'\s*', r'\1', html)
    html = re.sub(r'(<a href="#recap-voli[^"]*">)\s*' + EMOJI + r'\s*', r'\1', html)
    return html

final_html = taccuino(final_html)

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

def controlla_giorni_settimana(schede):
    """I giorni della settimana scritti a mano si sbagliano: "mer 8 apr" era
    in realta' un giovedi', proprio nella tabella che serve a comprare i voli.
    Ogni scheda si confronta col calendario del SUO anno: cercare una
    corrispondenza in un anno qualsiasi non serve, perche' un anno in cui
    l'8 aprile cade di mercoledi' esiste sempre."""
    import re, datetime
    GIORNI = {0:'lun', 1:'mar', 2:'mer', 3:'gio', 4:'ven', 5:'sab', 6:'dom'}
    MESI = {'gen':1,'feb':2,'mar':3,'apr':4,'mag':5,'giu':6,
            'lug':7,'ago':8,'set':9,'ott':10,'nov':11,'dic':12}
    NOMI = ('gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|'
            'agosto|settembre|ottobre|novembre|dicembre')
    sbagliati = []
    for nome, html in schede:
        m = re.search(r'\d{1,2}\s*[–-]\s*\d{1,2}\s+(?:' + NOMI + r')\s+(20\d\d)', html)
        if not m:
            continue
        anno = int(m.group(1))
        for abbrev, giorno, mese in re.findall(
                r'\b(lun|mar|mer|gio|ven|sab|dom)\s+(\d{1,2})\s+'
                r'(gen|feb|mar|apr|mag|giu|lug|ago|set|ott|nov|dic)\b', html):
            try:
                d = datetime.date(anno, MESI[mese], int(giorno))
            except ValueError:
                sbagliati.append('  %s: "%s %s %s" non e\' una data valida nel %d'
                                 % (nome, abbrev, giorno, mese, anno))
                continue
            giusto = GIORNI[d.weekday()]
            if giusto != abbrev:
                sbagliati.append('  %s: scritto "%s %s %s", ma nel %d e\' un %s'
                                 % (nome, abbrev, giorno, mese, anno, giusto))
    if sbagliati:
        print("  Giorni della settimana che non tornano:")
        for s in sbagliati:
            print(s)
        return False
    print("  Giorni della settimana: tornano tutti")
    return True


if not controlla_giorni_settimana([(b["name"], b["block"]) for b in blocks]):
    raise SystemExit("Build interrotta: una data porta il giorno della settimana sbagliato.")

if controlla_javascript(final_html):
    print("  JavaScript: sintassi ok")
else:
    raise SystemExit("Build interrotta: JavaScript non valido nella pagina generata.")
