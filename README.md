# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b78-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b78-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up 23 November 2026's world news: the AI rout that hit Asian
markets, the UN chief's call to regulate AI before it is too late, and the US lead
over China falling to a record low — plus 28 more stories from every region.

## What's inside

- **3 hero stories** — Kospi −3.3% (4,708.54, −161 pts, intraday −5.8%), Guterres at the
  Bridgetown summit (150 delegates back a risk framework), Asia Power Index 2026
  (US 78.9 vs China 73.6, gap 5.3 — narrowest since 2018).
- **10 more of the day** — Bessent vs Nvidia, the NCIC hack probe, Trump on Iran,
  Nasdaq futures +3%, Skubal's $450M Mets deal, Tom Jackson at 75, states suing
  SpaceX, Anthropic's $107.3B IPO (raised at $83/share), Poland's missile-airspace
  claim, and the Russian nuclear-satellite warning.
- **18 also on Monday**, a world map with 13 numbered pins, and a red DATE CHECK box
  that keeps 22/21/19 November stories out of the 23 November record.

## How it is built

`draw.py` (PIL) renders `entry.png` (1024×1024, under 1 MiB) deterministically.
`main.py` is stdlib-only: it validates the PNG header by hand and copies it to
`$MAKEFUN_OUTPUT_DIR/entry.png`.

## License

MIT — see `LICENSE`.
