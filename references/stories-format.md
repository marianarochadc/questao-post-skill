# Stories format

Stories são a versão enxuta do carrossel, formatada pra 1080×1920 (proporção 9:16) com safe zones.

## Safe zones do Instagram

O IG sobrepõe UI nas extremidades. Trabalhe sempre dentro de:

```python
SAFE_TOP = 280        # foto + nome + "Story" sobrescrevem isso
SAFE_BOT = H - 380    # = 1540 — reactions, DM bar, "Enviar mensagem"
```

Margem horizontal: 60px de cada lado (40 em capas com imagem grande).

## Estrutura típica (5-6 stories)

Sempre **mais curto** que o carrossel — usuária vê 5 segundos por story, só.

1. **Capa** — brand grande + pergunta compacta + imagem chave gigante
2. **Caso** — 4 blocos compactos
3. **Achado/Germe** — diagnóstico em destaque azul + imagem auxiliar
4. **ATB/Conduta** — pills com nomes-chave + observação crítica
5. **Manejo** — 3 passos numerados (não 5 como no carrossel)
6. **CTA** — fundo NAVY + "Salve. Compartilha. Revisa." + @handle

Se a questão for SIMPLES, pode comprimir em **4 stories**: capa + caso + resposta + CTA.

## Tipografia ajustada pra 1920

| Elemento | Tamanho | Notas |
|----------|---------|-------|
| Brand capa | 78-90 | uma linha "BANCA-UF, ANO." |
| Pergunta capa | 58-72 | uma linha curta |
| Título story | 120-140 | Playfair 900 |
| Cloze gigante | 100-130 | resposta principal |
| Subtítulo | 36-48 | DM Sans 700 |
| Body | 30-44 | DM Sans 500 |
| CTA verbos | 140 | Playfair 900 — atenção que 180+ pode estourar a largura ("Compartilha." tem 12 chars) |
| Handle CTA | 78-88 | "@medproflashcards" |

## Detalhe crítico — escala de imagens

Se a imagem da questão é pequena (ex: cultura 529×505) e você quer ela GIGANTE no story, **NÃO use `thumbnail()`** — ele só REDUZ.

Use:

```python
iw, ih = src_img.size
ratio = min(w / iw, h / ih)
new_size = (int(iw * ratio), int(ih * ratio))
src_img = src_img.resize(new_size, Image.LANCZOS)
```

Já tá assim no template.

## Header/footer simplificado

Stories também têm header com "M. medpro" e linha, mas o espaçamento é diferente:

```python
def header(draw, dark=False):
    f_logo   = FP(52, 900)
    f_handle = FS(26, 700)
    draw.text((60, SAFE_TOP - 130), "M.", font=f_logo, fill=...)
    draw.text((130, SAFE_TOP - 110), "medpro", font=f_handle, fill=...)
    draw.line([(60, SAFE_TOP - 40), (W-60, SAFE_TOP - 40)], ...)

def footer_handle(draw, dark=False):
    draw.line([(60, SAFE_BOT + 40), (W-60, SAFE_BOT + 40)], ...)
    # "@medproflashcards" centrado em SAFE_BOT + 70
```

## Quando NÃO fazer stories

- Questão sem imagem (perde o impacto visual no formato vertical)
- Questão MUITO simples (basta o carrossel)
- Quando a usuária pede só carrossel

Sempre confirme se ela quer stories antes de gerar. É arquivo extra e tempo extra.
