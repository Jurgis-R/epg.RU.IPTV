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

## Additional feeds requested for comparison

### Smotrim

`https://smotrim.uno/epg/epg.xml.gz`

The endpoint returned a gzip response during checking. A public Jellyfin log from August 2024 shows this URL being loaded as XMLTV and lists channel IDs such as `X2na2`, `Xmir`, and `Xru-tv`. Those IDs differ from the target playlist's IDs (for example, `2x2.ru@SD`, `Mir.ru@SD`, and `RUTV.ru@SD`). This indicates name-level channel candidates, not exact ID matches. The available log is historical and does not establish the current feed's complete channel list or current schedule freshness.

The gzip XML itself could not be downloaded and parsed in this environment. Therefore no exhaustive Smotrim ID coverage count is claimed, and no speculative mappings were added to `channels.xml`.

### EPG.ONE / former EPG it999

The provider's own page says EPG.ONE is the new domain for EPG it999 and that the old it999 domain was scheduled to be disabled after 15 May 2024. The old URL supplied for checking is therefore legacy:

`http://epg.it999.ru/edem.xml.gz`

Use the current EPG.ONE domain instead:
- `http://epg.one/edem.xml.gz` — replacement for the old Edem endpoint, as listed by a recent IPTV guide.
- `https://epg.one/ru2.xml.gz` — Russian-language XMLTV feed.
- `https://epg.one/ru.xml.gz` — Russian-language XMLTV feed.
- `https://epg.one/epg.xml.gz` — full XMLTV feed.

EPG.ONE describes its guide as combining multiple programme sources and offering about a week of guide data. Its own site lists the Russian-only feeds. However, the feed payload was not parsed here, so exact `tvg-id` overlap with the 653 playlist entries remains unverified.

## Other public Russian EPG candidates

- IPTV-EPG.org Russia: `https://iptv-epg.org/files/epg-ru.xml`
- TeleGuide: `https://www.teleguide.info/download/new3/xmltv.xml.gz`
- IptvX full guide: `https://iptvx.one/epg/epg.xml.gz`

These are candidate alternatives, not merged into the primary feed. Their exact `tvg-id` coverage against this playlist has not been established here.

## Upstream catalogues

- Playlist: https://github.com/iptv-org/iptv/blob/gh-pages/languages/rus.m3u
- IptvX scraper: https://github.com/iptv-org/epg/tree/master/sites/epg.iptvx.one
- Mail scraper: https://github.com/iptv-org/epg/tree/master/sites/tv.mail.ru
- CTC scraper: https://github.com/iptv-org/epg/tree/master/sites/ctc.ru
- GalamTV scraper: https://github.com/iptv-org/epg/tree/master/sites/galamtv.kz
- CGates scraper: https://github.com/iptv-org/epg/tree/master/sites/cgates.lt

`channels.xml` is a channel-mapping catalogue, not a programme guide. The primary XMLTV feed is still hosted by IptvX. No merged XMLTV file is generated or hosted by this repository.
