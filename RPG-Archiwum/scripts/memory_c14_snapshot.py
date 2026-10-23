from pathlib import Path
import json,re,copy
R=Path('repo_c14/RPG-Archiwum');D=R/'06_PAMIEC_POSTACI';o=json.load(open(D/'pamiec_postaci.json'));ix=json.load(open(D/'indeks_wzmianek.json'));cards={c['id']:c for c in o['cards']};m=json.load(open('c14_safe_messages.json'));man=json.load(open(R/'03_INDEKS/INDEKS_PLIKOW.json'))
def wr(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
def js(p,v):wr(p,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
new=[('xenophilius-lovegood','Xenophilius Lovegood','Xenophilius|Ksenofilius','Ojciec Luny; wiadomość przekazana w jej liście.'),('eleanor-branstone','Eleanor Branstone','Eleanor|Branstone','Hufflepuff, II rok; pomaga organizować wspólny stół.'),('laura-madley','Laura Madley','Laura|Madley','Hufflepuff, II rok.'),('dennis-creevey','Dennis Creevey','Dennis','Gryffindor, II rok; młodszy brat Colina.'),('euan-abercrombie','Euan Abercrombie','Euan|Abercrombie','Gryffindor, I rok.'),('orla-quirke','Orla Quirke','Orla|Orli|Quirke','Ravenclaw, II rok; gra w szachy.'),('stewart-ackerley','Stewart Ackerley','Stewart|Ackerley','Ravenclaw, II rok.'),('owen-cauldwell','Owen Cauldwell','Owen|Cauldwell','Hufflepuff, II rok.'),('kevin-whitby','Kevin Whitby','Kevin|Whitby','Hufflepuff, II rok.'),('rose-zeller','Rose Zeller','Rose|Zeller','Hufflepuff, I rok; robi papierowe ozdoby.'),('amelia-pritchard','Amelia — siostra Grahama','Ameli','Postać kampanii; 9 lat, według Grahama 10 urodziny w styczniu.'),('merriweather','Pani Merriweather','Merriweather','Sprzedawczyni w Hogsmeade; postać tej sceny.'),('edgar-whitlock','Edgar Whitlock','Edgar|Whitlock','Jubiler w Hogsmeade; postać tej sceny.')]
for id,name,pat,role in new:
 if id not in cards:
  c=dict(id=id,name=name,pattern=pat,role=role,behavior='Odtwarzaj z dialogów C14; nie nadawaj wiedzy dorosłego ani automatycznej uległości.',knowledge_limits='Wiedza tylko ze scen z własnym udziałem lub przekazanych informacji. Brak znajomości prywatnych listów Jamesa. Nowa karta obejmuje C14; nie rozstrzyga braku dawnych spotkań.',facts=[],mention_ids=[],mention_count=0);o['cards'].append(c);cards[id]=c
facts=[]
def fact(who,txt,ns):
 for id in who.split(','):
  assert id in cards,id
  f=dict(id=f'{id}-C14-{len(cards[id]["facts"])+1:03d}',text=txt,sources=[f'C14-M{n:04d}' for n in ns],source_label='C14 — przyrost ze sprawdzonych fragmentów',evidence='Synteza dostępnego tekstu; sprawdź źródła, luki i korekty.',latest_evidence_id=f'C14-M{max(ns):04d}',sources_verified_exist=True,temporal_rule='Wiedza od zdarzenia; nie przenosić wstecz.')
  cards[id]['facts'].append(f);facts.append((id,f))
group='malcolm-baddock,eleanor-branstone,laura-madley,dennis-creevey,euan-abercrombie,orla-quirke,stewart-ackerley,owen-cauldwell,kevin-whitby,rose-zeller'
fact('draco-malfoy,theodore-nott,pansy-parkinson,james-brown','Rozmowa o proteście od M0064 do M0074 została cofnięta. Obowiązuje M0078: Draco nie współczuje Weasleyom, Pansy wspiera go, Nott nie jest rzecznikiem Jamesa.',[76,78])
fact('james-brown,severus-snape','Ostatni szlaban u Umbridge odbył się bez krwawego pióra. Snape ma wyjaśnienia Jamesa oraz dokumentację dawnego pióra; sprawa pozostaje otwarta. Zapowiedź listu do Ministerstwa była blefem, co James ujawnił Snape’owi.',[184,185,186,191,192,194])
fact('dolores-umbridge,james-brown','Podczas listopadowego szlabanu James korzystał z własnych przyborów, złożył pisemne wyjaśnienia i przepisał sto zdań; kara została zakończona. Odpowiedzi na pytania o Lucjusza i Veritaserum nie ma w eksporcie.',[120,121,125,145,146,149,151,154])
fact('minerva-mcgonagall,james-brown,hermiona-granger','21 XII McGonagall przekazała obojgu, że Artur żyje i jest leczony w Mungu. Nie oznacza to znajomości całej wizji Harry’ego ani adresu kwatery.',[262])
fact('minerva-mcgonagall,james-brown','W Wigilię James powiedział McGonagall o niepokoju z powodu świąt Hermiony z Ronem. Rozmowa była ściszona; reszta szkoły nie poznaje jej automatycznie.',[591,592,593,594,598])
fact('hermiona-granger,james-brown','Para pozostaje razem; list z 25 XII potwierdza miłość, tęsknotę i odmowę narzucania Ronowi odstępu. Podpisy o przyszłym mężu/narzeczonym nie są zaręczynami. Randka nadal nie ma potwierdzonego rozegrania.',[167,648,649])
fact('hermiona-granger','Z listów Jamesa zna wspólne posiłki czterech domów, szachy i bitwę na śnieżki. Chce poznać Orlę i z nią zagrać. To nie daje jej wiedzy o wszystkich rozmowach w Hogwarcie.',[605,648])
fact('irma-pince,james-brown','Poranne wizyty w bibliotece są znanym zwyczajem, nie pierwszą wizytą. Pince pamięta dawny stolik z widokiem na Hermionę; James pomaga i czyta także podczas świąt. Dowiaduje się od niego o odpowiedzi Hermiony.',[356,364,366,533,537,657])
fact(group+',james-brown','23 XII wspólny stół uczniów różnych domów. Rozmawiają o zaproszeniu Hermiony; James prosi o używanie Hermiona lub panna Granger. Poznają jego relację o konflikcie z Draco, nie są automatycznie dawnymi świadkami.',[374,381,383,384,397])
fact(group+',james-brown','Świąteczne szachy: James wygrywa opisane partie poza remisem z Orlą. Rose uczy się zasad i nie gra przeciw niemu. Nie przypisuj Jamesowi pokonania Orli.',[414,416])
fact('graham-pritchard,james-brown','Graham opowiada o dziewięcioletniej siostrze Amelii, która ma skończyć dziesięć w styczniu. Przyjmuje kolczyk-klucz przeznaczony pierwotnie dla Luny. Chce, aby James ich sobie przedstawił; M0521 potwierdza zgodę.',[512,520,521,522])
fact('amelia-pritchard','Według listu relacjonowanego przez Grahama otrzymała świecący kolczyk-klucz. Nie była przy rozmowie Jamesa z Grahamem; nie dopisuj spotkania z Jamesem ani Luną.',[682,690])
fact('graham-pritchard','25 XII otrzymał list Amelii potwierdzający doręczenie kolczyka; 26 XII kolejny. Luna nie zna automatycznie przekazania części prezentu.',[682,690])
fact('james-brown,merriweather','Zakup w Hogsmeade: róża z Walcem nr 2 Szostakowicza i mapa nieba nad Hogwartem 25 XII 1994, razem 48 galeonów, wspólna szkatułka bez bileciku. Kopuła i medalion tylko proponowane.',[468,471,472,473,475,477,480,481])
fact('james-brown,edgar-whitlock','Kupiono różne kolczyki motyl i klucz. Jubiler zna zakup, nie późniejsze przekazanie klucza Amelii.',[485,486,487,488])
fact('albus-dumbledore,james-brown','Jednorazowe pozwolenie na Hogsmeade w sprawie prezentów, powrót przed zmrokiem i bez wyjazdu poza wioskę.',[453,456,457])
fact('rose-zeller,eleanor-branstone,laura-madley,malcolm-baddock,graham-pritchard,james-brown','Przygotowano notes dla Luny o niezwykłych spostrzeżeniach. James prosi o osobiste wręczenie po powrocie. Notes zachowany, pod koniec u Rose; Luna nie dostała go jeszcze.',[496,667,684,690])
fact(group+',graham-pritchard,james-brown','Wigilijna bitwa na śnieżki odbyła się bez zaklęć. James staranował fort i później odpadł; czerwoni wygrali 2:1. To wspólne doświadczenie, nie pierwsze spotkanie przy następnym posiłku.',[549,555,571,579,583,584])
fact('james-brown','Wysłał świąteczne listy do Kruma, Weasleyów, Luny z ojcem, Élodie z rodziną i Hermiony. Samotne leżenie opisane jako czuwanie nie oznacza snu. Odpowiedź Weasleyów do M0704 nie nadeszła.',[603,605,607,613,645,690])
fact('luna-lovegood,james-brown','List Luny 25 XII podtrzymuje przyjaźń; spędza święta z ojcem w domu. Chce opowiedzieć historię osobiście. Nie potwierdza otrzymania notesu ani motyla.',[684])
fact('xenophilius-lovegood','Według listu Luny dziękuje za życzenia Jamesa i ma nową teorię o Narglach. Nie był przy świątecznych wydarzeniach w Hogwarcie.',[684])
fact('viktor-krum,james-brown','List z 28 XII: Krum spędza święta z rodziną w Bułgarii, pamięta zaproszenie do Anglii, termin nieustalony. Prosi o pozdrowienie Hermiony; nie zakładaj, że pozdrowienia już przekazano.',[692])
fact('elodie-moreau,james-brown','List z 28 XII: Élodie chciałaby odwiedzić Anglię, musi uzgodnić podróż z rodzicami; następne wakacje tylko możliwością. Rodzina odwzajemnia pozdrowienia.',[694])
fact('graham-pritchard,malcolm-baddock,orla-quirke,dennis-creevey,eleanor-branstone,laura-madley,rose-zeller,euan-abercrombie,james-brown','28 XII słyszą rozmowę o Krumie, Cedryku i obawach przed wojną. Zapewnienie Jamesa, że młodsi nie będą musieli walczyć, nie jest gwarancją przyszłości. Potem planują Sylwestra; Graham pyta Jamesa o pozostanie na Nowy Rok, odpowiedzi jeszcze nie ma.',[695,697,699,700,701,702,703,704])
# Append mention index; these hits are not evidence of knowledge.
for c in o['cards']:
 rx=re.compile(c['pattern'].replace('\\\\','\\'),re.I);oldmatches=ix['index'].get(c['id'],{}).get('matches',[])
 for e in man['small']:
  if not e['first'].startswith('C14-'):continue
  lines=(R/e['file']).read_text().splitlines();marks=[(n,l[1:-1]) for n,l in enumerate(lines) if re.fullmatch(r'\[C14-M\d{4}\]',l)]
  for j,(ln,id) in enumerate(marks):
   body='\n'.join(lines[ln:marks[j+1][0] if j+1<len(marks) else len(lines)])
   if rx.search(body) or any(id in f['sources'] for f in c['facts']):oldmatches.append(dict(id=id,path=e['file'],line=ln+1,status='Wzmianka/źródło; sprawdź obecność, luki i korekty.'))
 c['mention_ids']=list(dict.fromkeys([z['id'] for z in oldmatches]));c['mention_count']=len(c['mention_ids']);ix['index'][c['id']]=dict(name=c['name'],pattern=c['pattern'],matches=oldmatches)
 body=f"# {c['name']}\n\nGranica aktualizacji: C14-M0704. Starsze fakty zachowane, nowe tylko przy źródłach C14. C14 ma luki; brak wpisu nie dowodzi braku zdarzenia.\n\nRola: {c['role']}\n\nCharakter: {c['behavior']}\n\nGranice wiedzy: {c['knowledge_limits']}\n\n"+'\n'.join('- '+f['text']+' Źródła: '+', '.join(f['sources']) for f in c['facts'])
 wr(D/'karty'/f"{c['id']}.md",body+'\n')
meta=o['metadata'];meta.update(cutoff='C14-M0704',messages=13778,cards=len(cards),source_sha256=man['merged_sha256'],source_commit='Publikacja C14 — patrz historia Git.',coverage='Zachowano wcześniejsze fakty; przyrost C14 ze źródeł dostępnych. 89 luk eksportu jawnie oznaczono. Wzmianka nie jest dowodem wiedzy, a synteza nie jest pełną transkrypcją.')
ix['metadata']=meta;js(D/'pamiec_postaci.json',o);js(D/'indeks_wzmianek.json',ix);js(D/'metryka.json',meta)
wr(D/'CZYTAJ_NAJPIERW.md',f'# Pamięć C1–C14\n\n{len(cards)} kart; stan C14-M0704. Zachowano starsze fakty. C14 zawiera 89 luk: najpierw sprawdź korekty i źródło, nie dopisuj brakujących reakcji.\n\nZapytanie: `python 06_PAMIEC_POSTACI/query_memory.py 06_PAMIEC_POSTACI hermiona --term list`\n\nWzmianki służą wyszukiwaniu, nie dowodzą obecności ani wiedzy.\n')
wr(D/'Pamiec_postaci_Hogwarts_C1-C14.md','\n\n'.join(p.read_text() for p in sorted((D/'karty').glob('*.md'))))
js(Path('c14_new_facts.json'),facts)
print(len(cards),'cards;',len(facts),'sourced fact assignments')
