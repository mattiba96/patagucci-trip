---
name: Patagucci Trips
description: Il taccuino a pennarello dei quattro Patagucci, un quaderno a quadretti per meta.
colors:
  carta: "#ffffff"
  quadretto: "#dbe4ee"
  margine: "#f2a3a3"
  riga-matita: "#cfd6de"
  campitura-matita: "#eef2f6"
  pennarello: "#161616"
  matita: "#555b63"
  penna-blu: "#1d3fa8"
  penna-rossa: "#c8102e"
  evid-casa: "#ffe14d"
  evid-casa-calcato: "#f2c200"
  evid-casa-ink: "#6b5600"
  evid-secondo: "#ff8fb8"
  evid-islanda: "#7deaa0"
  evid-islanda-calcato: "#2fbf6a"
  evid-islanda-ink: "#146b3a"
  evid-corea: "#ff92bb"
  evid-corea-calcato: "#ee4f8b"
  evid-corea-ink: "#a3164f"
  evid-brunei: "#ffc93c"
  evid-brunei-calcato: "#e09c00"
  evid-brunei-ink: "#7a5200"
  evid-singapore: "#cdb0ff"
  evid-singapore-calcato: "#9b6bef"
  evid-singapore-ink: "#5b2ba8"
  logo-verde: "#09442d"
  logo-rosso: "#b30e1a"
  logo-nero: "#060606"
  logo-cresta: "#fcfbfc"
  logo-scritta: "#fcf8ec"
typography:
  display:
    fontFamily: "'Permanent Marker', 'Marker Felt', 'Comic Sans MS', cursive"
    fontSize: "clamp(2.7rem, 6.4vw, 5.6rem)"
    fontWeight: 400
    lineHeight: 1.02
    letterSpacing: "0.005em"
  headline:
    fontFamily: "'Permanent Marker', 'Marker Felt', 'Comic Sans MS', cursive"
    fontSize: "clamp(1.85rem, 3.5vw, 2.7rem)"
    fontWeight: 400
    lineHeight: 1.12
    letterSpacing: "0.005em"
  numeral:
    fontFamily: "'Permanent Marker', 'Marker Felt', 'Comic Sans MS', cursive"
    fontSize: "3.4rem"
    fontWeight: 400
    lineHeight: 1
  title:
    fontFamily: "'Patrick Hand SC', 'Marker Felt', 'Comic Sans MS', cursive"
    fontSize: "1.45rem"
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: "0.02em"
  label:
    fontFamily: "'Patrick Hand SC', 'Marker Felt', 'Comic Sans MS', cursive"
    fontSize: "1.05rem"
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: "0.02em"
  body:
    fontFamily: "'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.6
    fontFeature: "'tnum'"
  body-lead:
    fontFamily: "'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    fontSize: "1.1rem"
    fontWeight: 400
    lineHeight: 1.6
  body-small:
    fontFamily: "'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    fontSize: "0.88rem"
    fontWeight: 400
    lineHeight: 1.55
  micro:
    fontFamily: "'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    fontSize: "0.8rem"
    fontWeight: 400
    lineHeight: 1.5
  mono:
    fontFamily: "'Atkinson Hyperlegible Mono', ui-monospace, Consolas, monospace"
    fontSize: "0.8rem"
    fontWeight: 400
    lineHeight: 1.5
rounded:
  cornice: "4px"
  polaroid: "3px"
  mano-piccola: "12px 7px 14px 8px / 8px 13px 7px 12px"
  mano-tonda: "52% 48% 55% 45% / 47% 55% 45% 53%"
spacing:
  quadretto: "22px"
  gap: "16px"
  riquadro: "18px 22px"
  pagina: "72px 20px 34px"
  pagina-mobile: "52px 16px 26px"
  giustezza: "1040px"
components:
  bottone-azione:
    backgroundColor: "{colors.evid-casa}"
    textColor: "{colors.pennarello}"
    typography: "{typography.label}"
    rounded: "{rounded.mano-piccola}"
    padding: "9px 18px 7px"
  bottone-carta:
    backgroundColor: "{colors.carta}"
    textColor: "{colors.pennarello}"
    typography: "{typography.label}"
    rounded: "{rounded.mano-piccola}"
    padding: "9px 18px 7px"
  filtro:
    backgroundColor: "{colors.carta}"
    textColor: "{colors.pennarello}"
    typography: "{typography.label}"
    rounded: "{rounded.mano-piccola}"
    padding: "7px 14px 5px"
  filtro-hover:
    backgroundColor: "{colors.campitura-matita}"
  filtro-attivo:
    backgroundColor: "{colors.evid-casa}"
  etichetta:
    backgroundColor: "{colors.carta}"
    textColor: "{colors.pennarello}"
    typography: "{typography.label}"
    rounded: "{rounded.mano-piccola}"
    padding: "5px 12px 4px"
  etichetta-da-prenotare:
    backgroundColor: "{colors.carta}"
    textColor: "{colors.penna-rossa}"
    typography: "{typography.label}"
    rounded: "{rounded.mano-piccola}"
    padding: "5px 12px 4px"
  riquadro:
    backgroundColor: "{colors.carta}"
    textColor: "{colors.pennarello}"
    rounded: "{rounded.cornice}"
    padding: "{spacing.riquadro}"
  campo:
    backgroundColor: "{colors.carta}"
    textColor: "{colors.pennarello}"
    typography: "{typography.body}"
    rounded: "{rounded.mano-piccola}"
    padding: "9px 12px"
  polaroid:
    backgroundColor: "{colors.carta}"
    rounded: "{rounded.polaroid}"
    padding: "10px 10px 0"
  numero-giorno:
    backgroundColor: "{colors.evid-casa}"
    textColor: "{colors.pennarello}"
    rounded: "{rounded.mano-tonda}"
    size: "44px"
  nota-manca:
    backgroundColor: "{colors.carta}"
    textColor: "{colors.penna-rossa}"
    typography: "{typography.label}"
    rounded: "{rounded.cornice}"
    padding: "8px 16px 8px 10px"
  copertina-entra:
    backgroundColor: "{colors.evid-casa}"
    textColor: "{colors.pennarello}"
    typography: "{typography.headline}"
    rounded: "{rounded.mano-piccola}"
    padding: "12px 30px 11px 34px"
    height: "58px"
  copertina-musica:
    backgroundColor: "transparent"
    textColor: "{colors.carta}"
    typography: "{typography.label}"
    rounded: "{rounded.mano-piccola}"
    padding: "6px 14px 5px 11px"
    height: "44px"
---

# Design System: Patagucci Trips

## Overview

**Creative North Star: "Il taccuino a pennarello"**

Il sito è un quaderno di scuola italiano a quadretti da 5 mm su cui i quattro Patagucci prendono appunti di viaggio. Il foglio è bianco, con i quadretti azzurrini (22px) e, dove lo schermo è largo, la riga rossa del margine. Sopra ci sono quattro strumenti, e ognuno ha un compito solo: il pennarello nero scrive i titoli e i numeri, la matita grigia il testo di contorno, la penna Bic blu i link e i comandi, la penna rossa soltanto quello che manca da prenotare. In più c'è l'evidenziatore, e il suo colore cambia con il paese che si sta leggendo.

Le cose non si mettono in scatola, si disegnano. I riquadri hanno un bordo tirato a mano (un SVG usato come border-image) e non fanno ombra, perché l'inchiostro su un foglio non ne fa. L'ombra c'è solo sugli oggetti di carta appoggiati sul quaderno: polaroid, nastro adesivo, il foglio che si volta, la copertina. Le foto non fanno da sfondo, sono polaroid inclinate e attaccate col nastro. Le pagine non diventano mai scure e non si tingono mai di crema: cambia solo il colore dei quadretti.

Il movimento è fatto di gesti di carta, e senza di esso non si perde niente. Ci sono l'aereo della copertina che vola fino al quaderno, la pagina che si volta quando si cambia meta, la passata di evidenziatore sulla parola del titolo, la penna rossa che cerchia, le polaroid che si sollevano sotto il mouse. Se Motion non arriva, o chi guarda chiede meno movimento, la pagina è già intera e ferma. Questo mondo sostituisce del tutto quello precedente: niente foto a tutto schermo, niente card arrotondate con ombra, niente pannelli scuri alternati.

**Key Characteristics:**
- Foglio bianco a quadretti da 22px; la riga rossa del margine compare solo da 1220px in su.
- Tre mani tipografiche: pennarello (Permanent Marker), stampatello a mano (Patrick Hand SC), testo leggibile (Atkinson Hyperlegible Next), più il mono per codici e orari.
- Un evidenziatore per meta, registrato con @property perché il passaggio di colore scorra invece di saltare.
- Riquadri a tratto di pennarello, e niente ombra sull'inchiostro.
- Polaroid con il nastro strappato per le foto, l'equipaggio e le mete.
- Penna rossa riservata a «da prenotare».
- Ingresso dalla copertina del quaderno, con il logo vero del gruppo e la «Patagucci song».

## Colors

Una carta e quattro inchiostri restano fissi in tutto il sito. L'unica cosa che cambia è l'evidenziatore, uno per meta.

### Primary
- **Evidenziatore** (`evid-casa`, `evid-islanda`, `evid-corea`, `evid-brunei`, `evid-singapore`): passa sotto la parola del titolo, sotto la linguetta attiva, nei numeri dei giorni, nelle rotte delle cartine, nei filtri attivi, nei paesi visitati sul mappamondo. In CSS è `--accent`. La home è gialla, l'Islanda verde aurora, la Corea rosa ciliegio, il Brunei oro della cupola, Singapore lilla Supertree. Le mete archiviate hanno già il loro evidenziatore nel foglio di stile (Nepal, Pakistan, Sudafrica, India, Uganda, Tanzania, Uzbekistan, Groenlandia, Christmas Island, Georgia, e il turchese del «prossimo»), così il giorno che tornano in linea sono già pronte.
- **Evidenziatore calcato** (`evid-*-calcato`, `--accent-deep`): lo stesso colore ripassato più volte. Serve per i tratti spessi e l'alone pulsante sulle cartine.
- **Evidenziatore leggibile** (`evid-*-ink`, `--accent-ink`): il colore del paese scurito quanto basta per stare come testo sulla carta (circa 6,6:1). Si usa per i pallini degli elenchi e per ogni testo che deve portare il colore della meta.
- **Evidenziatore tenue** (`--evid-tenue`, accento al 34% sul bianco) e **quadretti della meta** (`--quadretto-meta`, al 58%): si ricavano con color-mix e non sono primitive. Il primo colora le note (callout), i risultati e i livelli medi; il secondo i quadretti delle pagine alternate.

### Secondary
- **Penna Bic blu** (`penna-blu`): link, link alla home, link alle mappe, anello del focus. I link nel testo sono sottolineati a 1,5px con la sottolineatura al 45% di trasparenza; al passaggio del mouse la sottolineatura diventa piena e dietro il link passa l'evidenziatore.
- **Secondo evidenziatore** (`evid-secondo`, `--accent-2`): il secondo pennarello dell'astuccio. Ha un compagno diverso per ogni meta. Si usa per gli avvisi (callout tratteggiato), per i livelli difficili e per le etichette messe in risalto.

### Tertiary
- **Penna rossa** (`penna-rossa`): soltanto «da prenotare». Ricorre in cinque punti: la nota della home con il numero cerchiato, l'etichetta d'azione nell'intestazione, il riquadro dei voli mancanti, la casella del calendario di un volo non comprato, l'etichetta «volo da prenotare» nei giorni.

### Neutral
- **Carta** (`carta`): il foglio, il fondo dei riquadri, la cornice delle polaroid.
- **Quadretto** (`quadretto`): le righe del quaderno, 1px ogni 22px nei due versi.
- **Margine** (`margine`): la riga rossa verticale a sinistra della colonna di testo, larga 2px.
- **Riga a matita** (`riga-matita`): righe delle tabelle e divisori sottili.
- **Campitura a matita** (`campitura-matita`): passaggio del mouse sui filtri, binari delle barre, fondo della barra di scorrimento.
- **Pennarello** (`pennarello`): titoli, testo, bordi, contorni.
- **Matita** (`matita`): testo secondario, crediti, sottotitoli (7:1 sulla carta).

### Il logo (solo copertina)
- **Verde cielo** (`logo-verde`), **rosso banda** (`logo-rosso`), **nero montagne** (`logo-nero`), **bianco cresta** (`logo-cresta`), **crema scritta** (`logo-scritta`). Sono i colori del logo animato del gruppo e vivono soltanto sulla copertina d'ingresso. Il nero è anche il fondo dell'anta, la crema è il contorno ripassato del bottone «Entra», che è giallo come l'evidenziatore della home.

### Named Rules

**La Regola della Penna Rossa.** Il rosso (`penna-rossa`) compare solo su ciò che manca da prenotare, e sempre insieme a un secondo segnale che non dipende dal colore: tratteggio, numero cerchiato o la scritta «da prenotare». Gli avvisi qualunque usano il tratteggio nero e il secondo evidenziatore, mai il rosso.

**La Regola del Nero sull'Evidenziatore.** Sopra l'evidenziatore si scrive solo con il pennarello nero. Il grigio matita non va mai sopra un colore di meta: il grigio sul rosa scendeva a 3,3:1. Il colore pieno dell'evidenziatore non diventa mai testo; quando il testo deve avere il colore della meta si usa la sua versione leggibile (`--accent-ink`).

**La Regola del Foglio Bianco.** Nessuna pagina diventa scura o color crema. Le pagine alternate (`section.panel.alt`) cambiano colore solo nei quadretti, che prendono la tinta della meta. Il fondo resta la carta.

**La Regola del Paese.** I componenti usano solo i token semantici (`--accent`, `--accent-deep`, `--accent-ink`, `--accent-2`, `--evid-tenue`). La meta si imposta con `data-dest` e `data-paese` sull'elemento `<html>`. Gli unici esadecimali ripetuti fuori dall'astuccio sono gli evidenziatori locali di paese (il divisore di paese, le caselle del calendario, i trattini delle linguette): devono restare identici a quelli dell'astuccio.

**La Regola del Logo a Parte.** I cinque colori del logo stanno sulla copertina e non entrano nel quaderno. Il logo non si ridisegna: i livelli sono le immagini e i contorni del logo vero del gruppo. L'unico pezzo del logo che entra nel quaderno è l'aereo Royal Brunico, la stessa immagine ritagliata, accanto al titolo della home: ci arriva in volo dalla copertina.

## Typography

**Display Font:** Permanent Marker (con Marker Felt, Comic Sans MS, cursive)
**Label Font:** Patrick Hand SC (con Marker Felt, Comic Sans MS, cursive)
**Body Font:** Atkinson Hyperlegible Next (con Atkinson Hyperlegible e lo stack di sistema)
**Mono Font:** Atkinson Hyperlegible Mono (con ui-monospace, Consolas)

**Character:** Il pennarello urla i titoli, lo stampatello a mano scrive le etichette, e le frasi da leggere sono sempre in un carattere progettato per leggersi bene. L'aria di quaderno la danno i titoli e le etichette. Il testo resta comodo da leggere come in una guida.

### Hierarchy
- **Display** (400, clamp(2.7rem, 6.4vw, 5.6rem), 1.02): il titolo della prima pagina di ogni meta. Una sola parola è evidenziata.
- **Headline** (400, clamp(1.85rem, 3.5vw, 2.7rem), 1.12, al massimo 30ch): i titoli di sezione, evidenziati riga per riga. Il divisore di paese usa la stessa voce più grande (clamp(2.2rem, 6vw, 3.6rem)).
- **Numeral** (Permanent Marker, 3.4rem / 2.7rem / 2.1rem): numeri grossi, conteggi dei paesi, numeri del mappamondo. Lo stesso pennarello scrive anche le date del calendario, i numeri dei giorni e il risultato del cambio valuta.
- **Title** (Patrick Hand SC 400, 1.45rem / 1.25rem, 1.2, 0.02em): h3, titoli dei giorni, nomi nelle schede.
- **Label** (Patrick Hand SC 400, 1–1.12rem, 0.02em): linguette, etichette, tag, bottoni, intestazioni delle tabelle, didascalie delle polaroid, nota della home.
- **Body** (Atkinson 400, 17px, 1.6; 16,5px sotto i 760px): tutto il testo da leggere, al massimo 72ch. Cifre tabellari su tutto il sito.
- **Lead / Small / Micro** (1.1rem / 0.88rem / 0.8rem): sottotitoli di sezione (62ch), testi delle schede, fonti e crediti.
- **Mono** (0.8rem, matita): codici di prenotazione, numeri di volo, orari nelle tabelle.

### Named Rules

**La Regola delle Tre Mani.** Pennarello per titoli e numeri, stampatello a mano per le etichette, Atkinson per qualsiasi frase. Un paragrafo non si scrive mai in Patrick Hand o in Permanent Marker.

**La Regola della Parola Sola.** Nel titolo della meta si evidenzia una parola sola, quella che conta («Patagucci», «Corea»). Se tutte le righe sono evidenziate, non risalta niente. Nei titoli di sezione la passata copre il titolo intero, una riga alla volta.

**La Regola del 12,8.** La scala ha sei gradini per il testo e tre per i numeri. Il più piccolo è 0.8rem (12,8px): sotto i 12px non si legge. Sul telefono le scritte delle cartine passano a 19px e quelle secondarie si nascondono.

## Layout

Una colonna di testo larga 1040px, centrata, su un foglio che riempie lo schermo. Le pagine (sezioni) hanno 72px sopra, 20px ai lati e 34px sotto (52 / 16 / 26 sotto i 760px, 46 / 13 / 22 sotto i 400px). Fra una pagina e l'altra c'è una riga a pennarello disegnata a mano (`--riga-mano`, un SVG da 240×10 ripetuto in orizzontale). La riga rossa del margine corre lungo tutto il quaderno, 44px a sinistra della colonna, e solo da 1220px in su.

L'intestazione di ogni meta divide lo spazio fra testo e foto in proporzione 1,12 : 0,88, con il titolo a sinistra e la polaroid a destra (al massimo 430px, 4:5). Sotto i 760px diventa una colonna sola: testo, poi foto (78% della larghezza, al massimo 330px), poi credito. Le griglie di schede usano `auto-fit` con un minimo fra 200 e 300px e collassano da sole. L'equipaggio resta su due colonne sul telefono.

In alto ci sono due barre fisse: il selettore delle mete (con la riga a pennarello sotto) e le linguette delle sezioni (con una riga a matita). Entrambe stanno su una riga sola che scorre orizzontalmente a qualsiasi larghezza e restano centrate quando c'è spazio. Sotto i 600px il selettore mostra i nomi corti. Gli elementi toccabili sul telefono sono alti almeno 44px. Le tabelle a quattro colonne scorrono orizzontalmente, con un'ombra sul bordo che indica che c'è altro da vedere. In stampa spariscono quadretti, barre e ombre, e i riquadri non si spezzano fra due pagine.

## Elevation & Depth

Il sistema è ibrido e la regola che lo divide è materiale. L'inchiostro è piatto: riquadri, giorni, note, cartine, caselle, domande frequenti. Hanno il tratto a pennarello e nessuna ombra, nemmeno quando sono aperti o sotto il mouse. La carta appoggiata sul quaderno fa invece un'ombra corta e morbida. La profondità della copertina e della pagina che si volta viene dalla prospettiva 3D e da una sfumatura scura sul bordo, non da un alone.

### Shadow Vocabulary
- **Carta su carta** (`box-shadow: 0 1px 1px rgba(20,24,30,0.06), 0 12px 22px -16px rgba(20,24,30,0.38)`): la foto piccola dentro un giorno, i riquadri delle pagine sorgente più vecchie che non hanno il tratto.
- **Polaroid** (`box-shadow: 0 2px 3px rgba(20,24,30,0.10), 0 22px 34px -18px rgba(20,24,30,0.48)`): foto dell'intestazione, equipaggio, striscia delle foto del gruppo, cartoline delle mete, striscia fotografica.
- **Nastro** (`box-shadow: 0 1px 2px rgba(0,0,0,0.08)`): il nastro adesivo sopra la polaroid.
- **Foglio che si volta** (`box-shadow: inset -40px 0 60px -40px rgba(0,0,0,0.25)`, più una sfumatura che scurisce il lato che si alza mentre gira): la pagina a quadretti che gira sul bordo sinistro, o sul destro tornando a una meta che viene prima.

### Named Rules

**La Regola dell'Inchiostro Senza Ombra.** Un riquadro disegnato a pennarello non fa ombra, mai, nemmeno da aperto o sotto il mouse. L'ombra spetta solo agli oggetti di carta: polaroid, nastro, il foglio che si volta, la copertina.

## Shapes

Nessun angolo è uguale all'altro. I riquadri di inchiostro hanno un bordo trasparente da 2px con `border-image: var(--tratto) 16 / 16px / 4px round` sopra un raggio di 4px. Il disegno sborda di qualche pixel agli angoli, come una riga vera. Il tratto esiste in tre versioni: nero pieno (`--tratto`), nero tratteggiato per gli avvisi e il preventivo che sfora (`--tratto-tratteggio`), rosso tratteggiato per il da prenotare (`--tratto-rosso`). Nelle tabelle che scorrono il tratto non sborda.

Etichette, bottoni, linguette, filtri, tag e campi usano il raggio asimmetrico `mano-piccola` e alcuni sono leggermente ruotati (da −1,5° a 0,8°). I numeri dei giorni sono cerchi storti (`mano-tonda`, ruotati di −4° o 3°, con il secondo profilo sui giorni pari). Le polaroid hanno angoli da 3px, il bordo bianco più alto in basso e un'inclinazione propria fra −2° e 2,6°, scritta in `--gira` perché il movimento la conservi. Il nastro ha le estremità strappate (`--nastro`, una maschera SVG). Le barre dei grafici hanno la cima arrotondata a mano (10px 6px 2px 2px).

Anche le icone sono disegnate e si applicano come maschere SVG colorate con il colore del testo: la spunta (`--spunta`) accanto ai nomi e alle mete confermate, l'aeroplanino di carta (`--aereo`) nei giorni di volo. Sulle cartine le tappe sono puntine a pennarello, cioè cerchi evidenziati con il contorno nero. La grana dell'evidenziatore (`--evid-grana`) è un velo bianco sopra la passata di colore: sfrangia le estremità e lascia le righe del pennarello.

### Named Rules

**La Regola del Tratto Intero.** Per ridare il bordo a un riquadro disegnato si riscrive sempre per intero: `border` e poi `border-image`. La forma abbreviata di `border` azzera il border-image, e il riquadro torna una scatola CSS.

**La Regola del Disegno, non del Carattere.** Le icone sono disegni SVG, non emoji e non caratteri. In fase di montaggio `build.py` toglie le emoji davanti a titoli, titoletti, etichette e link. Restano due eccezioni, perché sono dati e non decorazione: le bandiere (nelle etichette dei paesi visti, sulle cartoline e nelle caselle del calendario) e il veicolo che percorre le cartine del percorso, che lo script cambia a seconda del mezzo.

## Components

### Bottoni
- **Character:** etichette evidenziate con il tratto ripassato.
- **Azione** (`bottone-azione`): stampatello a mano 1.12rem, fondo evidenziatore, contorno pennarello da 2px. Dietro c'è un secondo contorno spostato di 3px a destra e 4px in basso (`::after`, solo contorno, nessuna campitura). La variante su carta (`bottone-carta`) ha il fondo bianco; quella per l'esportazione usa il secondo evidenziatore.
- **Hover / Focus:** il bottone si stacca dal secondo contorno (`translate(-1px,-1px) rotate(-1deg)`, 0,2s su curva `cubic-bezier(.16,1,.3,1)`). Il focus è l'anello unico del sito: penna blu da 3px con 2px di distacco e un alone bianco da 6px, che resta visibile anche sopra l'evidenziatore.

### Filtri e linguette delle mete
- **Filtri** (`filtro`): stampatello a mano su carta, contorno nero da 1,5px. Sotto il mouse prendono la campitura a matita; da attivi prendono l'evidenziatore e ruotano di −1,5°. Le linguette delle mete in home (con il conteggio in pennarello) usano la stessa forma, alte almeno 46px.

### Etichette e tag
- **Style:** stampatello a mano su carta, contorno pennarello da 1,5px, `mano-piccola`, leggera rotazione alternata. Livelli e difficoltà si distinguono per il fondo: carta (facile), evidenziatore tenue (media), secondo evidenziatore (difficile), matita tratteggiata (assente). Aperto e chiuso si distinguono anche per il contorno: pieno o tratteggiato.
- **Da prenotare:** penna rossa, tratteggio da 2px, fondo carta.

### Riquadri
- **Corner Style:** il tratto a pennarello (raggio 4px sotto il disegno).
- **Background:** carta. Le note (callout) hanno l'evidenziatore tenue; gli avvisi hanno il secondo evidenziatore al 30% e il tratto tratteggiato.
- **Shadow Strategy:** nessuna (Regola dell'Inchiostro Senza Ombra).
- **Internal Padding:** 18px 22px (16px sul telefono); note 15px 20px.
- **Hover:** nessuno. È un foglio, non un bottone.

### Campi
- **Style:** riga da riempire a penna. Carta, contorno pennarello da 1,5px, `mano-piccola`, padding 9px 12px, Atkinson. L'etichetta sopra è in stampatello a mano.
- **Focus:** l'anello in penna blu.
- **Mobile:** 16px nel campo (sotto, iOS ingrandisce da solo al focus) e larghezza piena.

### Navigazione
- **Selettore delle mete:** Permanent Marker 1.08rem, in matita. Ogni linguetta ha il suo evidenziatore (`--dab`): da chiusa è un trattino da 22×5px sotto la scritta, sotto il mouse il trattino si allunga, da aperta diventa la passata intera con la grana dietro le lettere. Le mete con le date fissate hanno la spunta disegnata.
- **Linguette delle sezioni:** stampatello a mano in matita. Sotto il mouse sono sottolineate a matita; la sezione attiva ha l'evidenziatore all'82% dell'altezza, con la grana. Il ritorno alla home è in penna blu.
- **Nastro della bandiera:** una striscia da 6px in cima, con i colori della bandiera della meta. È un dato, non una decorazione del sistema.

### Polaroid (componente firma)
Bordo bianco (12px, e 54px in basso nell'intestazione), angoli da 3px, ombra da polaroid, inclinazione propria in `--gira`. Nell'intestazione c'è il nastro strappato, tinto con l'evidenziatore al 62%. Con un mouse vero si inclina in 3D seguendo il puntatore (fino a ±6° in verticale e ±7° in orizzontale, sollevata di 16px) e torna giù in 0,55s rallentando, senza rimbalzo. L'inclinazione piena spetta alle foto che si aprono (cartoline delle mete, equipaggio); quelle che non si aprono (l'intestazione, la striscia delle foto del gruppo) si sollevano appena, al 40% e di 6px, perché un'inclinazione piena sembrerebbe un invito al clic. Quando arriva una meta, la polaroid cade sul foglio (`rotateX(32deg)` → 0, da −46px, 0,85s), e intanto non segue il mouse. Le cartoline delle mete e le foto dell'equipaggio sono polaroid, con la didascalia in stampatello a mano.

### Il numero del giorno e l'itinerario (componente firma)
Ogni giorno è un riquadro a tratto che si apre. Il numero è scritto in pennarello dentro un cerchio storto evidenziato (44×42px, 38×36px sul telefono). Il titolo è in stampatello a mano, e la freccia ruota di 90° all'apertura. Aprendolo, il giorno si spiega come un foglio piegato: il riquadro si allunga e lo scritto compare (0,34s, curva `[.16,1,.3,1]`); si ripiega più svelto (0,24s), e la freccia torna subito a destra. Un secondo clic a metà strada torna indietro da dove si trova. Le aperture fatte dallo script (il primo giorno, la casella del calendario) restano immediate. Il calendario a colpo d'occhio ha una casella per giorno: la data è passata con l'evidenziatore del paese, il giorno di volo ha l'aeroplanino di carta, il volo da comprare ha il tratto rosso tratteggiato e la scritta «da prenotare».

### La nota di quello che manca
In home, sotto il sottotitolo, c'è una nota a penna rossa con il tratto rosso tratteggiato, ruotata di −0,8°. Il numero (in pennarello) è cerchiato da un tratto rosso che si disegna da solo, una volta, quando entra nello schermo (0,9s, curva `[.65,0,.35,1]`). Dopo la copertina è l'ultimo colpo dell'arrivo sulla home: cerchia i voli da prenotare quando la polaroid è caduta e la passata si è stesa. La nota è sempre visibile, ma non è mai la cosa principale della pagina.

### La copertina (componente firma)
Il quaderno chiuso, a schermo pieno, con il logo vero del gruppo stampato in copertina. Il logo è fatto a livelli: cielo, banda e aereo sono immagini in `assets/logo/`, montagne, cresta e lettere sono vettori da `_sources/logo/forme.json`. Il disegno si misura in unità del disegno originale (`--u`, su una tavola di 1672×941) e il colore pieno continua oltre i bordi. Sul dorso ci sono i due punti metallici; in basso a destra la scritta «Quadretti 5 mm»; in alto a destra il tasto della musica (bianco, contorno a mano, dice quello che fa: «Accendi la musica» o «Spegni la musica»). All'apertura il logo si stampa da solo, a colpi, come un manifesto (solo CSS, 2,6s): il cielo, la banda, montagne e cresta, la scritta con un tonfo; poi l'aereo Royal Brunico entra in volo, si posa e ondeggia, e compare «Entra». Ogni colpo rallenta e si posa, senza rimbalzi e senza sfocature. L'intro aspetta che le immagini del logo siano pronte, al massimo 1,5s; Esc, o un tocco sulla copertina, la porta subito alla fine. «Entra» è inerte finché non ha finito di comparire (fine dell'animazione `cpAppare`): il tab non raggiunge un bottone che non si vede. Il resto della pagina invece è inerte finché c'è la copertina, ogni pezzo da quando arriva: su una rete lenta il tab non scivola dietro la copertina. Aspetta anche lo script del volo, al massimo 2,5s in più, così su una rete lenta non si cade sulla dissolvenza di riserva solo perché lo script era in ritardo. Motion è una copia del pacchetto ufficiale in `assets/vendor/`, e i due script stanno in testa alla pagina, rimandati.

Su «Entra» parte il volo verso il quaderno (Motion, 2,6s). L'aereo si stacca dal logo e vola verso lo schermo: accelera, cresce fino a 4 volte, si inclina di −8° e ti passa oltre (0,8s), e intanto la copertina gli va incontro di un 5%. Niente sfocature: la velocità la dice la crescita. Il cielo diventa il foglio: le righe orizzontali dei quadretti corrono da sinistra a destra, poi quelle verticali dall'alto in basso (0,4s ciascuna, come tirate col righello), e sotto il verde si fa bianco. Lo stesso aereo rientra da sinistra, perché era uscito a destra: piccolo, col muso sempre in avanti e senza picchiate. Scende piano fino alla riga del titolo, riprende quota tracciando la scia tratteggiata a matita e si posa accanto a «Patagucci Trips», esattamente sopra l'aereo che sta lì. Mentre arriva, il foglio si scopre (0,6s) e sotto c'è la home, che lo accoglie con il suo arrivo: la polaroid cade, la passata si stende e per ultima la penna rossa cerchia i voli da prenotare. Posizione, misura e inclinazione dell'atterraggio vengono dal disegno sulla home, quindi tornano su qualsiasi schermo. Le righe crescono in scala, non ritagliate, così il volo resta fluido anche su un telefono.

Il volo si può saltare: un secondo «Entra» premuto entro 0,6s è un doppio clic e non conta, dopo invece salta. Saltano anche Esc e un cambio di misura della finestra a volo iniziato. Saltando, i movimenti del volo si fermano, la copertina svanisce in 0,2s e la home fa subito il suo arrivo, una volta sola. Chi è entrato da tastiera (Invio o Esc) si ritrova col focus sul titolo della pagina. Una rete di sicurezza chiude comunque la copertina dopo 6s.

Il disegno sulla home è l'aereo del logo inclinato di −6°, 2,73em di larghezza, con il fondo sulla riga del testo. La sua scia parte dalla riga, subito dopo l'ultima lettera, e sale fino alla coda.

La «Patagucci song» suona sulla copertina e sfuma in 1,8s quando si preme «Entra». Senza Motion la copertina sfuma (0,6s). Con il movimento ridotto il logo è già intero e la copertina si dissolve in 0,25s. Senza JavaScript la copertina non c'è e il sito è già aperto. Il focus qui è bianco, perché il blu sul verde e sul nero non si vedrebbe.

### Il movimento (assets/anima.js)
Motion senza React, otto gesti:
- Il volo verso il quaderno, all'uscita dalla copertina (vedi sopra).
- La pagina che si volta: un foglio a quadretti grande quanto lo schermo gira sul bordo sinistro in 0,55s, partendo deciso e rallentando. Tornando a una meta che viene prima gira sul bordo destro. Passa sotto le linguette, che restano ferme e dicono dove si è. Si volta solo quando la meta cambia davvero: non per un link a una sezione della stessa meta, non ripremendo la linguetta aperta, e una volta sola con Indietro e Avanti.
- La polaroid che cade sul foglio.
- La passata di evidenziatore, solo sulla parola del titolo della meta (0,75s). Riparte da vuota senza che la si veda ritirarsi.
- La penna rossa che si disegna, una volta, quando entra nello schermo: attorno al «2» della nota in home, e attorno alle parole da prenotare nel titolo del riquadro dei biglietti della Corea (`.cerchiato`: un giro storto che sborda di un terzo di lettera per parte e allarga un poco la riga, così sul telefono, se il titolo va a capo, non passa sulla riga di sopra come una cancellatura).
- Le polaroid che si inclinano sotto il mouse.
- I giorni che si spiegano come un foglio piegato (vedi l'itinerario).
- I petali dei ciliegi, sulla pagina dei ciliegi della Corea: quando la pagina arriva nello schermo passa una folata di petali, evidenziatore rosa col contorno a pennarello come le puntine delle cartine (uno ogni 70px di larghezza: da nove sul telefono a venti sullo schermo largo, da 12 a 22px). Cadono girando su se stessi e mostrando l'altro lato, ondeggiano nel vento e spariscono prima del fondo: la folata finisce in una decina di secondi. Passano sopra lo scritto senza toccarsi, e ripartono solo quando si torna sulla pagina; quando la pagina esce dallo schermo i petali se ne vanno con lei. È l'unico movimento della pagina che non risponde a un gesto di chi legge: per questo è uno solo, breve, e non torna da solo.

L'arrivo su una meta, dopo la copertina o dopo la pagina che si volta, è un regista solo e fa un gesto alla volta: prima cade la polaroid, 0,35s dopo si stende la passata, 0,4s dopo ancora la penna rossa cerchia quello che manca, se si vede. Sulle cartine il veicolo fa il viaggio quando la cartina entra nello schermo: un giro intero in 20s, poi si ferma all'arrivo, e intanto l'alone attorno alla partenza pulsa tre volte. Tornando a guardarla riparte da capo; fuori dallo schermo non si muove niente. Le foto del gruppo stanno ferme in una striscia che si scorre a mano, col dito, con le frecce o con la tastiera.

Il cambio di colore della meta scorre in 0,6s grazie a @property. Con il movimento ridotto, o senza Motion, non si muove niente: gli evidenziatori sono già stesi, l'aereo della copertina non ondeggia, sulle cartine il veicolo resta alla partenza e l'alone non pulsa, i petali non cadono, i giorni si aprono di colpo, la striscia delle foto e i salti di pagina scorrono senza scivolare e i colori cambiano di colpo.

## Do's and Don'ts

### Do:
- **Do** scrivere i titoli in Permanent Marker, le etichette in Patrick Hand SC e ogni frase in Atkinson Hyperlegible Next, con le cifre tabellari.
- **Do** dare a ogni riquadro di inchiostro il tratto a pennarello (`--tratto`, `--tratto-tratteggio` o `--tratto-rosso`, `16 / 16px / 4px round`), riscrivendo `border` e `border-image` per intero.
- **Do** usare la penna rossa per «da prenotare» insieme al tratteggio o al cerchio, così si distingue anche senza colore.
- **Do** prendere il colore della meta dai token (`--accent`, `--accent-ink`, `--evid-tenue`) e lasciarlo cambiare a `data-dest` e `data-paese`.
- **Do** mettere le foto in polaroid inclinate con `--gira`, con il nastro strappato quando la foto è da sola.
- **Do** disegnare le icone come maschere SVG (spunta, aeroplanino, puntine) colorate con il colore del testo.
- **Do** fare in modo che ogni movimento sia un gesto di carta, e che senza Motion o con il movimento ridotto la pagina sia già intera e ferma.
- **Do** tenere il testo dentro 72ch (62ch per i sottotitoli) e lasciare gli elementi toccabili alti almeno 44px sul telefono.

### Don't:
- **Don't** mettere ombre sui riquadri di inchiostro, nemmeno al passaggio del mouse o da aperti: l'ombra spetta solo a polaroid, nastro, il foglio che si volta e la copertina.
- **Don't** fare pagine scure o color crema: le pagine alternate cambiano solo il colore dei quadretti.
- **Don't** usare il rosso per avvisi generici: quelli prendono il tratteggio nero e il secondo evidenziatore.
- **Don't** mettere testo grigio, o il colore pieno dell'evidenziatore come testo, sopra un evidenziatore.
- **Don't** evidenziare più di una parola nel titolo della meta, né animare l'entrata di ogni titolo di sezione.
- **Don't** usare emoji o caratteri come icone. Le bandiere e il veicolo sulla cartina sono dati, non decorazione.
- **Don't** usare foto a tutto schermo con un velo scuro sotto il testo, né card arrotondate in modo uniforme con l'ombra.
- **Don't** portare i colori del logo dentro il quaderno, né ridisegnare il logo. L'unica eccezione è l'aereo Royal Brunico accanto al titolo della home, dove la copertina lo fa posare.
- **Don't** scendere sotto 0.8rem per qualsiasi testo.
