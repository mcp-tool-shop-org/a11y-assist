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

**CLI (कमांड लाइन इंटरफेस) विफल होने पर, सुलभ सहायता। योज्य, केवल SAFE विकल्पों का उपयोग करने वाला, प्रोफाइल-आधारित।**

---

**v0.4 गैर-इंटरैक्टिव और निश्चित है।**
यह कभी भी टूल के आउटपुट को दोबारा नहीं लिखता है। यह केवल एक 'सहायता' ब्लॉक जोड़ता है।

---

## क्यों?

जब कोई CLI टूल विफल होता है, तो त्रुटि संदेश आमतौर पर उस डेवलपर के लिए लिखा जाता है जिसने इसे बनाया है, न कि उस व्यक्ति के लिए जो इसे ठीक करने की कोशिश कर रहा है। यदि आप स्क्रीन रीडर का उपयोग करते हैं, आपकी दृष्टि कमजोर है, या आप मानसिक तनाव में हैं, तो ढेर सारे त्रुटि संदेश और संक्षिप्त कोड आपकी मदद नहीं करेंगे - यह एक और बाधा है।

**a11y-assist** किसी भी CLI विफलता में एक संरचित रिकवरी ब्लॉक जोड़ता है:

- यह सुझावों को मूल त्रुटि आईडी से जोड़ता है (जब उपलब्ध हो)।
- यह क्रमांकित, प्रोफाइल-अनुकूल रिकवरी योजनाएं उत्पन्न करता है।
- यह केवल SAFE कमांड (केवल पढ़ने के लिए, परीक्षण, स्थिति जांच) का सुझाव देता है।
- यह आत्मविश्वास का स्तर बताता है ताकि उपयोगकर्ता को पता चल सके कि उसे सुझाव पर कितना भरोसा करना चाहिए।
- यह कभी भी मूल टूल के आउटपुट को दोबारा नहीं लिखता है या उसे छिपाता नहीं है।

पांच पहुंच प्रोफाइल डिफ़ॉल्ट रूप से उपलब्ध हैं: कम दृष्टि, मानसिक तनाव, स्क्रीन रीडर, डिस्लेक्सिया और सरल भाषा।

---

## इंस्टॉल करें

```bash
pip install a11y-assist
```

इसके लिए Python 3.11 या बाद के संस्करण की आवश्यकता है।

---

## शुरुआत

```bash
# 1. Wrap any command — a11y-assist captures its output
assist-run some-tool do-thing

# 2. If it fails, get accessible recovery guidance
a11y-assist last

# 3. Switch profiles to match your needs
a11y-assist last --profile cognitive-load
```

---

## कमांड

| कमांड | विवरण |
| --------- | ------------- |
| `a11y-assist explain --json <path>` | `cli.error.v0.1` JSON से उच्च-विश्वास वाली सहायता |
| `a11y-assist triage --stdin` | कच्चे CLI टेक्स्ट से सर्वोत्तम संभव सहायता |
| `a11y-assist last` | अंतिम कैप्चर किए गए लॉग (`~/.a11y-assist/last.log`) से सहायता |
| `a11y-assist ingest <findings.json>` | a11y-evidence-engine से निष्कर्ष आयात करें |
| `assist-run <cmd> [args...]` | एक रैपर जो `last` के लिए आउटपुट कैप्चर करता है |

सभी कमांड `--profile`, `--json-response`, और `--json-out` ध्वज स्वीकार करते हैं।

---

## पहुंच प्रोफाइल

अपनी आवश्यकताओं के अनुसार आउटपुट को अनुकूलित करने के लिए `--profile` का उपयोग करें:

```bash
a11y-assist explain --json message.json --profile screen-reader
```

| प्रोफाइल | मुख्य लाभ | अधिकतम चरण | मुख्य अनुकूलन |
| --------- | ----------------- | ----------- | ----------------- |
| **lowvision** (डिफ़ॉल्ट) | दृश्य स्पष्टता | 5 | स्पष्ट लेबल, क्रमांकित चरण, SAFE कमांड |
| **cognitive-load** | मानसिक चरणों में कमी | 3 | लक्ष्य रेखा, 'पहला/अगला/अंतिम' लेबल, छोटे वाक्य |
| **screen-reader** | ऑडियो-प्रथम | 3-5 | TTS-अनुकूल, संक्षिप्त शब्दों का विस्तार, कोई दृश्य संदर्भ नहीं |
| **dyslexia** | पढ़ने में कठिनाई में कमी | 5 | स्पष्ट लेबल, प्रतीकात्मक जोर नहीं, अतिरिक्त स्पेसिंग |
| **plain-language** | अधिकतम स्पष्टता | 4 | प्रत्येक वाक्य में एक खंड, सरलीकृत संरचना |

---

## आत्मविश्वास स्तर

| Level | अर्थ | When |
| ------- | --------- | ------ |
| **High** | ID के साथ मान्य `cli.error.v0.1` JSON | टूल संरचित त्रुटि आउटपुट उत्सर्जित करता है |
| **Medium** | पहचान योग्य `(ID: ...)` के साथ कच्चा टेक्स्ट | असंरचित टेक्स्ट में त्रुटि आईडी पाया गया |
| **Low** | सर्वोत्तम संभव पार्सिंग, कोई आईडी नहीं मिला | कोई एंकर नहीं; सुझाव अनुमानित हैं |

आत्मविश्वास हमेशा आउटपुट में बताया जाता है। यह प्रोफाइल परिवर्तन के दौरान कभी नहीं बढ़ता है।

---

## सुरक्षा गारंटी

a11y-assist अपने प्रोफाइल गार्ड सिस्टम के माध्यम से रनटाइम पर सख्त सुरक्षा नियमों का पालन करता है:

- **केवल सुरक्षित कमांड** — केवल पढ़ने के लिए, परीक्षण चलाने और स्थिति जांचने वाले कमांडों की सिफारिश की जाती है।
- **कोई मनगढ़ंत आईडी नहीं** — त्रुटि आईडी या तो इनपुट से आती हैं या अनुपस्थित होती हैं; कभी भी बनाई नहीं जाती हैं।
- **कोई मनगढ़ंत सामग्री नहीं** — प्रोफाइल जानकारी को फिर से प्रस्तुत करते हैं, लेकिन कभी भी नई तथ्यात्मक जानकारी नहीं जोड़ते हैं।
- **आत्मविश्वास का खुलासा** — हमेशा दिखाया जाता है; यह कम हो सकता है, लेकिन कभी भी बढ़ नहीं सकता।
- **केवल अतिरिक्त** — मूल टूल का आउटपुट कभी भी संशोधित, छिपाया या दबाया नहीं जाता है।
- **निश्चित** — समान इनपुट हमेशा समान आउटपुट उत्पन्न करता है; कोई नेटवर्क कॉल नहीं, कोई यादृच्छिकता नहीं।
- **सुरक्षा जांच** — प्रत्येक प्रोफाइल परिवर्तन को प्रस्तुत करने से पहले, अपरिवर्तनीयताओं के विरुद्ध मान्य किया जाता है।

---

## JSON आउटपुट (CI / पाइपलाइन)

स्वचालन के लिए, मशीन-पठनीय आउटपुट प्राप्त करने के लिए `--json-response` का उपयोग करें:

```bash
# JSON to stdout (instead of rendered text)
a11y-assist explain --json error.json --json-response

# JSON to file + rendered text to stdout
a11y-assist explain --json error.json --json-out assist.json
```

---

## संबंधित

- [a11y-evidence-engine](https://github.com/mcp-tool-shop-org/a11y-evidence-engine) - हेडलेस प्रमाण इंजन
- [a11y-mcp-tools](https://github.com/mcp-tool-shop-org/a11y-mcp-tools) - पहुंच के लिए MCP उपकरण
- [a11y-demo-site](https://github.com/mcp-tool-shop-org/a11y-demo-site) - CI वर्कफ़्लो के साथ डेमो

---

## योगदान

मार्गदर्शिका के लिए [CONTRIBUTING.md](CONTRIBUTING.md) देखें।

---

## लाइसेंस

[MIT](LICENSE)
