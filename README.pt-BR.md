<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.md">English</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/a11y-assist/readme.png" alt="a11y-assist" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/a11y-assist/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/a11y-assist/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/a11y-assist/"><img src="https://img.shields.io/pypi/v/a11y-assist?color=blue" alt="PyPI"></a>
  <a href="https://codecov.io/gh/mcp-tool-shop-org/a11y-assist"><img src="https://codecov.io/gh/mcp-tool-shop-org/a11y-assist/branch/main/graph/badge.svg" alt="Coverage"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/a11y-assist/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

**Assistência determinística para acessibilidade em caso de falhas na interface de linha de comando (CLI). Aditiva, exclusiva para comandos SAFE, e orientada por perfil.**

---

**A versão 0.4 é não interativa e determinística.**
Ela nunca reescreve a saída da ferramenta. Ela apenas adiciona um bloco de ASSISTÊNCIA.

---

## Por que?

Quando uma ferramenta de linha de comando falha, a mensagem de erro geralmente é escrita para o desenvolvedor que a criou, e não para a pessoa que está tentando resolver o problema. Se você usa um leitor de tela, tem baixa visão ou está sob carga cognitiva, uma série de mensagens de erro e códigos abreviados não são úteis – são apenas mais um obstáculo.

O **a11y-assist** adiciona um bloco estruturado de recuperação a qualquer falha na linha de comando:

- Vincula as sugestões ao ID de erro original (quando disponível).
- Gera planos de recuperação numerados e adaptados ao perfil.
- Sugere apenas comandos SAFE (somente leitura, teste, verificação de status).
- Informa o nível de confiança para que o usuário saiba o quão confiável é a sugestão.
- Nunca reescreve ou oculta a saída original da ferramenta.

Cinco perfis de acessibilidade são fornecidos por padrão: baixa visão, carga cognitiva, leitor de tela, dislexia e linguagem simples.

---

## Instalação

```bash
pip install a11y-assist
```

Requer Python 3.11 ou superior.

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
|---------|-------------|
| `a11y-assist explain --json <path>` | Assistência com alta confiança a partir de JSON `cli.error.v0.1`. |
| `a11y-assist triage --stdin` | Assistência com o máximo de esforço a partir de texto bruto da linha de comando. |
| `a11y-assist last` | Assistência a partir do último log capturado (`~/.a11y-assist/last.log`). |
| `a11y-assist ingest <findings.json>` | Importa resultados do a11y-evidence-engine. |
| `assist-run <cmd> [args...]` | Wrapper que captura a saída para o comando `last`. |

Todos os comandos aceitam as flags `--profile`, `--json-response` e `--json-out`.

---

## Perfis de Acessibilidade

Use a flag `--profile` para selecionar a saída adaptada às suas necessidades:

```bash
a11y-assist explain --json message.json --profile screen-reader
```

| Perfil | Benefício principal | Número máximo de etapas | Adaptações principais |
|---------|-----------------|-----------|-----------------|
| **lowvision** (default) | Clareza visual | 5 | Rótulos claros, etapas numeradas, comandos SAFE. |
| **cognitive-load** | Redução da carga mental | 3 | Linha de objetivo, rótulos "Próximo/Anterior", frases mais curtas. |
| **screen-reader** | Prioridade para áudio | 3-5 | Compatível com TTS, abreviações expandidas, sem referências visuais. |
| **dyslexia** | Redução do esforço de leitura | 5 | Rótulos explícitos, sem ênfase simbólica, espaçamento extra. |
| **plain-language** | Máxima clareza | 4 | Uma cláusula por frase, estrutura simplificada. |

---

## Níveis de Confiança

| Nível | Significado | Quando |
|-------|---------|------|
| **High** | JSON `cli.error.v0.1` validado com ID. | A ferramenta emite uma saída de erro estruturada. |
| **Medium** | Texto bruto com "(ID: ...)" detectável. | ID de erro encontrado em texto não estruturado. |
| **Low** | Análise com o máximo de esforço, sem ID encontrado. | Sem referência; as sugestões são heurísticas. |

A confiança é sempre exibida na saída. Ela nunca aumenta durante a transformação do perfil.

---

## Garantias de Segurança

O a11y-assist impõe invariantes de segurança rigorosos em tempo de execução por meio de seu sistema de Profile Guard:

- **Apenas comandos SAFE** — são sugeridos apenas comandos de somente leitura, teste e verificação de status.
- **Sem IDs inventados** — os IDs de erro vêm da entrada ou estão ausentes; nunca são fabricados.
- **Sem conteúdo inventado** — os perfis reformulam, mas nunca adicionam novas afirmações factuais.
- **Confiança divulgada** — sempre exibida; pode diminuir, mas nunca aumentar.
- **Apenas aditivo** — a saída original da ferramenta nunca é modificada, ocultada ou suprimida.
- **Determinístico** — a mesma entrada sempre produz a mesma saída; sem chamadas de rede, sem aleatoriedade.
- **Verificado por guardião** — todas as transformações de perfil são validadas em relação a invariantes antes de serem renderizadas.

---

## Saída JSON (CI / Pipelines)

Para automação, utilize a opção `--json-response` para obter uma saída legível por máquina:

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

Consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para obter as diretrizes.

---

## Segurança e Escopo de Dados

**Dados acessados:** JSON/texto de erro da linha de comando, passados como argumentos (somente leitura), `~/.a11y-assist/last.log` (escrito por `assist-run`), saída do assistente para a saída padrão ou para o caminho especificado com `--json-out`. **Dados NÃO acessados:** nenhum arquivo fora dos argumentos e caminhos de saída especificados, nenhuma credencial do sistema operacional, nenhum dado do navegador. **Não há tráfego de rede** – todo o processamento é local e determinístico. **Nenhuma telemetria** é coletada ou enviada.

## Licença

[MIT](LICENSE)

---

Desenvolvido por <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
