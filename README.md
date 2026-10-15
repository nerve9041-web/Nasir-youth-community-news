# Nasir Youth Community

<p align="center">
  <img src="nasir_logo.svg" alt="Nasir Youth Community logo" width="120" />
</p>

<p align="center">
  <img alt="Static Website" src="https://img.shields.io/badge/Type-Static%20Website-0b1727" />
  <img alt="HTML5" src="https://img.shields.io/badge/Stack-HTML5%20%2B%20CSS%20%2B%20JS-245ce8" />
  <img alt="No Build Step" src="https://img.shields.io/badge/Setup-No%20Build%20Required-2a7a4b" />
</p>

Independent community news, investigations, and the documented Nasir Crisis timeline from Upper Nile State, South Sudan.

## Overview

Nasir Youth Community is a static website that brings together local reporting, community voices, historical documentation, and verified crisis coverage in a simple, accessible, mobile-friendly format.

The site is designed to support:

- public awareness and historical record-keeping
- local storytelling and community reporting
- searchable timelines of major events
- memorialization and documented casualty records
- editorial accountability through source attribution

## Highlights

- Home page with a hero section, featured updates, and timeline summaries
- Newsroom with filterable story listings
- Searchable Nasir Crisis timeline
- Memorial page for documented casualties and community voices
- About page covering mission, values, and editorial approach
- Submission form for community tips and corrections
- Responsive layout for desktop, tablet, and mobile devices
- Accessibility-focused navigation and keyboard support

## Project structure

```text
.
├── index.html               # Main page structure, content, styles, and scripts
├── nasir_logo.svg           # Brand/logo asset
├── nasir-community-aerial.svg
├── missing-photo.svg        # Fallback image for missing media
├── daily-posts.js           # Generated daily draft stories
├── automation/              # RSS source metadata and automation helpers
├── .github/workflows/       # GitHub Actions for scheduled drafting/deployment
├── Prod/                    # Project packaging or production-related assets
├── README.md                # Documentation
└── screenshots/             # Optional screenshot assets (if added locally)
```

## Run locally

### Open directly

Double-click `index.html` in your project folder, or open it in a browser.

### Run with a local server

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

Alternatively:

```bash
npx serve .
```

Then visit:

```text
http://localhost:3000
```

## Features requiring internet access

- External original-report links open in the browser
- Some photo assets are loaded from external sources or wrapped SVG references
- Local SVG files work offline, but internet access is needed for remote reporting images and third-party source sites
- If media fails to load, the site falls back to `missing-photo.svg`

## Backend note

The community submission form is frontend-only. It currently displays a confirmation notice after submission, but to make it functional in production it needs a backend endpoint and the form action configured in `index.html`.

## Automated story drafting

This project includes GitHub Actions for daily drafting and deployment:

- `daily-draft.yml` generates daily AI-assisted story drafts from trusted RSS feeds
- `deploy-infinityfree.yml` deploys the site after changes are pushed to `main`
- Required secrets such as `OPENAI_API_KEY`, `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`, and `FTP_SERVER_DIR` must be configured in the GitHub repository settings

Important:

- Keep credentials in GitHub Secrets, not in source files
- The repository should use a default branch named `main`
- Review generated stories before merging them to production

## Editorial standards

The project is designed to prioritize transparency and accountability:

- Articles and timeline entries are attributed to named reporting organizations
- Casualty figures are tied to their source organizations
- Multiple-county figures are clearly distinguished from Nasir-only totals
- Dates and publication dates are kept separate where relevant
- Placeholder content should be replaced with verified reporting before publication

## License

This project is for community documentation and informational use. Please check the repository for any licensing details before reusing content or media.

## Contributing

Contributions are welcome for:

- improving content accuracy
- refining the site layout and accessibility
- expanding the crisis timeline and archival material
- strengthening automation and source verification workflows
