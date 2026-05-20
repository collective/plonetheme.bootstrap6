Initial alpha release of ``plonetheme.bootstrap6``.

A new Plone 6.2 Classic UI theme based on **Bootstrap 6 alpha**, replacing
Barceloneta's Bootstrap 5 foundation. Highlights:

- Bootstrap 6 alpha with native ``@use``/``@forward`` Sass module system —
  no deprecated ``@import``.
- Plone brand color (``--primary-base``) and state colors (``--plone-state-*``)
  emitted as CSS custom properties on ``:root``; dark-mode variant via
  ``@media (prefers-color-scheme: dark)`` and ``[data-bs-theme="dark"]``.
- Bootstrap 5 compatibility shim (``_bs5-compat.scss``) so existing Classic UI
  templates render correctly without changes: dropdown → menu aliases, named
  button variants (``btn-primary`` etc.), offcanvas → drawer, modal → dialog,
  responsive utility infix classes, navbar-expand backport, and ``--bs-*``
  CSS property aliases for Mockup components.
- Standard Bootstrap 6 breakpoints (``lg: 1024px``, ``xl: 1280px``,
  ``2xl: 1536px``).
- Diazo rules mirroring the Barceloneta structure for drop-in compatibility.
