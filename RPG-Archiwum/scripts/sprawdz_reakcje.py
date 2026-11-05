#!/usr/bin/env python3
"""Sprawdza źródła i integralność modelu reakcji; nie ocenia jakości narracji."""
from pathlib import Path
import hashlib,json,re
from collections import defaultdict
from urllib.parse import urlparse

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
    # A newer part can be indexed separately while the historical merged file
    # deliberately stays unchanged. Read that explicit source, without inventing IDs.
    extra=index.get('c15_source_file')
    if extra and not re.search(r'^\[C15-M0001\]',raw,re.M):
        raw+='\n'+(root/extra).read_text(encoding='utf-8-sig')
    pieces=re.split(r'^\[(C\d+-M\d{4})\]\s*$',raw,flags=re.M)
    messages=dict(zip(pieces[1::2],pieces[2::2]))
    assert model['metadata']['cutoff']==memory['metadata']['cutoff']==index['current_id']
    assert model['metadata']['characters']==len(cards)
    order=lambda s:tuple(map(int,re.findall(r'\d+',s)))
    seen=set()
    book_ids=set()
    book_fragments=defaultdict(set)
    for kind in ['conversation','beliefs','voice']:
        for entry in model[kind]:
            assert entry['id'] not in seen,entry['id'];seen.add(entry['id'])
            book_only=kind=='voice' and entry.get('status')=='WZORZEC_KSIĄŻKOWY'
            if book_only:
                assert entry['sources']==[] and entry['as_of'] is None and entry['period'] is None and entry['quote'] is None,entry['id']
                assert entry.get('book_references'),entry['id']
            else:
                assert entry['sources'] and all(s in messages for s in entry['sources']),entry['id']
                assert all(order(s)<=order(entry['as_of'])<=order(index['current_id']) for s in entry['sources']),entry['id']
            assert entry['characters'] and set(entry['characters'])<=set(cards),entry['id']
            assert not any(s.startswith('C12-') and 922<=int(s.split('M')[1])<=949 or s in ['C14-M0276','C14-M0064'] for s in entry['sources']),entry['id']
            if kind=='voice':
                if not book_only:
                    assert entry['status']=='PRÓBKA_KAMPANII' and entry['quote'] in messages[entry['sources'][0]],entry['id']
                assert entry['context'] and entry['limits']
                for sample in entry.get('book_references',[]):
                    assert sample['id'] not in book_ids,sample['id'];book_ids.add(sample['id'])
                    assert sample['kind'] in ['CYTAT_KSIĄŻKOWY','OMÓWIENIE_SCENY_KSIĄŻKOWEJ']
                    assert sample['character'] in entry['characters']
                    assert sample['language'] and sample['stage'] and sample['context'] and sample['analysis'] and sample['limits']
                    assert sample['work']['author'] and sample['work']['title'] and sample['work']['volume']>0
                    if sample['kind']=='CYTAT_KSIĄŻKOWY':
                        assert sample['fragments'] and all(isinstance(q,str) and q.strip() for q in sample['fragments'])
                    else:
                        assert sample['fragments']==[],sample['id']
                    assert sample['translation_note'] and sample['verification']['method']
                    assert re.fullmatch(r'\d{4}-\d{2}-\d{2}',sample['verification']['verified_on'])
                    assert sample['source']['title'] and sample['source']['section']
                    for url in [sample['source']['url']]+sample['source'].get('additional_urls',[]):
                        parsed=urlparse(url)
                        assert parsed.scheme=='https' and parsed.hostname=='www.harrypotter.com' and parsed.path.startswith('/features/'),url
                    book_fragments[sample['work']['title']].update(sample['fragments'])
            elif kind=='beliefs':
                assert entry['owner'] in entry['characters'] and set(entry['known_to'])<=set(cards)
                assert entry['kind'] in ['WŁASNE_PRZEKONANIE','RELACJA_CUDZEJ_OPINII']
                assert entry['world_status'] in ['POTWIERDZONE','NIEZWERYFIKOWANE','SPRZECZNE_Z_FAKTEM','SPROSTOWANE']
                if entry['world_status']=='SPROSTOWANE':assert entry['changed_by'] in messages
            else:
                assert entry['status'] in ['OTWARTE','ODPOWIEDZIANE','PRZYJĘTE','ODŁOŻONE','PLAN','NIEPOTWIERDZONE','ZASTĄPIONE']
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
    # This project's small quotation budget is a guard against accidental bulk imports.
    # It does not replace editorial source verification or assess permissions.
    assert all(sum(map(len,quotes))<90 for quotes in book_fragments.values())
    print(f'OK: {len(cards)} kart, {len(seen)} wpisów reakcji, {len(book_ids)} wzorców książkowych, {len(cases)} przypadków; wersje zgodne. Cytaty internetowe sprawdzane osobno.')

if __name__=='__main__':validate()
