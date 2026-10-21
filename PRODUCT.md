# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Quattro amici italiani che viaggiano insieme: **Manu**, **Kiki**, **Mala**, **Bacci**. Non c'è altro pubblico — il sito è uno strumento interno del gruppo, e il contesto condiviso (soprannomi, battute, chi è fatto come) si può dare per scontato.

Il momento d'uso principale è **prima della partenza, per organizzare**: da casa, su schermo grande, per decidere e prenotare. La consultazione durante il viaggio esiste ma non è il caso d'uso che comanda le scelte.

## Product Purpose

Tenere in un posto solo un viaggio già deciso, nel dettaglio che serve per organizzarlo: itinerario giorno per giorno, mappa del percorso, meteo, regole d'ingresso, cosa si mangia, cosa non si può perdere, quali voli sono comprati e quali no.

Funziona quando il gruppo riesce a pianificare e prenotare senza andare a ricercare altrove quello che è già stato cercato una volta.

Da ottobre 2026 il sito **si legge come il diario di viaggio del gruppo**, non come un promemoria di cose da fare: stessa struttura e stessi fatti, ma la voce è un racconto in prima persona plurale («partiamo», «dormiamo», «ci serve»). Quello che manca da prenotare resta visibile nella pagina del suo viaggio, a penna rossa. **La home racconta il gruppo**, non le cose da fare: chi siamo, i paesi visti, il viaggio fatto insieme, con la nostra foto a Machu Picchu in copertina.

## Positioning

Non è un pianificatore di viaggi generico: è il registro di *questi* viaggi. Ogni affermazione fattuale — orari, prezzi, regole, date di fioritura, divieti — è ricercata e porta la sua fonte con la data di verifica, e dove il dato non esiste o non è verificabile lo si dichiara invece di riempire il buco. È la differenza fra una pagina che si può usare per prenotare e una che si può solo leggere.

## Operating Context

- Tutto in **italiano**.
- I viaggi pubblicati sono **confermati e in buona parte pagati**: i contenuti devono corrispondere alle prenotazioni reali, non a un'ipotesi.
- I dati arrivano dalle prenotazioni del gruppo e dalle loro schermate, passate a mano.
- Le mete archiviate restano come sorgenti in `_sources/` anche quando non sono pubblicate: rimetterne una in linea è una riga di configurazione.
- Anche **«Quale sarà il prossimo?»** (la pagina di ricerca voli per la meta futura) è fuori dal sito da ottobre 2026, per scelta del gruppo: la sorgente resta in `_sources/prossimo.html` e la funzione di ricerca voli in `api/`.

## Capabilities and Constraints

- Sito statico generato da `_sources/build.py`, che unisce una pagina HTML per meta in un unico `index.html`; le mete si cambiano senza ricaricare.
- Pubblicato su Vercel da GitHub, con funzioni serverless in `api/`: ricerca voli e ricerca concerti. La chat «Chiedi ai Patagucci» è stata tolta a ottobre 2026, perché non serviva più: niente pannello in pagina e niente funzione.
- **Il repository è pubblico**: nessuna chiave può stare nel codice, vivono come variabili d'ambiente.
- **L'architettura a file unico senza framework non è un vincolo**: è l'implementazione attuale, che l'utente ha scelto di non vincolare.
- Tensione da tenere presente: il sito è pensato per quattro persone, ma l'indirizzo Vercel è **raggiungibile da chiunque lo conosca**. Non è protetto da password.
- In Corea, da ottobre 2026, il programma ha una notte in Giappone (Tsushima, 4–5 aprile) e i due voli interni (Busan–Jeju il 7, Jeju–Seul il 9) **sono comprati**. **Non sono prenotati** il treno Seul–Busan del 3 e le due navi per Tsushima, e la nave della sera del 4 non risulta negli orari trovati: il sito deve continuare a distinguere ciò che è comprato da ciò che non lo è, e dichiarare quello che non torna.

## Brand Commitments

- Nome: **Patagucci Trips**.
- **Solo italiano**, in ogni parte del sito.
- **Niente gergo tecnico** rivolto a chi sviluppa: nessun nome di servizio, CORS, variabile d'ambiente, percorso `/api/...`, codice di stato o messaggio d'errore grezzo. La diagnosi tecnica va nei log privati, mai in pagina.
- **Niente fonti private**: mai riferimenti a Revolut, Instagram o altre fonti personali da cui provengono i dati.
- I quattro soprannomi e le loro caratterizzazioni sono voce stabilita, non decorazione sostituibile.
- Il testo non racconta come è stato scritto: niente note in prima persona sul processo.
- **Voce da diario**: prima persona plurale, al presente o al futuro vicino. Niente impressioni inventate: i viaggi non sono ancora fatti. Le informazioni pure (leggi, regole, prezzi) possono restare impersonali.
- **Il logo è quello vero del gruppo** (progetto «menu cena kiki/logo-animato»: cielo verde, banda rossa, montagne nere con la cresta bianca, scritta crema, aereo Royal Brunico). Non se ne disegnano versioni inventate.

## Evidence on Hand

- **Voli comprati**, con numeri reali: Etihad `7GJHW8` (EY 82/822 all'andata, EY 499/81 al ritorno), Royal Brunei `BI 652` e `BI 421`. I due voli interni coreani sono comprati, ma di loro abbiamo solo data e orario (arrivo a Jeju alle 11:00 del 7, volo per Seul alle 20:45 del 9): compagnia e numero mancano.
- **Foto** in `foto/destinazioni/`, da Wikimedia Commons, ognuna con autore e licenza citati nel piè di pagina della scheda.
- Eccezione nota: `bn-royalbrunico.jpg` è un fotomontaggio fornito dal gruppo, **senza autore né licenza noti** — non ha crediti perché non ne esistono. Ogni altra immagine di provenienza esterna porta autore e licenza nel piè di pagina della sua scheda. L'intestazione della home ha una foto del gruppo, che non ha crediti come tutte le foto del gruppo.
- **Elenchi dei paesi visitati** per persona, dai registri del gruppo. Quello di Manu potrebbe essere incompleto. A ottobre 2026 Bacci ha aggiunto Macedonia del Nord e Kosovo per sé, Mala e Manu.
- **I cinque ricordi della copertina** (Machu Picchu, Salar di Uyuni, i fenicotteri, Sol de Mañana, Palccoyo) vengono dal diario del Sud America, l'unico viaggio fatto in quattro, e li ha scelti il gruppo.
- **Logo a livelli** in `assets/logo/` (cielo, banda rossa, aereo come immagini; montagne, cresta e lettere come contorni in `_sources/logo/forme.json`), presi dal logo animato del gruppo: nessuna generazione.
- **«Patagucci song»** (`assets/audio/patagucci-song.mp3`), fornita dal gruppo: parte con la copertina d'ingresso e continua dentro il sito, dove un tasto la spegne e la riaccende. Sulla copertina il tasto non c'è, per scelta del gruppo.
- Non esistono testimonianze, clienti, prezzi di vendita o metriche: non è un prodotto commerciale e non deve inventarseli.

## Product Principles

1. **Fatti verificati, o si dichiara il buco.** Ogni dato porta la fonte; quando il dato non c'è, lo si scrive invece di stimarlo.
2. **Racconta, non elenca.** I viaggi sono già decisi e il sito li racconta come un diario: le sezioni che argomentavano la scelta non hanno più ragione di esistere, e quelle pratiche parlano al noi invece che all'imperativo.
3. **Comprato e non comprato restano distinti.** Un volo da prenotare non deve mai sembrare prenotato.
4. **Parla come il gruppo**: italiano, soprannomi, nessun gergo tecnico, nessuna nota sul processo.
5. **Le fonti private restano fuori dalla pagina**, anche quando i dati che ne derivano ci stanno.
