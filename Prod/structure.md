# Project Structure

```
/
├── index.html      # Page markup, embedded CSS and JavaScript
├── *.svg           # Local image assets, including SVG-wrapped photos
└── Prod/           # Project documentation
```

## Embedded JavaScript Organization (top to bottom)
1. `const stories` — array of story objects (the content database)
2. `const timelineIds` — IDs of stories shown in the Nasir Crisis timeline
3. Utility functions: `esc()`, `$()`, `$()`, `sourceName()`, `sourceshort()`, `verificationBadge()`
4. Renderers: `card()`, `renderTimeline()`, `renderHome()`, `renderListing()`, `openArticle()`, `closeArticle()`
5. Search: `openSearch()`, `closeSearch()`, `search()`
6. Form: `initSubmitForm()`
7. View manager: `showView()`
8. Init block: sets date, renders home, registers all event listeners

## Story Object Shape
```js
{
  id: Number,
  category: String,         // "Nasir Crisis" | "Recovery" | "Community" | "Youth" | "Investigations" | etc.
  date: String,             // Display date range
  incidentDate: String,     // Optional: when event occurred
  pubDate: String,          // Optional: when report was published
  title: String,
  excerpt: String,
  glyph: String,            // Single character shown as decorative image
  tone: String,             // CSS class: tone-blue | tone-lime | tone-orange | tone-purple | tone-dark | tone-pink
  featured: Boolean,
  verification: String|null, // "Reported" | "UN-documented" | "Corroborated" | "Details disputed" | null
  body: String[],           // Paragraphs rendered as <p> tags
  sources: [{ label: String, url: String }]
}
```

## CSS Conventions
- CSS custom properties on `:root` for all design tokens (colors, fonts)
- BEM-lite class naming: `.story-card`, `.story-body`, `.story-meta`
- Tone modifier classes on image containers: `.tone-blue`, `.tone-dark`, etc.
- Responsive via `@media(max-width:900px)` and `@media(max-width:650px)`
- `.hidden` utility class uses `display:none!important`
