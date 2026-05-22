"""
Renderiza prints fiéis da UI do Anki usando o CSS da usuária:
  font: Helvetica · fundo #f9f9f9 · texto #000 · cloze #0000FF bold
  extra: #555 italic · text-align center · line-height 1.6em
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = "/Users/marianarocha/Documents/Claude/MedPro Flashcards/Instagram/Posts/carrossel_usp2023/anki_prints"
os.makedirs(OUT, exist_ok=True)

# Helvetica — .ttc com múltiplos weights; fallback pra Arial
FONT_REG    = "/System/Library/Fonts/Helvetica.ttc"
FONT_BOLD   = "/System/Library/Fonts/Helvetica.ttc"
FONT_ITALIC = "/System/Library/Fonts/Helvetica.ttc"

def F(size, style="regular"):
    idx = {"regular": 0, "bold": 1, "italic": 2}[style]
    try:
        return ImageFont.truetype(FONT_REG, size, index=idx)
    except Exception:
        arial = {"regular": "/System/Library/Fonts/Supplemental/Arial.ttf",
                 "bold":    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                 "italic":  "/System/Library/Fonts/Supplemental/Arial Italic.ttf"}[style]
        return ImageFont.truetype(arial, size)

# Paleta conforme CSS
BG_COLOR    = (249, 249, 249)   # #f9f9f9
TEXT_COLOR  = (0, 0, 0)         # #000000
CLOZE_COLOR = (0, 0, 255)       # #0000FF puro
EXTRA_COLOR = (85, 85, 85)      # #555555
HR_COLOR    = (220, 220, 220)

# Canvas — simulando container max-width 700px do CSS, render maior p/ qualidade
W, H = 1200, 1400

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

# Tipografia-alvo (escalada do CSS 18px/16px)
# Canvas 1200px ~ 1.7× um container 700px → 18px → ~44px
BASE_SIZE   = 46
EXTRA_SIZE  = 40

def draw_line_centered(d, parts, y, base_font_size, line_h):
    """parts = [(text, font, color), ...] renderiza em linha única centrada."""
    total_w = sum(d.textlength(t, font=f) for t, f, _ in parts)
    x = W // 2 - total_w // 2
    for text, font, color in parts:
        d.text((x, y), text, font=font, fill=color)
        x += d.textlength(text, font=font)

def render_jobert():
    img = Image.new("RGB", (W, H), BG_COLOR)
    d   = ImageDraw.Draw(img)

    max_w    = W - 120
    line_h   = int(BASE_SIZE * 1.6)

    # Pergunta: <b><u>Sinal de Jobert</u></b>?
    q_font_b = F(BASE_SIZE, "bold")
    q_font_r = F(BASE_SIZE, "regular")
    label    = "Sinal de Jobert"
    suffix   = "?"
    lw       = d.textlength(label, font=q_font_b)
    sw       = d.textlength(suffix, font=q_font_r)
    total    = lw + sw
    qy       = 160
    qx       = W // 2 - total // 2
    d.text((qx, qy), label, font=q_font_b, fill=TEXT_COLOR)
    d.text((qx + lw, qy), suffix, font=q_font_r, fill=TEXT_COLOR)
    # Underline só no 'Sinal de Jobert'
    ul_y = qy + BASE_SIZE + 6
    d.line([(qx, ul_y), (qx + lw, ul_y)], fill=TEXT_COLOR, width=3)

    # HR separador
    hr_y = qy + line_h + 50
    d.line([(60, hr_y), (W - 60, hr_y)], fill=HR_COLOR, width=1)

    # Resposta — cloze revelado (bold azul puro)
    a_font = F(BASE_SIZE, "bold")
    answer = "Perda da macicez hepática = pneumoperitôneo"
    ay     = hr_y + 70
    lines  = wrap(d, answer, a_font, max_w)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=a_font)
        d.text((W // 2 - tw // 2, ay + i * line_h), ln, font=a_font, fill=CLOZE_COLOR)

    # Extra / hint — #555 italic 16px
    extra_y = ay + len(lines) * line_h + 60
    extra_font = F(EXTRA_SIZE, "italic")
    extra = "Comum no abd perfurativo"
    tw = d.textlength(extra, font=extra_font)
    d.text((W // 2 - tw // 2, extra_y), extra, font=extra_font, fill=EXTRA_COLOR)

    img.save(f"{OUT}/anki_jobert.png", quality=95)
    print(f"Jobert: {img.size}")

def render_pneumo():
    img = Image.new("RGB", (W, H), BG_COLOR)
    d   = ImageDraw.Draw(img)

    max_w  = W - 120
    line_h = int(BASE_SIZE * 1.6)

    # Pergunta
    q_font = F(BASE_SIZE, "regular")
    q_text = "Diagnóstico?"
    tw = d.textlength(q_text, font=q_font)
    qy = 120
    d.text((W // 2 - tw // 2, qy), q_text, font=q_font, fill=TEXT_COLOR)

    # HR separador
    hr_y = qy + line_h + 20
    d.line([(60, hr_y), (W - 60, hr_y)], fill=HR_COLOR, width=1)

    # Resposta — cloze revelado (com acento)
    a_font = F(BASE_SIZE, "bold")
    ans    = "Pneumoperitônio"
    ay     = hr_y + 50
    tw = d.textlength(ans, font=a_font)
    d.text((W // 2 - tw // 2, ay), ans, font=a_font, fill=CLOZE_COLOR)

    # Imagem do pneumoperitoneo
    img_y = ay + line_h + 20
    pneumo = Image.open("/tmp/anki_preview/ea05_pneumoperit.png").convert("RGB")
    max_iw, max_ih = 880, 700
    ratio = min(max_iw / pneumo.width, max_ih / pneumo.height)
    new_size = (int(pneumo.width * ratio), int(pneumo.height * ratio))
    pneumo = pneumo.resize(new_size, Image.LANCZOS)
    img.paste(pneumo, (W // 2 - new_size[0] // 2, img_y))

    # Extra / hint
    extra_y = img_y + new_size[1] + 50
    extra_font = F(EXTRA_SIZE, "italic")
    extra = "Linha é o ligamento falciforme"
    tw = d.textlength(extra, font=extra_font)
    d.text((W // 2 - tw // 2, extra_y), extra, font=extra_font, fill=EXTRA_COLOR)

    img.save(f"{OUT}/anki_pneumo.png", quality=95)
    print(f"Pneumo: {img.size}")

def render_causas():
    """Card: Principais causas de abd perfurativo?"""
    img = Image.new("RGB", (W, H), BG_COLOR)
    d   = ImageDraw.Draw(img)

    max_w  = W - 120
    line_h = int(BASE_SIZE * 1.6)

    # Pergunta: "Principais causas de abdomen agudo perfurativo?"
    q_reg  = F(BASE_SIZE, "regular")
    q_bold = F(BASE_SIZE, "bold")
    prefix = "Principais causas de abdomen agudo "
    word   = "perfurativo"
    suffix = "?"
    pw = d.textlength(prefix, font=q_reg)
    ww = d.textlength(word,   font=q_bold)
    sw = d.textlength(suffix, font=q_reg)
    total = pw + ww + sw
    qy = 180
    # Se não couber em 1 linha, quebra antes do 'perfurativo'
    if total > W - 60:
        # Linha 1: "Principais causas de abdomen agudo"
        line1 = "Principais causas de abdomen agudo"
        l1w = d.textlength(line1, font=q_reg)
        d.text((W // 2 - l1w // 2, qy), line1, font=q_reg, fill=TEXT_COLOR)
        # Linha 2: "perfurativo?"
        qy2 = qy + line_h
        ww2 = d.textlength(word, font=q_bold)
        sw2 = d.textlength(suffix, font=q_reg)
        qx2 = W // 2 - (ww2 + sw2) // 2
        d.text((qx2, qy2), word, font=q_bold, fill=TEXT_COLOR)
        d.text((qx2 + ww2, qy2), suffix, font=q_reg, fill=TEXT_COLOR)
        ul_y = qy2 + BASE_SIZE + 6
        d.line([(qx2, ul_y), (qx2 + ww2, ul_y)], fill=TEXT_COLOR, width=3)
        qend = qy2
    else:
        qx = W // 2 - total // 2
        d.text((qx, qy), prefix, font=q_reg, fill=TEXT_COLOR)
        d.text((qx + pw, qy), word, font=q_bold, fill=TEXT_COLOR)
        d.text((qx + pw + ww, qy), suffix, font=q_reg, fill=TEXT_COLOR)
        ul_y = qy + BASE_SIZE + 6
        d.line([(qx + pw, ul_y), (qx + pw + ww, ul_y)], fill=TEXT_COLOR, width=3)
        qend = qy

    # HR separador
    hr_y = qend + line_h + 40
    d.line([(60, hr_y), (W - 60, hr_y)], fill=HR_COLOR, width=1)

    # Resposta — cloze revelado em azul bold
    a_font = F(BASE_SIZE, "bold")
    ans_lines = [
        "#1 Doença ulcerosa péptica",
        "Trauma",
    ]
    ay = hr_y + 70
    for i, ln in enumerate(ans_lines):
        tw = d.textlength(ln, font=a_font)
        d.text((W // 2 - tw // 2, ay + i * line_h), ln, font=a_font, fill=CLOZE_COLOR)

    img.save(f"{OUT}/anki_causas.png", quality=95)
    print(f"Causas: {img.size}")

render_jobert()
render_pneumo()
render_causas()
print(f"\ndone → {OUT}")
