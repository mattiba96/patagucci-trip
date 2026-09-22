// "Ci sono concerti mentre ci siamo?"
//
// I calendari K-pop escono pochi mesi prima, quindi una lista scritta a
// mano sul sito nasce vecchia. Questo endpoint va a guardare ogni volta.
//
// Passa da OneProvider, che e' la chiave che il sito ha gia': la ricerca
// del gateway funziona, va solo presa in due tempi (api/ricerca.js).
// Gemini resta sotto come riserva, per quando il gateway non risponde,
// e parte solo se la sua chiave c'e'.
//
// Il punto delicato, con tutti e due: se la ricerca non si e' potuta
// fare, la risposta arriva lo stesso ma scritta a memoria dal modello.
// In quel caso non si spacciano date per vere — `ricercaFatta: false`
// torna al sito, che lo scrive a chiare lettere.

const { cercaERiassumi } = require('./ricerca.js');
const { chiediGemini } = require('./gemini.js');

// Le parole che vanno al motore di ricerca. Due, perche' la Corea e le
// due tappe finali non stanno nella stessa domanda.
const RICERCHE = [
  'concerti K-pop Corea del Sud aprile 2027 Seoul Busan date annunciate biglietti',
  'concerti ed eventi musicali Taipei Hong Kong aprile 2027 date annunciate',
];

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

Non raccontare quello che stai facendo: niente "sto cercando", niente "[ricerca in corso]", niente preamboli. La prima riga e' gia' la risposta.

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
    let esito;
    try {
      esito = await cercaERiassumi({
        sistema: SISTEMA,
        domanda: domanda(),
        query: RICERCHE,
        maxToken: 1600,
        tempo: 45000,
      });
    } catch (e) {
      // Il gateway giu' non deve spegnere il bottone: se la chiave di
      // Gemini c'e', la domanda va li'.
      console.warn('[kpop] OneProvider non ha risposto, provo Gemini:', e && e.message ? e.message : e);
      try {
        esito = await chiediGemini({
          prompt: domanda(),
          sistema: SISTEMA,
          conRicerca: true,
          maxToken: 1600,
          timeout: 45000,
        });
      } catch (e2) {
        // Due motori, due errori diversi da raccontare. "Non ancora
        // attiva" vale solo se non c'e' nessuna chiave: se la chiave
        // c'era e il motore e' caduto, dirlo cosi' manderebbe a cercare
        // una configurazione che invece e' a posto.
        if (e.codice === 'senza-chiave' && e2.codice === 'senza-chiave') throw e;
        const caduto = new Error('nessun motore ha risposto');
        caduto.codice = 'motori-giu';
        throw caduto;
      }
    }

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
    if (e.codice === 'motori-giu') {
      return res.status(502).json({ errore: 'Il motore non risponde in questo momento. Riprova fra qualche minuto.' });
    }
    return res.status(502).json({ errore: 'Ricerca non riuscita. Riprova fra un attimo.' });
  }
};
