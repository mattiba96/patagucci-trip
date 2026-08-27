# Mini API dei voti

Una sola funzione, `voti.js`, senza dipendenze. Vercel la pubblica da sola:
qualsiasi file dentro `/api` diventa un endpoint.

## Endpoint

| Metodo | Percorso | Cosa fa |
|---|---|---|
| `GET` | `/api/voti` | Restituisce tutti i voti |
| `POST` | `/api/voti` | Corpo `{ "nome": "Kiki", "picks": ["np","tz"] }` — massimo 3 mete |
| `DELETE` | `/api/voti?nome=Kiki` | Cancella quel votante |

Tutte rispondono `{ voti: { nome: { picks, ts } }, aggiornato }`.

## Serve collegare lo storage

Finché non lo colleghi, l'API risponde **503 `non_configurato`** e la pagina
votazioni ricade da sola sulla modalità link — continua a funzionare, ma ognuno
vede solo se stesso.

Per attivarla, dal pannello Vercel del progetto:

1. **Storage → Upstash for Redis → Create / Connect**
2. Collega il database a questo progetto
3. **Redeploy**

L'integrazione imposta da sola `KV_REST_API_URL` e `KV_REST_API_TOKEN`, che sono
le uniche variabili che servono. La funzione accetta anche i nomi
`UPSTASH_REDIS_REST_URL` / `UPSTASH_REDIS_REST_TOKEN`.

## Scrittura protetta (facoltativa)

L'endpoint è pubblico: chiunque conosca l'URL può votare. Per il gruppo va bene,
ma se vuoi chiuderlo imposta la variabile d'ambiente **`VOTI_SEGRETO`**: da quel
momento `POST` e `DELETE` richiedono l'header `x-voti-segreto` con lo stesso
valore (la lettura resta libera).

Attenzione: la pagina **non** manda quell'header. Se imposti `VOTI_SEGRETO`,
i voti dal sito smettono di salvarsi online e si torna alla modalità link.
Serve solo se vuoi usare l'API a mano.

## Come sono salvati

Una hash Redis, `patagucci:voti`, con **un campo per votante**. Ognuno scrive
solo il proprio campo: due persone che votano nello stesso momento non si
sovrascrivono a vicenda.
