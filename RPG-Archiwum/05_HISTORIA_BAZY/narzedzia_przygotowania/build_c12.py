from pathlib import Path
import json,re,hashlib,shutil,zipfile
R=Path('/workspace/scratch/d9fac05cbafd'); G=R/'repo_c12/RPG-Archiwum'; B=G/'04_BAZA_PELNA'; O=R/'RPG_Baza_Wiedzy_12_czesci'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,s):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.strip()+'\n')
def js(p,v):put(p,json.dumps(v,ensure_ascii=False,indent=2))
old=json.loads((G/'03_INDEKS/INDEKS_PLIKOW.json').read_text()); base=(G/old['merged_file']).read_bytes();assert sha(base)==old['merged_sha256']
# Preserve the complete previous knowledge version before changing any current file.
hist=G/'05_HISTORIA_BAZY/do_C11'
if not hist.exists():shutil.copytree(B,hist)
activeold={p.name:p.read_text() for p in (G/'02_PLIKI_AKTYWNE').glob('*.md')}
fullold={p.name:p.read_text() for p in B.glob('*.md')}
M=json.loads((R/'c12_messages.json').read_text());mp=json.loads((R/'c12_mapping.json').read_text());assert len(M)==1109 and len(mp)==555
header='\n\nARCHIWUM CZATU 12 — treść rozmowy w dotychczasowym formacie\n\n555 bloków TURN; 1109 wiadomości. TURN 471 zawiera wyłącznie USER, po nim TURN 472 zapisuje zmienioną wersję tego ruchu. Oryginalny eksport zachowano. Odrzucone warianty, cytaty, dopiski interfejsu i komentarze OOC nie są automatycznie kanonem; zobacz 09_REJESTR_KOREKT.md.\n\n'
a12=(header+''.join(f"[{m['id']}]\n===== {m['role']} =====\n\n{m['text']}\n\n\n" for m in M)).encode(); merged=base+a12
large=old['large'].copy();small=old['small'].copy()
def meta(file,b,first,last,num,**kw):return dict(file=file,first=first,last=last,messages=num,bytes=len(b),sha256=sha(b),**kw)
rel='01_ARCHIWA_CZATY/01_ARCHIWUM_CZAT_12.txt';(G/rel).write_bytes(a12);large.append(meta(rel,a12,M[0]['id'],M[-1]['id'],len(M),part=12))
marks=list(re.finditer(rb'^\[C12-M\d{4}\]$',a12,re.M))
for start in range(0,len(M),200):
 end=min(start+200,len(M));b=a12[0 if start==0 else marks[start].start():marks[end].start() if end<len(M) else len(a12)]
 rel=f"01_ARCHIWA_CZATY/mniejsze_czesci/ARCHIWUM_{len(small)+1:03d}_{M[start]['id']}_{M[end-1]['id']}.txt";(G/rel).write_bytes(b);small.append(meta(rel,b,M[start]['id'],M[end-1]['id'],end-start))
mergedrel='01_ARCHIWA_CZATY/scalone/01_ARCHIWUM_CZAT_1-12_SCALONE.txt';(G/mergedrel).write_bytes(merged)
(G/'04_ORYGINALY').mkdir(exist_ok=True);shutil.copyfile(R/'c12_input/ChatGPT_CALY_CZAT12.txt',G/'04_ORYGINALY/ChatGPT_CALY_CZAT12.txt')
state='Stan C12-M1109: początek września 1995, po lekcjach w dniu porannego zgłoszenia krwawego pióra; Pokój Życzeń, VII piętro Hogwartu. Dokładna data i godzina nieustalone. Następny ruch należy do użytkownika (Jamesa).'
U={}
U['02_TIMELINE.md']='''# Timeline — aktualizacja C12

| Czas | Zdarzenie i status | Źródło |
|---|---|---|
| 9 VII, po C11 | Hermiona odpowiada na końcowe wyznanie; wspólny odpoczynek, rzeczywisty sen Jamesa i Hermiony, pobudka przy biciu zegara o 16:00 | C12-M0004–C12-M0042 |
| 9 VII | James opowiada Hermionie o śnie o dorosłym życiu i ślubie z Luną; to sen, nie rzeczywiste małżeństwo. Rozmowa o ślubie z Hermioną po szkole pozostaje warunkowa | C12-M0043–C12-M0066 |
| Po 16:00 | Biblioteka domu Jamesa, lektura run i kolejny rzeczywisty sen na kolanach Hermiony | C12-M0067–C12-M0088 |
| 18:45 | Tobik przypomina o powrocie; James budzi się, podnosi głos, po czym łagodnie dziękuje. Hermiona broni właściwego traktowania skrzata | C12-M0089–C12-M0108 |
| Wieczór | Zakończenie lektury; wyjazd razem taksówką na 8 Heathgate. Hermiona zasypia w drodze. Przyjazd o 19:55, wniesienie do pokoju za zgodą rodziców, pożegnanie | C12-M0109–C12-M0174 |
| 9/10 VII | Powrót do Belgravii; należność £18,60, wręczone £100 bez zapisu reszty. James odmawia pomocy Tobika, myje się i czuwa | C12-M0175–C12-M0194 |
| Lipiec–sierpień | Autoryzowany skok czasu: Hermiona trafia do tajnej kwatery; miejsce nieznane Jamesowi. Tło: atak dementorów 2 VIII, przybycie Harry’ego 6 VIII i rozprawa 12 VIII. Nie są to zdarzenia obserwowane przez Jamesa | C12-M0195–C12-M0206 |
| Wakacje | Niemal codzienne listy Jamesa do Hermiony; korespondencja z Luną, Élodie i Krumem. Czarna koperta spalona bez otwierania. Nie rozegrano kolejnych wizyt ani podróży do zamku | C12-M0197–C12-M0206 |
| 31 VIII | Hermiona pisze o odznakach swojej i Rona, nie o wspólnym miejscu zamieszkania | C12-M0206 |
| 1 IX | James od 7:00 na peronie; grupa przybywa później. Wita Hermionę i prawdziwego Moody’ego, rozpoznaje Syriusza w postaci psa | C12-M0207–C12-M0218 |
| Pociąg | Kłótnia o wakacyjną rozłąkę i Rona. James uderza głową w szybę, następnie ją naprawia; Harry widzi skutek. Nott informuje o prefekturze Draco i Pansy. Rozmowa z Luną, Ginny, Neville’em | C12-M0219–C12-M0260 |
| Podróż | Hermiona ujawnia obecność Weasleyów i późniejsze przybycie Harry’ego, bez adresu. Częściowe uspokojenie; obchody prefektów, słodycze, sen Jamesa przy niej i czuwanie podczas jej nieobecności | C12-M0261–C12-M0342 |
| Hogsmeade | Wspólny powóz z Harrym, Ronem i Ginny. James potwierdza, że widzi czarne skrzydlate stworzenia; przyczyna nie zostaje im wyjaśniona | C12-M0343–C12-M0378 |
| Uczta 1 IX | Osobne stoły, spór z Draco, przedstawienie Umbridge; James idzie do dyrektora | C12-M0379–C12-M0444 |
| Po uczcie | Rozmowa z Dumbledore’em o prefekturze. James nie dostaje odznaki; dyrektor odróżnia dyscyplinę od osobistej zemsty. McGonagall odchodzi przed rozmową | C12-M0445–C12-M0478 |
| Noc i poranek | Nott, potem Draco i Pansy w pokoju wspólnym; groźby i spór, bez nowej bójki. James deklaruje noc bez snu i bez czuwania, ćwiczy od 4:00 | C12-M0479–C12-M0542 |
| Pierwszy rozegrany dzień lekcji (D) | Spotkanie i pojednanie z Hermioną pod biblioteką, Pince otwiera o 6:00; śniadanie przy Gryffindorze, odwołany żart o ślubie za W, plany lekcji i ustalenie fakultetów | C12-M0543–C12-M0674 |
| D | Sen na Historii Magii; Wywar Spokoju z jednym płatkiem lilii, zaakceptowany przez Snape’a jako kontrolowana modyfikacja; próbka oddana. Przerwa i obiad | C12-M0675–C12-M0768 |
| D, Runy | Przekład tekstu i zakład o wyniki z dziewięciu wspólnych SUM-ów; stawki uzgodnione, wynik jeszcze nieznany | C12-M0769–C12-M0812 |
| D, Obrona | Umbridge odrzuca powrót Voldemorta. Harry dostaje szlaban na ten wieczór; James, po publicznym sporze i skorygowaniu zakresu swego świadectwa, na następny dzień o 17:00 | C12-M0813–C12-M0850 |
| D+1, 17:00 | James pisze jedną literę krwawym piórem i odmawia dalszej kary. Umbridge zapowiada zgłoszenie Snape’owi i dyrektorowi; puszcza go | C12-M0851–C12-M0868 |
| D+1 | Hermiona widzi nacięcie i podejrzewa Umbridge, ale nie dostaje wyjaśnienia. Prywatna rozmowa Jamesa z Harrym o piórze i zgodzie na zgłoszenie. Pożegnanie z Hermioną | C12-M0869–C12-M0921 |
| Odrzucony wariant | M0922–M0949 anulowane w M0952–M0953, łącznie z nocą, porankiem i ujawnieniami Draco. Nie są drugim przebiegiem tych dni | C12-M0950–C12-M0953 |
| D+1 / D+2 | Poprawiona rozmowa z Draco o piórze, noc czuwania, ćwiczenia od 4:00 i kawa; tym razem rano Nott, nie Draco | C12-M0953–C12-M0976 |
| D+2, około 5:00 | Zgłoszenie Snape’owi, sprowadzenie Harry’ego, oględziny obu dłoni, przybycie Dumbledore’a, polecenie dokumentacji i dyskrecji. Brak zwolnienia Umbridge | C12-M0977–C12-M1023 |
| D+2, przed śniadaniem | Oczekiwanie na Hermionę; odmowa wejścia do pokoi wspólnych, przejście do Pokoju Życzeń, wspólny odpoczynek. Wyjście na śniadanie | C12-M1024–C12-M1084 |
| D+2, po lekcjach | Ponowny Pokój Życzeń według pomysłu Hermiony; wyobrażenia wspólnego domu, nie przepowiednia. Rozmowa i odpoczynek; James ujawnia jej prywatny sekret łaskotek. Koniec po odpowiedzi Hermiony | C12-M1085–C12-M1109 |

## Rozbieżność dat

Po uczcie 1 IX następny poranek prowadzi bez jawnego przeskoku do lekcji w kolejności poniedziałkowej (M0662, M0674–M0850). Nie dopisujemy brakującego weekendu ani nie uznajemy arbitralnie końca za 4 lub 6 IX. Pewne jest następstwo D → szlaban D+1 → zgłoszenie i końcowa scena D+2. M0851 pomija zwykłą resztę D i część D+1; M1084 pomija lekcje D+2. Cofnięcie sceny Draco nie dodaje dnia.
'''
U['03_PROFILE_POSTACI.md']='''# Profile postaci — aktualizacja C12

James i Hermiona rozpoczęli V rok; w zapisie nadal mają po 15 lat. Nie dodano daty urodzin Jamesa ani nowego pomiaru wzrostu Hermiony (jej „możliwe” w M0564 nie jest pomiarem).

- **James:** nie został prefektem po rozmowie z Dumbledore’em (M0445–M0478). Regularnie ćwiczy, ma rzeczywiste epizody snu przy Hermionie (M0013, M0029, M0083, M0331, M0341, M0681), lecz samotne noce nadal są czuwaniem albo jawnym brakiem obu stanów. To nie diagnoza ani trwałe wyleczenie. Jednoliterowy ślad po piórze pokazany nauczycielom; brak potwierdzonego leczenia.
- **Fakultety Jamesa:** Starożytne Runy i Opieka nad Magicznymi Stworzeniami. Numerologia i Mugoloznawstwo zaliczone wewnętrznie przy transferze do IV klasy, w zakresie do końca III; nie państwowe SUM-y. Nie chodzi obecnie na te dwa przedmioty. Uzgodnienie AU, nie potwierdzona procedura z książek (M0659–M0662).
- **Hermiona:** prefekt Gryffindoru razem z Ronem, wykonuje obchody. Nadal ma Runy, Opiekę i Numerologię. Ma własne ambicje i przyjaciół; odrzuca utożsamienie wspólnego pobytu z romansem (M0220–M0224, M0288, M0556). Jej spontaniczna, zaczepna strona nie stanowi osobnej osobowości (M1081–M1083, M1091).
- **Draco:** prefekt Slytherinu, Pansy prefektką. Respekt wobec Jamesa nie znosi dumy, uprzedzeń, złośliwości i przychylności dla ministerialnej ingerencji. Zastrzeżenie wobec pióra nie robi z niego przeciwnika całej polityki Umbridge. Obowiązuje poprawiona scena M0953–M0969; serdeczniejszy wariant M0922–M0949 anulowany.
- **Harry:** nie jest prefektem; przeżył pierwszy szlaban z piórem i zgodził się pokazać ślady nauczycielom. Współpracuje z Jamesem, zachowuje upór i niechęć do Snape’a (M0882–M0890, M0999–M1023).
- **Ron:** prefekt, przyjaciel Hermiony; brak dowodu romansu. Napięcie z Jamesem pozostaje. Nie sprowadzać go do samej zazdrości (M0956–M0957).
- **Tobik:** nazwany skrzat domu Jamesa; przypomniał o godzinie, widział sen w bibliotece i powrót Jamesa do holu. Nie utożsamiać go automatycznie ze wszystkimi nienazwanymi skrzatami wcześniejszych scen (M0090–M0096, M0188–M0192).
- **Snape i Dumbledore:** obejrzeli ślady, reagują dokumentacją i dyskretnym działaniem. Snape pozostaje chłodny i stronniczy; dyrektor nie odwołał Umbridge (M0983–M1021).
- **Umbridge:** nauczycielka Obrony narzucona przez Ministerstwo; na obecnym etapie nie nadawać jej późniejszych uprawnień Wielkiego Inkwizytora ani pełnej władzy nad karami (M0864).
'''
U['04_KTO_CO_WIE.md']='''# Kto co wie — aktualizacja C12

| Fakt | Kto i skąd wie | Czego nie wolno dopowiadać | Źródło |
|---|---|---|---|
| Sen o dorosłym małżeństwie z Luną | James śnił; Hermiona poznała jego skróconą relację | Luna nie wie; nie jest to fakt rzeczywistego ślubu ani import osobnej kampanii | C12-M0031–C12-M0066 |
| Rzeczywisty sen w domu | Hermiona obserwuje oba epizody; Tobik widzi Jamesa w bibliotece | Nie daje to Hermionie wiedzy o każdej samotnej nocy | C12-M0013–C12-M0094 |
| Wakacyjne zwierzenia i zaproszenia | Luna, Élodie, Krum znają tylko własną korespondencję. Ginny i Neville słyszą w pociągu, że Luna dostawała listy, bez ich treści | Hermiona nie została poinformowana o tych listach; zaproszenia użytkownik skierował do Luny i Élodie, nie jawnie do Kruma | C12-M0197–C12-M0206, C12-M0240 |
| Kwatera Zakonu | Hermiona i osoby tam obecne znają ją w swoim zakresie | James nadal nie zna adresu Grimmauld Place ani szczegółów Zakonu; narracyjne tło nie jest jego wiedzą | C12-M0196–C12-M0224 |
| Ron i inni podczas rozłąki | James dowiaduje się w pociągu o wspólnym pobycie, następnie o Ginny, bliźniakach i rodzicach Weasleyów; Harry dołączył później | List o odznakach nie informował o wspólnym pobycie; nie było pobytu sam na sam | C12-M0206, C12-M0222, C12-M0256, C12-M0296 |
| Uderzenie głową o szybę | James zna czyn; Harry słyszy/ogląda skutek i obiecuje milczeć; Hermiona widzi ślad na czole | Hermiona nie dostaje przyczyny; Harry nie widział samego uderzenia | C12-M0225–C12-M0230, C12-M0262–C12-M0264 |
| Plan rozmowy o prefekturze | Nott słyszy plan w pociągu, Hermiona też. Dumbledore zna własną rozmowę. McGonagall widzi przybycie, potem odchodzi | Draco nie zna planu z wiedzy narratora; M0390 zastąpione M0394. Nott nie zna pełnego przebiegu gabinetu | C12-M0233–C12-M0236, C12-M0270, C12-M0391–C12-M0394, C12-M0444–C12-M0478 |
| Czarne skrzydlate stworzenia | James i Harry widzą, Ron, Ginny, Hermiona słyszą ich relacje | Nie przedstawiono im tutaj przyczyny widzenia ani nie potwierdzono, że znają nazwę testrali | C12-M0356–C12-M0364 |
| Świadectwo Jamesa o Crouchu | Uczestnicy lekcji słyszą twierdzenia Jamesa oraz wycofanie twierdzenia o osobistym słuchaniu Veritaserum | Publiczna wypowiedź nie przekazuje automatycznie całego podsłuchu z C9. James odszedł przed przesłuchaniem | C12-M0831–C12-M0847; C9-M0064–C9-M0086 |
| Pióro: Hermiona | Widzi świeży ślad po wyjściu Jamesa, wie o odmowie i zapowiedzi eskalacji; wiąże ślad z Umbridge | Nie usłyszała mechanizmu pióra, prywatnej rozmowy z Harrym ani spotkania u Snape’a. Harry tylko przewiduje, że się dowie | C12-M0869–C12-M0892 |
| Pióro: Harry | Własne doświadczenie; rozmowa z Jamesem, później wspólne oględziny | Nie ma automatycznej wiedzy o rozmowie Jamesa z Draco | C12-M0882–C12-M0890, C12-M1007–C12-M1023 |
| Pióro: Draco | Wie z poprawionej rozmowy o odmowie, nacinaniu skóry i zapowiedzianym zgłoszeniu | M0922–M0949 anulowane. Nie zna ujawnienia o zasypianiu tylko przy Hermionie ani późniejszej interwencji nauczycieli | C12-M0953–C12-M0969 |
| Pióro: Snape i Dumbledore | Zgłoszenie, oględziny rąk obu uczniów i ich relacje; Snape otrzymuje polecenie notatki | Nie zakładać, że Umbridge już przekazała swoją zapowiedzianą skargę. McGonagall nie uczestniczy | C12-M0979–C12-M1021 |
| Portret | Gruba Dama jest obecna przy rozmowach na korytarzu, słyszy też wzmiankę o Snape’ie i piórze | Nie przenika ścian ani nie zna rozmów gabinetowych; potencjalny podsłuch nie jest wszechwiedzą | C12-M0874–C12-M0918, C12-M1001, C12-M1029–C12-M1049 |
| Nowy prywatny sekret | Hermiona dowiaduje się o łaskotkach Jamesa w dolnej części szyi; on określa ją jako jedyną osobę znającą sekret, ona obiecuje dyskrecję | Nikt poza obojgiem nie był w Pokoju. Deklaracja wyłączności pochodzi od Jamesa | C12-M1098–C12-M1109 |

Szeptane ustalenia nie stają się wiedzą całego stołu czy klasy. Odrzucona gałąź jest wyłączona także z pamięci NPC.
'''
U['05_RELACJE.md']='''# Relacje — aktualizacja C12

**James–Hermiona:** związek trwa. Wakacyjna rozłąka prowadzi do kłótni 1 IX, zazdrości o Rona i częściowego uspokojenia w pociągu. Poranek pod biblioteką przynosi ponowne zapewnienie o przyjaźni z Ronem i bliskość; nie należy utrzymywać nieprzerwanej ostrej kłótni jako CURRENT (M0219–M0290, M0543–M0584). Zamek i wspólne podróże nie odbyły się tylko dlatego, że wcześniej je planowano.

Ślub po szkole pozostaje warunkową teorią (M0061–M0064). Żart „W oznacza ślub” zostaje odrzucony przez Hermionę i odwołany publicznie przez Jamesa (M0633–M0644). Zwrot „Granger-Brown” w M1102 również nie zmienia nazwiska i nie ustanawia zaręczyn (M1103).

Granice Hermiony zależą od sytuacji; zgoda w jednej scenie nie jest blankietową zgodą na wszystkie przyszłe. Zachowuje naukę, przyjaciół, prawo odmowy i samodzielne decyzje. „Szalona Hermiona” to jej bardziej spontaniczna, inicjatywna i figlarna strona, nie inna osoba (M0956–M0957, M1081–M1083, M1091).

**Zakład o SUM-y:** dziewięć wspólnych przedmiotów, porównanie ocen parami, wygrywa więcej lepszych wyników, przy remisie dogrywka jeszcze do ustalenia. Jeśli Hermiona przegra, sama wybiera sukienkę, zaprasza na randkę i odgrywa umówioną przesadną fascynację; jeśli James przegra, publicznie przy śniadaniu przyznaje jej przewagę, elegancko zaprasza na randkę i spełnia uzgodnione gesty grzecznościowe. Randka po wynikach, nie dowolnie po ślubie. To dobrowolna gra, bez rzeczywistej utraty autonomii (M0783–M0798). Pierwszy pomysł cotygodniowych pytań i noszenia książek zastąpiono zakładem o SUM-y.

**James–Harry:** po szorstkim epizodzie w pociągu podejmują współpracę w sprawie pióra; Harry przyjmuje przeprosiny i pokazuje nauczycielom rękę. Nie czyni to ich automatycznie najbliższymi przyjaciółmi (M0226–M0228, M0884–M0890, M0999–M1023).

**James–Ron/Ginny/Luna:** brak nowego pojednania z Ronem i brak dowodu romansu Rona z Hermioną. Ginny odrzuca zbiorowe obwinianie Weasleyów; późniejsza pomoc przy wysiadaniu i wspólne śniadanie nie są osobnym formalnym rozejmem. Luna pozostaje przyjaciółką i korespondentką; sen nie zmienia relacji. Élodie jest korespondentką, bez rozegranej wakacyjnej wizyty (M0197–M0206, M0239–M0260, M0375–M0376).

**James–Draco:** rywalizacja i respekt, groźby podczas sporów nie są wykonaną bójką. James nie uzyskuje władzy nad Draco ani odznaki. Rozmowa o piórze nie oznacza serdecznej przyjaźni lub zmiany poglądów Malfoya (M0381–M0534, M0950–M0969).

**Grangerowie:** odnotowują punktualny i bezpieczny powrót córki 9 VII, zgadzają się na wniesienie jej do pokoju; nadal wymagają informacji, gdzie idzie i kiedy wróci (M0152–M0172). Nie ma zgody na nocowanie u Jamesa.
'''
U['06_PRZEDMIOTY_I_SEKRETY.md']='''# Przedmioty, miejsca i sekrety — aktualizacja C12

| Element | Stan | Źródło |
|---|---|---|
| Czarna koperta | Spalona nieotwarta; nadawca, treść i cel nieznane. Nie przypisywać jej Voldemortowi, Ministerstwu ani rodzinie | C12-M0203–C12-M0204 |
| Książka run z domu | Hermiona kończy rozdział i odkłada na kanapę; brak wywiezienia lub zwrotu na półkę w zapisie | C12-M0078–C12-M0110 |
| Płaszcz Jamesa | 9 VII zdjęty z Hermiony w jej pokoju, dalsze zabranie nieopisane; 1 IX użytkownik znów jawnie zakłada płaszcz, na stacji daje Hermionie, ona oddaje przed ucztą. To później potwierdzony stan, bez dopisywania odzyskania | C12-M0163, C12-M0207, C12-M0345–C12-M0380 |
| Gotówka | Taksówkarz żąda £18,60 za kurs z postojem i powrotem; James wręcza £100. Nie pokazano wydania reszty. Kolejny kurs na dworzec opłacony bez kwoty; nie wyliczać nowego dokładnego salda | C12-M0186–C12-M0187, C12-M0207 |
| Sakiewka / słodycze | Hermiona kupuje słodycze, oddaje sakiewkę; kwota niepodana | C12-M0319–C12-M0320 |
| Mundurek i krawat | James: czarna szata z zieloną podszewką i herbem Slytherinu, szara kamizelka, biała koszula, czarne spodnie, bordowo-złoty krawat. Kolejne poranki powtarzają ten zestaw. Nie zmieniać koloru krawata na ślizgoński | C12-M0207, C12-M0535, C12-M0970 |
| Pióro Umbridge | Pozostaje u niej; użycie zostawia Jamesowi ślad po pierwszej literze, Harry’emu rozleglejsze ślady. Nie jest zabrane jako dowód. Ślady i relacje oglądają nauczyciele; brak opisanego leczenia | C12-M0852–C12-M0866, C12-M0983–C12-M1021 |
| Dokumentacja | Snape pisze wiadomość i otrzymuje polecenie dokładnej notatki o czasie, śladach i relacjach; Dumbledore poleca ją zachować i później ponowić oględziny | C12-M1009–C12-M1021 |
| Wywar Spokoju | Jeden płatek lilii wodnej dodany przez Jamesa, Snape akceptuje modyfikację właściwości drugorzędnych; próbka oddana. To ustalenie fikcyjnej kampanii, nie ogólna receptura książkowa | C12-M0692–C12-M0727 |
| Pokój Życzeń rano | Salon z kominkiem, regałami, wspólnym biurkiem, sofą, stolikiem i fotelami. Późniejsze słowo „łóżko” w M1058 nie ma opisanego przeobrażenia sofy | C12-M1051–C12-M1059 |
| Pokój Życzeń po lekcjach | Duży salon, sofa, książki, rośliny, świece, poczęstunek, łóżko z baldachimem, ogród zimowy z dwiema huśtawkami; tablica ruchomych obrazów wyobrażonej przyszłości. Nie wyrocznia ani autentyczne przyszłe zdjęcia | C12-M1085 |
| Koniec sceny | Buty obojga zdjęte przy łóżku; baldachim zamknięty różdżką przez Jamesa, pełna ciemność. Torba Hermiony ostatnio odłożona pod ścianą przed przywołaniem pokoju; brak opisu przeniesienia jej do środka. Różdżka po użyciu nie ma wskazanego miejsca | C12-M1085–C12-M1094 |

Naszyjniki, zwierciadła, majątek, rodzinne sekrety i rozbieżność londyńskich adresów zachowują wcześniejsze ustalenia, jeśli C12 jawnie ich nie zmienia. Nie zakładać, że wszystkie stare rekwizyty są w aktualnym pokoju.
'''
U['07_OTWARTE_WATKI.md']='''# Otwarte wątki — po C12

| Wątek | Bieżący stan | Źródło |
|---|---|---|
| Kontynuacja | Po C12-M1109; następny ruch Jamesa, bez dopisywania go w plikach | C12-M1109 |
| Pióro i Umbridge | Zgłoszenie wykonane, ślady obejrzane, dyskretne działania i dalsze oględziny zapowiedziane. Brak wyniku rozmów z Umbridge, zwolnienia, nowej kary lub formalnego umorzenia odmowy Jamesa | C12-M0979–C12-M1021 |
| Wiedza Hermiony | Podejrzewa związek rany z Umbridge; nie pokazano pełnego wyjaśnienia ani relacji z porannego gabinetu | C12-M0874–C12-M0890, C12-M1024–C12-M1109 |
| SUM-y i zakład | Trwa V rok, wyników brak; dogrywka nieustalona, randka po wynikach. Wewnętrzne egzaminy Jamesa nie zastępują SUM-ów | C12-M0659–C12-M0674, C12-M0783–C12-M0798 |
| Sen | Kolejne epizody przy Hermionie, nadal nocne czuwanie i brak potwierdzonego wyleczenia; nie przeprowadzono nowego badania | C12-M0013–C12-M0033, C12-M0083, C12-M0341, C12-M0681, C12-M0970 |
| Draco | Nie został pozbawiony odznaki; rozmowa z dyrektorem nie dała Jamesowi stanowiska. Konflikt nadal istnieje, nowa bójka nie nastąpiła | C12-M0445–C12-M0534, C12-M0953–C12-M0969 |
| Wakacyjne plany | Wizyty w zamku i innych posiadłościach oraz spotkania z Luną/Élodie niepotwierdzone. Nie realizować ich wstecz przez sam upływ wakacji | C12-M0196–C12-M0206, C12-M0275–C12-M0278 |
| Nieznana koperta | Spalona, brak wiedzy o nadawcy/treści; nie ma obowiązku tworzenia z niej spisku | C12-M0203–C12-M0204 |
| Chronologia | Dokładny dzień września nierozstrzygnięty; zachować D/D+1/D+2 | 02_TIMELINE, 09_REJESTR_KOREKT |

## Zamknięte lub zmienione statusy z C11

Hermiona odpowiedziała na końcowe wyznanie; wizyta 9 VII zakończona, powrót do rodziców o 19:55 wykonany. Wakacje skończone, bohaterowie w Hogwarcie. Obecnie nie czekają na obiad w domu ani na odpowiedź na C11-M0409. Zapowiedź pójścia do Dumbledore’a i zgłoszenia pióra wykonana. Powrót do Pokoju Życzeń po lekcjach również wykonany. Małżeństwo pozostaje wyobrażeniem.

## Trwałe wcześniejsze sprawy bez nowego rozstrzygnięcia

Rita i zapowiadane wypuszczenie; świstoklik i dawne sprawy organizacyjne bez wykonanego finału; fundusz Toma; niepodarowany drugi naszyjnik i niepokazane stare zwierciadło; rozbieżność Eaton Square / Belgrave Square; pełna historia tragedii i rodzinne tajemnice. Szczegóły i starsze identyfikatory w historycznej bazie. Nie ogłaszać ich wykonania przez skok czasu.
'''
U['09_REJESTR_KOREKT.md']='''# Rejestr korekt — aktualizacja C12

| Zakres | Obowiązujące rozstrzygnięcie | Źródło |
|---|---|---|
| Styl | Czysta narracja i dialog w scenie; konieczne wyjaśnienie dopiero w osobnej krótkiej notce na końcu | C12-M0101–C12-M0104 |
| Wiek | Poprawiona reakcja Ginny M0254 zastępuje M0252; postacie mają zachowywać się odpowiednio do wieku | C12-M0253–C12-M0254 |
| Listy a Ron | Wspólnego pobytu z Ronem nie ujawniono w korespondencji. List o jego odznace nie jest takim ujawnieniem | C12-M0206, C12-M0255–C12-M0256 |
| Pamięć postaci | M0306 zastępuje zbyt stenograficzne M0302; wspomnienie oddaje sens, nie zawsze dokładny cytat | C12-M0303–C12-M0306 |
| Wiedza Draco | M0394 zastępuje M0390. Draco nie zna planu pójścia do Dumbledore’a tylko dlatego, że wiedział o nim Nott | C12-M0391–C12-M0394 |
| Pince i Hermiona | Hermiona nie odkrywa od nowa, że James ją obserwował w bibliotece; wiedziała wcześniej, nowością jest komentarz Pince | C12-M0593–C12-M0594 |
| Plan i fakultety | Pierwotny plan M0652 odwołany; wybór użytkownika M0659 i akceptacja M0661 ustanawiają Runy + Opiekę oraz wewnętrzne zaliczenia Numerologii/Mugoloznawstwa. Wersje planu M0662 i M0674 różnią się czwartkiem/piątkiem: nie dopisywać identyczności całego tygodnia | C12-M0653–C12-M0674 |
| Veritaserum | Wypowiedź Jamesa M0833 nie zmienia jego przeszłości. Po przypomnieniu M0838 w M0839 wycofuje osobistą obecność przy Veritaserum, pozostaje świadkiem wcześniejszego podsłuchu i demaskacji | C12-M0833–C12-M0840 |
| Pióro | Nie przejmuje magicznie kontroli nad ręką; odmowa możliwa, z konsekwencjami szkolnymi. Nie stosować późniejszej władzy Inkwizytora przed jej nadaniem | C12-M0863–C12-M0866 |
| Duże cofnięcie Draco | **M0922–M0949 w całości anulowane**, łącznie z ujawnieniem snu przy Hermionie, przeprosinami, nocą i porankiem. Zachowany punkt M0921; nowa odpowiedź M0953 i dalszy ciąg od M0954 | C12-M0950–C12-M0953 |
| Wszystkie NPC | Zachowywać osobowości, samodzielność i ograniczoną wiedzę. Nie robić z Draco serdecznego kumpla, z Rona tylko rywala, ze Snape’a łagodnego opiekuna | C12-M0956–C12-M0957 |
| Główna fabuła | James zmienia szczegóły i własne wątki, nie wykoleja przypadkowo kanonicznego biegu V roku. Zgłoszenie pióra nie powoduje automatycznego zwolnienia Umbridge | C12-M1014–C12-M1021 |
| Spontaniczna Hermiona | Figlarna i bardziej inicjatywna, nadal ta sama osoba, z własnymi granicami | C12-M1082–C12-M1083, C12-M1091 |
| Łaskotki | James jawnie koryguje dawną deklarację ich braku i ujawnia wyjątek. Wcześniejsze nieskuteczne próby nie znikają; Hermiona poznaje nowy sekret | C12-M1097–C12-M1103 |

## Nieciągłości i ograniczenia, bez dopisywania historii

- TURN 471 = M0941, tylko USER; TURN 472 = M0942–M0943 zawiera zmienioną wersję urwanej kwestii. Obie zachowane i obie znajdują się w później anulowanej gałęzi.
- Eksport zawiera daty interfejsu, podpisy źródeł, „Przetwarzano przez”, OOC i końcowe sugestie „Jeśli chcesz, mogę…”. To nie wydarzenia ani dialog NPC. Oryginał zachowano; mapowanie pokazuje wszystkie TURN i KEY.
- M0196 zatrzymuje skok 6 VIII, a M0198 ponownie doprowadza do 6 VIII. To nakładające się opisy jednego okresu, nie drugi sierpień.
- M0201 zaprasza Lunę i Élodie; odpowiedź Kruma M0202 zakłada otrzymanie zaproszenia bez odpowiadającej deklaracji użytkownika. Zachować jako niespójność, nie jako dopisany list Jamesa.
- M0346 nazywa Hagrida osobą zwołującą pierwszorocznych mimo wcześniejszego kanonicznego tła; nie wyprowadzać z tego nieodwołanego rozstrzygnięcia jego misji. W archiwum pozostaje literalnie.
- Następstwo uczty 1 IX, poranka i poniedziałkowego planu nie wyznacza bezspornego dnia końca. Nie naprawiać dat retrospektywnie bez korekty użytkownika.
- M1051 ustanawia sofę, M1058 mówi „łóżko”, bez opisu zmiany. To rozbieżność porannej aranżacji; po lekcjach M1085 jednoznacznie wprowadza łóżko.
- Ciemność w M1094 obowiązuje do końca: NPC nie widzą rumieńców ani wyrazu twarzy bez światła. Kwestie o domyślnych reakcjach Jamesa nie uprawniają narratora do przejmowania go.
- „Granger-Brown”, ślub za ocenę i obrazy w pokoju nie ustanawiają małżeństwa, nowego nazwiska ani pewnej przyszłości.
'''
U['10_ZASADY_I_CIAGLOSC.md']='''# Zasady i ciągłość — obowiązujące po C12

1. Najpierw aktualne CURRENT, rejestr korekt, wiedza NPC i te zasady. Po rozpoczęciu sceny rozwijaj bieżący stan; nie wracaj do dawnego CURRENT.
2. James Brown należy wyłącznie do użytkownika. Aktualizacja plików nie jest turą RPG; nie dopisuj działań ani odpowiedzi postaci.
3. Najpierw indeks i plik tematyczny, potem konkretny zakres archiwum. Odsyłacze do dużych i małych części są równorzędnymi drogami do tego samego tekstu.
4. Jawna korekta działa tylko w swoim zakresie. M0922–M0949 C12 są anulowane także dla wiedzy postaci. OOC, sny, żarty i plany nie są wydarzeniami.
5. Pilnuj źródła wiedzy NPC, świadków, szeptów i obecności. Hermiona nie zna całej sprawy pióra; Draco nie pamięta odrzuconej rozmowy o śnie.
6. Pisz sceny naturalnie, bez przypisów i encyklopedycznych komentarzy. Potrzebne wyjaśnienie wyraźnie oddziel na końcu. Wspomnienia przeważnie oddają sens, nie stenogram (C12-M0101–M0104, M0303–M0306).
7. Zachowuj wiek, osobowość i samodzielność każdej postaci (C12-M0253, M0956). Respekt Draco nie jest posłuszeństwem; Hermiona ma przyjaciół, naukę i własne zdanie; Snape nie staje się łagodny przez jedną interwencję.
8. Podtrzymuj kanoniczny kierunek głównej fabuły z rozegranymi zmianami AU; nie ogłaszaj przyszłych scen już wykonanymi (C12-M1014–M1015). Lorebook jest dodatkiem, nie instrukcją wymuszenia przyszłości.
9. Bieżąca scena: Pokój Życzeń po lekcjach, nie londyńska sypialnia z C11. Dokładnej wrześniowej daty nie ustalono; nie utożsamiać dat eksportu z czasem świata.
10. Nie utożsamiaj czuwania ze snem ani pojedynczego snu z wyleczeniem. Szkolne egzaminy kwalifikacyjne Jamesa nie zastępują SUM-ów.
11. Przed turą sprawdź pozycje, światło, stroje, przedmioty i ostatnią wypowiedź. W ciemności polegaj na słuchu i dotyku; nie dopisuj widzenia.
12. Zachowuj wzajemne granice i samodzielność bohaterów. „Szalona Hermiona” nie znosi jej granic. Wątki romantyczne nie zmieniają wieku postaci.
13. Brak źródła zgłoś krótko zamiast uzupełniać z wyobraźni. Nie obiecuj automatycznej synchronizacji; odróżniaj pliki, repozytorium i załączniki projektu.

Starsze niesprzeczne zasady pozostają w historycznej części pełnego pliku. Powyższe są aktualnym skrótem.
'''
current='''# CURRENT — jedyny punkt kontynuacji

'''+state+'''

## Miejsce i chwila

James i Hermiona są sami w Pokoju Życzeń na VII piętrze Hogwartu, po lekcjach. Tego ranka James z Harrym zgłosili pióro Snape’owi i Dumbledore’owi. To nie jest 9 lipca ani dom Jamesa. Użytkownik przeszedł przez śniadanie i szkolny dzień w C12-M1084; ich powrót do pokoju już nastąpił.

Data: początek września, dzień D+2 względem pierwszej rozegranej lekcji Umbridge; dokładny dzień miesiąca pozostaje nierozstrzygnięty z powodu przejścia od 1 IX do poniedziałkowego planu. Okna z gwiazdami są aranżacją pokoju, nie zegarem.

## Pozycje i ostatnie działanie

Oboje pozostają na dużym łóżku. Ostatnie jawne ułożenie Jamesa to leżenie nad Hermioną z podparciem na łokciach (M1090); później nie opisano pełnej zmiany pozycji. Baldachim zasunięty różdżką w M1094: kompletna ciemność. Buty obojga zdjęte. Nie wprowadzono rozbierania z mundurków, nowego snu ani zamknięcia drzwi na klucz.

W M1098–M1103 James ujawnił Hermionie prywatny sekret łaskotek i poprosił o dyskrecję. W M1107 Hermiona przestała łaskotać; w końcowej odpowiedzi M1109 pozostaje przy spokojnym masażu karku i głaskaniu włosów. Oboje przytomni. Ostatnia kwestia NPC dotyczy zaufania. Końcowa lista propozycji dalszych działań jest dopiskiem interfejsowym/OOC, nie dialogiem Hermiony.

**Następna tura należy do Jamesa. Nie dopisano jego reakcji.**

## Wystrój i przedmioty

Druga, popołudniowa aranżacja Hermiony (M1085): ciepły duży salon, kominek, wielka sofa, regały i rośliny, unoszące się świece, stolik ze słodyczami i napojami; łóżko z baldachimem, ogród zimowy z dwiema huśtawkami, tablica ruchomych wyobrażeń wspólnego życia. Obrazy nie pokazują pewnej przyszłości.

James nosił rano mundurek Slytherinu z bordowo-złotym krawatem (M0970); brak późniejszego przebrania. Hermiona w szkolnym stroju; nie przywracaj lipcowej błękitnej sukienki. Torba Hermiony ostatnio pod ścianą przy wejściu (M1085), bez potwierdzonego wniesienia. Miejsce odłożenia różdżki po M1094 niepodane. Nie sprowadzaj pozostałych rekwizytów z Londynu bez podstaw.

## Wiedza i sprawy w tle

- Hermiona widziała świeży ślad na dłoni Jamesa po szlabanie i podejrzewa Umbridge. Nie poznała jawnie pełnego mechanizmu pióra, rozmowy z Harrym ani porannego zgłoszenia.
- Snape i Dumbledore obejrzeli obie dłonie. Dokumentacja, dyskrecja i dalsze działania są polecone; nie opisano zwolnienia Umbridge ani zakończenia sprawy. Brak opisanego leczenia śladu Jamesa.
- Draco zna tylko poprawioną rozmowę o piórze. M0922–M0949 anulowane: nie zna z tej gałęzi sekretu snu przy Hermionie.
- Związek trwa, wcześniejsza kłótnia o rozłąkę złagodniała. Hermiona ma własne obowiązki i przyjaciół. Brak ślubu/zaręczyn; nazwisko Granger pozostaje.
- Zakład o dziewięć wspólnych SUM-ów otwarty. James nie jest prefektem. Nie ogłaszać wyleczenia bezsenności.

Przed ważnym faktem: 04_KTO_CO_WIE, 09_REJESTR_KOREKT, odpowiedni dział i indeks C12. Nie rozwijać fabuły podczas odczytu tego pliku.
'''
# Current summaries override only their own scope. Keep old text intact under an explicit historical label.
for name,t in U.items():
 oldtext=fullold[name]
 put(B/name,t+'\n\n---\n# Historia do C11 — nie jest bieżącym punktem startu\n\nPoniższy zapis zachowano dla źródeł. Zakończone wizyty i dawne statusy zastępuje aktualizacja C12 powyżej; niesprzeczne fakty pozostają.\n\n'+oldtext)
 anchor=activeold.get(name,'')
 # Historical active summaries are not repeated as equal-status current facts.
 put(G/'02_PLIKI_AKTYWNE'/name,t+'\n\nPełna wcześniejsza historia i źródła: [pełny dział](../04_BAZA_PELNA/'+name+').')
put(B/'08_CURRENT.md',current);put(G/'02_PLIKI_AKTYWNE/08_CURRENT.md',current)
# Exact agreed schedules with the unresolved discrepancies made explicit.
plan='''# Plany V roku — ustalenia kampanii C12

| Dzień | James — C12-M0662 | Hermiona — C12-M0674 |
|---|---|---|
| Poniedziałek | Historia Magii, przerwa, podwójne Eliksiry, obiad, Runy, podwójna Obrona | Historia Magii, podwójne Eliksiry, obiad, Runy, podwójna Obrona |
| Wtorek | podwójne Zaklęcia, przerwa, podwójna Transmutacja, obiad, Opieka, Zielarstwo | podwójne Zaklęcia, podwójna Transmutacja, obiad, Opieka, Zielarstwo |
| Środa | nauka własna, Transmutacja, obiad, podwójne Zielarstwo, Opieka, Astronomia wieczorem | Numerologia, Transmutacja, obiad, podwójne Zielarstwo, Opieka, Astronomia wieczorem |
| Czwartek | Eliksiry, Zaklęcia, przerwa, Historia Magii, obiad, Obrona, nauka własna | Eliksiry, Zaklęcia, obiad, Obrona, Numerologia |
| Piątek | podwójne Runy, Transmutacja, obiad, Zaklęcia, wolny blok | podwójne Runy, Historia Magii, obiad, podwójna Numerologia |

To zapis dwóch przyjętych tabel, nie pełny plan książkowy. M0674 stwierdza okna Jamesa przy Numerologii, ale nie uzgadnia sprzecznych bloków czwartku/piątku z M0662. Do scen wymagających dokładnego wspólnego terminu trzeba rozstrzygnąć tę rozbieżność; nie zmieniać fakultetów i nie wybierać ich ponownie. Pierwotny plan M0652 jest odrzucony.
'''
put(B/'12_PLAN_LEKCJI.md',plan);put(G/'02_PLIKI_AKTYWNE/12_PLAN_LEKCJI.md',plan)
scenes=[(1,4,'Start C12 i odpowiedź na koniec C11'),(5,42,'Sen obojga; zegar 16:00'),(43,66,'Relacja ze snu; warunkowa rozmowa o ślubie'),(67,88,'Biblioteka domu i drugi sen'),(89,104,'Tobik o 18:45; korekta stylu'),(105,118,'Koniec czytania; rozmowa o ojcu Hermiony'),(119,148,'Taksówka do Grangerów, przyjazd 19:55'),(149,174,'Powrót do rodziców i pożegnanie'),(175,194,'Powrót Jamesa, opłata i czuwanie'),(195,206,'Skok wakacyjny, listy, koperta, prefektury'),(207,218,'Peron 1 IX; prawdziwy Moody i powitanie'),(219,230,'Kłótnia, szyba, Harry'),(231,260,'Nott i prefektura; Luna, Ginny, Neville'),(261,306,'Wyjaśnienia Hermiony; korekta pamięci'),(307,342,'Obchody, słodycze i sen w pociągu'),(343,378,'Hogsmeade, powóz i widziane stworzenia'),(379,394,'Uczta i korekta wiedzy Draco'),(395,440,'Spór z Draco, ceremonia i Umbridge'),(441,478,'Rozmowa o odznace z Dumbledore’em'),(479,534,'Pokój Slytherinu; Nott, Draco i Pansy'),(535,584,'Poranek, biblioteka i pojednanie'),(585,610,'Pince, wspólna lektura'),(611,644,'Śniadanie i odwołany żart o ślubie'),(645,674,'Fakultety, egzaminy i plany lekcji'),(675,690,'Historia Magii, sen i przejście do lochów'),(691,728,'Eliksiry, lilia i oddana próbka'),(729,768,'Przerwa, granice i obiad'),(769,812,'Runy i zakład o SUM-y'),(813,840,'Obrona, Harry i korekta Veritaserum'),(841,850,'Spór o Ministerstwo; szlaban Jamesa'),(851,866,'Krwawe pióro i odmowa'),(867,892,'Ślad widziany przez Hermionę; rozmowa z Harrym'),(893,921,'Pożegnanie i powrót do Slytherinu'),(922,949,'ANULOWANA gałąź Draco, noc i poranek'),(950,957,'Jawne cofnięcie i zasady charakterów'),(958,976,'Poprawiona rozmowa, noc i Nott rano'),(977,994,'Zgłoszenie pióra Snape’owi'),(995,1023,'Harry, oględziny, Dumbledore i dokumentacja'),(1024,1050,'Oczekiwanie na Hermionę; odmowa wejścia do wieży'),(1051,1084,'Poranny Pokój Życzeń; uzgodnienie powrotu'),(1085,1097,'Pokój po lekcjach, wyobrażony dom i baldachim'),(1098,1109,'Prywatny sekret i końcowy odpoczynek')]
assert [n for a,b,_ in scenes for n in range(a,b+1)]==list(range(1,1110))
js(B/'scenes_c12.json',scenes)
# Mapping to raw export, preserving all source keys.
maptext='# Mapowanie C12: TURN / KEY / ID\n\n555 TURN, 1109 wiadomości. Etykieta UNKNOWN nie oznacza nieznanego autora: separator „ChatGPT powiedział:” rozdziela USER i ASSISTANT. Usunięto wyłącznie początkowe metadane interfejsu oraz końcowe linie przetwarzania; oryginał jest dostępny osobno. TURN 471 bez odpowiedzi; niczego nie dopisano.\n\n| TURN | KEY | ID |\n|---|---|---|\n'+'\n'.join(f"| {x['turn']} | {x['key']} | {', '.join(x['ids'])} |" for x in mp)
put(B/'00_MAPOWANIE_C12.md',maptext);put(G/'03_INDEKS/00_MAPOWANIE_C12.md',maptext)
manifest=dict(version='C1-C12',current_id='C12-M1109',messages=12045,merged_file=mergedrel,merged_sha256=sha(merged),small=small,large=large);js(G/'03_INDEKS/INDEKS_PLIKOW.json',manifest)
for kind,items,names in [('dużych',large,['INDEKS_CZATY.md','INDEKS_DUZYCH_CZESCI.md']),('małych',small,['INDEKS_MALYCH_CZESCI.md'])]:
 txt=f'# Indeks {kind} części — C1–C12\n\n12045 wiadomości; 12 dużych i 66 małych części. Małe części mają do 200 pełnych wiadomości. Starsze pliki i ID zachowano bez zmian.\n\n| Plik | Od | Do | Liczba |\n|---|---|---|---|\n'
 txt+='\n'.join(f"| [{Path(c['file']).name}](../{c['file']}) | {c['first']} | {c['last']} | {c['messages']} |" for c in items)
 for name in names:put(G/'03_INDEKS'/name,txt)
scenehead='\n\n# C12 — indeks scen (także wersje odrzucone)\n\n| Zakres | Scena | Duża część | Małe fragmenty |\n|---|---|---|---|\n'
rows=[]
for a,b,title in scenes:
 chunks=[c for c in small if c['first'].startswith('C12-') and int(c['first'].split('M')[1])<=b and int(c['last'].split('M')[1])>=a]
 links=', '.join(f"[{Path(c['file']).stem.split('_')[1]}](../{c['file']})" for c in chunks)
 rows.append(f'| C12-M{a:04d}–C12-M{b:04d} | {title} | [C12](../01_ARCHIWA_CZATY/01_ARCHIWUM_CZAT_12.txt) | {links} |')
idx=G/'03_INDEKS/INDEKS_SCEN.md';put(idx,idx.read_text()+scenehead+'\n'.join(rows))
put(B/'01_ARCHIWUM_SCEN_INDEKS.md',fullold['01_ARCHIWUM_SCEN_INDEKS.md']+scenehead+'\n'.join(rows))
for target,src in [('00_INDEKS_DUZYCH_CZESCI.md','INDEKS_DUZYCH_CZESCI.md'),('00_INDEKS_MNIEJSZYCH_CZESCI.md','INDEKS_MALYCH_CZESCI.md')]:put(B/target,(G/'03_INDEKS'/src).read_text())
p=G/'03_INDEKS/PODSUMOWANIA.md';put(p,p.read_text()+'\n\n## C12\n\n9 VII: sen, biblioteka i powrót Hermiony o 19:55. Wakacyjna rozłąka, listy, powrót na V rok, spór o prefekturę, nowe fakultety i zakład o SUM-y. Umbridge i pióro: odmowa Jamesa, świadectwo Harry’ego i zgłoszenie nauczycielom. Cofnięta gałąź Draco wyłączona z kanonu. Koniec w Pokoju Życzeń po lekcjach, C12-M1109; następna tura użytkownika. Dokładna wrześniowa data nieustalona.')
# Updated lore preserves world entries, marks all earlier campaign entries historical.
oldlore=json.loads((B/'Hogwarts_RPG_1994_SpicyChat_PL_EN_SAFE.json').read_text());entries=[]
for name,txt in [('RPG — pierwszeństwo i użycie',state+' Aktualizacja C12 zmienia tylko jawnie wskazany zakres; dawne CURRENT są historyczne.')]+[(f'C12 — {n[3:-3]}',t) for n,t in U.items()]+[('C12 — CURRENT',current),('C12 — PLAN LEKCJI',plan)]:
 keys=[name,'James Brown','Hermiona Granger','C12'];entries.append(dict(name=name,keys=keys,keywords=keys,content=txt.strip()))
for e in oldlore['entries']:
 e=dict(e)
 if not e['name'].startswith('ŚWIAT'):
  e['name']='HISTORIA DO C11 — '+e['name'];e['content']='ZAPIS HISTORYCZNY: punkt końcowy i statusy mogą być zmienione przez C12. Nie jest bieżącym CURRENT. Niesprzeczne fakty pozostają.\n\n'+e['content']
 entries.append(e)
lore=dict(name='Hogwarts RPG — C1–C12',description=state+' Wpisy świata zachowane; import zewnętrzny nietestowany.',entries=entries)
js(B/'Hogwarts_RPG_1994_SpicyChat_PL_EN_SAFE.json',lore)
put(B/'11_LOREBOOK_HOGWARTS_C1-C12.md','# Lorebook Hogwart — C1–C12\n\n'+lore['description']+f'\n\nLiczba wpisów: {len(entries)}.\n\n'+'\n\n'.join(f"## Wpis {i:03d}: {e['name']}\n\nSłowa kluczowe: {', '.join(e['keys'])}\n\n{e['content']}" for i,e in enumerate(entries,1)))
# Old named lore remains as a pointer; original exact text is in version history.
put(B/'11_LOREBOOK_HOGWARTS_C1-C11.md','# Wersja historyczna C1–C11\n\nAktualna wersja: [lorebook C1–C12](11_LOREBOOK_HOGWARTS_C1-C12.md). Oryginalną wersję C11 zachowano w [historii](../05_HISTORIA_BAZY/do_C11/11_LOREBOOK_HOGWARTS_C1-C11.md).')
put(G/'02_PLIKI_AKTYWNE/LOREBOOK.md','# Lorebook — użycie po C12\n\n'+state+'\n\nNajpierw CURRENT, wiedza NPC i korekty. [Pełny lorebook C1–C12](../04_BAZA_PELNA/11_LOREBOOK_HOGWARTS_C1-C12.md) uzupełnia świat. Czarne pióro jest u Umbridge; tajna kwatera nieznana Jamesowi; obrazy w Pokoju Życzeń nie są przepowiednią. Dawne punkty startowe nie obowiązują.')
put(G/'02_PLIKI_AKTYWNE/MAPA.md','# Miejsca — po C12\n\nAktualnie: Pokój Życzeń, VII piętro Hogwartu, po lekcjach; aranżacja M1085. Gabinet Snape’a w lochach był miejscem porannego zgłoszenia. Gruba Dama pilnuje wejścia do wieży Gryffindoru, James nie został wpuszczony. Pokój wspólny Slytherinu pozostaje jego domowym zapleczem w szkole.\n\nLondyn: dom Jamesa przy 14B Belgrave Square i dom Grangerów przy 8 Heathgate (M0125–M0126). Historyczna rozbieżność Eaton Square/Belgrave Square nierozstrzygnięta. Grimmauld Place istnieje jako tło, ale adres pozostaje poza wiedzą Jamesa.\n\n[Wcześniejsza mapa](../05_HISTORIA_BAZY/MAPA_DO_C11.md).')
put(G/'05_HISTORIA_BAZY/MAPA_DO_C11.md',activeold['MAPA.md'])
start='# Baza kampanii C1–C12\n\n'+state+'\n\n12045 wiadomości, 12 dużych części, 66 małych (do 200 wiadomości). C1–C11 i ich 60 fragmentów zachowane bajt w bajt; C12 ma 555 TURN i 1109 wiadomości.\n\nCzytaj CURRENT, zasady, korekty i wiedzę NPC, potem indeks i konkretną scenę. Odrzucone wersje zachowano w archiwum, lecz wyłączono z kanonu. Dawne pliki w historii nie są równorzędnymi punktami startu.\n\nBieżące dane i indeksy zaktualizowano po C12. Starsze archiwa kontrolowano bajtowo; nie wykonano ponownej interpretacji całej kampanii. Zapis repozytorium nie podmienia automatycznie załączników projektu.'
put(B/'00_START.md',start)
counts=json.loads((hist/'KONTROLA_ARCHIWUM.json').read_text())['message_counts'];counts['C12']=1109
control=dict(version='C1-C12',current_id='C12-M1109',current_date=None,current_date_description='początek września 1995; D+2 od pierwszych rozegranych lekcji, dokładna data nieustalona',current_time='po lekcjach',next_turn='USER — James',message_counts=counts,total_messages=12045,source_c12_turns=555,source_c12_messages=1109,smaller_parts=66,large_parts=12,lorebook_entries=len(entries),world_entries=sum(e['name'].startswith('ŚWIAT') for e in entries),merged_sha256=sha(merged),previous_merged_sha256=sha(base),source_c12_sha256=sha((R/'c12_input/ChatGPT_CALY_CZAT12.txt').read_bytes()),chunks=[dict(c,file=c['file'].replace('01_ARCHIWA_CZATY/','')) for c in small],large_files=[dict(c,file='duze_czesci/'+Path(c['file']).name) for c in large],checks=dict(previous_60_chunks_unchanged=True,previous_11_large_files_unchanged=True,concatenations_exact=True,unique_contiguous_ids=True,raw_c12_unchanged=True),scope='Aktualizacja po C12; poprzednie archiwa zachowane i sprawdzone bajtowo. Nie pełna ponowna interpretacja C1–C11.')
js(B/'KONTROLA_ARCHIWUM.json',control)
# Work with the repository's actual nested layout and renamed folders.
config=dict(repository_url='https://github.com/tmmateuszkruk-dev/RPG-Archiwum',default_branch='main',base_path='RPG-Archiwum',raw_base='https://raw.githubusercontent.com/tmmateuszkruk-dev/RPG-Archiwum/refs/heads/main/RPG-Archiwum/',state='C12-M1109');js(G/'REPO_CONFIG.json',config)
p=G/'AGENTS.md';put(p,p.read_text().replace('05_BAZA_PELNA','04_BAZA_PELNA').replace('Następny numer C12','Następny numer C13').replace('C11-M0409','C12-M1109')+'\n\nAktualny zakres C1–C12. Wycofana gałąź C12-M0922–C12-M0949 nie daje wiedzy NPC. Repozytorium ma podfolder RPG-Archiwum; ścieżki RAW muszą go zawierać.')
instr='''# Instrukcje projektu — aktualizacja po C12

Prowadź RPG po polsku, zachowując ciągłość. Przed pierwszą kontynuacją czytaj najnowsze 08_CURRENT, 10_ZASADY_I_CIAGLOSC, 09_REJESTR_KOREKT i 04_KTO_CO_WIE, także wersje z dopiskami w nazwie. Zakres i zawartość rozstrzygają aktualność.

James Brown wyłącznie użytkownika. Narrator prowadzi świat i NPC, nie dopisuje Jamesowi myśli, uczuć, słów, reakcji ani działań. Późniejsze rozegrane zdarzenia rozwijają CURRENT; nie cofaj do pliku co turę. Jawna korekta zastępuje starsze ustalenie tylko w swoim zakresie. Odrzucone wersje nie są kanonem ani wiedzą NPC.

Najpierw sprawdź właściwy dział, następnie indeks i tylko potrzebny fragment archiwum. Przed użyciem faktu przez NPC ustal, jak go poznał. Pilnuj obecności, szeptów, czasu, pozycji i rekwizytów. Zachowuj kanoniczne charaktery i samodzielność; respekt Draco nie jest uległością, związek nie odbiera Hermionie przyjaciół i celów.

Pisz naturalnie, bez encyklopedycznych wstawek. Konieczne wyjaśnienia oddziel na końcu. Lorebook C1–C12 jest dodatkiem; nie narzuca przyszłych wydarzeń. Przy braku źródła powiedz to krótko, nie wymyślaj historii. Nie deklaruj automatycznej synchronizacji plików.

Repozytorium: https://github.com/tmmateuszkruk-dev/RPG-Archiwum

**Pliki znajdują się w podfolderze RPG-Archiwum.**

RAW baza: https://raw.githubusercontent.com/tmmateuszkruk-dev/RPG-Archiwum/refs/heads/main/RPG-Archiwum/

Bieżący punkt: `02_PLIKI_AKTYWNE/08_CURRENT.md`.
Indeks scen: `03_INDEKS/INDEKS_SCEN.md`.
Pełny Part12: `01_ARCHIWA_CZATY/01_ARCHIWUM_CZAT_12.txt`.
Małe fragmenty: `01_ARCHIWA_CZATY/mniejsze_czesci/`.
Pełne działy: `04_BAZA_PELNA/`.

Nie wczytuj całego repozytorium przy każdej odpowiedzi. Podczas aktualizacji zachowaj oryginał i zakończ CURRENT bez dopisywania następnej akcji.
'''
put(G/'INSTRUKCJE_PROJEKTU.md',instr)
readme='''# RPG-Archiwum — C1–C12

**12045 wiadomości, 12 dużych archiwów, 66 fragmentów po maksymalnie 200 wiadomości.** Stan: C12-M1109, Pokój Życzeń po lekcjach, początek września 1995. Dokładna data nieustalona; następna tura Jamesa.

- [CURRENT](RPG-Archiwum/02_PLIKI_AKTYWNE/08_CURRENT.md)
- [Duże części](RPG-Archiwum/03_INDEKS/INDEKS_CZATY.md)
- [Małe części](RPG-Archiwum/03_INDEKS/INDEKS_MALYCH_CZESCI.md)
- [Indeks scen](RPG-Archiwum/03_INDEKS/INDEKS_SCEN.md)
- [Instrukcje projektu z właściwymi adresami RAW](RPG-Archiwum/INSTRUKCJE_PROJEKTU.md)

| Folder wewnątrz RPG-Archiwum | Zawartość |
|---|---|
| 01_ARCHIWA_CZATY | Pełne części, małe fragmenty i scalone archiwum |
| 02_PLIKI_AKTYWNE | Bieżący stan, wiedza NPC, zasady i skróty |
| 03_INDEKS | Indeksy i mapowania do oryginalnych eksportów |
| 04_BAZA_PELNA | Pełne działy, lorebook Markdown/JSON |
| 04_ORYGINALY | Oryginał eksportu C12 |
| 05_HISTORIA_BAZY | Zachowane wcześniejsze wersje wiedzy |
| scripts | Wyszukiwanie ID i kontrola integralności |

Najpierw indeks, potem konkretny fragment. C12-M0922–C12-M0949 to odrzucona gałąź, zachowana wyłącznie archiwalnie. Sny, plany i OOC nie stają się faktami świata.

```bash
cd RPG-Archiwum
python scripts/sprawdz.py
python scripts/znajdz.py C12-M1109
```

Starsze archiwa C1–C11 i 60 fragmentów zachowano bajt w bajt. Aktualizacja repozytorium nie podmienia automatycznie załączników ani ustawień projektu ChatGPT. Do ręcznej podmiany przeznaczony jest folder 02_PLIKI_AKTYWNE.
'''
put(G.parent/'README.md',readme)
p=G/'scripts/sprawdz.py';s=p.read_text().replace('range(1,12)','range(1,13)').replace("if '06_HISTORIA_BAZY' in p.parts:continue","if '05_HISTORIA_BAZY' in p.parts:continue");put(p,s)
# Repair inherited bad paths in live metadata, preserving historical files.
for folder in ['02_PLIKI_AKTYWNE','03_INDEKS','04_BAZA_PELNA']:
 for p in (G/folder).glob('*.md'):
  s=p.read_text().replace('../05_BAZA_PELNA/','../04_BAZA_PELNA/').replace('../06_HISTORIA_BAZY/','../05_HISTORIA_BAZY/')
  put(p,s)
# Standalone downloadable full package mirrors the verified repository.
O.mkdir(exist_ok=True)
for p in B.iterdir():
 if p.is_file():shutil.copyfile(p,O/p.name)
for c in small:
 p=O/'mniejsze_czesci'/Path(c['file']).name;p.parent.mkdir(exist_ok=True);shutil.copyfile(G/c['file'],p)
for c in large:
 p=O/'duze_czesci'/Path(c['file']).name;p.parent.mkdir(exist_ok=True);shutil.copyfile(G/c['file'],p)
shutil.copyfile(G/mergedrel,O/Path(mergedrel).name)
shutil.copytree(G/'04_ORYGINALY',O/'oryginaly',dirs_exist_ok=True);shutil.copytree(G/'05_HISTORIA_BAZY/do_C11',O/'historia_wersji/do_C11',dirs_exist_ok=True)
for p in O.glob('*.md'):
 s=p.read_text().replace('../01_ARCHIWA_CZATY/mniejsze_czesci/','mniejsze_czesci/').replace('../01_ARCHIWA_CZATY/','duze_czesci/').replace('../05_HISTORIA_BAZY/do_C11/','historia_wersji/do_C11/')
 put(p,s)
# Document all source parsing rules; raw file retained separately.
put(G/'03_INDEKS/KONTROLA_C12.md',f'''# Kontrola C12

555 bloków TURN; 555 USER i 554 ASSISTANT; 1109 ID. Jeden blok bez odpowiedzi (471), zachowany. 42 zakresy scen pokrywają wszystkie ID. 12 dużych i 66 małych plików odtwarzają scalone archiwum bajt w bajt. Poprzednie 60 fragmentów i 11 dużych części zachowano dokładnie.

Oryginał SHA-256: {control['source_c12_sha256']}
Scalone SHA-256: {sha(merged)}

Daty z interfejsu nie datują fabuły. Końcowe sugestie i komentarze źródłowe w archiwum nie są fabułą. Zastosowano jawne cofnięcie M0922–M0949 i mniejsze korekty z rejestru. Starszych streszczeń nie reinterpretowano w całości.
''')
# Persist preparatory source in the git-backed project.
for p in ['build_c12.py','parse_c12.py']:
 dest=G/'05_HISTORIA_BAZY/narzedzia_przygotowania'/p;shutil.copyfile(R/p,dest)
print(json.dumps({'messages':12045,'large':len(large),'small':len(small),'scenes_c12':len(scenes),'lore_entries':len(entries)}))
