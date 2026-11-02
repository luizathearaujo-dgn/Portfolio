"""
i18n_en.py — tradução central do site (PT-BR -> EN).

COMO FUNCIONA
- O site é escrito em português (idioma padrão, indexável pelo Google).
- Ao escolher "EN", js/i18n.js troca cada texto pelo equivalente deste dicionário, sem recarregar a página.
- A CHAVE é o texto em português exatamente como aparece na página (espaços repetidos são ignorados).
- Ao editar um texto em português no build.py, atualize a chave aqui. O build avisa se faltar alguma tradução.
- Depois de editar, rode:  python3 build.py
"""

# Textos que não mudam entre idiomas (nomes próprios, siglas, números). O build não cobra tradução deles.
IDENTITY = {
    "PT", "EN", "Menu", "LinkedIn", "Instagram", "E-mail", "UI/UX", "UI/UX Design", "Figma", "IndexPonto", "Product designer",
    "Parnamirim, RN", "Luíza de Araújo", "@luizathearaujo.design", "2019 — 2020", "Web designer", "Product design", "Web design",
    "Framer", "Maze", "Miro", "Hotjar", "Notion", "Jira", "Claude", "Adobe XD", "IndexTech", "SmartRetail/IMD", "PROPESQ",
    "Português (Brasil)", "English", "Luíza Araújo", "2025", "Luíza Araújo — Product Designer", "IndexPonto — Luíza Araújo",
    "2025 · UI/UX", "luizathearaujo@gmail.com",
}

# Mensagens geradas por JavaScript (formulário). {email} é substituído automaticamente.
UI = {
    "pt-BR": {
        "form.notConfigured": "O envio por este formulário ainda não foi ativado. Sua mensagem não foi enviada. Escreva diretamente para {email}.",
        "form.sending": "Enviando…",
        "form.success": "Mensagem enviada. Responderei assim que possível.",
        "form.error": "Não foi possível enviar a mensagem. Tente novamente ou escreva para {email}.",
        "form.required": "Preencha este campo.",
        "form.email": "Insira um endereço de e-mail válido.",
    },
    "en": {
        "form.notConfigured": "This form is not active yet. Your message was not sent. Please write directly to {email}.",
        "form.sending": "Sending…",
        "form.success": "Message sent. I will reply as soon as possible.",
        "form.error": "We couldn't send your message. Please try again or write to {email}.",
        "form.required": "Please fill out this field.",
        "form.email": "Please enter a valid email address.",
    },
}

EN = {
    # --- Navegação, acessibilidade e rodapé
    "Ir para o conteúdo": "Skip to content",
    "Principal": "Main", "Rodapé": "Footer", "Idioma": "Language",
    "Projetos": "Projects", "Sobre mim": "About me", "Contato": "Contact",
    "Navegação": "Navigation",
    "Studio de design": "Design studio",
    "(abre em nova aba)": "(opens in a new tab)",
    "Luíza Araújo — página inicial": "Luíza Araújo — home page",

    # --- Hero (home)
    "Clareza como resultado": "Clarity as the result",
    "de decisões bem projetadas.": "of well-designed decisions.",
    "Cada detalhe tem um porquê.": "Every detail has a reason.",
    "O essencial, sem ruído.": "The essentials, without the noise.",
    "Vamos conversar": "Let's talk",

    # --- Projeto mais recente
    "Projeto mais recente": "Latest project",
    "O IndexPonto é um sistema de ponto eletrônico desenvolvido para modernizar o controle de jornada de servidores públicos. O projeto busca digitalizar esse controle, reduzir erros operacionais e aumentar a transparência entre usuários e gestão.":
        "IndexPonto is an electronic time-tracking system designed to modernize working-hours control for public servants. The project aims to digitize this control, reduce operational errors and increase transparency between users and management.",
    "Ver projeto": "View project",
    "Capa do projeto IndexPonto": "IndexPonto project cover",
    "Telas do IndexPonto": "IndexPonto screens",

    # --- Serviços
    "Quatro áreas que se conectam através do design.": "Four areas connected through design.",
    "Diferentes perspectivas, um mesmo propósito: criar experiências visuais e digitais mais claras, funcionais e significativas.":
        "Different perspectives, one shared purpose: creating clearer, more functional and more meaningful visual and digital experiences.",
    "Ilustração": "Illustration",
    "Ideias que ganham forma através de traços, cores e composições visuais. Crio ilustrações que traduzem conceitos, comunicam mensagens e adicionam personalidade a projetos.":
        "Ideas that take shape through lines, colors and visual compositions. I create illustrations that translate concepts, communicate messages and add personality to projects.",
    "Experiências digitais pensadas para pessoas. Uno pesquisa, estratégia e design de interfaces para criar produtos intuitivos, funcionais e alinhados às necessidades dos usuários.":
        "Digital experiences designed for people. I combine research, strategy and interface design to create intuitive, functional products aligned with users' needs.",
    "Acessibilidade": "Accessibility",
    "Design que considera diferentes formas de perceber, compreender e interagir. Busco reduzir barreiras e tornar experiências digitais mais inclusivas e acessíveis.":
        "Design that considers different ways of perceiving, understanding and interacting. I work to reduce barriers and make digital experiences more inclusive and accessible.",
    "Identidade visual": "Visual identity",
    "Marcas com personalidade, propósito e consistência. Desenvolvo sistemas visuais que traduzem a essência de cada projeto e constroem conexões através da comunicação.":
        "Brands with personality, purpose and consistency. I develop visual systems that translate the essence of each project and build connections through communication.",

    # --- Chamada para contato
    "Fale comigo": "Get in touch",
    "Disponível para projetos, colaborações e oportunidades em design.": "Available for projects, collaborations and design opportunities.",
    "Entre em contato para conversarmos.": "Get in touch so we can talk.",
    "Vamos conversar!": "Let's talk!",

    # --- Página Projetos
    "Projetos de produto com foco em usabilidade, eficiência e soluções para contextos complexos. Cada projeto apresenta como estruturo problemas, crio fluxos e evoluo soluções digitais.":
        "Product projects focused on usability, efficiency and solutions for complex contexts. Each project shows how I structure problems, create flows and evolve digital solutions.",
    "Projetos de produto com foco em usabilidade, eficiência e soluções para contextos complexos.":
        "Product projects focused on usability, efficiency and solutions for complex contexts.",
    "O IndexPonto é um sistema de ponto eletrônico desenvolvido para modernizar o controle de jornada de servidores públicos.":
        "IndexPonto is an electronic time-tracking system designed to modernize working-hours control for public servants.",

    # --- Sobre mim
    "Busco impactar sistemas, transformando problemas complexos em designs funcionais e eficientes.":
        "I aim to make an impact on systems, turning complex problems into functional and efficient designs.",
    "Experiência": "Experience", "5 anos": "5 years", "De onde sou": "Where I'm from", "Atuação": "Focus",
    "Motivação": "Motivation",
    "O Design transforma a maneira como vemos o mundo, e ao percebermos suas barreiras, enxergamos também como o Design pode transformá-lo.":
        "Design changes the way we see the world, and by noticing its barriers, we also see how Design can transform it.",
    "Busco descobrir soluções visuais que equilibram forma e propósito, em que cada detalhe tem intenção e a simplicidade se destaca.":
        "I look for visual solutions that balance form and purpose, where every detail has intent and simplicity stands out.",
    "Experiência profissional": "Professional experience",
    "2025 — Atualmente": "2025 — Present", "2021 — Atualmente": "2021 — Present",
    "Web Designer Pleno": "Mid-level Web Designer", "Product Designer Pleno": "Mid-level Product Designer",
    "Atuo na criação de identidades visuais e interfaces web. Contribuo para design systems, promovendo padronização e escalabilidade dos produtos.":
        "I create visual identities and web interfaces. I contribute to design systems, promoting standardization and scalability across products.",
    "Colaboro com times multidisciplinares, realizo a manutenção do design system e a validação de soluções com usuários.":
        "I collaborate with multidisciplinary teams, maintain the design system and validate solutions with users.",
    "Construção de identidades visuais e diagramação de manuais para eventos científicos da UFRN.":
        "Creation of visual identities and layout of manuals for UFRN scientific events.",
    "Ferramentas": "Tools",
    "Testes de usabilidade": "Usability testing", "Jornadas e fluxos": "Journeys and flows", "Análise de dados": "Data analysis",
    "Documentação e organização": "Documentation and organization", "Organização e planejamento": "Organization and planning",
    "Ferramenta de apoio": "Support tool",
    "Foto de Luíza Araújo": "Photo of Luíza Araújo",

    # --- Contato
    "Vamos construir algo!": "Let's build something!",
    "Se você tem um desafio de produto ou quer trocar uma ideia, vamos conversar.": "If you have a product challenge or just want to exchange ideas, let's talk.",
    "Currículo": "Resume", "Clique e visualize": "Click to view",
    "Nome": "Name", "Assunto": "Subject", "Mensagem": "Message", "Enviar mensagem": "Send message",
    "Não preencha": "Leave this field empty",

    # --- Estudo de caso: IndexPonto
    "Ano": "Year", "Tempo": "Duration", "Área": "Area", "32 dias": "32 days",
    "Contexto": "Context",
    "A gestão de ponto, especialmente no setor público, ainda enfrenta os seguintes desafios estruturais:":
        "Time and attendance management, especially in the public sector, still faces the following structural challenges:",
    "Processos manuais e burocráticos": "Manual and bureaucratic processes",
    "Dificuldade no controle de horas, faltas e atrasos": "Difficulty tracking hours, absences and delays",
    "Baixa visibilidade para gestores": "Low visibility for managers",
    "Inconsistências em auditorias": "Inconsistencies in audits",
    "Falta de rastreabilidade dos dados": "Lack of data traceability",
    "Objetivo": "Goal",
    "Digitalizar o controle de jornada;": "Digitize working-hours control;",
    "Reduzir erros operacionais;": "Reduce operational errors;",
    "Acompanhar a carga horária dos funcionários;": "Track employees' working hours;",
    "Aumentar a transparência entre usuários e gestão;": "Increase transparency between users and management;",
    "Agilizar processos e análises de solicitações;": "Speed up request processing and review;",
    "Garantir conformidade com normas legais.": "Ensure compliance with legal regulations.",
    "Processo de design": "Design process",
    "O projeto foi criado com base na metodologia Double Diamond adaptada, devido à ausência de contato com usuários durante o desenvolvimento, concentrando validações nas etapas internas.":
        "The project was created using an adapted Double Diamond methodology, due to the lack of contact with users during development, concentrating validations in the internal stages.",
    "Diagrama do processo de design (Double Diamond adaptado)": "Design process diagram (adapted Double Diamond)",
    "Cronograma de projeto": "Project schedule",
    "O cronograma exibe o planejamento e deadlines em que as etapas de design foram delimitadas, garantindo alinhamento com o time e previsibilidade no desenvolvimento.":
        "The schedule shows the planning and deadlines that framed the design stages, ensuring alignment with the team and predictability in development.",
    "Cronograma do projeto": "Project schedule",
    "Detalhamento das etapas do cronograma": "Breakdown of the schedule stages",
    "Direcionamentos de UX": "UX guidelines",
    "Decisões tomadas com base no entendimento das dores dos usuários, nas regras do sistema e na busca por uma experiência mais simples, clara e eficiente.":
        "Decisions made based on understanding user pain points, the system's rules and the pursuit of a simpler, clearer and more efficient experience.",
    "Direcionamento de UX do IndexPonto": "IndexPonto UX guidelines",

    # --- Títulos e descrições das páginas (SEO)
    "Portfólio de Luíza Araújo, Product Designer: projetos de interface e UX com estética minimalista, agradável e simples de usar.":
        "Portfolio of Luíza Araújo, Product Designer: interface and UX projects with a minimalist, pleasant and easy-to-use aesthetic.",
    "Projetos — Luíza Araújo": "Projects — Luíza Araújo",
    "Sobre mim — Luíza Araújo": "About me — Luíza Araújo",
    "Contato — Luíza Araújo": "Contact — Luíza Araújo",
    "Product designer com 5 anos de experiência, em Parnamirim, RN. Experiência, motivação e ferramentas.":
        "Product designer with 5 years of experience, based in Parnamirim, RN. Experience, motivation and tools.",
}
