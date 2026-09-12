// Ponte fra il sito e SerpApi (motore Google Flights).
//
// Serve per due motivi, nessuno dei quali aggirabile lato pagina:
//  1. SerpApi non manda header CORS, quindi il browser non puo' chiamarla.
//  2. Il repo e' pubblico: la chiave non puo' stare nell'HTML. Qui vive
//     come variabile d'ambiente su Vercel (SERPAPI_KEY) e non esce mai.
//
// Il piano free ha 250 ricerche al mese e questo endpoint e' raggiungibile
// da chiunque: da qui i tre freni piu' sotto (riserva, tetto orario, cache).

const SERPAPI = 'https://serpapi.com/search.json';
const ACCOUNT = 'https://serpapi.com/account';

// Sotto questa soglia la funzione si rifiuta di cercare: qualunque cosa
// succeda restano crediti per le ricerche che contano davvero.
const RISERVA_CREDITI = 20;

// Tetto per singolo IP, finestra scorrevole di un'ora.
const LIMITE_ORARIO = 40;

// Le lambda restano calde qualche minuto: cache e contatori vivono li'.
// Non e' persistente ed e' giusto cosi' — servono a smorzare le raffiche,
// non a garantire un conteggio esatto.
const cache = new Map();
const chiamate = new Map();
const TTL_CACHE = 30 * 60 * 1000;

function pulisci(mappa, ora, finestra) {
  for (const [k, v] of mappa) {
    if (ora - (Array.isArray(v) ? Math.max(...v) : v.quando) > finestra) mappa.delete(k);
  }
}

function ipDi(req) {
  const fwd = req.headers['x-forwarded-for'];
  return (Array.isArray(fwd) ? fwd[0] : (fwd || '')).split(',')[0].trim() || 'sconosciuto';
}

// Solo codici IATA: tre lettere, fino a cinque aeroporti di partenza.
// Google Flights accetta la lista separata da virgola e risponde col piu'
// economico fra tutti, a un credito solo invece che uno per aeroporto.
function codici(valore, max) {
  const lista = String(valore || '')
    .toUpperCase()
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);
  if (!lista.length || lista.length > max) return null;
  if (!lista.every((c) => /^[A-Z]{3}$/.test(c))) return null;
  return lista.join(',');
}

// Data ISO, non nel passato e non oltre un anno: Google Flights non ha
// prezzi piu' in la' e una data assurda brucerebbe un credito per nulla.
function data(valore) {
  const s = String(valore || '');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(s)) return null;
  const d = new Date(s + 'T12:00:00Z');
  if (Number.isNaN(d.getTime()) || d.toISOString().slice(0, 10) !== s) return null;
  const oggi = new Date();
  oggi.setUTCHours(0, 0, 0, 0);
  const limite = new Date(oggi.getTime() + 400 * 86400000);
  if (d < oggi || d > limite) return null;
  return s;
}

async function crediti(chiave) {
  const r = await fetch(ACCOUNT + '?api_key=' + chiave);
  if (!r.ok) throw new Error('SerpApi /account ha risposto ' + r.status);
  const d = await r.json();
  return {
    rimasti: d.total_searches_left,
    totali: d.searches_per_month,
    usateQuestoMese: d.this_month_usage,
    rinnovo: d.plan_renewal_date,
  };
}

// Dalla risposta di SerpApi tengo solo cio' che la pagina disegna: la
// risposta piena e' ~200 kB per ricerca, quasi tutto rumore.
function screma(volo) {
  const tratte = volo.flights || [];
  const primo = tratte[0] || {};
  const ultimo = tratte[tratte.length - 1] || {};
  return {
    prezzo: volo.price,
    durata: volo.total_duration,
    scali: (volo.layovers || []).map((l) => ({ dove: l.id, minuti: l.duration })),
    compagnie: [...new Set(tratte.map((t) => t.airline).filter(Boolean))],
    logo: volo.airline_logo,
    da: (primo.departure_airport || {}).id,
    daNome: (primo.departure_airport || {}).name,
    a: (ultimo.arrival_airport || {}).id,
    aNome: (ultimo.arrival_airport || {}).name,
    partenza: (primo.departure_airport || {}).time,
    arrivo: (ultimo.arrival_airport || {}).time,
    co2: (volo.carbon_emissions || {}).this_flight,
  };
}

// Il nome canonico e' SERPAPI_KEY, ma sbagliarne la forma e' facile e il
// sintomo (500 a ogni ricerca) non dice quale sia il problema. Accettare le
// grafie ovvie costa nulla e risparmia un giro di deploy.
const NOMI_CHIAVE = ['SERPAPI_KEY', 'SERP_API_KEY', 'SERPAPI_API_KEY', 'SERPAPI_TOKEN', 'SERPAPI'];

function trovaChiave() {
  for (const n of NOMI_CHIAVE) {
    const v = (process.env[n] || '').trim();
    if (v) return v;
  }
  return null;
}

// Distingue i due casi che si confondono: nome sbagliato (variabili
// personali ci sono, nessuna somiglia) e ambiente sbagliato o progetto
// sbagliato (alla funzione non arriva nessuna variabile personale).
// Riporta solo NOMI, e solo quelli che contengono "serp": nessun valore.
function diagnosiChiave() {
  const sistema = /^(VERCEL|AWS|NODE|NEXT|LAMBDA|_|PATH$|HOME$|TZ$|LANG$|PWD$|SHLVL$|TMPDIR$|LD_|EXEC_|AMZN_|X_)/;
  const tutti = Object.keys(process.env);
  const personali = tutti.filter((k) => !sistema.test(k));
  const somiglianti = tutti.filter((k) => /serp/i.test(k));
  // I nomi per esteso finiscono nei log del progetto, che sono privati,
  // e non nella risposta, che e' pubblica. I valori non escono mai.
  console.log('[diagnosi chiave] nomi non di sistema visti dalla funzione:', personali.join(', ') || '(nessuno)');
  return {
    cercate: NOMI_CHIAVE,
    trovateSimili: somiglianti,
    quanteVariabiliPersonali: personali.length,
    interpretazione: somiglianti.length
      ? 'Una variabile con "serp" nel nome esiste ma non ha uno dei nomi attesi, oppure e\' vuota. Rinominala in SERPAPI_KEY.'
      : personali.length
        ? 'Alla funzione arrivano ' + personali.length + ' variabili tue, ma nessuna con "serp" nel nome: il nome e\' diverso da quelli cercati.'
        : 'Alla funzione non arriva nessuna variabile personale: la variabile non e\' spuntata per l\'ambiente Production, oppure e\' su un altro progetto Vercel.',
  };
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'GET') return res.status(405).json({ errore: 'Solo GET.' });

  const chiave = trovaChiave();
  if (!chiave) {
    return res.status(500).json({ errore: 'SERPAPI_KEY non configurata su Vercel.', diagnosi: diagnosiChiave() });
  }

  const q = req.query || {};
  const azione = q.action || q.azione || 'cerca';

  try {
    // Questa non consuma ricerche: serve alla pagina per mostrare il
    // contatore prima di far partire una scansione.
    if (azione === 'crediti') {
      res.setHeader('Cache-Control', 's-maxage=60');
      return res.status(200).json({ ok: true, crediti: await crediti(chiave) });
    }

    if (azione !== 'cerca') return res.status(400).json({ errore: 'Azione sconosciuta: ' + azione });

    const partenze = codici(q.da, 5);
    const arrivo = codici(q.a, 1);
    const andata = data(q.andata);
    const ritorno = q.ritorno ? data(q.ritorno) : null;

    if (!partenze) return res.status(400).json({ errore: 'Aeroporti di partenza non validi (max 5 codici IATA).' });
    if (!arrivo) return res.status(400).json({ errore: 'Aeroporto di arrivo non valido (un codice IATA).' });
    if (!andata) return res.status(400).json({ errore: 'Data di andata non valida (YYYY-MM-DD, entro un anno).' });
    if (q.ritorno && !ritorno) return res.status(400).json({ errore: 'Data di ritorno non valida.' });
    if (ritorno && ritorno < andata) return res.status(400).json({ errore: 'Il ritorno precede l\'andata.' });

    const adulti = Math.min(Math.max(parseInt(q.adulti, 10) || 4, 1), 9);

    const firma = [partenze, arrivo, andata, ritorno, adulti].join('|');
    const ora = Date.now();

    const salvata = cache.get(firma);
    if (salvata && ora - salvata.quando < TTL_CACHE) {
      return res.status(200).json({ ...salvata.dato, daCache: true });
    }

    // Il tetto per IP si applica solo alle ricerche vere: una risposta
    // dalla cache non tocca SerpApi e non ha motivo di contare.
    pulisci(chiamate, ora, 3600000);
    const ip = ipDi(req);
    const recenti = (chiamate.get(ip) || []).filter((t) => ora - t < 3600000);
    if (recenti.length >= LIMITE_ORARIO) {
      return res.status(429).json({
        errore: 'Troppe ricerche da questo indirizzo in un\'ora (tetto: ' + LIMITE_ORARIO + '). Riprova piu\' tardi.',
      });
    }

    const conto = await crediti(chiave);
    if (conto.rimasti <= RISERVA_CREDITI) {
      return res.status(429).json({
        errore:
          'Crediti SerpApi quasi esauriti (' + conto.rimasti + ' rimasti, riserva ' + RISERVA_CREDITI +
          '). Si riparte il ' + conto.rinnovo + '.',
        crediti: conto,
      });
    }

    const url = new URL(SERPAPI);
    url.searchParams.set('engine', 'google_flights');
    url.searchParams.set('departure_id', partenze);
    url.searchParams.set('arrival_id', arrivo);
    url.searchParams.set('outbound_date', andata);
    if (ritorno) {
      url.searchParams.set('return_date', ritorno);
      url.searchParams.set('type', '1'); // andata e ritorno
    } else {
      url.searchParams.set('type', '2'); // sola andata
    }
    url.searchParams.set('adults', String(adulti));
    url.searchParams.set('currency', 'EUR');
    url.searchParams.set('hl', 'it');
    url.searchParams.set('gl', 'it');
    url.searchParams.set('api_key', chiave);

    chiamate.set(ip, [...recenti, ora]);

    const r = await fetch(url, { signal: AbortSignal.timeout(25000) });
    const dato = await r.json();

    if (dato.error) {
      // Nessun volo su quella tratta/data non e' un guasto: la pagina lo
      // mostra come casella vuota e va avanti con le altre date.
      const vuoto = /hasn't returned any results|no results/i.test(dato.error);
      return res.status(vuoto ? 200 : 502).json(
        vuoto
          ? { ok: true, voli: [], vuoto: true, crediti: { rimasti: conto.rimasti - 1, totali: conto.totali } }
          : { errore: 'SerpApi: ' + dato.error }
      );
    }

    const voli = [...(dato.best_flights || []), ...(dato.other_flights || [])]
      .map(screma)
      .filter((v) => typeof v.prezzo === 'number')
      .sort((a, b) => a.prezzo - b.prezzo)
      .slice(0, 6);

    const insights = dato.price_insights || {};
    const risposta = {
      ok: true,
      da: partenze,
      a: arrivo,
      andata,
      ritorno,
      voli,
      livelloPrezzo: insights.price_level || null,
      rangeTipico: insights.typical_price_range || null,
      link: (dato.search_metadata || {}).google_flights_url || null,
      crediti: { rimasti: conto.rimasti - 1, totali: conto.totali },
    };

    cache.set(firma, { quando: ora, dato: risposta });
    pulisci(cache, ora, TTL_CACHE);

    return res.status(200).json(risposta);
  } catch (e) {
    return res.status(502).json({ errore: 'Ricerca fallita: ' + (e && e.message ? e.message : String(e)) });
  }
};
