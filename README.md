[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/DizellaCapital/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/DizellaCapital/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Saturday 21 November 2026 — The World in One Day

[![Bounty: news-image-20261121](https://make.fun/c/news-image-20261121)](https://make.fun/c/news-image-20261121)
[![Enter via referral qxacafna](https://make.fun/r/qxacafna)](https://make.fun/r/qxacafna)
[![make.fun](https://make.fun)](https://make.fun)

One image that sums up the world's news of **Saturday 21 November 2026**:
40 sourced stories, 7 regions, every one dated — COP31 into overtime with no
deal, Russian strikes kill 12 in Ukraine, three Houthi missiles downed over
Riyadh, BepiColombo reaches Mercury after eight years, Rutte in Warsaw.

## The entry

- `entry.png` — the front page, 1024×1024, drawn in code (see `render.py`).
  Classic newspaper grammar: cream serif masthead, a stat strip of the day's
  six biggest numbers under the masthead, a region bar, three large hero scenes,
  ten vignettes in two rows of five, a dotted world map with numbered pins at the
  bottom, briefs numbered 14–40, and a date-check footer listing what was
  deliberately left out because it happened on another day.
- `render.py` — draws `entry.png` with PIL only. No network, no randomness, no
  external assets: run it twice and the bytes are identical.
- `main.ts` — the program the harness runs. It copies `entry.png` byte-identical
  to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png` locally).

## Build it

```sh
python3 render.py            # writes entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
cmp entry.png out/entry.png  # byte-identical
```

## Sources

Every story is sourced and dated in `NEWS-RESEARCH.md` (in the work directory,
not shipped here): Reuters, AP, AFP, ESA, BBC, Kyiv Independent, PIB, ATP and
others, all 21 November 2026. Confidence is marked per story (Officials say /
Reported / Ongoing / Estimate). The date-check footer names the Friday and
Thursday stories that were left out on purpose — the Poland missile landings,
Kyiv's bridges, Cyclone Akvan's landfall, Bayer's $7.25bn settlement,
Anthropic's $81.3bn IPO, and more.

## Bounty

- Competition: [news-image-20261121 — Sum up 21 November's world news in one image](https://make.fun/c/news-image-20261121)
- Pot: $100 — 1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20
- Deadline: 23 November 2026, 07:00 WIB
- Entrant: [@dizellacapital](https://make.fun/r/qxacafna) — referral code `qxacafna`

## License

MIT — see `LICENSE`.
