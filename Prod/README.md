# Nasir Youth Community Website

Independent community news, investigations, and the documented Nasir Crisis timeline.

## Opening locally (Windows)

1. Double-click `index.html` — it will open in your default browser.
2. No installation or build step is required. The HTML file contains the page, styles, and JavaScript. Local SVG images alongside `index.html` work offline; external photos and links require an internet connection.
3. External source links (Human Rights Watch, Radio Tamazuj, UNMISS, MSF, The Guardian) will open in your browser when you have internet access.

## Optional: run with a local server

If you prefer a local server (avoids any browser file-access restrictions):

```
npx serve .
```
or
```
python -m http.server
```

Then open http://localhost:3000 (npx serve) or http://localhost:8000 (Python).

## Files

| File        | Purpose                                                     |
|-------------|-------------------------------------------------------------|
| index.html  | Full page markup, embedded styles and JavaScript            |
| README.md   | Project documentation                                       |

## Features

- Home with an aerial community photo in the hero, Nasir Crisis timeline, featured stories, and latest updates
- Newsroom with filterable story listings
- Nasir Crisis timeline — searchable, filterable by source and period
- Memorial page with documented casualties and community voices
- Submit page — community tip/correction form (frontend only; see below)
- About page — mission, values, editorial approach
- Search overlay — searches all story text, categories, and sources
- Responsive — works on desktop, tablet, and mobile
- Accessible — keyboard navigation, ARIA labels, focus management

## Features requiring internet access

- All "Read original report" / "Original report" links open external URLs
- Report photos include local images and credited photos from Radio Tamazuj and UNMISS
- The March 2025 Nasir field report includes its local overview map and three related satellite images from the project folder
- Local photos are SVG wrappers around their original image data; externally hosted publisher photos are displayed inside inline SVG wrappers and still require internet access
- If a photo cannot be loaded, the page tries the local `missing-photo.svg` placeholder
- Footer source links

## Features requiring backend configuration

The submission form (Submit page) is frontend-only. It will show a notice when submitted. To make submissions functional, a backend endpoint must be configured and the form action updated in `index.html`.

## Daily AI story drafts (GitHub + InfinityFree)

- `.github/workflows/daily-draft.yml` runs daily at 06:00 UTC (09:00 in South Sudan) and can also be started manually from GitHub Actions.
- Add trusted RSS feeds to `automation/sources.json`. The generator only uses feed titles and summaries from the last three days; it does not claim to have verified the linked articles.
- Add the GitHub Actions secret `OPENAI_API_KEY`. The workflow creates a pull request that updates `daily-posts.js`; review the story and sources before merging it.
- `.github/workflows/deploy-infinityfree.yml` deploys the site after changes are pushed to `main`. Configure the `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`, and `FTP_SERVER_DIR` Actions secrets with values from InfinityFree.
- Keep API and FTP credentials in GitHub Secrets. Never put them in site files.
- The project folder must be pushed to a GitHub repository with the default branch named `main` before either workflow can run.

## Editorial notes

- All Nasir Crisis content is attributed to named sources (HRW, Radio Tamazuj, UNMISS, MSF, The Guardian)
- Casualty figures are not fabricated — they are attributed to the reporting organisation
- Figures covering multiple counties (Nasir + Longechuk + Ulang) are not presented as Nasir-only
- Incident dates and publication dates are distinguished wherever known
- Community and editorial stories marked as placeholder content should be replaced with verified reporting before publication
