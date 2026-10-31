# Third-party notices

Project Carlo's own code is under the [AGPL-3.0](LICENSE) and its data under
CC BY 4.0 (see the License section of the [README](README.md)). This file lists
the third-party material the site ships or shows that carries its own terms.
Code dependencies keep their licenses in their own packages; `pnpm licenses
list` shows the web app's.

## Fonts

The web app bundles these fonts, from [Fontsource](https://fontsource.org),
and serves them with the site. Both are licensed under the
[SIL Open Font License, Version 1.1](https://openfontlicense.org), which allows
bundling, embedding and redistributing them with any software as long as the
fonts themselves are not sold on their own. The shipped font files carry their
copyright notice and a link to the license in their metadata.

- **Cardo** (`@fontsource/cardo`): Copyright (c) 2002-2011, David J. Perry
  (hospes02@scholarsfonts.net).
- **EB Garamond** (`@fontsource-variable/eb-garamond`): Copyright 2017 The EB
  Garamond Project Authors (https://github.com/octaviopardo/EBGaramond12).

The share images in `apps/web/public/` are set in Cardo and EB Garamond; the
Open Font License places no conditions on images made with a font.

## Maps and geographic data

- **Map tiles** come from OpenStreetMap's tile servers
  (`tile.openstreetmap.org`), under the
  [OpenStreetMap tile usage policy](https://operations.osmfoundation.org/policies/tiles/).
  Every map credits "© OpenStreetMap contributors" with a link to
  https://www.openstreetmap.org/copyright, as the policy requires.
- **Coordinates from OpenStreetMap** (churches looked up in Nominatim or taken
  from an OpenStreetMap node, and the town centers in
  `apps/web/src/data/cityCenters.json`) are © OpenStreetMap contributors,
  available under the
  [Open Database License](https://opendatacommons.org/licenses/odbl/). See the
  README's License section for which church coordinates these are.
- **Leaflet**, the map library, is under the BSD 2-Clause license.

## Parish bulletins

The bulletins the pipeline reads belong to their parishes. They are not part
of this repository and not covered by its licenses.
