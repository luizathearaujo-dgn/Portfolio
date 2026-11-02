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
from html.parser import HTMLParser
from i18n_en import EN as TR_EN, UI as TR_UI, IDENTITY

# 1. CONFIG ---------------------------------------------------------------
SITE = "https://luiza-araujo.theux.workers.dev"  # TROQUE pelo domínio próprio, se registrar um (canonical, sitemap, Open Graph)
NAME, ROLE = "Luíza Araújo", "Product Designer"
EMAIL = "luizathearaujo@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/luiza-the-araujo/"
INSTAGRAM = "https://www.instagram.com/luizathearaujo.design/"
BEHANCE = "https://www.behance.net/luizathearaujo"
CV = "https://drive.google.com/file/d/1tVH7KKMKC_sWvBa-YASBtUuK7AV2qZm1/view?usp=sharing"
FORM_ENDPOINT = ""                          # URL do serviço de e-mail (ex.: https://formspree.io/f/xxxxxxx). Vazio = não envia.
DESC = "Portfólio de Luíza Araújo, Product Designer: projetos de interface e UX com estética minimalista, agradável e simples de usar."
FB = "https://framerusercontent.com/images/"
OG_IMAGE = SITE + "/assets/img/og.jpg"
ICON_STYLE = "filled"                       # estilo dos ícones de serviços: "filled" (silhueta) ou "outlined" (traço)
IMGS = set()                                # imagens usadas (para --download)

# 2. CONTEÚDO -------------------------------------------------------------
# Blocos: ("p", texto) ("h3", texto) ("ul", [itens]) ("img", [arquivos], alt)  — **negrito** é aceito.
PROJECTS = [
 dict(slug="indexponto", year="2025", area="UI/UX", title="IndexPonto", time="32 dias", tools="Figma",
  intro="O IndexPonto é um sistema de ponto eletrônico desenvolvido para modernizar o controle de jornada de servidores públicos. O projeto busca digitalizar esse controle, reduzir erros operacionais e aumentar a transparência entre usuários e gestão.",
  featured=[("dpFfXagJD4o3bU8u3H9I2oIgVo.png", "Capa do projeto IndexPonto", 2880, 2048), ("J6VNGDIL5jWhC9em6vGzuab1HsE.png", "Telas do IndexPonto", 1600, 1000)],
  summary="O IndexPonto é um sistema de ponto eletrônico desenvolvido para modernizar o controle de jornada de servidores públicos.",
  cover=("dpFfXagJD4o3bU8u3H9I2oIgVo.png", "Capa do projeto IndexPonto", 2880, 2048), sections=[
  ("Contexto", [("p", "A gestão de ponto, especialmente no setor público, ainda enfrenta os seguintes desafios estruturais:"), ("ul", ["Processos manuais e burocráticos", "Dificuldade no controle de horas, faltas e atrasos", "Baixa visibilidade para gestores", "Inconsistências em auditorias", "Falta de rastreabilidade dos dados"])]),
  ("Objetivo", [("ul", ["Digitalizar o controle de jornada;", "Reduzir erros operacionais;", "Acompanhar a carga horária dos funcionários;", "Aumentar a transparência entre usuários e gestão;", "Agilizar processos e análises de solicitações;", "Garantir conformidade com normas legais."])]),
  ("Processo de design", [("p", "O projeto foi criado com base na metodologia Double Diamond adaptada, devido à ausência de contato com usuários durante o desenvolvimento, concentrando validações nas etapas internas."), ("img", ["os8OZQgEcN2IzZKDUZN8UNrCpws.png"], "Diagrama do processo de design (Double Diamond adaptado)")]),
  ("Cronograma de projeto", [("p", "O cronograma exibe o planejamento e deadlines em que as etapas de design foram delimitadas, garantindo alinhamento com o time e previsibilidade no desenvolvimento."), ("img", ["qrva5yIVLnVq0oY3yKXX9afZWi4.png"], "Cronograma do projeto"), ("img", ["qzLlm2XlR4UKmQRJto6NinjxsY.png", "CLJ1HsIh1ozBxkzalUjdcUx6Fg.png"], "Detalhamento das etapas do cronograma")]),
  ("Direcionamentos de UX", [("p", "Decisões tomadas com base no entendimento das dores dos usuários, nas regras do sistema e na busca por uma experiência mais simples, clara e eficiente."), ("img", ["aQ0PKEnNFqD43vsNaaNczgFPO64.png"], "Direcionamento de UX do IndexPonto"), ("img", ["J6VNGDIL5jWhC9em6vGzuab1HsE.png"], "Telas do IndexPonto")])]),
]
SERVICES = [  # (arquivo-base, título, descrição)
 ("illustration", "Ilustração", "Criação de ilustrações autorais que comunicam ideias, traduzem conceitos e dão vida a narrativas visuais."),
 ("ui-ux", "UI/UX Design", "Criação de interfaces intuitivas e experiências digitais centradas nas necessidades das pessoas."),
 ("accessibility", "Acessibilidade", "Desenvolvimento de experiências mais inclusivas, considerando diferentes necessidades e formas de interação."),
 ("brand", "Identidade visual", "Construção de identidades visuais que traduzem a essência de marcas em sistemas gráficos consistentes e reconhecíveis."),
]
# Trajetória (página Sobre mim): condensado a partir das experiências já publicadas no portfólio. Ordem: mais recente primeiro. Exibida em "Sobre mim".
EXPERIENCE = [  # (empresa, cargo, período, descrição curta)
 ("IndexTech", "Web Designer Pleno", "(2025 - 2026)", "Criação de identidades visuais e interfaces web, com contribuições em design systems."),
 ("SmartRetail/IMD", "Product Designer Pleno", "(2021 - Atualmente)", "Times multidisciplinares, manutenção do design system e validação com usuários."),
 ("PROPESQ", "Web designer", "(2019 - 2020)", "Identidades visuais e diagramação de manuais para eventos científicos da UFRN."),
]
RECENT = [  # (arquivo da página, imagem provisória). Troque por projetos reais quando existirem.
 ("projeto-1", "placeholder-1.jpg"), ("projeto-2", "placeholder-2.jpg"), ("projeto-3", "placeholder-3.jpg"),
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

def head(title, desc, path, root, ld=None, noindex=False):
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    ldjson = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}/{path}">
<meta name="robots" content="{robots}">
<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}/{path}"><meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1F0E08">
<link rel="icon" type="image/png" sizes="64x64" href="{root}assets/favicon-dark.png" media="(prefers-color-scheme: light)">
<link rel="icon" type="image/png" sizes="64x64" href="{root}assets/favicon-light.png" media="(prefers-color-scheme: dark)">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap">
<script>document.documentElement.classList.add('js');if(window.scrollY<8)document.documentElement.classList.add('at-top');try{{if(localStorage.getItem('lang')==='en'){{document.documentElement.classList.add('i18n-pending');document.documentElement.lang='en';setTimeout(function(){{document.documentElement.classList.remove('i18n-pending')}},1500)}}}}catch(e){{}}</script>
<link rel="stylesheet" href="{root}css/styles.css">
<script src="{root}js/translations.js" defer></script>
<script src="{root}js/i18n.js" defer></script>
<script src="{root}js/site.js" defer></script>
{ldjson}
</head>"""

MENU_ICON = '<svg class="icon-menu" viewBox="0 0 20 20" aria-hidden="true" focusable="false"><path d="M3 5.5h14M3 10h14M3 14.5h14" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
LANG_SWITCH = ('<div class="lang" role="group" aria-label="Idioma">'
               '<button type="button" class="lang__btn" data-lang="pt-BR" lang="pt-BR" aria-pressed="true" aria-label="Português (Brasil)">PT</button>'
               '<button type="button" class="lang__btn" data-lang="en" lang="en" aria-pressed="false" aria-label="English">EN</button></div>')

def header(root, active):
    items = [("projetos.html", "Projetos", "projetos"), ("sobre-mim.html", "Sobre mim", "sobre"), ("contato.html", "Contato", "contato")]
    lis = "".join(f'<li><a href="{root}{h}"{" aria-current=\"page\"" if k == active else ""}>{t}</a></li>' for h, t, k in items)
    return f"""<a class="skip-link" href="#conteudo">Ir para o conteúdo</a>
<header class="site-header"><div class="container bar">
<a class="logo" href="{root}index.html"><img class="logo__dark" src="{root}assets/img/logo-marrom.png" width="295" height="160" alt="Luíza Araújo — página inicial"><img class="logo__light" src="{root}assets/img/logo-bege.png" width="295" height="160" alt="" aria-hidden="true"></a>
<nav id="menu" class="nav" aria-label="Principal"><ul>{lis}</ul></nav>
{LANG_SWITCH}
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">{MENU_ICON}<span>Menu</span></button>
</div></header>"""

def footer(root):
    return f"""<footer class="site-footer"><div class="container footer-grid">
<div class="footer-brand"><a class="footer-logo" href="{root}index.html"><img src="{root}assets/img/logo-bege.png" width="295" height="160" alt="Luíza Araújo — página inicial"></a><p class="footer-tagline">Studio de design</p></div>
<nav aria-label="Rodapé"><h2>Navegação</h2><ul><li><a href="{root}projetos.html">Projetos</a></li><li><a href="{root}sobre-mim.html">Sobre mim</a></li><li><a href="{root}contato.html">Contato</a></li></ul></nav>
<div><h2>Contato</h2><ul><li><a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">LinkedIn<span class="visually-hidden"> (abre em nova aba)</span></a></li><li><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">Instagram<span class="visually-hidden"> (abre em nova aba)</span></a></li><li><a href="{BEHANCE}" target="_blank" rel="noopener noreferrer">Behance<span class="visually-hidden"> (abre em nova aba)</span></a></li></ul></div>
</div></footer>"""

def cta(root):
    i = f"{root}assets/img/"
    return f"""<section class="cta section" aria-labelledby="cta-t">
<img class="cta__bg" src="{i}cta-leaves-1920.jpg" srcset="{i}cta-leaves-960.jpg 960w, {i}cta-leaves-1920.jpg 1920w" sizes="100vw" alt="" width="1920" height="667" loading="lazy" decoding="async">
<div class="container cta__inner">
<p class="cta__eyebrow">Fale comigo</p>
<h2 id="cta-t">Disponível para projetos, colaborações e oportunidades em design.</h2>
<p class="cta__desc">Entre em contato para conversarmos.</p>
<div class="cta__action"><a class="btn btn--light btn--compact" href="{root}contato.html">Vamos conversar!{ARROW}</a></div></div></section>"""

ARROW = '<svg class="icon-arrow" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M2 8h11M9 3.5 13.5 8 9 12.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def latest_section(root):
    """Seção "Projeto mais recente": usa o primeiro projeto da lista PROJECTS (campos intro e featured)."""
    p = PROJECTS[0]
    figs = "".join(f'<li><figure class="latest__card">{img(f, alt, w, h, root=root, sizes="(min-width: 48rem) 45vw, 100vw")}</figure></li>' for f, alt, w, h in p["featured"])
    return f"""<section class="latest" aria-labelledby="latest-t"><div class="container">
<div class="latest__intro"><h2 id="latest-t">Projeto mais recente</h2><p>{html.escape(p["intro"])}</p></div>
<ul class="latest__grid">{figs}</ul>
<div class="latest__action"><a class="link-arrow" href="{root}trabalhos/{p["slug"]}.html">Ver projeto{ARROW}</a></div>
</div></section>"""

def services_section(root, surface="light"):
    """Quatro áreas de atuação. surface="light" (fundo claro -> ícones escuros) ou "dark" (fundo escuro -> ícones claros).
    A troca das versões dos SVGs é feita por CSS a partir de data-surface; os arquivos originais não são modificados."""
    items = ""
    for slug, title, desc in SERVICES:
        base = f"assets/img/services/{slug}-{ICON_STYLE}"
        m = re.search(r'viewBox="0 0 (\d+) (\d+)"', open(f"{base}-dark.svg", encoding="utf-8").read())
        w, h = m.group(1), m.group(2)
        art = "".join(f'<img class="art-{tone}" src="{root}{base}-{tone}.svg" alt="" width="{w}" height="{h}" loading="lazy" decoding="async">' for tone in ("dark", "light"))
        items += f'<li class="service service--{slug}"><div class="service__art">{art}</div><h3 class="service__title">{title}</h3><p class="service__text">{desc}</p></li>'
    return f"""<section class="services" data-surface="{surface}" aria-labelledby="services-t"><div class="container">
<div class="services__intro"><h2 id="services-t">Quatro áreas do design em que atuo.</h2>
<p>Atuo em diferentes áreas do design, unindo criatividade, estratégia e funcionalidade para criar soluções e experiências.</p></div>
<ul class="services__grid">{items}</ul></div></section>"""


ARROW_UR = '<svg class="icon-arrow icon-arrow--ur" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M4 12 12 4M5.5 4H12v6.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def recent_section(root):
    """Últimos projetos: 3 cards (180x200) provisórios; cada um leva a uma página "em construção". Link final leva a outra página "em construção"."""
    cards = "".join(f'<li><a class="recent__card" href="{root}trabalhos/{slug}.html" aria-label="Projeto {n} — em construção">'
                    f'<img src="{root}assets/img/{ph}" alt="" width="360" height="400" loading="lazy" decoding="async"></a></li>'
                    for n, (slug, ph) in enumerate(RECENT, 1))
    return f"""<section class="recent" aria-labelledby="recent-t"><div class="container">
<div class="recent__intro"><h2 id="recent-t">Últimos projetos</h2>
<p>Uma seleção de projetos que refletem minha experiência, criatividade e diferentes formas de explorar o design.</p></div>
<ul class="recent__grid">{cards}</ul>
<div class="recent__action"><a class="link-arrow" href="{root}pagina-em-construcao.html">Ver todos os projetos{ARROW_UR}</a></div>
</div></section>"""

def construction_page(path, kind):
    """Página 404 personalizada ("em construção"), no padrão visual do site."""
    title = "Projeto em construção" if kind == "projeto" else "Página em construção"
    desc = ("Estou preparando este projeto para compartilhar com você. Volte em breve para conferir as novidades." if kind == "projeto"
            else "Estou preparando esta página para compartilhar com você. Volte em breve para conferir as novidades.")
    def body(r):
        i = f"{r}assets/img/"
        return f"""<section class="hero hero--404">
<img class="hero__bg" src="{i}hero-1920.jpg" srcset="{i}hero-960.jpg 960w, {i}hero-1920.jpg 1920w" sizes="100vw" alt="" width="1920" height="1080" fetchpriority="high" decoding="async">
<div class="hero__inner"><p class="error-code">404</p><h1>{title}</h1><p class="hero__lead">{desc}</p>
<div class="hero__cta"><a class="btn btn--light btn--compact" href="{r}index.html">Voltar para a página inicial{ARROW}</a></div></div></section>"""
    page(path, f"{title} — {NAME}", desc, body, noindex=True)

def experience_section(root):
    """Trajetória profissional: apresentação (esquerda) + linha do tempo vertical (direita). Dados em EXPERIENCE."""
    items = "".join(f'<li class="xp__item"><h3 class="xp__company">{html.escape(c)}</h3>'
                    f'<p class="xp__meta"><span>{html.escape(r)}</span><span>{html.escape(d)}</span></p>'
                    f'<p class="xp__text">{html.escape(t)}</p></li>' for c, r, d, t in EXPERIENCE)
    return f"""<section class="experience" aria-labelledby="xp-t"><div class="container">
<div class="experience__grid">
<div class="experience__intro"><h2 id="xp-t" class="experience__title">Minha trajetória através do design.</h2>
<p>Experiências que moldaram meu olhar criativo e ampliaram minha forma de pensar e desenvolver soluções em design.</p>
<a class="btn btn--outline btn--compact" href="{CV}" target="_blank" rel="noopener noreferrer">Visualizar currículo completo{ARROW}<span class="visually-hidden"> (abre em nova aba)</span></a></div>
<ol class="xp">{items}</ol></div>
</div></section>"""

def hero(root, title_html, lead=None, home=False):
    """Hero. Na home usa a fotografia (assets/img/hero-photo-*.jpg); nas demais, a textura. Textos vêm de quem chama."""
    if lead and home:   # na home, cada frase é um bloco: a quebra de linha acontece sempre depois do ponto
        lead = " ".join(f'<span class="s">{x}</span>' for x in re.split(r"(?<=[.!?])\s+", lead))
    p = f'<p class="hero__lead">{lead}</p>' if lead else ""
    cta = f'<div class="hero__cta"><a class="btn btn--light btn--compact" href="{root}contato.html">Vamos conversar{ARROW}</a></div>' if home else ""
    i = f"{root}assets/img/"
    if home:
        bg = (f'<picture><source media="(orientation: portrait)" srcset="{i}hero-photo-m.jpg">'
              f'<img class="hero__bg" src="{i}hero-photo-1920.jpg" srcset="{i}hero-photo-1920.jpg 1920w, {i}hero-photo-2560.jpg 2560w" sizes="100vw" alt="" width="2560" height="1440" fetchpriority="high" decoding="async"></picture>')
    else:
        bg = f'<img class="hero__bg" src="{i}hero-1920.jpg" srcset="{i}hero-960.jpg 960w, {i}hero-1920.jpg 1920w" sizes="100vw" alt="" width="1920" height="1080" fetchpriority="high" decoding="async">'
    return f"""<section class="hero{" hero--home hero--photo" if home else ""}">
{bg}
<div class="hero__inner"><h1>{title_html}</h1>{p}{cta}</div></section>"""

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

def page(path, title, desc, body, active="", ld=None, noindex=False):
    root = "../" * path.count("/")
    html_ = f"""{head(title, desc, path, root, ld, noindex)}
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
{hero(r, "<strong>Clareza como resultado</strong> de decisões bem projetadas.", "Cada detalhe tem um porquê. O essencial, sem ruído.", home=True)}
{latest_section(r)}
{services_section(r)}
{recent_section(r)}
{cta(r)}""", ld=ld)

    page("projetos.html", f"Projetos — {NAME}", "Projetos de produto com foco em usabilidade, eficiência e soluções para contextos complexos.", lambda r: f"""
{hero(r, "Projetos", "Projetos de produto com foco em usabilidade, eficiência e soluções para contextos complexos. Cada projeto apresenta como estruturo problemas, crio fluxos e evoluo soluções digitais.")}
<section class="section"><div class="container"><ul class="card-grid">{"".join(project_card(p, r) for p in PROJECTS)}</ul></div></section>
{cta(r)}""", active="projetos")

    def about(r):
        tools = "".join(f"<li><strong>{n}</strong><span>{d}</span></li>" for n, d in TOOLS)
        return f"""
{hero(r, "Sobre mim", "Busco impactar sistemas, transformando problemas complexos em designs funcionais e eficientes.")}
<section class="section"><div class="container about-grid"><div>
<dl class="facts"><div><dt>Experiência</dt><dd>5 anos</dd></div><div><dt>De onde sou</dt><dd>Parnamirim, RN</dd></div><div><dt>Atuação</dt><dd>Product designer</dd></div></dl>
<h2 class="section-title" style="font-size:var(--fs-h3);margin-bottom:.75rem">Motivação</h2>
<p class="statement"><strong>O Design transforma a maneira como vemos o mundo, e ao percebermos suas barreiras, enxergamos também como o Design pode transformá-lo.</strong> Busco descobrir soluções visuais que equilibram forma e propósito, em que cada detalhe tem intenção e a simplicidade se destaca.</p></div>
{img(PORTRAIT, "Foto de " + NAME, 1526, 1514, eager=True, root=r, sizes="(min-width: 56rem) 45vw, 100vw").replace('<img ', '<img class="about-photo" ')}
</div></section>
{experience_section(r)}
<section class="section" style="padding-top:0" aria-labelledby="tools-t"><div class="container"><h2 id="tools-t" class="section-title">Ferramentas</h2><ul class="tools">{tools}</ul></div></section>
{cta(r)}"""
    page("sobre-mim.html", f"Sobre mim — {NAME}", "Product designer com 5 anos de experiência, em Parnamirim, RN. Experiência, motivação e ferramentas.", about, active="sobre")

    def contact(r):
        def link(href, small, strong, ext=True):
            t = ' target="_blank" rel="noopener noreferrer"' if ext else ""
            return f'<a href="{href}"{t}><small>{small}</small><strong>{strong}</strong></a>'
        return f"""
{hero(r, "Vamos construir algo!", "Se você tem um desafio de produto ou quer trocar uma ideia, vamos conversar.")}
<section class="section"><div class="container contact-grid">
<div class="contact-links">{link("mailto:" + EMAIL, "E-mail", EMAIL, False)}{link(LINKEDIN, "LinkedIn", "Luíza de Araújo")}{link(INSTAGRAM, "Instagram", "@luizathearaujo.design")}{link(CV, "Currículo", "Clique e visualize")}</div>
<form id="contact-form" class="form" data-endpoint="{FORM_ENDPOINT}" data-fallback-email="{EMAIL}" method="post" action="{FORM_ENDPOINT or '#'}">
<div class="field"><label for="f-name">Nome</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
<div class="field"><label for="f-email">E-mail</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="f-subject">Assunto</label><input id="f-subject" name="subject" type="text" required></div>
<div class="field"><label for="f-message">Mensagem</label><textarea id="f-message" name="message" required></textarea></div>
<div class="hp" aria-hidden="true"><label>Não preencha<input name="_gotcha" type="text" tabindex="-1" autocomplete="off"></label></div>
<p id="form-status" class="form__status" role="status" aria-live="polite" data-i18n-skip></p>
<div><button class="btn" type="submit">Enviar mensagem</button></div>
</form></div></section>"""
    page("contato.html", f"Contato — {NAME}", "Se você tem um desafio de produto ou quer trocar uma ideia, vamos conversar.", contact, active="contato")

    for p in PROJECTS:
        def case(r, p=p):
            f, alt, w, h = p["cover"]
            others = "".join(project_row(o, r) for o in PROJECTS if o is not p)
            secs = "".join(f'<section class="case-section" aria-labelledby="s{i}"><h2 id="s{i}">{html.escape(t)}</h2><div class="case-section__body">{render_blocks(b, r)}</div></section>' for i, (t, b) in enumerate(p["sections"]))
            return f"""
<article>{hero(r, html.escape(p["title"]), html.escape(p["summary"]))}<div class="container">
<dl class="case-meta"><div><dt>Ano</dt><dd>{p["year"]}</dd></div><div><dt>Tempo</dt><dd>{p["time"]}</dd></div><div><dt>Ferramentas</dt><dd>{p["tools"]}</dd></div><div><dt>Área</dt><dd>{p["area"]}</dd></div></dl>
<figure class="case-cover">{img(f, alt, w, h, eager=True, root=r, sizes="100vw")}</figure>
{secs}
{('<div class="more-projects"><h2 class="section-title">Veja outros projetos</h2><ul class="project-list">' + others + '</ul></div>') if others else ""}
</div></article>
<div class="section"></div>{cta(r)}"""
        page(f"trabalhos/{p['slug']}.html", f"{p['title']} — {NAME}", p["summary"], case, active="projetos")

    for slug, _ in RECENT: construction_page(f"trabalhos/{slug}.html", "projeto")
    construction_page("pagina-em-construcao.html", "pagina")

    urls = ["index.html", "projetos.html", "sobre-mim.html", "contato.html"] + [f"trabalhos/{p['slug']}.html" for p in PROJECTS]
    open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")

class _Collector(HTMLParser):
    """Coleta todos os textos e atributos traduzíveis de uma página gerada."""
    def __init__(self):
        super().__init__(); self.out = set(); self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"): self.skip += 1
        d = dict(attrs)
        for a in ("alt", "aria-label", "placeholder", "title"):
            if d.get(a): self.out.add(re.sub(r"\s+", " ", d[a]).strip())
        if tag == "meta" and (d.get("name") == "description" or d.get("property") in ("og:title", "og:description")):
            self.out.add(re.sub(r"\s+", " ", d.get("content", "")).strip())
    def handle_endtag(self, tag):
        if tag in ("script", "style"): self.skip -= 1
    def handle_data(self, data):
        t = re.sub(r"\s+", " ", data).strip()
        if t and not self.skip: self.out.add(t)

def build_translations(pages):
    """Gera js/translations.js e avisa sobre textos sem tradução."""
    found = set()
    for p in pages:
        c = _Collector(); c.feed(open(p, encoding="utf-8").read()); found |= c.out
    needed = {t for t in found if re.search(r"[A-Za-zÀ-ÿ]", t) and t not in IDENTITY}
    missing = sorted(t for t in needed if t not in TR_EN)
    used = {k: v for k, v in TR_EN.items() if k in found}
    open("js/translations.js", "w", encoding="utf-8").write("/* GERADO por build.py a partir de i18n_en.py — não edite aqui. */\nwindow.I18N = " + json.dumps({"en": used, "ui": TR_UI}, ensure_ascii=False, indent=1) + ";\n")
    print(f"Traduções: {len(used)} textos em EN" + (f" | FALTAM {len(missing)}:" if missing else " | cobertura completa"))
    for m in missing: print("  -", m[:110])
    stale = sorted(k for k in TR_EN if k not in found)
    if stale: print(f"  (aviso: {len(stale)} chaves do dicionário não aparecem mais nas páginas)")

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
    import glob
    build_translations(sorted(glob.glob("*.html") + glob.glob("trabalhos/*.html")))
    print("Páginas geradas.")
