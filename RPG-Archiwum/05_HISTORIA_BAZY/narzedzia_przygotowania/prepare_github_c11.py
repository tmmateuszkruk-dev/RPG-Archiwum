from pathlib import Path
import json,re,shutil,hashlib,zipfile
R=Path('/workspace/scratch/d9fac05cbafd');O=R/'RPG_Baza_Wiedzy_11_czesci';G=R/'RPG-Archiwum_GitHub_C1-C11';B=R/'c10_restored'
def put(n,t):
 p=G/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t.strip()+'\n')
def cp(s,n):
 p=G/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(s,p)
def table(rows):return '\n'.join('| '+' | '.join(map(str,x))+' |' for x in rows)
C=json.loads((O/'KONTROLA_ARCHIWUM.json').read_text()); small=C['chunks'];big=C['large_files']
for p in O.glob('*.md'):cp(p,'05_BAZA_PELNA/'+p.name)
for p in O.glob('*.json'):cp(p,'05_BAZA_PELNA/'+p.name)
for c in big:cp(O/c['file'],'01_ARCHIWA_CZATY/'+Path(c['file']).name)
for c in small:cp(O/c['file'],'01_ARCHIWA_CZATY/mniejsze_czesci/'+Path(c['file']).name)
cp(O/'01_ARCHIWUM_CZAT_1-11_SCALONE.txt','01_ARCHIWA_CZATY/scalone/01_ARCHIWUM_CZAT_1-11_SCALONE.txt')
for p in (O/'oryginaly').iterdir():cp(p,'04_ORYGINALY/'+p.name)
for p in (O/'historia_wersji/do_C10').iterdir():cp(p,'06_HISTORIA_BAZY/do_C10/'+p.name)
# Correct links in full-base indices for the repo layout.
for name in ['00_INDEKS_DUZYCH_CZESCI.md','00_INDEKS_MNIEJSZYCH_CZESCI.md']:
 p=G/'05_BAZA_PELNA'/name;s=p.read_text();s=s.replace('(duze_czesci/','(../01_ARCHIWA_CZATY/').replace('(mniejsze_czesci/','(../01_ARCHIWA_CZATY/mniejsze_czesci/');p.write_text(s)
cp(O/'08_CURRENT.md','02_PLIKI_AKTYWNE/08_CURRENT.md')
# Small current files contain actual current changes + durable anchors. Full source history remains external.
anchors={
'02_TIMELINE.md':'''## Wcześniejsza oś kampanii — skrót

Początek 1 IX 1994, transfer Jamesa do Slytherinu; rozwój znajomości z Hermioną, bal 25 XII i after w Pokoju Życzeń. Pod koniec lutego związek, treningi, częściowa poprawa snu; przeskok w C7 do 23 VI. 24 VI w C8 odpoczynek nad jeziorem, a finał dopiero w C9. Cedric ginie, fałszywy Moody zostaje ujawniony, Voldemort wraca. Uczta 30 VI, wyjazd 1 VII; późniejsza jawna korekta dat ma pierwszeństwo. 5 VII list ustala wizytę 8 VII. James poznaje Grangerów, wręcza kwiaty i zwierciadło, w C10 daje Hermionie diament, jedzą obiad, idą do Hampstead Heath i wracają. Szczegóły i źródła: pełny TIMELINE oraz indeks scen C1–C10.
''',
'03_PROFILE_POSTACI.md':'''## Trwałe kotwice

James: 15 lat, około 180 cm, blond włosy; IV rok ukończony, data urodzenia nieustalona. Rodzice i młodsza siostra zginęli, gdy miał 5 lat, siostra 4; imiona i sprawca nieustalone. Rodzice uczyli go magicznej obrony; połączył ich style. Pochodzenie od Salazara potwierdzono jako AU, początkowo było dla uczniów plotką; „ostatni publicznie znany” nie znaczy jedyny biologiczny potomek. Majątek rzeczywisty, Lodgok jest goblinem zarządcą. Źródła: C1-M1187–C1-M1189, C2-M1578–C2-M1580, C5-M0439–C5-M0461, C6-M0114–C6-M0119; pełny profil rozstrzyga szczegóły.

Hermiona: 15 lat, około 163 cm; własna nauka, przyjaciele i cele. Nie „terapeutka” ani osoba podporządkowana związkowi. Draco zachowuje dumę, uprzedzenia i samodzielność; respekt nie jest uległością. Pansy nie staje się przyjaciółką Hermiony, Nott nie żartuje przy każdym geście, Ron nie jest tylko obiektem drwin. Luna pozostaje przyjaciółką Jamesa (C9-M0231–C9-M0254), Élodie koleżanką bez potwierdzonego romansu. Nie importować innej kampanii o ślubie Jamesa i Luny.

Cedric nie żyje; prawdziwy Moody nie prowadził zajęć impostora. Crouch Junior został zdemaskowany, a Pocałunek dementora jest znany z relacji w szpitalu, nie równa się stwierdzonej biologicznej śmierci (C9-M0061–C9-M0086).
''',
'04_KTO_CO_WIE.md':'''## Wcześniejsze ważne granice wiedzy

- Hermiona zna tragedię Jamesa, czuwanie, ich wcześniejsze rozmowy i rzeczywiste sny; nie zna automatycznie nowej nocy 8/9 VII. Pomfrey zna problem snu i historię leczenia; wspólna wizyta została uznana za odbytą w C6-M0375, wyników nie dopisano.
- James zna sekret Pettigrew i niewinność/psią postać Syriusza od C6-M0216–C6-M0234. W C9 podsłuchał część ujawnienia fałszywego Moody’ego, ale odszedł przed pełnym przesłuchaniem. Hermiona nie zna automatycznie całego podsłuchu; Dumbledore, McGonagall i Snape widzieli Jamesa przy drzwiach, nie muszą znać dokładnego zakresu tego, co usłyszał (C9-M0064–C9-M0086).
- Szkoła usłyszała na uczcie o zamordowaniu Cedrika i powrocie Voldemorta; nie jest to uznanie tych faktów przez Ministerstwo (C9-M0112–C9-M0114).
- Grangerowie poznali Jamesa, jego związek, ogólny majątek, Lodgoka, 14B Belgrave Square, list około 30 stron i historię unikania z pierwszorocznymi. Nie znają cen/salda, pełnej tragedii, bezsenności ani rozmów na piętrze. Według Hermiony powiedziała im o śmierci Cedrika i słowach Dumbledore’a, bez całej historii Harry’ego (C10-M0002–C10-M0008, C10-M0195–C10-M0252, C10-M0372–C10-M0374).
- Konflikt z Draco nie ma udowodnionych wszystkich świadków; Krum, Hermiona i Luna otrzymali różne ograniczone relacje. Nott i Pansy nie znają automatycznie pełnej rozmowy (C8-M0086–C8-M0100, C8-M0111–C8-M0134, C8-M0217–C8-M0237, C8-M0625–C8-M0626).
''',
'05_RELACJE.md':'''## Wcześniejsze kotwice

Partnerem Hermiony na balu był James, nie Krum; rozmowy o alternatywnych parach nie zmieniają kampanii. Związek nie jest nowym szkolnym odkryciem. Nie używać „Hermionka” po odwołaniu zgody (C2-M1591–C2-M1594; C3-M1130). Ślizgońsko-gryfońskie krawaty pozostają wakacyjną wymianą, nie zaręczynami (C9-M0115–C9-M0116).

Luna: jawna przyjaźń, bez potwierdzonego zakochania (C9-M0231–C9-M0254). Élodie: korespondencja i możliwość spotkań, bez potwierdzonego romansu. Draco: nie ma nowego rozejmu; Ron: brak pełnego pojednania i brak potwierdzonego wyznania uczuć do Hermiony. Nott według własnej relacji nie jest oficjalną parą z Daphne (C8-M0601–C8-M0604). Szczegóły pozostałych relacji w pełnej bazie.
''',
'06_PRZEDMIOTY_I_SEKRETY.md':'''## Kotwice sprzed C11

Diament (£875) wręczony Hermionie 8 VII; drugi naszyjnik, szmaragd/rubin (£650), niewręczony, ostatnio w czerwonym pudełku w walizeczce u Jamesa. Nowe zwierciadło ze wspomnieniem wejścia na bal podarowane Grangerom i na komodzie; dawne małe zwierciadło nadal Jamesa, niepokazane Hermionie. Zwierciadła odtwarzają zapis, nie są komunikatorem ani podglądem na żywo. Zdjęcie rodziny to osobny przedmiot (C9-M0312–C9-M0374, C9-M0401–C9-M0410; C10-M0169–C10-M0190).

Kufer z pociągu wniesiono nieotwarty do sypialni; walizeczka z gotówką i podział jej zawartości pozostają jak w pełnej bazie, bez domyślnego przejrzenia przez gościa. Szata została podarowana Lunie. Wypuszczenie Rity zapowiedziano, ale nie pokazano (C8-M0628–C8-M0630; C9-M0143–C9-M0148, C9-M0328–C9-M0336).

Saldo po wymianie: 487 312 240 galeonów w zinwentaryzowanych pieniądzach, nie wycena całego majątku. £18 365 było bilansem znanych wydatków do C10, teraz pomniejszonym o niepodaną cenę taksówki C11. Fundusz Toma ma nieustaloną kwotę i nie jest rozliczony (C9-M0287–C9-M0311).
''',
'09_REJESTR_KOREKT.md':'''## Nadrzędne kotwice starszych korekt

James wyłącznie użytkownika. Późniejsza jawna korekta zastępuje starszą tylko w swoim zakresie, nie każdy późniejszy błąd narratora. Sceny odrzucone pozostają w archiwum, lecz nie są dodatkowymi zdarzeniami. Wersja C5 ma 766 wiadomości; stare C5v1 rozwiązuj przez mapowanie. Początkowa plotka o pochodzeniu nie unieważnia późniejszej korekty potwierdzającej genealogię. Tragedia: James 5 lat, siostra 4. Wzrost Jamesa 180 cm i Hermiony około 163 cm to późniejsze ustalenia, a nie wiecznie otwarte dane. Źródła i całość korekt w 05_BAZA_PELNA/09_REJESTR_KOREKT.md.

Draco nie staje się potulny; korekty C8 przeciwdziałają Hermionie-terapeutce i chórowi drwin z Rona. Pochwała pojedynczego gestu nie jest globalną zgodą. Zdarzały się rzeczywiste sny, lecz nie udowodniono trwałego wyleczenia. Nieznana forma bogina i pierwotne źródło rdzenia różdżki pozostają niepotwierdzone.

C9-M0109–C9-M0113 korygują daty: uczta 30 VI, wyjazd 1 VII. C9-M0413 jest wtrąceniem, nie resetem. C10-M0367 rozszerza książkowy domyślny przebieg na dalszą kampanię z zachowaniem rozegranego AU. Płaszcz został zdjęty przy wejściu u Grangerów według C10-M0275–C10-M0278; pudełko diamentu rzeczywiście wręczono mimo pominiętego przełożenia między kieszeniami.
'''
}
for n,anchor in anchors.items():
 s=(O/n).read_text().split('# Historia do C10')[0].rstrip().removesuffix('---').rstrip()
 put('02_PLIKI_AKTYWNE/'+n,s+'\n\n'+anchor+'\n\nPełny dział z wcześniejszymi źródłami: [wersja pełna](../05_BAZA_PELNA/'+n+').')
cp(O/'07_OTWARTE_WATKI.md','02_PLIKI_AKTYWNE/07_OTWARTE_WATKI.md')
put('02_PLIKI_AKTYWNE/10_ZASADY_I_CIAGLOSC.md','''# Zasady i ciągłość — C1–C11

1. Prowadź RPG po polsku. Użytkownik steruje tylko Jamesem Brownem; narrator światem i NPC. Nie dopisuj Jamesowi myśli, uczuć, kwestii, reakcji, decyzji ani ruchów.
2. Przed pierwszą kontynuacją przeczytaj 08_CURRENT, ten plik, 09_REJESTR_KOREKT i 04_KTO_CO_WIE. W kolejnych turach rozwijaj bieżącą rozmowę; nie cofaj jej do zapisanego CURRENT.
3. CURRENT kończy się na C11-M0409, po akcji użytkownika. Następna odpowiedź należy do Hermiony, ale bez jej dopisania podczas aktualizacji bazy.
4. Weryfikuj ważny fakt w odpowiednim dziale. Gdy skrót nie wystarcza: indeks scen → ID → jeden mały fragment; duży Part tylko dla szerszej sceny. Nie czytaj wszystkich archiwów naraz.
5. Późniejsze jawne korekty użytkownika mają pierwszeństwo w swoim zakresie. Odrzucone odpowiedzi i omyłki narratora nie są kanonem. Oddziel fakty, relacje postaci, plotki, plany, domysły i wyobrażenia.
6. NPC zna tylko to, co widział, usłyszał lub wiarygodnie poznał. Pliki i prywatne myśli Jamesa nie są wiedzą NPC. Pilnuj świadków, szeptu, odległości, ciemności, miejsca i czasu.
7. Zachowuj niezależne charaktery, wiek, granice i zainteresowania postaci. Draco: duma i uprzedzenia mimo respektu; Nott: nie stały dowcipniś; Pansy: nie automatyczna przyjaciółka Hermiony; Ron: nie tylko cel zbiorowych drwin. Hermiona ma rodzinę, przyjaciół, naukę i własne zdanie. Żart o „szalonej Hermionie” nie zmienia osobowości ani granic.
8. Charaktery opieraj na książkach, wygląd i mundurki na filmach, z pierwszeństwem kampanii. Od C10-M0367 książki są domyślną drogą całej dalszej kampanii, z naturalnym wplataniem Jamesa i zachowaniem rozegranych zmian AU. Nie narzucaj przyszłych wydarzeń lub działań Jamesa w imię kanonu.
9. Lorebook jest uzupełnieniem, nie automatycznym wyzwalaczem słów kluczowych. Przyszła wiedza z książek nie przechodzi do NPC.
10. Pisz naturalną narrację, bez technicznych wyjaśnień w dialogach, mechanicznego komentowania każdego gestu i stałego chóru reakcji.
11. Gdy źródła nie można odczytać, powiedz to krótko. Nie twierdź, że sprawdziłeś nieprzeczytany plik, i nie rekonstruuj brakującej historii z domysłu. Pytaj tylko, gdy brak blokuje spójną kontynuację.
12. Na zleconą aktualizację zachowaj oryginalny transkrypt, stabilne ID i korekty, uaktualnij CURRENT bez następnej akcji. Nie obiecuj automatycznej aktualizacji plików, projektu lub GitHuba. Następna część ma prefiks C12.

Pełne reguły i historyczne źródła: [10_ZASADY_I_CIAGLOSC](../05_BAZA_PELNA/10_ZASADY_I_CIAGLOSC.md).
''')
put('02_PLIKI_AKTYWNE/MAPA.md','''# Mapa miejsc — stan C11

To mapa opisowa kampanii, nie dokładny plan pięter. Nie dopisuje połączeń, których nie ustalono.

| Miejsce | Stan i wiedza | Źródło |
|---|---|---|
| Dom Grangerów, 8 Heathgate, Londyn | Wizyta Jamesa 8 VII zakończona; pokój Hermiony na piętrze, rodzice poznani. Szczotka i pudełko naszyjnika pozostały tutaj | C9-M0395–C10-M0506; C11-M0005–C11-M0092 |
| Londyński dom Jamesa, adres pobytu 14B Belgrave Square | Hermiona odwiedza 9 VII. Wcześniejszy opis The Obsidian Hearth wskazywał Eaton Square; nie ma jawnego rozstrzygnięcia tożsamości adresów | C9-M0327; C10-M0163–C10-M0168; C11-M0093–C11-M0136 |
| Hol | Jasny marmur, samoczyszcząca figura nimfy; Hermiona widziała | C11-M0110 |
| Salon powitalny | Kominek, miejsce rozmów; widziany | C11-M0112 |
| The Conservatory of Whispers | Zaczarowane niebo Francji, samopodlewające rośliny i nucące białe róże; widziany | C11-M0114–C11-M0115 |
| Jadalnia | Ametystowe akcenty, wielki marmurowy stół, żyrandol. Para zjadła tutaj obiad obok siebie | C11-M0116, C11-M0279–C11-M0310 |
| Gabinet / galeria | Jasny dąb, rodzinne portrety rodu Slytherina według Jamesa; widziane | C11-M0120–C11-M0122 |
| Biblioteka | Runy, zielarstwo, prawo magiczne; zgoda na lekturę, jeden tom odłożony | C11-M0122–C11-M0126 |
| Aportatorium | Bez okien, dywany, runy. Jedyny punkt bezpiecznej aportacji do/z chronionego domu; Hermiona poznała wyjaśnienie | C11-M0128–C11-M0134 |
| Główna sypialnia | Obecna scena: łóżko z baldachimem, zielone tkaniny, zasłony zamknięte, całkowita ciemność | C11-M0098, C11-M0136, C11-M0313–C11-M0409 |
| Ukryta kuchnia | James przekazał skrzatom zamówienie; Hermiona nie brała udziału w tej wizycie | C11-M0259 |
| Łazienka, pokoje gościnne, pracownia eliksirów | Elementy wcześniejszego opisu domu, bez pokazanego oprowadzenia Hermiony | C9-M0327 |
| Zamek w Szkocji | James mówi o Fiu; wyjazd pozostaje planem | C10-M0253–C10-M0264 |
| Pokój Życzeń w Hogwarcie | Ważne wcześniejsze miejsce spotkań, treningów i afteru, nie obecna lokalizacja | indeks scen C2–C8 |

Obejrzenie domu nie daje wiedzy o wszystkich zabezpieczeniach. Nie ustalono Strażnika Fideliusa ani mechanizmu dopuszczenia Hermiony. Nie rysować dokładnej topologii pięter z kolejności zwiedzania.
''')
put('02_PLIKI_AKTYWNE/LOREBOOK.md','''# Lorebook aktywny — C1–C11

Skrót do bieżących scen; pełne 265 wpisów świata i historii: [11_LOREBOOK_HOGWARTS_C1-C11](../05_BAZA_PELNA/11_LOREBOOK_HOGWARTS_C1-C11.md). JSON jest obok, dla aplikacji używających lorebooków. Nie zakładać automatycznego uruchamiania wpisów po słowach kluczowych.

| Klucze | Bieżąca zasada |
|---|---|
| CURRENT, C11, kontynuacja | 9 VII 1995, po obiedzie i deserze; sypialnia Jamesa, całkowita ciemność, koniec na C11-M0409. Następna odpowiedź NPC |
| James Brown, Slytherin | Wyłącznie postać użytkownika; 15 lat; po IV roku. Potwierdzone AU genealogii, nie automatyczna władza nad szkołą |
| Hermiona, Granger, Brown | Partnerka Jamesa, 15 lat, własne cele. „Brown” i „Granger-Brown” to prywatne wyobrażenia przyszłości, bez zaręczyn i zmiany nazwiska |
| czuwanie, sen, Pomfrey | Rzeczywiste sny zdarzały się wcześniej. Noc 8/9 VII to czuwanie; brak trwałego wyleczenia i nowej diagnozy |
| Belgrave Square, Eaton Square, dom | Bieżący adres pobytu 14B Belgrave Square, znajome wnętrza zwiedzane w C11; sprzeczność z wcześniejszym Eaton Square nadal nie ma jawnej korekty |
| biblioteka, runy | Hermiona ma zgodę na lekturę, jeden tom odłożyła. Nie przeczytała całego księgozbioru |
| aportatorium | Wyjątek od blokady aportacji do/z domu; nie dowód uprawnień ani pokaz aportacji Jamesa |
| rodzice, 20:00 | Zgoda na dzienną wizytę 9 VII z powrotem do 20:00. Nie byli obecni przy zwierzeniach |
| Ron, zazdrość | Drobna zazdrość może podobać się Hermionie, lecz groźby, przemoc i kontrola przyjaciół nie |
| diament, zwierciadło | Diament na Hermionie, bez zaręczyn; nowe zwierciadło u rodziców, stary egzemplarz niepokazany |
| finał, Cedric, Moody, Voldemort | Finał odbyty w C9. Cedric nie żyje, impostor ujawniony, Voldemort powrócił; wiedza NPC nadal zależy od źródła |
| Luna, Élodie | C9: Luna przyjaciółka, Élodie koleżanka; nie przenosić romansu ani małżeństwa z innej kampanii |

Encyklopedia nie nadpisuje AU, korekt i wydarzeń. Przyszłe tomy nie narzucają faktów ani wiedzy NPC.
''')
# Rich two-level navigation.
summaries={1:'Początek kampanii, transfer, lekcje i biblioteka; rozwój znajomości z Hermioną.',2:'Rozwój relacji i przygotowania do balu; nauka, organizacja oraz rodzinne ujawnienia.',3:'Bal, after w Pokoju Życzeń i późniejsze wspólne sceny; pierwsze jednoznaczne sny.',4:'Dalsze sceny pary, szkolna codzienność, sen i Pomfrey; koniec 24 II.',5:'Pełniejszy zapis 24–25 II, konflikt, trening, Pomfrey i Luna; majątek i Lodgok.',6:'Trening Hermiony, sekret Pettigrew i Syriusza, plan rozmowy z Harrym; wieczór 25 II.',7:'26 II, rozmowa z Harrym i Pince; przeskok do 23 VI, przed finałem.',8:'23–24 VI, konflikt z Draco, noc i sny, pakowanie; koniec nad jeziorem przed finałem.',9:'Finał Turnieju, koniec roku, pociąg, zakupy i dom; początek wizyty u Grangerów 8 VII.',10:'8 VII: dalsza wizyta, diament, obiad, Hampstead Heath i powrót; podanie szczotki.',11:'8–9 VII: czesanie, pożegnanie, czuwanie i pierwsza wizyta Hermiony; dom, obiad, zwierzenia.'}
index='# Indeks dużych części — C1–C11\n\nNajpierw znajdź temat w [indeksie scen](INDEKS_SCEN.md), potem czytaj jedną część. Dla węższego odczytu użyj [małych fragmentów](INDEKS_MALYCH_CZESCI.md).\n\n| Part | Plik | Zakres | Liczba | Zawartość |\n|---|---|---|---|---|\n'
index+=table([(f'C{x["part"]}',f'[{Path(x["file"]).name}](../01_ARCHIWA_CZATY/{Path(x["file"]).name})',x['first']+'–'+x['last'],x['messages'],summaries[x['part']]) for x in big]);put('03_INDEKS/INDEKS_CZATY.md',index)
put('03_INDEKS/INDEKS_DUZYCH_CZESCI.md',index)
put('03_INDEKS/PODSUMOWANIA.md','# Podsumowania części\n\nSkróty do wyszukania, nie zamiennik korekt lub źródeł. C11 jest najnowsze.\n\n'+ '\n\n'.join(f'## C{i}\n\n{summaries[i]}' for i in range(1,12)))
put('03_INDEKS/INDEKS_MALYCH_CZESCI.md','# Indeks 60 małych fragmentów\n\nDo 200 pełnych wiadomości. Stare 57 plików bez zmian; nowe fragmenty 58–60. Zakres ID rozstrzyga wybór pliku.\n\n| Plik | Od | Do | Wiadomości |\n|---|---|---|---|\n'+table([(f'[{Path(c["file"]).name}](../01_ARCHIWA_CZATY/mniejsze_czesci/{Path(c["file"]).name})',c['first'],c['last'],c['messages']) for c in small]))
# Add direct large/small links to every scene row, including older abbreviated ranges.
s=(O/'01_ARCHIWUM_SCEN_INDEKS.md').read_text();out=[]
for line in s.splitlines():
 match=re.search(r'\| (C(\d+)-S\d+) \| C\d+-M(\d{4})[–-](?:C\d+-)?M(\d{4}) \|',line)
 if match:
  part,a,b=map(int,match.group(2,3,4));links=[]
  for c in small:
   k=int(c['first'].split('-')[0][1:]);ca=int(c['first'].split('M')[1]);cb=int(c['last'].split('M')[1])
   if k==part and ca<=b and cb>=a:links.append(f'[{Path(c["file"]).name.split("_")[1]}](../01_ARCHIWA_CZATY/mniejsze_czesci/{Path(c["file"]).name})')
  line=line.rstrip()[:-1]+f'| [C{part}](../01_ARCHIWA_CZATY/01_ARCHIWUM_CZAT_{part}.txt) | '+', '.join(links)+' |'
 elif line.startswith('| Blok |'):line+=' Duży Part | Małe fragmenty |'
 elif line=='|---|---|---|':line+='---|---|'
 out.append(line)
put('03_INDEKS/INDEKS_SCEN.md','\n'.join(out).replace('(00_INDEKS_MNIEJSZYCH_CZESCI.md)', '(INDEKS_MALYCH_CZESCI.md)'))
for n in ['00_MAPOWANIE_C5.md','00_MAPOWANIE_C10.md','00_MAPOWANIE_C11.md']:cp(O/n,'03_INDEKS/'+n)
manifest={'version':'C1-C11','current_id':'C11-M0409','messages':10936,'merged_file':'01_ARCHIWA_CZATY/scalone/01_ARCHIWUM_CZAT_1-11_SCALONE.txt','merged_sha256':C['merged_sha256'],'small':[{**c,'file':'01_ARCHIWA_CZATY/mniejsze_czesci/'+Path(c['file']).name} for c in small],'large':[{**c,'file':'01_ARCHIWA_CZATY/'+Path(c['file']).name} for c in big]}
put('03_INDEKS/INDEKS_PLIKOW.json',json.dumps(manifest,ensure_ascii=False,indent=2))
put('REPO_CONFIG.json',json.dumps({'repository_url':None,'default_branch':'main','state':'C11-M0409','note':'Wstaw rzeczywisty adres repozytorium po jego utworzeniu; adres nie był podany. Same pliki nie zapewniają połączenia z czatem.'},ensure_ascii=False,indent=2))
put('AGENTS.md','''# Instrukcje pracy z kampanią

To repozytorium jest bazą ciągłości polskiego RPG. James Brown należy wyłącznie do użytkownika. Nie kontynuuj sceny podczas aktualizacji archiwum.

Przed pierwszą narracją przeczytaj pliki z 02_PLIKI_AKTYWNE: 08_CURRENT.md, 10_ZASADY_I_CIAGLOSC.md, 09_REJESTR_KOREKT.md, 04_KTO_CO_WIE.md. Potem rozwijaj bieżącą rozmowę; nie resetuj do CURRENT.

Do ważnego faktu dobierz dział. Jeżeli skrót jest niejasny, sprawdź 03_INDEKS/INDEKS_SCEN.md oraz właściwy fragment archiwum. Jedno ID znajduje `python scripts/znajdz.py C11-M0409`; zakres przyjmuje dwa ID z tego samego Part. Pełne działy są w 05_BAZA_PELNA. Historyczne punkty końcowe nie są bieżącym stanem.

Późniejsza jawna korekta użytkownika ma pierwszeństwo tylko w swoim zakresie. Oddziel wiedzę NPC, narratora, prywatne myśli, plotki, deklaracje i marzenia. Nie mieszaj odrębnych kampanii. Zachowuj osobowości, wiek i samodzielność NPC. Brak źródła zgłoś zamiast zgadywać.

Przy aktualizacji: zachowaj oryginał, istniejące ID i odrzucone wersje w archiwum; dopisz nowy Part. Uaktualnij pełną bazę, aktywne skróty, oba indeksy, indeks scen, CURRENT, rejestr korekt i lorebook. Następny numer C12. Nie dopisuj odpowiedzi NPC ani ruchu Jamesa poza transkryptem.

Sprawdź `python scripts/sprawdz.py`. Nie usuwaj historii i nie publikuj repozytorium bez zlecenia. Samo istnienie AGENTS.md nie oznacza, że dowolny czat automatycznie go odczyta. Nie obiecuj automatycznej synchronizacji.
''')
put('INSTRUKCJE_PROJEKTU.md','''# Tekst do instrukcji projektu

Przed użyciem zastąp `[ADRES_REPOZYTORIUM]` rzeczywistym adresem swojego repozytorium. Bez tego tekst nie wskazuje miejsca archiwum. Jeżeli korzystasz z repozytorium prywatnego, czat musi mieć uprawniony dostęp; sam adres nie wystarcza.

---

Prowadź RPG po polsku, zachowując kampanię Jamesa Browna. Użytkownik kontroluje wyłącznie Jamesa — jego słowa, myśli, reakcje, decyzje i działania. Narrator prowadzi świat i NPC.

Pełne archiwa znajdują się w `[ADRES_REPOZYTORIUM]`. W źródłach projektu są krótsze pliki aktywne. Przed pierwszą kontynuacją przeczytaj najnowsze 08_CURRENT, 10_ZASADY_I_CIAGLOSC, 09_REJESTR_KOREKT i 04_KTO_CO_WIE. Uwzględniaj również nazwy z dopiskami „(1)”; zakres treści rozstrzyga wersję. Późniejsze wydarzenia bieżącego czatu rozwijają ten stan, nie wracaj do zapisanego CURRENT przy każdej turze.

Ważny fakt sprawdzaj w odpowiednim dziale. Jeśli potrzebujesz źródła, najpierw 03_INDEKS/INDEKS_SCEN.md i odpowiedni zakres, potem pojedynczy mały fragment z 01_ARCHIWA_CZATY/mniejsze_czesci. Duży Part wybieraj przez 03_INDEKS/INDEKS_CZATY.md. Nie pobieraj wszystkich archiwów naraz. Pełne opracowania tematyczne są w 05_BAZA_PELNA.

Późniejsze jawne korekty użytkownika mają pierwszeństwo w swoim zakresie. Błąd narratora lub odrzucona odpowiedź nie stają się kanonem. Rozróżniaj fakty, deklaracje, plotki, plany i wyobrażenia. NPC zna tylko to, co widział, usłyszał lub wiarygodnie poznał; pliki i prywatne myśli Jamesa nie są jego wiedzą.

Zachowuj osobowości, wiek i samodzielność NPC. Hermiona ma własne zdanie, rodzinę, przyjaciół i cele; Draco zachowuje dumę i uprzedzenia. Pilnuj miejsca, czasu, pozycji, przedmiotów, świadków i ostatniej wypowiedzi. Pisz naturalnie, bez raportów technicznych w dialogach.

Lorebook jest dodatkiem świata, nie nadpisuje kampanii i nie narzuca przyszłych wydarzeń. Domyślny książkowy przebieg z C10-M0367 zachowuje rozegrane różnice AU. Nie łącz odrębnych kampanii na podstawie imion.

Jeżeli potrzebnego pliku nie da się odczytać, powiedz to krótko i nie udawaj weryfikacji. Nie wymyślaj brakującej historii. Pliki aktualizuj na zlecenie, zachowując źródła i kończąc CURRENT na ostatniej zapisanej akcji, bez dopisanej kontynuacji. Nie deklaruj samoczynnej synchronizacji.
''')
put('README.md','''# RPG-Archiwum — C1–C11

Gotowy zestaw plików do repozytorium: **10 936 wiadomości, 11 dużych części, 60 małych fragmentów**. Stan: **C11-M0409, 9 lipca 1995 po obiedzie i deserze**, następna odpowiedź Hermiony. Repozytorium nie zostało utworzone ani opublikowane przez przygotowanie tej paczki.

## Gdzie zacząć

- [CURRENT](02_PLIKI_AKTYWNE/08_CURRENT.md) — dokładny punkt kontynuacji.
- [Indeks dużych części](03_INDEKS/INDEKS_CZATY.md) — jeden plik na Part.
- [Indeks małych fragmentów](03_INDEKS/INDEKS_MALYCH_CZESCI.md) — zakresy do 200 wiadomości.
- [Indeks scen](03_INDEKS/INDEKS_SCEN.md) — tematy i odsyłacze do obu rozmiarów plików.
- [Podsumowania](03_INDEKS/PODSUMOWANIA.md) — krótki opis wszystkich części.

## Struktura

| Folder / plik | Zastosowanie |
|---|---|
| 01_ARCHIWA_CZATY | C1–C11 osobno, małe fragmenty w mniejsze_czesci/, całość w scalone/ |
| 02_PLIKI_AKTYWNE | Krótszy bieżący zestaw do źródeł projektu, obejmuje także MAPA i LOREBOOK |
| 03_INDEKS | Wybór Part, fragmentu i sceny; mapowanie C5, C10, C11; manifest JSON |
| 04_ORYGINALY | Niezmienione eksporty C10 i C11 |
| 05_BAZA_PELNA | Zaktualizowane pełne działy, rejestr korekt, lorebook Markdown/JSON i kontrola archiwum |
| 06_HISTORIA_BAZY | Poprzednia baza do C10, wyłącznie historyczna |
| scripts | Odszukanie ID i kontrola integralności bez zewnętrznych bibliotek |
| AGENTS.md | Instrukcje dla agenta pracującego w repozytorium |
| INSTRUKCJE_PROJEKTU.md | Tekst do instrukcji projektu po uzupełnieniu rzeczywistego adresu |
| REPO_CONFIG.json | Miejsce na rzeczywisty adres repozytorium; teraz null |

## Użycie

Rozpakuj paczkę i umieść **zawartość tego folderu** w katalogu głównym swojego repozytorium, zachowując nazwy i podfoldery. Nie trzeba uruchamiać skryptów, żeby używać plików. Po utworzeniu repozytorium wpisz jego adres w REPO_CONFIG.json oraz INSTRUKCJE_PROJEKTU.md.

Do źródeł projektu przeznaczony jest folder 02_PLIKI_AKTYWNE; nie trzeba dodawać wszystkich archiwów i pełnego lorebooka. Instrukcje mają wskazywać repozytorium i indeks. Nie zostawiaj równolegle starych CURRENT jako równorzędnych punktów startu. Samo zapisanie plików tutaj nie podmienia źródeł projektu i nie daje każdemu czatowi dostępu do prywatnego repozytorium.

Ustal dostęp odpowiednio do tego, komu chcesz udostępnić pełne rozmowy. Paczka nie zmienia widoczności ani nie nadaje licencji cudzym elementom świata; dlatego nie dołączono domyślnej LICENSE.

## Wyszukiwanie i sprawdzanie

```bash
python scripts/znajdz.py C11-M0409
python scripts/znajdz.py C11-M0153 C11-M0158
python scripts/sprawdz.py
```

Indeks prowadzi do konkretnego fragmentu. Nie jest potrzebny serwer, API, klucz ani automatyzacja. Żaden skrypt nie wysyła danych ani nie aktualizuje repozytorium samoczynnie.

## Kontrola wykonana

C1–C10 odtworzono z 57 fragmentów i porównano SHA-256 z poprzednim manifestem: zgodność bajt w bajt. Zachowano te 57 fragmentów; dodano 58–60. Połączenie 11 dużych części lub 60 małych odtwarza scalone C1–C11. Identyfikatory są unikalne i ciągłe w każdym Part. Oryginał C11 jest niezmieniony. Format TURN zamieniono na 409 wiadomości, zachowując końcowy USER bez odpowiedzi.

Pełna analiza dotyczy C11 i porównania z wcześniejszą bazą; nie wykonano ponownej interpretacji wszystkich dawnych scen. Odrzucone odpowiedzi zachowano i oznaczono. Dokładna godzina końca, relacja obu londyńskich adresów i cena powrotnej taksówki pozostają nieustalone.
''')
put('.gitattributes','* -text\n*.py text eol=lf\n.gitattributes text eol=lf\n.gitignore text eol=lf')
put('.gitignore','__pycache__/\n*.pyc\n.DS_Store\nThumbs.db')
put('scripts/znajdz.py','''#!/usr/bin/env python3
"""Odczyt konkretnej wiadomości lub zakresu; bez sieci i zależności."""
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
def parse(s):
 m=re.fullmatch(r'C(\\d+)-M(\\d{4})',s)
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
  s=(ROOT/c['file']).read_text();matches=list(re.finditer(r'^\\[(C\\d+-M\\d{4})\\]\\s*\\n===== (USER|ASSISTANT) =====\\s*\\n',s,re.M))
  for i,m in enumerate(matches):
   k=parse(m[1])
   if a[1]<=k[1]<=b[1]:
    body=s[m.end():matches[i+1].start() if i+1<len(matches) else len(s)]
    body=re.split(r'(?m)^(?:===== )?ARCHIWUM CZATU \\d+ ',body)[0].rstrip()
    found.append((k[1],f'[{m[1]}] {m[2]}\\n{body}'))
 if len(found)!=b[1]-a[1]+1:raise ValueError('Nie znaleziono pełnego zakresu; sprawdź indeks.')
 print('\\n\\n'.join(v for _,v in sorted(found)))
if __name__=='__main__':
 try:main()
 except ValueError as e:sys.exit(str(e))
''')
put('scripts/sprawdz.py','''#!/usr/bin/env python3
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
  ids=re.findall(rb'^\\[(C\\d+-M\\d{4})\\]\\r?$',b,re.M)
  assert len(ids)==c['messages'] and ids[0].decode()==c['first'] and ids[-1].decode()==c['last'],c['file']
  if typ=='small':assert len(ids)<=200
 assert b''.join(buffers)==merged,typ
ids=[x.decode() for x in re.findall(rb'^\\[(C\\d+-M\\d{4})\\]\\r?$',merged,re.M)]
assert len(ids)==len(set(ids))==m['messages']
for part in range(1,12):
 sub=[x for x in ids if x.startswith(f'C{part}-')]
 assert sub==[f'C{part}-M{i:04d}' for i in range(1,len(sub)+1)]
assert ids[-1]==m['current_id']
for p in R.rglob('*.md'):
 if '06_HISTORIA_BAZY' in p.parts:continue
 for target in re.findall(r'\\[[^\\]]*\\]\\(([^)]+)\\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  assert (p.parent/target.split('#')[0]).exists(),f'{p}: {target}'
print(f"OK: {len(ids)} wiadomości, {len(m['large'])} dużych i {len(m['small'])} małych plików; SHA, podział, ID i linki zgodne.")
''')
# Script sources for reproducibility of the prepared artifact, not an automatic importer.
for n in ['build_c11.py','parse_c11.py','prepare_github_c11.py']:
 cp(R/n,'06_HISTORIA_BAZY/narzedzia_przygotowania/'+n)
print('Repo przygotowane',G)
