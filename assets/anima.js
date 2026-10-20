// ------------------------------------------------------------------
// Il taccuino si muove.
//
// Tutto passa da Motion (gia' Framer Motion, la versione senza React),
// caricata da index.html prima di questo file. Pochi gesti, tutti di
// carta: la copertina che si apre all'ingresso, la pagina che si volta
// quando si cambia meta, l'evidenziatore che si stende sui titoli, la
// penna rossa che cerchia quello che manca, le polaroid che si sollevano
// dal foglio sotto il mouse.
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

  // ---- 6. La copertina d'ingresso ----
  // Premendo "Entra" il logo si compone come nel video del logo animato:
  // la cresta bianca si disegna dalla vetta verso i due lati, il nero sale
  // a riempire le montagne, la scritta spunta lettera per lettera e l'aereo
  // arriva al suo posto. Intanto il logo gira come un plastico, a strati
  // (il cielo indietro, la scritta e l'aereo in avanti), e torna piatto.
  // Poi la copertina si alza attorno al dorso e sotto c'e' la home.
  // Lo script della copertina (in index.html) chiama questa funzione se
  // c'e'; altrimenti apre col CSS, col logo gia' intero.
  window.PatagucciCopertina = {
    apri: function(copertina, chiudi){
      var $ = function(sel){ return copertina.querySelector(sel); };
      var pl = $('.pl'), anta = $('.cp-anta'), aereo = $('.pl-aereo img');
      var r = pl.getBoundingClientRect();
      var u = r.width / 1672;
      var px = function(unita){ return (unita * u).toFixed(1) + 'px'; };

      // L'aereo si ferma dov'e' (sta ancora entrando o ondeggia) e da li'
      // riparte verso il suo posto.
      var ora = getComputedStyle(aereo).transform;
      aereo.style.transform = (ora && ora !== 'none') ? ora : 'translate(' + px(-330) + ', ' + px(38) + ')';
      copertina.classList.add('in-volo');

      // Il bottone affonda nel suo contorno e si fa da parte.
      animate($('.cp-entra'), { transform: ['translate(0px, 0px)', 'translate(4px, 5px)'] }, { duration: 0.12 });
      animate($('.cp-basso'), { opacity: [1, 0] }, { duration: 0.35, delay: 0.14 });

      // Il plastico: il logo gira di lato e torna di fronte, e intanto gli
      // strati si staccano in profondita' e si richiudono.
      var giro = { duration: 2, times: [0, 0.4, 1], ease: [0.45, 0, 0.2, 1] };
      animate(pl, { transform: ['rotateY(0deg) rotateX(0deg) scale(1)', 'rotateY(-16deg) rotateX(7deg) scale(0.9)', 'rotateY(0deg) rotateX(0deg) scale(1)'] }, giro);
      [['.pl-cielo', -300], ['.pl-rossa', -160], ['.pl-cresta', 8], ['.pl-lettere', 90], ['.pl-aereo', 180]].forEach(function(strato){
        animate($(strato[0]), { transform: ['translateZ(0px)', 'translateZ(' + px(strato[1]) + ')', 'translateZ(0px)'] }, giro);
      });

      // L'aereo arriva: sale presto, si livella e si posa.
      animate(aereo, { transform: [aereo.style.transform, 'translate(' + px(-140) + ', ' + px(8) + ') rotate(-4deg)', 'translate(0px, 0px) rotate(0deg)'] },
              { duration: 1.55, times: [0, 0.55, 1], ease: [0.33, 1, 0.68, 1] });

      // La cresta si scopre dalla vetta verso i due lati, con il passo
      // misurato sui bordi dello schermo: la tavola e' molto piu' larga, e
      // il pezzo che sta fuori si scopre di colpo alla fine.
      var cresta = $('.pl-cresta');
      var vetta = parseFloat(getComputedStyle(cresta).getPropertyValue('--vetta')) || 54;
      var tavola = cresta.getBoundingClientRect();
      var bordoSx = Math.max(0, Math.min(vetta, -tavola.left / tavola.width * 100));
      var bordoDx = Math.max(0, Math.min(100 - vetta, (tavola.right - anta.clientWidth) / tavola.width * 100));
      var taglio = function(dx, sx){ return 'inset(0% ' + dx.toFixed(2) + '% 0% ' + sx.toFixed(2) + '%)'; };
      animate(cresta, { clipPath: [taglio(100 - vetta, vetta), taglio(bordoDx, bordoSx), taglio(0, 0)] },
              { duration: 0.95, delay: 0.1, times: [0, 0.97, 1], ease: [0.4, 0, 0.4, 1] });

      // Il nero sale a riempire le montagne, partendo dal fondo dello
      // schermo e non dal fondo del disegno.
      var fondo = (anta.clientHeight - (r.top - anta.getBoundingClientRect().top)) / u;
      var parti = Math.max(0, Math.min(100, (fondo - 360) / 3640 * 100));
      animate($('.pl-monti'), { clipPath: ['inset(' + parti.toFixed(2) + '% 0% 0% 0%)', 'inset(0% 0% 0% 0%)'] },
              { duration: 0.75, delay: 0.45, ease: [0.3, 0, 0.15, 1] });

      // La scritta spunta lettera per lettera.
      animate(copertina.querySelectorAll('.pl-l'), { opacity: [0, 1], transform: ['translateY(' + px(44) + ')', 'translateY(0px)'] },
              { duration: 0.5, delay: M.stagger(0.06, { startDelay: 0.85 }), ease: [0.16, 1, 0.3, 1] });

      // Poi la copertina si alza attorno al dorso; sotto, la home arriva.
      var apertura = animate(anta,
        { transform: ['rotateY(0deg)', 'rotateY(-98deg)'], filter: ['brightness(1)', 'brightness(0.72)'] },
        { duration: 1.05, delay: 2.3, ease: [0.62, 0.02, 0.3, 1] });
      animate($('.cp-ombra'), { opacity: [0, 0.85, 0] }, { duration: 1.05, delay: 2.3, ease: 'easeInOut' });
      var home = document.getElementById('dest-hub');
      var titolo = home && home.querySelector('header.hero .tt');
      if(titolo) titolo.classList.remove('steso');
      setTimeout(function(){ arrivo(home, 0.15); }, 2400);
      finito(apertura, chiudi);
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
