# Portfólio — Luíza Araújo

Site estático (HTML + CSS + JS puros). Sem framework, sem build obrigatório, publicável em qualquer hospedagem
(Netlify, Vercel, Cloudflare Pages, GitHub Pages, servidor próprio).

## Estrutura
- `index.html`, `projetos.html`, `sobre-mim.html`, `contato.html`, `trabalhos/*.html` — páginas geradas
- `build.py` — **fonte do conteúdo** (textos, projetos, links) e componentes (cabeçalho, rodapé, cards)
- `css/styles.css` — estilos; cores e fontes ficam nos **Tokens** (topo do arquivo)
- `js/site.js` — menu mobile, estado do cabeçalho e formulário
- `js/i18n.js` — troca de idioma PT-BR/EN (sem recarregar; preferência salva no localStorage)
- `js/translations.js` — GERADO pelo build a partir de `i18n_en.py` (não edite)
- `i18n_en.py` — **todas as traduções para inglês** (um único arquivo)
- `assets/img/services/` — ícones dos serviços (originais, claros e escuros; `filled` e `outlined`)
- `scripts/check_responsive.py` — teste de rolagem horizontal/menu/formulário (Playwright)

## Editar
1. Altere textos/projetos em `build.py` (seções CONFIG e CONTEÚDO) e rode `python3 build.py`.
2. Ou edite os `.html` diretamente (o build sobrescreve; escolha um dos dois caminhos).

## Antes de publicar (checklist)
1. `SITE` em `build.py`: troque `https://SEU-DOMINIO.com.br` pelo domínio real e rode `python3 build.py`.
2. **Imagens**: hoje vêm do CDN do Framer. Rode `python3 build.py --download` para copiá-las para `assets/img/`
   (necessário se o site Framer for desativado). Depois ajuste `width/height` reais em `PROJECTS` se quiser.
3. **Formulário**: crie um endpoint (Formspree, Web3Forms, Getform…) e cole a URL em `FORM_ENDPOINT` no `build.py`.
   Enquanto estiver vazio, o formulário avisa que NÃO enviou e indica o e-mail direto.
4. Imagem de compartilhamento (`OG_IMAGE`): idealmente 1200×630 hospedada no seu domínio.
5. Rode `python3 scripts/check_responsive.py` após qualquer mudança de layout.

## Idiomas (PT-BR / EN)
- Português é o padrão; o inglês é aplicado no navegador pelo botão PT | EN do cabeçalho.
- Ao alterar um texto em português no `build.py`, atualize a mesma frase em `i18n_en.py` e rode `python3 build.py`.
  O build lista qualquer texto que ainda estiver sem tradução.
- Observação de SEO: o Google indexa o conteúdo em português (HTML original); o inglês é aplicado por JavaScript.

## Ícones dos serviços
- Em `build.py`, `ICON_STYLE = "filled"` (silhueta) ou `"outlined"` (traço).
- A versão clara/escura troca sozinha pelo fundo da seção: `services_section(r, surface="light")` usa os ícones escuros;
  `surface="dark"` usa os claros.

## Favicon
- `assets/favicon-dark.png` (logo marrom) para abas claras e `assets/favicon-light.png` (logo bege) para abas escuras,
  selecionados por `prefers-color-scheme`. `favicon.ico` é o fallback para navegadores sem esse suporte.

## Trajetória profissional (página Sobre mim)
- Os dados ficam em `EXPERIENCE` no `build.py` (empresa, cargo, período, descrição curta), do mais recente para o mais antigo.
- O título usa a fonte serifada Cormorant Garamond (só nessa seção); o restante segue a Montserrat.
- Os links do currículo (`CV`) e do Behance (`BEHANCE`) ficam no topo do `build.py`.

## Últimos projetos (Home) e páginas "em construção"
- Os 3 cards usam imagens provisórias (`assets/img/placeholder-1..3.jpg`, recortes de ativos da marca). Dados em `RECENT` no `build.py`.
- Cada card abre `trabalhos/projeto-N.html` e "Ver todos os projetos" abre `pagina-em-construcao.html`: páginas 404 personalizadas
  (marcadas como `noindex` e fora do `sitemap.xml`).
- Quando houver projetos reais: crie o projeto em `PROJECTS`, aponte o card para ele em `RECENT` e troque a imagem provisória.
