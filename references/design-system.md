# Design System — @medproflashcards

Sistema visual canônico dos posts de questão. Definido em produção no template `carrossel_usp2023/render_q03.py`.

## Canvas

| Formato | Dimensões | Uso |
|---------|-----------|-----|
| Post Instagram | 1080×1350 | Carrossel (até 10 slides) |
| Stories | 1080×1920 | Stories sequenciais |

**Stories safe zones**: o IG corta ~250-280px no topo (foto+nome) e ~330-380px no rodapé (reactions + DM). Trabalhe entre `y=280` e `y=1540`.

## Paleta

```python
PAPER       = (253, 253, 252)   # fundo papel claro
PAPER_DARK  = (240, 240, 238)   # variação mais escura
NAVY        = (13, 27, 42)      # texto principal, fundo escuro
DEEP_BLUE   = (27, 58, 92)      # variação navy
BRAND_BLUE  = (91, 164, 207)    # accent, labels, "cloze" em destaque
LIGHT_BLUE  = (135, 206, 235)   # accent claro, linhas em fundo navy
INK_DARK    = (26, 26, 26)      # body text
INK_MED     = (74, 74, 74)      # body text secundário
ANKI_BG     = (249, 249, 249)   # = #f9f9f9 (fundo CSS real dos cards Anki)
```

## Tipografia

| Fonte | Arquivo | Uso |
|-------|---------|-----|
| Playfair Display Bold (variable) | `fonts/PlayfairDisplay-Bold.ttf` | títulos, números, hooks |
| DM Sans (variable) | `fonts/DMSans-Regular.ttf` | labels, body, handle |
| Helvetica (sistema) | `/System/Library/Fonts/Helvetica.ttc` | apenas dentro dos cards Anki |

### Helpers padrão

```python
def FP(size, weight=900):
    """Playfair com peso variável (400-900)."""
    f = ImageFont.truetype(PLAYFAIR_VAR, size)
    try: f.set_variation_by_axes([weight])
    except: pass
    return f

def FS(size, weight=500, opsz=None):
    """DM Sans com opsz + weight (400-900)."""
    if opsz is None:
        opsz = max(9, min(40, size // 3))
    f = ImageFont.truetype(DMSANS_VAR, size)
    try: f.set_variation_by_axes([opsz, weight])
    except: pass
    return f
```

### Tamanhos típicos

| Elemento | Tamanho | Peso | Fonte |
|----------|---------|------|-------|
| Brand capa ("USP-SP") | 150-170 | 900 | Playfair |
| Ano | 96-120 | 900 | Playfair |
| Título slide ("O caso.") | 108-140 | 900 | Playfair |
| Subtítulo | 56-88 | 700-900 | Playfair |
| Label categoria | 26-32 | 800 | DM Sans |
| Body | 30-44 | 500-600 | Playfair ou DM Sans |
| Handle / footer | 22-26 | 700 | DM Sans |
| Hook (slide 3) | 80-100 | 900 | Playfair |

## Assets compartilhados

Todos vivem fora da skill, no Mac da Mariana:

```python
PAPER_SRC   = "/Users/marianarocha/Documents/Claude/MedPro Flashcards/Design/textura-de-papel-aquarela-ou-fundo-textura-sem-costura-pronto-para-o-azulejos_463999-10308.jpg-2.avif"
BUTTONS_SRC = "/Users/marianarocha/Documents/Claude/MedPro Flashcards/Design/Botões anki.jpg"
NEURON_SRC  = "/Users/marianarocha/Documents/Claude/MedPro Flashcards/Instagram/Posts antigos/questões/recriado/assets/neuron_outline.png"
```

- **Papel aquarela** (AVIF seamless): tiled como fundo do post, dá textura
- **Neurônio outline**: tintado em NAVY ou BRAND_BLUE, aplicado com alpha baixa (~10%) como ornamento decorativo no canto sup-dir e inf-esq
- **Botões Anki** (De novo / Difícil / Bom / Fácil): colados abaixo dos cards Anki nos slides centrais

## Layout / convenções

### Header (todo slide, com exceção da CTA navy)

```
M.  medpro          ← logo (Playfair "M." + DM Sans "medpro")
─────────────────   ← linha y=115
```

**SEM** tags tipo "• CATEGORIA", "R1 ACESSO DIRETO", "QUESTÃO 33". Foi removido de todos os templates por ser redundante.

### Footer

```
─────────────────   ← linha y=H-95
   @medproflashcards
```

**SEM** numeração de slide. Só handle centrado.

### Posicionamento

- Títulos no topo: `y=140-150`
- Body começa: `y=320-450` dependendo do slide
- Distribua o conteúdo preenchendo TODO o canvas — evite "espaço morto" abaixo do título
- Bullets / listas com bom espaçamento entre items (~`line_h * 1.6`)

## Ornamentos

```python
def paste_neuron(canvas, pos, size, rot=0, alpha=0.10, tint=NAVY):
    n = NEURON_OUTLINE.copy()
    n = tint_rgba(n, tint)
    n = n.resize(size, Image.LANCZOS)
    if rot: n = n.rotate(rot, expand=True, resample=Image.BICUBIC)
    n = set_alpha(n, alpha)
    rgba = canvas.convert("RGBA")
    rgba.alpha_composite(n, pos)
    return rgba.convert("RGB")

def bg_paper():
    img = PAPER_TEX.copy()
    img = paste_neuron(img, pos=(W - 400, -150), size=(700, 770), rot=-12, alpha=0.10, tint=NAVY)
    img = paste_neuron(img, pos=(-200, H - 500), size=(540, 590), rot=165, alpha=0.08, tint=NAVY)
    return img

def bg_navy():
    img = Image.new("RGB", (W, H), NAVY)
    img = paste_neuron(img, pos=(W - 450, -180), size=(750, 820), rot=-18, alpha=0.14, tint=BRAND_BLUE)
    img = paste_neuron(img, pos=(-180, H - 420), size=(500, 540), rot=150, alpha=0.10, tint=BRAND_BLUE)
    return img
```

## Cantos arredondados (cards / imagens)

```python
mask = Image.new("L", (sw, sh), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw, sh], radius=28, fill=255)
src_rgba = src_img.convert("RGBA")
src_rgba.putalpha(mask)
img_canvas.alpha_composite(src_rgba, (cx, cy))
```

Use radius=28-32 pra imagens, radius=18-24 pra pills/badges.

## Limitações conhecidas

- **Helvetica e Playfair NÃO suportam** caracteres `→` `↑` `←` `↓`. Substitua por `:` ou palavra ("aumenta", "leva a").
- **PIL thumbnail() só REDUZ** — não escala pra cima. Pra imagens pequenas em canvas grande, use `resize()` com cálculo de ratio.
- **AVIF** precisa de `pillow-heif` ou abertura especial. Geralmente a textura papel tá em `.avif` e PIL abre direto se estiver instalado.
