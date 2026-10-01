from pathlib import Path
import re,json
p=Path('/workspace/scratch/d9fac05cbafd');s=(p/'c11_input/chatgpt_caly_czat11.txt').read_text()
pat=r'^={50}\nTURN (\d+) — ([^\n]+)\nKEY: ([^\n]+)\n={50}\n'
ms=list(re.finditer(pat,s,re.M));out=[];maps=[]
for i,m in enumerate(ms):
 body=s[m.end():ms[i+1].start() if i+1<len(ms) else len(s)].strip()
 body=re.sub(r'^(?:niedziela|poniedziałek|wtorek|środa|czwartek|piątek|sobota), \d+:\d+\n','',body).strip()
 body=re.sub(r'^Twoja wiadomość:\s*','',body)
 chunks=body.split('ChatGPT powiedział:',1)
 ids=[]
 for role,txt in zip(['USER','ASSISTANT'],chunks):
  txt=re.sub(r'\nPrzetwarzano przez [^\n]+\s*$','',txt).strip()
  id=f'C11-M{len(out)+1:04d}';out.append(dict(id=id,role=role,text=txt,turn=int(m[1])));ids.append(id)
 maps.append(dict(turn=int(m[1]),key=m[3],ids=ids))
(p/'c11_messages.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));(p/'c11_mapping.json').write_text(json.dumps(maps,ensure_ascii=False,indent=2))
(p/'c11_reading.txt').write_text('\n\n'.join(f"[{m['id']}] {m['role']}\n{m['text']}" for m in out))
print(len(ms),len(out));print([x for x in maps if len(x['ids'])!=2])
