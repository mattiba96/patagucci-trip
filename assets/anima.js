// ------------------------------------------------------------------
// Il taccuino si muove.
//
// Tutto passa da Motion (gia' Framer Motion, la versione senza React),
// caricata da index.html prima di questo file. Pochi gesti, tutti di
// carta: l'aereo che dalla copertina vola fino al quaderno, la pagina
// che si volta quando si cambia meta, l'evidenziatore che si stende sui
// titoli, la penna rossa che cerchia quello che manca, le polaroid che
// si sollevano dal foglio sotto il mouse.
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
  if(!M || !M.animate || !M.inView || meno) return;

  var animate = M.animate, inView = M.inView;
  var radice = document.documentElement;
  radice.classList.add('anima');

  // Una molla morbida per quando la carta torna giu': Motion la converte
  // in un'animazione del browser. Se questa versione non la accetta, una
  // curva che rallenta fa lo stesso lavoro.
  function molla(durata){
    return M.spring ? { type: M.spring, visualDuration: durata || 0.5, bounce: 0.18 }
                    : { duration: durata || 0.5, ease: [0.16, 1, 0.3, 1] };
  }
  function finito(controlli, fatto){
    var p = controlli && (controlli.finished || (controlli.then ? controlli : null));
    if(p && p.then) p.then(fatto, fatto); else fatto();
  }

  // ---- 1. L'evidenziatore sul titolo della meta ----
  // Il CSS lo tiene vuoto finche' c'e' la classe "anima"; quando il titolo
  // entra nello schermo si stende. Solo la parola evidenziata della prima
  // pagina: i titoli di sezione sono gia' evidenziati, un'entrata uguale
  // su ogni sezione stancherebbe.
  function stendiTitoli(){
    document.querySelectorAll('header.hero .tt:not([data-osservato])').forEach(function(el){
      el.setAttribute('data-osservato', '1');
      inView(el, function(){ el.classList.add('steso'); }, { amount: 0.6 });
    });
  }

  // ---- 2. La penna rossa ----
  // pathLength=1 rende la lunghezza indipendente dal disegno: il tratto
  // parte nascosto e si scopre dall'inizio alla fine.
  function preparaPenna(){
    document.querySelectorAll('svg.a-penna path:not([data-osservato])').forEach(function(p){
      p.setAttribute('data-osservato', '1');
      p.setAttribute('pathLength', '1');
      p.style.strokeDasharray = '1';
      p.style.strokeDashoffset = '1';
      var svg = p.ownerSVGElement || p;
      // La freccia parte dopo il cerchio: data-ritardo sul disegno.
      var ritardo = parseFloat(svg.getAttribute('data-ritardo')) || 0.35;
      inView(svg, function(){
        finito(animate(p, { strokeDashoffset: [1, 0] }, { duration: 0.9, delay: ritardo, ease: [0.65, 0, 0.35, 1] }),
               function(){ p.style.strokeDashoffset = '0'; });
      }, { amount: 0.8 });
    });
  }

  // ---- 4. Le polaroid si sollevano dal foglio ----
  // Solo con un mouse vero: col dito non c'e' niente da inseguire.
  var mouse = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  function inclinazione(el){
    return (getComputedStyle(el).getPropertyValue('--gira') || '').trim() || '0deg';
  }
  function polaroid(el){
    if(!mouse || el.hasAttribute('data-polaroid')) return;
    el.setAttribute('data-polaroid', '1');
    var gira = inclinazione(el);
    el.addEventListener('pointermove', function(e){
      var r = el.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - 0.5;
      var y = (e.clientY - r.top) / r.height - 0.5;
      animate(el, { transform: 'perspective(900px) rotate(' + gira + ') rotateX(' + (-y * 12).toFixed(2) + 'deg) rotateY(' + (x * 14).toFixed(2) + 'deg) translateZ(16px)' },
              { duration: 0.35, ease: [0.16, 1, 0.3, 1] });
    });
    el.addEventListener('pointerleave', function(){
      animate(el, { transform: 'perspective(900px) rotate(' + gira + ') rotateX(0deg) rotateY(0deg) translateZ(0px)' }, molla(0.55));
    });
  }
  function preparaPolaroid(){
    document.querySelectorAll('.crew-card, .trip-card, header.hero .bg, .group-marquee-item, .qp-meta-card').forEach(polaroid);
  }

  // ---- 5. La pagina che si volta ----
  // Un foglio a quadretti grande quanto lo schermo copre la meta appena
  // aperta e gira attorno al bordo sinistro, come in un quaderno. Sotto,
  // la polaroid della nuova meta cade sul foglio e il titolo si evidenzia.
  var inVolo = null;
  function voltaPagina(){
    if(inVolo) inVolo.remove();
    var foglio = document.createElement('div');
    foglio.className = 'voltapagina';
    foglio.setAttribute('aria-hidden', 'true');
    document.body.appendChild(foglio);
    inVolo = foglio;
    finito(animate(foglio,
      { transform: ['perspective(2400px) rotateY(0deg)', 'perspective(2400px) rotateY(-100deg)'],
        filter: ['brightness(1)', 'brightness(0.78)'] },
      { duration: 0.75, ease: [0.55, 0.05, 0.35, 1] }),
      function(){ foglio.remove(); if(inVolo === foglio) inVolo = null; });
    // Se il browser non disegna (scheda in secondo piano) l'animazione
    // aspetta: il foglio comunque non deve restare sopra la pagina.
    setTimeout(function(){ foglio.remove(); if(inVolo === foglio) inVolo = null; }, 1600);

    arrivo(document.querySelector('.destination.active'), 0.3);
  }

  // La prima pagina che compare: la polaroid cade sul foglio e il titolo
  // si evidenzia. La usano sia la pagina che si volta sia la copertina.
  function arrivo(meta, ritardo){
    if(!meta) return;
    var foto = meta.querySelector('header.hero .bg');
    if(foto){
      var gira = inclinazione(foto);
      animate(foto,
        { transform: ['perspective(900px) rotate(' + gira + ') rotateX(32deg) translateY(-46px)', 'perspective(900px) rotate(' + gira + ') rotateX(0deg) translateY(0px)'],
          opacity: [0, 1] },
        { duration: 0.85, delay: ritardo, ease: [0.16, 1, 0.3, 1] });
    }
    var titolo = meta.querySelector('header.hero .tt');
    if(titolo){
      titolo.classList.remove('steso');
      setTimeout(function(){ titolo.classList.add('steso'); }, ritardo * 1000 + 180);
    }
  }

  // ---- 6. L'uscita dalla copertina: il volo verso il quaderno ----
  // L'intro del logo la fa il CSS, da solo, all'apertura. Premendo "Entra":
  // l'aereo Royal Brunico si stacca dal logo e vola verso di te, sempre
  // piu' grande e mosso; quando ti passa davanti una nuvola bianca copre
  // tutto e, quando si dirada, sotto c'e' il foglio a quadretti. Lo stesso
  // aereo ci rientra da sinistra (era uscito a destra), scende, risale
  // lasciando la scia tratteggiata e si posa accanto al titolo della home,
  // esattamente sopra l'aereo che sta li'. Poi il foglio si scopre e la
  // home arriva. Lo script della copertina (in index.html) chiama questa
  // funzione se c'e'; altrimenti la copertina sfuma col CSS.
  window.PatagucciCopertina = {
    apri: function(copertina, chiudi){
      var $ = function(sel){ return copertina.querySelector(sel); };
      var vw = window.innerWidth, vh = window.innerHeight;
      var aereo = $('.pl-aereo');
      var r = aereo.getBoundingClientRect();
      var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
      copertina.classList.add('in-volo');

      // Il bottone affonda nel suo contorno e si fa da parte.
      animate($('.cp-entra'), { transform: ['translate(0px, 0px)', 'translate(4px, 5px)'] }, { duration: 0.12 });
      animate($('.cp-basso'), { opacity: [1, 0] }, { duration: 0.3, delay: 0.1 });

      // 1. L'aereo vola verso di te: accelera, cresce, si inclina e si muove.
      var vaX = vw * 0.62 - cx, vaY = vh * 0.38 - cy;
      animate(aereo,
        { transform: ['translate(0px, 0px) scale(1) rotate(0deg)', 'translate(' + vaX.toFixed(0) + 'px, ' + vaY.toFixed(0) + 'px) scale(5.2) rotate(-8deg)'],
          filter: ['blur(0px)', 'blur(7px)'] },
        { duration: 0.8, delay: 0.05, ease: [0.45, 0, 0.75, 0.35] });
      // la copertina si avvicina un poco: la camera va incontro all'aereo
      animate($('.pl'), { transform: ['scale(1)', 'scale(1.07)'] }, { duration: 1, ease: [0.4, 0, 0.6, 1] });

      // 2. La nuvola: si apre bianca dove passa l'aereo e copre tutto.
      var nuvola = $('.cp-nuvola');
      nuvola.style.setProperty('--nx', (vw * 0.62).toFixed(0) + 'px');
      nuvola.style.setProperty('--ny', (vh * 0.38).toFixed(0) + 'px');
      // Ogni sbuffo e' subito pieno e poi si gonfia, uno dopo l'altro; il
      // primo quando l'aereo e' gia' grande, cosi' lo si vede arrivare.
      copertina.querySelectorAll('.cp-nuvola i').forEach(function(sbuffo, i){
        var quando = 0.62 + i * 0.045;
        animate(sbuffo, { transform: ['scale(0.05)', 'scale(3)'] }, { duration: 0.55, delay: quando, ease: [0.25, 0, 0.2, 1] });
        animate(sbuffo, { opacity: [0, 1] }, { duration: 0.14, delay: quando });
      });

      // 3. Sotto la nuvola c'e' gia' il foglio; la nuvola si dirada. Il
      // foglio resta fino all'atterraggio, poi si scopre sulla home: una
      // sola animazione per tutta la sua vita, perche' Motion ferma la
      // precedente se se ne avvia un'altra sulla stessa proprieta'.
      var arrivoHome = 2.35, fine = arrivoHome + 0.45;
      var carta = $('.cp-carta');
      var chiusura = animate(carta, { opacity: [0, 0, 1, 1, 0] },
              { duration: fine, times: [0, 1 / fine, 1.01 / fine, arrivoHome / fine, 1], ease: 'linear' });
      animate($('.cp-anta'), { opacity: [1, 0] }, { duration: 0.01, delay: 1.05 });
      animate(nuvola, { opacity: [1, 0] }, { duration: 0.4, delay: 1.1, ease: [0.4, 0, 0.2, 1] });

      // 4. L'aereo rientra piccolo: dove si posa, quanto e' grande e com'e'
      // inclinato lo dice l'aereo disegnato accanto al titolo della home.
      var home = document.getElementById('dest-hub');
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

        // La rotta, sempre col muso in avanti e senza picchiate: entra da
        // sinistra poco piu' in alto, scende piano fino alla riga del
        // titolo, poi riprende quota sulla scia del disegno fino al centro
        // dell'aereo.
        var p = function(q){ return q.x.toFixed(1) + ' ' + q.y.toFixed(1); };
        var dx = coda[0].x + largo * 1.4;
        var via = { x: -largo * 1.4, y: coda[0].y - Math.min(vh * 0.12, dx * 0.3) };
        var rotta = 'M' + p(via) +
          ' C' + p({ x: via.x + dx * 0.4, y: via.y }) + ' ' + p({ x: coda[0].x - dx * 0.4, y: coda[0].y }) + ' ' + p(coda[0]) +
          ' C' + p(coda[1]) + ' ' + p(coda[2]) + ' ' + p(coda[3]) +
          ' L' + p(meta);
        var scia = volo.querySelector('.cp-scia');
        var scopri = volo.querySelector('.cp-scopri');
        scia.setAttribute('d', rotta);
        scopri.setAttribute('d', rotta);
        var lunga = scia.getTotalLength();
        var piccolo = volo.querySelector('.cp-aeroplanino');
        animate(volo, { opacity: [0, 0, 1, 1, 0] },
                { duration: fine, times: [0, 1.12 / fine, 1.27 / fine, (arrivoHome + 0.1) / fine, 1], ease: 'linear' });
        animate(0, 1, {
          duration: 1.35, delay: 1.12, ease: [0.3, 0, 0.25, 1],
          onUpdate: function(v){
            var dd = v * lunga;
            var a = scia.getPointAtLength(dd);
            var prima = scia.getPointAtLength(Math.max(0, dd - 1)), dopo = scia.getPointAtLength(Math.min(lunga, dd + 1));
            var verso = Math.atan2(dopo.y - prima.y, dopo.x - prima.x) * 180 / Math.PI;
            // nell'ultimo tratto il muso prende l'inclinazione del disegno
            var ultimo = Math.max(0, (v - 0.85) / 0.15);
            var delta = ((gradi - verso + 540) % 360) - 180;
            var angolo = verso + delta * ultimo * ultimo;
            // arriva da davanti, piu' grande, e si posa alla misura del disegno
            var s = scala * (1 + 1.6 * Math.pow(1 - v, 1.5));
            piccolo.setAttribute('transform', 'translate(' + a.x.toFixed(2) + ' ' + a.y.toFixed(2) + ') rotate(' + angolo.toFixed(2) + ') scale(' + s.toFixed(4) + ')');
            scopri.style.strokeDashoffset = (1 - v).toFixed(4);
          }
        });
      }

      // 5. Posato: il foglio si scopre (vedi sopra) e sotto c'e' la home.
      setTimeout(function(){ arrivo(home, 0.05); }, arrivoHome * 1000);
      finito(chiusura, chiudi);
      // Qualsiasi cosa succeda all'animazione, la copertina non resta chiusa.
      setTimeout(chiudi, 6000);
    }
  };

  function prepara(){
    stendiTitoli();
    preparaPenna();
    preparaPolaroid();
  }
  // Senza copertina (link diretto, o gia' entrati in questa scheda) il
  // titolo della pagina aperta parte gia' evidenziato: la passata si vede
  // solo dopo la copertina o quando si volta pagina.
  if(!radice.classList.contains('con-copertina')){
    var primoTitolo = document.querySelector('.destination.active header.hero .tt');
    if(primoTitolo){ primoTitolo.classList.add('steso'); primoTitolo.setAttribute('data-osservato', '1'); }
  }
  prepara();

  // L'evento lo manda showDest() a ogni cambio di meta. Il primo, quando
  // l'indirizzo apre gia' una meta, arriva prima di questo ascoltatore:
  // registrandolo dopo DOMContentLoaded non si volta pagina all'apertura.
  function ascolta(){
    window.addEventListener('destinazione-cambiata', function(){
      voltaPagina();
      // Le polaroid di una meta mai aperta prima hanno appena preso le
      // loro misure: si preparano adesso.
      setTimeout(prepara, 50);
    });
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function(){ setTimeout(ascolta, 0); });
  else setTimeout(ascolta, 0);
})();
