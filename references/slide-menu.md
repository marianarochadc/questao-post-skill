# Menu de slides

A skill tem 9 tipos de slide disponíveis. **NÃO é ordem fixa nem precisa todos**. Use só os que fizerem sentido pra questão.

## 1. Capa

**Quando**: sempre — é o slide 1.

**Estrutura**:
- "BANCA-UF," (Playfair 150-170) e "ANO." (Playfair 96-120, BRAND_BLUE)
- Pergunta hook: "Dx em 2 linhas?" ou "Qual a conduta?"
- Linha horizontal
- Grade 2×2 das imagens da questão (TCs com labels A/B/C/D), OU
- Imagem única grande centralizada (quando só tem 1 — ex: cultura, eletrocardiograma)

**Variações**:
- Se a questão tem 4+ imagens → grade 2×2 com labels
- Se tem 1-2 imagens → imagem grande com label externo "TC ABDOME" ou "ECG"
- Se não tem imagem → texto maior, branding ainda maior

## 2. O caso

**Quando**: sempre que a questão tem história clínica relevante (95% das vezes).

**Estrutura**: 4-6 blocos com label BRAND_BLUE + texto INK_DARK.

Labels típicos:
- **PACIENTE** — idade, sexo, comorbidades
- **HISTÓRIA** — quadro atual, tempo de evolução
- **EXAME** — sinais relevantes
- **LAB** — só os exames-chave (não todos)
- **IMAGEM** — descrição em 1 linha do achado
- **INTERVENÇÃO** — o que já foi feito até agora

**Não copie a questão na íntegra** — destila pra ~60 palavras totais.

## 3. Hook

**Quando**: opcional. Use pra criar suspense entre o caso e a resposta.

**Estrutura**: fundo NAVY + frase grande Playfair PAPER, tipo:
- "Saberia responder agora?"
- "E aí, qual a sua resposta?"
- "Pegou a sutileza?"

Slide curto, alta densidade visual, baixa densidade textual.

## 4. Card Anki — imagem

**Quando**: a questão tem um ACHADO DE IMAGEM patognomônico (pneumoperitônio, fundoscopia diabética, ECG STEMI, cultura MDR).

**Estrutura**: print do flashcard com:
- Pergunta no topo (preto, Helvetica regular)
- Imagem do achado no meio
- Resposta cloze azul bold
- Extra italic cinza embaixo
- Botões De novo/Difícil/Bom/Fácil abaixo

Renderizado em `render_anki_prints.py`, embutido no slide com `paste_anki_print()`.

## 5. Card Anki — conexão

**Quando**: precisa amarrar **achado → causa** ou **germe → ATB**.

**Estrutura**: card só-texto:
- "Abscesso pós-CCE → cobertura empírica?"
- Resposta: "Piperacilina-tazobactam OU Meropenem"

Mais largo que o card-imagem (target_w=780 vs 680).

## 6. EXTRA — Card Anki

**Quando**: tem uma curiosidade/sinal/pegadinha que vale a pena destacar.

Ex: "Sinal de Jobert" no abdome perfurativo, "ESBL ≠ MDR Pseudomonas", "ceftazidima-avibactam é pra KPC".

Mesmo formato do anterior, mas com label "EXTRA" navy no topo.

## 7. Diagnóstico

**Quando**: a questão tem um diagnóstico final claro que merece destaque.

**Estrutura**:
- Título grande Playfair ("Pneumoperitônio.")
- Subtítulo Playfair menor ("Abdome agudo perfurativo.")
- Imagem central da prova
- 3 bullets à direita ou abaixo:
  - **KEYWORD** (BRAND_BLUE bold) + subtexto explicativo
  - Ex: "**UC perfurada** — causa #1 em adultos."

## 8. Manejo

**Quando**: a questão é prática (de conduta) ou o dx implica intervenção.

**Estrutura**: 5 itens numerados com:
- Número grande Playfair BRAND_BLUE (01, 02, 03, 04, 05)
- TÍTULO DM Sans 800 NAVY
- Corpo DM Sans 500 INK_DARK em 1-2 linhas

Ex:
```
01  DRENAR
    Percutânea guiada por imagem.

02  CULTURA
    Orienta o ATB direcionado.

03  ATB
    Pipe-tazo ou meropenem em dose máxima.
```

## 9. CTA

**Quando**: sempre — é o slide final.

**Estrutura**:
- Fundo NAVY
- "Salve. Compartilha. Revisa." em Playfair gigante (180+), Revisa em BRAND_BLUE
- Linha horizontal
- Texto curto explicando o deck
- "@medproflashcards" em Playfair bem grande no canto inferior

## Combos típicos

### Carrossel mínimo (5 slides)
1. Capa
2. Caso
4. Anki (imagem)
8. Manejo
9. CTA

### Carrossel padrão (7 slides)
1. Capa
2. Caso
4. Anki imagem
5. Anki conexão
7. Diagnóstico
8. Manejo
9. CTA

### Carrossel completo (9 slides)
Todos os 9, na ordem da lista.

### Stories enxutos (5-6)
1. Capa (brand + pergunta + imagem grande)
2. Caso (4 blocos compactos)
3. Achado/germe (cloze gigante)
4. ATB/conduta-chave (pills)
5. Manejo (3 passos)
6. CTA
