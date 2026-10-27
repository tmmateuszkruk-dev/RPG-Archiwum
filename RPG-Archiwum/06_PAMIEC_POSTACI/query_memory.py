#!/usr/bin/env python3
"""Read a character card and paginate evidence candidates. Does not infer NPC knowledge."""
import argparse,json,re,unicodedata,hashlib
from pathlib import Path

def norm(s):
 return ''.join(c for c in unicodedata.normalize('NFD',s.casefold().replace('ł','l')) if not unicodedata.combining(c))
def key(s):return tuple(map(int,re.findall(r'\d+',s)))
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('directory',type=Path)
 p.add_argument('character',help='Exact card ID or unambiguous name substring')
 p.add_argument('--term',action='append',default=[])
 p.add_argument('--archive',type=Path,help='Optional complete local UTF-8 archive for contextual text search')
 p.add_argument('--at',help='Historical cutoff Cn-Mnnnn; later cards require source reconstruction')
 p.add_argument('--offset',type=int,default=0);p.add_argument('--limit',type=int,default=12)
 a=p.parse_args()
 if a.offset<0 or a.limit<1:p.error('offset >= 0 and limit > 0 required')
 if a.at and not re.fullmatch(r'C\d+-M\d{4}',a.at):p.error('Use Cn-Mnnnn')
 data=json.loads((a.directory/'pamiec_postaci.json').read_text())
 exact=[c for c in data['cards'] if c['id']==a.character]
 cs=exact or [c for c in data['cards'] if norm(a.character) in norm(c['name'])]
 if len(cs)!=1:p.error('Choose one card: '+', '.join(c['id'] for c in cs))
 c=cs[0];terms=[norm(t) for t in a.term]
 ix=json.loads((a.directory/'indeks_wzmianek.json').read_text())['index'][c['id']]['matches']
 lookup={x['id']:x for x in ix};hits=ix;mode='name mentions / explicit anchors, not witnessed events'
 if a.archive:
  archive_bytes=a.archive.read_bytes()
  if hashlib.sha256(archive_bytes).hexdigest()!=data['metadata']['source_sha256']:p.error('Archive version differs from this memory base; update/rebuild before relying on message IDs.')
  txt=archive_bytes.decode('utf-8-sig');marks=list(re.finditer(r'^\[(C\d+-M\d{4})\]',txt,re.M))
  bodies=[txt[m.end():marks[i+1].start() if i+1<len(marks) else len(txt)] for i,m in enumerate(marks)]
  hits=[]
  for i,m in enumerate(marks):
   lo=max(0,i-2);hi=min(len(marks),i+3)
   neighbors=[marks[j][1] for j in range(lo,hi)]
   # Search all blocks, including pronoun-only actions next to a named character.
   if not any(id in lookup for id in neighbors):continue
   if terms and not any(t in norm(bodies[i]) for t in terms):continue
   hits.append({'id':m[1],'context_ids':neighbors,'status':lookup.get(m[1],{}).get('status','context candidate; verify correction register')})
  mode='text terms in full archive, within two messages of a name/anchor; not proof of presence'
 elif terms:
  mode+='; --term filters facts only without --archive'
 if a.at:hits=[h for h in hits if key(h['id'])<=key(a.at)]
 facts=[f for f in c['facts'] if not terms or any(t in norm(f['text']) for t in terms)]
 historical=bool(a.at and key(a.at)<key(data['metadata']['cutoff']))
 page=hits[a.offset:a.offset+a.limit]
 result={'character':c['name'],'campaign':data['metadata']['campaign'],'source_cutoff':data['metadata']['cutoff'],
 'content_revision':data['metadata'].get('content_revision'),
 'card_source':c.get('card_source'),
 'current_profile':None if historical else c.get('current_profile'),
 'historical_warning':'Reconstruct the state at requested ID from sources; present-day role/limits suppressed.' if historical else None,
 'role':None if historical else c['role'],'behavior':None if historical else c['behavior'],
 'knowledge_limits':None if historical else c['knowledge_limits'],
 'facts':[f for f in facts if not a.at or key(f['latest_evidence_id'])<=key(a.at)],
 'later_syntheses_to_reconstruct':[f['source_label'] for f in facts if a.at and key(f['latest_evidence_id'])>key(a.at)],
 'candidate_mode':mode,'total_candidates':len(hits),'offset':a.offset,'next_offset':a.offset+len(page) if a.offset+len(page)<len(hits) else None,'evidence_candidates':page}
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
