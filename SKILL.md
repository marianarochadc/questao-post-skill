---
name: questão-post
description: Gera carrossel Instagram (9 slides, 1080x1350) e opcionalmente sequência de stories (1080x1920) a partir de uma questão de prova de residência médica para o @medproflashcards. Use SEMPRE que a usuária mencionar "criar post da questão", "transformar questão em carrossel", "fazer post da Q##", "fazer stories da questão", "post Instagram dessa prova", ou pedir pra adaptar uma questão (USP, UNIFESP, ENARE, Unicamp, SUS-SP, AMP, etc) em conteúdo visual. Também trigga quando ela fala "faz da Q##", "agora a Q##", "transforma em stories", ou se referir a renderizadores tipo `render_q##.py`. NÃO use pra criar posts de teoria/resumo sem questão-base; pra isso a usuária tem outras skills.
---

# questão-post

Skill pra adaptar uma questão de prova de residência médica em conteúdo visual (carrossel + stories) seguindo o design system da @medproflashcards.

## O que essa skill faz

Pega uma questão (texto + imagens) e gera:
- **Carrossel Instagram** (1080×1440, 3:4 orgânico): 4 a 9 slides em formato editorial premium alinhado à skill `/medpro-carrossel`
- **Stories** (1080×1920, opcional): versão enxuta em 5-6 stories respeitando safe zones do IG
- **Cards Anki embutidos**: fundo branco/off, pergunta Inter preta, resposta em **azul cloze `#1F00FF`** com uma palavra-chave sublinhada (estilo screenshot raw do Anki)

## Identidade visual (resumida)

- **Paleta**: navy `#0F2340`, off `#FAFAF7`, cream `#EFE9D9`, red `#C9352B`, gold `#C9A961`, black `#0A0A0A`, cloze blue `#1F00FF`
- **Fontes**: Fraunces (headlines 800-900), Inter (corpo 400-700), Caveat (assinatura "Feito por aprovados")
- **Header em TODOS os slides**: logo MedPro à esquerda + `@medproflashcards` à direita + linha divisória sutil
- **Pontuação como ornamento**: ponto/interrogação gigante em `RED`
- **Referências editoriais**: Bloomberg Businessweek, Osler, NYT Magazine, Granta

## REGRAS DURAS (não negociáveis)

1. **NUNCA usar eyebrow.** Nada de `§ 02 — Tese`, "§ NN — XYZ" no topo de slides, bolinhas vermelhas com texto. Removido em definitivo.
2. **Header em TODOS os slides**: logo MedPro grande à esquerda (140px altura) + `@MedProFlashcards` em JetBrains Mono à direita. **SEM linha divisória.**
3. **Capitalização do handle**: sempre `@MedProFlashcards` em CamelCase (M, P, F maiúsculos). Não usar lowercase.
4. **Sem labels A/B/C/D** em imagens sequenciais. Só quando a questão pede comparação explícita.
5. **Capa**: BANCA + ANO em Fraunces 900 ~190-200px (maior que tudo), pergunta menor em Fraunces 700.
6. **JetBrains Mono** permitida em: (a) handle do header, (b) folio dos cards Anki, (c) badge "FLASHCARD MEDPRO". Mais nada.
7. **LEGENDA SEMPRE VOLTADA PRA VENDA.** Conteúdo no carrossel + venda na legenda. Hook nas 2 primeiras linhas (corte do "...mais") → resumo do caso → agitação do problema/pegadinha → solução (deck) → CTA explícito (link na bio) → sign-off "Feito por aprovados." → 15-25 hashtags. Framework completo em [references/legenda.md](references/legenda.md).

Detalhes completos em [references/design-system.md](references/design-system.md).

## Fluxo de trabalho

### 1. Coletar inputs

A usuária normalmente chega com uma das três situações:
1. Já tem a pasta da prova com PDF/TXT extraído (ex: `prova_unifesp2026/prova_text.txt`)
2. Aponta direto a questão por número ("faz da Q33")
3. Manda o texto da questão na conversa

**Antes de renderizar, confirme com ela:**
- Qual o ano e banca? (vai no canto da capa)
- Qual a alternativa correta? (define o "diagnóstico" e o "manejo")
- Há imagens (TC, RX, fundoscopia, eletro, cultura)? Onde estão?
- Quer só carrossel, ou carrossel + stories?

### 2. Ler o texto e identificar os ganchos

Leia a questão e extraia:
- **Caso clínico** → vira slide "O caso" (6 blocos: PACIENTE, HISTÓRIA, EXAME, LAB, IMAGEM, INTERVENÇÃO)
- **Imagens** → viram material pra capa, slides Anki, e slide de diagnóstico
- **Diagnóstico/conceito-chave** → vira a "cloze" do card Anki principal
- **Conduta** → vira o slide "Manejo" (3-5 passos numerados)
- **Pegadinhas/extras** → viram cards Anki extras ou linhas no manejo

A regra de ouro: **a questão tem que virar um mini-aula visual em 30 segundos de scroll.**

### 3. Escolher os slides do menu

A skill tem 9 tipos de slide disponíveis, mas **NÃO precisa usar todos**. Use só os que fizerem sentido pra questão. Detalhes completos em [references/slide-menu.md](references/slide-menu.md).

Sugestão por complexidade:
- **Questão simples** (1 conceito): capa + caso + 1 Anki + manejo + CTA = 5 slides
- **Questão média** (TC + dx + tx): capa + caso + 2 Anki + dx + manejo + CTA = 7 slides
- **Questão complexa** (várias armadilhas): todos os 9

### 4. Extrair/preparar imagens

Se a questão tem imagens dentro do PDF:
```python
import fitz  # PyMuPDF
doc = fitz.open("prova.pdf")
page = doc[N]  # página da questão
for img in page.get_images(full=True):
    xref = img[0]
    pix = fitz.Pixmap(doc, xref)
    pix.save(f"q##_raw.png")
```

Depois autocrop pra remover margens brancas:
```python
from PIL import Image, ImageChops
im = Image.open("q##_raw.png")
bg = Image.new(im.mode, im.size, (255,255,255))
bbox = ImageChops.difference(im, bg).getbbox()
im.crop(bbox).save("q##_clean.png")
```

### 5. Criar a pasta e copiar templates

```bash
BASE="/Users/marianarocha/Documents/Claude/MedPro Flashcards/Instagram/Posts"
mkdir -p "$BASE/carrossel_<banca><ano>_q##/"
cp ~/.claude/skills/questão-post/assets/render_post_template.py "$BASE/carrossel_<banca><ano>_q##/render_q##.py"
cp ~/.claude/skills/questão-post/assets/render_anki_template.py "$BASE/carrossel_<banca><ano>_q##/render_anki_prints.py"
# (opcional) cp render_stories_template.py se forem fazer stories
```

A pasta `fonts/` é compartilhada — pode dar symlink pra `carrossel_usp2023/fonts` ou copiar.

### 6. Adaptar os templates

Os arquivos em `assets/` são templates funcionais usados em produção. **Não reescreva do zero** — abra o template e troque só o que é específico da questão:

- `slide_capa()`: ano, banca, pergunta, imagens da grade 2×2
- `slide_caso()`: blocos com dados do paciente
- `slide_anki_*()`: troca apenas o texto que vai no print (chama `render_anki_prints.py`)
- `slide_dx()`: imagem principal + 3 bullets (keyword + subtexto)
- `slide_manejo()`: 5 itens numerados (num / TÍTULO / corpo)

O design system completo (paleta, fontes, dimensões) está em [references/design-system.md](references/design-system.md).

### 7. Rodar e validar

```bash
cd "$BASE/carrossel_<banca><ano>_q##"
python3 render_anki_prints.py   # gera os prints dos cards Anki primeiro
python3 render_q##.py            # gera os slides finais
open slide_*.png                  # visualizar pra confirmar com a usuária
```

**Sempre abra os slides** pra ela conferir antes de declarar pronto. Erros comuns:
- Fonte não suporta arrow `→` ou `↑` (Helvetica e Playfair não têm). Solução: trocar por `:` ou texto.
- Imagem cortada por badge sobreposta. Solução: mover label pra fora da imagem (BRAND_BLUE acima dela).
- Texto da pergunta sobrepondo o ano na capa. Solução: quebrar em 2 linhas.

### 8. Stories (se pedido)

Use `render_stories_template.py` como base. Canvas é 1080×1920, mas o IG corta os primeiros 280px (top) e últimos 380px (bottom). **Trabalhe entre y=280 e y=1540.**

Estrutura típica de 5-6 stories:
1. Capa (brand + pergunta + imagem chave grande)
2. Caso (4 blocos compactos)
3. Germe/diagnóstico (achado central + cloze azul gigante)
4. Manejo/conduta (3 passos numerados)
5. CTA (Salve. Compartilha. Revisa. + @handle)

Stories é **mais enxuto** que o carrossel — corte tudo que não couber em 5s de leitura por slide.

## Detalhe importante: imagens pequenas

A função `rounded_image` original usava `thumbnail()` que SÓ REDUZ. Pra escalar pra cima quando a imagem é pequena (ex: cultura 529×505 num canvas 1020 de largura), use:

```python
iw, ih = src_img.size
ratio = min(w / iw, h / ih)
new_size = (int(iw * ratio), int(ih * ratio))
src_img = src_img.resize(new_size, Image.LANCZOS)
```

Já tá corrigido no `render_stories_template.py`.

## Referências completas

- [references/design-system.md](references/design-system.md) — paleta, fontes, layout
- [references/slide-menu.md](references/slide-menu.md) — os 9 tipos de slide com exemplos
- [references/anki-cards.md](references/anki-cards.md) — formato dos cards Anki (CSS real)
- [references/stories-format.md](references/stories-format.md) — safe zones e layout stories

## Templates funcionais

- [assets/render_post_template.py](assets/render_post_template.py) — renderer 9 slides 1080×1350
- [assets/render_stories_template.py](assets/render_stories_template.py) — renderer 6 stories 1080×1920
- [assets/render_anki_template.py](assets/render_anki_template.py) — renderer cards Anki

## Template canônico — Einstein 2026 Q17

**Use sempre como referência** (`Posts/carrossel_einstein2026_q17/`):
- Capa BBW-style com BANCA + ANO gigantes
- Header logo + `@MedProFlashcards` em mono (todos os slides)
- Slides Anki estilo card editorial com badge "FLASHCARD MEDPRO" + cloze inline + botões De novo/Difícil/Bom/Fácil
- Hook navy puro + CTA editorial minimalista (URL como headline)
- Sem eyebrows, sem labels A/B, sem JBMono fora de handle/folio/badge

Os 2 posts anteriores (USP 2023 Q03, UNIFESP 2026 Q33) usavam paleta/fontes antigas e **não são mais referência ativa** — só histórico.

Detalhes completos em [examples/README.md](examples/README.md).
