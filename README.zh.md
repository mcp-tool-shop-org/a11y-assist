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

**用于解决 CLI 错误的确定性辅助功能。增量式，仅支持 SAFE，基于配置文件的。**

---

**v0.4 版本不提供交互功能，且结果是确定的。**
它不会重写工具的输出。它只会添加一个辅助信息块。

---

## 原因

当 CLI 工具出现错误时，错误信息通常是为构建该工具的开发人员编写的，而不是为试图解决错误的用户编写的。如果您使用屏幕阅读器，视力较差，或者处于认知负荷状态，那么大量的堆栈跟踪和缩写代码并不能提供帮助，反而会成为一种障碍。

**a11y-assist** 为任何 CLI 错误添加一个结构化的恢复信息块：

- 将建议与原始错误 ID 相关联（如果可用）。
- 生成编号的、与配置文件相适应的恢复计划。
- 仅建议 SAFE 命令（只读、模拟运行、状态检查）。
- 公示置信度，以便用户了解应该对建议的信任程度。
- 绝不会重写或隐藏原始工具的输出。

默认情况下，提供五个辅助功能配置文件：低视力、认知负荷、屏幕阅读器、阅读障碍和简单语言。

---

## 安装

```bash
pip install a11y-assist
```

需要 Python 3.11 或更高版本。

---

## 快速入门

```bash
# 1. Wrap any command — a11y-assist captures its output
assist-run some-tool do-thing

# 2. If it fails, get accessible recovery guidance
a11y-assist last

# 3. Switch profiles to match your needs
a11y-assist last --profile cognitive-load
```

---

## 命令

| 命令 | 描述 |
| --------- | ------------- |
| `a11y-assist explain --json <path>` | 从 `cli.error.v0.1` JSON 获取高置信度的辅助信息。 |
| `a11y-assist triage --stdin` | 从原始 CLI 文本获取最佳的辅助信息。 |
| `a11y-assist last` | 从上次捕获的日志文件 (`~/.a11y-assist/last.log`) 获取辅助信息。 |
| `a11y-assist ingest <findings.json>` | 从 a11y-evidence-engine 导入发现结果。 |
| `assist-run <cmd> [args...]` | 一个包装器，用于捕获 `last` 命令的输出。 |

所有命令都接受 `--profile`、`--json-response` 和 `--json-out` 标志。

---

## 辅助功能配置文件

使用 `--profile` 标志选择适合您需求的输出：

```bash
a11y-assist explain --json message.json --profile screen-reader
```

| 配置文件 | 主要优势 | 最大步骤数 | 主要调整 |
| --------- | ----------------- | ----------- | ----------------- |
| **lowvision** (默认) | 视觉清晰度 | 5 | 清晰的标签、编号的步骤、SAFE 命令 |
| **cognitive-load** | 减少认知负担 | 3 | 目标线、"开始/下一步/结束" 标签、更短的句子 |
| **screen-reader** | 以语音为优先 | 3-5 | 适合文本转语音、展开缩写、无视觉引用 |
| **dyslexia** | 减少阅读障碍 | 5 | 明确的标签、无符号强调、额外的间距 |
| **plain-language** | 最大清晰度 | 4 | 每个句子一个子句、简化的结构 |

---

## 置信度级别

| Level | 含义 | When |
| ------- | --------- | ------ |
| **High** | 已验证的 `cli.error.v0.1` JSON，包含 ID | 工具发出结构化的错误输出 |
| **Medium** | 原始文本，包含可检测的 `(ID: ...)` | 在非结构化文本中找到错误 ID |
| **Low** | 最佳尝试解析，未找到 ID | 没有锚点；建议是基于启发式方法 |

置信度始终在输出中显示。在配置文件转换过程中，置信度不会增加。

---

## 安全保障

a11y-assist 通过其配置文件保护系统，在运行时强制执行严格的安全约束：

- **仅限 SAFE 模式下的命令** — 仅建议使用只读、模拟运行和状态检查命令。
- **不使用虚构的 ID** — 错误 ID 来自输入，或者不存在；绝不虚构。
- **不添加额外内容** — 配置文件是对已有内容的重述，绝不添加新的事实性主张。
- **明确显示置信度** — 始终显示；可以降低，但绝不能升高。
- **仅进行增量修改** — 原始工具的输出永远不会被修改、隐藏或压制。
- **确定性** — 相同的输入始终产生相同的输出；不涉及网络调用，不包含随机性。
- **经过安全检查** — 每次配置文件转换都经过对不变性的验证，然后再进行渲染。

---

## JSON 输出（CI / 流水线）

为了自动化，请使用 `--json-response` 参数以获取机器可读的输出。

```bash
# JSON to stdout (instead of rendered text)
a11y-assist explain --json error.json --json-response

# JSON to file + rendered text to stdout
a11y-assist explain --json error.json --json-out assist.json
```

---

## 相关项目

- [a11y-evidence-engine](https://github.com/mcp-tool-shop-org/a11y-evidence-engine) - 无头证据引擎
- [a11y-mcp-tools](https://github.com/mcp-tool-shop-org/a11y-mcp-tools) - 用于辅助功能的 MCP 工具
- [a11y-demo-site](https://github.com/mcp-tool-shop-org/a11y-demo-site) - 包含 CI 工作流的演示站点

---

## 贡献

请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 以获取贡献指南。

---

## 许可证

[MIT](LICENSE)
