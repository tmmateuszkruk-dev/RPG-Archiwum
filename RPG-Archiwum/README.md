# RPG-Archiwum — C1–C11

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
