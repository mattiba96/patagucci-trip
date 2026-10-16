---
name: Patagucci Trips
description: L'almanacco di viaggio di quattro amici — tipografia condensata, numeri grossi, e una palette che cambia col paese.
colors:
  accent: "#FFCE00"
  accent-deep: "#E0AE00"
  accent-ink: "#8A6B00"
  accent-2: "#D21034"
  accent-2-deep: "#A80E29"
  theme-900: "#16362a"
  theme-800: "#1f4d3a"
  theme-700: "#2a6b4d"
  dark-base: "#141414"
  paper: "#fffdf9"
  tint-100: "#f8f5ef"
  tint-200: "#efe8d9"
  line: "#e2d9c6"
  ink: "#20281f"
  ink-soft: "#5b6a61"
typography:
  display:
    fontFamily: "Bebas Neue, Impact, Arial Narrow, sans-serif"
    fontSize: "clamp(3rem, 9vw, 5.6rem)"
    fontWeight: 400
    lineHeight: 0.95
    letterSpacing: "0.02em"
  headline:
    fontFamily: "Bebas Neue, Impact, Arial Narrow, sans-serif"
    fontSize: "clamp(1.9rem, 4.2vw, 3rem)"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "0.01em"
  title:
    fontFamily: "Bebas Neue, Impact, Arial Narrow, sans-serif"
    fontSize: "1.2rem"
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: "0.01em"
  body:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "16.5px"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "normal"
  label:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "0.8rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0.04em"
rounded:
  md: "18px"
  lg: "26px"
  pill: "999px"
  dot: "50%"
spacing:
  xs: "6px"
  sm: "14px"
  md: "20px"
  lg: "30px"
  panel: "78px"
components:
  card:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "18px 20px"
  card-hover:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
  nav-tab:
    backgroundColor: "transparent"
    textColor: "#cfcfcf"
    rounded: "{rounded.pill}"
    padding: "9px 16px"
    typography: "{typography.label}"
  nav-tab-active:
    backgroundColor: "{colors.accent}"
    textColor: "#10100e"
    rounded: "{rounded.pill}"
    padding: "9px 16px"
  filter-chip:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink-soft}"
    rounded: "{rounded.pill}"
    padding: "7px 14px"
  filter-chip-active:
    backgroundColor: "{colors.theme-800}"
    textColor: "#ffffff"
    rounded: "{rounded.pill}"
    padding: "7px 14px"
  badge:
    backgroundColor: "rgba(255,255,255,0.14)"
    textColor: "#fdf9f0"
    rounded: "20px"
    padding: "6px 14px"
  day-number:
    backgroundColor: "{colors.theme-900}"
    textColor: "{colors.accent}"
    rounded: "{rounded.dot}"
    size: "40px"
---

# Design System: Patagucci Trips

## Overview

**Creative North Star: "L'almanacco dei Patagucci"**

Un annuario sportivo, non una brochure di agenzia. Il sistema tratta un viaggio come una stagione da archiviare: tabelle di tratte, numeri grossi battuti in carattere condensato, conteggi di paesi e percentuali, giorni numerati come giornate di campionato. È rigoroso e un po' nerd — ci sono più tabelle che fotografie — ma sta su fondo carta e in caratteri caldi, quindi non diventa mai un cruscotto.

La firma vera del sistema non è un colore: è il fatto che **la pagina cambia palette col paese che si sta guardando**. Un attributo sulla radice (`data-dest`, e dentro una meta `data-paese`) riscrive i token semantici, e con loro accenti, titoli, pannelli scuri, bordi e la fascia-bandiera in cima. L'Islanda è verde aurora su blu notte, la Corea rosa ciliegio su blu, il Brunei oro su verde foresta. Il layout non si muove di un pixel: cambia solo il colore, e lo fa scorrendo.

La palette gialla della home è **provvisoria e non vincolante**: non porta un significato, è il punto di partenza da cui le mete divergono. Quello che è invariante è il meccanismo, non la tinta.

**Key Characteristics:**
- Tipografia condensata tutta maiuscola per ogni titolo e ogni numero; corpo neutro per la lettura
- Palette semantica ritematizzata per paese, layout immutato
- Superfici sollevate: card che galleggiano e si alzano al passaggio
- Alternanza obbligata di pannelli chiari e scuri, sezione dopo sezione
- Densità da almanacco: tabelle, conteggi, griglie filtrabili

## Colors

Una palette calda su base carta, in cui l'accento è l'unica voce satura e cambia identità a ogni meta.

### Primary
- **Giallo Insegna** (`#FFCE00`): l'accento della home. Numeri grossi, tab attiva, percorsi sulle mappe, anelli e bordi al passaggio. Su fondo chiaro non si usa mai per il testo — per quello c'è la sua versione inchiostro.
- **Oro Bruciato** (`#E0AE00`): la variante scura dell'accento. Bordi, gradienti, stati al passaggio.
- **Senape Inchiostro** (`#8A6B00`): l'accento reso leggibile su carta. È il colore dei numeri grossi nei pannelli chiari.

### Secondary
- **Rosso Bandiera** (`#D21034`): il contrasto. Tag evidenziati, pulsazioni sulla mappa, allarmi. Usato con parsimonia.

### Tertiary
- **Verde Spedizione** (`#16362a` / `#1f4d3a` / `#2a6b4d`): la famiglia dei titoli e dei pannelli scuri. Dal più scuro per i titoli su carta al più chiaro per link e bottoni mappa.

### Neutral
- **Carta** (`#fffdf9`): il fondo delle card.
- **Carta Ingiallita** (`#f8f5ef`): il fondo pagina.
- **Sabbia** (`#efe8d9`): chip, righe di risultato, campiture tenui.
- **Bordo Spago** (`#e2d9c6`): tutte le linee e i divisori su fondo chiaro.
- **Nero Pannello** (`#141414`): la base dei pannelli scuri.
- **Inchiostro** (`#20281f`) e **Inchiostro Tenue** (`#5b6a61`): testo primario e secondario su carta.

### Named Rules

**La Regola delle Due Coppie.** Ogni componente che porta testo dichiara il colore per fondo chiaro *e* quello per `section.panel.dark`. Scriverne uno solo è il difetto ricorrente di questo progetto: un componente pensato per il pannello scuro, spostato su quello chiaro, sparisce. Test: cercare la classe nel CSS e verificare che esista la riga `section.panel.dark .classe{ color: … }`.

**La Regola dell'Accento Inchiostro.** L'accento saturo non tocca mai il testo su carta. Su fondo chiaro si usa `accent-ink`; su fondo scuro si usa `accent`.

**La Regola del Paese.** Nessun colore si scrive a mano nei componenti: si usano i token semantici, così la ritematizzazione per paese funziona senza toccare il componente.

## Typography

**Display Font:** Bebas Neue (fallback Impact, Arial Narrow)
**Body Font:** Inter (fallback stack di sistema)

**Character:** Un condensato da manifesto contro un grottesco neutro. Bebas grida i titoli e i numeri in maiuscolo stretto; Inter si fa dimenticare e porta il peso della lettura. Il contrasto fra i due è tutta la tensione tipografica del sistema: non ci sono pesi intermedi né terzo carattere.

### Hierarchy
- **Display** (400, `clamp(3rem, 9vw, 5.6rem)`, line-height 0.95): solo il titolo della meta nell'intestazione a tutta altezza. Maiuscolo, con un filetto sfumato sotto.
- **Headline** (400, `clamp(1.9rem, 4.2vw, 3rem)`, line-height 1): i titoli di sezione, preceduti da un'emoji che fa da segnaposto visivo.
- **Title** (400, `1.2rem`): titoli dei giorni nell'itinerario, nomi nelle schede fatti, intestazioni di card.
- **Body** (400, `16.5px`, line-height 1.6): tutto il testo corrente.
- **Label** (700, `0.8rem`, letter-spacing `0.04em`, maiuscolo): tab di navigazione, chip, intestazioni di tabella.

### Named Rules

**La Regola del Numero Grosso.** Qualunque cifra che valga la pena ricordare — percentuale di mondo visto, giorni di viaggio, durata di una tratta — va in Bebas a corpo molto maggiore del testo attorno, con l'unità in piccolo accanto. I numeri sono il contenuto, non la decorazione.

**La Regola degli Undici Pixel.** Nessun testo che si legge o si tocca scende sotto gli 11px. Il sistema oggi viola questa regola in più punti (crediti foto a 10,56px, note fonti a 11,8px): è debito, non licenza.

## Layout

Colonna unica centrata, mai una griglia multi-colonna a tutta pagina. Il contenitore è `.inner` con larghezza massima intorno ai 1100px; le sezioni sono `section.panel` con `78px` di respiro sopra e `30px` sotto, ridotti a `44px / 16px` sotto i 760px.

Dentro le sezioni il lavoro lo fanno due griglie fluide: `.info-grid` e `.family-grid`, entrambe `repeat(auto-fit, minmax(260px, 1fr))`, che collassano da sole senza breakpoint dedicati. Le tabelle non si impilano: restano tabelle e scorrono dentro la loro card.

La navigazione è a due piani appiccicosi: il selettore delle mete in cima (`position:sticky; top:0`) e sotto la barra delle sezioni, che si ancora all'altezza del selettore tramite la variabile `--switcher-h` misurata a runtime. Entrambe scorrono orizzontalmente a qualsiasi larghezza invece di andare a capo — ad andare a capo mangiavano un terzo dello schermo su telefono.

**La Regola dell'Alternanza.** I pannelli alternano chiaro e scuro senza eccezioni, in sequenza. Togliere o inserire una sezione obbliga a rinumerare l'alternanza: due pannelli chiari di fila sono un difetto visibile.

## Elevation & Depth

Sistema **sollevato**, non piatto. Due ombre ambientali portano quasi tutto: `--shadow` (`0 10px 30px rgba(20,20,20,0.10)`) a riposo e `--shadow-lg` (`0 24px 60px rgba(20,20,20,0.22)`) in evidenza. La profondità è morbida e diffusa, mai una cornice dura.

Lo stato al passaggio non cambia solo l'ombra: la card si alza di 4px e guadagna un anello sottile nel colore dell'accento. È il gesto tattile che tiene insieme il sistema.

### Shadow Vocabulary
- **Ambientale** (`0 10px 30px rgba(20,20,20,0.10)`): stato di riposo di card e contenitori.
- **Sollevata** (`0 24px 60px rgba(20,20,20,0.22)`): passaggio del mouse, pannelli flottanti, pannello chat.
- **Anello d'accento** (`0 0 0 1px rgba(var(--accent-rgb),0.35)`): si somma alla sollevata per segnare il focus senza bordo duro.
- **Spinta colorata** (`0 4px 12px rgba(var(--theme-rgb),0.3)`): sotto bottoni e chip attivi.

### Named Rules

**La Regola dell'Alone Sobrio.** Le ombre colorate si usano solo sotto un elemento, mai come alone a offset zero attorno a un testo. Un bagliore cromatico centrato è l'effetto più datato del repertorio.

## Shapes

Forme morbide e generose. Due raggi soli per le superfici: `18px` per card e callout, `26px` per i contenitori grandi e le schede meta. I controlli — tab, chip, bottoni filtro, badge — sono completamente a pillola (`999px`). I numeri dei giorni sono cerchi pieni da 40px.

Le linee sono sempre da 1px e nel colore `line`; non esistono bordi spessi a scopo decorativo, con una sola eccezione ereditata: `.callout` e `.cal-giorno` portano un `border-left` da 4px su un contenitore arrotondato. È il tell più riconoscibile dell'interfaccia generata, ed è l'unico punto dove il sistema lo fa.

## Components

### Cards
- **Corner Style:** arrotondate (18px)
- **Background:** carta (`#fffdf9`) su pannello chiaro; bianco al 6% su pannello scuro
- **Shadow Strategy:** ambientale a riposo, sollevata + anello d'accento al passaggio
- **Border:** 1px in `line`, che al passaggio diventa `accent-deep`
- **Internal Padding:** `18px 20px`
- **Carattere:** solide e tattili. Si alzano di 4px al passaggio con l'easing unico del sistema.

### Navigation
Due barre appiccicose sovrapposte. Il **selettore delle mete** sta sopra, su gradiente quasi nero, con bottoni a pillola in maiuscolo; l'attivo si riempie dell'accento con testo scurissimo. La **barra delle sezioni** sta sotto, stessa grammatica ma trasparente, e si ancora sotto il selettore misurandone l'altezza a runtime. Entrambe scorrono in orizzontale, senza scrollbar visibile, e su mobile i bersagli salgono a 44px.

### Chips e filtri
- **Riposo:** fondo carta, bordo `line`, testo inchiostro tenue, pillola piena
- **Passaggio:** fondo sabbia, bordo `accent-deep`
- **Attivo:** fondo `theme-800`, testo bianco, spinta colorata sotto

### Badge
Pillole in vetro smerigliato sull'intestazione fotografica: bianco al 14% con `backdrop-filter: blur(6px)` e bordo nell'accento. Si alzano di 2px al passaggio.

### Pannelli di sezione
Il pannello chiaro è carta nuda. Il pannello scuro è costruito a gradienti radiali: una luce d'accento in alto a sinistra, una di tema in basso a destra, sopra la base nera. Ogni sezione tranne la prima porta un filetto sfumato centrato in cima, largo `min(680px, 74%)`, che fa da divisore.

### Timeline dei giorni (componente firma)
Ogni giorno è un `<details>` con un cerchio numerato in Bebas sul colore tema, titolo condensato maiuscolo, una riga di tag e un link a Maps. È il componente che definisce il prodotto: la struttura dell'itinerario si legge dai numeri prima che dal testo.

### Calendario a colpo d'occhio (componente firma)
Griglia di celle cliccabili, una per giorno, con numero di giornata, data, luogo e bandiera. Un filo di colore a sinistra codifica il paese. Cliccando si apre il giorno corrispondente nella timeline.

## Do's and Don'ts

### Do:
- **Do** usare i token semantici (`--accent`, `--theme-900`, `--ink`) e mai un colore letterale dentro un componente: è ciò che rende possibile la ritematizzazione per paese.
- **Do** dichiarare sempre la coppia chiaro/scuro di ogni componente testuale, con la variante `section.panel.dark`.
- **Do** mettere in Bebas ogni numero che conta, molto più grande del testo attorno.
- **Do** usare l'unico easing del sistema, `cubic-bezier(.16,1,.3,1)`, per ogni transizione di stato.
- **Do** far scorrere in orizzontale le barre di navigazione invece di mandarle a capo.
- **Do** mantenere l'alternanza chiaro/scuro dei pannelli quando se ne aggiunge o toglie uno.

### Don't:
- **Don't** scendere sotto gli 11px su testo leggibile o toccabile.
- **Don't** aggiungere un terzo carattere: il sistema è Bebas più Inter, e basta.
- **Don't** usare l'accento saturo per il testo su fondo chiaro: c'è `accent-ink` per quello.
- **Don't** mettere alone colorato a offset zero attorno a testo o riquadri.
- **Don't** aggiungere nuovi `border-left` spessi su contenitori arrotondati: quelli esistenti sono debito ereditato, non un modello da seguire.
- **Don't** annidare una card dentro un'altra card: la profondità si fa con spazio e tipografia.
- **Don't** usare easing elastici o di rimbalzo.
