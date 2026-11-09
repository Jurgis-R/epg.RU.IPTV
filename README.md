# Russian IPTV EPG

This repository builds a playlist-matched XMLTV guide for:

https://iptv-org.github.io/iptv/languages/rus.m3u

## TV-box EPG URL

Use this URL in the TV box after the first successful GitHub Actions build:

`https://raw.githubusercontent.com/Jurgis-R/epg.RU.IPTV/data/epg.xml.gz`

Uncompressed alternative:

`https://raw.githubusercontent.com/Jurgis-R/epg.RU.IPTV/data/epg.xml`

The `data` branch is generated automatically. The guide is rebuilt every 12 hours and can also be started manually from the repository's Actions tab.

## How the guide is built

- Uses the official [iptv-org/epg grabber](https://github.com/iptv-org/epg).
- Uses [channels.xml](./channels.xml) as the custom channel map. Its `site_id` values identify channels at the upstream EPG sources; its `xmltv_id` values are the exact IDs used by the target M3U.
- Collects programme schedules from the mapped sources, then emits XMLTV channel and programme records under the playlist IDs.
- Validates the generated guide against the current playlist before publishing. A build with too few matching channels or programme records is rejected.
- Publishes both plain XML and gzip XMLTV to the `data` branch.

The guide is not a static channel list: it contains actual `<channel>` and `<programme>` records. The source coverage depends on the upstream providers and their current availability.

## Exact channel-ID cross-check

The playlist snapshot used for the original comparison had 653 entries and 653 unique `tvg-id` values. These were compared against eight upstream channel catalogues:

| Source catalogue | Exact IDs found |
|---|---:|
| epg.iptvx.one | 231 |
| tv.mail.ru | 229 |
| ctc.ru | 1 |
| galamtv.kz | 11 |
| cgates.lt | 4 |
| teliatv.ee (Russian feed) | 21 |
| magticom.ge (Russian channels) | 43 |
| 9tv.co.il (Russian-language Israeli channel) | 1 |
| **Unique IDs across all eight** | **338 / 653** |

The combined map adds **107 IDs** beyond the original IptvX-only map. **315 IDs** had no exact match in those eight catalogues at the time of the comparison. These are catalogue matches, not a guarantee that every matched channel currently has programme data.

## Repository files

- [channels.xml](./channels.xml) — upstream source/site IDs mapped to playlist `tvg-id` values.
- [coverage.csv](./coverage.csv) — playlist entries and source catalogues with exact matches.
- [additional-ids.txt](./additional-ids.txt) — additional exact IDs beyond the original IptvX catalogue.
- [epg-url.txt](./epg-url.txt) — TV-box feed URLs.
- [.github/workflows/build-epg.yml](./.github/workflows/build-epg.yml) — scheduled XMLTV build and publishing workflow.

## Public source information

The upstream [iptv-org/epg project](https://github.com/iptv-org/epg) supports custom channel mapping files and generates XMLTV guides from configured source sites. Its [contribution guide](https://github.com/iptv-org/epg/blob/master/CONTRIBUTING.md) explains that the XMLTV channel ID must match the playlist/database channel ID for programme data to link correctly.

EPG.ONE publicly lists full and Russian-language XMLTV feeds and describes its guide coverage and source fallback on its [official site](https://epg.one/). Those external feeds are not used as the output URL for this repository.

## Upstream source catalogues

- [Target playlist](https://github.com/iptv-org/iptv/blob/gh-pages/languages/rus.m3u)
- [IptvX scraper](https://github.com/iptv-org/epg/tree/master/sites/epg.iptvx.one)
- [Mail scraper](https://github.com/iptv-org/epg/tree/master/sites/tv.mail.ru)
- [CTC scraper](https://github.com/iptv-org/epg/tree/master/sites/ctc.ru)
- [GalamTV scraper](https://github.com/iptv-org/epg/tree/master/sites/galamtv.kz)
- [CGates scraper](https://github.com/iptv-org/epg/tree/master/sites/cgates.lt)
- [Telia TV Estonia Russian feed](https://github.com/iptv-org/epg/tree/master/sites/teliatv.ee)
- [Magticom Georgia](https://github.com/iptv-org/epg/tree/master/sites/magticom.ge)
- [9 канал / Israel](https://github.com/iptv-org/epg/tree/master/sites/9tv.co.il) — official Russian-language schedule
