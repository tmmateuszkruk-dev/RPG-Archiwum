# Pamięć C1–C14

131 kart; stan C14-M0704. Zachowano starsze fakty. C14 ma 704 wiadomości i 0 luk eksportu; sprawdź korekty i źródło, szczególnie odrzucone M0276.

Zapytanie: `python 06_PAMIEC_POSTACI/query_memory.py 06_PAMIEC_POSTACI hermiona --term list`

Wzmianki służą wyszukiwaniu, nie dowodzą obecności ani wiedzy.

## Aktualny profil a zakres historii

Ten sam końcowy numer wiadomości może mieć nową korektę wieku, urodzin, wyglądu lub zasad. Czytaj bieżącą kartę Markdown i porównuj jej wersję z `card_source` oraz `current_profile` w JSON. `content_revision` i `card_source_blobs` w metryce pozwalają sprawdzić treść niezależnie od cutoff. Profil bieżący nie służy do automatycznego odgrywania wcześniejszych lat.

Po zmianie kart uruchom `python scripts/synchronizuj_profile.py` z katalogu RPG-Archiwum; sprawdź `--check`. Skrypt przenosi sekcje nadrzędnego profilu do JSON, zachowując zapisane fakty i ID, oraz sprawdza wszystkie karty. Przeglądarkę należy potem odświeżyć i opublikować osobno. Sam zapis karty nie aktualizuje innej kopii.
