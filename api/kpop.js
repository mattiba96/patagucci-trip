// "Ci sono concerti mentre ci siamo?"
//
// I calendari K-pop escono pochi mesi prima, quindi una lista scritta a
// mano sul sito nasce vecchia. Questo endpoint la chiede a Gemini ogni
// volta, con la ricerca su Google accesa quando la chiave ce l'ha.
//
// Il punto delicato: se la ricerca non e' disponibile (il grounding non e'
// compreso nel piano gratuito) la risposta arriva lo stesso, ma scritta a
// memoria dal modello. In quel caso non si spacciano date per vere —
// `ricercaFatta: false` torna al sito, che lo scrive a chiare lettere.

const { chiediGemini } = require('./gemini.js');

// Le date del viaggio, che sono il motivo della domanda.
const DA = '2 aprile 2027';
const A = '18 aprile 2027';

const LIMITE_ORARIO = 10;
const chiamate = new Map();

function ipDi(req) {
  const h = req.headers || {};
  return (h['x-forwarded-for'] || '').split(',')[0].trim() || h['x-real-ip'] || 'ignoto';
}

const SISTEMA = `Rispondi in italiano, breve e asciutto, per quattro amici italiani in viaggio.

Non inventare MAI una data, un prezzo o un nome di locale. Se non trovi niente di confermato, dillo in una riga: "per ora non risulta niente di annunciato". Una lista vuota e' una risposta corretta; una lista inventata no.

Distingui sempre fra quello che e' ANNUNCIATO e quello che e' solo probabile o abituale. Se una cosa e' ricorrente ogni anno ma non ancora annunciata per quest'anno, scrivilo con quelle parole.

Formato: righe brevi. Per ogni evento trovato: **nome** — data, citta', luogo, e dove si comprano i biglietti. Niente introduzioni e niente conclusioni. Massimo otto voci.`;

function domanda() {
  const oggi = new Date().toLocaleDateString('it-IT', { timeZone: 'Europe/Rome' });
  return `Oggi e' il ${oggi}.

Cerca i concerti K-pop e i grandi eventi musicali annunciati in COREA DEL SUD fra il ${DA} e il ${A}, soprattutto a Seul e Busan.

Aggiungi, se ce ne sono, anche quelli a TAIPEI il 15-16 aprile 2027 e a HONG KONG il 17-18 aprile 2027, che sono le altre due tappe del viaggio.

Interessano anche: registrazioni degli show musicali settimanali a cui si puo' assistere come pubblico (Music Bank, Inkigayo, M Countdown, Show Champion), i fan meeting aperti agli stranieri, e le date dei tour gia' confermate.

Per ognuno di' dove si comprano i biglietti e se gli stranieri possono comprarli senza un numero di telefono coreano, perche' su quello ci si arena sempre.`;
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();

  const ora = Date.now();
  const ip = ipDi(req);
  for (const [k, v] of chiamate) if (ora - Math.max(...v) > 3600000) chiamate.delete(k);
  const recenti = (chiamate.get(ip) || []).filter((t) => ora - t < 3600000);
  if (recenti.length >= LIMITE_ORARIO) {
    return res.status(429).json({ errore: 'Troppe ricerche in un\'ora. Riprova piu\' tardi.' });
  }
  chiamate.set(ip, [...recenti, ora]);

  try {
    const esito = await chiediGemini({
      prompt: domanda(),
      sistema: SISTEMA,
      conRicerca: true,
      maxToken: 1600,
      timeout: 45000,
    });

    if (!esito.testo) {
      return res.status(502).json({ errore: 'Non e\' arrivata nessuna risposta. Riprova fra un attimo.' });
    }

    res.setHeader('Cache-Control', 's-maxage=1800');
    return res.status(200).json({
      ok: true,
      testo: esito.testo,
      fonti: esito.fonti,
      ricercaFatta: esito.ricercaFatta,
      quando: new Date().toISOString(),
    });
  } catch (e) {
    const messaggio = e && e.message ? e.message : String(e);
    console.error('[kpop] ricerca fallita:', messaggio);
    if (e.codice === 'senza-chiave') {
      return res.status(500).json({ errore: 'La ricerca dei concerti non e\' ancora attiva.' });
    }
    return res.status(502).json({ errore: 'Ricerca non riuscita. Riprova fra un attimo.' });
  }
};
