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

**Assistance déterministe pour les erreurs des interfaces en ligne de commande (CLI). Additive, uniquement pour les commandes SAFE, basée sur des profils.**

---

**La version 0.4 est non interactive et déterministe.**
Elle ne modifie jamais la sortie des outils. Elle ajoute uniquement un bloc d'ASSISTANCE.

---

## Pourquoi ?

Lorsqu'un outil CLI rencontre une erreur, le message d'erreur est généralement rédigé pour le développeur qui l'a créé, et non pour la personne qui essaie de résoudre le problème. Si vous utilisez un lecteur d'écran, si vous avez une déficience visuelle ou si vous êtes en état de stress cognitif, une longue liste de traces de pile et de codes abrégés n'est pas une aide ; c'est un autre obstacle.

**a11y-assist** ajoute un bloc de récupération structuré à toute erreur CLI :

- Les suggestions sont liées à l'ID d'erreur d'origine (lorsqu'il est disponible).
- Elle génère des plans de récupération numérotés et adaptés au profil.
- Elle ne propose que des commandes SAFE (lecture seule, test, vérifications d'état).
- Elle indique le niveau de confiance afin que l'utilisateur sache dans quelle mesure il peut faire confiance à la suggestion.
- Elle ne modifie ni ne masque jamais la sortie d'origine de l'outil.

Cinq profils d'accessibilité sont disponibles par défaut : déficience visuelle, surcharge cognitive, lecteur d'écran, dyslexie et langage clair.

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
| --------- | ------------- |
| `a11y-assist explain --json <path>` | Assistance de haute qualité à partir du JSON `cli.error.v0.1` |
| `a11y-assist triage --stdin` | Assistance de qualité variable à partir du texte brut de la CLI |
| `a11y-assist last` | Assistance à partir du dernier journal capturé (`~/.a11y-assist/last.log`) |
| `a11y-assist ingest <findings.json>` | Importation des résultats de a11y-evidence-engine |
| `assist-run <cmd> [args...]` | Wrapper qui capture la sortie pour la commande `last` |

Toutes les commandes acceptent les drapeaux `--profile`, `--json-response` et `--json-out`.

---

## Profils d'accessibilité

Utilisez le drapeau `--profile` pour sélectionner une sortie adaptée à vos besoins :

```bash
a11y-assist explain --json message.json --profile screen-reader
```

| Profil | Avantage principal | Nombre maximal d'étapes | Adaptations clés |
| --------- | ----------------- | ----------- | ----------------- |
| **lowvision** (par défaut) | Clarté visuelle | 5 | Étiquettes claires, étapes numérotées, commandes SAFE |
| **cognitive-load** | Réduction de la charge mentale | 3 | Ligne de but, étiquettes "Précédent/Suivant/Dernier", phrases plus courtes |
| **screen-reader** | Priorité à l'audio | 3-5 | Compatible avec la synthèse vocale, abréviations développées, pas de références visuelles |
| **dyslexia** | Réduction des difficultés de lecture | 5 | Étiquettes explicites, pas d'emphase symbolique, espacement supplémentaire |
| **plain-language** | Clarté maximale | 4 | Une clause par phrase, structure simplifiée |

---

## Niveaux de confiance

| Level | Signification | When |
| ------- | --------- | ------ |
| **High** | JSON `cli.error.v0.1` validé avec ID | L'outil émet une sortie d'erreur structurée |
| **Medium** | Texte brut avec `(ID: ...)` détectable | ID d'erreur trouvé dans un texte non structuré |
| **Low** | Analyse approximative, aucun ID trouvé | Pas d'ancre ; les suggestions sont heuristiques |

Le niveau de confiance est toujours indiqué dans la sortie. Il n'augmente jamais lors de la transformation du profil.

---

## Garanties de sécurité

a11y-assist applique des invariants de sécurité stricts au moment de l'exécution grâce à son système de "Profile Guard" :

- **Commandes SAFE uniquement** : Seules les commandes en lecture seule, les tests préliminaires et les vérifications d'état sont proposées.
- **Aucune ID inventée** : Les identifiants d'erreur proviennent de l'entrée ou sont absents ; ils ne sont jamais fabriqués.
- **Aucun contenu inventé** : Les profils reformulent, mais n'ajoutent jamais de nouvelles affirmations factuelles.
- **Confiance divulguée** : Affichée en permanence ; elle peut diminuer, mais jamais augmenter.
- **Additive uniquement** : La sortie de l'outil original n'est jamais modifiée, masquée ou supprimée.
- **Déterministe** : La même entrée produit toujours la même sortie ; aucune requête réseau, aucune aléatoire.
- **Vérification des contraintes** : Chaque transformation de profil est validée par rapport aux contraintes avant d'être affichée.

---

## Sortie JSON (CI / Pipelines)

Pour l'automatisation, utilisez `--json-response` pour obtenir une sortie lisible par machine :

```bash
# JSON to stdout (instead of rendered text)
a11y-assist explain --json error.json --json-response

# JSON to file + rendered text to stdout
a11y-assist explain --json error.json --json-out assist.json
```

---

## Liés

- [a11y-evidence-engine](https://github.com/mcp-tool-shop-org/a11y-evidence-engine) - Moteur d'analyse headless
- [a11y-mcp-tools](https://github.com/mcp-tool-shop-org/a11y-mcp-tools) - Outils MCP pour l'accessibilité
- [a11y-demo-site](https://github.com/mcp-tool-shop-org/a11y-demo-site) - Démonstration avec des flux de travail CI

---

## Contribution

Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour connaître les directives.

---

## Licence

[MIT](LICENSE)
