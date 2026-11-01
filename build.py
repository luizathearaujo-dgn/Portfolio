#!/usr/bin/env python3
"""
build.py — gera as páginas HTML estáticas do portfólio.

Uso:
    python3 build.py              # gera as páginas (imagens remotas do Framer, se não houver locais)
    python3 build.py --download   # baixa as imagens para assets/img/ e gera usando cópias locais

Estrutura: 1) CONFIG  2) CONTEÚDO  3) COMPONENTES  4) PÁGINAS.
Para editar textos, projetos ou links, altere as seções 1 e 2 e rode o script de novo.
O HTML gerado é estático: pode ser publicado em qualquer hospedagem.
"""
import html, json, os, re, sys, urllib.request

# 1. CONFIG ---------------------------------------------------------------
SITE = "https://SEU-DOMINIO.com.br"        # TROQUE pelo domínio final (canonical, sitemap, Open Graph)
NAME, ROLE = "Luíza Araújo", "Product Designer"
EMAIL = "luizathearaujo@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/luiza-the-araujo/"
INSTAGRAM = "https://www.instagram.com/luizathearaujo.design/"
CV = "https://drive.google.com/file/d/1tVH7KKMKC_sWvBa-YASBtUuK7AV2qZm1/view?usp=sharing"
FORM_ENDPOINT = ""                          # URL do serviço de e-mail (ex.: https://formspree.io/f/xxxxxxx). Vazio = não envia.
DESC = "Portfólio de Luíza Araújo, Product Designer: projetos de interface e UX com estética minimalista, agradável e simples de usar."
FB = "https://framerusercontent.com/images/"
OG_IMAGE = "https://framerusercontent.com/assets/Nl1fcH3IRXSe6rc7JmywGI36Jp4.jpg"
IMGS = set()                                # imagens usadas (para --download)

# 2. CONTEÚDO -------------------------------------------------------------
# Blocos: ("p", texto) ("h3", texto) ("ul", [itens]) ("img", [arquivos], alt)  — **negrito** é aceito.
PROJECTS = [
 dict(slug="indexponto", year="2025", area="UI/UX", title="IndexPonto", time="32 dias", tools="Figma",
  summary="O IndexPonto é um sistema de ponto eletrônico desenvolvido para modernizar o controle de jornada de servidores públicos.",
  cover=("dpFfXagJD4o3bU8u3H9I2oIgVo.png", "Capa do projeto IndexPonto", 2880, 2048), sections=[
  ("Contexto", [("p", "A gestão de ponto, especialmente no setor público, ainda enfrenta os seguintes desafios estruturais:"), ("ul", ["Processos manuais e burocráticos", "Dificuldade no controle de horas, faltas e atrasos", "Baixa visibilidade para gestores", "Inconsistências em auditorias", "Falta de rastreabilidade dos dados"])]),
  ("Objetivo", [("ul", ["Digitalizar o controle de jornada;", "Reduzir erros operacionais;", "Acompanhar a carga horária dos funcionários;", "Aumentar a transparência entre usuários e gestão;", "Agilizar processos e análises de solicitações;", "Garantir conformidade com normas legais."])]),
  ("Processo de design", [("p", "O projeto foi criado com base na metodologia Double Diamond adaptada, devido à ausência de contato com usuários durante o desenvolvimento, concentrando validações nas etapas internas."), ("img", ["os8OZQgEcN2IzZKDUZN8UNrCpws.png"], "Diagrama do processo de design (Double Diamond adaptado)")]),
  ("Cronograma de projeto", [("p", "O cronograma exibe o planejamento e deadlines em que as etapas de design foram delimitadas, garantindo alinhamento com o time e previsibilidade no desenvolvimento."), ("img", ["qrva5yIVLnVq0oY3yKXX9afZWi4.png"], "Cronograma do projeto"), ("img", ["qzLlm2XlR4UKmQRJto6NinjxsY.png", "CLJ1HsIh1ozBxkzalUjdcUx6Fg.png"], "Detalhamento das etapas do cronograma")]),
  ("Direcionamentos de UX", [("p", "Decisões tomadas com base no entendimento das dores dos usuários, nas regras do sistema e na busca por uma experiência mais simples, clara e eficiente."), ("img", ["aQ0PKEnNFqD43vsNaaNczgFPO64.png"], "Direcionamento de UX do IndexPonto"), ("img", ["J6VNGDIL5jWhC9em6vGzuab1HsE.png"], "Telas do IndexPonto")])]),
]
JOBS = [
 ("2025 — Atualmente", "IndexTech", "Web Designer Pleno", "Atuo na criação de identidades visuais e interfaces web. Contribuo para design systems, promovendo padronização e escalabilidade dos produtos."),
 ("2021 — Atualmente", "SmartRetail/IMD", "Product Designer Pleno", "Colaboro com times multidisciplinares, realizo a manutenção do design system e a validação de soluções com usuários."),
 ("2019 — 2020", "PROPESQ", "Web designer", "Construção de identidades visuais e diagramação de manuais para eventos científicos da UFRN."),
]
TOOLS = [("Figma", "Product design"), ("Adobe XD", "Product design"), ("Framer", "Web design"), ("Maze", "Testes de usabilidade"), ("Miro", "Jornadas e fluxos"),
         ("Hotjar", "Análise de dados"), ("Notion", "Documentação e organização"), ("Jira", "Organização e planejamento"), ("Claude", "Ferramenta de apoio")]
PORTRAIT = "ldjrPg1f5fQ71f6M3f9obrigyjw.png"

# 3. COMPONENTES ----------------------------------------------------------
def esc(t):
    """Escapa HTML e converte **negrito**."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html.escape(t, quote=False))

def img(f, alt, w=1600, h=1000, eager=False, sizes="(min-width: 60rem) 60vw, 100vw", root=""):
    """<img> otimizada: lazy-load, dimensões (evita salto de layout) e srcset quando remota."""
    IMGS.add(f)
    if os.path.exists(f"assets/img/{f}"):
        src, extra = f"{root}assets/img/{f}", ""
    else:
        src = FB + f
        extra = ' srcset="%s" sizes="%s"' % (", ".join(f"{FB}{f}?scale-down-to={n} {n}w" for n in (512, 1024, 2048)), sizes)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="{src}"{extra} alt="{html.escape(alt)}" width="{w}" height="{h}" {load} decoding="async">'

def head(title, desc, path, root, ld=None):
    ldjson = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}/{path}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}/{path}"><meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f5f6f8">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<script>document.documentElement.classList.add('js')</script>
<link rel="stylesheet" href="{root}css/styles.css">
<script src="{root}js/site.js" defer></script>
{ldjson}
</head>"""

def header(root, active):
    items = [("projetos.html", "Projetos", "projetos"), ("sobre-mim.html", "Sobre mim", "sobre"), ("contato.html", "Contato", "contato")]
    lis = "".join(f'<li><a href="{root}{h}"{" aria-current=\"page\"" if k == active else ""}>{t}</a></li>' for h, t, k in items)
    return f"""<a class="skip-link" href="#conteudo">Ir para o conteúdo</a>
<header class="site-header"><div class="container bar">
<a class="brand" href="{root}index.html"><strong>{NAME}</strong><span> | The UX</span></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
<nav id="menu" class="nav" aria-label="Principal"><ul>{lis}</ul></nav>
</div></header>"""

def footer(root):
    return f"""<footer class="site-footer"><div class="container footer-grid">
<div><p><strong>{NAME}</strong><br><span class="muted">{ROLE}</span></p></div>
<nav aria-label="Rodapé"><h2>Navegação</h2><ul><li><a href="{root}projetos.html">Projetos</a></li><li><a href="{root}sobre-mim.html">Sobre mim</a></li><li><a href="{root}contato.html">Contato</a></li></ul></nav>
<div><h2>Contato</h2><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">LinkedIn<span class="visually-hidden"> (abre em nova aba)</span></a></li><li><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">Instagram<span class="visually-hidden"> (abre em nova aba)</span></a></li></ul></div>
</div></footer>"""

def cta(root):
    return f"""<section class="cta section" aria-labelledby="cta-t"><div class="container cta__inner">
<p class="muted">Fale comigo</p>
<h2 id="cta-t">Disponível para projetos, colaborações e oportunidades em design. Entre em contato para conversarmos.</h2>
<a class="btn btn--light" href="{root}contato.html">Vamos conversar!</a></div></section>"""

def project_row(p, root):
    return f'<li><a class="project-row" href="{root}trabalhos/{p["slug"]}.html"><span class="project-row__meta">{p["year"]} · {p["area"]}</span><span class="project-row__title">{html.escape(p["title"])}</span></a></li>'

def project_card(p, root):
    f, alt, w, h = p["cover"]
    return f'''<li><a class="card" href="{root}trabalhos/{p["slug"]}.html"><div class="card__media">{img(f, alt, w, h, root=root, sizes="(min-width: 48rem) 45vw, 100vw")}</div>
<span class="card__meta">{p["year"]} · {p["area"]}</span><h3 class="card__title">{html.escape(p["title"])}</h3><p>{html.escape(p["summary"])}</p></a></li>'''

def render_blocks(blocks, root):
    out = []
    for b in blocks:
        if b[0] == "p": out.append(f"<p>{esc(b[1])}</p>")
        elif b[0] == "h3": out.append(f"<h3>{esc(b[1])}</h3>")
        elif b[0] == "ul": out.append("<ul>" + "".join(f"<li>{esc(i)}</li>" for i in b[1]) + "</ul>")
        elif b[0] == "img":
            cls = "figure figure--single" if len(b[1]) == 1 else "figure"
            out.append(f'<div class="{cls}">' + "".join(f'<div>{img(f, b[2], root=root)}</div>' for f in b[1]) + "</div>")
    return "\n".join(out)

def page(path, title, desc, body, active="", ld=None):
    root = "../" * path.count("/")
    html_ = f"""{head(title, desc, path, root, ld)}
<body>
{header(root, active)}
<main id="conteudo" tabindex="-1">
{body(root)}
</main>
{footer(root)}
</body>
</html>
"""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh: fh.write(html_)

# 4. PÁGINAS --------------------------------------------------------------
def build():
    IMGS.clear()
    os.makedirs("assets/img", exist_ok=True)
    ld = {"@context": "https://schema.org", "@type": "Person", "name": NAME, "jobTitle": ROLE, "url": SITE, "email": EMAIL,
          "address": {"@type": "PostalAddress", "addressLocality": "Parnamirim", "addressRegion": "RN", "addressCountry": "BR"},
          "sameAs": [LINKEDIN, INSTAGRAM]}

    page("index.html", f"{NAME} — {ROLE}", DESC, lambda r: f"""
<section class="hero"><div class="container">
<h1>Clareza como resultado de decisões bem projetadas.</h1>
<p class="hero__lead">Cada detalhe tem um porquê. O essencial, sem ruído.</p></div></section>
<section class="section" style="padding-top:0" aria-labelledby="proj-t"><div class="container">
<h2 id="proj-t" class="visually-hidden">Projetos</h2>
<ul class="project-list">{"".join(project_row(p, r) for p in PROJECTS)}</ul></div></section>
{cta(r)}""", ld=ld)

    page("projetos.html", f"Projetos — {NAME}", "Projetos de produto com foco em usabilidade, eficiência e soluções para contextos complexos.", lambda r: f"""
<section class="page-head"><div class="container"><h1>Projetos</h1>
<p>Projetos de produto com foco em usabilidade, eficiência e soluções para contextos complexos. Cada projeto apresenta como estruturo problemas, crio fluxos e evoluo soluções digitais.</p></div></section>
<section class="section" style="padding-top:2rem"><div class="container"><ul class="card-grid">{"".join(project_card(p, r) for p in PROJECTS)}</ul></div></section>
{cta(r)}""", active="projetos")

    def about(r):
        jobs = "".join(f'<li><p class="when">{w}</p><div><h3>{c}</h3><p class="muted" style="margin:0">{role}</p><p>{d}</p></div></li>' for w, c, role, d in JOBS)
        tools = "".join(f"<li><strong>{n}</strong><span>{d}</span></li>" for n, d in TOOLS)
        return f"""
<section class="page-head"><div class="container"><h1>Sobre mim</h1>
<p>Busco impactar sistemas, transformando problemas complexos em designs funcionais e eficientes.</p></div></section>
<section class="section" style="padding-top:2rem"><div class="container about-grid"><div>
<dl class="facts"><div><dt>Experiência</dt><dd>5 anos</dd></div><div><dt>De onde sou</dt><dd>Parnamirim, RN</dd></div><div><dt>Atuação</dt><dd>Product designer</dd></div></dl>
<h2 class="section-title" style="font-size:var(--fs-h3);margin-bottom:.75rem">Motivação</h2>
<p class="statement"><strong>O Design transforma a maneira como vemos o mundo, e ao percebermos suas barreiras, enxergamos também como o Design pode transformá-lo.</strong> Busco descobrir soluções visuais que equilibram forma e propósito, em que cada detalhe tem intenção e a simplicidade se destaca.</p></div>
{img(PORTRAIT, "Foto de " + NAME, 1526, 1514, eager=True, root=r, sizes="(min-width: 56rem) 45vw, 100vw").replace('<img ', '<img class="about-photo" ')}
</div></section>
<section class="section" style="padding-top:0" aria-labelledby="exp-t"><div class="container"><h2 id="exp-t" class="section-title">Experiência profissional</h2><ul class="timeline">{jobs}</ul></div></section>
<section class="section" style="padding-top:0" aria-labelledby="tools-t"><div class="container"><h2 id="tools-t" class="section-title">Ferramentas</h2><ul class="tools">{tools}</ul></div></section>
{cta(r)}"""
    page("sobre-mim.html", f"Sobre mim — {NAME}", "Product designer com 5 anos de experiência, em Parnamirim, RN. Experiência, motivação e ferramentas.", about, active="sobre")

    def contact(r):
        def link(href, small, strong, ext=True):
            t = ' target="_blank" rel="noopener noreferrer"' if ext else ""
            return f'<a href="{href}"{t}><small>{small}</small><strong>{strong}</strong></a>'
        return f"""
<section class="page-head"><div class="container"><h1>Vamos construir algo!</h1>
<p>Se você tem um desafio de produto ou quer trocar uma ideia, vamos conversar.</p></div></section>
<section class="section" style="padding-top:2rem"><div class="container contact-grid">
<div class="contact-links">{link("mailto:" + EMAIL, "E-mail", EMAIL, False)}{link(LINKEDIN, "LinkedIn", "Luíza de Araújo")}{link(INSTAGRAM, "Instagram", "@luizathearaujo.design")}{link(CV, "Currículo", "Clique e visualize")}</div>
<form id="contact-form" class="form" data-endpoint="{FORM_ENDPOINT}" data-fallback-email="{EMAIL}" method="post" action="{FORM_ENDPOINT or '#'}">
<div class="field"><label for="f-name">Nome</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
<div class="field"><label for="f-email">E-mail</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="f-subject">Assunto</label><input id="f-subject" name="subject" type="text" required></div>
<div class="field"><label for="f-message">Mensagem</label><textarea id="f-message" name="message" required></textarea></div>
<div class="hp" aria-hidden="true"><label>Não preencha<input name="_gotcha" type="text" tabindex="-1" autocomplete="off"></label></div>
<p id="form-status" class="form__status" role="status" aria-live="polite"></p>
<div><button class="btn" type="submit">Enviar mensagem</button></div>
</form></div></section>"""
    page("contato.html", f"Contato — {NAME}", "Se você tem um desafio de produto ou quer trocar uma ideia, vamos conversar.", contact, active="contato")

    for p in PROJECTS:
        def case(r, p=p):
            f, alt, w, h = p["cover"]
            others = "".join(project_row(o, r) for o in PROJECTS if o is not p)
            secs = "".join(f'<section class="case-section" aria-labelledby="s{i}"><h2 id="s{i}">{html.escape(t)}</h2><div class="case-section__body">{render_blocks(b, r)}</div></section>' for i, (t, b) in enumerate(p["sections"]))
            return f"""
<article><div class="container">
<header class="page-head" style="padding-inline:0"><h1>{html.escape(p["title"])}</h1><p>{html.escape(p["summary"])}</p></header>
<dl class="case-meta"><div><dt>Ano</dt><dd>{p["year"]}</dd></div><div><dt>Tempo</dt><dd>{p["time"]}</dd></div><div><dt>Ferramentas</dt><dd>{p["tools"]}</dd></div><div><dt>Área</dt><dd>{p["area"]}</dd></div></dl>
<figure class="case-cover">{img(f, alt, w, h, eager=True, root=r, sizes="100vw")}</figure>
{secs}
{('<div class="more-projects"><h2 class="section-title">Veja outros projetos</h2><ul class="project-list">' + others + '</ul></div>') if others else ""}
</div></article>
<div class="section"></div>{cta(r)}"""
        page(f"trabalhos/{p['slug']}.html", f"{p['title']} — {NAME}", p["summary"], case, active="projetos")

    open("assets/favicon.svg", "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#15171d"/><path d="M22 14v30h22" fill="none" stroke="#f5f6f8" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    urls = ["index.html", "projetos.html", "sobre-mim.html", "contato.html"] + [f"trabalhos/{p['slug']}.html" for p in PROJECTS]
    open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    build()
    if "--download" in sys.argv:
        for f in sorted(IMGS):
            dest = f"assets/img/{f}"
            if not os.path.exists(dest):
                try: urllib.request.urlretrieve(FB + f, dest); print("baixada:", f)
                except Exception as e: print("falhou:", f, e)
        build()
    print("Páginas geradas.")
