#!/usr/bin/env python3
"""Merge only externally verified XMLTV programme records into the Russian guide.

Exact XMLTV IDs are preferred. Cross-provider aliases are deliberately explicit;
no fuzzy/name-only mapping is ever published.
"""
import csv
import gzip
import io
import re
import sys
from datetime import datetime, timedelta, timezone
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

GUIDE = Path("public/epg.xml")
COVERAGE = Path("coverage.csv")
PLAYLIST_URL = "https://iptv-org.github.io/iptv/languages/rus.m3u"
SOURCES = [
    ("M3U Edit UA1", "https://m3u-edit.com/epg-source.php?file=UA1.xml.gz", True),
    ("M3U Edit IL1", "https://m3u-edit.com/epg-source.php?file=IL1.xml.gz", True),
    ("IPTV-EPG Russia", "https://iptv-epg.org/files/epg-ru.xml", False),
    ("IPTV-EPG Belarus", "https://iptv-epg.org/files/epg-by.xml", False),
    ("IPTV-EPG Armenia", "https://iptv-epg.org/files/epg-am.xml", False),
    ("IPTV-EPG Israel", "https://iptv-epg.org/files/epg-il.xml", False),
]

# Confirmed catalogue-name equivalents. The programme test below is still mandatory.
ALIASES = {
    "1HDMusicTelevision.ru@HD": [
        ("M3U Edit UA1", "1HD.[RU].ua"),
    ],
    "BRIDGEDeluxe.ru@SD": [
        ("M3U Edit UA1", "Bridge.TV.Deluxe.[RU].ua"),
    ],
    "DW.de@Russian": [
        ("M3U Edit UA1", "DW.Russian.[EU].ua"),
        ("M3U Edit IL1", "DW.רוסית.il"),
    ],
    "FONMusic.ru@SD": [
        ("M3U Edit UA1", "FON.Music.[RU].ua"),
    ],
    "NTVMir.ru@SD": [
        ("M3U Edit IL1", "NTV.MIR.il"),
    ],
    "StarCinema.ru@SD": [
        ("M3U Edit UA1", "Star.Cinema.[UA-RU].ua"),
    ],
    "StarFamily.ru@SD": [
        ("M3U Edit UA1", "Star.Family.Европа.[UA-RU].ua"),
    ],
}

def fetch_xml(url, is_gzip):
    req = urllib.request.Request(url, headers={"User-Agent": "Russian-XMLTV-coverage-audit/1.0"})
    with urllib.request.urlopen(req, timeout=90) as response:
        raw = response.read()
    if is_gzip:
        raw = gzip.decompress(raw)
    return ET.fromstring(raw)

def clean_tag(element):
    return element.tag.rsplit("}", 1)[-1]

def in_active_window(programme, now):
    # XMLTV timestamps are YYYYMMDDhhmmss [+-]ZZZZ. Treat absent offsets as UTC.
    def parse(value):
        if not value:
            return None
        match = re.match(r"^(\d{14})(?:\s+([+-]\d{4}))?", value)
        if not match:
            return None
        dt = datetime.strptime(match.group(1), "%Y%m%d%H%M%S")
        offset = match.group(2)
        if offset:
            sign = 1 if offset[0] == "+" else -1
            minutes = sign * (int(offset[1:3]) * 60 + int(offset[3:5]))
            dt = dt.replace(tzinfo=timezone(timedelta(minutes=minutes)))
        else:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    start = parse(programme.get("start"))
    stop = parse(programme.get("stop"))
    return bool(start and stop and start < now + timedelta(hours=48) and stop > now - timedelta(hours=3))

def parse_source(label, url, is_gzip):
    root = fetch_xml(url, is_gzip)
    channels = {
        node.get("id"): node
        for node in root
        if clean_tag(node) == "channel" and node.get("id")
    }
    programmes = defaultdict(list)
    now = datetime.now(timezone.utc)
    for node in root:
        if clean_tag(node) == "programme" and node.get("channel") and in_active_window(node, now):
            programmes[node.get("channel")].append(node)
    return channels, programmes

def main():
    tree = ET.parse(GUIDE)
    root = tree.getroot()
    existing_channels = {
        node.get("id"): node for node in root
        if clean_tag(node) == "channel" and node.get("id")
    }
    existing_programmes = defaultdict(list)
    for node in root:
        if clean_tag(node) == "programme" and node.get("channel"):
            existing_programmes[node.get("channel")].append(node)

    with COVERAGE.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    unmatched = {
        row["tvg_id"] for row in rows
        if row.get("tvg_id") and not row.get("matched_sources", "").strip()
    }
    print(f"Unmatched playlist IDs at audit start: {len(unmatched)}")

    loaded = {}
    report = []
    for label, url, is_gzip in SOURCES:
        try:
            channels, programmes = parse_source(label, url, is_gzip)
            loaded[label] = (channels, programmes)
            ids_with_programmes = sum(1 for sid, rows in programmes.items() if rows)
            print(f"SOURCE OK: {label}: {len(channels)} channels; {ids_with_programmes} IDs with programmes")
        except Exception as exc:
            print(f"SOURCE UNAVAILABLE: {label}: {type(exc).__name__}: {exc}")
            report.append(f"SOURCE_UNAVAILABLE\t{label}\t{type(exc).__name__}: {exc}")

    # Audit every unmatched target against every fetched feed. Exact IDs first.
    selected = {}
    target_audit = {}
    for target_id in sorted(unmatched):
        exact_catalogue = []
        exact_with_programmes = []
        for label, (channels, programmes) in loaded.items():
            if target_id in channels:
                exact_catalogue.append(label)
                if programmes.get(target_id):
                    exact_with_programmes.append(label)
        if exact_with_programmes and target_id not in existing_programmes:
            label = exact_with_programmes[0]
            selected[target_id] = (label, target_id)
            target_audit[target_id] = f"EXACT_PROGRAMMES\\t{label}\\t{len(loaded[label][1][target_id])}"
        elif exact_catalogue:
            target_audit[target_id] = f"EXACT_CHANNEL_NO_CURRENT_PROGRAMMES\\t{','.join(exact_catalogue)}"

    # Then test only explicit, reviewed cross-provider aliases.
    for target_id, candidates in ALIASES.items():
        if target_id not in unmatched or target_id in selected or target_id in existing_programmes:
            continue
        seen_catalogue = []
        for label, source_id in candidates:
            if label not in loaded:
                continue
            channels, programmes = loaded[label]
            if source_id in channels:
                seen_catalogue.append(f"{label}:{source_id}")
                if programmes.get(source_id):
                    selected[target_id] = (label, source_id)
                    target_audit[target_id] = f"ALIAS_PROGRAMMES\\t{label}\\t{source_id}\\t{len(programmes[source_id])}"
                    break
        if target_id not in selected and seen_catalogue:
            target_audit[target_id] = f"ALIAS_CHANNEL_NO_CURRENT_PROGRAMMES\\t{','.join(seen_catalogue)}"

    for target_id in sorted(unmatched):
        if target_id not in target_audit:
            target_audit[target_id] = "NO_EXACT_ID_OR_REVIEWED_ALIAS\\t-"


    added_channels = 0
    added_programmes = 0
    for target_id, (label, source_id) in sorted(selected.items()):
        channels, programmes = loaded[label]
        source_channel = channels[source_id]
        new_channel = ET.fromstring(ET.tostring(source_channel, encoding="utf-8"))
        new_channel.set("id", target_id)
        if target_id not in existing_channels:
            root.append(new_channel)
            existing_channels[target_id] = new_channel
            added_channels += 1
        for source_programme in programmes[source_id]:
            new_programme = ET.fromstring(ET.tostring(source_programme, encoding="utf-8"))
            new_programme.set("channel", target_id)
            root.append(new_programme)
            added_programmes += 1
        report.append(f"ADDED\t{target_id}\t{label}\t{source_id}\t{len(programmes[source_id])}")

    GUIDE.parent.mkdir(parents=True, exist_ok=True)
    tree.write(GUIDE, encoding="utf-8", xml_declaration=True)
    still_missing = len(unmatched - set(selected))
    report.insert(0, f"UNMATCHED_AT_START\t{len(unmatched)}")
    report.insert(1, f"VERIFIED_CHANNELS_ADDED\t{added_channels}")
    report.insert(2, f"VERIFIED_PROGRAMMES_ADDED\t{added_programmes}")
    report.insert(3, f"STILL_UNMATCHED\t{still_missing}")
    Path("public/external-epg-audit.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"EXTERNAL EPG RESULT: {added_channels} channels; {added_programmes} programmes added; {still_missing} of {len(unmatched)} still unmatched")

if __name__ == "__main__":
    main()
