<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.md">English</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

**Asistencia determinista para accesibilidad en caso de fallos de la interfaz de línea de comandos (CLI). Aditiva, solo comandos SAFE, basada en perfiles.**

---

**La versión 0.4 es no interactiva y determinista.**
Nunca modifica la salida de las herramientas. Solo añade un bloque de ASISTENCIA.

---

## ¿Por qué?

Cuando una herramienta de la interfaz de línea de comandos falla, el mensaje de error suele estar escrito para el desarrollador que la creó, no para la persona que intenta solucionar el problema. Si utiliza un lector de pantalla, tiene problemas de visión o está bajo estrés cognitivo, una gran cantidad de trazas de pila y códigos abreviados no son útiles; son otro obstáculo.

**a11y-assist** añade un bloque de recuperación estructurado a cualquier fallo de la interfaz de línea de comandos:

- Vincula las sugerencias al ID de error original (cuando esté disponible).
- Genera planes de recuperación numerados y adaptados al perfil.
- Solo sugiere comandos SAFE (solo lectura, pruebas, comprobaciones de estado).
- Indica el nivel de confianza para que el usuario sepa cuánto puede confiar en la sugerencia.
- Nunca modifica ni oculta la salida original de la herramienta.

Cinco perfiles de accesibilidad están disponibles de forma predeterminada: visión reducida, estrés cognitivo, lector de pantalla, dislexia y lenguaje sencillo.

---

## Instalación

```bash
pip install a11y-assist
```

Requiere Python 3.11 o posterior.

---

## Inicio rápido

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

| Comando | Descripción |
|---------|-------------|
| `a11y-assist explain --json <path>` | Asistencia de alta confianza a partir de JSON de `cli.error.v0.1`. |
| `a11y-assist triage --stdin` | Asistencia con el máximo esfuerzo a partir de texto sin formato de la interfaz de línea de comandos. |
| `a11y-assist last` | Asistencia a partir del último registro capturado (`~/.a11y-assist/last.log`). |
| `a11y-assist ingest <findings.json>` | Importa resultados de a11y-evidence-engine. |
| `assist-run <cmd> [args...]` | Envoltorio que captura la salida para el comando `last`. |

Todos los comandos aceptan las opciones `--profile`, `--json-response` y `--json-out`.

---

## Perfiles de accesibilidad

Utilice la opción `--profile` para seleccionar una salida adaptada a sus necesidades:

```bash
a11y-assist explain --json message.json --profile screen-reader
```

| Perfil | Beneficio principal | Número máximo de pasos | Adaptaciones clave |
|---------|-----------------|-----------|-----------------|
| **lowvision** (default) | Claridad visual | 5 | Etiquetas claras, pasos numerados, comandos SAFE. |
| **cognitive-load** | Reducción de la carga cognitiva | 3 | Línea de meta, etiquetas "Primero/Siguiente/Último", frases más cortas. |
| **screen-reader** | Prioridad al audio | 3-5 | Compatible con síntesis de voz, abreviaturas expandidas, sin referencias visuales. |
| **dyslexia** | Reducción de la dificultad de lectura | 5 | Etiquetas explícitas, sin énfasis simbólico, espaciado adicional. |
| **plain-language** | Máxima claridad | 4 | Una cláusula por frase, estructura simplificada. |

---

## Niveles de confianza

| Nivel | Significado | Cuándo |
|-------|---------|------|
| **High** | JSON de `cli.error.v0.1` validado con ID. | La herramienta emite una salida de error estructurada. |
| **Medium** | Texto sin formato con "(ID: ...)" detectable. | Se encuentra un ID de error en texto no estructurado. |
| **Low** | Análisis con el máximo esfuerzo, no se encuentra ningún ID. | Sin referencia; las sugerencias son heurísticas. |

El nivel de confianza se muestra siempre en la salida. Nunca aumenta durante la transformación del perfil.

---

## Garantías de seguridad

a11y-assist aplica estrictas invariantes de seguridad en tiempo de ejecución a través de su sistema de Protección de Perfiles:

- **Solo comandos SAFE** — solo se sugieren comandos de solo lectura, pruebas y comprobaciones de estado.
- **Sin IDs inventados** — los IDs de error provienen de la entrada o están ausentes; nunca se inventan.
- **Sin contenido inventado** — los perfiles reformulan, pero nunca añaden afirmaciones fácticas nuevas.
- **Confianza indicada** — siempre se muestra; puede disminuir, pero nunca aumentar.
- **Solo aditivo** — la salida original de la herramienta nunca se modifica, se oculta ni se suprime.
- **Determinista** — la misma entrada siempre produce la misma salida; no hay llamadas a la red, ni aleatoriedad.
- **Comprobado por el protector** — cada transformación de perfil se valida contra las invariantes antes de renderizarse.

---

## Salida en formato JSON (CI / Pipelines)

Para la automatización, utilice `--json-response` para obtener una salida legible por máquinas:

```bash
# JSON to stdout (instead of rendered text)
a11y-assist explain --json error.json --json-response

# JSON to file + rendered text to stdout
a11y-assist explain --json error.json --json-out assist.json
```

---

## Relacionado

- [a11y-evidence-engine](https://github.com/mcp-tool-shop-org/a11y-evidence-engine) - Motor de análisis de accesibilidad sin interfaz.
- [a11y-mcp-tools](https://github.com/mcp-tool-shop-org/a11y-mcp-tools) - Herramientas MCP para la accesibilidad.
- [a11y-demo-site](https://github.com/mcp-tool-shop-org/a11y-demo-site) - Demostración con flujos de trabajo de CI.

---

## Contribuciones

Consulte [CONTRIBUTING.md](CONTRIBUTING.md) para obtener las directrices.

---

## Seguridad y alcance de los datos

**Datos accedidos:** JSON/texto de errores de la línea de comandos pasados como argumentos (solo lectura), `~/.a11y-assist/last.log` (escrito por `assist-run`), salida de `assist` a la salida estándar o a la ruta especificada con `--json-out`. **Datos NO accedidos:** ningún archivo fuera de los argumentos y rutas de salida especificados, ninguna credencial del sistema operativo, ningún dato del navegador. **No hay salida de red**; todo el procesamiento es local y determinista. **No se recopila ni se envía telemetría**.

## Licencia

[MIT](LICENSE)

---

Creado por <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
