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

## Positioning

Non è un pianificatore di viaggi generico: è il registro di *questi* viaggi. Ogni affermazione fattuale — orari, prezzi, regole, date di fioritura, divieti — è ricercata e porta la sua fonte con la data di verifica, e dove il dato non esiste o non è verificabile lo si dichiara invece di riempire il buco. È la differenza fra una pagina che si può usare per prenotare e una che si può solo leggere.

## Operating Context

- Tutto in **italiano**.
- I viaggi pubblicati sono **confermati e in buona parte pagati**: i contenuti devono corrispondere alle prenotazioni reali, non a un'ipotesi.
- I dati arrivano dalle prenotazioni del gruppo e dalle loro schermate, passate a mano.
- Le mete archiviate restano come sorgenti in `_sources/` anche quando non sono pubblicate: rimetterne una in linea è una riga di configurazione.

## Capabilities and Constraints

- Sito statico generato da `_sources/build.py`, che unisce una pagina HTML per meta in un unico `index.html`; le mete si cambiano senza ricaricare.
- Pubblicato su Vercel da GitHub, con funzioni serverless in `api/`: chat sul contenuto del sito, ricerca voli, ricerca concerti.
- **Il repository è pubblico**: nessuna chiave può stare nel codice, vivono come variabili d'ambiente.
- **L'architettura a file unico senza framework non è un vincolo**: è l'implementazione attuale, che l'utente ha scelto di non vincolare.
- Tensione da tenere presente: il sito è pensato per quattro persone, ma l'indirizzo Vercel è **raggiungibile da chiunque lo conosca**. Non è protetto da password.
- Due voli interni coreani (Busan–Jeju, Jeju–Seul) **non sono prenotati**: il sito deve continuare a distinguere ciò che è comprato da ciò che non lo è.

## Brand Commitments

- Nome: **Patagucci Trips**.
- **Solo italiano**, in ogni parte del sito.
- **Niente gergo tecnico** rivolto a chi sviluppa: nessun nome di servizio, CORS, variabile d'ambiente, percorso `/api/...`, codice di stato o messaggio d'errore grezzo. La diagnosi tecnica va nei log privati, mai in pagina.
- **Niente fonti private**: mai riferimenti a Revolut, Instagram o altre fonti personali da cui provengono i dati.
- I quattro soprannomi e le loro caratterizzazioni sono voce stabilita, non decorazione sostituibile.
- Il testo non racconta come è stato scritto: niente note in prima persona sul processo.

## Evidence on Hand

- **Voli comprati**, con numeri reali: Etihad `7GJHW8` (EY 82/822 all'andata, EY 499/81 al ritorno), Royal Brunei `BI 652` e `BI 421`.
- **Foto** in `foto/destinazioni/`, da Wikimedia Commons, ognuna con autore e licenza citati nel piè di pagina della scheda.
- Eccezione nota: `bn-royalbrunico.jpg` è un fotomontaggio fornito dal gruppo, **senza autore né licenza noti** — non ha crediti perché non ne esistono. Ogni altra immagine di provenienza esterna porta autore e licenza nel piè di pagina della sua scheda, compresa quella dell'intestazione della home (Hunza Valley, Maqalam97, CC BY-SA 4.0).
- **Elenchi dei paesi visitati** per persona, dai registri del gruppo. Quello di Manu potrebbe essere incompleto.
- Non esistono testimonianze, clienti, prezzi di vendita o metriche: non è un prodotto commerciale e non deve inventarseli.

## Product Principles

1. **Fatti verificati, o si dichiara il buco.** Ogni dato porta la fonte; quando il dato non c'è, lo si scrive invece di stimarlo.
2. **Serve a organizzare, non a convincere.** I viaggi sono già decisi: le sezioni che argomentavano la scelta non hanno più ragione di esistere.
3. **Comprato e non comprato restano distinti.** Un volo da prenotare non deve mai sembrare prenotato.
4. **Parla come il gruppo**: italiano, soprannomi, nessun gergo tecnico, nessuna nota sul processo.
5. **Le fonti private restano fuori dalla pagina**, anche quando i dati che ne derivano ci stanno.
