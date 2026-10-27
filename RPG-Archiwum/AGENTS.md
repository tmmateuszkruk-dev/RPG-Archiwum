# Instrukcje pracy z kampanią — C1–C14

Aktualny punkt: C14-M0704. 13 778 pozycji, 14 dużych części, 76 fragmentów, 131 kart pamięci.
Aktualny zestaw: `01_ARCHIWA_CZATY/wersja_do_udostepniania/`; starszy zestaw C1–C13 poza nim jest zachowany historycznie.
Indeksy: `03_INDEKS/INDEKS_DUZYCH_CZESCI.md` i `03_INDEKS/INDEKS_MALYCH_CZESCI.md`.


To repozytorium jest bazą ciągłości polskiego RPG. James Brown należy wyłącznie do użytkownika. Nie kontynuuj sceny podczas aktualizacji archiwum.

Przed pierwszą narracją przeczytaj pliki z 02_PLIKI_AKTYWNE: 08_CURRENT.md, 10_ZASADY_I_CIAGLOSC.md, 09_REJESTR_KOREKT.md, 04_KTO_CO_WIE.md. Potem rozwijaj bieżącą rozmowę; nie resetuj do CURRENT.

Obowiązujące reguły prowadzenia są w 02_PLIKI_AKTYWNE/10_ZASADY_I_CIAGLOSC.md. Dawne wersje instrukcji i punktów startowych w 05_HISTORIA_BAZY są źródłem historycznym. Przy sprawdzaniu aktualności porównuj osobno końcowe ID historii oraz wersję treści kart i korekt. Ten sam cutoff nie wyklucza nowszej korekty wieku lub profilu. Czytaj indywidualną kartę, nie tylko jej kopię JSON.

Po zmianie kart uruchom `python scripts/synchronizuj_profile.py`, następnie `python scripts/synchronizuj_profile.py --check`. Sekcja `## Dane bieżące` (lub istniejąca sekcja nadrzędnego profilu Jamesa) jest źródłem profilu bieżącego w JSON; nie zmienia automatycznie dawnych wydarzeń. Zapisz razem karty i pochodną bazę. Przeglądarka wymaga osobnego odświeżenia danych i publikacji; sprawdź jej sourceCommit i sourceVersions, także bez nowej części. Zachowaj prywatność strony.

Do ważnego faktu dobierz dział. Jeżeli skrót jest niejasny, sprawdź 03_INDEKS/INDEKS_SCEN.md oraz właściwy fragment archiwum. Jedno ID znajduje `python scripts/znajdz.py C14-M0704`; zakres przyjmuje dwa ID z tego samego Part. Pełne działy są w 04_BAZA_PELNA. Historyczne punkty końcowe nie są bieżącym stanem.

Późniejsza jawna korekta użytkownika ma pierwszeństwo tylko w swoim zakresie. Oddziel wiedzę NPC, narratora, prywatne myśli, plotki, deklaracje i marzenia. Nie mieszaj odrębnych kampanii. Zachowuj osobowości, wiek i samodzielność NPC. Brak źródła zgłoś zamiast zgadywać.

Przy aktualizacji: zachowaj oryginał, istniejące ID i odrzucone wersje w archiwum; dopisz nowy Part. Uaktualnij pełną bazę, aktywne skróty, oba indeksy, indeks scen, CURRENT, rejestr korekt i lorebook. Następny nowy Part: C15; ponowny eksport C14 zachowuje jego ID. Nie dopisuj odpowiedzi NPC ani ruchu Jamesa poza transkryptem.

Sprawdź `python scripts/sprawdz.py`. Nie usuwaj historii i nie publikuj repozytorium bez zlecenia. Samo istnienie AGENTS.md nie oznacza, że dowolny czat automatycznie go odczyta. Nie obiecuj automatycznej synchronizacji.


Wycofana gałąź C12-M0922–C12-M0949 nie daje wiedzy NPC. Repozytorium ma podfolder RPG-Archiwum; ścieżki RAW muszą go zawierać.
