# plonetheme.bootstrap6

> [!NOTE]
> **The package name `plonetheme.bootstrap6` is a working title** and is still open
> for discussion. The final name may change before any stable release.

A Plone 6.2 Classic UI theme based on **Bootstrap 6**.

> [!WARNING]
> **This theme is under active development and not yet production-ready.**
> It depends on [Bootstrap 6](https://v6-dev--twbs-bootstrap.netlify.app/docs/6.0/), which is
> currently in **alpha** and subject to breaking changes without notice.
> The Bootstrap 6 alpha API — including configuration variables, mixins, and
> class names — may change in any future alpha or beta release.
> Do not use this theme in production environments.

[![PyPI version](https://img.shields.io/pypi/v/plonetheme.bootstrap6.svg)](https://pypi.org/project/plonetheme.bootstrap6/)
[![Bootstrap 6 alpha](https://img.shields.io/badge/Bootstrap-6_alpha-orange.svg)](https://v6-dev--twbs-bootstrap.netlify.app/docs/6.0/)
[![Development status](https://img.shields.io/badge/status-under_development-red.svg)](https://github.com/plone/plonetheme.bootstrap6)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

## Overview

`plonetheme.bootstrap6` is a Diazo-based Plone theme that brings Bootstrap 6 to the Plone Classic UI. Unlike Barceloneta (Bootstrap 5), it uses Bootstrap 6's native `@use`/`@forward` Sass module system and its standard breakpoints. Whether this theme becomes the basis for Plone 7's Classic UI is an idea currently under evaluation.

Key characteristics:

- **Bootstrap 6 alpha** ([docs](https://v6-dev--twbs-bootstrap.netlify.app/docs/6.0/), [`twbs/bootstrap#v6-dev`](https://github.com/twbs/bootstrap/tree/v6-dev)) with native `@use`/`@forward` Sass module system — no deprecated `@import`
- **Plone Classic UI compatible** — uses the same HTML selectors as Barceloneta (`#content-header`, `#portal-globalnav-wrapper`, `#portal-column-content`, etc.)
- **Dark mode support** via Bootstrap 6 color-mode system (`@media (prefers-color-scheme: dark)`)
- **Standard Bootstrap 6 breakpoints** (`lg: 1024px`, `xl: 1280px`, `2xl: 1536px`) — no barceloneta backports
- **CSS custom properties** for Plone colors (`--plone-link`, `--plone-state-*`) without a vendor prefix (Bootstrap 6 dropped `--bs-`)

## Requirements

| Dependency         | Version    |
|--------------------|------------|
| Plone              | ≥ 6.2      |
| plone.app.theming  | any        |
| Python             | ≥ 3.10     |
| Node.js / pnpm     | for SCSS builds only |

## Installation

### Python package

Add `plonetheme.bootstrap6` to your Plone instance's `install_requires` or buildout `eggs`:

```ini
[instance]
eggs +=
    plonetheme.bootstrap6
```

Then activate the theme in the Plone control panel under *Site Setup → Theming*, or via a Generic Setup profile that depends on this package.

### Activate via Generic Setup

The included `profiles/default` profile sets the active theme automatically when applied:

```xml
<!-- profiles/default/metadata.xml -->
<dependencies>
    <dependency>profile-plonetheme.bootstrap6:default</dependency>
</dependencies>
```

## SCSS Structure

The theme is built from a set of modular SCSS files inside `scss/`. Bootstrap 6 requires that its configuration variables are set *before* the first `@use "bootstrap/scss/..."` call — this is handled centrally in `_bs-forward.scss`.

```
scss/
├── _bs-forward.scss        # Bootstrap 6 config + forward (must be first)
├── _plone-colors.scss      # Plone brand colors and state color maps
├── _plone-root.scss        # CSS custom properties emitted on :root
├── bootstrap6.scss       # Main entry point (compiled to CSS)
└── plone/
    ├── _scaffolding.scss   # Base layout, skip nav, link colors
    ├── _header.scss        # #content-header, logo, livesearch
    ├── _sitenav.scss       # .navbar-bootstrap6, dropdowns, offcanvas
    ├── _toolbar.scss       # #edit-bar (Classic UI edit toolbar)
    ├── _breadcrumbs.scss   # #above-content-wrapper
    ├── _content.scss       # Column layout, #content, related items
    ├── _portlets.scss      # .portletWrapper, .portlet, navigation portlet
    ├── _forms.scss         # .field, form widgets, login, search
    └── _footer.scss        # #portal-footer-wrapper, doormat, site-actions
```

### Key Bootstrap 6 differences from barceloneta (Bootstrap 5)

| Topic | Bootstrap 5 (barceloneta) | Bootstrap 6 (bootstrap6) |
|---|---|---|
| Sass API | `@import` (global namespace) | `@use` / `@forward` (module-scoped) |
| Configuration | `$var !default;` before `@import` | `@use "config" with ($var: value)` |
| Variable files | `_variables.scss`, `_variables-dark.scss` | `_config.scss`, `_colors.scss`, `_theme.scss` |
| CSS variable prefix | `--bs-body-bg` | `--body-bg` (no prefix) |
| Color functions | `darken()` / `lighten()` | `color.adjust()` via `@use "sass:color"` |
| Z-index names | `$zindex-dropdown`, `$zindex-offcanvas` | `$zindex-menu`, `$zindex-drawer` |
| Breakpoint `lg` / `xl` / `xxl` | `992px` / `1200px` / `1400px` | `1024px` / `1280px` / `1536px` (standard BS6; `xxl` renamed to `2xl`) |
| Color system | HSL | oklch |
| RFS / `font-size()` mixin | present | removed |

## Bootstrap 5 Compatibility Shim

Plone Classic UI templates were written against Bootstrap 5. Several component names changed in Bootstrap 6. The file `scss/_bs5-compat.scss` bridges the gap so that existing templates render correctly without modification.

> [!NOTE]
> This shim is a **transitional measure**. It will be removed once the upstream
> Plone templates have been updated to Bootstrap 6 class names. To remove it,
> delete the `@use "bs5-compat"` line in `scss/bootstrap6.scss`.

### Covered components

#### Dropdown → Menu

Bootstrap 6 renamed the dropdown component to *menu*.

| BS5 class | BS6 equivalent | Notes |
|---|---|---|
| `.dropdown` | `.dropdown` | unchanged (position wrapper) |
| `.dropdown-toggle` | — | caret re-added via `::after` in shim |
| `.dropdown-menu` | `.menu` | full style set, uses BS6 CSS variables |
| `.dropdown-item` | `.menu-item` | hover / active / disabled states |
| `.dropdown-header` | `.menu-header` | section label |
| `.dropdown-divider` | `.menu-divider` | horizontal rule |
| `.dropdown-menu-end` | — | right-align alias |
| `.dropdown-menu-md-end` | — | responsive right-align |

**JavaScript note**: `data-bs-toggle="dropdown"` must be changed to `data-bs-toggle="menu"` in templates once the Bootstrap 6 JS bundle is active. The shim covers the CSS side only.

#### Button color variants

Bootstrap 6 replaced the colour-named button classes with a functional modifier system (`btn-solid`, `btn-outline`, …) driven by `--theme-*` CSS custom properties. The shim re-introduces the old names by setting the `--btn-*` variables that the base `.btn` rule reads.

| BS5 class | BS6 approach | Shim |
|---|---|---|
| `.btn-primary` | `.btn.btn-solid` + `--theme-*: var(--primary-*)` | ✓ |
| `.btn-secondary` | `.btn.btn-solid` + `--theme-*: var(--secondary-*)` | ✓ |
| `.btn-success` | `.btn.btn-solid` + `--theme-*: var(--success-*)` | ✓ |
| `.btn-danger` | `.btn.btn-solid` + `--theme-*: var(--danger-*)` | ✓ |
| `.btn-warning` | `.btn.btn-solid` + `--theme-*: var(--warning-*)` | ✓ |
| `.btn-info` | `.btn.btn-solid` + `--theme-*: var(--info-*)` | ✓ |
| `.btn-light` / `.btn-dark` | `.btn.btn-subtle` / `.btn.btn-solid` | ✓ |
| `.btn-outline-{color}` | `.btn.btn-outline` + `--theme-*` | ✓ (all 8 variants) |

Unchanged classes (`btn`, `btn-sm`, `btn-lg`, `btn-link`) still exist natively in Bootstrap 6 and do not need the shim.

#### Directional dropdown containers

Bootstrap 6 removed `.dropend` / `.dropstart` / `.dropup`. Side-opening menus now use `data-bs-placement`. The shim restores positioning and caret styles for the old class names.

| BS5 class | Notes |
|---|---|
| `.dropend` | submenu opens inline-end (right in LTR); right-pointing caret |
| `.dropstart` | submenu opens inline-start (left in LTR); left-pointing caret |
| `.dropup` | submenu opens upward |

#### Offcanvas → Drawer

Bootstrap 6 replaced the offcanvas panel with a native `<dialog>`-based drawer component. Plone Classic UI uses Bootstrap 5 offcanvas for the mobile navigation panel (see `#offcanvasNavbar` in `index.html`) and Bootstrap 5 JS controls the `.show` state.

| BS5 class | BS6 equivalent | Notes |
|---|---|---|
| `.offcanvas` | `.drawer` | position, slide-in, visibility toggle via `.show` |
| `.offcanvas-end` | `.drawer-end` | slides in from the right |
| `.offcanvas-start` | `.drawer-start` | slides in from the left |
| `.offcanvas-top` | `.drawer-top` | slides in from the top |
| `.offcanvas-bottom` | `.drawer-bottom` | slides in from the bottom |
| `.offcanvas-header` | `.drawer-header` | header row with close button |
| `.offcanvas-title` | `.drawer-title` | title text |
| `.offcanvas-body` | `.drawer-body` | scrollable content area |
| `.offcanvas-backdrop` | `::backdrop` (native) | semi-transparent overlay; `.show` triggers visibility |

At the `navbar-expand-{bp}` breakpoint the offcanvas is shown inline (always visible, no slide-in), matching Bootstrap 5 navbar behaviour.

#### Modal → Dialog

Bootstrap 6 replaced the `.modal` component with the native `<dialog>` element styled via `.dialog-*`. Mockup's `pat-plone-modal` pattern (`data-pat-plone-modal` / `.pat-plone-modal`) still generates Bootstrap 5 `.modal` HTML (plain `<div>` elements, not `<dialog>`). This shim re-introduces all `.modal-*` CSS using Bootstrap 6 design tokens.

| BS5 class | BS6 equivalent | Notes |
|---|---|---|
| `.modal` | `.dialog` | full-viewport container; `.show` triggers visibility |
| `.modal-backdrop` | `::backdrop` (native) | `.show` **and** `.backdrop-active` supported (Mockup uses the latter) |
| `.modal-dialog` | — | no inner wrapper in BS6; replicated for Mockup's `<div>` structure |
| `.modal-content` | `.dialog` directly | styled card; uses BS6 `--border-color-translucent`, `--radius-7`, `--box-shadow-lg` |
| `.modal-header` | `.dialog-header` | title + close button row |
| `.modal-title` | `.dialog-title` | heading text |
| `.modal-body` | `.dialog-body` | main content area |
| `.modal-footer` | `.dialog-footer` | action button row |
| `.modal-sm` / `.modal-lg` / `.modal-xl` | `.dialog-sm` / `.dialog-lg` / `.dialog-xl` | width variants |
| `.modal-fullscreen` | `.dialog-fullscreen` | full-viewport variant |
| `.modal-dialog-centered` | native (dialog centres via `margin: auto`) | replicated for `<div>` structure |
| `.modal-dialog-scrollable` | — | scrollable body variant |
| `body.modal-open` | `.dialog-open` | prevents background scroll while open |

**Mockup note**: `pat-plone-modal` adds `.backdrop-active` (not `.show`) to its backdrop element. The shim accepts both.

### What is *not* covered

| BS5 feature | Status |
|---|---|
| `.nav-tabs`, `.nav-pills`, `.nav-underline` | unchanged in BS6, no shim needed |
| `collapse` | still present in BS6 |

## Building CSS

See [DEVELOPMENT.md](DEVELOPMENT.md) for the full development workflow.

Quick build:

```shell
cd path/to/plonetheme.bootstrap6
pnpm install
pnpm build
```

The compiled CSS lands in `src/plonetheme/bootstrap6/theme/css/`.

## Theming & Customisation

The easiest way to customise bootstrap6 is to create a new theme package that depends on it and override individual SCSS partials. Alternatively, use the Diazo TTW editor in Plone's theming control panel to add extra CSS rules on top.

To change a Bootstrap 6 config variable (e.g. primary color), you need to do it via `@use "bootstrap/scss/config" with (...)` **before** any other Bootstrap import — follow the pattern in `_bs-forward.scss`.

## Diazo Theme Rules

The Diazo rules are defined in `src/plonetheme/bootstrap6/theme/rules.xml` and mirror the structure of `plonetheme.barceloneta`.

## Changelog

See [CHANGES.md](CHANGES.md).

## Source Code and Contribution

- GitHub: <https://github.com/plone/plonetheme.bootstrap6>
- Issue tracker: <https://github.com/plone/plonetheme.bootstrap6/issues>
- Contributing guide: [DEVELOPMENT.md](DEVELOPMENT.md)

Please read the [Plone contributor agreement](https://plone.org/foundation/contributors-agreement) before submitting a pull request.

## License

GNU General Public License v2. See [LICENSE](LICENSE) for details.
