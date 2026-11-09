# Russian IPTV EPG

Target playlist:
https://iptv-org.github.io/iptv/languages/rus.m3u

## Primary XMLTV URL

`https://iptvx.one/epg/epg_noarch.xml.gz`

This is the URL configured by the `epg.iptvx.one` scraper in `iptv-org/epg`. The scraper configuration specifies a 2-day guide; its channel catalogue is Russian-language. The endpoint returned an HTTP response with gzip content type during checking. The web reader cannot parse gzip payloads, so I did not inspect the programme records themselves.

Use the primary URL as the XMLTV source in your TV box. Keep the M3U playlist unchanged.

## Exact channel-ID cross-check

The current playlist has 653 entries and 653 unique `tvg-id` values. I compared them against five channel catalogues in `iptv-org/epg`:

| Source catalogue | Exact IDs found |
|---|---:|
| epg.iptvx.one | 231 |
| tv.mail.ru | 229 |
| ctc.ru | 1 |
| galamtv.kz | 11 |
| cgates.lt | 4 |
| **Unique IDs across all five** | **319 / 653** |

The combined match adds **88 IDs** beyond the previous iptvx-only map. **334 IDs remain unmatched** in these five catalogues.

Repository files:
- [channels.xml](./channels.xml) — upstream source/site IDs mapped to your playlist's exact `tvg-id` values.
- [coverage.csv](./coverage.csv) — all playlist entries and the source catalogues where exact matches exist.
- [additional-ids.txt](./additional-ids.txt) — the additional exact IDs found beyond the original iptvx catalogue.
- [epg-url.txt](./epg-url.txt) — primary URL and other public Russian EPG candidates.

## Other public Russian EPG sources found

These are alternatives, not merged into the primary feed. Their exact `tvg-id` coverage against this playlist was not established:

- EPG.ONE: `https://epg.one/ru2.xml.gz` and `https://epg.one/ru.xml.gz`. The provider describes multi-source schedule collection and roughly one week of guide data.
- IPTV-EPG.org Russia: `https://iptv-epg.org/files/epg-ru.xml`. Its public guide index lists 198 Russia channels.
- TeleGuide: `https://www.teleguide.info/download/new3/xmltv.xml.gz`.
- IptvX full guide: `https://iptvx.one/epg/epg.xml.gz`.

The guide index for IPTV-EPG.org was accessible and lists the Russia feed. The XML endpoint returned XML content type, but its records could not be parsed by the web reader. Gzip endpoints from other providers could not all be independently downloaded and inspected here. No unverified source is presented as tested.

## Upstream catalogues

- Playlist: https://github.com/iptv-org/iptv/blob/gh-pages/languages/rus.m3u
- IptvX scraper: https://github.com/iptv-org/epg/tree/master/sites/epg.iptvx.one
- Mail scraper: https://github.com/iptv-org/epg/tree/master/sites/tv.mail.ru
- CTC scraper: https://github.com/iptv-org/epg/tree/master/sites/ctc.ru
- GalamTV scraper: https://github.com/iptv-org/epg/tree/master/sites/galamtv.kz
- CGates scraper: https://github.com/iptv-org/epg/tree/master/sites/cgates.lt

`channels.xml` is a channel-mapping catalogue, not a programme guide. The primary XMLTV feed is still hosted by IptvX.
