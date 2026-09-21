// Cercare sul web passando da OneProvider.
//
// Il gateway accetta lo strumento web_search ma non e' quello vero di
// Anthropic: cerca davvero, poi incolla l'elenco dei risultati come se
// fosse la risposta — in inglese, numerato — e si ferma. E come query
// usa l'ultimo messaggio dell'utente parola per parola.
//
// Da qui i due tempi: prima una chiamata il cui unico scopo e' far
// cercare al gateway le parole che gli diamo noi, poi una seconda che
// quell'elenco se lo legge e scrive la risposta. E' lo stesso giro che
// fa api/chat.js; sta qui perche' lo usa anche api/kpop.js.

const Anthropic = require('@anthropic-ai/sdk');

const MODELLO = 'claude-haiku-4-5-20251001';
const BASE_ONEPROVIDER = 'https://api.oneprovider.dev';
const NOMI_CHIAVE = ['ANTHROPIC_API_KEY', 'CLAUDE_API_KEY', 'ANTHROPIC_KEY', 'ANTHROPIC_TOKEN',
                     'ONEPROVIDER_API_KEY', 'LLM_API_KEY'];

function normalizza(s) { return s.toUpperCase().replace(/[^A-Z]/g, ''); }

function trovaChiave() {
  const attesi = NOMI_CHIAVE.map(normalizza);
  for (const [nome, valore] of Object.entries(process.env)) {
    if (attesi.indexOf(normalizza(nome)) >= 0 && String(valore || '').trim()) {
      return String(valore).trim();
    }
  }
  return null;
}

function clienteDi(chiave) {
  const base = process.env.LLM_BASE_URL || (chiave.startsWith('sk-ant-') ? null : BASE_ONEPROVIDER);
  return new Anthropic(Object.assign({ apiKey: chiave, maxRetries: 0 }, base ? { baseURL: base } : {}));
}

// Gli indirizzi dell'elenco, col titolo in grassetto che li precede. Se
// il gateway cambiasse formato resterebbero gli indirizzi, che e' il
// pezzo che conta.
function indirizziDa(testo) {
  const trovati = [];
  let titolo = '';
  for (const riga of String(testo || '').split('\n')) {
    const t = riga.match(/\*\*(.+?)\*\*/);
    if (t) titolo = t[1].trim();
    const u = riga.match(/https?:\/\/[^\s)\]]+/);
    if (u && !trovati.some((f) => f.url === u[0])) {
      trovati.push({ url: u[0], titolo: titolo || u[0] });
    }
  }
  return trovati;
}

async function testoDi(cliente, corpo, tempo) {
  const flusso = cliente.messages.stream(corpo, { timeout: Math.max(2000, tempo), maxRetries: 0 });
  let testo = '';
  for await (const evento of flusso) {
    if (evento.type === 'content_block_delta' && evento.delta.type === 'text_delta') {
      testo += evento.delta.text;
    }
  }
  await flusso.finalMessage();
  return testo;
}

// query: una o piu' stringhe, una ricerca per ognuna.
// Torna { testo, fonti, ricercaFatta } — la stessa forma di chiediGemini,
// cosi' chi chiama puo' tenere i due motori uno accanto all'altro.
async function cercaERiassumi({ sistema, domanda, query, maxToken = 1600, tempo = 40000 }) {
  const chiave = trovaChiave();
  if (!chiave) {
    const e = new Error('Nessuna chiave per il motore.');
    e.codice = 'senza-chiave';
    throw e;
  }
  const cliente = clienteDi(chiave);
  const scade = Date.now() + tempo;
  const resta = () => scade - Date.now();

  const richieste = [].concat(query).filter(Boolean);
  const pezzi = [];
  for (const q of richieste) {
    if (resta() < 12000) break;   // meglio una ricerca sola che un timeout
    try {
      pezzi.push(await testoDi(cliente, {
        model: MODELLO,
        max_tokens: 1200,
        tools: [{ type: 'web_search_20250305', name: 'web_search', max_uses: 2,
                  user_location: { type: 'approximate', country: 'IT', timezone: 'Europe/Rome' } }],
        messages: [{ role: 'user', content: q }],
      }, Math.min(20000, resta() - 8000)));
    } catch (e) {
      console.warn('[ricerca] "' + q + '" non ha risposto:', e && e.message ? e.message : e);
    }
  }

  const grezzo = pezzi.join('\n\n').trim();
  const fonti = indirizziDa(grezzo);

  const materiale = grezzo
    ? 'Qui sotto ci sono i risultati grezzi di una ricerca sul web fatta adesso: titoli, righe di '
      + 'descrizione e indirizzi, in ordine sparso e in parte fuori tema.\n\n'
      + '=== RISULTATI ===\n' + grezzo.slice(0, 12000) + '\n=== FINE RISULTATI ===\n\n'
      + 'Non ricopiarli e non elencarli tutti: leggili e scrivi tu la risposta, tenendo solo cio\' che '
      + 'c\'entra davvero. Quello che non trovi qui dentro non lo sai: non riempirlo a memoria.'
    : 'La ricerca sul web non ha risposto. Non hai risultati da leggere: dillo, invece di scrivere '
      + 'date o nomi a memoria.';

  const testo = await testoDi(cliente, {
    model: MODELLO,
    max_tokens: maxToken,
    system: [
      { type: 'text', text: sistema },
      { type: 'text', text: materiale },
    ],
    messages: [{ role: 'user', content: domanda }],
  }, Math.max(8000, resta()));

  return { testo: testo.trim(), fonti: fonti.slice(0, 6), ricercaFatta: Boolean(grezzo) };
}

module.exports = { cercaERiassumi };
