[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/DizellaCapital/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/DizellaCapital/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# THE SATURDAY LEDGER — Saturday 21 November 2026

A one-page broadsheet front page for 21 November 2026: **36 dated stories,
7 regions, 13 illustrated cards** — COP31 overtime, Riyadh intercepts, Peru
M6.7 quake, BepiColombo at Mercury, the Davao jet, Rutte in Warsaw, Ethiopia
displacement, and more. Warm newsprint, serif headlines, a "21 Nov by the
numbers" strip, a dotted world map with numbered pins for stories 1–13, and
a date-check footer that names the big Friday stories deliberately left out.

## How it is built

- `render.html` is the whole 1024×1024 front page (inline CSS + SVG
  illustrations + a small script that draws the dotted world map and pins
  from the stories' coordinates).
- `render.mjs` screenshots it with Playwright (Chromium) to `entry.png`.
- `main.ts` (Node 22, standard library only) copies `entry.png` to the
  output directory. That is the entry the judge sees.
- `stories_20261121.json` is the verified dataset behind the page: all 36
  stories, dated Saturday 21 November 2026, with region, dateline, source,
  and coordinates for the illustrated stories.

```sh
node render.mjs          # render.html -> entry.png (1024x1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # -> out/entry.png
```

## Sources

All 36 stories verified 21 November 2026 via live web search: Reuters, AP,
AFP, USGS, ESA, CAAP, Kyiv Independent, BBC, PIB, Asahi, FIA/F1,
CoinGecko, Islamic Relief, UN News.
