#!/usr/bin/env python3
"""Sprawdza źródła i integralność modelu reakcji; nie ocenia jakości narracji."""
from pathlib import Path
import hashlib,json,re

ROOT=Path(__file__).resolve().parents[1]
def blob(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

def validate(root=ROOT):
    model_path=root/'06_PAMIEC_POSTACI/model_reakcji.json'
    model=json.loads(model_path.read_text())
    memory=json.loads((root/'06_PAMIEC_POSTACI/pamiec_postaci.json').read_text())
    cards={c['id']:c for c in memory['cards']}
    index=json.loads((root/'03_INDEKS/INDEKS_PLIKOW.json').read_text())
    raw=(root/index['merged_file']).read_text(encoding='utf-8-sig')
    pieces=re.split(r'^\[(C\d+-M\d{4})\]\s*$',raw,flags=re.M)
    messages=dict(zip(pieces[1::2],pieces[2::2]))
    assert model['metadata']['cutoff']==memory['metadata']['cutoff']==index['current_id']
    assert model['metadata']['characters']==len(cards)
    order=lambda s:tuple(map(int,re.findall(r'\d+',s)))
    seen=set()
    for kind in ['conversation','beliefs','voice']:
        for entry in model[kind]:
            assert entry['id'] not in seen,entry['id'];seen.add(entry['id'])
            assert entry['sources'] and all(s in messages for s in entry['sources']),entry['id']
            assert all(order(s)<=order(entry['as_of'])<=order(index['current_id']) for s in entry['sources']),entry['id']
            assert entry['characters'] and set(entry['characters'])<=set(cards),entry['id']
            assert not any(s.startswith('C12-') and 922<=int(s.split('M')[1])<=949 or s in ['C14-M0276','C14-M0064'] for s in entry['sources']),entry['id']
            if kind=='voice':
                assert entry['quote'] in messages[entry['sources'][0]],entry['id']
                assert entry['status']=='PRÓBKA_KAMPANII' and entry['context'] and entry['limits']
            elif kind=='beliefs':
                assert entry['owner'] in entry['characters'] and set(entry['known_to'])<=set(cards)
                assert entry['kind'] in ['WŁASNE_PRZEKONANIE','RELACJA_CUDZEJ_OPINII']
                assert entry['world_status'] in ['POTWIERDZONE','NIEZWERYFIKOWANE','SPRZECZNE_Z_FAKTEM','SPROSTOWANE']
                if entry['world_status']=='SPROSTOWANE':assert entry['changed_by'] in messages
            else:
                assert entry['status'] in ['OTWARTE','ODPOWIEDZIANE','PRZYJĘTE','ODŁOŻONE','PLAN','ZASTĄPIONE']
    expected_source={'path':'06_PAMIEC_POSTACI/model_reakcji.json','blob_sha':blob(model_path.read_bytes())}
    assert memory['metadata']['reaction_source']==expected_source
    for cid,card in cards.items():
        assert card['reaction_state']['source']==expected_source,cid
        for kind in ['conversation','beliefs','voice']:
            assert card['reaction_state'][kind]==[x for x in model[kind] if cid in x['characters']],(cid,kind)
    cases=json.loads((root/'07_SPRAWDZIANY/przypadki.json').read_text())['cases']
    rubric=json.loads((root/'07_SPRAWDZIANY/kryteria.json').read_text())['rubric']
    assert len({c['id'] for c in cases})==len(cases) and set(rubric)=={c['id'] for c in cases}
    for case in cases:
        for source in case['sources']:
            assert source['text'] in messages[source['id']],(case['id'],source['id'])
    print(f'OK: {len(cards)} kart, {len(seen)} wpisów reakcji, {len(cases)} przypadków; źródła i wersje zgodne. Ocena zachowania jest osobna.')

if __name__=='__main__':validate()
