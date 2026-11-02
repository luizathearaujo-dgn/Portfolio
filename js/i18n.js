/**
 * i18n.js — troca de idioma PT-BR <-> EN, sem recarregar a página.
 *
 * - O HTML é entregue em português (padrão). Ao escolher EN, cada texto é trocado pelo equivalente em
 *   window.I18N.en (arquivo gerado js/translations.js, a partir de i18n_en.py).
 * - Também traduz atributos (alt, aria-label, placeholder, title), <title> e as meta descrições.
 * - A escolha fica em localStorage ("lang") e vale em todas as páginas e visitas futuras NAQUELE dispositivo.
 * - Visitantes novos veem português (pt-BR).
 */
(function () {
  'use strict';
  var KEY = 'lang', root = document.documentElement;
  var DATA = window.I18N || {}, EN = DATA.en || {}, UI = DATA.ui || {};
  var ATTRS = ['alt', 'aria-label', 'placeholder', 'title'];
  var META = ['meta[name="description"]', 'meta[property="og:title"]', 'meta[property="og:description"]'];
  var textStore = new WeakMap(), attrStore = new WeakMap(), titleOrig = document.title, lang = 'pt-BR';

  function read() { try { return localStorage.getItem(KEY) === 'en' ? 'en' : 'pt-BR'; } catch (e) { return 'pt-BR'; } }
  function write(l) { try { localStorage.setItem(KEY, l); } catch (e) { /* armazenamento indisponível: segue sem persistir */ } }
  function norm(s) { return s.replace(/\s+/g, ' ').trim(); }
  function tr(s) { var k = norm(s); return Object.prototype.hasOwnProperty.call(EN, k) ? EN[k] : null; }

  function apply(l) {
    var en = l === 'en', walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT), n, orig, t, p;
    while ((n = walker.nextNode())) {
      p = n.parentNode;
      if (/^(SCRIPT|STYLE|NOSCRIPT)$/.test(p.nodeName) || (p.closest && p.closest('[data-i18n-skip]'))) continue;
      orig = textStore.get(n);
      if (orig === undefined) { orig = norm(n.nodeValue) ? n.nodeValue : null; textStore.set(n, orig); }
      if (orig === null) continue;
      t = en ? tr(orig) : null;
      n.nodeValue = t !== null ? orig.match(/^\s*/)[0] + t + orig.match(/\s*$/)[0] : orig;
    }
    document.querySelectorAll('[alt],[aria-label],[placeholder],[title]').forEach(function (el) {
      var st = attrStore.get(el);
      if (!st) { st = {}; ATTRS.forEach(function (a) { if (el.hasAttribute(a)) st[a] = el.getAttribute(a); }); attrStore.set(el, st); }
      Object.keys(st).forEach(function (a) { t = en ? tr(st[a]) : null; el.setAttribute(a, t !== null ? t : st[a]); });
    });
    t = en ? tr(titleOrig) : null; document.title = t !== null ? t : titleOrig;
    META.forEach(function (sel) {
      var m = document.querySelector(sel); if (!m) return;
      if (!m.dataset.pt) m.dataset.pt = m.getAttribute('content');
      t = en ? tr(m.dataset.pt) : null; m.setAttribute('content', t !== null ? t : m.dataset.pt);
    });
  }

  function paintSwitch(l) {
    document.querySelectorAll('[data-lang]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.lang === l)); });
  }

  function setLang(l, persist) {
    lang = l === 'en' ? 'en' : 'pt-BR';
    apply(lang);
    root.lang = lang;
    paintSwitch(lang);
    if (persist !== false) write(lang);
    document.dispatchEvent(new CustomEvent('languagechange', { detail: { lang: lang } }));
  }

  // API usada por outros scripts (ex.: mensagens do formulário)
  window.i18n = {
    get lang() { return lang; },
    t: function (key, vars) {
      var s = (UI[lang] && UI[lang][key]) || (UI['pt-BR'] && UI['pt-BR'][key]) || key;
      Object.keys(vars || {}).forEach(function (k) { s = s.split('{' + k + '}').join(vars[k]); });
      return s;
    }
  };

  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-lang]');
    if (b) setLang(b.dataset.lang);
  });
  window.addEventListener('storage', function (e) { if (e.key === KEY) setLang(read(), false); }); // sincroniza abas abertas

  lang = read();
  if (lang === 'en') setLang('en', false); else { paintSwitch(lang); root.lang = 'pt-BR'; }
  root.classList.remove('i18n-pending');
})();
