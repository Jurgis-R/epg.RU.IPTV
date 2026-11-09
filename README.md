# Russian IPTV EPG

EPG for the playlist:
https://iptv-org.github.io/iptv/languages/rus.m3u

## Main XMLTV URL

`https://iptvx.one/epg/epg_noarch.xml.gz`

This URL is configured by the `epg.iptvx.one` scraper in [iptv-org/epg](https://github.com/iptv-org/epg/blob/master/sites/epg.iptvx.one/epg.iptvx.one.config.js). The scraper config declares a 2-day guide and labels its channel catalogue as Russian (`lang: ru`).

Add the URL above as the EPG/XMLTV source in the TV box. Keep the M3U playlist URL separate.

## Channel ID matching

[channels.xml](./channels.xml) contains exact `tvg-id` matches between the playlist and the iptv-org/epg `epg.iptvx.one` channel catalogue.

- Playlist entries inspected: 653
- Exact ID mappings included: 231
- Playlist entries without an exact mapping: 422

The TV box must match each playlist `tvg-id` to the same XMLTV channel ID. This mapping file is a reference; it is not itself the programme guide.

## Upstream sources

- Playlist: https://github.com/iptv-org/iptv/blob/gh-pages/languages/rus.m3u
- EPG scraper configuration: https://github.com/iptv-org/epg/blob/master/sites/epg.iptvx.one/epg.iptvx.one.config.js
- EPG channel catalogue: https://github.com/iptv-org/epg/blob/master/sites/epg.iptvx.one/epg.iptvx.one.channels.xml

A live HTTP download test of the guide endpoint was not possible in this run, so endpoint availability is not independently confirmed.
