<p align="center">
  <a href="README.md">English</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

**CLIの失敗に対する、決定論的なアクセシビリティ支援機能。追加機能であり、SAFEコマンドのみを使用し、プロファイルに基づいた動作。**

---

**v0.4は、インタラクティブではなく、決定論的な動作です。**
ツールからの出力を書き換えることはありません。あくまでも、ASSISTブロックを追加するだけです。

---

## なぜ

CLIツールが失敗した場合、通常、エラーメッセージはツールを開発した開発者向けに書かれており、問題を解決しようとしているユーザー向けではありません。スクリーンリーダーを使用している、視覚障害がある、または認知的な負担がある場合、大量のスタックトレースや省略されたコードは役に立ちません。むしろ、別の障害となります。

**a11y-assist**は、あらゆるCLIの失敗に対して、構造化された復旧ブロックを追加します。

- 元のエラーIDに関連する提案を行います（利用可能な場合）。
- 番号付きで、プロファイルに応じた復旧プランを生成します。
- SAFEコマンド（読み取り専用、テスト実行、ステータスチェック）のみを提案します。
- 提案に対する信頼度を明示し、ユーザーが提案をどの程度信頼できるかを知ることができます。
- 元のツールの出力を書き換えたり、隠したりすることはありません。

以下の5つのアクセシビリティプロファイルが標準で用意されています：視覚障害者向け、認知負荷軽減向け、スクリーンリーダー向け、読字障害者向け、平易な表現向け。

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
|---------|-------------|
| `a11y-assist explain --json <path>` | `cli.error.v0.1` JSONからの、高信頼度の支援 |
| `a11y-assist triage --stdin` | 生のCLIテキストからの、可能な範囲での支援 |
| `a11y-assist last` | 最後にキャプチャされたログファイル（`~/.a11y-assist/last.log`）からの支援 |
| `a11y-assist ingest <findings.json>` | a11y-evidence-engineからの情報をインポート |
| `assist-run <cmd> [args...]` | `last`コマンドの出力をキャプチャするラッパー |

すべてのコマンドは、`--profile`、`--json-response`、および`--json-out`フラグを受け入れます。

---

## アクセシビリティプロファイル

`--profile`を使用して、ニーズに合わせた出力を選択します。

```bash
a11y-assist explain --json message.json --profile screen-reader
```

| プロファイル | 主な利点 | 最大ステップ数 | 主な変更点 |
|---------|-----------------|-----------|-----------------|
| **lowvision** (default) | 視覚的な明瞭さ | 5 | 明確なラベル、番号付きステップ、SAFEコマンド |
| **cognitive-load** | 認知的な負担軽減 | 3 | 目標線、開始/次/終了ラベル、短い文 |
| **screen-reader** | 音声優先 | 3-5 | テキスト読み上げ対応、略語の展開、視覚的な参照なし |
| **dyslexia** | 読みやすさの向上 | 5 | 明確なラベル、記号的な強調なし、余白の追加 |
| **plain-language** | 最大限の明瞭さ | 4 | 文に一つの節のみ、簡潔な構造 |

---

## 信頼度

| レベル | 意味 | 適用条件 |
|-------|---------|------|
| **High** | `cli.error.v0.1` JSONがID付きで検証されている | ツールが構造化されたエラー出力を生成している |
| **Medium** | `(ID: ...)`が検出可能な生のテキスト | 構造化されていないテキスト内にエラーIDが存在する |
| **Low** | 解析は可能だが、IDが見つからない | アンカーがないため、提案はヒューリスティックに基づいている |

信頼度は常に出力に表示されます。プロファイル変換中に信頼度が低下することはありません。

---

## 安全性の保証

a11y-assistは、Profile Guardシステムを通じて、実行時に厳格な安全性の制約を適用します。

- **SAFEコマンドのみ**：読み取り専用、テスト実行、およびステータスチェックのコマンドのみが提案されます。
- **架空のIDは使用しない**：エラーIDは入力から取得するか、存在しない場合があり、作成されることはありません。
- **架空のコンテンツは使用しない**：プロファイルは言い換えるだけで、新しい事実を追加することはありません。
- **信頼度は明示する**：常に表示され、低下することはあっても、増加することはありません。
- **追加機能のみ**：元のツールの出力は変更、非表示、または抑制されることはありません。
- **決定論的**：同じ入力は常に同じ出力を生成し、ネットワーク接続や乱数は使用しません。
- **ガードチェック**：すべてのプロファイル変換は、レンダリング前に、制約に対する検証が行われます。

---

## JSON出力（CI / パイプライン）

自動化を行う場合は、`--json-response` オプションを使用して、機械が読み取り可能な形式で結果を得ることができます。

```bash
# JSON to stdout (instead of rendered text)
a11y-assist explain --json error.json --json-response

# JSON to file + rendered text to stdout
a11y-assist explain --json error.json --json-out assist.json
```

---

## 関連情報

- [a11y-evidence-engine](https://github.com/mcp-tool-shop-org/a11y-evidence-engine) - ヘッドレス型の証拠収集エンジン
- [a11y-mcp-tools](https://github.com/mcp-tool-shop-org/a11y-mcp-tools) - アクセシビリティのための MCP ツール
- [a11y-demo-site](https://github.com/mcp-tool-shop-org/a11y-demo-site) - CI ワークフローを使用したデモサイト

---

## 貢献について

ガイドラインについては、[CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

---

## セキュリティとデータ範囲

**アクセスするデータ:** コマンドライン引数として渡されるエラーメッセージの JSON/テキスト（読み取り専用）、`~/.a11y-assist/last.log`（`assist-run`によって書き込まれる）、`assist` の出力（標準出力または `--json-out` で指定されたパス）。 **アクセスしないデータ:** 指定された引数と出力パス以外のファイル、OS の認証情報、ブラウザのデータ。 **外部ネットワークへのアクセスはありません**。すべての処理はローカルで行われ、結果は常に同じです。 **テレメトリーは収集または送信されません**。

## ライセンス

[MIT](LICENSE)

---

<a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a> が作成しました。
