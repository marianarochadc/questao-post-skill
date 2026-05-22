"""
Stories UNIFESP 2026 Q33 — versão compacta em 6 telas 1080x1920.
Mesmo design system do post (paper, Playfair+DMSans, navy/brand).
Ordem:
  1 capa (pergunta + cultura)
  2 caso (compacto)
  3 germe (Pseudomonas MDR + cultura)
  4 ATB (pipe-tazo OU mero + infusão prolongada)
  5 manejo (3 passos principais)
  6 CTA
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE    = "/Users/marianarocha/Documents/Claude/MedPro Flashcards/Instagram/Posts/carrossel_unifesp2026_q33"
FONTS   = f"{BASE}/fonts"
NEURON  = "/Users/marianarocha/Documents/Claude/MedPro Flashcards/Instagram/Posts antigos/questões/recriado/assets"
OUT     = f"{BASE}/stories"
PAPER_SRC   = "/Users/marianarocha/Documents/Claude/MedPro Flashcards/Design/textura-de-papel-aquarela-ou-fundo-textura-sem-costura-pronto-para-o-azulejos_463999-10308.jpg-2.avif"
CULTURA_SRC = f"{BASE}/cultura_clean.png"
os.makedirs(OUT, exist_ok=True)

W, H   = 1080, 1920
PAPER       = (253, 253, 252)
INK_DARK    = (26, 26, 26)
INK_MED     = (74, 74, 74)
NAVY        = (13, 27, 42)
BRAND_BLUE  = (91, 164, 207)
LIGHT_BLUE  = (135, 206, 235)

PLAYFAIR_VAR = f"{FONTS}/PlayfairDisplay-Bold.ttf"
DMSANS_VAR   = f"{FONTS}/DMSans-Regular.ttf"

def FP(size, weight=900):
    f = ImageFont.truetype(PLAYFAIR_VAR, size)
    try: f.set_variation_by_axes([weight])
    except: pass
    return f

def FS(size, weight=500, opsz=None):
    if opsz is None:
        opsz = max(9, min(40, size // 3))
    f = ImageFont.truetype(DMSANS_VAR, size)
    try: f.set_variation_by_axes([opsz, weight])
    except: pass
    return f

def _paper():
    src = Image.open(PAPER_SRC).convert("RGB")
    tw, th = src.size
    canvas = Image.new("RGB", (W, H), (255, 255, 255))
    for y in range(0, H, th):
        for x in range(0, W, tw):
            canvas.paste(src, (x, y))
    return canvas

PAPER_TEX = _paper()
NEURON_OUTLINE = Image.open(f"{NEURON}/neuron_outline.png").convert("RGBA")

def tint_rgba(rgba, color):
    base = Image.new("RGBA", rgba.size, color + (0,))
    alpha = rgba.split()[-1]
    base.putalpha(alpha)
    return base

def set_alpha(rgba, factor):
    r, g, b, a = rgba.split()
    a = a.point(lambda v: int(v * factor))
    return Image.merge("RGBA", (r, g, b, a))

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
    img = paste_neuron(img, pos=(W - 420, -200), size=(780, 860), rot=-12, alpha=0.10, tint=NAVY)
    img = paste_neuron(img, pos=(-220, H - 600), size=(620, 680), rot=165, alpha=0.08, tint=NAVY)
    return img

def bg_navy():
    img = Image.new("RGB", (W, H), NAVY)
    img = paste_neuron(img, pos=(W - 450, -200), size=(830, 900), rot=-18, alpha=0.14, tint=BRAND_BLUE)
    img = paste_neuron(img, pos=(-200, H - 500), size=(580, 620), rot=150, alpha=0.10, tint=BRAND_BLUE)
    return img

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

# Safe zones de stories (Instagram corta ~250px topo, ~330px rodapé)
SAFE_TOP = 280
SAFE_BOT = H - 380  # 1540

def header(draw, dark=False):
    f_logo   = FP(52, 900)
    f_handle = FS(26, 700)
    lc = PAPER if dark else NAVY
    mc = LIGHT_BLUE if dark else INK_MED
    draw.text((60, SAFE_TOP - 130), "M.", font=f_logo, fill=lc)
    draw.text((130, SAFE_TOP - 110), "medpro", font=f_handle, fill=mc)
    line_c = LIGHT_BLUE if dark else (190, 183, 170)
    draw.line([(60, SAFE_TOP - 40), (W-60, SAFE_TOP - 40)], fill=line_c, width=1)

def footer_handle(draw, dark=False):
    lc = PAPER if dark else INK_MED
    line_c = LIGHT_BLUE if dark else (190, 183, 170)
    f_pg = FS(26, 700)
    draw.line([(60, SAFE_BOT + 40), (W-60, SAFE_BOT + 40)], fill=line_c, width=1)
    bbox = draw.textbbox((0, 0), "@medproflashcards", font=f_pg)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, SAFE_BOT + 70), "@medproflashcards", font=f_pg, fill=lc)

def rounded_image(img_rgba_canvas, src_img, x, y, w, h, radius=28, border=NAVY):
    """Cola src_img em (x,y) com cantos arredondados + frame. Escala up/down mantendo proporção."""
    iw, ih = src_img.size
    ratio = min(w / iw, h / ih)
    new_size = (int(iw * ratio), int(ih * ratio))
    src_img = src_img.resize(new_size, Image.LANCZOS)
    sw, sh = src_img.size
    cx = x + (w - sw) // 2
    cy = y + (h - sh) // 2

    # Frame
    frame = Image.new("RGBA", (sw + 6, sh + 6), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(frame)
    fdraw.rounded_rectangle([0, 0, sw + 6, sh + 6],
                            radius=radius + 3, outline=border, width=3)
    img_rgba_canvas.alpha_composite(frame, (cx - 3, cy - 3))

    # Máscara
    mask = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw, sh], radius=radius, fill=255)
    src_rgba = src_img.convert("RGBA")
    src_rgba.putalpha(mask)
    img_rgba_canvas.alpha_composite(src_rgba, (cx, cy))
    return img_rgba_canvas, cx, cy, sw, sh

# ============================================================
# STORY 1 — Capa
# ============================================================
def story_1():
    img = bg_paper()
    d   = ImageDraw.Draw(img)
    header(d)

    # Brand (1 linha)
    f_brand = FP(78, 900)
    d.text((40, SAFE_TOP), "UNIFESP-SP, ", font=f_brand, fill=NAVY)
    b1w = d.textbbox((0, 0), "UNIFESP-SP, ", font=f_brand)[2]
    d.text((40 + b1w, SAFE_TOP), "2026.", font=f_brand, fill=BRAND_BLUE)

    # Pergunta compacta
    f_q = FP(58, 900)
    d.text((40, SAFE_TOP + 100), "Abscesso pós-CCE?", font=f_q, fill=INK_DARK)

    # Label
    f_label = FS(26, 800)
    d.text((40, SAFE_TOP + 190), "CULTURA DO ASPIRADO", font=f_label, fill=BRAND_BLUE)

    cult = Image.open(CULTURA_SRC).convert("RGB")
    max_w = W - 60
    max_h = SAFE_BOT - (SAFE_TOP + 230) - 10
    rgba = img.convert("RGBA")
    rgba, cx, cy, cw, ch = rounded_image(rgba, cult, 30, SAFE_TOP + 230, max_w, max_h)
    img = rgba.convert("RGB")
    d = ImageDraw.Draw(img)

    footer_handle(d)
    img.save(f"{OUT}/story_1.png", quality=95)
    print("1 capa")

# ============================================================
# STORY 2 — Caso (compacto)
# ============================================================
def story_2():
    img = bg_paper()
    d   = ImageDraw.Draw(img)
    header(d)

    # Título
    f_t1 = FP(140, 900)
    d.text((60, SAFE_TOP), "O caso.", font=f_t1, fill=NAVY)

    # Caso em 4 blocos compactos
    f_head = FS(34, 800)
    f_body = FP(52, 600)
    blocks = [
        ("PACIENTE", "Homem, 56a. Internado há 10 dias."),
        ("HISTÓRIA", "CCE por colecistite + peritonite.\nDreno de Penrose desde então."),
        ("HOJE",     "Febre, calafrios, dor no dreno.\nTC: coleção subfrênica."),
        ("CULTURA",  "Drenagem percutânea: cultura positiva."),
    ]
    y = SAFE_TOP + 220
    for head_text, body_text in blocks:
        d.text((60, y), head_text, font=f_head, fill=BRAND_BLUE)
        yy = y + 54
        for line in body_text.split("\n"):
            lines = wrap(d, line, f_body, W - 120)
            for ln in lines:
                d.text((60, yy), ln, font=f_body, fill=INK_DARK)
                yy += 66
        y = yy + 28

    footer_handle(d)
    img.save(f"{OUT}/story_2.png", quality=95)
    print("2 caso")

# ============================================================
# STORY 3 — Germe (Pseudomonas MDR + cultura)
# ============================================================
def story_3():
    img = bg_paper()
    d   = ImageDraw.Draw(img)
    header(d)

    f_t1 = FP(120, 900)
    d.text((60, SAFE_TOP), "O germe.", font=f_t1, fill=NAVY)

    # Resposta destacada
    f_a1 = FP(78, 900)
    d.text((60, SAFE_TOP + 170), "Pseudomonas", font=f_a1, fill=INK_DARK)
    f_a2 = FP(78, 900)
    d.text((60, SAFE_TOP + 270), "aeruginosa", font=f_a2, fill=INK_DARK)
    f_tag = FP(100, 900)
    d.text((60, SAFE_TOP + 380), "MDR.", font=f_tag, fill=BRAND_BLUE)

    # Cultura abaixo
    cult = Image.open(CULTURA_SRC).convert("RGB")
    max_w = W - 120
    max_h = SAFE_BOT - (SAFE_TOP + 560) - 20
    rgba = img.convert("RGBA")
    rgba, cx, cy, cw, ch = rounded_image(rgba, cult, 60, SAFE_TOP + 560, max_w, max_h)
    img = rgba.convert("RGB")
    d = ImageDraw.Draw(img)

    footer_handle(d)
    img.save(f"{OUT}/story_3.png", quality=95)
    print("3 germe")

# ============================================================
# STORY 4 — ATB
# ============================================================
def story_4():
    img = bg_paper()
    d   = ImageDraw.Draw(img)
    header(d)

    f_t1 = FP(120, 900)
    d.text((60, SAFE_TOP), "A cobertura.", font=f_t1, fill=NAVY)

    f_sub = FS(36, 700)
    d.text((60, SAFE_TOP + 170), "EMPÍRICA, ANTI-PSEUDOMONAS", font=f_sub, fill=BRAND_BLUE)

    # Pill 1
    def pill(x, y, label, subtitle):
        f_lbl = FP(72, 900)
        f_sub = FS(30, 500)
        bbox = d.textbbox((0, 0), label, font=f_lbl)
        tw = bbox[2] - bbox[0]
        pad_x, pad_y = 40, 28
        pw = tw + pad_x*2
        ph = 110
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=18, fill=NAVY)
        d.text((x + pad_x, y + 18), label, font=f_lbl, fill=PAPER)
        # subtitle abaixo
        d.text((x, y + ph + 14), subtitle, font=f_sub, fill=INK_MED)

    pill(60, SAFE_TOP + 270, "Piperacilina-tazobactam", "4,5g EV 6/6h")
    pill(60, SAFE_TOP + 470, "OU Meropenem", "2g EV 8/8h")

    # Dica crítica
    d.line([(60, SAFE_TOP + 700), (W - 60, SAFE_TOP + 700)], fill=(190, 183, 170), width=1)

    f_crit_lbl = FS(30, 800)
    d.text((60, SAFE_TOP + 730), "O DETALHE QUE CAI NA PROVA", font=f_crit_lbl, fill=BRAND_BLUE)

    f_crit = FP(64, 900)
    d.text((60, SAFE_TOP + 790), "Infusão prolongada", font=f_crit, fill=NAVY)
    d.text((60, SAFE_TOP + 870), "(3–4h).", font=f_crit, fill=BRAND_BLUE)

    f_why = FS(30, 500)
    why = "Betalactâmico é tempo-dependente: aumenta T>CIM e permite tratar germe com CIM intermediário."
    lines = wrap(d, why, f_why, W - 120)
    yy = SAFE_TOP + 980
    for ln in lines:
        d.text((60, yy), ln, font=f_why, fill=INK_MED)
        yy += 42

    footer_handle(d)
    img.save(f"{OUT}/story_4.png", quality=95)
    print("4 ATB + infusão")

# ============================================================
# STORY 5 — Manejo (3 passos)
# ============================================================
def story_5():
    img = bg_paper()
    d   = ImageDraw.Draw(img)
    header(d)

    f_t1 = FP(140, 900)
    d.text((60, SAFE_TOP), "O manejo.", font=f_t1, fill=NAVY)

    items = [
        ("01", "DRENAR",  "O foco — percutânea guiada por imagem."),
        ("02", "CULTIVAR", "Orienta o ATB direcionado."),
        ("03", "ATB",     "Pipe-tazo ou meropenem em DOSE MÁXIMA e infusão prolongada."),
    ]
    f_num   = FP(110, 900)
    f_title = FS(48, 800)
    f_body  = FS(36, 500)
    y = SAFE_TOP + 240
    for num, title, txt in items:
        d.text((60, y), num, font=f_num, fill=BRAND_BLUE)
        d.text((240, y + 20), title, font=f_title, fill=NAVY)
        lines = wrap(d, txt, f_body, W - 240 - 60)
        yy = y + 95
        for ln in lines:
            d.text((240, yy), ln, font=f_body, fill=INK_DARK)
            yy += 46
        y = yy + 60

    footer_handle(d)
    img.save(f"{OUT}/story_5.png", quality=95)
    print("5 manejo")

# ============================================================
# STORY 6 — CTA
# ============================================================
def story_6():
    img = bg_navy()
    d   = ImageDraw.Draw(img)
    header(d, dark=True)

    f_tag = FS(32, 800)
    d.text((60, SAFE_TOP), "NÃO SE ARRISQUE NA PROVA.", font=f_tag, fill=BRAND_BLUE)

    f_t1 = FP(140, 900)
    d.text((60, SAFE_TOP + 80), "Salve.", font=f_t1, fill=PAPER)
    d.text((60, SAFE_TOP + 240), "Compartilha.", font=f_t1, fill=PAPER)
    d.text((60, SAFE_TOP + 400), "Revisa.", font=f_t1, fill=BRAND_BLUE)

    d.line([(60, SAFE_TOP + 600), (W - 60, SAFE_TOP + 600)], fill=LIGHT_BLUE, width=1)

    f_body = FS(36, 500)
    body = "Deck completo de flashcards UNIFESP no link da bio."
    lines = wrap(d, body, f_body, W - 120)
    yy = SAFE_TOP + 640
    for ln in lines:
        d.text((60, yy), ln, font=f_body, fill=(230, 230, 230))
        yy += 50

    f_handle = FP(78, 900)
    d.text((60, SAFE_TOP + 820), "@medproflashcards", font=f_handle, fill=PAPER)

    footer_handle(d, dark=True)
    img.save(f"{OUT}/story_6.png", quality=95)
    print("6 cta")

# RUN
story_1()
story_2()
story_3()
story_4()
story_5()
story_6()
print(f"\nsaída: {OUT}")
