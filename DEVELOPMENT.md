# Development Guide — plonetheme.bootstrap6

This document explains how to set up a local development environment, work with the SCSS sources, run the build, and release the package.

---

## Prerequisites

### Python environment

A Plone 6 buildout or `pip`-based environment with `plone.app.theming` and its dependencies installed. The `src/plonetheme.bootstrap6` checkout must be on the Python path (e.g. via a develop egg or `pip install -e .`).

### Node.js / pnpm

The CSS build uses [Dart Sass](https://sass-lang.com/dart-sass), [PostCSS](https://postcss.org/), and [clean-css](https://github.com/clean-css/clean-css-cli). All are managed as devDependencies and installed via [pnpm](https://pnpm.io/).

Install pnpm via corepack (recommended):

```shell
corepack prepare pnpm@latest --activate
```

or via npm:

```shell
npm install -g pnpm@latest
```

Verify:

```shell
pnpm --version
```

---

## Install dependencies

From the package root (`src/plonetheme.bootstrap6/`):

```shell
pnpm install
```

To update all dependencies to their latest allowed versions:

```shell
pnpm update
```

To interactively review available upgrades:

```shell
pnpm update --interactive --latest
```

---

## SCSS development workflow

### Watch mode

Start a file watcher that recompiles whenever a `.scss` file changes:

```shell
pnpm watch
```

The compiled CSS is written directly to `src/plonetheme/bootstrap6/theme/css/`.

### Single compile

Compile, auto-prefix, and minify in one step:

```shell
pnpm build
```

Or run each step individually:

```shell
pnpm run css-compile-main   # Dart Sass → expanded CSS + source map
pnpm run css-prefix-main    # PostCSS autoprefixer
pnpm run css-minify-main    # clean-css → .min.css + source map
```

### Lint

```shell
pnpm run css-lint
```

Stylelint is configured via `.stylelintrc` (inherited from the Bootstrap config `stylelint-config-twbs-bootstrap`).

---

## SCSS architecture

### Bootstrap 6 module system

Bootstrap 6 uses Sass's `@use`/`@forward` module system. Variables are **not** globally accessible after a plain `@import`; they must be configured once via:

```scss
@use "bootstrap/scss/config" with (
  $breakpoints: (...),
  $enable-dark-mode: true,
  ...
);
```

This call **must happen before** any other `@use "bootstrap/scss/..."`. In this theme it is centralised in `scss/_bs-forward.scss`, which is the first `@use` in `scss/bootstrap6.scss`.

### File overview

| File | Purpose |
|---|---|
| `scss/_bs-forward.scss` | Configure Bootstrap 6 config vars; forward all Bootstrap styles |
| `scss/_plone-colors.scss` | Plone brand + state colors as Sass variables |
| `scss/_plone-root.scss` | Emit `--plone-*` CSS custom properties on `:root` |
| `scss/bootstrap6.scss` | Main entry point — `@use`s everything in order |
| `scss/plone/_scaffolding.scss` | Page layout, skip nav, link colors |
| `scss/plone/_header.scss` | Header, logo, livesearch |
| `scss/plone/_sitenav.scss` | Main navbar, dropdowns, offcanvas |
| `scss/plone/_toolbar.scss` | Edit bar (`#edit-bar`) |
| `scss/plone/_breadcrumbs.scss` | Above-content breadcrumb area |
| `scss/plone/_content.scss` | Column layout, document content, related items |
| `scss/plone/_portlets.scss` | Portlet wrappers, navigation portlet |
| `scss/plone/_forms.scss` | Form fields, widgets, login, search |
| `scss/plone/_footer.scss` | Footer, doormat, site actions |

### Adding a new component

1. Create `scss/plone/_mycomponent.scss`.
2. Start with the required imports:
   ```scss
   @use "bootstrap/scss/config" as *;
   // add further @use calls as needed, e.g.:
   // @use "bootstrap/scss/layout/breakpoints" as *;
   // @use "sass:color";
   ```
3. Add your styles.
4. Add `@use "plone/mycomponent";` to `scss/bootstrap6.scss`.

### Overriding Bootstrap 6 configuration

To change a Bootstrap 6 config variable (e.g. primary color, border-radius), edit the `with (...)` block in `scss/_bs-forward.scss`. Only variables declared `!default` in `bootstrap/scss/_config.scss` can be overridden there. Check the full list:

```
node_modules/bootstrap/scss/_config.scss
```

---

## Diazo theme rules

The Diazo rules live in:

```
src/plonetheme/bootstrap6/theme/rules.xml
```

The HTML template used by Diazo is:

```
src/plonetheme/bootstrap6/theme/index.html
```

Use Plone's *Site Setup → Theming* to test rule changes without restarting the server (TTW mode).

---

## Python package development

Install in development mode inside your Plone environment:

```shell
pip install -e path/to/plonetheme.bootstrap6
```

or with buildout, add to `develop`:

```ini
[buildout]
develop += src/plonetheme.bootstrap6
```

Run the test suite (requires a running Plone test layer):

```shell
cd path/to/buildout
bin/test -s plonetheme.bootstrap6
```

---

## Release Instructions

> You need write access to both PyPI and npm to publish a release.

### Python / PyPI release

Use [zest.releaser](https://zestreleaser.readthedocs.io/) from the buildout environment:

```shell
cd src/plonetheme.bootstrap6
fullrelease
```

This bumps the version in `setup.py`, creates a git tag, and publishes to PyPI.

### npm release

After the PyPI release, update the version in `package.json` to match:

```shell
pnpm version 1.0.0
```

Then publish:

```shell
pnpm publish
```

### Pre-releases

Based on <https://survivejs.com/maintenance/packaging/publishing/#publishing-a-pre-release-version>

```shell
pnpm version 1.0.0-beta.1
pnpm publish --tag beta
```

To consume the pre-release:

```shell
pnpm install @plone/plonetheme-bootstrap6@beta
```

---

## Compatibility notes

This theme targets **Bootstrap 6** (v6 alpha) and is **not** compatible with Bootstrap 5. The key differences that affect custom SCSS on top of this theme:

- Use `@use "sass:color"` and `color.adjust()` instead of the deprecated `lighten()`/`darken()` functions.
- Use `@use "bootstrap/scss/config" as *` to access Bootstrap config variables (`$enable-*`, `$zindex-*`, `$spacer`, etc.) — they are no longer globally available.
- CSS custom properties have **no prefix**: `--body-bg`, `--border-color` (not `--bs-body-bg`).
- The breakpoint `xxl` from Bootstrap 5 is now called `2xl`.
- Z-index names changed: `$zindex-dropdown` → `$zindex-menu`, `$zindex-offcanvas` → `$zindex-drawer`.
