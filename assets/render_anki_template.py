"""
Cards Anki para Q17 Einstein 2026 (abdome agudo perfurativo / úlcera perfurada).
3 cards:
  - anki_achado.png   — TC com pneumoperitônio
  - anki_causa.png    — etilismo agudo → úlcera perfurada
  - anki_extra.png    — Boerhaave como diagnóstico diferencial
"""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = "/Users/marianarocha/Documents/Claude/MedPro Flashcards/Instagram/Posts/carrossel_einstein2026_q17"
OUT  = f"{BASE}/anki_prints"
TC_SRC = f"{BASE}/tc_clean.png"
os.makedirs(OUT, exist_ok=True)

FONT_REG = "/System/Library/Fonts/Helvetica.ttc"

def F(size, style="regular"):
    idx = {"regular": 0, "bold": 1, "italic": 2}[style]
    try:
        return ImageFont.truetype(FONT_REG, size, index=idx)
    except Exception:
        arial = {"regular": "/System/Library/Fonts/Supplemental/Arial.ttf",
                 "bold":    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                 "italic":  "/System/Library/Fonts/Supplemental/Arial Italic.ttf"}[style]
        return ImageFont.truetype(arial, size)

BG_COLOR    = (249, 249, 249)
TEXT_COLOR  = (0, 0, 0)
CLOZE_COLOR = (0, 0, 255)
EXTRA_COLOR = (85, 85, 85)
HR_COLOR    = (220, 220, 220)

W, H = 1200, 1400
BASE_SIZE  = 46
EXTRA_SIZE = 40

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

# Card 1 — Achado de imagem (TC com pneumoperitônio)
def render_achado():
    img = Image.new("RGB", (W, H), BG_COLOR)
    d   = ImageDraw.Draw(img)
    line_h = int(BASE_SIZE * 1.6)

    q_reg = F(BASE_SIZE, "regular")
    line1 = "TC de abdome com ar livre"
    line2 = "subdiafragmático. Achado?"
    qy = 100
    tw = d.textlength(line1, font=q_reg)
    d.text((W//2 - tw//2, qy), line1, font=q_reg, fill=TEXT_COLOR)
    qy2 = qy + line_h
    tw = d.textlength(line2, font=q_reg)
    d.text((W//2 - tw//2, qy2), line2, font=q_reg, fill=TEXT_COLOR)

    hr_y = qy2 + line_h + 20
    d.line([(60, hr_y), (W-60, hr_y)], fill=HR_COLOR, width=1)

    a_font = F(BASE_SIZE, "bold")
    ans = "Pneumoperitônio"
    ay = hr_y + 50
    tw = d.textlength(ans, font=a_font)
    d.text((W//2 - tw//2, ay), ans, font=a_font, fill=CLOZE_COLOR)

    img_y = ay + line_h + 10
    tc = Image.open(TC_SRC).convert("RGB")
    max_iw, max_ih = 900, 580
    ratio = min(max_iw/tc.width, max_ih/tc.height)
    new_size = (int(tc.width*ratio), int(tc.height*ratio))
    tc = tc.resize(new_size, Image.LANCZOS)
    img.paste(tc, (W//2 - new_size[0]//2, img_y))

    extra_y = img_y + new_size[1] + 40
    extra_font = F(EXTRA_SIZE, "italic")
    extra = "Perfuração de víscera oca até prova em contrário"
    lines = wrap(d, extra, extra_font, W - 120)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=extra_font)
        d.text((W//2 - tw//2, extra_y + i*int(EXTRA_SIZE*1.4)), ln, font=extra_font, fill=EXTRA_COLOR)

    img.save(f"{OUT}/anki_achado.png", quality=95)
    print("achado")

# Card 2 — Causa (etilismo agudo)
def render_causa():
    img = Image.new("RGB", (W, H), BG_COLOR)
    d   = ImageDraw.Draw(img)
    max_w  = W - 120
    line_h = int(BASE_SIZE * 1.6)

    q_reg  = F(BASE_SIZE, "regular")
    q_bold = F(BASE_SIZE, "bold")

    qy = 180
    l1 = "Jovem, binge drinking,"
    tw = d.textlength(l1, font=q_reg)
    d.text((W//2 - tw//2, qy), l1, font=q_reg, fill=TEXT_COLOR)
    qy += line_h
    l2 = "dor epigástrica súbita."
    tw = d.textlength(l2, font=q_reg)
    d.text((W//2 - tw//2, qy), l2, font=q_reg, fill=TEXT_COLOR)
    qy += line_h

    pre = "Causa "
    bold_w = "mais provável"
    post = "?"
    pw = d.textlength(pre, font=q_reg)
    bw = d.textlength(bold_w, font=q_bold)
    sw = d.textlength(post, font=q_reg)
    total = pw + bw + sw
    qx = W//2 - total//2
    d.text((qx, qy), pre, font=q_reg, fill=TEXT_COLOR)
    d.text((qx+pw, qy), bold_w, font=q_bold, fill=TEXT_COLOR)
    d.text((qx+pw+bw, qy), post, font=q_reg, fill=TEXT_COLOR)
    ul_y = qy + BASE_SIZE + 6
    d.line([(qx+pw, ul_y), (qx+pw+bw, ul_y)], fill=TEXT_COLOR, width=3)

    hr_y = qy + line_h + 40
    d.line([(60, hr_y), (W-60, hr_y)], fill=HR_COLOR, width=1)

    a_font = F(BASE_SIZE, "bold")
    ans_lines = ["Úlcera péptica", "perfurada"]
    ay = hr_y + 80
    for i, ln in enumerate(ans_lines):
        tw = d.textlength(ln, font=a_font)
        d.text((W//2 - tw//2, ay + i*line_h), ln, font=a_font, fill=CLOZE_COLOR)

    extra_y = ay + len(ans_lines)*line_h + 60
    extra_font = F(EXTRA_SIZE, "italic")
    extra = "Álcool em altas doses lesa mucosa e inibe prostaglandinas protetoras"
    lines = wrap(d, extra, extra_font, max_w)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=extra_font)
        d.text((W//2 - tw//2, extra_y + i*int(EXTRA_SIZE*1.4)), ln, font=extra_font, fill=EXTRA_COLOR)

    img.save(f"{OUT}/anki_causa.png", quality=95)
    print("causa")

# Card 3 — EXTRA: Boerhaave (DDx)
def render_extra():
    img = Image.new("RGB", (W, H), BG_COLOR)
    d   = ImageDraw.Draw(img)
    max_w  = W - 120
    line_h = int(BASE_SIZE * 1.6)

    q_reg  = F(BASE_SIZE, "regular")
    q_bold = F(BASE_SIZE, "bold")

    qy = 180
    l1 = "Vômitos forçados, dor"
    tw = d.textlength(l1, font=q_reg)
    d.text((W//2 - tw//2, qy), l1, font=q_reg, fill=TEXT_COLOR)
    qy += line_h
    l2 = "torácica baixa, choque."
    tw = d.textlength(l2, font=q_reg)
    d.text((W//2 - tw//2, qy), l2, font=q_reg, fill=TEXT_COLOR)
    qy += line_h

    pre = "Pensar em "
    bold_w = "qual"
    post = " DDx?"
    pw = d.textlength(pre, font=q_reg)
    bw = d.textlength(bold_w, font=q_bold)
    sw = d.textlength(post, font=q_reg)
    total = pw + bw + sw
    qx = W//2 - total//2
    d.text((qx, qy), pre, font=q_reg, fill=TEXT_COLOR)
    d.text((qx+pw, qy), bold_w, font=q_bold, fill=TEXT_COLOR)
    d.text((qx+pw+bw, qy), post, font=q_reg, fill=TEXT_COLOR)
    ul_y = qy + BASE_SIZE + 6
    d.line([(qx+pw, ul_y), (qx+pw+bw, ul_y)], fill=TEXT_COLOR, width=3)

    hr_y = qy + line_h + 40
    d.line([(60, hr_y), (W-60, hr_y)], fill=HR_COLOR, width=1)

    a_font = F(BASE_SIZE, "bold")
    ans_lines = ["Síndrome de", "Boerhaave"]
    ay = hr_y + 80
    for i, ln in enumerate(ans_lines):
        tw = d.textlength(ln, font=a_font)
        d.text((W//2 - tw//2, ay + i*line_h), ln, font=a_font, fill=CLOZE_COLOR)

    extra_y = ay + len(ans_lines)*line_h + 60
    extra_font = F(EXTRA_SIZE, "italic")
    extra = "Ruptura esofágica espontânea por vômitos. Tríade de Mackler"
    lines = wrap(d, extra, extra_font, max_w)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=extra_font)
        d.text((W//2 - tw//2, extra_y + i*int(EXTRA_SIZE*1.4)), ln, font=extra_font, fill=EXTRA_COLOR)

    img.save(f"{OUT}/anki_extra.png", quality=95)
    print("extra")

render_achado()
render_causa()
render_extra()
print(f"\ndone → {OUT}")
