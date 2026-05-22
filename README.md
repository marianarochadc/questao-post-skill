# questão-post

Claude Code skill pra gerar posts Instagram (carrossel + stories) a partir de questões de prova de residência médica. Feito pra workflow do @medproflashcards.

## O que faz

Pega uma questão (texto + imagens) e produz:
- **Carrossel Instagram** 1080×1350 (até 9 slides) com design system "papel + Playfair + neurônio"
- **Stories** 1080×1920 (5-6 stories opcionais) respeitando safe zones
- **Cards Anki** embutidos com CSS real (Helvetica + cloze azul)

## Instalação

```bash
git clone https://github.com/marianarochadc/questao-post-skill ~/.claude/skills/questão-post
```

Ou via Claude Code (plugin loader):
```
/plugin install marianarochadc/questao-post-skill
```

## Uso

Em qualquer conversa do Claude Code, digite:

```
/questão-post
```

ou frase natural tipo:

```
faz da Q33
transforma essa questão em carrossel
agora a stories da UNIFESP Q47
```

A skill assume o trabalho a partir daí.

## Estrutura

```
questão-post/
├── SKILL.md                           # instruções principais
├── README.md                          # esse arquivo
├── references/
│   ├── design-system.md               # paleta, fontes, layout
│   ├── slide-menu.md                  # 9 tipos de slide
│   ├── anki-cards.md                  # formato CSS Anki
│   └── stories-format.md              # safe zones, layout stories
├── assets/
│   ├── render_post_template.py        # renderer 9 slides
│   ├── render_stories_template.py     # renderer stories
│   └── render_anki_template.py        # renderer cards Anki
└── examples/
    └── README.md                      # exemplos de posts produzidos
```

## Dependências do sistema

A skill espera assets locais (fontes, texturas) nos paths do Mac da Mariana:
- `~/Documents/Claude/MedPro Flashcards/Design/` — texturas e botões Anki
- `~/Documents/Claude/MedPro Flashcards/Instagram/Posts antigos/questões/recriado/assets/` — neurônio
- Fontes Playfair Display + DM Sans (instaladas em `carrossel_usp2023/fonts/`)

Python:
- Pillow (PIL)
- PyMuPDF (fitz) — opcional, pra extrair imagens de PDFs

## Template original

Baseado no carrossel USP-SP 2023 Q03 (Abdome Agudo Perfurativo) — primeiro post completo do sistema.

## Licença

Uso pessoal — Mariana Rocha.
