# Deployment

GitHub Pages serves this repository's `main` branch at the repository root. `.nojekyll` keeps static assets untouched.

URL: https://karso1.github.io/fretflow-guitar-lab/

Publish `index.html`, `app.js`, `songs.js`, `style.css`, `detail.css`, `lab.html`, `lab.css`, `assets/`, and `vendor/` together. A Git tree / commit update publishes an internally consistent revision.

The content sources and generators are included under `content/` and `tools/`. Screenshots, generated visual directions, local test data and development notes are kept outside the published tree.

Browser-local uploads, favorites and notes are private to the browser origin. No credentials or user-uploaded score files are committed. The previous `fretflow_state`, `fretflow_notes` and training task keys continue to be used by the preserved learning tools.
