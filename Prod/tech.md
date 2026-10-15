# Tech Stack

## Stack
- Vanilla HTML, CSS, JavaScript — no build system, no frameworks, no dependencies
- Single-page application rendered entirely client-side
- All markup, CSS, and JavaScript are contained in `index.html`
- Story data is defined in the embedded JavaScript as a `const stories` array

## Files
- `index.html` — page markup, all views, styles, data, rendering logic, event handling, and view management

## No Build Step
There is no `package.json`, bundler, or compiler. Open `index.html` directly in a browser or serve with any static file server:

```
npx serve .
# or
python -m http.server
```

## Patterns
- DOM queries use `$` (aliased to `document.querySelector`) and `$$` (aliased to `document.querySelectorAll`)
- All user-generated/dynamic HTML is escaped via the `esc()` helper to prevent XSS
- Views are toggled by adding/removing the `hidden` class on `.page-section` elements
- Event handling uses a single delegated listener on `document` for click events
- No external fonts, icons, or CDN dependencies — system font stack only
