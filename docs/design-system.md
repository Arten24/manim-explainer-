# Design system

Default theme: **quonitron_dark**.

## Color roles

| Role | Hex | Use |
| --- | --- | --- |
| `background` | `#0D1117` | Scene background |
| `surface` | `#161B22` | Cards and panels |
| `text_primary` | `#F5F7FA` | Titles and body |
| `text_secondary` | `#9AA4B2` | Kickers, labels, captions |
| `accent` | `#4C8DFF` | Rules, markers, focus |
| `accent_secondary` | `#8B7CFF` | Sparse secondary accent |
| `highlight` | `#5EC8C5` | Values, important numbers |
| `success` / `warning` / `danger` | semantic only | Status, never decoration |

The look is premium dark editorial: clean type, restrained accents, readable
diagrams, smooth motion. Do not add neon glow, grid spam, or random hues.

## Typography

Manim `Text` font sizes:

| Role | Size | Color role |
| --- | --- | --- |
| title | 48 | text_primary |
| heading | 36 | text_primary |
| body | 28 | text_primary |
| label | 22 | text_secondary |
| caption | 20 | text_secondary |
| code | 26 | highlight |

Font stacks, first available wins:

- Sans: DejaVu Sans, Liberation Sans, Noto Sans, Inter, Segoe UI, Arial, Helvetica, sans-serif
- Mono: DejaVu Sans Mono, Liberation Mono, Cascadia Mono, Consolas, Courier New, monospace

No font is assumed to be installed. On Windows, Arial / Segoe UI / Consolas
are typical fallbacks. On Linux, DejaVu or Liberation are typical.

## Layout

Scene units, default frame height 8, width ≈ 14.22 (16:9).

- Outer margin `0.55`
- Safe margin `0.80` — titles and captions stay inside this band
- Spacing scale: `xxs` … `xl`

## Motion

| Token | Seconds |
| --- | --- |
| instant | 0.15 |
| fast | 0.30 |
| normal | 0.60 |
| slow | 1.00 |
| hold | 0.70 |

Default easing alias: `smooth` → Manim `rate_functions.smooth`.

## Overrides

```python
from quonitron_manim.design import get_theme, register_theme

theme = get_theme().override(name="lecture", colors={"accent": "#5B9BFF"})
register_theme("lecture", theme)
```

Components take a `theme=` argument. Do not pass raw hex into new code.
