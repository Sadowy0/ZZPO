# Planowanie Diety - Projekt Studencki

Repozytorium zawiera realizacje tematu nr 10: planowanie diety.
Zakres projektu jest celowo "studencki": aplikacja jest dosc rozbudowana, aby pokazac dobre podejscie obiektowe, ale jednoczesnie pozostaje prosta do wyjasnienia podczas konsultacji.

## Cel projektu
Stworzenie aplikacji, ktora generuje tygodniowy plan posilkow na podstawie profilu uzytkownika:
- wiek, masa ciala, wzrost, plec,
- poziom aktywnosci,
- cel zywieniowy (redukcja, utrzymanie, masa),
- preferencje dietetyczne (np. vegetarian, quick, high-protein).

## Najwazniejsze funkcje
- szacowanie dziennego zapotrzebowania kalorycznego,
- obliczanie orientacyjnego celu makroskladnikow,
- generowanie planu na 7 dni,
- filtrowanie posilkow po preferencjach,
- tworzenie listy zakupow,
- eksport planu do pliku JSON.

## Architektura
Projekt jest podzielony na warstwy:
- models: obiekty domenowe (UserProfile, Meal, DailyPlan, WeeklyPlan, Nutrition),
- repository: odczyt danych o posilkach z JSON,
- services: logika biznesowa i algorytmy,
- cli: interfejs tekstowy dla uzytkownika.

## Szczegolowy podzial rol dla 4 osob
Kazda osoba ma swoj glowny obszar, ale musi znac calosc projektu, aby umiec odpowiedziec na pytania prowadzacego.

### Osoba 1 - Analityk i architekt domeny
Zakres odpowiedzialnosci:
- przygotowanie opisu problemu i slownika pojec,
- definicja modelu klas i relacji (pojecia domenowe),
- utrzymanie spojnosci miedzy wymaganiami a implementacja.

Co oddaje:
- opis sekcji 1-4 raportu,
- diagram klas UML,
- uzasadnienie decyzji projektowych.

Co ma umiec wyjasnic na konsultacjach:
- dlaczego takie klasy, a nie inne,
- gdzie jest kompozycja i odpowiedzialnosc klas,
- jakie byly alternatywy i dlaczego je odrzucono.

### Osoba 2 - Logika biznesowa i algorytm planowania
Zakres odpowiedzialnosci:
- obliczanie kalorii i makro,
- implementacja generowania planu dziennego i tygodniowego,
- obsluga warunkow brzegowych (np. za malo posilkow po filtrach).

Co oddaje:
- kod w services,
- opis algorytmu i reguly biznesowe,
- uzasadnienie uproszczen modelu.

Co ma umiec wyjasnic na konsultacjach:
- jak dziala wzor kalorii,
- jak dobierane sa posilki,
- jak aplikacja reaguje na brak danych.

### Osoba 3 - Interfejs CLI, dane i integracja
Zakres odpowiedzialnosci:
- przeplyw menu CLI,
- walidacja wejscia uzytkownika,
- integracja z repozytorium danych i eksportem JSON,
- skrypty uruchomieniowe.

Co oddaje:
- kod CLI i repozytorium,
- gotowe dane testowe w JSON,
- instrukcje uruchamiania.

Co ma umiec wyjasnic na konsultacjach:
- jak wyglada scenariusz od uruchomienia do eksportu,
- jakie dane sa wymagane,
- gdzie i jak mozna rozszerzyc aplikacje.

### Osoba 4 - Testy, jakosc i dokumentacja koncowa
Zakres odpowiedzialnosci:
- przygotowanie i utrzymanie testow,
- weryfikacja stabilnosci funkcji,
- domkniecie raportu, diagramu sekwencji i opisu ograniczen.

Co oddaje:
- testy jednostkowe,
- sekcje raportu o implementacji i podsumowaniu,
- checkliste pod oddanie.

Co ma umiec wyjasnic na konsultacjach:
- co i dlaczego testujemy,
- jakie sa ryzyka i ograniczenia projektu,
- jak projekt przygotowano do dalszej rozbudowy.

## Miniharmonogram (kto i kiedy)
Plan bazowy na 4 tygodnie od 15.04.2026.

| Tydzien | Kiedy | Osoba 1 (analiza i architektura) | Osoba 2 (logika biznesowa) | Osoba 3 (CLI i integracja) | Osoba 4 (testy i dokumentacja) | Kamien milowy |
|---|---|---|---|---|---|---|
| 1 | 15.04-21.04 | Slownik pojec, wymagania, szkic diagramu klas | Szkic obliczen kalorii i makro, prototyp planera dnia | Szkic menu CLI, przeplyw uzytkownika, repozytorium danych | Przygotowanie planu testow i struktury testow | M1: uzgodniony model i dzialajace menu |
| 2 | 22.04-28.04 | Finalizacja diagramu klas i opis decyzji projektowych | Implementacja create_weekly_plan i warunkow brzegowych | Integracja CLI z services, poprawna walidacja wejscia | Testy jednostkowe dla obliczen i planowania | M2: generowanie planu tygodniowego dziala |
| 3 | 29.04-05.05 | Przeglad spojnosci raportu z kodem | Korekty algorytmu i stabilizacja logiki | Lista zakupow, eksport JSON, skrypty uruchamiania | Rozszerzenie testow i regresja po integracji | M3: pelny przeplyw od profilu do eksportu |
| 4 | 06.05-12.05 | Domkniecie sekcji analitycznych i UML do oddania | Finalne poprawki logiki i przygotowanie odpowiedzi na pytania | Finalne poprawki UX CLI i komunikatow | Finalny raport, sekcja krytyczna, checklista oddania | M4: wersja finalna gotowa do konsultacji/oddania |

### Punkty kontrolne (obowiazkowe)
- 21.04: kontrola M1 i podzial poprawek.
- 28.04: kontrola M2, decyzja o zamrozeniu API modulow.
- 05.05: kontrola M3, test przejscia scenariusza end-to-end.
- 12.05: proba generalna prezentacji i finalne poprawki.

### Zasada odpowiedzialnosci
- Kazde zadanie ma jednego wlasciciela (owner), ale minimum jedna osoba robi review.
- Blokery zglaszane tego samego dnia na wspolnym kanale komunikacji.
- Jesli termin tygodniowy jest zagrozony, priorytetem jest stabilnosc dzialajacego MVP.

## Jak uruchomic projekt skryptem
Najprosciej:
1. Przejdz do katalogu projektu.
2. Uruchom:

   ./scripts/uruchom.sh

Skrypt automatycznie:
- tworzy lokalne srodowisko .venv (jesli go nie ma),
- instaluje zaleznosci,
- uruchamia aplikacje CLI.

## Jak uruchomic testy skryptem
Uruchom:

./scripts/testy.sh

## Dlaczego ten projekt jest dobry na 4.0-4.5
- ma czytelna architekture i sensowny podzial odpowiedzialnosci,
- jest wystarczajaco zlozony, by pokazac znajomosc OOP,
- daje sie szybko pokazac i obronic krok po kroku,
- zawiera testy i dokumentacje, wiec wyglada dojrzale mimo prostoty.

## Dalszy kierunek po konsultacjach
- dokladniejsze porcje i gramatury skladnikow,
- bardziej realistyczne ograniczenia (alergie, budzet),
- ewentualny frontend webowy jako kolejny etap.
