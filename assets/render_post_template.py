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
# ============================================================
# Card Anki estilo /medpro-carrossel
# Fundo cream + card off com sombra + card branco com border navy +
# badge "Flashcard MedPro" flutuante + Helvetica + cloze azul inline
# ============================================================
HELVETICA = "/System/Library/Fonts/Helvetica.ttc"

def FH(size, style="regular"):
    """Helvetica (system) — pergunta dentro do card."""
    idx = {"regular": 0, "bold": 1, "italic": 2}[style]
    try:
        return ImageFont.truetype(HELVETICA, size, index=idx)
    except Exception:
        fb = {"regular": "/System/Library/Fonts/Supplemental/Arial.ttf",
              "bold":    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "italic":  "/System/Library/Fonts/Supplemental/Arial Italic.ttf"}[style]
        return ImageFont.truetype(fb, size)

def draw_cloze_line(d, segments, y_baseline, font_q, font_cloze, center_x, max_w):
    """Desenha uma linha com segmentos mistos (texto normal + cloze).
    segments: lista de tuplas (texto, is_cloze, underlined).
    Retorna (last_y, num_lines_drawn).

    Faz wrap respeitando max_w. Centraliza cada linha.
    """
    # Quebra cada segmento em palavras mantendo o estilo
    tokens = []  # [(word, is_cloze, underlined)]
    for txt, is_cloze, ul in segments:
        for w in txt.split(" "):
            if w:
                tokens.append((w, is_cloze, ul))

    # Monta linhas respeitando max_w
    lines = []  # [[(word, is_cloze, ul, w_pixels), ...], ...]
    cur_line = []
    cur_w = 0
    space_w = d.textlength(" ", font=font_q)
    for word, is_cloze, ul in tokens:
        f = font_cloze if is_cloze else font_q
        ww = d.textlength(word, font=f)
        sep = space_w if cur_line else 0
        if cur_w + sep + ww > max_w and cur_line:
            lines.append(cur_line)
            cur_line = [(word, is_cloze, ul, ww)]
            cur_w = ww
        else:
            cur_line.append((word, is_cloze, ul, ww))
            cur_w += sep + ww
    if cur_line:
        lines.append(cur_line)

    # Renderiza cada linha centralizada
    line_h = int(font_q.size * 1.45)
    for li, line in enumerate(lines):
        total_w = sum(w for _,_,_,w in line) + space_w * (len(line) - 1)
        x = center_x - total_w // 2
        ly = y_baseline + li * line_h
        for word, is_cloze, ul, ww in line:
            f = font_cloze if is_cloze else font_q
            color = CLOZE_BLUE if is_cloze else BLACK
            d.text((x, ly), word, font=f, fill=color)
            if ul:
                ul_y = ly + f.size + 4
                d.line([(x, ul_y), (x + ww, ul_y)], fill=CLOZE_BLUE, width=3)
            x += ww + space_w
    return y_baseline + len(lines) * line_h, len(lines)

def slide_anki_card(headline, pergunta_segments, extra=None,
                    tc_image=None, slide_filename="slide_anki.png"):
    """Slide de card Anki estilo /medpro-carrossel:
    - Fundo cream
    - Card off off-white com sombra + border sutil
    - Headline Fraunces 96 NAVY
    - Card branco interno com border navy 2px + badge "Flashcard MedPro"
    - Pergunta Helvetica 32 com cloze azul (sublinhada opcional) inline
    - Extra italic cinza opcional
    - Imagem opcional
    - Footer: "Card curto. Resposta cirúrgica." + folio mono
    """
    # Fundo cream
    img = bg_cream()

    # Card off (inset 48) com sombra
    inset = 48
    card_x = inset
    card_y = inset
    card_w = W - inset * 2
    card_h = H - inset * 2

    # Sombra (gaussian blur abaixo do card)
    shadow_pad = 50
    shadow_layer = Image.new("RGBA", (card_w + shadow_pad*2, card_h + shadow_pad*2), (0,0,0,0))
    sd = ImageDraw.Draw(shadow_layer)
    sd.rounded_rectangle([shadow_pad, shadow_pad + 12,
                          shadow_pad + card_w, shadow_pad + card_h + 12],
                         radius=28, fill=(15, 35, 64, 50))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(20))
    rgba = img.convert("RGBA")
    rgba.alpha_composite(shadow_layer, (card_x - shadow_pad, card_y - shadow_pad))
    img = rgba.convert("RGB")

    # Card off arredondado
    card_layer = Image.new("RGBA", (card_w, card_h), (0,0,0,0))
    cd = ImageDraw.Draw(card_layer)
    cd.rounded_rectangle([0, 0, card_w, card_h], radius=28, fill=OFF + (255,),
                         outline=(15, 35, 64, 26), width=1)
    rgba = img.convert("RGBA")
    rgba.alpha_composite(card_layer, (card_x, card_y))
    img = rgba.convert("RGB")

    d = ImageDraw.Draw(img)

    # Headline Fraunces NAVY 96 — padding generoso no topo
    f_head = FF(96, 900, soft=20)
    head_x = card_x + 52
    head_y = card_y + 60
    head_lines = wrap(d, headline, f_head, card_w - 104)
    for ln in head_lines:
        d.text((head_x, head_y), ln, font=f_head, fill=NAVY)
        head_y += int(96 * 0.92)

    # Card flashcard interno (border navy 2px, bg branco)
    # JSX: margin "48px 40px 0", padding "32px 40px", borderRadius 18
    inner_margin_x = card_x + 40
    inner_margin_top = head_y + 24
    inner_w = card_w - 80
    inner_padding_x = 40
    inner_padding_y = 32

    # Calcular altura do conteúdo interno antes de desenhar a borda
    # Pergunta Helvetica 32, line-height 1.45
    f_q = FH(32, "regular")
    f_cloze = FH(32, "bold")
    f_extra = FH(22, "italic")

    # Simular dry-run pra medir altura
    inner_content_max_w = inner_w - inner_padding_x * 2
    dummy = Image.new("RGB", (10, 10))
    dd = ImageDraw.Draw(dummy)
    # Conta linhas da pergunta
    tokens = []
    for txt, is_cloze, ul in pergunta_segments:
        for w in txt.split(" "):
            if w: tokens.append((w, is_cloze, ul))
    cur_w, line_count = 0, 1
    space_w = dd.textlength(" ", font=f_q)
    for word, is_cloze, ul in tokens:
        f = f_cloze if is_cloze else f_q
        ww = dd.textlength(word, font=f)
        sep = space_w if cur_w > 0 else 0
        if cur_w + sep + ww > inner_content_max_w and cur_w > 0:
            line_count += 1
            cur_w = ww
        else:
            cur_w += sep + ww
    pergunta_h = line_count * int(32 * 1.45)

    extra_h = 0
    if extra:
        extra_lines = wrap(dd, extra, f_extra, inner_content_max_w)
        extra_h = 18 + len(extra_lines) * int(22 * 1.4)

    img_h_render = 0
    tc_w_eff = 0
    tc_h_eff = 0
    if tc_image:
        tc_meta = Image.open(tc_image)
        # Limita a TC pra max 360px de altura E max ~70% da largura (centralizada)
        max_tc_h = 360
        max_tc_w = int(inner_content_max_w * 0.75)
        ratio = min(max_tc_w / tc_meta.width, max_tc_h / tc_meta.height)
        tc_w_eff = int(tc_meta.width * ratio)
        tc_h_eff = int(tc_meta.height * ratio)
        img_h_render = tc_h_eff + 24

    # Botões Anki (sempre presentes nos cards Anki)
    btns_meta = Image.open(f"{BRAND}/anki-buttons.jpg")
    btns_w_target = int(inner_content_max_w * 0.85)
    btns_ratio = btns_w_target / btns_meta.width
    btns_h_render = int(btns_meta.height * btns_ratio) + 28

    inner_content_h = pergunta_h + extra_h + img_h_render + btns_h_render
    inner_h = inner_padding_y * 2 + inner_content_h

    # Border navy 2px + bg branco
    d.rounded_rectangle([inner_margin_x, inner_margin_top,
                         inner_margin_x + inner_w, inner_margin_top + inner_h],
                        radius=18, fill=(255, 255, 255), outline=NAVY, width=2)

    # Badge "Flashcard MedPro" flutuante (top: -12, left: 32 do JSX)
    badge_x = inner_margin_x + 32
    badge_y = inner_margin_top - 12
    f_badge = FM(15, 600)
    badge_pad_x = 12
    bb1 = dd.textbbox((0, 0), "FLASHCARD", font=f_badge)
    bb2 = dd.textbbox((0, 0), "MEDPRO", font=f_badge)
    # Tracking 0.32em (~5px)
    badge_track = 5
    w1 = text_width(dd, "FLASHCARD", f_badge, tracking=badge_track)
    w2 = text_width(dd, "MEDPRO", f_badge, tracking=badge_track)
    badge_total_w = w1 + 10 + w2  # gap 10 entre eles
    # Fundo branco do badge
    badge_h = 24
    d.rectangle([badge_x - badge_pad_x, badge_y - 2,
                 badge_x + badge_total_w + badge_pad_x, badge_y + badge_h],
                fill=(255, 255, 255))
    draw_text(d, (badge_x, badge_y), "FLASHCARD", f_badge, RED, tracking=badge_track)
    draw_text(d, (badge_x + w1 + 10, badge_y), "MEDPRO", f_badge, NAVY, tracking=badge_track)

    # Pergunta + cloze
    pergunta_y = inner_margin_top + inner_padding_y
    center_x = inner_margin_x + inner_w // 2
    draw_cloze_line(d, pergunta_segments, pergunta_y, f_q, f_cloze,
                    center_x, inner_content_max_w)

    # Extra italic cinza (opcional)
    extra_y = pergunta_y + pergunta_h
    if extra:
        extra_y += 18
        lines = wrap(d, extra, f_extra, inner_content_max_w)
        for ln in lines:
            lw = d.textlength(ln, font=f_extra)
            d.text((center_x - lw // 2, extra_y), ln, font=f_extra, fill=(85, 85, 85))
            extra_y += int(22 * 1.4)

    # Imagem opcional dentro do card (centralizada, com limite de tamanho)
    if tc_image:
        tc = Image.open(tc_image).convert("RGB").resize((tc_w_eff, tc_h_eff), Image.LANCZOS)
        img_y = extra_y + (24 if extra else 24)
        if not extra:
            img_y = pergunta_y + pergunta_h + 24
        tc_x = inner_margin_x + (inner_w - tc_w_eff) // 2
        img.paste(tc, (tc_x, img_y))
        bottom_after_img = img_y + tc_h_eff
    else:
        bottom_after_img = extra_y if extra else (pergunta_y + pergunta_h)

    # Botões Anki sempre — fica DENTRO do card branco no rodapé
    btns = Image.open(f"{BRAND}/anki-buttons.jpg").convert("RGB")
    btns_w_target = int(inner_content_max_w * 0.85)
    btns_ratio = btns_w_target / btns.width
    btns_h_final = int(btns.height * btns_ratio)
    btns = btns.resize((btns_w_target, btns_h_final), Image.LANCZOS)
    btns_y = bottom_after_img + 28
    btns_x = inner_margin_x + (inner_w - btns_w_target) // 2
    img.paste(btns, (btns_x, btns_y))

    # Footer: "Card curto. Resposta cirúrgica." + folio
    # JSX: padding "0 52px 36px", flex justify-content space-between
    d = ImageDraw.Draw(img)
    footer_y = card_y + card_h - 36 - 60
    f_left  = FF(28, 700, soft=20)
    f_left_em = FF(28, 400, soft=20)
    # "Card curto. " navy bold + "Resposta cirúrgica." red italic
    d.text((card_x + 52, footer_y), "Card curto.", font=f_left, fill=NAVY)
    cc_w = d.textlength("Card curto. ", font=f_left)
    d.text((card_x + 52 + cc_w, footer_y), "Resposta cirúrgica.", font=f_left_em, fill=RED)

    # Folio direita (JSX: JetBrains Mono 20, letter-spacing 0.24em, navy 55%)
    f_folio = FM(20, 500)
    fol_color = (15, 35, 64, 140)  # navy 55%
    # PIL não suporta alpha em fill direto pra draw — vou usar uma cor cinza-azulada
    fol_color = (105, 113, 130)
    fol_track = 4
    w_a = text_width(d, "PADRÃO MEDPRO", f_folio, tracking=fol_track)
    w_b = text_width(d, "DIRETO AO PONTO", f_folio, tracking=fol_track)
    draw_text(d, (card_x + card_w - 52 - w_a, footer_y),
              "PADRÃO MEDPRO", f_folio, fol_color, tracking=fol_track)
    draw_text(d, (card_x + card_w - 52 - w_b, footer_y + 30),
              "DIRETO AO PONTO", f_folio, fol_color, tracking=fol_track)

    img.save(f"{OUT}/{slide_filename}", quality=95)

# ============================================================
# SLIDE 4 — Anki: pneumoperitônio (com TC)
# ============================================================
def slide_4():
    slide_anki_card(
        headline="O achado.",
        pergunta_segments=[
            ("TC de abdome com ar livre subdiafragmático: ", False, False),
            ("Pneumoperitônio.", True, True),
        ],
        extra="Perfuração de víscera oca até prova em contrário.",
        tc_image=TC_SRC,
        slide_filename="slide_4.png",
    )

# ============================================================
# SLIDE 5 — Anki: causa (binge → úlcera perfurada)
# ============================================================
def slide_5():
    slide_anki_card(
        headline="A causa.",
        pergunta_segments=[
            ("Jovem + binge drinking + dor epigástrica súbita: ", False, False),
            ("úlcera péptica perfurada.", True, True),
        ],
        extra="Álcool em altas doses lesa a mucosa e inibe prostaglandinas protetoras.",
        tc_image=None,
        slide_filename="slide_5.png",
    )

# ============================================================
# SLIDE 6 — EXTRA Anki: Boerhaave (DDx)
# ============================================================
def slide_6():
    slide_anki_card(
        headline="Outro DDx.",
        pergunta_segments=[
            ("Vômitos forçados + dor torácica baixa + choque: ", False, False),
            ("síndrome de Boerhaave.", True, True),
        ],
        extra="Ruptura esofágica espontânea por vômitos. Tríade de Mackler.",
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
