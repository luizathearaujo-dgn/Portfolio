# Portfólio — Luíza Araújo

Site estático (HTML + CSS + JS puros). Sem framework, sem build obrigatório, publicável em qualquer hospedagem
(Netlify, Vercel, Cloudflare Pages, GitHub Pages, servidor próprio).

## Estrutura
- `index.html`, `projetos.html`, `sobre-mim.html`, `contato.html`, `trabalhos/*.html` — páginas geradas
- `build.py` — **fonte do conteúdo** (textos, projetos, links) e componentes (cabeçalho, rodapé, cards)
- `css/styles.css` — estilos; cores e fontes ficam nos **Tokens** (topo do arquivo)
- `js/site.js` — menu mobile e formulário
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
