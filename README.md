# Russian IPTV EPG

Target playlist:
https://iptv-org.github.io/iptv/languages/rus.m3u

## Primary XMLTV URL

`https://iptvx.one/epg/epg_noarch.xml.gz`

This remains the primary URL because it is directly configured by the `epg.iptvx.one` scraper in `iptv-org/epg`. The scraper configuration specifies a 2-day guide. The endpoint returned a gzip response during checking, but the programme records could not be parsed in this environment.

Use the primary URL as the XMLTV source in your TV box. Keep the M3U playlist unchanged.

## Exact channel-ID cross-check already completed

The playlist snapshot used for the original comparison had 653 entries and 653 unique `tvg-id` values. These were compared against five channel catalogues in `iptv-org/epg`:

| Source catalogue | Exact IDs found |
|---|---:|
| epg.iptvx.one | 231 |
| tv.mail.ru | 229 |
| ctc.ru | 1 |
| galamtv.kz | 11 |
| cgates.lt | 4 |
| **Unique IDs across all five** | **319 / 653** |

The combined match adds **88 IDs** beyond the original iptvx-only map. **334 IDs remain unmatched** in those five catalogues.

Repository files:
- [channels.xml](./channels.xml) — upstream source/site IDs mapped to exact playlist `tvg-id` values.
- [coverage.csv](./coverage.csv) — all playlist entries and source catalogues with exact matches.
- [additional-ids.txt](./additional-ids.txt) — additional exact IDs beyond the original iptvx catalogue.
- [epg-url.txt](./epg-url.txt) — primary URL and additional feed candidates.

## Smotrim

The two supplied variants are:
- `https://smotrim.uno/epg/epg.xml`
- `https://smotrim.uno/epg/epg.xml.gz`

The uncompressed `.xml` endpoint responded with `text/xml` when opened, but the web reader cannot parse XML payloads. A historical Jellyfin log from August 2024 for the gzip URL listed IDs such as `X2na2`, `Xmir`, and `Xru-tv`. These are not exact matches for target playlist IDs such as `2x2.ru@SD`, `Mir.ru@SD`, and `RUTV.ru@SD`. These examples are not an exhaustive current channel list.

Therefore no exact Smotrim coverage count is claimed, and no speculative mappings were added to `channels.xml`.

## EPG.ONE / former EPG it999

The supplied old address:
`http://epg.it999.ru/edem.xml`

redirects to:
`http://epg.one/edem.xml`

EPG.ONE's own page identifies it as the new domain for EPG it999 and says old it999-domain links were scheduled to be disabled after 15 May 2024. It lists the following formats:
- `http://epg.one/edem.xml` — simplified, uncompressed XMLTV for the current day; programme title only, no description.
- `http://epg.one/edem.xml.gz` — compressed Edem feed.
- `https://epg.one/ru2.xml.gz` and `https://epg.one/ru.xml.gz` — Russian-language channel packs.
- `https://epg.one/epg.xml.gz` — full channel pack.

EPG.ONE describes its full guide as using multiple programme sources and covering about a week forward and backward. Its own site also states that it uses fallback sources when a programme is missing from one source.

The exact XMLTV IDs in these feeds have not been extracted and cross-matched against all 653 target playlist IDs here. Do not treat the provider's claim of broad coverage as proof that every playlist ID matches.

## Other public Russian EPG candidates

- IPTV-EPG.org Russia: `https://iptv-epg.org/files/epg-ru.xml`
- TeleGuide: `https://www.teleguide.info/download/new3/xmltv.xml.gz`
- IptvX full guide: `https://iptvx.one/epg/epg.xml.gz`

Their exact `tvg-id` coverage against this playlist has not been established here.

## Upstream catalogues

- Playlist: https://github.com/iptv-org/iptv/blob/gh-pages/languages/rus.m3u
- IptvX scraper: https://github.com/iptv-org/epg/tree/master/sites/epg.iptvx.one
- Mail scraper: https://github.com/iptv-org/epg/tree/master/sites/tv.mail.ru
- CTC scraper: https://github.com/iptv-org/epg/tree/master/sites/ctc.ru
- GalamTV scraper: https://github.com/iptv-org/epg/tree/master/sites/galamtv.kz
- CGates scraper: https://github.com/iptv-org/epg/tree/master/sites/cgates.lt

`channels.xml` is a channel-mapping catalogue, not a programme guide. The primary XMLTV feed is still hosted by IptvX. No merged XMLTV file is generated or hosted by this repository.
