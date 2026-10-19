/* HITS Made Simple v3 — missions, points, animated phone, EN/AR */
(function () {
  'use strict';
  // asset paths; the offline single-file build maps them to embedded data
  var A = function (p) { return (window.HITS_ASSETS && window.HITS_ASSETS[p]) || p; };
  var D = window.HITS, TR = window.HITS_TRACKING || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var app = $('#app');
  var REVIEW = /[?&]review=1/.test(location.search);
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var PTS_TASK = 10, PTS_ANSWER = 10;

  /* ---------- storage (works when blocked) ---------- */
  var mem = {};
  function load() { try { return JSON.parse(localStorage.getItem('hits3') || '{}'); } catch (e) { return mem; } }
  function save() { try { localStorage.setItem('hits3', JSON.stringify(S)); } catch (e) { mem = S; } }
  var S = load();
  S.prog = S.prog || {};
  if (!S.lang) S.lang = (navigator.language || '').slice(0, 2) === 'ar' ? 'ar' : 'en';
  if (!S.role) S.role = 'employee';
  if (!S.sid) S.sid = Math.random().toString(36).slice(2, 10);
  save();

  /* ---------- i18n ---------- */
  function U(k) { return D.ui[S.lang][k]; }
  function tx(o) { return o == null ? '' : (typeof o === 'string' ? o : (o[S.lang] != null ? o[S.lang] : o.en)); }
  function num(n) { return S.lang === 'ar' ? new Intl.NumberFormat('ar-EG').format(n) : String(n); }
  function fmt(s, m) { return s.replace(/\{(\w+)\}/g, function (_, k) { return typeof m[k] === 'number' ? num(m[k]) : m[k]; }); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  // Isolate Latin runs (HITS labels) inside Arabic text so punctuation stays put.
  var LAT = /[A-Za-z][A-Za-z0-9 .,'’\/&+\-:()\[\]›…?]*[A-Za-z0-9)\]?.…]|[A-Za-z]/g;
  function h(s) {
    s = esc(s);
    if (S.lang !== 'ar') return s;
    return s.replace(LAT, function (m) {
      var trail = ''; var mm = m.match(/^(.*?)([.,:]+)$/);
      if (mm && !/\?$/.test(m)) { m = mm[1]; trail = mm[2]; }
      return '<bdi class="l" dir="ltr">' + m + '</bdi>' + trail;
    });
  }
  function two(parts, tag) {
    var p = tx(parts) || ['', ''];
    return '<' + tag + ' class="two"><span>' + h(p[0]) + '</span><span>' + h(p[1]) + '</span></' + tag + '>';
  }

  /* ---------- icons ---------- */
  var P = {
    star: '<path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.9l-5.2 2.7 1-5.8-4.3-4.1 5.9-.9z"/>',
    search: '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/>',
    arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
    back: '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    x: '<path d="M6 6l12 12M18 6L6 18"/>',
    expand: '<path d="M14 4h6v6M10 20H4v-6M20 4l-7 7M4 20l7-7"/>',
    swipe: '<path d="M4 12h16M14 7l5 5-5 5"/>',
    bulb: '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.7.6 1.1 1.3 1.1 2.2h5c0-.9.4-1.6 1.1-2.2A6 6 0 0 0 12 3z"/>',
    target: '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r=".6"/>',
    help: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.3a2.6 2.6 0 0 1 5 .9c0 1.7-2.5 2.2-2.5 3.8M12 17h.01"/>',
    mail: '<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="M3.5 7l8.5 6 8.5-6"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
    refresh: '<path d="M4 12a8 8 0 0 1 13.7-5.6L20 8.5M20 4v4.5h-4.5M20 12a8 8 0 0 1-13.7 5.6L4 15.5M4 20v-4.5h4.5"/>',
    trophy: '<path d="M8 4h8v5a4 4 0 0 1-8 0zM8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v4M8.5 20h7M10 17h4"/>',
    rocket: '<path d="M12 15l-3-3c1.5-4.5 4.8-7.6 10-8-.4 5.2-3.5 8.5-8 10z"/><path d="M9 12H5.5L8 9.5h3.5M12 15v3.5l2.5-2.5v-3.5M6.5 17.5c-1 1-1.5 3-1.5 3s2-.5 3-1.5"/>',
    calendar: '<rect x="4" y="5.5" width="16" height="15" rx="2"/><path d="M4 10h16M8.5 3.5v4M15.5 3.5v4"/>',
    'calendar-days': '<rect x="4" y="5.5" width="16" height="15" rx="2"/><path d="M4 10h16M8.5 3.5v4M15.5 3.5v4M8 14h.01M12 14h.01M16 14h.01M8 17.5h.01M12 17.5h.01"/>',
    'calendar-check': '<rect x="4" y="5.5" width="16" height="15" rx="2"/><path d="M4 10h16M8.5 3.5v4M15.5 3.5v4M9 15l2 2 4-4"/>',
    clock: '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    history: '<path d="M4 12a8 8 0 1 0 2.3-5.6L4 8.7M4 4.5v4.2h4.2"/><path d="M12 8v4l3 2"/>',
    pin: '<path d="M12 21s-6.5-6.1-6.5-11a6.5 6.5 0 0 1 13 0c0 4.9-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/>',
    bell: '<path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 1.5h-15zM10 20.5h4"/>',
    'check-badge': '<path d="M12 3l2.4 1.8 3 .1.9 2.9 2.4 1.8-.9 2.9.9 2.9-2.4 1.8-.9 2.9-3 .1L12 21l-2.4-1.8-3-.1-.9-2.9-2.4-1.8.9-2.9-.9-2.9 2.4-1.8.9-2.9 3-.1z"/><path d="M8.8 12.2l2.2 2.2 4.2-4.4"/>',
    hourglass: '<path d="M7 3.5h10M7 20.5h10M8 3.5c0 4.5 8 5 8 8.5s-8 4-8 8.5M16 3.5c0 4.5-8 5-8 8.5s8 4 8 8.5"/>',
    'log-in': '<path d="M14 4h4a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-4M10 16l4-4-4-4M14 12H4"/>',
    lock: '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>',
    list: '<path d="M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01"/>'
  };
  function ic(n) { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" overflow="visible">' + (P[n] || P.info) + '</svg>'; }

  /* ---------- progress & points ---------- */
  function points() { var n = 0; for (var k in S.prog) n += S.prog[k].pts || 0; return n; }
  function isDone(id) { return !!(S.prog[id] && S.prog[id].done); }
  function missionsFor(role) { return D.missions.filter(function (m) { return m.roles.indexOf(role) > -1; }).sort(function (a, b) { return role === 'manager' ? (a.id === 'approvals' ? -1 : b.id === 'approvals' ? 1 : 0) : 0; }); }
  function mStats(m) { var d = m.tasks.filter(isDone).length; return { done: d, total: m.tasks.length, pct: Math.round(100 * d / m.tasks.length) }; }
  function missionOf(tid) {
    var ms = missionsFor(S.role).concat(D.missions);
    for (var i = 0; i < ms.length; i++) if (ms[i].tasks.indexOf(tid) > -1) return ms[i];
    return D.missions[0];
  }
  function nextTask(m, cur) {
    var i = m.tasks.indexOf(cur), n = m.tasks.length;
    for (var j = 1; j <= n; j++) { var t = m.tasks[(i + j) % n]; if (!isDone(t)) return t; }
    return null;
  }

  /* ---------- tracking (anonymous, Google Form) ---------- */
  function track(event, task, score) {
    try {
      if (!TR.formAction || !TR.fields || !TR.fields.event) return;
      var f = TR.fields, p = new URLSearchParams();
      var add = function (k, v) { if (f[k]) p.append(f[k], v == null ? '' : String(v)); };
      add('event', event); add('role', S.role); add('language', S.lang); add('task', task || '');
      add('score', score == null ? '' : score); add('session', S.sid); add('department', S.dept || '');
      fetch(TR.formAction, { method: 'POST', mode: 'no-cors', body: p, keepalive: true }).catch(function () {});
    } catch (e) {}
  }

  /* ---------- shell ---------- */
  function setLangAttrs() {
    document.documentElement.lang = S.lang;
    document.documentElement.dir = S.lang === 'ar' ? 'rtl' : 'ltr';
    document.title = U('appName');
  }
  function header() {
    return '<a class="skip" href="#main">' + esc(U('skipToContent')) + '</a>' +
      '<header class="hdr" dir="ltr"><a class="brand" href="#/" aria-label="' + esc(U('appName')) + '"><span class="plate"><img src="' + A('assets/img/logo.webp') + '" alt="Al Safy Group"></span><b dir="auto">' + esc(U('appName')) + '</b></a>' +
      '<span class="chip-pts" id="pts" title="' + esc(U('pointsLabel')) + '">' + ic('star') + '<span>' + num(points()) + '</span></span>' +
      '<button class="ibtn" id="btnSearch" aria-label="' + esc(U('search')) + '">' + ic('search') + '</button>' +
      '<button class="lang" id="btnLang" data-to="' + (S.lang === 'ar' ? 'en' : 'ar') + '" aria-label="' + esc(U('langName')) + '">' + esc(U('langSwitch')) + '</button></header>' +
      '<div id="searchBox"></div><main id="main" tabindex="-1"></main><div class="sr" aria-live="polite" id="live"></div>';
  }
  function bindHeader() {
    $('#btnLang').onclick = function () { S.lang = S.lang === 'ar' ? 'en' : 'ar'; save(); render(true); };
    $('#btnSearch').onclick = toggleSearch;
  }
  function bumpPoints() {
    var el = $('#pts'); if (!el) return;
    el.querySelector('span').textContent = num(points());
    el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop');
  }
  function scrollTop() { window.scrollTo(0, 0); document.body.scrollTop = 0; document.documentElement.scrollTop = 0; }

  /* ---------- search ---------- */
  function toggleSearch() {
    var box = $('#searchBox');
    if (box.innerHTML) { box.innerHTML = ''; return; }
    box.innerHTML = '<div class="search" role="search"><div class="wrapi"><input id="q" type="search" autocomplete="off" placeholder="' + esc(U('searchPlaceholder')) + '" aria-label="' + esc(U('searchPlaceholder')) + '"><ul id="qres"></ul></div></div>';
    var q = $('#q'); q.focus();
    var run = function () {
      var v = q.value.trim().toLowerCase(), out = '';
      Object.keys(D.tasks).forEach(function (id) {
        var t = D.tasks[id], hay = (tx(t.name) + ' ' + tx(t.situation) + ' ' + tx(t.purpose) + ' ' + t.name.en + ' ' + (t.path || '')).toLowerCase();
        if (!v || hay.indexOf(v) > -1) out += taskRow(id, 0);
      });
      $('#qres').innerHTML = out || '<li class="muted">' + esc(U('noResults')) + '</li>';
    };
    q.oninput = run; run();
    q.onkeydown = function (e) { if (e.key === 'Escape') toggleSearch(); };
  }
  document.addEventListener('click', function (e) {
    var r = e.target.closest('[data-task]');
    if (r) { e.preventDefault(); $('#searchBox').innerHTML = ''; location.hash = '#/task/' + r.getAttribute('data-task'); }
  });

  /* ---------- home ---------- */
  function taskRow(id, n) {
    var t = D.tasks[id], d = isDone(id);
    return '<li><button class="trow' + (d ? ' done' : '') + '" data-task="' + id + '"><span class="tnum">' + (d ? ic('check') : (n ? num(n) : ic(t.icon))) + '</span><span class="ttxt"><b>' + h(tx(t.situation)) + '</b><small>' + h(tx(t.name)) + '</small></span><span class="go">' + ic('arrow') + '</span></button></li>';
  }
  function home() {
    var ms = missionsFor(S.role), all = 0, done = 0;
    ms.forEach(function (m) { var s = mStats(m); all += s.total; done += s.done; });
    var html = '<div class="wrap"><section class="hero">' + two(D.ui[S.lang].heroLine ? { en: D.ui.en.heroLine, ar: D.ui.ar.heroLine } : null, 'h1') +
      '<div class="rule"></div><p>' + h(U('heroSub')) + '</p>' +
      '<div class="seg" role="group" aria-label="' + esc(U('roleLabel')) + '"><button data-role="employee" aria-pressed="' + (S.role === 'employee') + '">' + esc(U('roleEmployee')) + '</button><button data-role="manager" aria-pressed="' + (S.role === 'manager') + '">' + esc(U('roleManager')) + '</button></div>' +
      '<div class="stats"><span class="stat">' + ic('star') + esc(fmt(U('points'), { n: points() })) + '</span><span class="stat">' + ic('check') + esc(fmt(U('tasksDone'), { done: done, total: all })) + '</span></div>' +
      (S.role === 'manager' ? '<p class="note">' + ic('info') + '<span>' + h(U('roleNoteManager')) + '</span></p>' : '') +
      '</section><section class="missions" aria-label="' + esc(U('allMissions')) + '">';
    ms.forEach(function (m) {
      var s = mStats(m), nx = nextTask(m, m.tasks[m.tasks.length - 1]);
      var cta = s.done === s.total ? U('reviewMission') : (s.done ? U('continueMission') : U('startMission'));
      html += '<article class="mcard' + (s.done === s.total ? ' complete' : '') + '">' +
        (s.done === s.total ? '<span class="badge-done">' + ic('trophy') + esc(U('done')) + '</span>' : '') +
        '<div class="mhead"><span class="micon">' + ic(m.icon) + '</span><div><span class="eyebrow">' + esc(U('mission')) + '</span><h2>' + h(tx(m.title)) + '</h2><p class="out">' + h(tx(m.outcome)) + '</p></div></div>' +
        '<div class="pbar"><div class="lbl"><span>' + esc(fmt(U('tasksDone'), { done: s.done, total: s.total })) + '</span><span>' + num(s.pct) + '%</span></div><div class="track"><i data-w="' + s.pct + '"></i></div></div>' +
        '<ul class="tlist">' + m.tasks.map(function (t, i) { return taskRow(t, i + 1); }).join('') + '</ul>' +
        '<button class="btn btn-p" data-task="' + (nx || m.tasks[0]) + '" data-m="' + m.id + '"><span>' + esc(cta) + '</span>' + ic(S.lang === 'ar' ? 'back' : 'arrow') + '</button></article>';
    });
    html += '</section><footer class="foot"><div class="row"><a class="tbtn" href="#/help">' + ic('help') + esc(U('help')) + '</a>' +
      (points() ? '<button class="tbtn" id="reset">' + ic('refresh') + esc(U('resetProgress')) + '</button>' : '') + '</div>' +
      ((TR.departments || []).length ? '<label class="dept row">' + esc(U('department')) + ' <select id="dept"><option value="">' + esc(U('departmentNone')) + '</option>' + TR.departments.map(function (d) { return '<option' + (S.dept === d ? ' selected' : '') + '>' + esc(d) + '</option>'; }).join('') + '</select></label>' : '') +
      '<p>' + h(U('privacy')) + '</p></footer></div>';
    $('#main').innerHTML = html;
    [].forEach.call(document.querySelectorAll('[data-role]'), function (b) { b.onclick = function () { S.role = b.getAttribute('data-role'); save(); home(); }; });
    [].forEach.call(document.querySelectorAll('[data-m]'), function (b) { b.addEventListener('click', function () { S.curM = b.getAttribute('data-m'); save(); }, true); });
    var r = $('#reset'); if (r) r.onclick = function () { if (confirm(U('resetConfirm'))) { S.prog = {}; save(); render(); } };
    var dp = $('#dept'); if (dp) dp.onchange = function () { S.dept = dp.value; save(); };
    requestAnimationFrame(function () { requestAnimationFrame(function () { [].forEach.call(document.querySelectorAll('.track i'), function (i) { i.style.width = i.getAttribute('data-w') + '%'; }); }); });
  }

  /* ---------- help ---------- */
  function help() {
    var hp = D.help || {};
    var html = '<div class="wrap help" style="max-width:760px">' + two(hp.title || { en: ['Help', 'and glossary.'], ar: ['المساعدة', 'والمصطلحات.'] }, 'h1') + '<div class="rule"></div><ul>' +
      (hp.support || []).map(function (s) { return '<li>' + h(tx(s)) + '</li>'; }).join('') + '</ul>' + supportCard() +
      '<div style="margin-top:28px">' + (D.glossary || []).map(function (g) { return '<details><summary>' + h(tx(g.term)) + '</summary><p>' + h(tx(g.meaning)) + '</p></details>'; }).join('') + '</div>' +
      '<p style="margin-top:24px"><a class="tbtn" href="#/">' + ic(S.lang === 'ar' ? 'arrow' : 'back') + esc(U('backToMissions')) + '</a></p></div>';
    $('#main').innerHTML = html;
  }
  function supportCard() {
    var t = U('helpCardTitle');
    return '<div class="supp"><h3 class="two"><span>' + h(t[0]) + '</span><span>' + h(t[1]) + '</span></h3><div class="rule"></div><p>' + h(U('helpCardLine')) + '</p><a class="pill" href="mailto:' + D.helpEmail + '">' + ic('mail') + D.helpEmail + '</a></div>';
  }

  /* ---------- task player ---------- */
  var V = null; // current view state
  function startTask(id) {
    var t = D.tasks[id]; if (!t) { location.hash = '#/'; return; }
    var m = (S.curM && D.missions.filter(function (x) { return x.id === S.curM && x.tasks.indexOf(id) > -1; })[0]) || missionOf(id);
    V = { id: id, t: t, m: m, phase: 'intro', i: 0, answered: null, order: shuffle(t.check.options.length), prevHot: null, prevScreen: null };
    taskView();
  }
  function shuffle(n) {
    var a = []; for (var i = 0; i < n; i++) a.push(i);
    for (var j = n - 1; j > 0; j--) { var k = Math.floor(Math.random() * (j + 1)); var x = a[j]; a[j] = a[k]; a[k] = x; }
    // the right answer must not sit in the same place every time
    return a;
  }
  function stripHtml() {
    var m = V.m, idx = m.tasks.indexOf(V.id);
    return '<div class="strip"><span class="mname">' + esc(U('mission')) + ': <b>' + h(tx(m.title)) + '</b> · ' + esc(fmt(U('missionOf'), { n: idx + 1, total: m.tasks.length })) + '</span><span class="segs" aria-hidden="true">' +
      m.tasks.map(function (t, i) { return '<i class="' + (t === V.id ? 'cur' : (isDone(t) ? 'on' : '')) + '"></i>'; }).join('') + '</span></div>';
  }
  function stageHtml() {
    return '<div class="stage" id="stage"><img class="bg" src="' + A('assets/img/stage-bg.webp') + '" alt=""><img class="glow" src="' + A('assets/img/phone-glow.webp') + '" alt="">' +
      '<div class="slot" id="slot" role="img"><div class="spot" id="spot"></div><div class="hring" id="hring"></div><div class="ripple" id="ripple"></div><div class="ptr" id="ptr"></div></div>' +
      '<img class="frame" src="' + A('assets/img/phone-frame.webp') + '" alt=""><button class="zoomchip" id="zoomchip">' + ic('expand') + esc(U('tapToEnlarge')) + '</button></div>';
  }
  function taskView() {
    var desk = innerWidth >= 900; V.desk = desk;
    var html = '<div class="task phase-' + V.phase + '"><div class="tgrid">' +
      (desk ? '<div class="stagecol"><div class="stagebox" id="sbox">' + stageHtml() + '</div></div>' : '') +
      '<div class="side">' + stripHtml() + '<div id="phase"></div>' +
      '<nav class="bar" id="bar"><button class="btn btn-g bk" id="bk"></button><button class="btn btn-p" id="nx"></button></nav></div></div></div>';
    $('#main').innerHTML = html;
    $('#bk').onclick = goBack; $('#nx').onclick = goNext;
    if (desk) bindStage();
    renderPhase(true);
  }
  function setBar(bk, nx, nxIcon) {
    var b = $('#bk'), n = $('#nx'), ar = S.lang === 'ar';
    b.hidden = !bk; n.hidden = !nx;
    if (bk) b.innerHTML = ic('back') + '<span class="t">' + esc(bk) + '</span>';
    if (nx) n.innerHTML = '<span class="t">' + esc(nx) + '</span>' + ic(nxIcon || 'arrow');
  }
  function renderPhase(first) {
    var desk = innerWidth >= 900, ph = $('#phase'), t = V.t;
    if (V.phase === 'intro') {
      ph.innerHTML = '<div class="panel"><span class="eyebrow">' + esc(fmt(U('missionOf'), { n: V.m.tasks.indexOf(V.id) + 1, total: V.m.tasks.length })) + '</span>' +
        '<div style="height:10px"></div>' + two(t.title, 'h1') + '<div class="rule"></div><p class="purpose">' + h(tx(t.purpose)) + '</p>' +
        (t.outcome ? '<div class="outcome">' + ic('target') + '<div><b>' + esc(U('youWillBeAble')) + '</b>' + h(tx(t.outcome)) + '</div></div>' : '') +
        (t.path ? '<div class="lbl2"><span class="eyebrow">' + esc(U('whereToGo')) + '</span><br><span class="pathchip">' + esc(t.path) + '</span></div>' : '') +
        (t.goodToKnow && t.goodToKnow.length ? '<div class="gtk"><h3>' + ic('bulb') + esc(U('goodToKnow')) + '</h3>' + t.goodToKnow.map(function (g) { return '<div class="gcard">' + h(tx(g)) + '</div>'; }).join('') + '</div>' : '') +
        (t.helpCard ? supportCard() : '') + '</div>';
      setBar(U('missionsShort'), U('startTask'));
      if (desk) showScreen(t.steps[0], null, true);
      if (!first) scrollTop();
    } else if (V.phase === 'steps') {
      var st = t.steps[V.i], n = t.steps.length;
      if (!$('#copy')) {
        ph.innerHTML = '<div class="steprow" id="steprow"></div>' + (desk ? '' : '<div class="stagebox" id="sbox">' + stageHtml() + '</div>') + '<div class="copy" id="copy"></div>';
        if (!desk) bindStage();
      }
      $('#steprow').innerHTML = '<span class="dots" aria-hidden="true">' + t.steps.map(function (s, i) { return '<i class="' + (i === V.i ? 'cur' : (i < V.i ? 'on' : '')) + '"></i>'; }).join('') + '</span><span>' + esc(fmt(U('stepOf'), { n: V.i + 1, total: n })) + '</span>';
      var cp = $('#copy');
      cp.innerHTML = two(st.headline, 'h2') + '<div class="rule"></div><p>' + h(tx(st.text)) + '</p>' +
        (st.helper ? '<p class="helper">' + h(tx(st.helper)) + '</p>' : '') + (REVIEW && st.verify ? '<span class="vtag">CONFIRM · ' + st.id + '</span>' : '') +
        (V.i === 0 && !S.swipe && !desk ? '<div class="swipehint">' + ic('swipe') + esc(U('swipeHint')) + '</div>' : '');
      if (!RM && !first) cp.animate([{ opacity: 0, transform: 'translateX(' + (12 * (V.dir || 1) * (S.lang === 'ar' ? -1 : 1)) + 'px)' }, { opacity: 1, transform: 'none' }], { duration: 260, easing: 'cubic-bezier(.2,.7,.2,1)' });
      setBar(U('back'), V.i === n - 1 ? U('toQuestion') : U('next'));
      if (!desk) mobileLayout();
      showScreen(st, V.dir || 1, false);
      $('#live').textContent = fmt(U('stepOf'), { n: V.i + 1, total: n }) + '. ' + tx(st.text);
    } else if (V.phase === 'quiz') {
      quizHtml(ph);
      setBar(U('back'), V.answered == null ? null : U('taskComplete'), 'check');
      if (desk) showScreen(t.steps[t.steps.length - 1], null, true);
      scrollTop();
    } else if (V.phase === 'result') {
      resultHtml(ph);
      if (desk) showScreen(t.steps[t.steps.length - 1], null, true);
      scrollTop();
    }
  }
  function mobileLayout() {
    // fit phone + copy + bar in one screen with no scrolling
    var sb = $('#sbox'), cp = $('#copy'); if (!sb) return;
    var avail = innerHeight - 56 - $('.strip').offsetHeight - $('#steprow').offsetHeight - cp.offsetHeight - $('#bar').offsetHeight - 12;
    var hgt = Math.max(240, Math.min(avail, innerHeight * 0.62));
    sb.style.height = hgt + 'px';
    var stg = $('#stage'); var w = Math.min(sb.clientWidth, hgt * 820 / 1200);
    stg.style.width = w + 'px'; stg.style.height = (w * 1200 / 820) + 'px';
  }
  function deskLayout() {
    var sb = $('#sbox'), stg = $('#stage'); if (!sb || !stg) return;
    var hgt = sb.clientHeight, w = Math.min(sb.clientWidth, hgt * 820 / 1200);
    stg.style.width = w + 'px'; stg.style.height = (w * 1200 / 820) + 'px';
  }
  var bound = false;
  function bindStage() {
    var slot = $('#slot'), chip = $('#zoomchip');
    if (slot) slot.onclick = openZoom; if (chip) chip.onclick = openZoom;
    var sb = $('#sbox'); if (!sb || sb._sw) return; sb._sw = 1;
    var x0 = null, y0 = 0;
    sb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
    sb.addEventListener('touchend', function (e) {
      if (x0 == null) return; var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0; x0 = null;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.4) { if (dx < 0) goNext(); else goBack(); }
    }, { passive: true });
  }

  /* ---------- animated phone ---------- */
  function showScreen(st, dir, still) {
    var slot = $('#slot'); if (!slot) return;
    if (innerWidth >= 900) deskLayout();
    var src = A('assets/screens/' + st.screen + '.webp');
    var cur = slot.querySelector('img.scr.cur');
    var spot = $('#spot'), ring = $('#hring'), ptr = $('#ptr'), rip = $('#ripple');
    [spot, ring, ptr, rip].forEach(function (e) { e.getAnimations && e.getAnimations().forEach(function (a) { a.cancel(); }); e.style.opacity = 0; });
    slot.setAttribute('aria-label', tx(st.text));
    var changed = !cur || cur.getAttribute('src') !== src;
    var hot = still ? null : st.hotspot;
    var from = (!changed && V.prevHot) ? V.prevHot : null;
    if (changed) {
      var img = new Image(); img.className = 'scr cur'; img.alt = ''; img.src = src; img.decoding = 'async';
      slot.insertBefore(img, slot.firstChild);
      if (cur) {
        cur.classList.remove('cur');
        if (RM || still) { cur.remove(); }
        else {
          var d = dir || 1;
          img.animate([{ transform: 'translateX(' + (14 * d) + '%)', opacity: 0 }, { transform: 'none', opacity: 1 }], { duration: 420, easing: 'cubic-bezier(.2,.7,.2,1)', fill: 'both' });
          var old = cur; old.style.zIndex = 0; img.style.zIndex = 1;
          old.animate([{ transform: 'none', opacity: 1 }, { transform: 'translateX(' + (-8 * d) + '%)', opacity: 0 }], { duration: 380, easing: 'cubic-bezier(.65,0,.35,1)', fill: 'forwards' }).onfinish = function () { old.remove(); };
        }
      }
    }
    var prevScreenSame = !changed;
    V.prevHot = hot;
    [].forEach.call(slot.querySelectorAll('img.scr'), function (im) { im.style.transform = ''; });
    if (!hot) {
      if (!RM && !still) { var c = slot.querySelector('img.scr.cur'); c.animate([{ transform: 'scale(1)' }, { transform: 'scale(1.035)' }], { duration: 2600, easing: 'ease-out', fill: 'forwards', delay: changed ? 420 : 0 }); }
      return;
    }
    var pad = 1.2;
    var r = { x: Math.max(1.2, hot.x - pad), y: Math.max(.6, hot.y - pad * .5) };
    r.w = Math.min(98.8, hot.x + hot.w + pad) - r.x; r.h = Math.min(99.4, hot.y + hot.h + pad * .5) - r.y;
    [spot, ring].forEach(function (e) { e.style.left = r.x + '%'; e.style.top = r.y + '%'; e.style.width = r.w + '%'; e.style.height = r.h + '%'; });
    var tx_ = hot.x + hot.w / 2, ty = hot.y + hot.h / 2;
    rip.style.left = tx_ + '%'; rip.style.top = ty + '%';
    if (RM) { spot.style.opacity = 1; ring.style.opacity = 1; return; }
    var delay = changed ? 300 : 40;
    var sx = from ? from.x + from.w / 2 : 50, sy = from ? from.y + from.h / 2 : 96;
    ptr.style.left = tx_ + '%'; ptr.style.top = ty + '%';
    var dxp = (sx - tx_) * slot.clientWidth / 100, dyp = (sy - ty) * slot.clientHeight / 100;
    var travel = Math.max(480, Math.min(780, Math.hypot(dxp, dyp) * 1.4));
    ptr.animate([
      { transform: 'translate(' + dxp + 'px,' + dyp + 'px) scale(.9)', opacity: 0 },
      { transform: 'translate(' + dxp * .92 + 'px,' + dyp * .92 + 'px) scale(1.15)', opacity: 1, offset: .12 },
      { transform: 'translate(0,0) scale(1.2)', opacity: 1, offset: .82 },
      { transform: 'translate(0,0) scale(1)', opacity: 1 }
    ], { duration: travel, delay: delay, easing: 'cubic-bezier(.65,0,.35,1)', fill: 'forwards' }).onfinish = function () {
      rip.animate([{ transform: 'scale(.4)', opacity: .9 }, { transform: 'scale(2.2)', opacity: 0 }], { duration: 520, easing: 'ease-out' });
      ptr.animate([{ transform: 'scale(1)' }, { transform: 'scale(.82)' }, { transform: 'scale(1)' }], { duration: 260 });
      spot.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 360, delay: 120, fill: 'forwards' });
      ring.animate([{ opacity: 0, transform: 'scale(1.06)' }, { opacity: 1, transform: 'scale(1)' }, { opacity: .75, transform: 'scale(1.03)', offset: .7 }, { opacity: 1, transform: 'scale(1)' }], { duration: 900, delay: 120, fill: 'forwards', easing: 'ease-out' });
      ptr.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 450, delay: 650, fill: 'forwards' });
    };
  }

  function openZoom() {
    var st = V.t.steps[V.phase === 'steps' ? V.i : V.t.steps.length - 1], hot = V.phase === 'steps' ? st.hotspot : null;
    var z = document.createElement('div'); z.className = 'zoom'; z.setAttribute('role', 'dialog'); z.setAttribute('aria-modal', 'true');
    z.innerHTML = '<div class="zt"><button class="btn btn-g" id="zc">' + ic('x') + esc(U('closeImage')) + '</button></div><div class="zs"><div class="zi" id="zi"><img src="' + A('assets/screens/' + st.screen + '.webp') + '" alt="' + esc(tx(st.text)) + '">' +
      (hot ? '<div class="hring" style="left:' + hot.x + '%;top:' + hot.y + '%;width:' + hot.w + '%;height:' + hot.h + '%"></div>' : '') + '</div></div>';
    document.body.appendChild(z);
    var close = function () { z.remove(); document.removeEventListener('keydown', esc_); };
    var esc_ = function (e) { if (e.key === 'Escape') close(); };
    $('#zc', z).onclick = close; document.addEventListener('keydown', esc_);
    $('#zi', z).ondblclick = function () { this.classList.toggle('big'); };
    $('#zc', z).focus();
  }

  /* ---------- quiz & result ---------- */
  function quizHtml(ph) {
    var c = V.t.check, first = !isDone(V.id);
    var keys = S.lang === 'ar' ? ['أ', 'ب', 'ج', 'د'] : ['A', 'B', 'C', 'D'];
    var html = '<div class="panel"><span class="eyebrow">' + esc(U('finalQuestion')) + '</span><div class="qcard"><p class="q">' + h(tx(c.q)) + '</p>' +
      (first ? '<span class="worth">' + ic('star') + esc(fmt(U('questionWorth'), { n: PTS_ANSWER })) + '</span>' : '') + '<div class="opts">';
    V.order.forEach(function (oi, k) {
      var o = c.options[oi], cls = '', mark = keys[k];
      if (V.answered != null) {
        if (o.correct) { cls = ' right'; mark = ic('check'); }
        else if (oi === V.answered) { cls = ' wrong'; mark = ic('x'); }
        else cls = ' dim';
      }
      html += '<button class="opt' + cls + '" data-o="' + oi + '"' + (V.answered != null ? ' disabled' : '') + '><span class="k">' + mark + '</span><span>' + h(tx(o.text)) + '</span></button>';
    });
    html += '</div>';
    if (V.answered != null) {
      var a = c.options[V.answered], right = c.options.filter(function (o) { return o.correct; })[0];
      var pick = function (arr) { return arr[(V.id.length + V.i) % arr.length]; };
      html += a.correct ? '<div class="fb in"><b>' + esc(U('correct')) + ' ' + esc(pick(U('praise'))) + '</b><p>' + h(tx(a.why)) + '</p></div>'
        : '<div class="fb in"><b>' + esc(U('notQuite')) + '</b><p>' + h(tx(a.why)) + '</p><p class="ra">' + esc(U('rightAnswer')) + ' ' + h(tx(right.text)) + '</p><p>' + h(tx(right.why)) + '</p><p class="enc">' + esc(pick(U('encourage'))) + '</p></div>';
    }
    ph.innerHTML = html + '</div></div>';
    [].forEach.call(ph.querySelectorAll('.opt'), function (b) {
      b.onclick = function () {
        if (V.answered != null) return;
        V.answered = +b.getAttribute('data-o');
        quizHtml(ph); setBar(U('back'), U('taskComplete'), 'check');
        var fb = ph.querySelector('.fb'); if (fb && fb.scrollIntoView) fb.scrollIntoView({ block: 'nearest', behavior: RM ? 'auto' : 'smooth' });
        $('#live').textContent = ph.querySelector('.fb').textContent;
      };
    });
  }
  function complete() {
    var first = !isDone(V.id), correct = V.t.check.options[V.answered].correct;
    var m = V.m, wasDone = mStats(m).done === m.tasks.length;
    V.earned = null;
    if (first) {
      var pts = PTS_TASK + (correct ? PTS_ANSWER : 0);
      S.prog[V.id] = { done: true, correct: correct, pts: pts }; save();
      V.earned = { task: PTS_TASK, answer: correct ? PTS_ANSWER : 0 };
      track('task_done', V.id, pts);
      if (!wasDone && mStats(m).done === m.tasks.length) { V.missionJustDone = true; track('mission_done', m.id, null); }
      bumpPoints();
    }
  }
  function resultHtml(ph) {
    var m = V.m, s = mStats(m), nx = nextTask(m, V.id), e = V.earned;
    var html = '<div class="panel result"><div class="medal">' + ic(s.done === s.total ? 'trophy' : 'check') + '</div><h1 class="two"><span>' + h(U('taskComplete')) + '</span></h1><div class="rule"></div><p class="purpose">' + h(tx(V.t.outcome) || '') + '</p>' +
      (e ? '<div class="earn"><div><span>' + esc(U('earnedTask')) + '</span><b>' + esc(fmt(U('earned'), { n: e.task })) + '</b></div><div class="' + (e.answer ? '' : 'no') + '"><span>' + esc(U('earnedAnswer')) + '</span><b>' + esc(fmt(U('earned'), { n: e.answer })) + '</b></div></div>' : '') +
      '<div class="pbar" style="max-width:460px;margin:20px auto 0"><div class="lbl"><span>' + h(tx(m.title)) + '</span><span>' + esc(fmt(U('tasksDone'), { done: s.done, total: s.total })) + '</span></div><div class="track"><i data-w="' + s.pct + '" style="width:' + Math.round(100 * Math.max(0, s.done - (e ? 1 : 0)) / s.total) + '%"></i></div></div>';
    if (nx) html += '<div class="nextcard"><span class="eyebrow">' + esc(U('nextTask')) + '</span><ul class="tlist" style="margin:0">' + taskRow(nx, m.tasks.indexOf(nx) + 1) + '</ul></div>';
    else html += '<div class="mdone"><span class="eyebrow">' + esc(U('badge')) + '</span><h2>' + esc(U('missionDone')) + '</h2><p>' + h(U('missionDoneLine')) + '</p></div>';
    ph.innerHTML = html + '</div>';
    setBar(U('replay'), nx ? U('nextTask') : U('backToMissions'));
    $('#bk').innerHTML = ic('refresh') + '<span class="t">' + esc(U('replay')) + '</span>';
    requestAnimationFrame(function () { requestAnimationFrame(function () { var i = ph.querySelector('.track i'); if (i) i.style.width = i.getAttribute('data-w') + '%'; }); });
    if (V.missionJustDone) { V.missionJustDone = false; confetti(); }
  }
  function confetti() {
    if (RM) return;
    var c = document.createElement('div'); c.className = 'confetti'; var cols = ['#C9A87C', '#FAF6F0', '#e3cba6', '#1B2A4A'];
    for (var i = 0; i < 60; i++) {
      var p = document.createElement('i'); p.style.left = Math.random() * 100 + '%'; p.style.background = cols[i % 4];
      c.appendChild(p);
      p.animate([{ transform: 'translateY(0) rotate(0)' }, { transform: 'translateY(' + (innerHeight + 40) + 'px) rotate(' + (360 + Math.random() * 540) + 'deg)' }], { duration: 1800 + Math.random() * 1600, delay: Math.random() * 500, easing: 'cubic-bezier(.3,.6,.4,1)', fill: 'forwards' });
    }
    document.body.appendChild(c); setTimeout(function () { c.remove(); }, 4200);
  }

  /* ---------- navigation ---------- */
  function goNext() {
    if (!V) return;
    var n = V.t.steps.length;
    if (V.phase === 'intro') { V.phase = 'steps'; V.i = 0; V.dir = 1; V.prevHot = null; taskView(); return; }
    if (V.phase === 'steps') {
      if (!S.swipe && V.i === 0) { S.swipe = 1; save(); }
      if (V.i < n - 1) { V.i++; V.dir = 1; renderPhase(); }
      else { V.phase = 'quiz'; V.answered = null; V.order = reorder(V.t.check); taskView(); }
      return;
    }
    if (V.phase === 'quiz') { if (V.answered == null) return; complete(); V.phase = 'result'; taskView(); return; }
    if (V.phase === 'result') {
      var nx = nextTask(V.m, V.id);
      if (nx) { S.curM = V.m.id; save(); location.hash = '#/task/' + nx; } else location.hash = '#/';
    }
  }
  function goBack() {
    if (!V) return;
    if (V.phase === 'intro') { location.hash = '#/'; return; }
    if (V.phase === 'steps') { if (V.i > 0) { V.i--; V.dir = -1; renderPhase(); } else { V.phase = 'intro'; taskView(); } return; }
    if (V.phase === 'quiz') { V.phase = 'steps'; V.i = V.t.steps.length - 1; V.dir = -1; V.prevHot = null; taskView(); return; }
    if (V.phase === 'result') { V.phase = 'intro'; V.answered = null; taskView(); }
  }
  // shuffle and make sure the right answer moves between attempts
  function reorder(c) {
    var o, ci = c.options.map(function (x) { return x.correct; }).indexOf(true), tries = 0, last = S.lastPos;
    do { o = shuffle(c.options.length); tries++; } while (tries < 8 && o.indexOf(ci) === last);
    S.lastPos = o.indexOf(ci); save();
    return o;
  }
  document.addEventListener('keydown', function (e) {
    if (!V || location.hash.indexOf('#/task/') !== 0 || document.querySelector('.zoom')) return;
    if (/input|select|textarea/i.test((e.target.tagName || ''))) return;
    if (e.key === 'ArrowRight') goNext(); else if (e.key === 'ArrowLeft') goBack();
  });
  var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { if (V && location.hash.indexOf('#/task/') === 0) { var d = innerWidth >= 900; if (d !== V.desk) { V.desk = d; taskView(); } else if (V.phase === 'steps') { d ? deskLayout() : mobileLayout(); } } }, 150); });

  /* ---------- router ---------- */
  function render(keep) {
    setLangAttrs();
    var keepV = keep && V && location.hash.indexOf('#/task/') === 0;
    app.innerHTML = header(); bindHeader();
    var hs = location.hash || '#/';
    if (hs.indexOf('#/task/') === 0) {
      var id = hs.slice(7);
      if (keepV && V.id === id) { V.desk = innerWidth >= 900; taskView(); } else { startTask(id); if (V) V.desk = innerWidth >= 900; }
      document.body.classList.add('in-task');
    } else {
      V = null; document.body.classList.remove('in-task');
      if (hs === '#/help') help(); else home();
    }
    if (!keep) scrollTop();
  }
  window.addEventListener('hashchange', function () { render(); });
  render();
  try { if (!sessionStorage.getItem('hits3o')) { sessionStorage.setItem('hits3o', 1); track('open', '', null); } } catch (e) { track('open', '', null); }
})();
