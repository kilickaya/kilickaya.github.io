# Organization marks

Transparent monochrome SVG adaptations for the career timeline. All five use a 96 × 96 canvas and the same optical margins. The website loads them as ordinary images with document-relative paths, so they also work in direct file previews and under a subdirectory. They use the site's stone color on a soft oat surface, with a brighter treatment in dark mode. Organization names remain visible text; the marks are decorative to avoid repeating names to screen readers.

## Sources

- `agendia.svg`: fingerprint silhouette traced from the existing `images/Agendia.png`. The small tagline and wordmark are omitted at icon size.
- `tu-eindhoven.svg`: TU/e silhouette traced from the existing `images/TUE.png`.
- `quva.svg`: laboratory emblem traced from the square symbol in the existing `images/QUVA.png`. The small text below the emblem is omitted at icon size.
- `huawei.svg`: flower silhouette traced from the existing `images/Huawei.jpg`, with its gradients flattened.
- `greyparrot.svg`: parrot symbol paths from [Greyparrot's official SVG](https://www.greyparrot.ai/hubfs/gpr01/Global%20styles/logo-dark.svg), linked by the [Greyparrot homepage](https://www.greyparrot.ai/). The downloaded original is retained as `source/greyparrot.svg`; the wordmark is omitted at icon size.

These are site-specific monochrome treatments of recognizable organization marks. Original source assets are unchanged.

Regenerate with `python3 scripts/draw-organization-marks.py`. The tracing helper uses Pillow; the website itself remains buildless and has no additional browser dependencies. The generator preserves transparent cutouts and uses deterministic silhouette simplification rather than generating new brand symbols.
