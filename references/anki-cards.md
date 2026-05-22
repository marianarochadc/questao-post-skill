# Cards Anki — formato

Os "prints de cards Anki" que vão nos slides centrais reproduzem o CSS REAL que a Mariana usa no Anki dela. Isso dá identidade visual e familiaridade pra quem já usa Anki.

## CSS de referência (do Anki real)

```css
.card {
  font-family: Helvetica, Arial, sans-serif;
  background-color: #f9f9f9;
  color: #000;
  text-align: center;
  line-height: 1.6em;
}

.cloze {
  color: #0000FF;
  font-weight: bold;
}

.extra {
  color: #555;
  font-style: italic;
  font-size: smaller;
}
```

## Implementação PIL

```python
FONT_REG = "/System/Library/Fonts/Helvetica.ttc"

def F(size, style="regular"):
    idx = {"regular": 0, "bold": 1, "italic": 2}[style]
    try:
        return ImageFont.truetype(FONT_REG, size, index=idx)
    except Exception:
        # fallback Arial em outros sistemas
        arial = {
            "regular": "/System/Library/Fonts/Supplemental/Arial.ttf",
            "bold":    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "italic":  "/System/Library/Fonts/Supplemental/Arial Italic.ttf"
        }[style]
        return ImageFont.truetype(arial, size)

BG_COLOR    = (249, 249, 249)
TEXT_COLOR  = (0, 0, 0)
CLOZE_COLOR = (0, 0, 255)
EXTRA_COLOR = (85, 85, 85)
HR_COLOR    = (220, 220, 220)
```

## Estrutura visual do card

```
┌────────────────────────────┐
│                            │
│  Pergunta da questão       │  ← Helvetica regular, preto
│  em 1-2 linhas curtas?     │
│                            │
│  ──────────────────────    │  ← HR cinza
│                            │
│  RESPOSTA EM CLOZE         │  ← Helvetica bold, AZUL #0000FF
│                            │
│  [imagem opcional]         │
│                            │
│  Extra em italic cinza     │  ← Helvetica italic, #555
│                            │
└────────────────────────────┘
```

## Canvas

- `W, H = 1200, 1400` (boa resolução pra colar em slide 1080)
- `BASE_SIZE = 46`
- `EXTRA_SIZE = 40`

## Render típico (3 cards)

```python
def render_germe():
    # Pergunta → resposta cloze + imagem + extra
    ...

def render_conexao():
    # Pergunta → 2 linhas de cobertura + extra explicativo
    ...

def render_extra():
    # Pergunta → 2 linhas de pegadinha + extra
    ...
```

## Caracteres não suportados

Helvetica NÃO renderiza:
- `→` (seta direita)
- `↑` (seta cima)
- `←` `↓` (similares)
- alguns símbolos médicos especiais

**Substitua por**:
- `→` → `:` ou `=` ou palavra ("vira", "leva a")
- `↑` → "aumenta", "eleva"
- `↓` → "diminui", "reduz"

Exemplo:
- ❌ "Betalactâmicos = tempo-dependentes → ↑T>CIM"
- ✅ "Betalactâmicos são tempo-dependentes: aumenta T>CIM"

## Integração com os slides

No `render_q##.py`, a função `paste_anki_print()` faz:

1. **Autocrop** do print pelo bbox de conteúdo não-bg (pad=36)
2. Adiciona **botões Anki** abaixo (escala 90% da largura do card, fundo branco → ANKI_BG)
3. Aplica **máscara com cantos arredondados** (radius=32)
4. Adiciona **frame branco** ao redor
5. Aplica **sombra gaussiana** (blur=12, alpha=0.15)

Larguras típicas:
- Card com imagem (ex: pneumoperitônio, cultura): `target_w=680-800`
- Card só-texto: `target_w=780`
