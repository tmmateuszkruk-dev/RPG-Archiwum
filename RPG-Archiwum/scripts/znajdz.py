#!/usr/bin/env python3
"""Odczyt konkretnej wiadomości lub zakresu; bez sieci i zależności."""
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
def parse(s):
 m=re.fullmatch(r'C(\d+)-M(\d{4})',s)
 if not m: raise ValueError('Format ID: C11-M0409')
 return tuple(map(int,m.groups()))
def main():
 if len(sys.argv) not in (2,3): raise ValueError('Podaj jedno ID albo początek i koniec zakresu.')
 a=parse(sys.argv[1]);b=parse(sys.argv[-1])
 if a[0]!=b[0] or a[1]>b[1]: raise ValueError('Zakres musi rosnąć w obrębie jednego Part.')
 manifest=json.loads((ROOT/'03_INDEKS/INDEKS_PLIKOW.json').read_text())
 found=[]
 for c in manifest['small']:
  lo,hi=parse(c['first']),parse(c['last'])
  if lo[0]!=a[0] or lo[1]>b[1] or hi[1]<a[1]:continue
  s=(ROOT/c['file']).read_text();matches=list(re.finditer(r'^\[(C\d+-M\d{4})\]\s*\n===== (USER|ASSISTANT) =====\s*\n',s,re.M))
  for i,m in enumerate(matches):
   k=parse(m[1])
   if a[1]<=k[1]<=b[1]:
    body=s[m.end():matches[i+1].start() if i+1<len(matches) else len(s)]
    body=re.split(r'(?m)^(?:===== )?ARCHIWUM CZATU \d+ ',body)[0].rstrip()
    found.append((k[1],f'[{m[1]}] {m[2]}\n{body}'))
 if len(found)!=b[1]-a[1]+1:raise ValueError('Nie znaleziono pełnego zakresu; sprawdź indeks.')
 print('\n\n'.join(v for _,v in sorted(found)))
if __name__=='__main__':
 try:main()
 except ValueError as e:sys.exit(str(e))
