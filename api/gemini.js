// La rete di sicurezza del sito: Gemini.
//
// Serve a due cose.
//  1. Quando Haiku si inchioda — sovraccarico, limite, gateway giu' — la
//     chat non deve morire: riscrive la risposta da qui.
//  2. La ricerca dei concerti K-pop, che gira solo su Gemini.
//
// La chiave vive come variabile d'ambiente su Vercel (GEMINI_API_KEY),
// mai nell'HTML: il repo del sito e' pubblico.
//
// Sul modello non c'e' un nome scritto a mano. I nomi dei Flash cambiano
// ogni pochi mesi e un nome morto qui vorrebbe dire 404 silenziosi, cosi'
// la lista dei modelli la si chiede all'API e si prende il Flash piu'
// recente che risponde. GEMINI_MODEL, se c'e', ha la precedenza.

const BASE = 'https://generativelanguage.googleapis.com/v1beta';

const NOMI_CHIAVE = ['GEMINI_API_KEY', 'GOOGLE_API_KEY', 'GOOGLE_AI_API_KEY'];

function chiaveGemini() {
  for (const nome of NOMI_CHIAVE) {
    const v = (process.env[nome] || '').trim();
    if (v) return v;
  }
  // Tollerante sul nome: maiuscole e separatori non devono far fallire
  // tutto solo perche' su Vercel e' stata scritta in un altro modo.
  const cercato = NOMI_CHIAVE.map((n) => n.replace(/[^a-z]/gi, '').toLowerCase());
  for (const [k, v] of Object.entries(process.env)) {
    if (cercato.includes(k.replace(/[^a-z]/gi, '').toLowerCase()) && (v || '').trim()) return v.trim();
  }
  return null;
}

// Il modello scelto resta in memoria finche' la lambda e' calda: la lista
// si chiede una volta, non a ogni domanda.
let modelloInUso = null;

async function scegliModello(chiave) {
  if (process.env.GEMINI_MODEL) return process.env.GEMINI_MODEL.trim();
  if (modelloInUso) return modelloInUso;

  try {
    const r = await fetch(`${BASE}/models?key=${encodeURIComponent(chiave)}&pageSize=200`, {
      signal: AbortSignal.timeout(10000),
    });
    const dato = await r.json();
    const modelli = (dato.models || [])
      .filter((m) => (m.supportedGenerationMethods || []).includes('generateContent'))
      .map((m) => String(m.name || '').replace(/^models\//, ''))
      // Solo i Flash: dall'aprile 2026 il piano gratuito e' Flash e
      // Flash-Lite, i Pro stanno dietro alla fatturazione.
      .filter((n) => /flash/i.test(n))
      // Niente anteprime, sperimentali e varianti a tema: durano poco.
      .filter((n) => !/(preview|exp|thinking|image|audio|tts|live|native)/i.test(n));

    // Prima il Flash pieno, poi il Flash-Lite che e' piu' povero; a
    // parita' di tipo, la versione piu' alta. In quest'ordine e non
    // mescolati, se no un 3.1-Lite scavalca un 3 pieno per un decimo.
    const versione = (n) => parseFloat((n.match(/(\d+(?:\.\d+)?)/) || [0, 0])[1]) || 0;
    modelli.sort((a, b) => {
      const liteA = /lite/i.test(a) ? 1 : 0, liteB = /lite/i.test(b) ? 1 : 0;
      if (liteA !== liteB) return liteA - liteB;
      return versione(b) - versione(a);
    });

    if (modelli.length) {
      modelloInUso = modelli[0];
      console.log('[gemini] modello scelto:', modelloInUso, '— candidati:', modelli.slice(0, 5).join(', '));
      return modelloInUso;
    }
    console.error('[gemini] nessun modello Flash nella lista, uso il nome di riserva');
  } catch (e) {
    console.error('[gemini] lista modelli non raggiungibile:', e && e.message ? e.message : e);
  }

  // Se la lista non risponde si tenta comunque: meglio un tentativo che
  // niente, e il chiamante sa gestire il fallimento.
  modelloInUso = 'gemini-2.5-flash';
  return modelloInUso;
}

function testoDi(dato) {
  const parti = ((dato.candidates || [])[0]?.content?.parts) || [];
  return parti.map((p) => p.text || '').join('').trim();
}

function fontiDi(dato) {
  const chunk = ((dato.candidates || [])[0]?.groundingMetadata?.groundingChunks) || [];
  const viste = new Set();
  const fonti = [];
  for (const c of chunk) {
    const url = c.web?.uri;
    if (!url || viste.has(url)) continue;
    viste.add(url);
    fonti.push({ url, titolo: c.web.title || url });
  }
  return fonti;
}

// Una domanda, una risposta.
//
// conRicerca chiede a Gemini di cercare su Google prima di rispondere.
// Attenzione: il grounding NON e' compreso nel piano gratuito — si paga a
// ricerca. Se la chiave non ce l'ha, la richiesta viene rifiutata e qui si
// ritenta senza strumento: torna comunque una risposta, ma scritta a
// memoria. Chi chiama lo sa da `ricercaFatta` e lo deve dire a schermo,
// perche' una data di concerto inventata e' peggio di nessuna data.
async function chiediGemini({ prompt, sistema, conRicerca = false, maxToken = 2000, timeout = 30000 }) {
  const chiave = chiaveGemini();
  if (!chiave) {
    const e = new Error('Gemini non configurato.');
    e.codice = 'senza-chiave';
    throw e;
  }
  const modello = await scegliModello(chiave);

  async function chiama(conStrumento) {
    const corpo = {
      contents: [{ role: 'user', parts: [{ text: prompt }] }],
      generationConfig: { maxOutputTokens: maxToken, temperature: 0.3 },
    };
    if (sistema) corpo.systemInstruction = { parts: [{ text: sistema }] };
    if (conStrumento) corpo.tools = [{ google_search: {} }];

    const r = await fetch(`${BASE}/models/${encodeURIComponent(modello)}:generateContent?key=${encodeURIComponent(chiave)}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(corpo),
      signal: AbortSignal.timeout(timeout),
    });
    const dato = await r.json().catch(() => ({}));
    if (!r.ok) {
      const msg = dato.error?.message || `HTTP ${r.status}`;
      const e = new Error(msg);
      e.stato = r.status;
      throw e;
    }
    return dato;
  }

  if (conRicerca) {
    try {
      const dato = await chiama(true);
      return { testo: testoDi(dato), fonti: fontiDi(dato), ricercaFatta: true, modello };
    } catch (e) {
      // Il piano gratuito rifiuta lo strumento: si riprova senza, e si
      // dichiara che non c'e' stata nessuna ricerca.
      console.error('[gemini] ricerca non disponibile, riprovo senza:', e.message);
    }
  }

  const dato = await chiama(false);
  return { testo: testoDi(dato), fonti: [], ricercaFatta: false, modello };
}

module.exports = { chiediGemini, chiaveGemini, scegliModello };
