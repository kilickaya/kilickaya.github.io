# Publication illustration system

Seven original SVG concept illustrations, drawn for Mert Kilickaya's research website. These are editorial explanations of each paper's central idea, not reproductions of its architecture diagrams or quantitative results. Original figures remain archived in `images/`; research entries display the unified illustrations.

## Shared drawing language

- Canvas: 800 × 500, consistent 8:5 proportions and generous margins.
- Warm oat background `#eee8dc`, paper surfaces `#f8f5ed`, charcoal lines `#514b40`.
- Muted terracotta `#ad7056` and sage `#7b8873` identify related elements.
- Rounded 2.5-unit strokes, flat fills, simple geometry, sparse readable labels.
- No gradients, shadows, stock photography, invented scores or decorative metrics.
- Each SVG includes an accessible title and description; website image alternatives describe the concept.

## Assets and primary sources

| Asset                          | Concept                                                    | Paper                                                        |
| ------------------------------ | ---------------------------------------------------------- | ------------------------------------------------------------ |
| `hytas.svg`                    | Spectral data, candidate search, selected architecture     | [HyTAS](https://arxiv.org/abs/2407.16269)                    |
| `hylite.svg`                   | Local context and spectra jointly inform classification    | [HyLITE](https://arxiv.org/abs/2309.01561)                   |
| `label-efficient-learning.svg` | Three supervision regimes learning over time               | [Survey](https://arxiv.org/abs/2302.00353)                   |
| `vinil.svg`                    | Two instance views, self-supervision, continued learning   | [VINIL](https://arxiv.org/abs/2301.11417)                    |
| `align-former.svg`             | Image-level supervision, alignment, localized interactions | [Align-Former](https://arxiv.org/abs/2112.00492)             |
| `composition-aware-search.svg` | Composition and representation change together             | [Composition-aware search](https://arxiv.org/abs/2010.14438) |
| `caption-evaluation.svg`       | Semantic comparison of reference and candidate captions    | [Caption evaluation](https://arxiv.org/abs/1612.07600)       |

Regenerate the illustrations with `python3 scripts/draw-publications.py` from the repository root. The generator has no external dependencies and owns all seven SVGs. Adjust the shared palette and drawing helpers there to preserve consistency. The images retain their warm paper palette in either website theme.
