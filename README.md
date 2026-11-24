# The World in One Day — Tuesday, 24 November 2026

[![make.fun competition](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![make.fun rank](https://make.fun/badge/news-image-20261124/Jeytm/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![make.fun reward](https://make.fun/badge/news-image-20261124/Jeytm/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

Sum up 24 November's world news in one image — an entry for the
[make.fun bounty](https://make.fun/bounty/news-image-20261124).

## The poster

A single 1024×1024 front page, "THE WORLD IN ONE DAY", dated Tuesday,
24 November 2026. Lead story: **fire at a candy factory in Banten kills
at least 24** — the day's deadliest single event. Around it, the day's
other headlines across regions and fields:

- **Ukraine war** — Kyiv region hit; cargo ship Sparta II burns in the
  Gulf of Finland after a drone attack.
- **Climate / COP31** — talks end divided in Antalya, no agreement on
  stronger language to phase out fossil fuels.
- **India–Nepal** — the Saryu–Kamala Express rail link opens.
- **Sport** — Verstappen takes Las Vegas; Alcaraz wins the ATP Finals;
  Pant hits 128.
- **Markets** — Sensex slides 1,484; the SpiceJet crisis deepens.

Every story is drawn by hand in code (no photos, no network): a factory
fire, a burning cargo ship, a divided globe, a new express train, a
checkered flag and trophy, and a falling market chart.

## How it works

- `render.py` — renders the poster deterministically (fixed seed, no
  network, no clock) and writes `entry.png` (1024×1024, 423,509 bytes).
- `main.ts` — the entry point: validates the PNG magic bytes and the
  1 MiB cap, copies `entry.png` to `/output/entry.png`, and verifies the
  copy is byte-identical (SHA-256).

```sh
python3 render.py   # regenerate entry.png
node main.ts        # write /output/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
