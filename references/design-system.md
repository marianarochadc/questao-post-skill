# Design System — MedPro Flashcards (editorial premium)

Sistema visual alinhado à skill `/medpro-carrossel`. Inspiração: Bloomberg Businessweek, Osler, NYT Magazine, Granta. **Não é "infoproduto" — é editorial.**

## Canvas

| Formato | Dimensões | Uso |
|---------|-----------|-----|
| Post Instagram (3:4 orgânico) | **1080×1440** | Carrossel padrão |
| Stories | 1080×1920 | Stories sequenciais |
| Anúncio 4:5 | 1080×1350 | Só sob pedido |

**Stories safe zones**: y=280 até y=1540.

## Paleta (RESTRITA — sem desvios)

```python
NAVY        = (15, 35, 64)      # #0F2340 — escuro principal, fundo dominante
OFF         = (250, 250, 247)   # #FAFAF7 — off-white neutro
CREAM       = (239, 233, 217)   # #EFE9D9 — papel / fundo claro alternativo
RED         = (201, 53, 43)     # #C9352B — acento, USAR COM ESCASSEZ (pontuação)
GOLD        = (201, 169, 97)    # #C9A961 — tagline, destaques editoriais
BLACK       = (10, 10, 10)      # #0A0A0A — extremo escuro
CLOZE_BLUE  = (31, 0, 255)      # #1F00FF — cloze nos cards Anki
```

**NUNCA INVENTAR COR.** Se não tá nessa lista, não usa.

## Tipografia

| Fonte | Arquivo | Uso |
|-------|---------|-----|
| **Fraunces** (variable: opsz, wght, SOFT, WONK) | `assets/fonts/Fraunces[SOFT,WONK,opsz,wght].ttf` | Headlines, números editoriais. Weight 700-900. `SOFT=20-30` |
| **Inter** (variable: opsz, wght) | `assets/fonts/Inter[opsz,wght].ttf` | Corpo, labels, UI. Weight 400-700 |
| **Caveat** (variable: wght) | `assets/fonts/Caveat[wght].ttf` | Assinatura "Feito por aprovados". Weight 600 |
| **JetBrains Mono** (variable: wght) | `assets/fonts/JetBrainsMono[wght].ttf` | Eyebrows (`§ 02`), folio, contadores. Weight 400-500 |

### Helpers padrão (Python/PIL)

```python
FONTS = os.path.expanduser("~/.claude/skills/questão-post/assets/fonts")

def FF(size, weight=800, opsz=None, soft=30):
    """Fraunces (headlines). Axes order: opsz, wght, SOFT, WONK."""
    if opsz is None:
        opsz = max(9, min(144, size // 2))
    f = ImageFont.truetype(f"{FONTS}/Fraunces[SOFT,WONK,opsz,wght].ttf", size)
    try: f.set_variation_by_axes([opsz, weight, soft, 0])
    except: pass
    return f

def FI(size, weight=500, opsz=None):
    """Inter (corpo). Axes: opsz, wght."""
    if opsz is None:
        opsz = max(14, min(32, size // 2))
    f = ImageFont.truetype(f"{FONTS}/Inter[opsz,wght].ttf", size)
    try: f.set_variation_by_axes([opsz, weight])
    except: pass
    return f

def FC(size, weight=600):
    """Caveat (assinatura). Axes: wght."""
    f = ImageFont.truetype(f"{FONTS}/Caveat[wght].ttf", size)
    try: f.set_variation_by_axes([weight])
    except: pass
    return f

def FM(size, weight=500):
    """JetBrains Mono (eyebrows/folio). Axes: wght."""
    f = ImageFont.truetype(f"{FONTS}/JetBrainsMono[wght].ttf", size)
    try: f.set_variation_by_axes([weight])
    except: pass
    return f
```

### Tamanhos típicos (1080×1440)

| Elemento | Tamanho | Peso | Fonte |
|----------|---------|------|-------|
| Headline gigante (capa) | 180-260 | 900 | Fraunces |
| Headline médio (slide interno) | 110-150 | 800-900 | Fraunces |
| Subtítulo | 56-88 | 700 | Fraunces |
| Drop cap / numeral grande | 200-340 | 900 | Fraunces |
| Eyebrow (`§ 02 — TESE`) | 18-26 | 500 | JetBrains Mono CAIXA-ALTA tracking 0.32em |
| Body | 28-44 | 400-600 | Inter |
| Label / micro | 18-26 | 600-700 | Inter |
| Tagline "Feito por aprovados" | 80-120 | 600 | Caveat (rotação -2 a -3°) |
| Folio / contador | 14-20 | 500 | JetBrains Mono |
| Card Anki pergunta | 38-46 | 500-600 | Inter |
| Card Anki resposta | 44-52 | 700 | Inter — **AZUL CLOZE #1F00FF** |

## Assets compartilhados

Logos e textura ficam em `assets/brand/` da skill:

```python
SKILL_BRAND = os.path.expanduser("~/.claude/skills/questão-post/assets/brand")
LOGO_CREAM  = f"{SKILL_BRAND}/logo-cream.png"   # sobre navy
LOGO_NAVY   = f"{SKILL_BRAND}/logo-navy.png"    # sobre cream/off
PAPER_TEX   = f"{SKILL_BRAND}/paper.png"        # textura editorial
```

**Logo aparece SÓ na capa (slide 1) e no slide final (CTA).** Lâminas do meio NÃO carregam logo.

## Textura de papel

- Aplicar em fundos sólidos com **blend modes**:
  - Fundos claros (cream/off): `multiply` (subtrai luz)
  - Fundos escuros (navy/black): `soft-light` (mantém luz mas dá grão)
- Em PIL não tem soft-light nativo, mas dá pra simular:

```python
def apply_paper(canvas, paper_path, dark=False, opacity=0.4):
    paper = Image.open(paper_path).convert("RGBA")
    paper = paper.resize(canvas.size, Image.LANCZOS)
    if dark:
        # soft-light fake: blend overlay com opacidade baixa
        return Image.blend(canvas.convert("RGB"),
                           Image.alpha_composite(canvas.convert("RGBA"), 
                                                  Image.eval(paper, lambda v: int(v*0.4))).convert("RGB"),
                           opacity*0.5)
    else:
        # multiply
        p = paper.convert("RGB")
        c = canvas.convert("RGB")
        from PIL import ImageChops
        return ImageChops.multiply(c, Image.eval(p, lambda v: int(v*0.6 + 255*0.4)))
```

## Regras editoriais (SEM EXCEÇÃO)

### REGRAS DURAS — nunca quebrar

1. **NUNCA usar eyebrow.** Proibido: `§ NN — TÍTULO`, bolinha vermelha + texto kicker, "QUESTÃO 17" em letterspacing wide no topo, etc. O header com logo + handle já assina visualmente.
2. **Header padronizado em TODOS os slides**: logo MedPro grande à esquerda (y=70, altura 140px) + `@MedProFlashcards` em JetBrains Mono 48px weight 600 à direita, centralizado verticalmente com o logo. **SEM linha divisória.**
3. **Capitalização do handle**: sempre `@MedProFlashcards` em CamelCase. Não usar lowercase nem all caps.
4. **Sem labels A/B/C/D** sobre imagens sequenciais. Apenas quando a questão pede comparação explícita.
5. **JetBrains Mono** é permitida em: (a) handle do header em todos slides; (b) folio `PADRÃO MEDPRO / DIRETO AO PONTO` no rodapé dos cards Anki; (c) badge `FLASHCARD MEDPRO` no card interno dos slides Anki. Em qualquer outro lugar usar Inter.

### Convenções editoriais

5. **Pontuação como ornamento**: ponto final / interrogação em `RED`, peso 900. Tamanho desproporcional permitido.
6. **Headlines em Fraunces 800-900**, leading apertado (0.86-0.92), tracking negativo (-0.035 a -0.045em).
7. **Capa**: BANCA + ANO em Fraunces 900 ~190-200px (maior que tudo), pergunta menor (Fraunces 700, ~56-60px).
8. **Citações**: aspas tipográficas `"` em tamanho monumental (300px+) em `RED`.
9. **Drop cap**: primeira letra em Fraunces 900 + `RED` no parágrafo de abertura.
10. **Assinatura Caveat**: rotação leve (-2 a -4°) em `GOLD` ou `RED`. **Só na CTA** ("Feito por aprovados.") — NÃO duplicar na capa pra não competir com o header.
11. **Sem emoji, sem ícones decorativos.** O neurônio (logo) é o único símbolo.
12. **Sem cantos arredondados** em imagens (ou raio máximo 4px).
13. **Imagens com `aspect-ratio: cover`**, sem máscaras suaves.

## Render de cards Anki

Cards Anki são **deliberadamente raw** — parecem screenshot do app, não diagramação editorial:

- **Fundo**: branco `#FFFFFF` ou off `#FAFAF7`. SEM paper texture, SEM ornamento, SEM logo.
- **Pergunta**: Inter weight 500-600, preto `#0A0A0A`, centralizada.
- **Resposta**: Inter weight 700, **AZUL CLOZE `#1F00FF`**, centralizada abaixo da pergunta.
- **Sublinhado**: UMA palavra-chave da resposta sublinhada (a mais importante semanticamente). Se o card original já tem sublinhado, mantém o original.
- **Polimento permitido** (sem alterar fato médico): capitalização, acentuação, pontuação, frase completa. Remover `&nbsp;`, `{{c1::…}}`.

Detalhes completos em [anki-cards.md](anki-cards.md).

## CTA final (slide N)

- Fundo NAVY
- Eyebrow JetBrains Mono em GOLD: `§ — MEDPROFLASHCARDS`
- Tagline em Caveat: **"Feito por aprovados."** em `RED` (`#C9352B`), rotação -2°
- Stats: `+19k flashcards · +700 aprovados · link na bio` em Inter 500
- Link: `medproflashcards.com.br/links`

## Combos cromáticos por slide

| Slide | Fundo | Texto | Acento |
|-------|-------|-------|--------|
| Capa | CREAM ou NAVY | NAVY ou OFF | RED/GOLD na pontuação |
| Caso | OFF | NAVY | GOLD nos labels |
| Hook | NAVY | OFF | GOLD ou RED no destaque |
| Anki card | OFF (branco) | BLACK | CLOZE_BLUE na resposta |
| Diagnóstico | OFF | NAVY | RED na pontuação grande |
| Manejo | OFF | NAVY | GOLD nos números (01, 02, 03) |
| CTA | NAVY | OFF | GOLD eyebrow + RED tagline Caveat |

## Limitações conhecidas

- Fraunces/Inter/Caveat/JetBrains Mono são **fontes baixadas** — vivem em `~/.claude/skills/questão-post/assets/fonts/`.
- Não há ícone setinha `→` na maioria delas — substitua por `:` ou palavra ("aumenta", "leva a").
- Para escalar imagens pra cima (não só reduzir), use `resize()` com cálculo de ratio, não `thumbnail()`.
