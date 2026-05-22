"""
Carrossel Q17 Einstein-SP 2026 — abdome agudo perfurativo (úlcera).
Identidade visual /medpro-carrossel: editorial premium.
Paleta navy/cream/red/gold + Fraunces/Inter/Caveat/JetBrains Mono.
9 slides 1080×1440.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

# ============================================================
# Paths
# ============================================================
BASE    = "/Users/marianarocha/Documents/Claude/MedPro Flashcards/Instagram/Posts/carrossel_einstein2026_q17"
TC_SRC  = f"{BASE}/tc_clean.png"
TC2_SRC = f"{BASE}/tc_axial2.png"
FONTS   = os.path.expanduser("~/.claude/skills/questão-post/assets/fonts")
BRAND   = os.path.expanduser("~/.claude/skills/questão-post/assets/brand")
ANKI    = f"{BASE}/anki_prints"
OUT     = f"{BASE}/slides"
os.makedirs(OUT, exist_ok=True)

# ============================================================
# Canvas + Paleta
# ============================================================
W, H = 1080, 1440

NAVY       = (15, 35, 64)       # #0F2340
OFF        = (250, 250, 247)    # #FAFAF7
CREAM      = (239, 233, 217)    # #EFE9D9
RED        = (201, 53, 43)      # #C9352B
GOLD       = (201, 169, 97)     # #C9A961
BLACK      = (10, 10, 10)       # #0A0A0A
CLOZE_BLUE = (31, 0, 255)       # #1F00FF
INK_MED    = (118, 118, 111)    # gray

# ============================================================
# Fontes (variable)
# ============================================================
FRAUNCES = f"{FONTS}/Fraunces[SOFT,WONK,opsz,wght].ttf"
INTER    = f"{FONTS}/Inter[opsz,wght].ttf"
CAVEAT   = f"{FONTS}/Caveat[wght].ttf"
JBMONO   = f"{FONTS}/JetBrainsMono[wght].ttf"

def FF(size, weight=800, opsz=None, soft=30):
    if opsz is None: opsz = max(9, min(144, size // 2))
    f = ImageFont.truetype(FRAUNCES, size)
    try: f.set_variation_by_axes([opsz, weight, soft, 0])
    except: pass
    return f

def FI(size, weight=500, opsz=None):
    if opsz is None: opsz = max(14, min(32, size // 2))
    f = ImageFont.truetype(INTER, size)
    try: f.set_variation_by_axes([opsz, weight])
    except: pass
    return f

def FC(size, weight=600):
    f = ImageFont.truetype(CAVEAT, size)
    try: f.set_variation_by_axes([weight])
    except: pass
    return f

def FM(size, weight=500):
    f = ImageFont.truetype(JBMONO, size)
    try: f.set_variation_by_axes([weight])
    except: pass
    return f

# ============================================================
# Helpers
# ============================================================
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

def draw_text(d, xy, text, font, fill, tracking=0):
    """Desenha texto com tracking opcional (letter-spacing)."""
    if tracking == 0:
        d.text(xy, text, font=font, fill=fill)
        return
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        bb = d.textbbox((0, 0), ch, font=font)
        x += (bb[2] - bb[0]) + tracking

def text_width(d, text, font, tracking=0):
    if tracking == 0:
        bb = d.textbbox((0, 0), text, font=font)
        return bb[2] - bb[0]
    w = 0
    for ch in text:
        bb = d.textbbox((0, 0), ch, font=font)
        w += (bb[2] - bb[0]) + tracking
    return w - tracking if text else 0

# ============================================================
# Backgrounds
# ============================================================
PAPER_RAW = Image.open(f"{BRAND}/paper.png").convert("RGB")

def apply_paper(canvas, dark=False, opacity=0.55):
    """Aplica textura paper.png com blend simulando multiply/soft-light."""
    paper = PAPER_RAW.resize(canvas.size, Image.LANCZOS)
    if dark:
        # Soft-light fake: aplica paper como overlay claro com alpha baixo
        # Pega a textura, reduz contraste, blend
        paper_rgba = paper.convert("RGBA")
        # Reduz alpha (suaviza)
        a = paper_rgba.split()[3].point(lambda v: int(v * 0.18))
        paper_rgba.putalpha(a)
        c = canvas.convert("RGBA")
        c.alpha_composite(paper_rgba)
        return c.convert("RGB")
    else:
        # Multiply
        # Para clarear o multiply (não escurecer demais), lerp da textura com branco
        mixed = Image.blend(Image.new("RGB", canvas.size, (255, 255, 255)),
                            paper, opacity * 0.5)
        return ImageChops.multiply(canvas, mixed)

def bg_navy():
    img = Image.new("RGB", (W, H), NAVY)
    return apply_paper(img, dark=True)

def bg_cream():
    img = Image.new("RGB", (W, H), CREAM)
    return apply_paper(img, dark=False)

def bg_off():
    img = Image.new("RGB", (W, H), OFF)
    return apply_paper(img, dark=False, opacity=0.35)

# ============================================================
# Logo
# ============================================================
LOGO_CREAM = Image.open(f"{BRAND}/logo-cream.png").convert("RGBA")
LOGO_NAVY  = Image.open(f"{BRAND}/logo-navy.png").convert("RGBA")

def paste_logo(canvas, dark=False, x=None, y=85, size=80):
    """Cola logo. Dark=True usa cream (sobre navy); False usa navy."""
    logo = (LOGO_CREAM if dark else LOGO_NAVY).copy()
    ratio = size / logo.height
    new_size = (int(logo.width * ratio), int(logo.height * ratio))
    logo = logo.resize(new_size, Image.LANCZOS)
    if x is None:
        x = 70
    rgba = canvas.convert("RGBA")
    rgba.alpha_composite(logo, (x, y))
    return rgba.convert("RGB")

# ============================================================
# Folio (canto inferior direito)
# ============================================================
def draw_folio(d, dark=False):
    color = OFF if dark else NAVY
    color = tuple(int(c*0.6 + 255*0.4) if not dark else int(c*0.7 + 0.3*c) for c in color) if False else (INK_MED if not dark else (180, 180, 175))
    f = FM(14, 500)
    text = "PADRÃO MEDPRO  /  DIRETO AO PONTO"
    w = text_width(d, text, f, tracking=2)
    draw_text(d, (W - 70 - w, H - 50), text, f, color, tracking=2)

# ============================================================
# Header padrão de TODOS os slides — logo MedPro + @medproflashcards
# ============================================================
def draw_header(canvas, dark=False):
    """Logo à esquerda + @medproflashcards à direita. Aplicado em todos os slides."""
    logo = (LOGO_CREAM if dark else LOGO_NAVY).copy()
    logo_size = 58
    ratio = logo_size / logo.height
    logo = logo.resize((int(logo.width * ratio), logo_size), Image.LANCZOS)
    rgba = canvas.convert("RGBA")
    rgba.alpha_composite(logo, (70, 80))
    img = rgba.convert("RGB")

    d = ImageDraw.Draw(img)
    f_handle = FI(20, 600)
    handle = "@medproflashcards"
    hw = text_width(d, handle, f_handle)
    handle_color = OFF if dark else BLACK
    d.text((W - 70 - hw, 100), handle, font=f_handle, fill=handle_color)

    # Linha divisória sutil
    line_color = (180, 180, 175) if dark else (160, 156, 145)
    d.line([(70, 165), (W - 70, 165)], fill=line_color, width=1)

    return img

# ============================================================
# SLIDE 1 — Capa: EINSTEIN 2026 gigante + pergunta + grid 2 imagens
# ============================================================
def slide_capa():
    img = bg_cream()
    img = draw_header(img, dark=False)
    d = ImageDraw.Draw(img)

    # ============================================================
    # EINSTEIN 2026: — Fraunces 900, GIGANTE (maior que tudo)
    # ============================================================
    f_brand = FF(195, 900, soft=20)
    brand_y = 220
    d.text((70, brand_y), "EINSTEIN", font=f_brand, fill=BLACK)
    d.text((70, brand_y + 170), "2026", font=f_brand, fill=BLACK)
    # Dois pontos vermelhos
    f_colon = FF(195, 900, soft=20)
    colon_x = 70 + text_width(d, "2026", f_brand)
    d.text((colon_x, brand_y + 170), ":", font=f_colon, fill=RED)

    # ============================================================
    # Pergunta (menor) — Fraunces 700
    # ============================================================
    q_y = brand_y + 380
    f_q = FF(56, 700, soft=20)
    d.text((70, q_y), "Dor abdominal + ingestão", font=f_q, fill=BLACK)
    d.text((70, q_y + 72), "de álcool — conduta", font=f_q, fill=BLACK)
    # "?" vermelho
    f_punct = FF(80, 900, soft=20)
    q2 = "de álcool — conduta"
    qmark_x = 70 + text_width(d, q2, f_q) + 4
    d.text((qmark_x, q_y + 60), "?", font=f_punct, fill=RED)

    # ============================================================
    # GRID 1×2 das duas TCs (lado a lado, BEM grandes, SEM labels)
    # ============================================================
    grid_y = 920
    grid_h = 440
    gap = 16
    cell_w = (W - 140 - gap) // 2

    for i, src in enumerate([TC_SRC, TC2_SRC]):
        tc = Image.open(src).convert("RGB")
        # Crop pra preencher o frame (aspect cover)
        target_ratio = cell_w / grid_h
        src_ratio = tc.width / tc.height
        if src_ratio > target_ratio:
            new_h = tc.height
            new_w = int(new_h * target_ratio)
            x0 = (tc.width - new_w) // 2
            tc = tc.crop((x0, 0, x0 + new_w, new_h))
        else:
            new_w = tc.width
            new_h = int(new_w / target_ratio)
            y0 = (tc.height - new_h) // 2
            tc = tc.crop((0, y0, new_w, y0 + new_h))
        tc = tc.resize((cell_w, grid_h), Image.LANCZOS)

        x = 70 + i * (cell_w + gap)
        img.paste(tc, (x, grid_y))

    img.save(f"{OUT}/slide_1.png", quality=95)

# ============================================================
# SLIDE 2 — O caso
# ============================================================
def slide_caso():
    img = bg_off()
    img = draw_header(img, dark=False)
    d = ImageDraw.Draw(img)

    f_h = FF(150, 900, soft=20)
    d.text((70, 230), "O caso", font=f_h, fill=NAVY)
    # Ponto vermelho gigante
    f_dot = FF(150, 900, soft=20)
    after_x = 70 + text_width(d, "O caso", f_h)
    d.text((after_x, 230), ".", font=f_dot, fill=RED)

    f_head = FI(22, 700)
    f_body = FF(40, 500, soft=20)
    blocks = [
        ("PACIENTE",    "Homem, 32 anos, previamente hígido."),
        ("ÁLCOOL",      "Binge drinking há 3 dias."),
        ("QUADRO",      "Dor andar superior 8/10 há 2 dias + 2 vômitos."),
        ("EXAME",       "FC 125 · PA 110×85 · abdome intocável por dor."),
        ("APÓS A TC",   "Rebaixamento, hipotensão, má perfusão."),
    ]
    y = 470
    for head_text, body_text in blocks:
        draw_text(d, (70, y), head_text, f_head, GOLD, tracking=4)
        lines = wrap(d, body_text, f_body, W - 140)
        yy = y + 38
        for ln in lines:
            d.text((70, yy), ln, font=f_body, fill=NAVY)
            yy += 56
        y = yy + 32

    draw_folio(d, dark=False)
    img.save(f"{OUT}/slide_2.png", quality=95)

# ============================================================
# SLIDE 3 — Hook (navy)
# ============================================================
def slide_hook():
    img = bg_navy()
    img = draw_header(img, dark=True)
    d = ImageDraw.Draw(img)

    # Aspas tipográficas monumentais em vermelho
    f_quote = FF(340, 900, soft=20)
    d.text((50, 240), "“", font=f_quote, fill=RED)

    f_big = FF(140, 800, soft=20)
    d.text((70, 580), "Saberia", font=f_big, fill=OFF)
    d.text((70, 730), "responder", font=f_big, fill=OFF)
    f_tail = FF(140, 800, soft=20)
    d.text((70, 880), "agora", font=f_tail, fill=GOLD)
    f_punct = FF(170, 900, soft=20)
    qmark_x = 70 + text_width(d, "agora", f_tail) + 4
    d.text((qmark_x, 850), "?", font=f_punct, fill=RED)

    img.save(f"{OUT}/slide_3.png", quality=95)

# ============================================================
# Card Anki render — fundo branco, pergunta preta, resposta cloze azul
# Uma palavra-chave sublinhada na resposta
# ============================================================
def slide_anki_card(slide_num, eyebrow_text, pergunta, resposta, palavra_sublinhada,
                    tc_image=None, slide_filename="slide_anki.png"):
    """Renderiza slide de card Anki "raw" estilo screenshot.
    Header com logo + @medproflashcards sempre presente.
    Sem eyebrow (REGRA DURA).
    """
    img = Image.new("RGB", (W, H), OFF)
    img = draw_header(img, dark=False)
    d = ImageDraw.Draw(img)

    # Pergunta — Inter 500-600
    f_q = FI(44, 600)
    q_lines = wrap(d, pergunta, f_q, W - 200)
    y = 280 if tc_image else 420
    for ln in q_lines:
        lw = text_width(d, ln, f_q)
        d.text(((W - lw) // 2, y), ln, font=f_q, fill=BLACK)
        y += 70

    # Imagem opcional (TC)
    if tc_image:
        tc = Image.open(tc_image).convert("RGB")
        img_h_target = 480
        ratio_tc = img_h_target / tc.height
        new_w = int(tc.width * ratio_tc)
        if new_w > W - 240:
            new_w = W - 240
            ratio_tc = new_w / tc.width
            img_h_target = int(tc.height * ratio_tc)
        tc = tc.resize((new_w, img_h_target), Image.LANCZOS)
        y += 30
        img.paste(tc, ((W - new_w) // 2, y))
        y += img_h_target + 60

    # Resposta — Inter 700 AZUL CLOZE
    f_r = FI(54, 700)
    r_lines = wrap(d, resposta, f_r, W - 200)
    if not tc_image:
        y += 30
    for ln in r_lines:
        lw = text_width(d, ln, f_r)
        x = (W - lw) // 2
        d.text((x, y), ln, font=f_r, fill=CLOZE_BLUE)

        # Sublinhar palavra-chave se aparecer nessa linha
        if palavra_sublinhada and palavra_sublinhada in ln:
            # achar posição da palavra
            before = ln.split(palavra_sublinhada, 1)[0]
            before_w = text_width(d, before, f_r)
            word_w = text_width(d, palavra_sublinhada, f_r)
            ul_y = y + 60
            d.line([(x + before_w, ul_y), (x + before_w + word_w, ul_y)],
                   fill=CLOZE_BLUE, width=4)
        y += 78

    # Sem folio, sem logo, sem ornamento — é card "raw"
    img.save(f"{OUT}/{slide_filename}", quality=95)

# ============================================================
# SLIDE 4 — Anki: pneumoperitônio (com TC)
# ============================================================
def slide_4():
    slide_anki_card(
        slide_num=4,
        eyebrow_text="§ 04 — Card",
        pergunta="TC de abdome com ar livre subdiafragmático. Achado?",
        resposta="Pneumoperitônio.",
        palavra_sublinhada="Pneumoperitônio",
        tc_image=TC_SRC,
        slide_filename="slide_4.png",
    )

# ============================================================
# SLIDE 5 — Anki: causa (binge → úlcera perfurada)
# ============================================================
def slide_5():
    slide_anki_card(
        slide_num=5,
        eyebrow_text="§ 05 — Card",
        pergunta="Jovem, binge drinking, dor epigástrica súbita. Causa mais provável?",
        resposta="Úlcera péptica perfurada.",
        palavra_sublinhada="perfurada",
        tc_image=None,
        slide_filename="slide_5.png",
    )

# ============================================================
# SLIDE 6 — EXTRA Anki: Boerhaave
# ============================================================
def slide_6():
    slide_anki_card(
        slide_num=6,
        eyebrow_text="§ 06 — Card · DDx",
        pergunta="Vômitos forçados, dor torácica baixa, choque. DDx?",
        resposta="Síndrome de Boerhaave.",
        palavra_sublinhada="Boerhaave",
        tc_image=None,
        slide_filename="slide_6.png",
    )

# ============================================================
# SLIDE 7 — Diagnóstico
# ============================================================
def slide_dx():
    img = bg_off()
    img = draw_header(img, dark=False)
    d = ImageDraw.Draw(img)

    # Headline
    f_h = FF(110, 900, soft=20)
    d.text((70, 230), "Abdome agudo", font=f_h, fill=NAVY)
    f_h2 = FF(110, 900, soft=20)
    d.text((70, 355), "perfurativo", font=f_h2, fill=NAVY)
    # Ponto vermelho
    f_punct = FF(140, 900, soft=20)
    dot_x = 70 + text_width(d, "perfurativo", f_h2)
    d.text((dot_x, 345), ".", font=f_punct, fill=RED)

    # TC à esquerda
    tc = Image.open(TC_SRC).convert("RGB")
    cell_w, cell_h = 480, 540
    ratio = min(cell_w/tc.width, cell_h/tc.height)
    new_size = (int(tc.width*ratio), int(tc.height*ratio))
    tc = tc.resize(new_size, Image.LANCZOS)
    iw, ih = new_size
    tc_x, tc_y = 70, 560
    img.paste(tc, (tc_x, tc_y))

    # Bullets à direita
    d = ImageDraw.Draw(img)
    tx = tc_x + iw + 50
    notes = [
        ("Ar livre",    "subdiafragmático na TC."),
        ("Úlcera",      "péptica perfurada por binge."),
        ("Após TC",     "evolui com choque séptico."),
    ]
    max_w = W - tx - 70
    block_h = ih // 3
    f_kw = FF(48, 800, soft=20)
    f_bt = FI(26, 500)
    for i, (kw, txt) in enumerate(notes):
        ny = tc_y + i * block_h + 20
        d.text((tx, ny), kw, font=f_kw, fill=GOLD)
        lines = wrap(d, txt, f_bt, max_w)
        yy = ny + 62
        for ln in lines:
            d.text((tx, yy), ln, font=f_bt, fill=NAVY)
            yy += 36

    draw_folio(d, dark=False)
    img.save(f"{OUT}/slide_7.png", quality=95)

# ============================================================
# SLIDE 8 — Manejo
# ============================================================
def slide_manejo():
    img = bg_off()
    img = draw_header(img, dark=False)
    d = ImageDraw.Draw(img)

    f_h = FF(150, 900, soft=20)
    d.text((70, 230), "O manejo", font=f_h, fill=NAVY)
    f_dot = FF(150, 900, soft=20)
    dot_x = 70 + text_width(d, "O manejo", f_h)
    d.text((dot_x, 230), ".", font=f_dot, fill=RED)

    items = [
        ("01", "RESSUSCITAR",  "Cristaloide em bolus + UTI. Alvo: PAM ≥ 65."),
        ("02", "ATB",          "Cefalo 3ª + metronidazol cobrindo víscera oca."),
        ("03", "IBP EV",       "Omeprazol 80 mg bolus + 8 mg/h."),
        ("04", "LAPAROTOMIA",  "Patch de Graham + lavagem da cavidade."),
        ("05", "PÓS-OP",       "Pesquisar H. pylori + IBP VO por 4-6 semanas."),
    ]
    f_num   = FF(78, 900, soft=20)
    f_title = FI(30, 700)
    f_body  = FI(28, 500)
    y = 520
    for num, title, txt in items:
        d.text((70, y), num, font=f_num, fill=GOLD)
        d.text((200, y + 10), title, font=f_title, fill=NAVY)
        lines = wrap(d, txt, f_body, W - 200 - 70)
        yy = y + 56
        for ln in lines:
            d.text((200, yy), ln, font=f_body, fill=NAVY)
            yy += 38
        y = yy + 38

    draw_folio(d, dark=False)
    img.save(f"{OUT}/slide_8.png", quality=95)

# ============================================================
# SLIDE 9 — CTA (NAVY)
# ============================================================
def slide_cta():
    img = bg_navy()
    img = draw_header(img, dark=True)
    d = ImageDraw.Draw(img)

    # "Feito por aprovados" em Caveat RED, rotação leve
    f_caveat = FC(180, 600)
    cv_layer = Image.new("RGBA", (W, 400), (0, 0, 0, 0))
    cv_d = ImageDraw.Draw(cv_layer)
    cv_d.text((50, 50), "Feito por", font=f_caveat, fill=RED)
    cv_d.text((50, 200), "aprovados.", font=f_caveat, fill=RED)
    cv_layer = cv_layer.rotate(-2.5, resample=Image.BICUBIC, expand=False)
    rgba = img.convert("RGBA")
    rgba.alpha_composite(cv_layer, (10, 380))
    img = rgba.convert("RGB")
    d = ImageDraw.Draw(img)

    # Linha
    d.line([(70, 920), (W - 70, 920)], fill=(180, 180, 175), width=1)

    # Stats em Inter
    f_stats = FI(28, 500)
    stats = "+19k flashcards · +700 aprovados · link na bio"
    sw = text_width(d, stats, f_stats)
    d.text(((W - sw) // 2, 970), stats, font=f_stats, fill=CREAM)

    # @handle em Fraunces
    f_handle = FF(60, 800, soft=20)
    handle = "@medproflashcards"
    hw = text_width(d, handle, f_handle)
    d.text(((W - hw) // 2, 1060), handle, font=f_handle, fill=OFF)

    # URL em Inter (sem JBMono — REGRA: nada de eyebrow, mas folio/URL pode usar mono — mantenho)
    f_url = FI(18, 600)
    url = "medproflashcards.com.br/links"
    uw = text_width(d, url, f_url, tracking=3)
    draw_text(d, ((W - uw) // 2, 1160), url, f_url, GOLD, tracking=3)

    img.save(f"{OUT}/slide_9.png", quality=95)

# ============================================================
# RUN
# ============================================================
slide_capa();   print("1 capa")
slide_caso();   print("2 caso")
slide_hook();   print("3 hook")
slide_4();      print("4 anki achado")
slide_5();      print("5 anki causa")
slide_6();      print("6 anki extra")
slide_dx();     print("7 diagnóstico")
slide_manejo(); print("8 manejo")
slide_cta();    print("9 cta")
print(f"\nsaída: {OUT}")
