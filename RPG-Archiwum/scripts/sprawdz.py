#!/usr/bin/env python3
"""Kontrola plików, podziału, ID i lokalnych linków. Niczego nie zapisuje."""
from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
m=json.loads((R/'03_INDEKS/INDEKS_PLIKOW.json').read_text())
merged=(R/m['merged_file']).read_bytes()
assert sha(merged)==m['merged_sha256'],'SHA całości'
for typ in ['small','large']:
 buffers=[]
 for c in m[typ]:
  b=(R/c['file']).read_bytes();buffers.append(b)
  assert len(b)==c['bytes'] and sha(b)==c['sha256'],c['file']
  ids=re.findall(rb'^\[(C\d+-M\d{4})\]\r?$',b,re.M)
  assert len(ids)==c['messages'] and ids[0].decode()==c['first'] and ids[-1].decode()==c['last'],c['file']
  if typ=='small':assert len(ids)<=200
 assert b''.join(buffers)==merged,typ
ids=[x.decode() for x in re.findall(rb'^\[(C\d+-M\d{4})\]\r?$',merged,re.M)]
assert len(ids)==len(set(ids))==m['messages']
for part in range(1,12):
 sub=[x for x in ids if x.startswith(f'C{part}-')]
 assert sub==[f'C{part}-M{i:04d}' for i in range(1,len(sub)+1)]
assert ids[-1]==m['current_id']
for p in R.rglob('*.md'):
 if '06_HISTORIA_BAZY' in p.parts:continue
 for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  assert (p.parent/target.split('#')[0]).exists(),f'{p}: {target}'
print(f"OK: {len(ids)} wiadomości, {len(m['large'])} dużych i {len(m['small'])} małych plików; SHA, podział, ID i linki zgodne.")
