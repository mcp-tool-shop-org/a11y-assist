<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  
            <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/a11y-assist/readme.png"
           alt="a11y-assist" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/a11y-assist/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/a11y-assist/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/a11y-assist/"><img src="https://img.shields.io/pypi/v/a11y-assist?color=blue" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/a11y-assist/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

**Assistência determinística para falhas na interface de linha de comando (CLI). Aditiva, exclusiva para comandos SAFE, orientada por perfil.**

---

**A versão 0.4 é não interativa e determinística.**
Ela nunca sobrescreve a saída da ferramenta. Ela apenas adiciona um bloco de ASSISTÊNCIA.

---

## Por que?

Quando uma ferramenta de linha de comando falha, a mensagem de erro geralmente é escrita para o desenvolvedor que a criou, e não para a pessoa que está tentando se recuperar do erro. Se você usa um leitor de tela, tem baixa visão ou está sob carga cognitiva, uma série de rastreamentos de pilha e códigos abreviados não são úteis – são apenas mais um obstáculo.

O **a11y-assist** adiciona um bloco de recuperação estruturado a qualquer falha na linha de comando:

- Vincula as sugestões ao ID de erro original (quando disponível).
- Gera planos de recuperação numerados e adaptados ao perfil.
- Sugere apenas comandos SAFE (somente leitura, teste, verificações de status).
- Informa o nível de confiança para que o usuário saiba o quanto pode confiar na sugestão.
- Nunca sobrescreve ou oculta a saída original da ferramenta.

Cinco perfis de acessibilidade são fornecidos por padrão: baixa visão, carga cognitiva, leitor de tela, dislexia e linguagem simples.

---

## Instalação

```bash
pip install a11y-assist
```

Requer Python 3.11 ou posterior.

---

## Início rápido

```bash
# 1. Wrap any command — a11y-assist captures its output
assist-run some-tool do-thing

# 2. If it fails, get accessible recovery guidance
a11y-assist last

# 3. Switch profiles to match your needs
a11y-assist last --profile cognitive-load
```

---

## Comandos

| Comando | Descrição |
| --------- | ------------- |
| `a11y-assist explain --json <path>` | Assistência com alta confiança a partir de JSON `cli.error.v0.1` |
| `a11y-assist triage --stdin` | Assistência com o máximo de esforço a partir de texto bruto da linha de comando |
| `a11y-assist last` | Assistência a partir do último log capturado (`~/.a11y-assist/last.log`) |
| `a11y-assist ingest <findings.json>` | Importa resultados do a11y-evidence-engine |
| `assist-run <cmd> [args...]` | Wrapper que captura a saída para o comando `last` |

Todos os comandos aceitam as flags `--profile`, `--json-response` e `--json-out`.

---

## Perfis de Acessibilidade

Use a flag `--profile` para selecionar a saída adaptada às suas necessidades:

```bash
a11y-assist explain --json message.json --profile screen-reader
```

| Perfil | Benefício principal | Número máximo de etapas | Adaptações principais |
| --------- | ----------------- | ----------- | ----------------- |
| **lowvision** (padrão) | Clareza visual | 5 | Rótulos claros, etapas numeradas, comandos SAFE |
| **cognitive-load** | Redução de etapas mentais | 3 | Linha de objetivo, rótulos "Primeiro/Próximo/Último", frases mais curtas |
| **screen-reader** | Prioridade para áudio | 3-5 | Compatível com TTS, abreviações expandidas, sem referências visuais |
| **dyslexia** | Redução do atrito na leitura | 5 | Rótulos explícitos, sem ênfase simbólica, espaçamento extra |
| **plain-language** | Máxima clareza | 4 | Uma cláusula por frase, estrutura simplificada |

---

## Níveis de Confiança

| Level | Significado | When |
| ------- | --------- | ------ |
| **High** | JSON `cli.error.v0.1` validado com ID | A ferramenta emite uma saída de erro estruturada |
| **Medium** | Texto bruto com `(ID: ...)` detectável | ID de erro encontrado em texto não estruturado |
| **Low** | Análise com o máximo de esforço, nenhum ID encontrado | Sem âncora; as sugestões são heurísticas |

A confiança é sempre informada na saída. Ela nunca aumenta durante a transformação do perfil.

---

## Garantias de Segurança

O a11y-assist impõe invariantes de segurança rigorosas em tempo de execução por meio de seu sistema de Profile Guard:

- **Comandos "SAFE"** — Apenas são sugeridos comandos de leitura, testes simulados e verificações de status.
- **Sem IDs inventados** — Os códigos de erro são provenientes da entrada ou estão ausentes; nunca são fabricados.
- **Sem conteúdo inventado** — Os perfis reformulam, mas nunca adicionam novas informações factuais.
- **Confiança divulgada** — Sempre exibida; pode diminuir, mas nunca aumentar.
- **Apenas aditivo** — A saída original da ferramenta nunca é modificada, ocultada ou suprimida.
- **Determinístico** — A mesma entrada sempre produz a mesma saída; não há chamadas de rede, nem aleatoriedade.
- **Verificado por "guard"** — Cada transformação de perfil é validada em relação a invariantes antes de ser renderizada.

---

## Saída JSON (CI / Pipelines)

Para automação, use `--json-response` para obter uma saída legível por máquina:

```bash
# JSON to stdout (instead of rendered text)
a11y-assist explain --json error.json --json-response

# JSON to file + rendered text to stdout
a11y-assist explain --json error.json --json-out assist.json
```

---

## Relacionado

- [a11y-evidence-engine](https://github.com/mcp-tool-shop-org/a11y-evidence-engine) - Motor de evidências sem interface.
- [a11y-mcp-tools](https://github.com/mcp-tool-shop-org/a11y-mcp-tools) - Ferramentas MCP para acessibilidade.
- [a11y-demo-site](https://github.com/mcp-tool-shop-org/a11y-demo-site) - Demonstração com fluxos de trabalho de CI.

---

## Contribuições

Consulte [CONTRIBUTING.md](CONTRIBUTING.md) para obter diretrizes.

---

## Licença

[MIT](LICENSE)
