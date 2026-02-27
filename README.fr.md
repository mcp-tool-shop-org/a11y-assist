<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.md">English</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

**Assistance déterministe pour l'accessibilité en cas d'échec des interfaces en ligne de commande. Ajout, uniquement des commandes SÛRES, basée sur des profils.**

---

**La version 0.4 est non interactive et déterministe.**
Elle ne modifie jamais la sortie des outils. Elle ajoute uniquement un bloc d'ASSISTANCE.

---

## Pourquoi ?

Lorsqu'un outil d'interface en ligne de commande échoue, le message d'erreur est généralement rédigé pour le développeur qui l'a créé, et non pour la personne qui essaie de résoudre le problème. Si vous utilisez un lecteur d'écran, si vous avez une déficience visuelle ou si vous êtes en état de stress cognitif, une série de messages d'erreur et de codes abrégés ne sont pas une aide ; c'est un obstacle supplémentaire.

**a11y-assist** ajoute un bloc de récupération structuré à tout échec d'interface en ligne de commande :

- Les suggestions sont liées à l'ID d'erreur d'origine (lorsqu'il est disponible).
- Elle génère des plans de récupération numérotés et adaptés au profil.
- Elle ne propose que des commandes SÛRES (lecture seule, exécution de test, vérifications d'état).
- Elle indique le niveau de confiance afin que l'utilisateur sache dans quelle mesure il peut faire confiance à la suggestion.
- Elle ne modifie ni ne masque jamais la sortie d'origine de l'outil.

Cinq profils d'accessibilité sont disponibles par défaut : déficience visuelle, stress cognitif, lecteur d'écran, dyslexie et langage simple.

---

## Installation

```bash
pip install a11y-assist
```

Nécessite Python 3.11 ou une version ultérieure.

---

## Démarrage rapide

```bash
# 1. Wrap any command — a11y-assist captures its output
assist-run some-tool do-thing

# 2. If it fails, get accessible recovery guidance
a11y-assist last

# 3. Switch profiles to match your needs
a11y-assist last --profile cognitive-load
```

---

## Commandes

| Commande | Description |
|---------|-------------|
| `a11y-assist explain --json <path>` | Assistance à partir du fichier JSON `cli.error.v0.1` avec un niveau de confiance élevé. |
| `a11y-assist triage --stdin` | Assistance à partir du texte brut de l'interface en ligne de commande, avec un niveau de confiance limité. |
| `a11y-assist last` | Assistance à partir du dernier journal de bord enregistré (`~/.a11y-assist/last.log`). |
| `a11y-assist ingest <findings.json>` | Importation des résultats depuis a11y-evidence-engine. |
| `assist-run <cmd> [args...]` | Wrapper qui capture la sortie pour la commande `last`. |

Toutes les commandes acceptent les options `--profile`, `--json-response` et `--json-out`.

---

## Profils d'accessibilité

Utilisez l'option `--profile` pour sélectionner une sortie adaptée à vos besoins :

```bash
a11y-assist explain --json message.json --profile screen-reader
```

| Profil | Avantage principal | Nombre maximal d'étapes | Adaptations clés |
|---------|-----------------|-----------|-----------------|
| **lowvision** (default) | Clarté visuelle | 5 | Étiquettes claires, étapes numérotées, commandes SÛRES. |
| **cognitive-load** | Réduction de la charge mentale | 3 | Ligne de but, étiquettes "Précédent/Suivant/Dernier", phrases plus courtes. |
| **screen-reader** | Priorité à l'audio | 3-5 | Compatible avec la synthèse vocale, abréviations développées, pas de références visuelles. |
| **dyslexia** | Réduction des difficultés de lecture | 5 | Étiquettes explicites, pas d'emphase symbolique, espacement supplémentaire. |
| **plain-language** | Clarté maximale | 4 | Une seule clause par phrase, structure simplifiée. |

---

## Niveaux de confiance

| Niveau | Signification | Quand |
|-------|---------|------|
| **High** | Fichier JSON `cli.error.v0.1` validé avec un ID. | L'outil émet une sortie d'erreur structurée. |
| **Medium** | Texte brut avec un `(ID: ...)` détectable. | Un ID d'erreur est trouvé dans un texte non structuré. |
| **Low** | Analyse approximative, aucun ID trouvé. | Pas d'ancrage ; les suggestions sont heuristiques. |

Le niveau de confiance est toujours affiché dans la sortie. Il ne peut jamais augmenter lors de la transformation du profil.

---

## Garanties de sécurité

a11y-assist applique des invariants de sécurité stricts au moment de l'exécution grâce à son système de "Profile Guard" :

- **Uniquement des commandes SÛRES** — seules les commandes de lecture seule, d'exécution de test et de vérification d'état sont proposées.
- **Pas d'ID inventés** — les ID d'erreur proviennent de l'entrée ou sont absents ; ils ne sont jamais inventés.
- **Pas de contenu inventé** — les profils reformulent mais n'ajoutent jamais de nouvelles affirmations factuelles.
- **Confiance affichée** — toujours affichée ; elle peut diminuer mais jamais augmenter.
- **Ajout uniquement** — la sortie d'origine de l'outil n'est jamais modifiée, masquée ou supprimée.
- **Déterministe** — la même entrée produit toujours la même sortie ; pas d'appels réseau, pas de hasard.
- **Vérifié par le "Guard"** — chaque transformation de profil est validée par rapport aux invariants avant d'être affichée.

---

## Sortie JSON (CI / Pipelines)

Pour l'automatisation, utilisez l'option `--json-response` pour obtenir une sortie lisible par machine :

```bash
# JSON to stdout (instead of rendered text)
a11y-assist explain --json error.json --json-response

# JSON to file + rendered text to stdout
a11y-assist explain --json error.json --json-out assist.json
```

---

## Liées

- [a11y-evidence-engine](https://github.com/mcp-tool-shop-org/a11y-evidence-engine) - Moteur de preuves sans interface utilisateur.
- [a11y-mcp-tools](https://github.com/mcp-tool-shop-org/a11y-mcp-tools) - Outils MCP pour l'accessibilité.
- [a11y-demo-site](https://github.com/mcp-tool-shop-org/a11y-demo-site) - Démonstration avec des flux de travail CI.

---

## Contributions

Consultez le fichier [CONTRIBUTING.md](CONTRIBUTING.md) pour connaître les directives.

---

## Sécurité et portée des données

**Données concernées :** JSON/texte des erreurs de l'interface en ligne de commande, transmis en arguments (lecture seule), `~/.a11y-assist/last.log` (écrit par `assist-run`), sortie de l'outil vers la sortie standard ou le chemin spécifié par `--json-out`. **Données non concernées :** aucun fichier en dehors des arguments et des chemins de sortie spécifiés, aucune information d'identification du système d'exploitation, aucune donnée de navigateur. **Aucun accès réseau** — tout le traitement est local et déterministe. **Aucune télémétrie** n'est collectée ou envoyée.

## Licence

[MIT](LICENSE)

---

Créé par <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
