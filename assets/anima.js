// ------------------------------------------------------------------
// Il taccuino si muove.
//
// Tutto passa da Motion (gia' Framer Motion, la versione senza React),
// copiata in assets/vendor/ e caricata da index.html prima di questo
// file. Pochi gesti, tutti di carta: l'aereo che dalla copertina vola
// fino al quaderno, la pagina che si volta quando si cambia meta,
// l'evidenziatore che si stende sui titoli, la penna rossa che cerchia
// quello che manca, le polaroid che si sollevano dal foglio sotto il
// mouse. Tutte le curve rallentano e si posano: niente rimbalzi.
//
// Se Motion non arriva, o se chi guarda ha chiesto meno movimento, non
// succede niente: la pagina e' gia' intera e ferma, con gli evidenziatori
// gia' stesi. Niente di quello che c'e' scritto dipende da questo file.
// ------------------------------------------------------------------
(function(){
  // Aprendo direttamente una meta (#kr, #is) il colore passerebbe dal
  // giallo della home a quello della meta sotto gli occhi: i passaggi di
  // colore si accendono solo dopo il primo disegno.
  requestAnimationFrame(function(){ requestAnimationFrame(function(){ document.documentElement.classList.add('pronto'); }); });

  var M = window.Motion;
  var meno = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var conMotion = !!(M && M.animate && M.inView) && !meno;
  // La copertina guarda questo segno per sapere che lo script e' arrivato,
  // con o senza Motion, prima di rendere premibile "Entra".
  window.PatagucciAnima = conMotion ? 'motion' : 'ferma';
  if(!conMotion) return;

  var animate = M.animate, inView = M.inView;
  var radice = document.documentElement;
  radice.classList.add('anima');
  var copertinaSu = function(){ return radice.classList.contains('con-copertina'); };

  // La curva di casa: parte decisa, rallenta e si posa senza superare il
  // punto d'arrivo.
  var POSA = [0.16, 1, 0.3, 1];
  function finito(controlli, fatto){
    var p = controlli && (controlli.finished || (controlli.then ? controlli : null));
    if(p && p.then) p.then(fatto, fatto); else fatto();
  }
  // Un elemento e' sullo schermo, almeno per buona parte.
  function inVista(el){
    var r = el.getBoundingClientRect();
    return r.width > 0 && r.top < window.innerHeight * 0.9 && r.bottom > window.innerHeight * 0.1;
  }

  // ---- 1. L'evidenziatore sul titolo della meta ----
  // Il CSS lo tiene vuoto finche' c'e' la classe "anima"; quando il titolo
  // entra nello schermo si stende. Solo la parola evidenziata della prima
  // pagina: i titoli di sezione sono gia' evidenziati, un'entrata uguale
  // su ogni sezione stancherebbe. Sotto la copertina il titolo della meta
  // aperta aspetta: lo stende arrivo(), quando la copertina se ne va.
  function stendiTitoli(){
    document.querySelectorAll('header.hero .tt:not([data-osservato])').forEach(function(el){
      if(copertinaSu() && el.closest('.destination.active')) return;
      el.setAttribute('data-osservato', '1');
      inView(el, function(){ el.classList.add('steso'); }, { amount: 0.6 });
    });
  }
  // Per stenderla di nuovo la passata riparte da vuota, ma senza che la si
  // veda ritirarsi: un evidenziatore non si cancella.
  function azzera(titolo){
    titolo.style.transition = 'none';
    titolo.classList.remove('steso');
    void titolo.offsetWidth;
    titolo.style.transition = '';
  }

  // ---- 2. La penna rossa ----
  // pathLength=1 rende la lunghezza indipendente dal disegno: il tratto
  // parte nascosto e si scopre dall'inizio alla fine, una volta sola.
  // Su un tracciato SVG Motion muove l'attributo stroke-dashoffset, non lo
  // stile: anche la partenza sta negli attributi, perche' uno stile in
  // linea li coprirebbe e il tratto comparirebbe di colpo alla fine.
  function preparaTratto(p){
    if(p.hasAttribute('data-pronta')) return;
    p.setAttribute('data-pronta', '1');
    p.setAttribute('pathLength', '1');
    p.setAttribute('stroke-dasharray', '1');
    p.setAttribute('stroke-dashoffset', '1');
  }
  function disegna(p, ritardo){
    if(p.hasAttribute('data-disegnata')) return;
    p.setAttribute('data-disegnata', '1');
    finito(animate(p, { strokeDashoffset: [1, 0] }, { duration: 0.9, delay: ritardo, ease: [0.65, 0, 0.35, 1] }),
           function(){ p.setAttribute('stroke-dashoffset', '0'); });
  }
  function osservaPenna(p){
    if(p.hasAttribute('data-osservato')) return;
    p.setAttribute('data-osservato', '1');
    inView(p.ownerSVGElement || p, function(){ disegna(p, 0.35); }, { amount: 0.8 });
  }
  function preparaPenna(){
    document.querySelectorAll('svg.a-penna path').forEach(function(p){
      preparaTratto(p);
      // Sotto la copertina la penna della meta aperta aspetta: e' l'ultimo
      // colpo dell'arrivo.
      if(copertinaSu() && p.closest('.destination.active')) return;
      osservaPenna(p);
    });
  }

  // ---- 3. Le polaroid si sollevano dal foglio ----
  // Solo con un mouse vero: col dito non c'e' niente da inseguire. Le foto
  // che si aprono (le cartoline delle mete, l'equipaggio che parla) si
  // inclinano piene; quelle che non si aprono si sollevano appena, perche'
  // un'inclinazione piena sembrerebbe un invito al clic. Un movimento per
  // fotogramma al massimo, e niente mentre la foto sta cadendo sul foglio.
  var mouse = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  function inclinazione(el){
    return (getComputedStyle(el).getPropertyValue('--gira') || '').trim() || '0deg';
  }
  function polaroid(el, piano){
    if(!mouse || el.hasAttribute('data-polaroid')) return;
    el.setAttribute('data-polaroid', '1');
    var gira = inclinazione(el);
    var forza = piano ? 0.4 : 1, alza = piano ? 6 : 16;
    var ultimo = null, atteso = false;
    el.addEventListener('pointermove', function(e){
      ultimo = e;
      if(atteso) return;
      atteso = true;
      requestAnimationFrame(function(){
        atteso = false;
        if(!ultimo || el.__cade) return;
        var r = el.getBoundingClientRect();
        var x = (ultimo.clientX - r.left) / r.width - 0.5;
        var y = (ultimo.clientY - r.top) / r.height - 0.5;
        animate(el, { transform: 'perspective(900px) rotate(' + gira + ') rotateX(' + (-y * 12 * forza).toFixed(2) + 'deg) rotateY(' + (x * 14 * forza).toFixed(2) + 'deg) translateZ(' + alza + 'px)' },
                { duration: 0.35, ease: POSA });
      });
    });
    el.addEventListener('pointerleave', function(){
      ultimo = null;
      if(el.__cade) return;
      animate(el, { transform: 'perspective(900px) rotate(' + gira + ') rotateX(0deg) rotateY(0deg) translateZ(0px)' },
              { duration: 0.55, ease: POSA });
    });
  }
  function preparaPolaroid(){
    document.querySelectorAll('.crew-card, .trip-card, .qp-meta-card').forEach(function(el){ polaroid(el, false); });
    document.querySelectorAll('header.hero .bg, .striscia-foto-item').forEach(function(el){ polaroid(el, true); });
  }

  // ---- 4. L'arrivo su una pagina ----
  // La usano sia la pagina che si volta sia la copertina, ed e' un regista
  // solo: un gesto alla volta, in fila. Prima la polaroid cade sul foglio,
  // poi la passata si stende sulla parola del titolo e infine, se c'e' e
  // si vede, la penna rossa cerchia quello che manca.
  function arrivo(meta, ritardo, conPenna){
    if(!meta) return;
    var t = ritardo || 0;
    var foto = meta.querySelector('header.hero .bg');
    if(foto){
      var gira = inclinazione(foto);
      foto.__cade = true;
      finito(animate(foto,
        { transform: ['perspective(900px) rotate(' + gira + ') rotateX(32deg) translateY(-46px)', 'perspective(900px) rotate(' + gira + ') rotateX(0deg) translateY(0px)'],
          opacity: [0, 1] },
        { duration: 0.85, delay: t, ease: POSA }),
        function(){ foto.__cade = false; });
    }
    var titolo = meta.querySelector('header.hero .tt');
    if(titolo){
      titolo.setAttribute('data-osservato', '1');
      azzera(titolo);
      setTimeout(function(){ titolo.classList.add('steso'); }, (t + 0.35) * 1000);
    }
    if(conPenna){
      meta.querySelectorAll('svg.a-penna path').forEach(function(p){
        preparaTratto(p);
        if(inVista(p.ownerSVGElement || p)) disegna(p, t + 0.75);
        else osservaPenna(p);
      });
    }
  }

  // ---- 5. La pagina che si volta ----
  // Un foglio a quadretti copre la meta appena aperta e gira sul bordo,
  // come in un quaderno: in avanti sul bordo sinistro, tornando a una meta
  // che viene prima sul bordo destro. Sta sotto le linguette, che restano
  // ferme e dicono dove si e'. Parte subito e rallenta: in poco piu' di
  // mezzo secondo la pagina nuova e' libera.
  var inVolo = null;
  function voltaPagina(dettaglio){
    if(inVolo) inVolo.remove();
    var ordine = window.SUFFISSI || [];
    var indietro = !!dettaglio && ordine.indexOf(dettaglio.a) < ordine.indexOf(dettaglio.da);
    var foglio = document.createElement('div');
    foglio.className = 'voltapagina' + (indietro ? ' indietro' : '');
    foglio.setAttribute('aria-hidden', 'true');
    document.body.appendChild(foglio);
    inVolo = foglio;
    var togli = function(){ foglio.remove(); if(inVolo === foglio) inVolo = null; };
    finito(animate(foglio,
      { transform: ['perspective(2400px) rotateY(0deg)', 'perspective(2400px) rotateY(' + (indietro ? 90 : -90) + 'deg)'] },
      { duration: 0.55, ease: [0.3, 0.5, 0.2, 1] }), togli);
    // Se il browser non disegna (scheda in secondo piano) l'animazione
    // aspetta: il foglio comunque non deve restare sopra la pagina.
    setTimeout(togli, 1600);

    arrivo(document.querySelector('.destination.active'), 0.2);
  }

  // ---- 6. L'uscita dalla copertina: il volo verso il quaderno ----
  // L'intro del logo la fa il CSS, da solo, all'apertura. Premendo "Entra":
  // l'aereo Royal Brunico si stacca dal logo e vola verso di te, sempre
  // piu' grande, finche' ti passa oltre. Intanto il cielo si riga a
  // quadretti, come se una penna li tirasse col righello, e diventa bianco:
  // e' il foglio del quaderno. Lo stesso aereo ci rientra da sinistra (era
  // uscito a destra) e fa il giro dei ricordi: cinque cose viste in quattro
  // in Sud America, che si disegnano a pennarello mentre ci passa sopra.
  // Finito il giro si posa accanto al titolo della home, esattamente sopra
  // l'aereo che sta li'. Mentre arriva il foglio si scopre, e la home lo
  // accoglie: la polaroid cade e la passata si stende. Lo script della
  // copertina (in index.html) chiama questa funzione se c'e', e tiene
  // quello che restituisce per poter saltare il volo; senza, la copertina
  // sfuma col CSS.
  window.PatagucciCopertina = {
    apri: function(copertina, chiudi){
      var tempi = [], movimenti = [], arrivato = false;
      // Tutto il volo dura LENTO volte i tempi scritti qui sotto: per
      // allungarlo o accorciarlo basta cambiare questo numero.
      var LENTO = 1.5;
      var dopo = function(s, fn){ tempi.push(setTimeout(fn, s * LENTO * 1000)); };
      var muovi = function(el, chiavi, opzioni){
        var o = Object.assign({}, opzioni);
        o.duration = (o.duration == null ? 0.3 : o.duration) * LENTO;
        if(o.delay) o.delay *= LENTO;
        var a = animate(el, chiavi, o); movimenti.push(a); return a;
      };
      // La rete di sicurezza per prima: qualsiasi cosa succeda dopo, la
      // copertina non resta chiusa.
      dopo(6, chiudi);

      var $ = function(sel){ return copertina.querySelector(sel); };
      var vw = window.innerWidth, vh = window.innerHeight;
      var home = document.getElementById('dest-hub');
      var arriva = function(ritardo){
        if(arrivato) return;
        arrivato = true;
        arrivo(home, ritardo, true);
      };
      var aereo = $('.pl-aereo');
      var r = aereo.getBoundingClientRect();
      var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
      copertina.classList.add('in-volo');

      // Il bottone affonda nel suo contorno e si fa da parte.
      muovi($('.cp-entra'), { transform: ['translate(0px, 0px)', 'translate(4px, 5px)'] }, { duration: 0.12 });
      muovi($('.cp-basso'), { opacity: [1, 0] }, { duration: 0.3, delay: 0.1 });

      // 1. L'aereo vola verso di te: accelera, cresce, si inclina, e alla
      // fine ti passa oltre. Niente sfocature: la velocita' la dice la
      // crescita.
      var vaX = vw * 0.62 - cx, vaY = vh * 0.38 - cy;
      muovi(aereo,
        { transform: ['translate(0px, 0px) scale(1) rotate(0deg)', 'translate(' + vaX.toFixed(0) + 'px, ' + vaY.toFixed(0) + 'px) scale(4) rotate(-8deg)'] },
        { duration: 0.8, delay: 0.05, ease: [0.45, 0, 0.75, 0.35] });
      muovi(aereo, { opacity: [1, 0] }, { duration: 0.3, delay: 0.55, ease: [0.4, 0, 1, 1] });
      // la copertina si avvicina un poco: la camera va incontro all'aereo
      muovi($('.pl'), { transform: ['scale(1)', 'scale(1.05)'] }, { duration: 1, ease: [0.4, 0, 0.6, 1] });

      // 2. Il cielo diventa il foglio: le righe orizzontali corrono da
      // sinistra a destra, poi quelle verticali dall'alto in basso, e sotto
      // il verde si fa bianco. Sono gli stessi quadretti della pagina.
      muovi($('.cp-righe-o'), { transform: ['scaleX(0)', 'scaleX(1)'] }, { duration: 0.4, delay: 0.42, ease: [0.3, 0, 0.2, 1] });
      muovi($('.cp-righe-v'), { transform: ['scaleY(0)', 'scaleY(1)'] }, { duration: 0.4, delay: 0.58, ease: [0.3, 0, 0.2, 1] });
      muovi($('.cp-carta'), { opacity: [0, 1] }, { duration: 0.55, delay: 0.45, ease: [0.4, 0, 0.2, 1] });
      muovi($('.cp-anta'), { opacity: [1, 0] }, { duration: 0.01, delay: 1.0 });

      // Il foglio si scopre quando l'aereo comincia la discesa verso il
      // titolo: SCOPRE e' quel momento. Senza il disegno della home non c'e'
      // il giro, e il foglio si scopre subito dopo essersi rigato.
      var SCOPRE = 1.75;
      var chiusura = null;

      // 3. L'aereo rientra piccolo e fa il giro dei ricordi. Dove si posa,
      // quanto e' grande e com'e' inclinato lo dice l'aereo disegnato
      // accanto al titolo della home.
      var sagoma = home && home.querySelector('.aeroplanino .ap-aereo');
      var traccia = home && home.querySelector('.aeroplanino .ap-scia');
      var ma = sagoma && traccia && sagoma.getScreenCTM && sagoma.getScreenCTM();
      if(ma){
        var volo = $('.cp-volo');
        volo.querySelector('svg').setAttribute('viewBox', '0 0 ' + vw + ' ' + vh);
        // Dalle misure del disegno ai pixel dello schermo.
        var schermo = function(m, x, y){ return { x: m.a * x + m.c * y + m.e, y: m.b * x + m.d * y + m.f }; };
        var meta = schermo(ma, +sagoma.getAttribute('x') + sagoma.getAttribute('width') / 2,
                               +sagoma.getAttribute('y') + sagoma.getAttribute('height') / 2);
        var scala = Math.hypot(ma.a, ma.b);
        var gradi = Math.atan2(ma.b, ma.a) * 180 / Math.PI;
        var largo = sagoma.getAttribute('width') * scala;
        var ms = traccia.getScreenCTM();
        var n = traccia.getAttribute('d').match(/-?\d*\.?\d+/g).map(Number);
        var coda = [0, 2, 4, 6].map(function(i){ return schermo(ms, n[i], n[i + 1]); });

        // I ricordi al loro posto, in giro sul foglio in senso orario:
        // largo sullo schermo orizzontale, in due colonne sul telefono.
        // L'aereo passa appena sopra ognuno.
        var ricordi = Array.prototype.slice.call(copertina.querySelectorAll('.cp-ricordo'));
        var posti = vw >= vh
          ? [[0.2, 0.32], [0.5, 0.24], [0.8, 0.32], [0.72, 0.72], [0.32, 0.74]]
          : [[0.28, 0.26], [0.72, 0.2], [0.74, 0.48], [0.7, 0.76], [0.3, 0.64]];
        var tappe = ricordi.map(function(el, i){
          var q = posti[i % posti.length];
          var x = q[0] * vw, y = q[1] * vh;
          el.style.left = x.toFixed(0) + 'px';
          el.style.top = y.toFixed(0) + 'px';
          el.classList.add('al-posto');
          return { x: x, y: y - el.offsetHeight * 0.62 };
        });

        // La rotta: entra da sinistra, passa sopra i ricordi con una curva
        // morbida che tocca ognuno, e arriva all'inizio della scia del
        // disegno gia' lanciata nel suo verso; poi la segue fino al centro
        // dell'aereo.
        var p = function(q){ return q.x.toFixed(1) + ' ' + q.y.toFixed(1); };
        var scia = volo.querySelector('.cp-scia');
        var scopri = volo.querySelector('.cp-scopri');
        var punti = [{ x: -largo * 1.6, y: (tappe.length ? tappe[0].y : coda[0].y) + vh * 0.14 }].concat(tappe, [coda[0]]);
        var ultimo = punti.length - 1;
        var tangenti = punti.map(function(q, i){
          if(i === 0) return { x: punti[1].x - q.x, y: (punti[1].y - q.y) * 0.3 };
          if(i === ultimo){
            var lx = coda[1].x - q.x, ly = coda[1].y - q.y, l = Math.hypot(lx, ly) || 1;
            var d = Math.hypot(q.x - punti[i - 1].x, q.y - punti[i - 1].y);
            return { x: lx / l * d, y: ly / l * d };
          }
          return { x: (punti[i + 1].x - punti[i - 1].x) / 2, y: (punti[i + 1].y - punti[i - 1].y) / 2 };
        });
        var rotta = 'M' + p(punti[0]);
        var alleTappe = [];
        for(var i = 1; i <= ultimo; i++){
          rotta += ' C' + p({ x: punti[i - 1].x + tangenti[i - 1].x / 3, y: punti[i - 1].y + tangenti[i - 1].y / 3 }) +
                   ' ' + p({ x: punti[i].x - tangenti[i].x / 3, y: punti[i].y - tangenti[i].y / 3 }) + ' ' + p(punti[i]);
          scia.setAttribute('d', rotta);
          alleTappe.push(scia.getTotalLength());
        }
        var giro = alleTappe[alleTappe.length - 1];
        rotta += ' C' + p(coda[1]) + ' ' + p(coda[2]) + ' ' + p(coda[3]) + ' L' + p(meta);
        scia.setAttribute('d', rotta);
        scopri.setAttribute('d', rotta);
        var lunga = scia.getTotalLength();
        var piccolo = volo.querySelector('.cp-aeroplanino');

        // I tempi del giro: entra a ENTRA, va a velocita' costante fino
        // all'inizio della scia (GIRO), poi rallenta e si posa. La discesa
        // parte alla stessa velocita' del giro: niente scatti.
        var ENTRA = 0.85, GIRO = 2.1;
        var veloce = giro / GIRO;
        var POSA_T = Math.max(0.3, Math.min(0.8, 2 * (lunga - giro) / veloce));
        var DURA = GIRO + POSA_T;
        SCOPRE = ENTRA + GIRO - 0.05;

        // Ogni ricordo si disegna mentre l'aereo arriva: la macchia
        // d'evidenziatore, poi i tratti uno dopo l'altro, poi il nome.
        ricordi.forEach(function(el, i){
          var quando = ENTRA + alleTappe[i] / veloce;
          muovi(el.querySelector('.cp-r-evid'), { opacity: [0, 0.8], transform: ['scale(0.85)', 'scale(1)'] }, { duration: 0.35, delay: quando - 0.3, ease: POSA });
          el.querySelectorAll('.cp-r-tratto').forEach(function(t, k){
            muovi(t, { strokeDashoffset: [1, 0] }, { duration: 0.45, delay: quando - 0.25 + k * 0.07, ease: [0.65, 0, 0.35, 1] });
          });
          muovi(el.querySelector('figcaption'), { opacity: [0, 1] }, { duration: 0.25, delay: quando, ease: POSA });
          muovi(el.querySelector('.cp-r-passata'), { transform: ['scaleX(0)', 'scaleX(1)'] }, { duration: 0.35, delay: quando + 0.05, ease: POSA });
        });

        // Una sola animazione per tutta la vita del livello: Motion ferma la
        // precedente se se ne avvia un'altra sulla stessa proprieta'.
        var fine = ENTRA + DURA + 0.25;
        chiusura = muovi(volo, { opacity: [0, 0, 1, 1, 0] },
                         { duration: fine, times: [0, ENTRA / fine, (ENTRA + 0.15) / fine, (ENTRA + DURA) / fine, 1], ease: 'linear' });
        // Visto di fianco, l'aereo guarda dalla parte in cui va e si
        // inclina solo un poco: quando il giro lo porta indietro si volta,
        // stringendosi come un aereo che vira, invece di finire a testa in
        // giu'.
        var faccia = 1, inclina = null, prima = 0;
        muovi(0, DURA, {
          duration: DURA, delay: ENTRA, ease: 'linear',
          onUpdate: function(t){
            var passo = Math.max(0, t - prima); prima = t;
            var u = t <= GIRO ? 0 : Math.min(1, (t - GIRO) / POSA_T);
            var dd = t <= GIRO ? Math.min(giro, veloce * t) : giro + (lunga - giro) * (1 - (1 - u) * (1 - u));
            var a = scia.getPointAtLength(dd);
            var p0 = scia.getPointAtLength(Math.max(0, dd - 2)), p1 = scia.getPointAtLength(Math.min(lunga, dd + 2));
            var vx = p1.x - p0.x, vy = p1.y - p0.y;
            var verso = Math.abs(vx) > Math.abs(vy) * 0.25 ? (vx < 0 ? -1 : 1) : (faccia < 0 ? -1 : 1);
            var gira = passo / 0.22 * 2;
            faccia = faccia < verso ? Math.min(verso, faccia + gira) : Math.max(verso, faccia - gira);
            var h = Math.atan2(vy, vx) * 180 / Math.PI;
            if(faccia < 0) h -= 180;
            h = ((h + 540) % 360) - 180;
            h = Math.max(-40, Math.min(40, h));
            inclina = inclina == null ? h : inclina + (h - inclina) * Math.min(1, passo / 0.12);
            // nell'ultimo tratto il muso prende l'inclinazione del disegno
            var k = Math.max(0, (u - 0.3) / 0.7);
            var angolo = inclina + (gradi - inclina) * k * k;
            // arriva da davanti, piu' grande, gira alla sua misura e si posa
            // a quella del disegno
            var s = scala * (t <= GIRO
              ? 1.1 + 0.9 * Math.pow(Math.max(0, 1 - t / (0.3 * GIRO)), 2)
              : 1 + 0.1 * Math.pow(1 - u, 1.5));
            var sx = s * (Math.abs(faccia) < 0.12 ? (faccia < 0 ? -0.12 : 0.12) : faccia);
            piccolo.setAttribute('transform', 'translate(' + a.x.toFixed(2) + ' ' + a.y.toFixed(2) + ') rotate(' + angolo.toFixed(2) + ') scale(' + sx.toFixed(4) + ' ' + s.toFixed(4) + ')');
            scopri.style.strokeDashoffset = (1 - dd / lunga).toFixed(4);
          }
        });
        // La scia lunga se ne va prima che la home sia scoperta del tutto:
        // non deve passare sopra il titolo. Resta solo quella del disegno.
        muovi(1, 0, { duration: 0.3, delay: SCOPRE + 0.1, ease: [0.4, 0, 0.2, 1], onUpdate: function(o){ scia.style.opacity = o.toFixed(3); } });
      }

      // 4. Mentre l'aereo scende verso il titolo il foglio si scopre, coi
      // ricordi sopra, e sotto c'e' la home: l'aereo si posa accanto a un
      // titolo che si vede gia'. A foglio ancora pieno la polaroid si
      // prepara a cadere; cade quando il foglio se n'e' andato.
      var scoperta = muovi($('.cp-foglio'), { opacity: [1, 0] }, { duration: 0.55, delay: SCOPRE, ease: [0.4, 0, 0.2, 1] });
      if(!chiusura) chiusura = scoperta;
      dopo(SCOPRE - 0.15, function(){ arriva(0.7 * LENTO); });

      // 5. Posato: la copertina se ne va quando il volo ha finito.
      finito(chiusura, chiudi);

      // Chi salta il volo non deve aspettare niente: si fermano i tempi e i
      // movimenti della copertina, e la home fa subito il suo arrivo.
      return {
        salta: function(){
          tempi.forEach(clearTimeout);
          movimenti.forEach(function(a){ try { a.stop(); } catch(e){} });
          arriva(0.15);
        }
      };
    }
  };

  // ---- 7. I petali dei ciliegi ----
  // Sulla pagina dei ciliegi della Corea (la sezione con data-petali),
  // quando arriva nello schermo, passa una folata di petali: cadono girando
  // su se stessi, ondeggiano nel vento e spariscono prima di toccare il
  // fondo. Una folata sola ogni volta che la pagina arriva, una decina di
  // secondi al massimo; quando la pagina esce dallo schermo i petali se ne
  // vanno con lei.
  var PETALO = '<svg viewBox="0 0 20 24" focusable="false">' +
    '<path d="M10 23 C 3.5 17.5, 1 10.5, 3 4.6 C 4.4 1.2, 7.4 1.4, 8.8 3.8 L 10 5.6 L 11.2 3.8 C 12.6 1.4, 15.6 1.2, 17 4.6 C 19 10.5, 16.5 17.5, 10 23 Z"/>' +
    '<path class="vena" d="M10 8 C 9.6 11.5, 9.8 14.5, 10 17.5"/></svg>';
  function folata(pagina){
    var cielo = pagina.querySelector(':scope > .petali');
    if(cielo && cielo.childElementCount) return;
    if(!cielo){
      cielo = document.createElement('div');
      cielo.className = 'petali';
      cielo.setAttribute('aria-hidden', 'true');
      pagina.appendChild(cielo);
    }
    var caso = Math.random;
    var largo = pagina.clientWidth, alto = pagina.clientHeight;
    var vh = window.innerHeight, r = pagina.getBoundingClientRect();
    // Cadono dentro quello che si vede: dal bordo alto dello schermo, o
    // da quello della pagina se e' piu' in basso.
    var cima = Math.max(-30, -r.top - 30);
    // Uno ogni 70px di larghezza: una decina sul telefono, venti al massimo.
    var quanti = Math.round(Math.min(20, Math.max(9, largo / 70)));
    cielo.__movimenti = [];
    for(var i = 0; i < quanti; i++){
      var el = document.createElement('span');
      el.className = 'petalo' + (i % 3 === 0 ? ' chiaro' : '');
      el.innerHTML = PETALO;
      el.style.width = (12 + caso() * 10).toFixed(1) + 'px';
      cielo.appendChild(el);
      var x0 = caso() * largo;
      var fondo = Math.min(alto - 20, cima + vh * (0.65 + caso() * 0.45));
      var vento = (caso() < 0.5 ? -1 : 1) * (30 + caso() * 90);
      var onda = 14 + caso() * 26, fase = caso() * 6.28, volte = 1.2 + caso() * 1.2;
      var giro0 = caso() * 360, giro = (caso() < 0.5 ? -1 : 1) * (160 + caso() * 260);
      var passi = [], luce = [];
      for(var k = 0; k <= 12; k++){
        var f = k / 12;
        var x = x0 + vento * f + Math.sin(fase + f * Math.PI * 2 * volte) * onda;
        var y = cima + (fondo - cima) * f;
        // si volta e mostra l'altro lato, senza diventare mai una riga
        var lato = Math.cos(fase + f * Math.PI * 2 * (volte + 0.6));
        var sx = (lato < 0 ? -1 : 1) * Math.max(0.25, Math.abs(lato));
        passi.push('translate(' + x.toFixed(1) + 'px, ' + y.toFixed(1) + 'px) rotate(' + (giro0 + giro * f).toFixed(1) + 'deg) scaleX(' + sx.toFixed(3) + ')');
        luce.push(f < 0.08 ? f / 0.08 : f > 0.84 ? (1 - f) / 0.16 : 1);
      }
      var volo = animate(el, { transform: passi, opacity: luce },
        { duration: 5 + caso() * 2.5, delay: i * (3 / quanti) + caso() * 0.4, ease: 'linear' });
      cielo.__movimenti.push(volo);
      finito(volo, (function(p){ return function(){ p.remove(); }; })(el));
    }
  }
  function viaPetali(pagina){
    var cielo = pagina.querySelector(':scope > .petali');
    if(!cielo) return;
    (cielo.__movimenti || []).forEach(function(a){ try { a.stop(); } catch(e){} });
    cielo.__movimenti = [];
    cielo.textContent = '';
  }
  function osservaPetali(){
    if(!('IntersectionObserver' in window)) return;
    var soglie = [];
    for(var s = 0; s <= 20; s++) soglie.push(s / 20);
    document.querySelectorAll('[data-petali]').forEach(function(pagina){
      if(pagina.__petali) return;
      pagina.__petali = true;
      new IntersectionObserver(function(voci){
        voci.forEach(function(v){
          if(!v.isIntersecting){ viaPetali(pagina); return; }
          // arrivata: ne vedi almeno meta' schermo, o un terzo se e' corta
          var visto = v.intersectionRect.height;
          if(visto >= Math.min(window.innerHeight * 0.5, v.boundingClientRect.height * 0.35)) folata(pagina);
        });
      }, { threshold: soglie }).observe(pagina);
    });
  }

  // ---- 8. I giorni che si aprono ----
  // Un giorno si apre come un foglio piegato che si spiega: il riquadro si
  // allunga e lo scritto compare al suo posto; si ripiega piu' svelto. Solo
  // quando lo apre chi legge, col mouse, col dito o con la tastiera: le
  // aperture dello script (il primo giorno, il calendario) restano subito.
  // Un secondo clic a meta' strada torna indietro da dove si trova.
  function piega(giorno, apri){
    var corpo = giorno.querySelector(':scope > .day-body');
    if(!corpo){ giorno.open = apri; return; }
    if(giorno.__piega){ try { giorno.__piega.stop(); } catch(e){} }
    // da dove parte: quello che si vede adesso
    var aperto = giorno.open;
    var cs = getComputedStyle(corpo);
    var da = aperto ? [corpo.getBoundingClientRect().height, parseFloat(cs.paddingTop), parseFloat(cs.paddingBottom), parseFloat(cs.opacity)] : [0, 0, 0, 0];
    // dove arriva: il riquadro intero, misurato senza i ritocchi
    if(!aperto) giorno.open = true;
    ['height', 'paddingTop', 'paddingBottom', 'opacity', 'overflow'].forEach(function(p){ corpo.style[p] = ''; });
    var cs2 = getComputedStyle(corpo);
    var a = apri ? [corpo.getBoundingClientRect().height, parseFloat(cs2.paddingTop), parseFloat(cs2.paddingBottom), 1] : [0, 0, 0, 0];
    giorno.classList.toggle('si-chiude', !apri);
    // Altezza, margini e inchiostro vanno con un orologio solo, scritto qui
    // a ogni fotogramma: fermandolo a meta' resta esattamente quello che si
    // vede, e il passo dopo riparte da li'.
    corpo.style.overflow = 'hidden';
    var metti = function(t){
      var v = function(i){ return da[i] + (a[i] - da[i]) * t; };
      corpo.style.height = v(0).toFixed(1) + 'px';
      corpo.style.paddingTop = v(1).toFixed(1) + 'px';
      corpo.style.paddingBottom = v(2).toFixed(1) + 'px';
      corpo.style.opacity = v(3).toFixed(3);
    };
    // il punto di partenza subito, prima che il browser disegni
    metti(0);
    var questa = animate(0, 1, apri
      ? { duration: 0.34, ease: POSA, onUpdate: metti }
      : { duration: 0.24, ease: [0.4, 0, 0.2, 1], onUpdate: metti });
    giorno.__piega = questa;
    finito(questa, function(){
      if(giorno.__piega !== questa) return;
      giorno.__piega = null;
      if(!apri){ giorno.open = false; giorno.classList.remove('si-chiude'); }
      ['height', 'paddingTop', 'paddingBottom', 'opacity', 'overflow'].forEach(function(p){ corpo.style[p] = ''; });
    });
  }
  document.addEventListener('click', function(e){
    if(e.defaultPrevented || e.button) return;
    var sommario = e.target.closest && e.target.closest('details.day > summary');
    if(!sommario) return;
    var giorno = sommario.parentNode;
    e.preventDefault();
    piega(giorno, !giorno.open || giorno.classList.contains('si-chiude'));
  });

  function prepara(){
    stendiTitoli();
    preparaPenna();
    preparaPolaroid();
    osservaPetali();
  }
  // Senza copertina (link diretto, o gia' entrati in questa scheda) il
  // titolo della pagina aperta parte gia' evidenziato: la passata si vede
  // solo dopo la copertina o quando si volta pagina.
  if(!copertinaSu()){
    var primoTitolo = document.querySelector('.destination.active header.hero .tt');
    if(primoTitolo){ primoTitolo.classList.add('steso'); primoTitolo.setAttribute('data-osservato', '1'); }
  }
  prepara();
  // Chiusa la copertina, entra in osservazione quello che l'aspettava.
  window.addEventListener('copertina-chiusa', function(){ setTimeout(prepara, 0); });

  // L'evento lo manda showDest() quando la meta cambia davvero. Il primo,
  // quando l'indirizzo apre gia' una meta, arriva prima di questo
  // ascoltatore: registrandolo dopo DOMContentLoaded non si volta pagina
  // all'apertura.
  function ascolta(){
    window.addEventListener('destinazione-cambiata', function(e){
      voltaPagina(e && e.detail);
      // Le polaroid di una meta mai aperta prima hanno appena preso le
      // loro misure: si preparano adesso.
      setTimeout(prepara, 50);
    });
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function(){ setTimeout(ascolta, 0); });
  else setTimeout(ascolta, 0);
})();
