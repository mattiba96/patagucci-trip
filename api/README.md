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

## Ognuno può votare solo per sé

La prima volta che un nome viene usato, il client manda una **chiave personale**
generata sul dispositivo (header `x-voti-chiave`) e il server ne salva l'impronta
SHA-256 accanto al voto. Da quel momento **solo chi ha quella chiave** può
modificare o cancellare quel voto: chiunque altro riceve `403 nome_occupato`.

L'impronta non esce mai dall'API: nelle risposte compare solo `protetto: true`.

Chi arriva per primo su un nome se lo prende. Se qualcuno perde la chiave
(cambio telefono, cronologia cancellata) perde il controllo di quel nome: dalla
pagina si usa **"La mia chiave"** per copiarla su un altro dispositivo, o per
incollarne una che si aveva già. In alternativa si vota con un altro nome e si
cancella il vecchio da un dispositivo che ha ancora la chiave.

## Azzerare tutti i voti

Serve la variabile d'ambiente **`VOTI_SEGRETO`** (Vercel → Settings → Environment
Variables, poi redeploy). Da quel momento:

```
curl -X DELETE -H "x-voti-segreto: IL_TUO_SEGRETO" \
  "https://patagucci-trip.vercel.app/api/voti?tutto=1"
```

`VOTI_SEGRETO` **non** blocca il voto normale: a quello pensano le chiavi
personali. Serve solo per l'azzeramento totale.

Per cancellare un voto singolo non serve nulla di tutto questo: chi l'ha
espresso lo azzera dalla propria pagina, con **Azzera il mio voto**.
