# Exemplos de posts

## 🎯 Modelo canônico — Einstein 2026 Q17

**Caso**: Abdome agudo perfurativo (úlcera péptica por binge drinking + choque pós-TC).
**Gabarito**: A (laparotomia exploradora) — pegadinha clássica vs. pancreatite.
**Pasta**: `Posts/carrossel_einstein2026_q17/`

### Por que este é o template canônico

Foi o primeiro post a fechar **todo o sistema visual** definitivo:

1. **Capa estilo BBW**: "EINSTEIN 2026:" gigante (Fraunces 900, ~195px, preto + dois pontos vermelhos) + pergunta menor (Fraunces 700) + ponto interrogação RED gigante + grid 2 imagens lado a lado (sem labels A/B, só conteúdo)
2. **Header padronizado**: logo grande à esquerda + `@MedProFlashcards` em JetBrains Mono à direita, sem linha divisória — em TODOS os slides
3. **Sem eyebrows** em lugar nenhum (regra dura)
4. **Slides Anki em estilo card editorial**: fundo cream com textura paper → card off-white com sombra → card branco interno com border NAVY 2px + badge "FLASHCARD MEDPRO" flutuante + pergunta Arial com cloze inline + extra italic + imagem opcional + **botões De novo/Difícil/Bom/Fácil sempre presentes** + footer "Card curto. Resposta cirúrgica." + folio mono
5. **Diagnóstico + Manejo** em fundo off com textura
6. **Hook navy puro** sem textura (preserva tom da paleta)
7. **CTA editorial minimalista** (slide 9): lead reflexivo + URL como headline + prova social sutil + Caveat signature

### Estrutura dos 9 slides

| # | Slide | Background | Função |
|---|-------|-----------|--------|
| 1 | Capa | cream + textura | Brand gigante + pergunta + grid 2 TCs |
| 2 | O caso | off + textura | 5 blocos com labels GOLD |
| 3 | Hook | navy puro | "Saberia responder agora?" + aspas RED gigantes |
| 4 | Anki achado | cream com card off + textura | Pergunta + imagem + cloze "Pneumoperitônio." sublinhada |
| 5 | Anki causa | cream com card off + textura | Pergunta + cloze "úlcera péptica perfurada" sublinhada |
| 6 | Anki extra (DDx) | cream com card off + textura | Pergunta + cloze "síndrome de Boerhaave" sublinhada |
| 7 | Diagnóstico | off + textura | Título grande + TC + 3 bullets gold (keyword + subtexto) |
| 8 | Manejo | off + textura | 5 itens numerados (gold + Inter weight 700 + body Inter) |
| 9 | CTA | navy puro | Lead reflexivo + URL editorial + prova social + Caveat sig |

### Configurações finais aprovadas

- Canvas: **1080×1440** (3:4 orgânico)
- Paleta: navy `#0F2340` · cream `#EFE9D9` · off `#FAFAF7` · red `#C9352B` · gold `#C9A961` · cloze `#1F00FF`
- Fontes: **Fraunces** (headlines), **Inter** (corpo), **Arial** (dentro dos cards Anki), **Caveat** (assinatura), **JetBrains Mono** (handle/folio/badge apenas)
- Header: logo 140px + handle JBMono 32px (padrão em todos os slides)
- Textura paper: blend 40-42% em fundos claros, sem textura no navy
- Cards Anki: arial 32 (pergunta) + 22 (extra italic), cloze azul bold sublinhado, botões anki sempre presentes

---

## Outros posts produzidos antes do template fechar

### USP-SP 2023 Q03 — Abdome agudo perfurativo

Primeira tentativa do template. **Não usar como referência ativa** — o design system mudou completamente. Está mantido apenas como histórico.

**Pasta**: `Posts/carrossel_usp2023/q03_abdome_perfurativo/`

### UNIFESP 2026 Q33 — Abscesso pós-CCE + Pseudomonas MDR

Segunda iteração, ainda com paleta antiga (Playfair + DM Sans + papel aquarela + neurônio). Tem versão Stories. **Não usar como referência ativa.**

**Pasta**: `Posts/carrossel_unifesp2026_q33/`

---

## Como aplicar o template em uma questão nova

1. Copiar `~/.claude/skills/questão-post/assets/render_post_template.py` pra pasta nova
2. Copiar `~/.claude/skills/questão-post/assets/render_anki_template.py` pra pasta nova
3. Trocar `BASE` no topo pra apontar pra pasta da questão
4. Adaptar:
   - `slide_capa()`: banca, ano, pergunta, imagens
   - `slide_caso()`: blocos com paciente/história/exame/lab
   - `slide_4/5/6()`: 3 cards Anki (cloze + extra + imagem opcional)
   - `slide_dx()`: título + imagem + 3 bullets
   - `slide_manejo()`: 5 itens numerados
5. Slides 3 (hook) e 9 (CTA) raramente precisam de mudança
6. Rodar `render_anki_prints.py` primeiro, depois `render_q##.py`
