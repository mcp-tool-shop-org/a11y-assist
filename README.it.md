<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/a11y-assist/main/assets/logo-a11y-assist.png" alt="a11y-assist" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/a11y-assist/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/a11y-assist/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/a11y-assist/"><img src="https://img.shields.io/pypi/v/a11y-assist?color=blue" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/a11y-assist/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

**Assistenza deterministica per la gestione degli errori delle interfacce a riga di comando (CLI). Approccio incrementale, esclusivamente SAFE, basato su profili.**

---

**La versione 0.4 è non interattiva e deterministica.**
Non sovrascrive mai l'output degli strumenti. Aggiunge solo un blocco di ASSISTENZA.

---

## Perché

Quando uno strumento CLI genera un errore, il messaggio di errore è spesso scritto per lo sviluppatore che lo ha creato, e non per la persona che sta cercando di risolvere il problema. Se si utilizza uno screen reader, si ha una vista limitata o si è sotto stress cognitivo, una serie di messaggi di errore e codici abbreviati non sono di aiuto: sono un ulteriore ostacolo.

**a11y-assist** aggiunge un blocco strutturato per la risoluzione dei problemi a qualsiasi errore di CLI:

- Associa i suggerimenti all'ID dell'errore originale (quando disponibile).
- Genera piani di risoluzione dei problemi numerati e adattati al profilo.
- Suggerisce solo comandi SAFE (solo lettura, test, controlli di stato).
- Indica il livello di affidabilità in modo che l'utente sappia quanto fidarsi del suggerimento.
- Non sovrascrive né nasconde mai l'output originale dello strumento.

Cinque profili di accessibilità sono inclusi: vista ridotta, carico cognitivo, screen reader, dislessia e linguaggio semplice.

---

## Installazione

```bash
pip install a11y-assist
```

Richiede Python 3.11 o versioni successive.

---

## Guida rapida

```bash
# 1. Wrap any command — a11y-assist captures its output
assist-run some-tool do-thing

# 2. If it fails, get accessible recovery guidance
a11y-assist last

# 3. Switch profiles to match your needs
a11y-assist last --profile cognitive-load
```

---

## Comandi

| Comando | Descrizione |
| --------- | ------------- |
| `a11y-assist explain --json <path>` | Assistenza da file JSON `cli.error.v0.1` con alta affidabilità. |
| `a11y-assist triage --stdin` | Assistenza approssimativa da testo CLI grezzo. |
| `a11y-assist last` | Assistenza dal log più recente (`~/.a11y-assist/last.log`). |
| `a11y-assist ingest <findings.json>` | Importazione di risultati da a11y-evidence-engine. |
| `assist-run <cmd> [args...]` | Wrapper che cattura l'output per il comando `last`. |

Tutti i comandi accettano i flag `--profile`, `--json-response` e `--json-out`.

---

## Profili di accessibilità

Utilizzare il flag `--profile` per selezionare un output adattato alle proprie esigenze:

```bash
a11y-assist explain --json message.json --profile screen-reader
```

| Profilo | Vantaggio principale | Numero massimo di passaggi | Adattamenti principali |
| --------- | ----------------- | ----------- | ----------------- |
| **lowvision** (predefinito) | Chiarezza visiva | 5 | Etichette chiare, passaggi numerati, comandi SAFE. |
| **cognitive-load** | Riduzione del carico mentale | 3 | Indicazioni chiare, etichette "Inizio/Avanti/Fine", frasi più brevi. |
| **screen-reader** | Priorità all'audio | 3-5 | Compatibile con la sintesi vocale, abbreviazioni espanse, nessuna referenza visiva. |
| **dyslexia** | Riduzione delle difficoltà di lettura | 5 | Etichette esplicite, nessuna enfasi simbolica, spaziatura aggiuntiva. |
| **plain-language** | Massima chiarezza | 4 | Una clausola per frase, struttura semplificata. |

---

## Livelli di affidabilità

| Level | Significato | When |
| ------- | --------- | ------ |
| **High** | File JSON `cli.error.v0.1` validato con ID. | Lo strumento emette un output di errore strutturato. |
| **Medium** | Testo grezzo con rilevamento di `(ID: ...)` | ID dell'errore trovato in testo non strutturato. |
| **Low** | Analisi approssimativa, nessun ID trovato. | Nessun riferimento; i suggerimenti sono euristici. |

L'affidabilità è sempre indicata nell'output. Non aumenta durante la trasformazione del profilo.

---

## Garanzie di sicurezza

a11y-assist applica rigidi vincoli di sicurezza durante l'esecuzione tramite il suo sistema di Profile Guard:

- **Comandi solo in modalità "SAFE"**: vengono suggeriti solo comandi di sola lettura, test preliminari e controlli di stato.
- **Nessun ID inventato**: gli ID degli errori provengono dall'input o sono assenti; non vengono mai creati artificialmente.
- **Nessun contenuto inventato**: i profili riformulano le informazioni, ma non aggiungono nuove affermazioni fattuali.
- **Livello di confidenza dichiarato**: viene sempre mostrato; può diminuire, ma non aumentare.
- **Solo aggiunte**: l'output dello strumento originale non viene mai modificato, nascosto o soppresso.
- **Deterministico**: lo stesso input produce sempre lo stesso output; non ci sono chiamate di rete, né elementi casuali.
- **Controllato tramite "guard"**: ogni trasformazione del profilo viene validata rispetto a vincoli predefiniti prima di essere visualizzata.

---

## Output JSON (CI / Pipeline)

Per l'automazione, utilizzare `--json-response` per ottenere un output leggibile dalle macchine:

```bash
# JSON to stdout (instead of rendered text)
a11y-assist explain --json error.json --json-response

# JSON to file + rendered text to stdout
a11y-assist explain --json error.json --json-out assist.json
```

---

## Correlati

- [a11y-evidence-engine](https://github.com/mcp-tool-shop-org/a11y-evidence-engine) - Motore di analisi headless
- [a11y-mcp-tools](https://github.com/mcp-tool-shop-org/a11y-mcp-tools) - Strumenti MCP per l'accessibilità
- [a11y-demo-site](https://github.com/mcp-tool-shop-org/a11y-demo-site) - Dimostrazione con flussi di lavoro CI

---

## Contributi

Consultare [CONTRIBUTING.md](CONTRIBUTING.md) per le linee guida.

---

## Licenza

[MIT](LICENSE)
