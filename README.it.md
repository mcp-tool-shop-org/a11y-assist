<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.md">English</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

**Assistenza deterministica per la gestione degli errori delle interfacce a riga di comando (CLI). Funzionalità aggiuntive, basata esclusivamente su comandi "SAFE", guidata da profili.**

---

**La versione 0.4 è non interattiva e deterministica.**
Non sovrascrive mai l'output degli strumenti. Aggiunge solo un blocco di assistenza.

---

## Perché

Quando uno strumento CLI genera un errore, il messaggio di errore è spesso scritto per lo sviluppatore che lo ha creato, e non per la persona che sta cercando di risolvere il problema. Se si utilizza uno screen reader, si ha una vista ridotta o si è sotto stress cognitivo, una serie di messaggi di errore e codici abbreviati non sono di aiuto: sono un ulteriore ostacolo.

**a11y-assist** aggiunge un blocco strutturato per la risoluzione dei problemi a qualsiasi errore di una CLI:

- Associa i suggerimenti all'ID dell'errore originale (quando disponibile).
- Genera piani di risoluzione dei problemi numerati e adattati al profilo.
- Suggerisce solo comandi "SAFE" (solo lettura, test, controlli di stato).
- Indica il livello di affidabilità in modo che l'utente sappia quanto fidarsi del suggerimento.
- Non sovrascrive né nasconde mai l'output originale dello strumento.

Cinque profili di accessibilità sono inclusi: vista ridotta, stress cognitivo, screen reader, dislessia e linguaggio semplice.

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
|---------|-------------|
| `a11y-assist explain --json <path>` | Assistenza con elevata affidabilità da file JSON `cli.error.v0.1`. |
| `a11y-assist triage --stdin` | Assistenza approssimativa da testo CLI non strutturato. |
| `a11y-assist last` | Assistenza dal log più recente (`~/.a11y-assist/last.log`). |
| `a11y-assist ingest <findings.json>` | Importa i risultati da a11y-evidence-engine. |
| `assist-run <cmd> [args...]` | Wrapper che cattura l'output per il comando `last`. |

Tutti i comandi accettano i flag `--profile`, `--json-response` e `--json-out`.

---

## Profili di accessibilità

Utilizzare il flag `--profile` per selezionare un output adattato alle proprie esigenze:

```bash
a11y-assist explain --json message.json --profile screen-reader
```

| Profilo | Vantaggio principale | Numero massimo di passaggi | Adattamenti principali |
|---------|-----------------|-----------|-----------------|
| **lowvision** (default) | Chiarezza visiva | 5 | Etichette chiare, passaggi numerati, comandi "SAFE". |
| **cognitive-load** | Riduzione del carico mentale | 3 | Indicazioni chiare, etichette "Inizio/Avanti/Fine", frasi più brevi. |
| **screen-reader** | Priorità all'audio | 3-5 | Adatto alla sintesi vocale, abbreviazioni espanse, nessuna referenza visiva. |
| **dyslexia** | Riduzione dell'attrito nella lettura | 5 | Etichette esplicite, nessuna enfasi simbolica, spaziatura aggiuntiva. |
| **plain-language** | Massima chiarezza | 4 | Una clausola per frase, struttura semplificata. |

---

## Livelli di affidabilità

| Livello | Significato | Quando |
|-------|---------|------|
| **High** | File JSON `cli.error.v0.1` validato con ID. | Lo strumento emette un output di errore strutturato. |
| **Medium** | Testo non strutturato con "(ID: ...)" rilevabile. | ID dell'errore trovato in testo non strutturato. |
| **Low** | Analisi approssimativa, nessun ID trovato. | Nessun riferimento; i suggerimenti sono euristici. |

L'affidabilità è sempre indicata nell'output. Non aumenta mai durante la trasformazione del profilo.

---

## Garanzie di sicurezza

a11y-assist applica rigidi vincoli di sicurezza durante l'esecuzione tramite il suo sistema di "Profile Guard":

- **Solo comandi "SAFE"** — vengono suggeriti solo comandi di sola lettura, test e controlli di stato.
- **Nessun ID inventato** — gli ID degli errori provengono dall'input o sono assenti; non vengono mai inventati.
- **Nessun contenuto inventato** — i profili riformulano, ma non aggiungono nuove affermazioni fattuali.
- **Affidabilità indicata** — sempre mostrata; può diminuire, ma non aumentare.
- **Solo aggiuntivo** — l'output originale dello strumento non viene mai modificato, nascosto o soppresso.
- **Deterministico** — lo stesso input produce sempre lo stesso output; nessuna chiamata di rete, nessuna casualità.
- **Controllato dal "Guard"** — ogni trasformazione del profilo viene validata rispetto ai vincoli prima della visualizzazione.

---

## Output JSON (CI / Pipelines)

Per l'automazione, utilizzare l'opzione `--json-response` per ottenere un output leggibile dalle macchine:

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
- [a11y-demo-site](https://github.com/mcp-tool-shop-org/a11y-demo-site) - Dimostrazione con workflow CI

---

## Contributi

Consultare il file [CONTRIBUTING.md](CONTRIBUTING.md) per le linee guida.

---

## Sicurezza e ambito dei dati

**Dati accessibili:** errori JSON/test della CLI passati come argomenti (solo lettura), `~/.a11y-assist/last.log` (scritti da `assist-run`), output di assist all'output standard o al percorso specificato con `--json-out`. **Dati NON accessibili:** nessun file al di fuori degli argomenti e dei percorsi di output specificati, nessuna credenziale del sistema operativo, nessun dato del browser. **Nessuna connessione in uscita**: tutte le elaborazioni sono locali e deterministiche. **Nessun dato di telemetria** viene raccolto o trasmesso.

## Licenza

[MIT](LICENSE)

---

Creato da <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
