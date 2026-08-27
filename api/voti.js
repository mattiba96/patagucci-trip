// Mini API dei voti — Vercel Function, nessuna dipendenza.
//
// Storage: Redis via API REST di Upstash (l'integrazione "Upstash for Redis"
// del marketplace Vercel imposta da sola le due variabili qui sotto).
// Se mancano, l'API risponde 503 con errore "non_configurato" e la pagina
// ricade da sola sulla modalita' link, che continua a funzionare.
//
//   GET    /api/voti            -> { voti: {...}, aggiornato }
//   POST   /api/voti            -> body { nome, picks: [suf,...] }  (max 3)
//   DELETE /api/voti?nome=Kiki  -> rimuove quel votante
//
// Ogni votante e' un campo separato di una hash: due persone che votano
// insieme non si sovrascrivono a vicenda (niente leggi-modifica-riscrivi).

const CHIAVE = 'patagucci:voti';
const MAX_SCELTE = 3;
const MAX_VOTANTI = 50;
const MAX_NOME = 24;

// Le mete valide: una scelta fuori da questa lista viene scartata.
const METE = ['np', 'pk', 'za', 'in', 'ug', 'tz', 'uk', 'gl', 'cx', 'ge'];

// I nomi cambiano a seconda di come e' stato collegato il database
// (integrazione KV storica, marketplace Upstash, collegamento manuale).
const URL_REDIS =
  process.env.KV_REST_API_URL ||
  process.env.UPSTASH_REDIS_REST_URL ||
  process.env.REDIS_REST_API_URL ||
  process.env.STORAGE_REST_API_URL;
const TOKEN_REDIS =
  process.env.KV_REST_API_TOKEN ||
  process.env.UPSTASH_REDIS_REST_TOKEN ||
  process.env.REDIS_REST_API_TOKEN ||
  process.env.STORAGE_REST_API_TOKEN;
// Facoltativa: se impostata, ogni scrittura deve portare lo stesso valore
// nell'header x-voti-segreto. Serve solo a evitare che un estraneo che
// scopre l'URL possa scrivere; in lettura non cambia nulla.
const SEGRETO = process.env.VOTI_SEGRETO || null;

async function redis(comando) {
  const r = await fetch(URL_REDIS, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${TOKEN_REDIS}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(comando),
  });
  if (!r.ok) throw new Error(`Redis ${r.status}: ${await r.text()}`);
  const dati = await r.json();
  if (dati.error) throw new Error(`Redis: ${dati.error}`);
  return dati.result;
}

// HGETALL torna un array piatto [campo, valore, campo, valore, ...]
function aVoti(piatto) {
  const voti = {};
  if (!Array.isArray(piatto)) return voti;
  for (let i = 0; i < piatto.length; i += 2) {
    const nome = piatto[i];
    try {
      const v = JSON.parse(piatto[i + 1]);
      if (v && Array.isArray(v.picks)) {
        voti[nome] = { picks: v.picks, ts: Number(v.ts) || 0 };
      }
    } catch (e) {
      // un campo illeggibile non deve far cadere tutta la risposta
    }
  }
  return voti;
}

function ripulisciNome(v) {
  return String(v == null ? '' : v).trim().slice(0, MAX_NOME);
}

function ripulisciScelte(v) {
  if (!Array.isArray(v)) return null;
  const viste = new Set();
  const out = [];
  for (const s of v) {
    if (typeof s !== 'string' || !METE.includes(s) || viste.has(s)) continue;
    viste.add(s);
    out.push(s);
  }
  return out.length > MAX_SCELTE ? null : out;
}

// Elenca quali variabili di storage sono presenti. Riporta SOLO i nomi:
// nessun valore, nessun token, mai.
const NOMI_NOTI = [
  'KV_REST_API_URL', 'KV_REST_API_TOKEN', 'KV_URL', 'KV_REST_API_READ_ONLY_TOKEN',
  'UPSTASH_REDIS_REST_URL', 'UPSTASH_REDIS_REST_TOKEN',
  'REDIS_REST_API_URL', 'REDIS_REST_API_TOKEN', 'REDIS_URL',
  'STORAGE_REST_API_URL', 'STORAGE_REST_API_TOKEN',
  'POSTGRES_URL', 'POSTGRES_PRISMA_URL', 'DATABASE_URL', 'NEON_DATABASE_URL',
  'BLOB_READ_WRITE_TOKEN', 'EDGE_CONFIG',
];

function diagnostica() {
  const presenti = NOMI_NOTI.filter((n) => !!process.env[n]);
  // Prendo anche eventuali nomi non previsti, per capire che integrazione e'.
  const altri = Object.keys(process.env).filter(
    (n) =>
      !NOMI_NOTI.includes(n) &&
      /(REDIS|UPSTASH|POSTGRES|DATABASE|^KV_|BLOB_|EDGE_CONFIG)/i.test(n)
  );
  return {
    variabiliTrovate: presenti,
    altreVariabiliDiStorage: altri,
    redisPronto: !!(URL_REDIS && TOKEN_REDIS),
    nota: 'Solo nomi di variabile, mai i valori.',
  };
}

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'GET' && req.query && req.query.diagnostica) {
    return res.status(200).json(diagnostica());
  }

  if (!URL_REDIS || !TOKEN_REDIS) {
    return res.status(503).json({
      errore: 'non_configurato',
      messaggio:
        'Manca lo storage. Su Vercel: Storage -> collega il database a questo progetto, poi rifai il deploy.',
      diagnostica: diagnostica(),
    });
  }

  try {
    if (req.method === 'GET') {
      const voti = aVoti(await redis(['HGETALL', CHIAVE]));
      return res.status(200).json({ voti, aggiornato: Date.now() });
    }

    if (req.method === 'POST') {
      if (SEGRETO && req.headers['x-voti-segreto'] !== SEGRETO) {
        return res.status(401).json({ errore: 'non_autorizzato' });
      }

      const body =
        typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body || {};

      const nome = ripulisciNome(body.nome);
      if (!nome) return res.status(400).json({ errore: 'nome_mancante' });

      if (!Array.isArray(body.picks)) {
        return res
          .status(400)
          .json({ errore: 'scelte_non_valide', messaggio: 'Le scelte devono essere una lista.' });
      }
      const picks = ripulisciScelte(body.picks);
      if (picks === null) {
        return res
          .status(400)
          .json({ errore: 'troppe_scelte', messaggio: `Al massimo ${MAX_SCELTE} mete.` });
      }

      // Tetto sui votanti: non e' sicurezza, e' un freno agli abusi.
      const esistenti = await redis(['HKEYS', CHIAVE]);
      if (
        Array.isArray(esistenti) &&
        esistenti.length >= MAX_VOTANTI &&
        !esistenti.includes(nome)
      ) {
        return res.status(429).json({ errore: 'troppi_votanti' });
      }

      await redis(['HSET', CHIAVE, nome, JSON.stringify({ picks, ts: Date.now() })]);
      const voti = aVoti(await redis(['HGETALL', CHIAVE]));
      return res.status(200).json({ voti, aggiornato: Date.now() });
    }

    if (req.method === 'DELETE') {
      if (SEGRETO && req.headers['x-voti-segreto'] !== SEGRETO) {
        return res.status(401).json({ errore: 'non_autorizzato' });
      }
      const nome = ripulisciNome(req.query && req.query.nome);
      if (!nome) return res.status(400).json({ errore: 'nome_mancante' });

      await redis(['HDEL', CHIAVE, nome]);
      const voti = aVoti(await redis(['HGETALL', CHIAVE]));
      return res.status(200).json({ voti, aggiornato: Date.now() });
    }

    res.setHeader('Allow', 'GET, POST, DELETE');
    return res.status(405).json({ errore: 'metodo_non_ammesso' });
  } catch (e) {
    return res.status(502).json({ errore: 'storage_non_raggiungibile', messaggio: String(e.message || e) });
  }
}
