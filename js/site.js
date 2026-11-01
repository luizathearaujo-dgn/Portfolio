/**
 * site.js — comportamento do site (sem dependências).
 *  1. Menu mobile e estado do cabeçalho acessível (aria-expanded, Esc fecha, foco volta ao botão)
 *  2. Formulário de contato com integração externa (ex.: Formspree, Web3Forms, Getform)
 */

/* 1. MENU MOBILE ------------------------------------------------------- */
(function () {
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('menu');
  if (!btn || !nav) return;

  var header = document.querySelector('.site-header');
  function setOpen(open) {
    btn.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
    header.classList.toggle('menu-open', open);   // fundo escuro enquanto o menu está aberto
  }
  btn.addEventListener('click', function () {
    setOpen(btn.getAttribute('aria-expanded') !== 'true');
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
      btn.focus();
    }
  });
  window.matchMedia('(min-width: 48rem)').addEventListener('change', function (m) {
    if (m.matches) setOpen(false);
  });
})();

/* 1b. CABEÇALHO: transparente no topo, sólido ao rolar */
(function () {
  var root = document.documentElement;
  function update() { root.classList.toggle('at-top', window.scrollY < 8); }
  update();
  window.addEventListener('scroll', update, { passive: true });
})();

/* 2. FORMULÁRIO DE CONTATO --------------------------------------------- */
(function () {
  var form = document.getElementById('contact-form');
  if (!form) return;
  var status = document.getElementById('form-status');
  var button = form.querySelector('button[type="submit"]');
  var fallbackEmail = form.dataset.fallbackEmail;

  function show(state, text) {
    status.dataset.state = state;
    status.textContent = text;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;                 // validação nativa (campos obrigatórios, e-mail)
    if (form.elements._gotcha && form.elements._gotcha.value) return; // honeypot anti-spam

    var endpoint = (form.dataset.endpoint || '').trim();
    if (!endpoint) {
      // Integração ainda não configurada: NÃO simulamos envio.
      show('info', 'O envio por este formulário ainda não foi ativado. Sua mensagem não foi enviada. ' +
        'Escreva diretamente para ' + fallbackEmail + '.');
      return;
    }

    button.disabled = true;
    show('info', 'Enviando…');
    fetch(endpoint, {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' }
    }).then(function (res) {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      form.reset();
      show('success', 'Mensagem enviada. Responderei assim que possível.');
    }).catch(function () {
      show('error', 'Não foi possível enviar a mensagem. Tente novamente ou escreva para ' + fallbackEmail + '.');
    }).finally(function () {
      button.disabled = false;
    });
  });
})();
