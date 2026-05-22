"""
Carrossel Q03 USP-SP 2023 — v5
Estrutura (9 slides, nova ordem):
  1 capa
  2 caso clínico
  3 hook
  4 Anki: Pneumoperitônio (com imagem)
  5 Anki: Principais causas de abd perfurativo
  6 EXTRA — Anki: Sinal de Jobert
  7 diagnóstico
  8 manejo
  9 CTA
"""

import os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

BASE    = "/Users/marianarocha/Documents/Claude/MedPro Flashcards/Instagram/Posts/carrossel_usp2023"
CROPS   = "/Users/marianarocha/Documents/Claude/MedPro Flashcards/Instagram/Posts/prova_original_usp/imagens_crops"
FONTS   = f"{BASE}/fonts"
NEURON  = "/Users/marianarocha/Documents/Claude/MedPro Flashcards/Instagram/Posts antigos/questões/recriado/assets"
ANKI    = f"{BASE}/anki_prints"
OUT     = f"{BASE}/q03_abdome_perfurativo"
PAPER_SRC = "/Users/marianarocha/Documents/Claude/MedPro Flashcards/Design/textura-de-papel-aquarela-ou-fundo-textura-sem-costura-pronto-para-o-azulejos_463999-10308.jpg-2.avif"
BUTTONS_SRC = "/Users/marianarocha/Documents/Claude/MedPro Flashcards/Design/Botões anki.jpg"
ANKI_BG = (249, 249, 249)
os.makedirs(OUT, exist_ok=True)

W, H   = 1080, 1350
PAPER       = (253, 253, 252)
PAPER_DARK  = (240, 240, 238)
CARD_WHITE  = (252, 251, 248)
INK_DARK    = (26, 26, 26)
INK_MED     = (74, 74, 74)
NAVY        = (13, 27, 42)
DEEP_BLUE   = (27, 58, 92)
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

# --- PAPER TEXTURE — carrega AVIF seamless e tila em 1080x1350 ---
def _paper():
    src = Image.open(PAPER_SRC).convert("RGB")
    tw, th = src.size
    canvas = Image.new("RGB", (W, H), (255, 255, 255))
    for y in range(0, H, th):
        for x in range(0, W, tw):
            canvas.paste(src, (x, y))
    return canvas

PAPER_TEX = _paper()

# --- NEURON ---
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
    img = paste_neuron(img, pos=(W - 400, -150), size=(700, 770), rot=-12, alpha=0.10, tint=NAVY)
    img = paste_neuron(img, pos=(-200, H - 500), size=(540, 590), rot=165, alpha=0.08, tint=NAVY)
    return img

def bg_navy():
    img = Image.new("RGB", (W, H), NAVY)
    img = paste_neuron(img, pos=(W - 450, -180), size=(750, 820), rot=-18, alpha=0.14, tint=BRAND_BLUE)
    img = paste_neuron(img, pos=(-180, H - 420), size=(500, 540), rot=150, alpha=0.10, tint=BRAND_BLUE)
    return img

# --- HELPERS ---
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

def header(draw, dark=False):
    f_logo   = FP(42, 900)
    f_handle = FS(22, 700)
    lc = PAPER if dark else NAVY
    mc = LIGHT_BLUE if dark else INK_MED
    draw.text((50, 50), "M.", font=f_logo, fill=lc)
    draw.text((108, 66), "medpro", font=f_handle, fill=mc)
    line_c = LIGHT_BLUE if dark else (190, 183, 170)
    draw.line([(50, 115), (W-50, 115)], fill=line_c, width=1)

def footer_handle(draw, dark=False):
    """Apenas handle, sem paginação."""
    lc = PAPER if dark else INK_MED
    line_c = LIGHT_BLUE if dark else (190, 183, 170)
    f_pg = FS(22, 700)
    draw.line([(50, H-95), (W-50, H-95)], fill=line_c, width=1)
    bbox = draw.textbbox((0, 0), "@medproflashcards", font=f_pg)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H-75), "@medproflashcards", font=f_pg, fill=lc)

# ============================================================
# SLIDE 1 — Capa: texto compacto no topo, imagens gigantes
# ============================================================
def slide_capa():
    img = bg_paper()
    d   = ImageDraw.Draw(img)
    header(d)

    # Headline mais compacto, mantido no topo
    f_brand = FP(170, 900)
    d.text((42, 145), "USP-SP", font=f_brand, fill=NAVY)
    f_year = FP(96, 900)
    d.text((W - 280, 165), "2023.", font=f_year, fill=BRAND_BLUE)

    # Pergunta hook
    f_q1 = FP(52, 900)
    d.text((50, 320), "Abdome agudo,", font=f_q1, fill=NAVY)
    f_q2 = FP(48, 700)
    d.text((50, 385), "qual é a causa?", font=f_q2, fill=INK_DARK)

    # Fio
    d.line([(50, 470), (W-50, 470)], fill=NAVY, width=3)

    # GRID GIGANTE — ocupando bastante do slide
    gy = 510
    cell_w = (W - 100 - 20) // 2   # 480
    cell_h = 340
    radius_ct = 24
    labels = [("A", "q03_A_axial.png"), ("B", "q03_B_axial.png"),
              ("C", "q03_C_axial.png"), ("D", "q03_D_axial.png")]
    for i, (lbl, fn) in enumerate(labels):
        row, col = i // 2, i % 2
        x = 50 + col * (cell_w + 20)
        y = gy + row * (cell_h + 20)
        # Frame arredondado navy
        rgba = img.convert("RGBA")
        frame = Image.new("RGBA", (cell_w + 6, cell_h + 6), (0, 0, 0, 0))
        fdraw = ImageDraw.Draw(frame)
        fdraw.rounded_rectangle([0, 0, cell_w + 6, cell_h + 6],
                                radius=radius_ct + 3, outline=NAVY, width=3)
        rgba.alpha_composite(frame, (x - 3, y - 3))
        img = rgba.convert("RGB")
        d = ImageDraw.Draw(img)

        # Carrega imagem, centraliza, aplica máscara arredondada
        ct = Image.open(f"{CROPS}/{fn}").convert("RGB")
        ct.thumbnail((cell_w, cell_h), Image.LANCZOS)
        cw_i, ch_i = ct.size
        cx_i = x + (cell_w - cw_i) // 2
        cy_i = y + (cell_h - ch_i) // 2
        # Canvas branco do tamanho da célula com CT centralizada
        cell = Image.new("RGB", (cell_w, cell_h), (255, 255, 255))
        cell.paste(ct, ((cell_w - cw_i)//2, (cell_h - ch_i)//2))
        mask = Image.new("L", (cell_w, cell_h), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, cell_w, cell_h],
                                               radius=radius_ct, fill=255)
        cell_rgba = cell.convert("RGBA")
        cell_rgba.putalpha(mask)
        rgba = img.convert("RGBA")
        rgba.alpha_composite(cell_rgba, (x, y))
        img = rgba.convert("RGB")
        d = ImageDraw.Draw(img)

        # Label navy no canto sup-esq (também arredondado pra combinar)
        badge = Image.new("RGBA", (72, 72), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(badge)
        bdraw.rounded_rectangle([0, 0, 72, 72],
                                radius=radius_ct, fill=NAVY + (255,))
        rgba = img.convert("RGBA")
        rgba.alpha_composite(badge, (x, y))
        img = rgba.convert("RGB")
        d = ImageDraw.Draw(img)
        f_lbl = FP(52, 900)
        bb = d.textbbox((0, 0), lbl, font=f_lbl)
        tw2, th2 = bb[2]-bb[0], bb[3]-bb[1]
        d.text((x + (72-tw2)//2, y + (72-th2)//2 - 10), lbl, font=f_lbl, fill=PAPER)

    # Redraw em cima de tudo
    d = ImageDraw.Draw(img)
    footer_handle(d)
    img.save(f"{OUT}/slide_1.png", quality=95)

# ============================================================
# SLIDE 3 — Hook dramático
# ============================================================
def slide_hook():
    img = bg_navy()
    d   = ImageDraw.Draw(img)
    header(d, dark=True)

    f_big = FP(200, 900)
    d.text((42, 320), "Saberia", font=f_big, fill=PAPER)
    d.text((42, 520), "responder", font=f_big, fill=PAPER)

    f_tail = FP(150, 900)
    d.text((42, 740), "agora?", font=f_tail, fill=BRAND_BLUE)

    footer_handle(d, dark=True)
    img.save(f"{OUT}/slide_3.png", quality=95)

# ============================================================
# SLIDE 2 — Caso clínico
# ============================================================
def slide_caso():
    img = bg_paper()
    d   = ImageDraw.Draw(img)
    header(d)

    f_t1 = FP(130, 900)
    d.text((42, 145), "O caso,", font=f_t1, fill=NAVY)
    f_t2 = FP(88, 700)
    d.text((48, 300), "em detalhes.", font=f_t2, fill=INK_DARK)

    f_head = FS(32, 800)
    f_body = FP(44, 600)
    blocks = [
        ("PACIENTE",   "Mulher, 63 anos."),
        ("HISTÓRIA",   "Artrite reumatoide em uso de AINE + corticoide."),
        ("QUADRO",     "Dor súbita, difusa, forte — há 2h."),
        ("EXAME",      "FC 110 · PA 100×60 · DB+ peritonite difusa."),
        ("LAB",        "Leuco 18.318 · PCR 84 · amilase e lipase normais."),
    ]
    y = 460
    for head_text, body_text in blocks:
        d.text((50, y), head_text, font=f_head, fill=BRAND_BLUE)
        lines = wrap(d, body_text, f_body, W - 100)
        yy = y + 50
        for ln in lines:
            d.text((50, yy), ln, font=f_body, fill=INK_DARK)
            yy += 56
        y = yy + 24

    footer_handle(d)
    img.save(f"{OUT}/slide_2.png", quality=95)

# ============================================================
# SLIDE 7 — Diagnóstico (confirma com imagem USP)
# ============================================================
def slide_dx():
    img = bg_paper()
    d   = ImageDraw.Draw(img)
    header(d)

    f_t1 = FP(118, 900)
    d.text((42, 150), "Pneumoperitônio.", font=f_t1, fill=NAVY)
    f_t2 = FP(68, 700)
    d.text((48, 295), "víscera perfurada.", font=f_t2, fill=INK_DARK)

    # Imagem grande — coluna esquerda
    ca = Image.open(f"{CROPS}/q03_A_full.png").convert("RGB")
    cell_w, cell_h = 520, 760
    ca.thumbnail((cell_w, cell_h), Image.LANCZOS)
    x = 50
    y = 440
    radius_dx = 28
    cw_i, ch_i = ca.width, ca.height

    rgba = img.convert("RGBA")
    frame = Image.new("RGBA", (cw_i + 6, ch_i + 6), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(frame)
    fdraw.rounded_rectangle([0, 0, cw_i + 6, ch_i + 6],
                            radius=radius_dx + 3, outline=NAVY, width=3)
    rgba.alpha_composite(frame, (x - 3, y - 3))

    mask = Image.new("L", (cw_i, ch_i), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, cw_i, ch_i],
                                           radius=radius_dx, fill=255)
    ca_rgba = ca.convert("RGBA")
    ca_rgba.putalpha(mask)
    rgba.alpha_composite(ca_rgba, (x, y))

    # Badge A arredondado
    badge = Image.new("RGBA", (82, 82), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(badge)
    bdraw.rounded_rectangle([0, 0, 82, 82], radius=radius_dx, fill=NAVY + (255,))
    rgba.alpha_composite(badge, (x, y))
    img = rgba.convert("RGB")
    d = ImageDraw.Draw(img)

    f_lbl = FP(56, 900)
    bb = d.textbbox((0, 0), "A", font=f_lbl)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    d.text((x + (82-tw)//2, y + (82-th)//2 - 8), "A", font=f_lbl, fill=PAPER)

    # Bullets à direita — distribuídos verticalmente no espaço da imagem
    tx = x + cw_i + 40
    f_bu = FP(60, 900)
    f_bt = FS(30, 500)
    notes = [
        ("Ar livre",  "na cavidade peritoneal."),
        ("Úlcera",    "duodenal perfurada."),
        ("AINE",      "+ corticoide = risco."),
    ]
    max_w = W - tx - 40
    block_h = ch_i // 3
    for i, (kw, txt) in enumerate(notes):
        ny = y + i * block_h + 20
        d.text((tx, ny), kw, font=f_bu, fill=BRAND_BLUE)
        lines = wrap(d, txt, f_bt, max_w)
        yy = ny + 78
        for ln in lines:
            d.text((tx, yy), ln, font=f_bt, fill=INK_DARK)
            yy += 40

    footer_handle(d)
    img.save(f"{OUT}/slide_7.png", quality=95)

# ============================================================
# SLIDE 8 — Manejo
# ============================================================
def slide_manejo():
    img = bg_paper()
    d   = ImageDraw.Draw(img)
    header(d)

    f_t1 = FP(150, 900)
    d.text((42, 145), "O manejo.", font=f_t1, fill=NAVY)

    items = [
        ("01", "CIRURGIA",        "Laparotomia ou laparoscopia + patch de Graham modificado."),
        ("02", "ÚLCERA DUODENAL", "Duodenotomia + ulcerorrafia + vagotomia + duodenoplastia."),
        ("03", "SUPORTE",         "Hidratação, analgesia, antibiótico."),
        ("04", "PÓS-OP",          "Omeprazol dose plena 4 sem + H. pylori."),
        ("05", "CONSERVADOR?",    "Só se alto risco cirúrgico, pneumoperitônio pequeno, sem líquido livre."),
    ]
    f_num   = FP(68, 900)
    f_title = FS(36, 800)
    f_body  = FS(30, 500)
    y = 395
    for num, title, txt in items:
        d.text((50, y), num, font=f_num, fill=BRAND_BLUE)
        d.text((170, y + 8), title, font=f_title, fill=NAVY)
        lines = wrap(d, txt, f_body, W - 170 - 50)
        yy = y + 68
        for ln in lines:
            d.text((170, yy), ln, font=f_body, fill=INK_DARK)
            yy += 40
        y = yy + 32

    footer_handle(d)
    img.save(f"{OUT}/slide_8.png", quality=95)

# ============================================================
# FLASHCARD SLIDE HELPER (legado, não usado mais)
# ============================================================
def draw_flashcard(img, d, x, y, w, h, front, back_highlight, back_extra=""):
    """Desenha um flashcard no estilo Anki do MedPro."""
    # Card branco com borda e "sombra"
    d.rectangle([x+6, y+8, x+w+6, y+h+8], fill=(210, 204, 195))  # sombra
    d.rectangle([x, y, x+w, y+h], fill=CARD_WHITE, outline=NAVY, width=2)

    # Cabeçalho da card (barra navy com selo)
    d.rectangle([x, y, x+w, y+56], fill=NAVY)
    f_brand = FP(22, 900)
    d.text((x+20, y+16), "M.", font=f_brand, fill=PAPER)
    f_hlabel = FS(16, 700)
    d.text((x+52, y+22), "FLASHCARD · MEDPRO", font=f_hlabel, fill=LIGHT_BLUE)
    # Ícone "virar" à direita
    f_flip = FS(16, 700)
    bb = d.textbbox((0, 0), "FRENTE  ·  VERSO", font=f_flip)
    d.text((x + w - 20 - (bb[2]-bb[0]), y+22), "FRENTE  ·  VERSO",
           font=f_flip, fill=BRAND_BLUE)

    # Corpo — pergunta em cima
    pad = 30
    f_q = FP(30, 700)
    f_qb = FP(30, 900)
    # Vamos renderizar "pergunta" como linha + "resposta" com destaque
    cy = y + 80
    # Label FRENTE
    f_lbl = FS(15, 800)
    d.text((x+pad, cy), "FRENTE", font=f_lbl, fill=BRAND_BLUE)
    cy += 22
    lines = wrap(d, front, f_q, w - pad*2)
    for ln in lines:
        d.text((x+pad, cy), ln, font=f_q, fill=INK_DARK)
        cy += 42

    # Divisor
    cy += 14
    d.line([(x+pad, cy), (x+w-pad, cy)], fill=(200, 194, 184), width=1)
    cy += 24

    # VERSO
    d.text((x+pad, cy), "VERSO", font=f_lbl, fill=BRAND_BLUE)
    cy += 22
    # Texto destacado em pill
    f_hl = FP(34, 900)
    hl_lines = wrap(d, back_highlight, f_hl, w - pad*2 - 30)
    # Desenhar pill atrás
    for ln in hl_lines:
        bbox = d.textbbox((0, 0), ln, font=f_hl)
        lw = bbox[2] - bbox[0]
        d.rectangle([x+pad-8, cy-4, x+pad+lw+10, cy+44],
                    fill=(BRAND_BLUE[0], BRAND_BLUE[1], BRAND_BLUE[2]))
        d.text((x+pad, cy), ln, font=f_hl, fill=PAPER)
        cy += 54
    if back_extra:
        cy += 6
        f_ex = FS(22, 500)
        ex_lines = wrap(d, back_extra, f_ex, w - pad*2)
        for ln in ex_lines:
            d.text((x+pad, cy), ln, font=f_ex, fill=INK_MED)
            cy += 30

# ============================================================
# ANKI PRINT HELPER — paste no paper com shadow + frame sutil
# ============================================================
def _autocrop(img, bg_rgb, pad=30):
    """Recorta a imagem nos limites do conteúdo não-bg."""
    ref = Image.new("RGB", img.size, bg_rgb)
    diff = ImageChops.difference(img, ref)
    bbox = diff.getbbox()
    if not bbox:
        return img
    x0 = max(0, bbox[0] - pad)
    y0 = max(0, bbox[1] - pad)
    x1 = min(img.width,  bbox[2] + pad)
    y1 = min(img.height, bbox[3] + pad)
    return img.crop((x0, y0, x1, y1))

def _prep_buttons(target_card_w):
    """Carrega botões do Anki, troca o fundo branco pelo bg do card, escala."""
    btns = Image.open(BUTTONS_SRC).convert("RGB")
    btns = _autocrop(btns, (255, 255, 255), pad=12)
    # Troca branco por bg do card
    px = list(btns.getdata())
    px = [ANKI_BG if (p[0] > 240 and p[1] > 240 and p[2] > 240) else p for p in px]
    out = Image.new("RGB", btns.size)
    out.putdata(px)
    # Escala
    new_w = int(target_card_w * 0.90)
    ratio = new_w / out.width
    return out.resize((new_w, int(out.height * ratio)), Image.LANCZOS)

def paste_anki_print(img, d, print_path, cx, cy, target_w, radius=32):
    """Cola um print do Anki recortado + botões de resposta, com sombra e frame."""
    pr = Image.open(print_path).convert("RGB")
    pr = _autocrop(pr, ANKI_BG, pad=36)

    ratio = target_w / pr.width
    pr = pr.resize((target_w, int(pr.height * ratio)), Image.LANCZOS)

    # Prepara botões e compõe: conteúdo + gap + botões + padding inferior
    btns = _prep_buttons(target_w)
    gap = 28
    bottom_pad = 32
    btn_x = (target_w - btns.width) // 2
    comp_h = pr.height + gap + btns.height + bottom_pad
    comp = Image.new("RGB", (target_w, comp_h), ANKI_BG)
    comp.paste(pr, (0, 0))
    comp.paste(btns, (btn_x, pr.height + gap))
    pr = comp

    pw, ph = pr.size
    x = cx - pw // 2
    y = cy

    # Máscara com cantos arredondados
    mask = Image.new("L", (pw, ph), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, pw, ph], radius=radius, fill=255)

    pr_rgba = pr.convert("RGBA")
    pr_rgba.putalpha(mask)

    # Frame branco arredondado
    frame_pad = 8
    fw, fh = pw + frame_pad*2, ph + frame_pad*2
    frame = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(frame)
    fdraw.rounded_rectangle([0, 0, fw, fh], radius=radius + frame_pad,
                            fill=(255, 255, 255, 255),
                            outline=NAVY, width=2)

    # Sombra
    shadow_pad = 30
    sw, sh = fw + shadow_pad*2, fh + shadow_pad*2
    shadow = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([shadow_pad, shadow_pad + 8,
                             shadow_pad + fw, shadow_pad + fh + 8],
                            radius=radius + frame_pad,
                            fill=(26, 26, 26, 100))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))

    rgba = img.convert("RGBA")
    rgba.alpha_composite(shadow, (x - frame_pad - shadow_pad, y - frame_pad - shadow_pad))
    rgba.alpha_composite(frame, (x - frame_pad, y - frame_pad))
    rgba.alpha_composite(pr_rgba, (x, y))
    img = rgba.convert("RGB")
    return img, x, y, pw, ph

# ============================================================
# SLIDE 4 — Anki print: Pneumoperitônio (com imagem)
# Posição: logo após o hook, é o reveal do diagnóstico
# ============================================================
def slide_anki_pneumo():
    img = bg_paper()
    d   = ImageDraw.Draw(img)
    header(d)

    f_t1 = FP(108, 900)
    d.text((42, 150), "A imagem.", font=f_t1, fill=NAVY)
    f_t2 = FP(56, 700)
    d.text((48, 272), "que você precisa reconhecer.", font=f_t2, fill=INK_DARK)

    img, x, y, pw, ph = paste_anki_print(
        img, d,
        f"{ANKI}/anki_pneumo.png",
        cx=W // 2, cy=380,
        target_w=680,
    )
    d = ImageDraw.Draw(img)

    footer_handle(d)
    img.save(f"{OUT}/slide_4.png", quality=95)

# ============================================================
# SLIDE 5 — Anki print: Principais causas de abd perfurativo
# ============================================================
def slide_anki_causas():
    img = bg_paper()
    d   = ImageDraw.Draw(img)
    header(d)

    f_t1 = FP(108, 900)
    d.text((42, 150), "Pneumo =", font=f_t1, fill=NAVY)
    f_t2 = FP(80, 900)
    d.text((42, 270), "abd perfurativo.", font=f_t2, fill=BRAND_BLUE)

    img, x, y, pw, ph = paste_anki_print(
        img, d,
        f"{ANKI}/anki_causas.png",
        cx=W // 2, cy=420,
        target_w=780,
    )
    d = ImageDraw.Draw(img)

    footer_handle(d)
    img.save(f"{OUT}/slide_5.png", quality=95)

# ============================================================
# SLIDE 6 — EXTRA — Anki print: Sinal de Jobert
# ============================================================
def slide_anki_jobert():
    img = bg_paper()
    d   = ImageDraw.Draw(img)
    header(d)

    # Badge EXTRA (pill destacada)
    badge_x, badge_y, badge_w, badge_h = 50, 155, 140, 42
    d.rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
                fill=NAVY)
    f_badge = FS(20, 800)
    bb = d.textbbox((0, 0), "EXTRA", font=f_badge)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    d.text((badge_x + (badge_w - tw)//2, badge_y + (badge_h - th)//2 - 6),
           "EXTRA", font=f_badge, fill=PAPER)

    f_t1 = FP(108, 900)
    d.text((42, 220), "Sinal de", font=f_t1, fill=NAVY)
    f_t2 = FP(108, 900)
    d.text((42, 340), "Jobert.", font=f_t2, fill=BRAND_BLUE)

    img, x, y, pw, ph = paste_anki_print(
        img, d,
        f"{ANKI}/anki_jobert.png",
        cx=W // 2, cy=490,
        target_w=780,
    )
    d = ImageDraw.Draw(img)

    footer_handle(d)
    img.save(f"{OUT}/slide_6.png", quality=95)

# ============================================================
# SLIDE 9 — CTA final
# ============================================================
def slide_cta():
    img = bg_navy()
    d   = ImageDraw.Draw(img)
    header(d, dark=True)

    f_tag = FS(26, 800)
    d.text((50, 180), "NÃO SE ARRISQUE NA PROVA.", font=f_tag, fill=BRAND_BLUE)

    f_t1 = FP(150, 900)
    d.text((42, 230), "Salve.", font=f_t1, fill=PAPER)
    d.text((42, 400), "Compartilha.", font=f_t1, fill=PAPER)
    d.text((42, 570), "Revisa.", font=f_t1, fill=BRAND_BLUE)

    # Linha fina
    d.line([(50, 760), (W-50, 760)], fill=LIGHT_BLUE, width=1)

    # Corpo
    f_body = FS(32, 500)
    body = ("Todo dia um pedaço da prova no seu feed. "
            "Deck completo de flashcards no link da bio.")
    lines = wrap(d, body, f_body, W - 100)
    yy = 810
    for ln in lines:
        d.text((50, yy), ln, font=f_body, fill=(230, 230, 230))
        yy += 44

    # CTA de @
    f_arrow = FP(68, 900)
    d.text((50, 1020), "→  segue", font=f_arrow, fill=BRAND_BLUE)
    f_handle = FP(68, 900)
    d.text((50, 1110), "@medproflashcards", font=f_handle, fill=PAPER)

    footer_handle(d, dark=True)
    img.save(f"{OUT}/slide_9.png", quality=95)

# --- RUN ---
# Ordem: capa → caso → hook → pneumo → causas → EXTRA Jobert → Dx → manejo → CTA
slide_capa();        print("1 capa")
slide_caso();        print("2 caso")
slide_hook();        print("3 hook")
slide_anki_pneumo(); print("4 pneumo")
slide_anki_causas(); print("5 causas")
slide_anki_jobert(); print("6 extra jobert")
slide_dx();          print("7 diagnóstico")
slide_manejo();      print("8 manejo")
slide_cta();         print("9 cta")
print(f"\nsaída: {OUT}")
