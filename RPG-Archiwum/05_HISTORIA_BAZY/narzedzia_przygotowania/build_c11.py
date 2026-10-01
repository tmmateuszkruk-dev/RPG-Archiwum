from pathlib import Path
import re,json,hashlib,shutil,zipfile
R=Path('/workspace/scratch/d9fac05cbafd'); O=R/'RPG_Baza_Wiedzy_11_czesci'; B=R/'c10_restored'
def write(n,t):
 p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t.strip()+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(a,b=None):return f'C11-M{a:04d}'+(f'–C11-M{b:04d}' if b else '')
def table(rows):return '\n'.join('| '+' | '.join(map(str,row))+' |' for row in rows)
M=json.loads((R/'c11_messages.json').read_text());mapping=json.loads((R/'c11_mapping.json').read_text())
# Keep UI residue in normalized text, documented, rather than guess whether ellipses hide words.
base=(B/'01_ARCHIWUM_CZAT_1-10_SCALONE.txt').read_bytes()
prev=json.loads((B/'KONTROLA_ARCHIWUM.json').read_text())
assert sha(base)==prev['merged_sha256']
for p in B.iterdir():
 if p.is_file() and p.suffix in ('.md','.json'):shutil.copyfile(p,O/'historia_wersji/do_C10'/p.name)
for n in ['00_MAPOWANIE_C5.md','00_MAPOWANIE_C10.md']:shutil.copyfile(B/n,O/n)
shutil.copyfile(R/'c11_input/chatgpt_caly_czat11.txt',O/'oryginaly/chatgpt_caly_czat11.txt')
shutil.copyfile(R/'RPG_Baza_Wiedzy_10_czesci/oryginaly/ChatGPT_CALY_CZAT10.txt',O/'oryginaly/ChatGPT_CALY_CZAT10.txt')
a11='\n\nARCHIWUM CZATU 11 — treść rozmowy w dotychczasowym formacie\n\n205 bloków TURN: 204 pary USER/ASSISTANT i końcowy USER bez odpowiedzi. Oryginalny eksport zachowany. Metadane eksportu nie datują fabuły. Odrzucone odpowiedzi zachowano jako zapis historyczny; status w 09_REJESTR_KOREKT.md.\n\n'
a11+=''.join(f"[{m['id']}]\n===== {m['role']} =====\n\n{m['text']}\n\n\n" for m in M)
merged=base+a11.encode();(O/'01_ARCHIWUM_CZAT_1-11_SCALONE.txt').write_bytes(merged)
# Preserve older small files byte-for-byte; C11 header belongs to its first small part.
chunks=[]
for c in prev['chunks']:
 p=R/'c10_parts'/Path(c['file']).name;assert sha(p.read_bytes())==c['sha256'];shutil.copyfile(p,O/c['file']);chunks.append(c)
ma=list(re.finditer(rb'^\[C11-M\d{4}\]$',a11.encode(),re.M))
for start in range(0,len(ma),200):
 end=min(start+200,len(ma));b=a11.encode()[0 if start==0 else ma[start].start():ma[end].start() if end<len(ma) else len(a11.encode())]
 name=f'ARCHIWUM_{len(chunks)+1:03d}_{M[start]["id"]}_{M[end-1]["id"]}.txt';rel='mniejsze_czesci/'+name;(O/rel).write_bytes(b)
 chunks.append(dict(file=rel,first=M[start]['id'],last=M[end-1]['id'],messages=end-start,bytes=len(b),sha256=sha(b)))
# Large parts start at the original archive heading, unlike old small fragments.
heads=list(re.finditer(rb'^(?:===== )?ARCHIWUM CZATU (\d+) ',merged,re.M));assert [int(x[1]) for x in heads]==list(range(1,12))
big=[]
for i,h in enumerate(heads):
 s=0 if i==0 else h.start();e=heads[i+1].start() if i+1<len(heads) else len(merged);b=merged[s:e]
 ids=re.findall(rb'^\[(C\d+-M\d{4})\]\r?$',b,re.M);n=f'01_ARCHIWUM_CZAT_{i+1}.txt';(O/'duze_czesci'/n).write_bytes(b)
 big.append(dict(file='duze_czesci/'+n,part=i+1,first=ids[0].decode(),last=ids[-1].decode(),messages=len(ids),bytes=len(b),sha256=sha(b)))
assert b''.join((O/c['file']).read_bytes() for c in chunks)==merged
assert b''.join((O/c['file']).read_bytes() for c in big)==merged
state='Stan: C11-M0409 — niedziela 9 lipca 1995, po obiedzie i deserze, dokładna godzina nieustalona; główna sypialnia londyńskiego domu Jamesa. Następna odpowiedź należy do NPC (Hermiony).'
updates={}
updates['02_TIMELINE.md']='''# Timeline — aktualizacja C11

## 8 lipca 1995 — dokończenie wizyty u Grangerów

| Etap | Zdarzenie | Źródło |
|---|---|---|
| Pokój, po końcu C10 | James rozczesuje włosy Hermiony i układa wysoki luźny kok z pasmami wokół twarzy. Szczotkę odkłada; Hermiona ogląda efekt w lustrze | C11-M0005–C11-M0024 |
| Pokój | Wspólna czułość, komplementy i chwilowa zabawa w milczenie, potem decyzja o zejściu | C11-M0025–C11-M0062 |
| Parter | James niesie Hermionę na dół. Rodzice widzą fryzurę i słyszą, że nauczył się czesać dzięki młodszej siostrze | C11-M0063–C11-M0070 |
| Przedpokój | Uzgodniona samotna wizyta Hermiony następnego dnia; powrót najpóźniej o 20:00. Godzina przyjścia pozostaje niespodzianką; rodzice chcą znać wyjście i cel oraz zmiany planów | C11-M0071–C11-M0082 |
| Wyjście | James zakłada płaszcz, prywatnie prosi o sukienkę na jutro, żegna się i wychodzi | C11-M0083–C11-M0092 |
| Londyn | Taksówka do Belgrave Square, zapłacony niepodany liczbowo rachunek; wejście do domu i sypialni, zdjęcie płaszcza, kamizelki i butów | C11-M0093–C11-M0100 |

## Noc 8/9 lipca i niedziela 9 lipca

| Etap | Zdarzenie | Źródło |
|---|---|---|
| Noc / 4:00 / rano | James czuwa bez utraty świadomości, o 4:00 wstaje, ćwiczy, biega, myje się i przebiera. Uprzedza skrzaty o Hermionie; je śniadanie. Gotowy o 9:00 | C11-M0101 |
| Później, brak godziny | Skrzat zgłasza przybycie Hermiony; James otwiera. Błękitna sukienka, diament i niewielka torba; pierwsza wizyta rzeczywiście się zaczyna | C11-M0102–C11-M0110 |
| Zwiedzanie | Hol, salon powitalny, oranżeria, jadalnia, galeria, biblioteka, aportatorium, sypialnia. Hermiona otrzymuje zgodę na książki; ogląda tom run i odkłada go. Poznaje zasadę wyjątku od blokady aportacji | C11-M0111–C11-M0136 |
| Przed obiadem | Zakończenie zwiedzania na razie; wspólny odpoczynek i prywatna rozmowa o bliskości, przerwie oraz odległej przyszłości. Nie nowy sen ani zaręczyny | C11-M0137–C11-M0250 |
| Przygotowanie obiadu | James przekazuje skrzatom zamówienie w ukrytej kuchni i wraca. Hermiona zakłada buty; para schodzi do jadalni i siada obok siebie | C11-M0251–C11-M0284 |
| Obiad | Kurczak, ziemniaki i sałatka. Negocjacja dobrowolnej zabawy: początkowo pięć, po obejrzeniu deseru dziesięć minut zwierzeń wybieranych przez Hermionę | C11-M0285–C11-M0304 |
| Deser | Hermiona dostaje tartę cytrynową; James pudding czekoladowy z sosem i malinami, który oddaje jej w całości. Ona zjada pudding; brak opisu losu tarty | C11-M0301–C11-M0310 |
| Sypialnia | James niesie Hermionę na górę, zdejmuje jej buty i różdżką zasuwa baldachim, robiąc zupełną ciemność. Rozpoczynają zwierzenia | C11-M0311–C11-M0314 |
| Rozmowa | Hermiona mówi o potrzebie uwagi, przywiązaniu, codziennych zwyczajach, nadziejach na wspólną dorosłość i wyobrażanym nazwisku. Zachowuje przyjaciół; wyklucza przemoc i groźby pod pretekstem zazdrości | C11-M0314–C11-M0406 |
| Zakończenie | James ogłasza upływ czasu; Hermiona kończy nadzieją, że pozostaną razem. James zmienia pozycję, całuje ją i mówi „Kocham cię”. Brak odpowiedzi NPC | C11-M0407–C11-M0409 |

Data 9 VII wynika z ciągłości „jutro” po 8 VII i jawnego przejścia przez noc w M0101; nie z dnia interfejsu eksportu. Nie przeliczaj długości wiadomości na minuty. C11-M0004 cytuje koniec C10, nie rozgrywa go drugi raz.
'''
updates['03_PROFILE_POSTACI.md']='''# Profile postaci — aktualizacja C11

## James Brown

Nadal piętnastoletni Ślizgon po IV roku; wyłącznie postać użytkownika. Kończy wizytę u Grangerów 8 VII i przyjmuje Hermionę 9 VII. Umiejętność czesania wiąże wprost z młodszą siostrą; rodzice Hermiony słyszą to po raz pierwszy w tej wizycie (C11-M0067). Nie dopisano nowych szczegółów tragedii.

Noc 8/9 VII spędza w czuwaniu ze świadomością; o 4:00 zaczyna ćwiczenia, potem biega. Nie nowy sen ani diagnoza (C11-M0101). Rano czarna koszulka, spodnie, pasek i skarpetki; bez opisanego założenia butów, krawata lub płaszcza. Wyjaśnia, że praktycznie nie zmieniał odziedziczonych wnętrz (C11-M0117), i oprowadza Hermionę. Nie demonstruje aportacji; wyposażenie domu nie daje mu automatycznie umiejętności ani licencji.

## Hermiona Granger

Nadal piętnaście lat, własne zdanie, przyjaciele, nauka i rodzina. 8 VII pozwala Jamesowi zrobić luźny wysoki kok, ogląda go i pokazuje rodzicom; 9 VII przychodzi z luźniejszymi włosami, w błękitnej sukience do kolan, diamentowym naszyjniku i z małą torbą (C11-M0019–C11-M0024, C11-M0066, C11-M0104).

Ogląda dom po raz pierwszy. Czyta krótko książkę o runach, odkłada ją i chce wrócić do biblioteki; nie przeczytała całego księgozbioru ani nie otrzymała własności domu (C11-M0121–C11-M0134). Określenie „szalona Hermiona” oznacza żartobliwie większą spontaniczność tej samej osoby, nie osobną osobowość (C11-M0258).

W prywatnej rozmowie opisuje własne uczucia, potrzebę uwagi, lubiane gesty i nadzieję na wspólną dorosłość. Deklaracje o przeszłych drobnych zwyczajach są jej relacją, nie nowo rozegranymi retrospekcjami. „Hermiona Brown” / „Granger-Brown” pozostają wyobrażeniami, nie zmianą nazwiska (C11-M0314–C11-M0408).

## Państwo Granger

Dentyści, imiona nieustalone. Poznali Jamesa osobiście; wiedzą już także, że miał młodszą siostrę i nauczył się dla niej fryzur. Nie ujawniono im wieku rodzeństwa w chwili tragedii ani sprawcy (C11-M0067–C11-M0070). Akceptują samodzielną wizytę córki 9 VII z powrotem do 20:00 i informacją o zmianach planu (C11-M0075–C11-M0078). Nie towarzyszą jej w domu Jamesa.

## Skrzaty i Lodgok

Skrzaty zostały uprzedzone o gościu, jedno zgłasza przybycie; otrzymują zamówienie obiadu i deseru. Brak nowych imion i brak dowodu podsłuchania prywatnych wyznań (C11-M0101–C11-M0102, C11-M0259). Lodgok nie pojawia się i nie ma nowego listu do niego.

Pozostałe postacie nie uczestniczą w nowych scenach; przywołanie imion Rona, Harry’ego i Ginny nie jest ich obecnością ani zmianą ich uczuć.
'''
updates['04_KTO_CO_WIE.md']='''# Kto co wie — aktualizacja C11

| Informacja | Odbiorca i droga poznania | Ograniczenie | Źródło |
|---|---|---|---|
| Czesanie i młodsza siostra | Grangerowie widzą efekt; Hermiona mówi, kto ją uczesał; James wyjaśnia genezę umiejętności | Brak szczegółów śmierci, dat i sprawcy | C11-M0066–C11-M0070 |
| Jutrzejsza wizyta i 20:00 | James, Hermiona i rodzice negocjują razem | Nie zgoda na tydzień, nocleg ani nieograniczone wakacje | C11-M0075–C11-M0082 |
| Prośba o sukienkę | Szept Jamesa do Hermiony, jej cicha odpowiedź | Rodzice nie znają automatycznie treści szeptu | C11-M0085–C11-M0088 |
| Nocne czuwanie i 4:00 | Prywatne działania Jamesa zadeklarowane przez użytkownika | Hermiona nie była obecna; nie dopisywać raportu dla niej lub Pomfrey | C11-M0101 |
| Przybycie Hermiony | Skrzaty uprzedzone; jedno zgłasza przybycie; James otwiera | Brak imion, wiedzy o wszystkich wcześniejszych scenach i prywatnych wyznaniach | C11-M0101–C11-M0110 |
| Wnętrza domu | Hermiona ogląda hol, salon, oranżerię, jadalnię, galerię, bibliotekę, aportatorium i sypialnię | Nie zna stąd całego planu, wszystkich zabezpieczeń, skarbców i zawartości kufra | C11-M0111–C11-M0136 |
| Odziedziczony wystrój | James mówi, że praktycznie nic nie zmienił | Nie zna dokładnego autora ani dat urządzenia wnętrz | C11-M0117–C11-M0118 |
| Portrety rodu Slytherina | James potwierdza Hermionie pochodzenie postaci z portretów | Brak imion i biografii konkretnych sportretowanych | C11-M0120–C11-M0122 |
| Dostęp do biblioteki | Zgoda Jamesa; Hermiona ogląda tom starożytnych run | Zgoda na lekturę nie jest przekazaniem książek na własność; tom odłożony | C11-M0123–C11-M0126 |
| Aportatorium | Wyjaśnienie Jamesa: jedyny punkt bezpiecznej aportacji do/z chronionego obiektu, potwierdzenie kontrolowanego wyjątku | Nie ujawnia Strażnika Fideliusa, hasła, pełnej procedury dostępu ani licencji Jamesa | C11-M0129–C11-M0134 |
| Obiad | James przekazuje skrzatom zamówienie; Hermiona widzi podanie i je | Skrzaty nie dostają automatycznie wiedzy o umowie za pudding | C11-M0259–C11-M0306 |
| Prywatne zwierzenia | James słyszy od Hermiony sam na sam, pod zasuniętym baldachimem | Brak świadków/podsłuchu rodziców, skrzatów, Rona, Luny czy Lodgoka | C11-M0313–C11-M0408 |
| Nadzieje i nazwisko | Hermiona mówi o wyobrażeniach; James odpowiada w tej samej konwencji | Nie oświadczyny, małżeństwo, wspólny dom ani zapowiedź nieuchronnej przyszłości | C11-M0338–C11-M0346, C11-M0380–C11-M0396, C11-M0408 |

Wiedza wcześniejsza pozostaje w swoim zakresie: Hermiona nie otrzymała pełnego podsłuchu C9, rodzice nie poznali bezsenności i cen prezentów. Noc C11 nie cofa wcześniejszych rzeczywistych snów. W ciemności postacie mogą słyszeć i wyczuwać dotyk; nie widzą automatycznie rumieńców ani mimiki.
'''
updates['05_RELACJE.md']='''# Relacje — aktualizacja C11

## James i Hermiona

Związek trwa; 8 VII wizyta u rodziców zakończona, 9 VII pierwsza dzienna wizyta Hermiony u Jamesa odbywa się za ich zgodą. Powrót do 20:00 pozostaje zobowiązaniem; brak noclegu (C11-M0075–C11-M0078, C11-M0104–C11-M0108).

Czesanie i gotowy kok zacieśniają zwykłą bliskość; Hermiona później mówi, że ceniła cierpliwość i chętnie da się uczesać ponownie (C11-M0019–C11-M0024, C11-M0400). Inicjatywa bywa wzajemna. „Szalona Hermiona” to żartobliwa nazwa spontanicznego zachowania, nie obowiązek ani druga osobowość (C11-M0176–C11-M0194, C11-M0258).

Odrzucona odpowiedź C11-M0154 została zastąpiona C11-M0158 po korekcie użytkownika. Zachować wcześniejsze uzgodnienia zwykłej czułości, a jednocześnie możliwość sytuacyjnej odmowy, przerwy i prośby o uprzedzenie przed nowym gestem. C11-M0164–C11-M0168 doprecyzowują właśnie uprzedzenie; później para zwalnia i rozmawia, bez przekroczenia ustalonej granicy (C11-M0213–C11-M0250). Treści prowadzić odpowiednio do wieku, bez erotycznego rozwijania.

## Dziesięć minut zwierzeń — wykonane, nie dług do odebrania

Początkowo pięć minut; po obejrzeniu puddingu Hermiona dobrowolnie wybiera dziesięć i sama wybiera treść. James oddaje jej cały deser. Porównanie do „sprzedaży godności” zostaje sprostowane, nie ustanawia przymusu (C11-M0287–C11-M0308). Rozmowa zaczyna się po powrocie do sypialni i kończy w C11-M0407–C11-M0408.

Hermiona ujawnia, że lubi uwagę Jamesa, czułe zwroty, noszenie, przedłużanie spotkań, poczucie bycia wybraną oraz dzielenie się codziennością. Ceni uwzględnianie jej zdania. Naszyjnik założyła także po to, by dostrzegł, że nosi coś od niego. Są to deklaracje Hermiony przekazane Jamesowi, nie wiedza wszystkich NPC (C11-M0314–C11-M0378).

Lekka zazdrość może jej się podobać, lecz wyklucza awantury, groźby, przemoc i robienie z Rona wroga za samą przyjaźń. Harry, Ron, Ginny, książki i czas dla siebie nadal należą do jej życia (C11-M0332, C11-M0352–C11-M0356). Nie dopisywać nowego romansu z Ronem.

Wyobrażenia wspólnego dorosłego domu, zwyczajów i nazwiska „Brown” lub „Granger-Brown” nie są zaręczynami, zmianą nazwiska ani gwarancją małżeństwa. Hermiona wyraża nadzieję na wspólną przyszłość; dzisiejsze imię pozostaje Hermiona Granger (C11-M0338–C11-M0346, C11-M0380–C11-M0408). Własna półka/sweter w domu Jamesa pozostają pragnieniem, nie wykonanym przeniesieniem (C11-M0402).

## Grangerowie i pozostali

Pożegnanie jest przyjazne; rodzice zapraszają Jamesa ponownie, dopuszczają jutrzejszą wizytę córki na uzgodnionych zasadach. Nie znają prywatnych rozmów pary (C11-M0071–C11-M0092). Luna pozostaje przyjaciółką zgodnie z C9; C11 nie zmienia tego ani relacji Jamesa z Draco, Nottem, Pansy, Harrym i Élodie.
'''
updates['06_PRZEDMIOTY_I_SEKRETY.md']='''# Przedmioty, miejsca i sekrety — aktualizacja C11

| Przedmiot / miejsce | Najnowszy stan | Źródło |
|---|---|---|
| Szczotka i fryzura | Szczotka użyta i odłożona w pokoju Hermiony. Wysoki luźny kok zrobiony 8 VII; 9 VII włosy luźniejsze, nie ten sam zachowany kok | C11-M0019–C11-M0020, C11-M0104 |
| Płaszcz i kamizelka Jamesa | Płaszcz założony przy wyjściu od Grangerów, potem oba elementy odwieszone w sypialni Jamesa | C11-M0083, C11-M0099–C11-M0100 |
| Strój Jamesa 9 VII | Czarna koszulka, czarne spodnie, pasek i skarpetki; brak opisanych butów i krawata po przebraniu | C11-M0101 |
| Strój Hermiony 9 VII | Błękitna letnia sukienka do kolan z krótkim rękawem, diament, mała torba; kolor butów i skarpetki nieustalone | C11-M0104 |
| Buty Hermiony | Zdjęte w sypialni, założone przed obiadem, ponownie zdjęte po powrocie; pozostają w sypialni. Nie opisano skarpetek ani gołych stóp | C11-M0141, C11-M0260, C11-M0313 |
| Torba | Przyniesiona do domu Jamesa; brak dokładnego miejsca odłożenia i wglądu w zawartość | C11-M0104 |
| Diamentowy naszyjnik | Na szyi Hermiony; brak zdejmowania. Pudełko nadal ostatnio w jej pokoju; nie wręczono drugiego naszyjnika | C10-M0169–C10-M0190; C11-M0104, C11-M0334–C11-M0336 |
| Książka o runach | Hermiona bierze tom za zgodą Jamesa, ogląda i odkłada na miejsce; brak wypożyczenia | C11-M0123–C11-M0126 |
| Aportatorium | James potwierdza jedyny punkt bezpiecznej aportacji do/z chronionego obiektu | C11-M0129–C11-M0134 |
| Baldachim | Zasunięty machnięciem różdżki przez Jamesa; kompletna ciemność. Nie odsunięto do końca zapisu | C11-M0313–C11-M0409 |
| Różdżka | Użyta do zasunięcia baldachimu; brak wskazanego schowania lub odłożenia. Nie zakładać stale zajętej dłoni | C11-M0313 |
| Desery | Tarta cytrynowa dla Hermiony; pudding czekoladowy z sosem i malinami oddany jej w całości i zjedzony. Los tarty nieopisany | C11-M0301–C11-M0310 |
| Własna półka Hermiony | Jedynie marzenie wypowiedziane przez nią, nie urządzona półka/pokój ani pozostawione rzeczy | C11-M0402 |

## Dom i adres — częściowe doprecyzowanie, nierozstrzygnięta rozbieżność

C11 pokazuje powrót w okolice Belgrave Square i zwiedzanie wnętrz zgodnych z dawnym opisem The Obsidian Hearth: marmurowy hol z nimfą, salon z kominkiem, Conservatory of Whispers, ametystowa jadalnia, galeria w jasnym dębie, biblioteka, aportatorium i główna sypialnia. Nie ma pokazanej przeprowadzki. Można prowadzić opis oglądanego domu, ale nie twierdzić, że sprzeczność Eaton Square / 14B Belgrave Square została jawnie wyjaśniona lub formalnie skorygowana. Nie dopisywać mechanizmu ujawnienia Fideliusa. C11-M0093–C11-M0136; C9-M0327; C10-M0163–C10-M0168.

Hermiona zna obejrzane wnętrza i wyjaśnienie aportatorium. Nie oprowadzono jej jawnie po wszystkich pokojach, łazience, pracowni i ukrytej kuchni. James sam przekazuje tam zamówienie (C11-M0259). Pełna mapa poniżej lub w MAPA.md nie jest automatycznie jej wiedzą.

## Finanse

C11-M0095: James opłaca taksówkę według licznika, ale kwota nie pada. Dawne £18 365 nie jest już potwierdzonym aktualnym stanem tej partii gotówki: należy odjąć nieustaloną cenę tego kursu, bez wymyślania stawki. Nie zmienia się od tego automatycznie saldo Gringotta i nie znamy podziału gotówki między kieszeń a dom. Nowych zakupów prezentów nie opisano.
'''
updates['09_REJESTR_KOREKT.md']='''# Rejestr korekt — aktualizacja C11

| Temat | Rozstrzygnięcie | Źródło |
|---|---|---|
| Początek | M0001–M0004 to wznowienie i cytat końca C10, nie drugie podanie szczotki. Pierwsza nowa akcja w M0005 | C11-M0001–C11-M0005 |
| Czesanie | Wykonane: wysoki luźny kok. Dawne „czesanie nie zaczęte” jest już historyczne | C11-M0019–C11-M0024 |
| Noc | Czuwanie ze świadomością, nie sen i nie udowodnione wyleczenie | C11-M0101 |
| Data i godziny | Następny dzień po 8 VII to 9 VII; 4:00 i gotowość o 9:00 jawne. Przyjście później bez minuty, koniec po obiedzie/deserze bez dokładnej godziny | C11-M0101–C11-M0104, C11-M0301–C11-M0409 |
| Pobyt | Jednodniowa wizyta z powrotem najpóźniej o 20:00; „zostaniesz na tydzień” to żart, nie nowa zgoda | C11-M0075–C11-M0078, C11-M0107–C11-M0108 |
| Zastąpiona odpowiedź | M0154 zakwestionowana w M0155, narrator przyznaje nieciągłość M0156, użytkownik prosi o poprawę M0157, obowiązująca odpowiedź M0158. Nie liczyć obu wersji jako kolejnych zdarzeń | C11-M0153–C11-M0158 |
| Granice | Korekta konkretnej odpowiedzi nie odbiera Hermionie prawa do późniejszej odmowy lub przerwy. Przy nowym geście prosi o uprzedzenie; James przeprasza | C11-M0163–C11-M0170 |
| „Szalona Hermiona” | Ta sama osoba, chwilowo swobodniejsza; nie inna osobowość ani bezwarunkowa zgoda | C11-M0257–C11-M0258 |
| Pięć lat | Wzmianka w rozmowie o odległej przyszłości; nie wyliczaj daty ślubu ani automatycznego przyzwolenia po upływie czasu | C11-M0243–C11-M0250 |
| Godność / umowa | Żart o sprzedaży godności sprostowany; rozmowa dobrowolna, Hermiona wybiera treść. Ostatecznie dziesięć minut, wykonane do końca | C11-M0287–C11-M0308, C11-M0407–C11-M0408 |
| Zazdrość i Ron | Podobanie się lekkiej zazdrości nie oznacza poparcia gróźb, przemocy, kontroli przyjaciół | C11-M0332, C11-M0352–C11-M0356 |
| Pocałunek policzka / nos | M0342 reaguje na gest z M0339 zamiast nowego pocałunku policzka M0341. Zachować ostatnią akcję użytkownika; nie dopisywać ponownego ruchu nosa | C11-M0339–C11-M0342 |
| „Pierwszy raz” komplement | Przypuszczenie Jamesa w dialogu; nowe wyraźne wyznanie w M0362 nie kasuje dawnych komplementów | C11-M0361–C11-M0364 |
| Nazwisko / żona / dom | Wyraźnie wyobrażenia odległej dorosłości i nadzieje; nie zaręczyny, ślub, nowy dom ani zmiana nazwiska | C11-M0380–C11-M0408 |
| Adresy | C11 pokazuje Belgrave Square i znajome wnętrza, ale nie zawiera jawnej korekty Eaton Square lub sceny przeprowadzki | C11-M0093–C11-M0136 |
| Ciągłość w ciemności | Narratorski opis rumieńca nie daje postaci wzroku przez zasunięty baldachim | C11-M0313–C11-M0409 |
| Ostatni blok | USER M0409 bez odpowiedzi. Nie kończyć CURRENT na M0408 ani dopisywać reakcji Hermiony | C11-M0407–C11-M0409 |

## Eksport

205 bloków TURN, 204 pary i końcowa pojedyncza wiadomość użytkownika. Zachowano tekst, kolejność i oryginalny plik. Usunięto tylko opakowanie TURN/KEY, etykiety autorów interfejsu, początkowy dzień/godzinę i końcowe linie „Przetwarzano przez…”. Pozostałości „Pokaż więcej”, wielokropki i nazwy cytowanych źródeł pozostały dosłownie; nie wiadomo, czy wielokropek był częścią treści lub interfejsu. Nie dorabiać ukrytych słów. Mapowanie w 00_MAPOWANIE_C11.md.
'''
for n,t in updates.items():
 old=(B/n).read_text()
 write(n,t.split('\n',1)[0]+'\n\n'+state+'\n'+t.split('\n',1)[1]+'\n\n---\n\n# Historia do C10 — wcześniejszy zapis z zachowanymi źródłami\n\nPoniższe „obecnie”, „aktualny”, „niewykonane” i punkty końcowe opisują stan ówczesny. W zakresie zmian C11 obowiązuje część powyżej. Nie resetuj CURRENT. Starsze niezmienione fakty i korekty nadal obowiązują.\n\n'+old)
write('08_CURRENT.md',f'''# CURRENT — jedyny punkt kontynuacji

**{state}**

## Ostatnia wiadomość — użytkownik, dosłownie

> {M[-1]['text']}

Odpowiedzi Hermiony nie ma. Nie dopisywać następnego ruchu, myśli, emocji ani kwestii Jamesa. C11-M0408 jest wcześniejszym ostatnim zwierzeniem Hermiony, nie końcem całego transkryptu.

## Scena

James i Hermiona są sam na sam na środku łóżka z baldachimem w głównej sypialni londyńskiego domu Jamesa. Zasłony zostały zasunięte różdżką w C11-M0313 i nadal panuje kompletna ciemność. Brak nowej informacji o zamknięciu drzwi na klucz lub zaklęciach dźwiękoszczelnych; nie wymyślać podsłuchu.

Wcześniej Hermiona leżała częściowo na Jamesie i kończyła zwierzenia podczas masażu. **M0409 zmienia pozycję: James leży na niej, zainicjował pocałunek i powiedział „Kocham cię”.** Nie utrzymuj poprzedniej pozycji ani nie dopisuj jej odpowiedzi. Obie postacie przytomne; rozluźnienie i senny ton Hermiony nie są zaśnięciem.

## Czas

Niedziela 9 VII 1995 wynika z następstwa po sobocie 8 VII i nocnym przejściu C11-M0101. James wstał o 4:00, był gotowy o 9:00; Hermiona przyszła później bez podanej godziny. Zwiedzanie, obiad i deser odbyły się. Dziesięć minut zwierzeń zostało zakończone przez M0407–M0408. Brak dokładnej godziny końca; nie wyznaczać jej z metadanych eksportu.

**Hermiona ma wrócić do rodziców najpóźniej o 20:00.** Nie nastąpił powrót, nie ma zgody na nocleg ani pobyt tygodniowy (M0075–M0078, M0108).

## Strój i rekwizyty

- James: czarna koszulka, czarne spodnie, czarny pasek i skarpetki z poranka M0101; brak późniejszego przebrania. Nie ma potwierdzenia założenia butów. Różdżką zasunął baldachim; jej późniejsze odłożenie/schowanie nieopisane.
- Hermiona: błękitna letnia sukienka do kolan, krótkie rękawy, diamentowy naszyjnik, luźniejsze włosy. Buty ponownie zdjęte w M0313 i pozostają w sypialni. Nie ustalono skarpetek ani bosych stóp. Małą torbę przyniosła do domu; miejsce odłożenia niepodane.
- Płaszcz i kamizelka Jamesa ostatnio na wieszaku w jego sypialni (M0099); gryfoński krawat po przebraniu nie ma wskazanego miejsca.
- Książka o runach odłożona na półkę. Szczotka została u Hermiony. Diament nie jest pierścionkiem zaręczynowym. Drugi naszyjnik i stare zwierciadło nie zostały pokazane/przekazane w C11.

## Ostatnia rozmowa i jej zakres

Hermiona dobrowolnie opowiedziała Jamesowi o przywiązaniu, potrzebie uwagi, własnym życiu i nadziejach na wspólną dorosłość. Wyobrażenia nazwiska „Brown” / „Granger-Brown”, domu, małżeństwa i półki z książkami pozostają wyobrażeniami. Jej nazwisko nadal Granger; brak zaręczyn. Ostatnie wyznanie: chce, żeby pozostali „nami” (M0408).

Lekka zazdrość nie daje zgody na groźby, przemoc i kontrolę przyjaciół; Ron, Harry, Ginny i nauka pozostają w jej życiu. „Szalona Hermiona” to ta sama postać, nie tryb znoszący granice. Aktualna prywatna rozmowa nie jest wiedzą rodziców, skrzatów, Luny lub kolegów.

## Istotne ciągłości

Noc Jamesa 8/9 VII była czuwaniem, nie snem; nie dopisuj wyleczenia. Pierwsza wizyta Hermiony i wspólny posiłek już odbyły się. Oglądała konkretne pomieszczenia, nie cały dom i jego sekrety. Adres obecnego pobytu: 14B Belgrave Square z C10; C11 pokazuje dojazd w tę okolicę i znajome wnętrza. Dawna rozbieżność z Eaton Square nie ma jawnego rozstrzygnięcia.

Nie importuj zdarzeń z odrębnych kampanii. Zasada książkowego przebiegu z zachowaniem rozegranego AU pozostaje. Dalsze źródła: 04_KTO_CO_WIE, 09_REJESTR_KOREKT, 10_ZASADY_I_CIAGLOSC oraz indeks scen C11.
''')
oldopen=(B/'07_OTWARTE_WATKI.md').read_text();rest=oldopen.split('| Zamek i Fiu |',1)[1].split('## Wykonane',1)[0]
rest=rest.replace('C10 pokazuje sen Hermiony, nie potwierdza nowego snu Jamesa. Brak raportu i diagnozy; dawna wspólna wizyta pozostaje odbytą', 'C11 potwierdza noc 8/9 VII w czuwaniu. Brak nowego raportu i diagnozy; dawna wspólna wizyta pozostaje odbytą').replace('C10-M0403–C10-M0411 |', 'C10-M0403–C10-M0411; C11-M0101 |')
write('07_OTWARTE_WATKI.md',f'''# Otwarte wątki — po C11

{state}

## Najbliższe

| Wątek | Stan | Źródło |
|---|---|---|
| Odpowiedź Hermiony | Ostatnia akcja Jamesa i „Kocham cię”; odpowiedź NPC niezapisana | C11-M0409 |
| Dokończenie wizyty | Trwa po obiedzie/deserze; powrót do 20:00, bez odjazdu i noclegu | C11-M0075–C11-M0078, C11-M0313–C11-M0409 |
| Biblioteka | Hermiona chce wrócić do lektury, ale dotąd oglądała jeden odłożony tom | C11-M0123–C11-M0126 |
| Własne miejsce Hermiony | Półka/książki/sweter tylko w wyobrażeniu; nie utworzone | C11-M0402 |
| Wizyta rodziców u Jamesa | Zaproszenie nadal bez wykonania; Hermiona przyszła sama | C10-M0259–C10-M0264; C11-M0075–C11-M0078 |
| Zamek i Fiu |{rest}

## Aktualizacje do starszej tabeli

Sen: C11-M0101 potwierdza kolejną noc czuwania, bez raportu Pomfrey. Adresy nadal nierozstrzygnięte, choć C11 pokazuje Belgrave Square i znajome wnętrza. Stare zwierciadło nie zostało obejrzane przez Hermionę podczas zwiedzania; drugi naszyjnik nadal niewręczony.

## Wykonane — nie otwierać ponownie

Czesanie i fryzura 8 VII; zakończenie wizyty u Grangerów i powrót Jamesa; ustalenie dnia odwiedzin oraz limitu 20:00; przybycie Hermiony 9 VII; opisane zwiedzanie; obiad; oddanie i zjedzenie puddingu; dziesięć minut zwierzeń (C11-M0019–C11-M0024, C11-M0091–C11-M0136, C11-M0289–C11-M0314, C11-M0407–C11-M0408). Dawne wykonane wydarzenia C1–C10, w tym finał i wręczenie diamentu, pozostają.
''')
rules=(B/'10_ZASADY_I_CIAGLOSC.md').read_text()
rules=rules.replace('Stan do C10-M0506.','Stan do C11-M0409.').replace('W kolejnej części użyj C11.','W kolejnej części użyj C12.').replace('Nie przenumerowuj dostarczonych C1–C10','Nie przenumerowuj dostarczonych C1–C11')
# Mark old end-state paragraphs as historical, not active instructions.
rules=rules.replace('Obecny punkt wyznacza C10-M0506','Historyczny punkt C10 wyznacza C10-M0506').replace('aktualny lorebook: 11_LOREBOOK_HOGWARTS_C1-C10.md','lorebook tamtej wersji: 11_LOREBOOK_HOGWARTS_C1-C10.md').replace('Aktualnie C10-M0506','Historycznie na końcu C10: C10-M0506').replace('- Aktualny koniec jest po odpowiedzi NPC:', '- Historyczny koniec C10 był po odpowiedzi NPC:')
write('10_ZASADY_I_CIAGLOSC.md',rules+'''

## Aktualny tryb po C11

- CURRENT kończy się na USER C11-M0409; następna reakcja należy do NPC, bez dodatkowej akcji Jamesa.
- C11-M0154 jest odpowiedzią zastąpioną przez M0158. Zapis archiwalny zachowuje obie, kanon nie sumuje ich jako kolejnych scen.
- Ciemność, umówiony powrót do 20:00, ubrania i ostatnia pozycja obowiązują. Nie powtarzać wykonanego czesania, pierwszego wejścia, obiadu ani zwierzeń.
- Nadzieje na ślub, nazwisko i wspólny dom nie są faktami przyszłości. Nie łączyć tej kampanii z inną historią Jamesa na podstawie samego imienia.
- Pełne archiwa czytaj celowo: indeks scen → zakres ID → odpowiedni mały fragment albo pojedynczy duży Part. Nie wczytuj wszystkich archiwów przy każdej turze.
- W repozytorium instrukcja robocza jest w AGENTS.md, bieżące skróty w 02_PLIKI_AKTYWNE, pełna baza w 05_BAZA_PELNA. Lorebook jest dodatkiem, nie automatycznym mechanizmem słów kluczowych i nie zastępuje korekt.
- Aktualizacja plików odbywa się na zlecenie. Zapis paczki nie oznacza automatycznej podmiany załączników projektu lub publikacji w GitHubie.
''')
# C11 scene boundaries cover every message exactly once.
scenes=[(1,4,'Wznowienie i cytat końca C10 — poza nową akcją'),(5,24,'Czesanie i wysoki luźny kok'),(25,58,'Czułość, komplementy i zabawa w milczenie'),(59,70,'Zejście na dół; rodzice poznają historię młodszej siostry'),(71,82,'Pożegnanie i umówienie wizyty 9 VII; powrót do 20:00'),(83,92,'Płaszcz, szeptana prośba o sukienkę i wyjście'),(93,100,'Taksówka, opłata bez kwoty i powrót do sypialni'),(101,102,'Noc czuwania, trening od 4:00, gotowość o 9:00, przybycie gościa'),(103,110,'Powitanie Hermiony: sukienka, diament, wejście'),(111,118,'Salon, oranżeria i jadalnia; odziedziczony wystrój'),(119,126,'Portrety Slytherinów i biblioteka; zgoda na lekturę'),(127,134,'Aportatorium i wyjaśnienie wyjątku od zabezpieczeń'),(135,152,'Sypialnia, zdjęcie butów, odpoczynek'),(153,158,'Korekta odrzuconej odpowiedzi M0154; nowa M0158'),(159,170,'Doprecyzowanie uprzedzania przed nowym gestem'),(171,212,'Wzajemna inicjatywa i zmiany pozycji'),(213,250,'Przerwa, rozmowa o granicach i przyszłości'),(251,278,'Zamówienie obiadu, buty, rozmowa o sukience'),(279,300,'Jadalnia, wspólny obiad, negocjacja zwierzeń'),(301,310,'Desery; dobrowolna umowa i oddanie całego puddingu'),(311,314,'Powrót na górę, zdjęcie butów, zasunięcie baldachimu'),(315,336,'Zwierzenia: uwaga, bliskość, zazdrość, naszyjnik'),(337,350,'Wyobrażenia codziennej dorosłości, nie wykonane wydarzenia'),(351,368,'Przyjaciele i Ron; granice zazdrości, komplementy i uwzględnianie zdania'),(369,378,'Szukanie wzrokiem, dzielenie się wiadomościami i jawny związek'),(379,396,'Wyobrażane nazwisko i wspólny dom; brak zaręczyn'),(397,406,'Masaż, wspomnienie czesania, półka i miejsce w bibliotece'),(407,409,'Koniec zwierzeń i ostatnia akcja Jamesa bez odpowiedzi')]
assert [i for a,b,t in scenes for i in range(a,b+1)]==list(range(1,410))
oldidx=(B/'01_ARCHIWUM_SCEN_INDEKS.md').read_text().split('## Czat 10',1)[1]
oldidx='## Czat 10'+oldidx.replace('— aktualna część','— wcześniejsza część').replace('— aktualny koniec','— historyczny koniec C10')
write('01_ARCHIWUM_SCEN_INDEKS.md','# Indeks scen — C1–C11\n\n10 936 wiadomości. Indeks obejmuje także OOC i odrzucone wersje; status rozstrzyga rejestr korekt. Wybór pliku według ID przez indeks dużych lub małych części.\n\n## Czat 11 — aktualna część\n\n| Blok | Wiadomości | Zawartość |\n|---|---|---|\n'+table([(f'C11-S{i:02d}',ref(a,b),t) for i,(a,b,t) in enumerate(scenes,1)])+'\n\n'+oldidx)
write('00_MAPOWANIE_C11.md','''# Mapowanie eksportu Part11

Oryginał: `oryginaly/chatgpt_caly_czat11.txt`, zachowany bajt w bajt. 205 bloków TURN, 409 wiadomości. Bloki 1–204 zawierają USER i ASSISTANT; blok 205 tylko USER. UNKNOWN w nagłówku rozstrzygnięto po etykietach wewnątrz bloku, nie przez zgadywanie autora.

Usunięto separatory TURN/KEY, etykiety „Twoja wiadomość:” / „ChatGPT powiedział:”, początkowy dzień/godzinę interfejsu i końcowe linie „Przetwarzano przez…”. Wyrównano białe znaki na brzegach wiadomości. Nie zmieniano pisowni, kolejności, cytatów, OOC i pozostałości cytowań. „Pokaż więcej” i poprzedzający wielokropek w M0019 pozostają dosłownie; bez odtwarzania hipotetycznych braków. Metadane czasu interfejsu nie są czasem fabuły.

| TURN | USER | ASSISTANT | KEY |
|---|---|---|---|
'''+table([(x['turn'],x['ids'][0],x['ids'][1] if len(x['ids'])>1 else 'brak',x['key']) for x in mapping]))
write('00_INDEKS_DUZYCH_CZESCI.md','# Indeks dużych części — C1–C11\n\nKażdy plik to jeden Part, w dotychczasowym formacie ID. Konkretne sceny: 01_ARCHIWUM_SCEN_INDEKS.md. Połączenie poniższych plików w tej kolejności odtwarza archiwum scalone bajt w bajt.\n\n| Part | Plik | Początek | Koniec | Wiadomości |\n|---|---|---|---|---|\n'+table([(c['part'],f"[{Path(c['file']).name}]({c['file']})",c['first'],c['last'],c['messages']) for c in big]))
write('00_INDEKS_MNIEJSZYCH_CZESCI.md','# Indeks mniejszych części — C1–C11\n\n60 fragmentów, do 200 pełnych wiadomości, bez zmiany ID. Pierwsze 57 plików C1–C10 zachowano bajt w bajt, dodano 58–60 dla C11. Połączenie w kolejności odtwarza scalone archiwum. W dawnym podziale nagłówek następnego Part może być na końcu poprzedniego fragmentu; samych wiadomości nie rozcięto.\n\n| Plik | Początek | Koniec | Wiadomości | KiB |\n|---|---|---|---|---|\n'+table([(f"[{Path(c['file']).name}]({c['file']})",c['first'],c['last'],c['messages'],f"{c['bytes']/1024:.1f}") for c in chunks]))
# Full lorebook: exact historical/world entries retained with explicit historical scope.
lore=json.loads((B/'Hogwarts_RPG_1994_SpicyChat_PL_EN_SAFE.json').read_text());entries=[]
for n,t in [('RPG — pierwszeństwo i użycie',state+' Czytaj CURRENT, zasady, korekty i wiedzę NPC. Stan C11 ma pierwszeństwo tylko w zakresie zmian. James wyłącznie użytkownika; następna odpowiedź NPC. Rozdziel fakty, deklaracje, plany i wyobrażenia.')]+[(f'C11 — {n[3:-3]}', (O/n).read_text().split('# Historia do C10')[0]) for n in updates]+[('C11 — CURRENT',(O/'08_CURRENT.md').read_text()),('C11 — otwarte wątki',(O/'07_OTWARTE_WATKI.md').read_text())]:
 keys=[n,'James Brown','Hermiona Granger','9 lipca','C11'];entries.append(dict(name=n,keys=keys,keywords=keys,content=t.strip()))
for e in lore['entries']:
 e=dict(e)
 if not e['name'].startswith('ŚWIAT'):
  e['name']='HISTORIA DO C10 — '+e['name'];e['content']='ZAPIS HISTORYCZNY DO C10. Dawny punkt końcowy i statusy mogą być zmienione przez C11; nie jest to bieżący CURRENT. Niezmienione fakty pozostają.\n\n'+e['content']
 entries.append(e)
lore={'name':'Hogwarts RPG — C1–C11','description':'Stan C11-M0409, 9 VII 1995 po obiedzie i deserze. Aktualizacja C11, historyczne wpisy do C10 oraz niezmienione wpisy świata. Nie testowano importu w zewnętrznej aplikacji.','entries':entries}
write('Hogwarts_RPG_1994_SpicyChat_PL_EN_SAFE.json',json.dumps(lore,ensure_ascii=False,indent=2))
write('11_LOREBOOK_HOGWARTS_C1-C11.md','# Lorebook Hogwart — C1–C11\n\n'+lore['description']+f'\n\nLiczba wpisów: {len(entries)}.\n\n'+'\n\n'.join(f"## Wpis {i:03d}: {e['name']}\n\nSłowa kluczowe: {', '.join(e['keys'])}\n\n{e['content']}" for i,e in enumerate(entries,1)))
write('00_START.md',f'''# Baza kampanii C1–C11

{state}

11 dużych części, 60 mniejszych fragmentów, 10 936 wiadomości. Nowe C11: 409 wiadomości z 205 TURN; ostatnia wiadomość to USER bez odpowiedzi. C1–C10 zachowane bajt w bajt. Oryginały C10 i C11 w `oryginaly/`, poprzednia baza w `historia_wersji/do_C10/`.

Najpierw 08_CURRENT, 10_ZASADY_I_CIAGLOSC, 09_REJESTR_KOREKT i 04_KTO_CO_WIE. Potem właściwy dział i wskazany fragment archiwum. Indeks scen obejmuje tematy, indeksy dużych i małych części kierują do plików po ID. Nie trzeba czytać wszystkich archiwów dla pojedynczej odpowiedzi.

Zachowano dotychczasowe pełne pliki tematyczne z oznaczoną historią; nowe sekcje C11 zmieniają tylko swój zakres. Osobny pakiet RPG-Archiwum_GitHub_C1-C11 ma krótsze pliki aktywne i komplet do repozytorium. Archiwa są przechowywane bez naprawiania dialogów, a odrzucone wersje oznaczone w korektach.

Sprawdzono pełne C11 i jego powiązania z bazą C10, kompletność i zgodność dawnych plików. Nie wykonywano ponownej interpretacji wszystkich 10 527 dawnych wiadomości ani nie twierdzi się, że wszystkie dawne streszczenia są bezbłędne.

Zapis paczki nie podmienia załączników projektu ani nie publikuje repozytorium. Przy podmianie źródeł korzystaj z jednego zestawu bieżących plików, bez równoległych starych CURRENT.
''')
ids=[x.decode() for x in re.findall(rb'^\[(C\d+-M\d{4})\]\r?$',merged,re.M)]
assert len(ids)==len(set(ids))==10936
counts={f'C{i}':sum(x.startswith(f'C{i}-') for x in ids) for i in range(1,12)}
for c,n in counts.items():assert [x for x in ids if x.startswith(c+'-')]==[f'{c}-M{i:04d}' for i in range(1,n+1)]
control=dict(version='C1-C11',current_id='C11-M0409',current_date='1995-07-09',current_time='po obiedzie i deserze; dokładna godzina nieustalona',next_turn='ASSISTANT — NPC Hermiona',message_counts=counts,total_messages=len(ids),source_c11_turns=205,source_c11_messages=409,smaller_parts=len(chunks),large_parts=len(big),lorebook_entries=len(entries),world_entries=sum(e['name'].startswith('ŚWIAT') for e in entries),merged_sha256=sha(merged),previous_merged_sha256=sha(base),source_c11_sha256=sha((O/'oryginaly/chatgpt_caly_czat11.txt').read_bytes()),chunks=chunks,large_files=big,checks=dict(c1_c10_byte_prefix=True,previous_57_chunks_unchanged=True,small_and_large_concatenations_exact=True,unique_contiguous_ids=True,c11_scene_coverage_complete=True,raw_c11_unchanged=True),scope='Pełna analiza C11 i porównanie z bazą C10; kontrola bajtowa C1–C10. Nie pełny ponowny odczyt całej wcześniejszej kampanii.')
write('KONTROLA_ARCHIWUM.json',json.dumps(control,ensure_ascii=False,indent=2))
(O/'scenes_c11.json').write_text(json.dumps(scenes,ensure_ascii=False,indent=2))
print(json.dumps(dict(total=len(ids),counts=counts,small=len(chunks),big=len(big),lore=len(entries)),ensure_ascii=False))
