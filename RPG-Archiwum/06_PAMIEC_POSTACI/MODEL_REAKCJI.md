# Pamięć rozmów, przekonania i głosy

Źródłem opracowanych wpisów jest [model_reakcji.json](model_reakcji.json). `synchronizuj_profile.py` przypisuje je do wszystkich 131 kart w JSON przez `reaction_state`. Puste listy oznaczają brak opracowanych wpisów, a nie amnezję, brak zdarzenia lub brak własnego zdania. Nie jest to pełny opis psychiki całej obsady.

## Aktualizacja

Zachowuj istniejące identyfikatory. Dodaj źródło każdej zmiany, jej moment i zakres. Rozpatrz późniejsze korekty oraz rozmowę po końcu archiwum. Ten plik opisuje wyłącznie kampanię Hogwarts Jamesa i Hermiony do wskazanego cutoff; nie przenoś go do świata ślubu z Luną. Daty publikacji nie są czasem sceny.

- `conversation`: temat, uczestnicy, źródłowa odpowiedź lub decyzja, status, to co czeka i powód powrotu. Statusy: OTWARTE, ODPOWIEDZIANE, PRZYJĘTE, ODŁOŻONE, PLAN, ZASTĄPIONE. Odpowiedź nie jest zgodą, odłożenie nie usuwa emocji, plan nie jest wykonaniem. Oczekująca odpowiedź Jamesa pozostaje jego decyzją.
- `beliefs`: właściciel, własne przekonanie albo przytoczona cudza opinia, treść, podstawa, wyrażona pewność, moment, odbiorcy i późniejsza zmiana. `world_status`: POTWIERDZONE, NIEZWERYFIKOWANE, SPRZECZNE_Z_FAKTEM, SPROSTOWANE. Osobno `lifecycle`: AKTUALNE_W_OSTATNIM_ŹRÓDLE lub HISTORYCZNE. Sprostowanie musi mieć nowe źródło i drogę doręczenia tej osobie. Nie uznawaj każdej wypowiedzi za przekonanie ani błędu narratora za intencjonalną omyłkę NPC. Niepewność postaci może dotyczyć faktu znanego narratorowi.
- `voice`: krótka sprawdzona próbka, osoba, kontekst, okres, źródło, interpretacja sposobu reagowania i ograniczenia. Cytat musi występować w źródle; interpretacja nie jest cytatem ani nowym faktem świata. Próbka kampanii nie dowodzi zgodności z kanonem i nie zastępuje karty wieku. Nie kopiuj całej sceny, refrenu, błędu lub odrzuconej wersji. Nie wymyślaj próbek dla zapełnienia wszystkich pól.

`sources` zawiera rzeczywiste ID, `as_of` ostatni moment odczytany dla tego wpisu. `characters` przypisuje wpis do kart, a `known_to` w przekonaniach opisuje odbiorców wypowiedzi, nie to, kto przyjął przekonanie za prawdę. Przy prywatnym przekonaniu nie dopisuj odbiorców bez podstawy. `changed_by` wskazuje późniejsze zdarzenie sprostowania; nie zmieniaj historii wstecz.

Przy nowej części sprawdź aktualność dotychczasowych wpisów i zmień metrykę razem z bazą; nie podnoś samego cutoff bez przeglądu zmian. Odśwież profile poleceniami `python scripts/synchronizuj_profile.py` i `python scripts/synchronizuj_profile.py --check`, następnie `python scripts/sprawdz_reakcje.py`. Odśwież i opublikuj prywatną przeglądarkę osobno. Nie obiecuj automatycznej synchronizacji czatów.

Sprawdziany w `07_SPRAWDZIANY` służą ocenie narracji. Ich polecenia i odpowiedzi próbne nie są historią kampanii. Na żądanie „sprawdź scenę” krótko oddziel odczytane źródła, istotne ustalenia, wynik kontroli i lukę lub poprawkę. Odczytu wykonanego podczas kontroli nie przypisuj wstecz poprzedniej odpowiedzi. Nie ujawniaj ukrytego toku rozumowania ani niezamówionych sekretów.
