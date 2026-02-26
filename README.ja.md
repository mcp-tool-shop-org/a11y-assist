<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/a11y-assist/readme.png" alt="a11y-assist" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/a11y-assist/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/a11y-assist/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/a11y-assist/"><img src="https://img.shields.io/pypi/v/a11y-assist?color=blue" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/a11y-assist/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

**CLIツールのエラーに対する、決定論的なアクセシビリティ支援機能。追加機能であり、SAFEのみを使用し、プロファイルに基づいています。**

---

**v0.4は、インタラクティブではなく、決定論的です。**
ツールからの出力を書き換えることはありません。ASSISTブロックのみを追加します。

---

## なぜ

CLIツールがエラーを起こした場合、通常、エラーメッセージはツールを開発した開発者向けに書かれており、エラーから回復しようとしている人向けではありません。スクリーンリーダーを使用している、視覚障害がある、または認知的な負担がある場合、エラーメッセージや省略されたコードの羅列は役に立ちません。むしろ、別の障害となります。

**a11y-assist**は、CLIエラーが発生した場合、構造化された回復ブロックを追加します。

- 可能な場合は、提案を元のエラーIDに紐付けます。
- 番号付きで、プロファイルに合わせて調整された回復プランを生成します。
- SAFEコマンド（読み取り専用、テスト実行、ステータスチェック）のみを提案します。
- 提案に対する信頼度を明示し、ユーザーが提案をどの程度信頼できるかを知ることができます。
- 元のツールの出力を書き換えたり、隠したりすることはありません。

5つのアクセシビリティプロファイルが標準で用意されています。視覚障害者向け、認知負荷軽減向け、スクリーンリーダー向け、ディスレクシア向け、平易な言葉向けです。

---

## インストール

```bash
pip install a11y-assist
```

Python 3.11以降が必要です。

---

## クイックスタート

```bash
# 1. Wrap any command — a11y-assist captures its output
assist-run some-tool do-thing

# 2. If it fails, get accessible recovery guidance
a11y-assist last

# 3. Switch profiles to match your needs
a11y-assist last --profile cognitive-load
```

---

## コマンド

| コマンド | 説明 |
| --------- | ------------- |
| `a11y-assist explain --json <path>` | `cli.error.v0.1` JSONからの高信頼度の支援 |
| `a11y-assist triage --stdin` | 生のCLIテキストからの最善の支援 |
| `a11y-assist last` | 最後にキャプチャされたログファイル (`~/.a11y-assist/last.log`)からの支援 |
| `a11y-assist ingest <findings.json>` | a11y-evidence-engineからの情報のインポート |
| `assist-run <cmd> [args...]` | `last`コマンドの出力をキャプチャするラッパー |

すべてのコマンドは、`--profile`、`--json-response`、および`--json-out`フラグを受け入れます。

---

## アクセシビリティプロファイル

`--profile`を使用して、ニーズに合わせて調整された出力を選択します。

```bash
a11y-assist explain --json message.json --profile screen-reader
```

| プロファイル | 主な利点 | 最大ステップ数 | 主な調整点 |
| --------- | ----------------- | ----------- | ----------------- |
| **lowvision** (デフォルト) | 視覚的な明瞭さ | 5 | 明確なラベル、番号付きのステップ、SAFEコマンド |
| **cognitive-load** | 認知的な負担の軽減 | 3 | 目標の明示、開始/次/終了ラベル、短い文 |
| **screen-reader** | 音声優先 | 3-5 | 音声読み上げ対応、省略形の展開、視覚的な参照なし |
| **dyslexia** | 読解の負担軽減 | 5 | 明確なラベル、記号的な強調なし、余白の追加 |
| **plain-language** | 最大限の明瞭さ | 4 | 文ごとに1つの節、簡潔な構造 |

---

## 信頼度

| Level | 意味 | When |
| ------- | --------- | ------ |
| **High** | ID付きの検証済み`cli.error.v0.1` JSON | ツールが構造化されたエラー出力を生成 |
| **Medium** | 検出可能な`(ID: ...)`を含む生のテキスト | 構造化されていないテキスト内でエラーIDが見つかった |
| **Low** | 最善を尽くして解析したが、IDが見つからなかった | アンカーがないため、提案はヒューリスティックに基づいています |

信頼度は常に出力に表示されます。プロファイル変換中は、信頼度が向上することはありません。

---

## 安全性の保証

a11y-assistは、Profile Guardシステムを通じて、実行時に厳格な安全性の制約を適用します。

- **SAFEモード専用コマンド:** 読み取り専用、テスト実行、および状態確認のコマンドのみが推奨されます。
- **架空のIDは使用しない:** エラーIDは入力から取得するか、存在しない場合は何も表示されません。決して捏造されることはありません。
- **架空の内容は使用しない:** プロファイルは内容を言い換えるだけで、新しい事実に基づく主張を追加することはありません。
- **信頼度は常に表示:** 常に表示され、値は減少する可能性がありますが、増加することはありません。
- **追加のみ:** 元のツールの出力は、変更、非表示、または抑制されることはありません。
- **決定論的:** 同じ入力は常に同じ出力を生成します。ネットワーク接続やランダムな要素は使用しません。
- **検証済み:** 各プロファイルの変換は、レンダリング前に不変条件に対して検証されます。

---

## JSON出力 (CI / パイプライン)

自動化のため、機械可読の出力を取得するには、`--json-response` オプションを使用してください。

```bash
# JSON to stdout (instead of rendered text)
a11y-assist explain --json error.json --json-response

# JSON to file + rendered text to stdout
a11y-assist explain --json error.json --json-out assist.json
```

---

## 関連

- [a11y-evidence-engine](https://github.com/mcp-tool-shop-org/a11y-evidence-engine) - ヘッドレス型エビデンスエンジン
- [a11y-mcp-tools](https://github.com/mcp-tool-shop-org/a11y-mcp-tools) - アクセシビリティのためのMCPツール
- [a11y-demo-site](https://github.com/mcp-tool-shop-org/a11y-demo-site) - CIワークフローを使用したデモサイト

---

## 貢献

ガイドラインについては、[CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

---

## ライセンス

[MIT](LICENSE)
