import re

DIR = "/Users/mattiabacileri/Library/Mobile Documents/com~apple~CloudDocs/progetti/patagucci trip /"
SRC_DIR = DIR + "_sources/"

DESTS = [
    {"file": "nepalbhutan-trip.html", "suf": "np", "flag": "🇳🇵🇧🇹", "name": "Nepal & Bhutan"},
    {"file": "pakistan-trip.html", "suf": "pk", "flag": "🇵🇰", "name": "Pakistan"},
    {"file": "southafrica-trip.html", "suf": "za", "flag": "🇿🇦", "name": "Sudafrica"},
    {"file": "india-trip.html", "suf": "in", "flag": "🇮🇳", "name": "India"},
    {"file": "uganda-trip.html", "suf": "ug", "flag": "🇺🇬", "name": "Uganda"},
    {"file": "tanzania-trip.html", "suf": "tz", "flag": "🇹🇿", "name": "Tanzania"},
    {"file": "uzbekistankyrgyzstan-trip.html", "suf": "uk", "flag": "🇺🇿🇰🇬", "name": "Uzbekistan & Kirghizistan"},
    {"file": "greenland-trip.html", "suf": "gl", "flag": "🇬🇱", "name": "Groenlandia"},
    {"file": "centroamerica-trip.html", "suf": "cx", "flag": "🇳🇮🇨🇷🇵🇦", "name": "Nicaragua, Costa Rica & Panama"},
    {"file": "georgia-trip.html", "suf": "ge", "flag": "🇬🇪", "name": "Georgia"},
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
    <header class="hero" style="min-height:64vh;">
      <div class="bg" style="background-image:linear-gradient(180deg, rgba(10,14,11,0.35) 0%, rgba(10,14,11,0.6) 55%, rgba(10,14,11,0.94) 100%), url('foto/destinazioni/A_land_enclosed_in_Mountains_-_Hunza_Valley.jpg'); background-position:center 55%;"></div>
      <div class="content">
        <h1>Patagucci Trips</h1>
        <p class="tagline">Machu Picchu, un vulcano attivo, Rio, la foresta pluviale di Bwindi — lo stesso gruppo, una meta nuova ogni volta. Qui dentro ci sono tutti i viaggi, con lo stesso livello di dettaglio ossessivo.</p>
        <div class="scroll-cue">↓ scegli la meta</div>
      </div>
    </header>

    <main>
      <section class="panel dark" data-nav>
        <div class="inner">
          <h2 class="section-title reveal">🔥 I Patagucci</h2>
          <p class="section-sub reveal">Machu Picchu, un vulcano attivo, Rio — e ora Uganda, Pakistan, Sudafrica, Nepal e Bhutan. Lo stesso gruppo, una meta nuova ogni volta.</p>
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

          <p class="section-sub reveal" style="margin-top:18px;">Machu Picchu, un vulcano attivo, Rio, la foresta pluviale di Bwindi, la Karakoram Highway — e ora l'Africa australe e l'Himalaya. Direi che siamo pronti per qualsiasi cosa.</p>
        </div>
      </section>

      <section class="panel" data-nav>
        <div class="inner" style="max-width:1060px;">
          <h2 class="section-title reveal">🌍 Tutte le mete</h2>
          <p class="section-sub reveal">Ogni viaggio ha la sua pagina interattiva: itinerario giorno per giorno, mappa animata, meteo storico, convertitore valuta e tutto il resto. Clicca una card per aprirla.</p>

          <div class="trip-grid reveal">
            <a class="trip-card" href="javascript:void(0)" onclick="showDest('np')">
              <img src="foto/destinazioni/The_Tigers_Nest_(_Paro_Taktsang_).jpg" alt="Tiger's Nest Monastery, Bhutan" loading="lazy">
              <div class="overlay"></div>
              <div class="content">
                <div class="flag">🇳🇵🇧🇹</div>
                <div class="title">Nepal &amp; Bhutan</div>
                <div class="meta">Marzo 2027 · 15 giorni</div>
                <p class="tagline">Trekking Poon Hill sull'Annapurna e i dzong del Bhutan.</p>
              </div>
            </a>

            <a class="trip-card" href="javascript:void(0)" onclick="showDest('pk')">
              <img src="foto/destinazioni/Baltit_Fort_(Front_Panorama).jpg" alt="Baltit Fort, Hunza Valley, Pakistan" loading="lazy">
              <div class="overlay"></div>
              <div class="content">
                <div class="flag">🇵🇰</div>
                <div class="title">Pakistan</div>
                <div class="meta">Marzo 2027 · 15 giorni</div>
                <p class="tagline">Lahore, la Karakoram Highway, Hunza Valley e Skardu.</p>
              </div>
            </a>

            <a class="trip-card" href="javascript:void(0)" onclick="showDest('za')">
              <img src="foto/destinazioni/Table_Mountain_from_Blouberg,_South_Africa_(4028515275).jpg" alt="Table Mountain, Cape Town, Sudafrica" loading="lazy">
              <div class="overlay"></div>
              <div class="content">
                <div class="flag">🇿🇦</div>
                <div class="title">Sudafrica</div>
                <div class="meta">Marzo 2027 · 15 giorni</div>
                <p class="tagline">Cape Town, Garden Route e safari Big Five nel Kruger.</p>
              </div>
            </a>

            <a class="trip-card" href="javascript:void(0)" onclick="showDest('in')">
              <img src="foto/destinazioni/Taj_Mahal_Tomb_at_sunrise.JPG" alt="Taj Mahal all'alba, Agra, India" loading="lazy">
              <div class="overlay"></div>
              <div class="content">
                <div class="flag">🇮🇳</div>
                <div class="title">India</div>
                <div class="meta">Marzo 2027 · 14 giorni</div>
                <p class="tagline">Triangolo d'Oro, safari delle tigri a Ranthambore e il Gange a Varanasi.</p>
              </div>
            </a>

            <a class="trip-card" href="javascript:void(0)" onclick="showDest('ug')">
              <img src="foto/destinazioni/Silverback.JPG" alt="Gorilla di montagna, Uganda" loading="lazy">
              <div class="overlay"></div>
              <div class="content">
                <div class="flag">🇺🇬</div>
                <div class="title">Uganda</div>
                <div class="meta">Fine feb / inizio mar 2027 · 10 giorni</div>
                <p class="tagline">Gorilla trekking a Bwindi, safari a Queen Elizabeth NP, rafting grado 5 a Jinja.</p>
              </div>
            </a>

            <a class="trip-card" href="javascript:void(0)" onclick="showDest('tz')">
              <img src="foto/destinazioni/tz-kilimanjaro.jpg" alt="Il Kilimangiaro visto dalla savana" loading="lazy">
              <div class="overlay"></div>
              <div class="content">
                <div class="flag">🇹🇿</div>
                <div class="title">Tanzania</div>
                <div class="meta">Settembre 2027 · 15 giorni</div>
                <p class="tagline">Salita al Kilimangiaro in 8 giorni e safari nel cratere di Ngorongoro.</p>
              </div>
            </a>

            <a class="trip-card" href="javascript:void(0)" onclick="showDest('uk')">
              <img src="foto/destinazioni/Registan_square_Samarkand-7d4b00.jpg" alt="Registan Square, Samarkand" loading="lazy">
              <div class="overlay"></div>
              <div class="content">
                <div class="flag">🇺🇿🇰🇬</div>
                <div class="title">Uzbekistan &amp; Kirghizistan</div>
                <div class="meta">Marzo 2027 · 14 giorni</div>
                <p class="tagline">Samarkand, Bukhara, Khiva e le montagne del Tian Shan.</p>
              </div>
            </a>

            <a class="trip-card" href="javascript:void(0)" onclick="showDest('gl')">
              <img src="foto/destinazioni/Ilulissat_Kangerlua_iceberg_2024.jpg" alt="Ilulissat Icefjord, Groenlandia" loading="lazy">
              <div class="overlay"></div>
              <div class="content">
                <div class="flag">🇬🇱</div>
                <div class="title">Groenlandia</div>
                <div class="meta">Giugno 2027 · 7 giorni</div>
                <p class="tagline">Iceberg, balene e sole di mezzanotte a Ilulissat.</p>
              </div>
            </a>

            <a class="trip-card" href="javascript:void(0)" onclick="showDest('cx')">
              <img src="foto/destinazioni/cx-arenal.jpg" alt="Il vulcano Arenal, Costa Rica" loading="lazy">
              <div class="overlay"></div>
              <div class="content">
                <div class="flag">🇳🇮🇨🇷🇵🇦</div>
                <div class="title">Nicaragua, Costa Rica &amp; Panama</div>
                <div class="meta">Marzo 2027 · 15 giorni</div>
                <p class="tagline">Vulcani del Nicaragua, foresta nuvolosa di Monteverde e il canale di Panama.</p>
              </div>
            </a>

            <a class="trip-card" href="javascript:void(0)" onclick="showDest('ge')">
              <img src="foto/destinazioni/Narikala_fortress,_Tbilisi,_Georgia-fb6b37.jpg" alt="Narikala Fortress, Tbilisi, Georgia" loading="lazy">
              <div class="overlay"></div>
              <div class="content">
                <div class="flag">🇬🇪</div>
                <div class="title">Georgia</div>
                <div class="meta">2-7 gennaio 2027 · 6 giorni</div>
                <p class="tagline">Tbilisi, bagni di zolfo, vino nel qvevri e un weekend sulla neve a Gudauri.</p>
              </div>
            </a>
          </div>
        </div>
      </section>

      <section class="panel dark" data-nav>
        <div class="inner">
          <h2 class="section-title reveal">🗺️ Viaggi già fatti</h2>
          <p class="section-sub reveal">Non tutti i viaggi sono stati fatti dal gruppo al completo — ecco chi c'era.</p>
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
        </div>
      </section>
    </main>

    <footer>
      Patagucci Trips — sito locale, un file unico per tutte le mete. Nessun dato viene inviato a server esterni: mappe, cambio valuta e ricerca voli richiedono internet solo al momento del click.
    </footer>
  </div>'''

destination_blocks = "\n\n".join(b["block"] for b in blocks)

switcher_buttons = '\n        '.join(
    f'<button class="switch-btn" data-dest="{b["suf"]}" onclick="showDest(\'{b["suf"]}\')">{b["flag"]} {b["name"]}</button>'
    for b in blocks
)

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
  .site-switcher{{
    position:sticky; top:0; z-index:200;
    display:flex; gap:6px; justify-content:center; flex-wrap:wrap;
    background:linear-gradient(180deg, rgba(var(--accent-rgb),0.12), transparent 60%), linear-gradient(180deg,#181818,#0e0e0e);
    padding:10px 12px; box-shadow:0 6px 18px rgba(0,0,0,0.35);
    border-bottom:1px solid rgba(var(--accent-rgb),0.22);
    transition:background .5s ease, border-color .5s ease;
  }}
  .site-switcher button{{
    border:1px solid transparent; background:rgba(255,255,255,0.06); color:#cfcfcf;
    padding:8px 16px; border-radius:999px; font-size:0.8rem; font-weight:700; cursor:pointer;
    text-transform:uppercase; letter-spacing:0.04em; transition:all .2s cubic-bezier(.16,1,.3,1);
  }}
  .site-switcher button:hover{{ background:rgba(255,255,255,0.14); transform:translateY(-1px); }}
  .site-switcher button.active{{ background:var(--accent); color:#10100e; box-shadow:0 4px 14px rgba(var(--accent-rgb),0.4); }}
  .site-switcher button.home-btn{{ color:var(--accent); border-color:rgba(var(--accent-rgb),0.4); }}
  .site-switcher button.home-btn.active{{ color:#10100e; }}
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

<script>
var FLAG_BARS = {{
  hub: 'linear-gradient(90deg,#141414 0 50%, #FFCE00 50% 100%)',
  ug: 'linear-gradient(90deg,#141414 0 33%, #FFCE00 33% 66%, #D21034 66% 100%)',
  pk: 'linear-gradient(90deg,#ffffff 0 25%, #01411C 25% 100%)',
  za: 'linear-gradient(90deg,#DE3831 0 16.6%, #ffffff 16.6% 33.3%, #002395 33.3% 50%, #007A4D 50% 66.6%, #FFB612 66.6% 83.3%, #000000 83.3% 100%)',
  np: 'linear-gradient(90deg,#DC143C 0 25%, #003893 25% 50%, #FF9933 50% 75%, #FFB612 75% 100%)',
  uk: 'linear-gradient(90deg,#0099B5 0 50%, #1EB53A 50% 100%)',
  gl: 'linear-gradient(90deg,#ffffff 0 50%, #C60C30 50% 100%)',
  ge: 'linear-gradient(90deg,#ffffff 0 20%, #DA291C 20% 40%, #ffffff 40% 60%, #DA291C 60% 80%, #ffffff 80% 100%)',
  in: 'linear-gradient(90deg,#FF9933 0 33%, #ffffff 33% 66%, #138808 66% 100%)',
  tz: 'linear-gradient(90deg,#1EB53A 0 30%, #FCD116 30% 40%, #000000 40% 60%, #FCD116 60% 70%, #00A3DD 70% 100%)',
  cx: 'linear-gradient(90deg,#0067C6 0 20%, #ffffff 20% 33%, #002B7F 33% 46%, #CE1126 46% 60%, #ffffff 60% 73%, #D21034 73% 86%, #005293 86% 100%)'
}};
function showDest(name){{
  document.documentElement.setAttribute('data-dest', name);
  document.querySelectorAll('.destination').forEach(function(el){{ el.classList.remove('active'); }});
  var target = document.getElementById(name === 'hub' ? 'dest-hub' : 'dest-' + name);
  if(target) target.classList.add('active');
  document.querySelectorAll('#site-switcher button').forEach(function(b){{ b.classList.remove('active'); }});
  var btn = document.querySelector('#site-switcher button[data-dest="' + name + '"]');
  if(btn) btn.classList.add('active');
  var flagbar = document.getElementById('flagbar');
  if(flagbar && FLAG_BARS[name]) flagbar.style.background = FLAG_BARS[name];
  window.scrollTo({{ top: 0, left: 0, behavior: 'instant' }});
  target.querySelectorAll('.reveal').forEach(function(el){{ el.classList.add('visible'); }});
  if(typeof syncSwitcherHeight === 'function') setTimeout(syncSwitcherHeight, 0);
}}
function showHub(){{ showDest('hub'); }}

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

</body>
</html>
'''

out_path = DIR + "index.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print("Written", out_path, "length", len(final_html))
