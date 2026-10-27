#!/usr/bin/env python3
"""Synchronize explicit current-profile sections from authored cards; never rewrite facts."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def blob_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def current_section(text):
    match = re.search(r'^## (?:Dane bieżące|Dane podstawowe i wygląd — nadrzędne ustalenia bieżące)\s*$', text, re.M)
    if not match:
        return None
    rest = text[match.end():]
    end = re.search(r'^(?:#{1,2} |Charakter:|Granice wiedzy:|Rola:)', rest, re.M)
    return rest[:end.start() if end else len(rest)].strip()


def synchronize(root, check=False):
    memory_dir = root / '06_PAMIEC_POSTACI'
    path = memory_dir / 'pamiec_postaci.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    versions = {}
    for card in data['cards']:
        rel = f"06_PAMIEC_POSTACI/karty/{card['id']}.md"
        raw = (root / rel).read_bytes()
        versions[rel] = blob_sha(raw)
        card['card_source'] = {'path': rel, 'blob_sha': versions[rel]}
        section = current_section(raw.decode('utf-8-sig'))
        if section:
            card['current_profile'] = {
                'text': section,
                'scope': 'Bieżące ustalenie; dla wcześniejszej sceny odtwórz stan ze źródeł.',
                'source_path': rel,
                'source_blob_sha': versions[rel],
                'archive_cutoff_at_sync': data['metadata']['cutoff'],
            }
        else:
            card.pop('current_profile', None)
    revision = hashlib.sha256(json.dumps(data['cards'], ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    data['metadata']['content_revision'] = revision
    data['metadata']['card_source_blobs'] = versions
    data['metadata']['bytes'] = data['metadata']['source_bytes']
    outputs = {path: data, memory_dir / 'metryka.json': data['metadata']}
    index_path = memory_dir / 'indeks_wzmianek.json'
    index = json.loads(index_path.read_text(encoding='utf-8'))
    index['metadata']['bytes'] = index['metadata']['source_bytes']
    outputs[index_path] = index
    changed = []
    for target, value in outputs.items():
        before = json.loads(target.read_text(encoding='utf-8'))
        if before != value:
            changed.append(target.name)
            if not check:
                target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if check and changed:
        raise SystemExit('Niezgodne profile lub metryka: ' + ', '.join(changed) + '. Uruchom synchronizuj_profile.py.')
    print(f"OK: {len(versions)} kart, {sum(bool(c.get('current_profile')) for c in data['cards'])} profili bieżących; wersja {revision[:12]}.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    synchronize(Path(__file__).resolve().parents[1], args.check)
