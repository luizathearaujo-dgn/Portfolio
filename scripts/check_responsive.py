#!/usr/bin/env python3
"""
Teste responsivo: abre cada página em várias larguras e detecta rolagem horizontal,
indicando os elementos que ultrapassam a viewport. Também testa menu mobile e formulário.

Requisitos: pip install playwright && playwright install chromium
Uso (na raiz do projeto):  python3 scripts/check_responsive.py
"""
import glob, os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WIDTHS = [320, 360, 390, 480, 768, 1024, 1280, 1440, 1920]
PAGES = sorted(glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "trabalhos", "*.html")))

JS_OFFENDERS = """() => {
  const vw = document.documentElement.clientWidth, out = [];
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width && (r.right > vw + 1 || r.left < -1)) out.push(el.tagName.toLowerCase() + '.' + (el.className || '') + ' right=' + Math.round(r.right));
  });
  return {overflow: document.documentElement.scrollWidth > vw, vw, sw: document.documentElement.scrollWidth, out: out.slice(0, 5)};
}"""

problems = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in WIDTHS:
        pg = b.new_page(viewport={"width": w, "height": 800})
        for f in PAGES:
            pg.goto("file://" + f, wait_until="domcontentloaded")
            r = pg.evaluate(JS_OFFENDERS)
            if r["overflow"]:
                problems += 1
                print(f"✗ {w}px  {os.path.relpath(f, ROOT)}  scrollWidth={r['sw']} > {r['vw']}  {r['out']}")
        pg.close()

    # Menu mobile: abre, fecha com Esc, aria-expanded coerente
    pg = b.new_page(viewport={"width": 375, "height": 800})
    pg.goto("file://" + os.path.join(ROOT, "index.html"))
    btn = pg.locator(".menu-btn")
    assert pg.locator("#menu").is_hidden(), "menu deveria iniciar fechado no mobile"
    btn.click(); assert btn.get_attribute("aria-expanded") == "true" and pg.locator("#menu").is_visible()
    pg.keyboard.press("Escape"); assert btn.get_attribute("aria-expanded") == "false" and pg.locator("#menu").is_hidden()
    print("✓ menu mobile: abre, fecha com Esc, aria-expanded correto")

    # Formulário sem endpoint: não pode simular sucesso
    pg.goto("file://" + os.path.join(ROOT, "contato.html"))
    pg.fill("#f-name", "Teste"); pg.fill("#f-email", "t@t.com"); pg.fill("#f-subject", "Oi"); pg.fill("#f-message", "Mensagem")
    pg.click("button[type=submit]")
    st = pg.locator("#form-status")
    assert st.get_attribute("data-state") == "info" and "não foi enviada" in st.inner_text()
    print("✓ formulário sem integração: avisa que NÃO enviou (não simula sucesso)")
    b.close()

print(f"\n{'✓ Sem rolagem horizontal' if not problems else '✗ ' + str(problems) + ' ocorrência(s)'} "
      f"em {len(PAGES)} páginas × {len(WIDTHS)} larguras")
sys.exit(1 if problems else 0)
