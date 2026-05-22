# Cards Anki — template editorial /medpro-carrossel

Os slides de card Anki seguem **EXATAMENTE** o template `SlideAnkiCard` da skill `/medpro-carrossel`. **NÃO inventar variação.**

## Anatomia do slide

```
┌──────────────────────────────────────────────┐
│ [fundo CREAM com paper texture]              │
│  ┌────────────────────────────────────────┐  │
│  │ [card OFF com shadow + border sutil]    │  │
│  │                                          │  │
│  │  Headline Fraunces 96 NAVY              │  │
│  │  "O achado."                            │  │
│  │                                          │  │
│  │  ┌──────────────────────────────────┐   │  │
│  │  │ ▸FLASHCARD MEDPRO◂  ← badge      │   │  │
│  │  │ ┌────────────────────────────┐    │   │  │
│  │  │ │ [card BRANCO interno]      │    │   │  │
│  │  │ │  border navy 2px           │    │   │  │
│  │  │ │                            │    │   │  │
│  │  │ │  Pergunta Helvetica 32     │    │   │  │
│  │  │ │  com [CLOZE azul] inline   │    │   │  │
│  │  │ │                            │    │   │  │
│  │  │ │  Extra italic cinza 22     │    │   │  │
│  │  │ │                            │    │   │  │
│  │  │ │  [imagem opcional]         │    │   │  │
│  │  │ └────────────────────────────┘    │   │  │
│  │  └──────────────────────────────────┘   │  │
│  │                                          │  │
│  │  Card curto. Resposta cirúrgica.        │  │
│  │                          PADRÃO MEDPRO   │  │
│  │                          DIRETO AO PONTO │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

## JSX de referência (canônico)

```jsx
const Cloze = ({ children, underlined = false }) => {
  const baseStyle = { color: "#0000FF", fontWeight: "bold" };
  if (underlined) return <u style={baseStyle}>{children}</u>;
  return <span style={baseStyle}>{children}</span>;
};

const SlideAnkiCard = ({ headline, pergunta, extra }) =>
  <div className="slide paper-light s-anki-card"
       style={{ background: "var(--cream)", padding: 0 }}>
    <div style={{
      position: "absolute", inset: 48,
      background: "var(--off)",
      borderRadius: 28,
      boxShadow: "0 8px 40px rgba(15,35,64,0.12)",
      border: "1px solid rgba(15,35,64,0.10)",
      display: "flex", flexDirection: "column",
      overflow: "hidden",
    }}>
      {/* Headline */}
      <h2 style={{
        fontFamily: '"Fraunces", serif',
        fontSize: 96, fontWeight: 900,
        lineHeight: 0.92, letterSpacing: "-0.04em",
        color: "var(--navy)",
        margin: 0, padding: "36px 52px 0",
      }}>{headline}</h2>

      {/* Card flashcard interno */}
      <div style={{
        margin: "48px 40px 0",
        position: "relative",
        border: "2px solid var(--navy)",
        borderRadius: 18,
        padding: "32px 40px",
        backgroundColor: "#FFFFFF",
      }}>
        {/* Badge flutuante */}
        <div style={{
          position: "absolute", top: -12, left: 32,
          backgroundColor: "#FFFFFF",
          padding: "0 12px",
          fontFamily: '"JetBrains Mono", monospace',
          fontSize: 15, letterSpacing: "0.32em",
          textTransform: "uppercase", fontWeight: 600,
          display: "flex", gap: 10,
        }}>
          <span style={{ color: "var(--red)" }}>Flashcard</span>
          <span style={{ color: "var(--navy)" }}>MedPro</span>
        </div>
        {/* Pergunta (com Cloze inline) */}
        <div style={{
          fontFamily: "Helvetica, Arial, sans-serif",
          fontWeight: 400, fontSize: 32, lineHeight: 1.45,
          color: "#000", textAlign: "center",
        }}>{pergunta}</div>
        {/* Extra italic */}
        {extra && <div style={{
          fontFamily: "Helvetica, Arial, sans-serif",
          fontSize: 22, lineHeight: 1.4, fontStyle: "italic",
          color: "#555", textAlign: "center", marginTop: 18,
        }}>{extra}</div>}
        {/* Imagem opcional */}
        <img src={IMG.anki} style={{
          display: "block", width: "100%", margin: "24px auto 0",
        }} />
      </div>

      <div style={{ flex: 1 }} />

      {/* Footer */}
      <div style={{
        padding: "0 52px 36px",
        display: "flex", justifyContent: "space-between",
        alignItems: "flex-end",
      }}>
        <div style={{ fontFamily: '"Fraunces", serif', fontSize: 28, color: "var(--navy)" }}>
          <b>Card curto.</b>{" "}
          <em style={{ color: "var(--red)", fontStyle: "italic" }}>Resposta cirúrgica.</em>
        </div>
        <div style={{
          fontFamily: '"JetBrains Mono", monospace',
          fontSize: 20, letterSpacing: "0.24em",
          color: "rgba(15,35,64,0.55)",
          textTransform: "uppercase", textAlign: "right",
        }}>
          PADRÃO MEDPRO<br />DIRETO AO PONTO
        </div>
      </div>
    </div>
  </div>;
```

## Spec de implementação Python (PIL)

A função `slide_anki_card(headline, pergunta_segments, extra=None, tc_image=None, slide_filename)` em `render_post_template.py` reproduz fielmente o JSX:

### Parâmetros

- **headline** (str): título do slide ("O achado.", "A causa.", "Outro DDx.")
- **pergunta_segments** (list of tuples): `[(texto, is_cloze, underlined), ...]` — permite cloze inline na pergunta. Exemplo:
  ```python
  [
    ("TC de abdome com ar livre subdiafragmático: ", False, False),
    ("Pneumoperitônio.", True, True),
  ]
  ```
- **extra** (str, opcional): texto italic cinza embaixo da pergunta
- **tc_image** (str, opcional): path da imagem (TC, RX, etc.) renderizada dentro do card

### Detalhes técnicos

- Canvas 1080×1440, fundo cream com paper texture
- Card off em `inset 48` (= x=48, y=48, w=984, h=1344)
- Sombra Gaussian blur (`radius=20, alpha=50`) abaixo do card
- Border cinza-navy sutil
- Headline Fraunces 96 weight 900 NAVY em y=card_y+60 (60px de pad pra dar respiro pra Fraunces ascender)
- Card interno branco com border NAVY 2px, radius 18
- Badge "FLASHCARD MEDPRO" em JetBrains Mono 15 weight 600 tracking ~5px, "FLASHCARD" em RED, "MEDPRO" em NAVY, posicionado em `top=-12, left=32` do card interno (sobrepondo a borda superior)
- Pergunta Helvetica 32 centralizada com cloze azul (`#0000FF`) bold opcionalmente sublinhada
- Extra Helvetica italic 22, color `#555`
- Imagem opcional ocupando 100% da largura do card interno
- Footer em `padding 0 52px 36px`:
  - Esquerda: "Card curto. Resposta cirúrgica." (Fraunces 28, "Card curto." NAVY weight 700, "Resposta cirúrgica." RED italic)
  - Direita: "PADRÃO MEDPRO\nDIRETO AO PONTO" JetBrains Mono 20 weight 500, navy ~55% alpha, tracking 4px

## Cloze — quando sublinhar?

- **Sublinhar (`underlined=True`)**: a palavra-chave SEMÂNTICA da resposta. Geralmente a resposta inteira ou o termo nuclear.
- **Não sublinhar**: pontuação, conectivos, palavras de apoio.

Exemplos:

```python
# Resposta inteira como cloze sublinhada
("Pneumoperitônio.", True, True)

# Frase com termo médio sublinhado
("síndrome de Boerhaave.", True, True)  # underline a frase toda

# Cloze sem sublinhado (palavra-chave inferida)
("úlcera péptica perfurada.", True, True)
```

## Caracteres não suportados

Helvetica NÃO renderiza `→` `↑` `←` `↓`. Substitua por `:`, `+`, palavra ("aumenta", "leva a").

Exemplos:
- ❌ "Vômitos forçados → Boerhaave"
- ✅ "Vômitos forçados: Boerhaave"
- ✅ "Vômitos forçados + Boerhaave"
