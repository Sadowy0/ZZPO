# Opracowanie projektu - Planowanie diety

## 1. Streszczenie
Cel projektu: przygotowac prosta aplikacje do planowania tygodniowej diety.

Typ systemu:
- samodzielna aplikacja konsolowa (CLI),
- logika obiektowa i dane zapisane w plikach JSON,
- architektura modulowa, latwa do testowania,
- mozliwosc rozbudowy do interfejsu webowego.

Techniki projektowe:
- kompozycja obiektow (WeeklyPlan sklada sie z DailyPlan, DailyPlan sklada sie z Meal),
- separacja odpowiedzialnosci (models, repository, services, cli),
- prosty wzorzec Repository,
- testy jednostkowe w pytest.

Jezyk i narzedzia:
- Python 3.10+,
- pytest,
- Mermaid do diagramow UML.

## 2. Wstepny opis slowny
Uzytkownik podaje dane profilu: wiek, mase, wzrost, plec, aktywnosc i cel zywieniowy.
System oblicza dzienne zapotrzebowanie kaloryczne oraz orientacyjny cel makroskladnikow.
Nastepnie generuje plan na 7 dni na podstawie bazy posilkow i preferencji dietetycznych.

Uzytkownik moze:
- obejrzec podsumowanie calego tygodnia,
- sprawdzic szczegoly wybranego dnia,
- wygenerowac liste zakupow,
- wyeksportowac plan do JSON.

## 3. Slownik pojec
- UserProfile: dane uzytkownika i jego preferencje.
- Nutrition: wartosci odzywcze (kcal, bialko, tluszcz, weglowodany).
- Meal: pojedynczy posilek z tagami i skladnikami.
- DailyPlan: plan posilkow jednego dnia.
- WeeklyPlan: plan posilkow na 7 dni.
- MealRepository: odczyt danych posilkow z JSON.
- NutritionService: obliczenia kalorii i makro.
- MealPlannerService: budowa planu dziennego i tygodniowego.
- ShoppingListService: agregacja skladnikow do listy zakupow.
- PlanExporter: zapis planu do pliku JSON.

## 4. Analiza wymagan uzytkownika
Glowny scenariusz:
1. Uzytkownik uruchamia aplikacje.
2. Wybiera opcje generowania planu.
3. Podaje dane profilu i preferencje.
4. System tworzy plan tygodniowy.
5. Uzytkownik przeglada podsumowanie i szczegoly dni.
6. Uzytkownik opcjonalnie pobiera liste zakupow i eksportuje plan.

Scenariusze poboczne:
- Za malo posilkow dla wybranych preferencji: system zwraca czytelny komunikat bledu.
- Proba podgladu bez wygenerowanego planu: system informuje, ze najpierw trzeba utworzyc plan.
- Niepoprawne dane wejsciowe: system prosi o ponowne podanie wartosci.

## 5. Modele systemu (UML)
- Diagram klas: docs/uml_class_diagram.mmd
- Diagram sekwencji: docs/uml_sequence_diagram.mmd

Komentarz projektowy:
- Logika domenowa jest odseparowana od interfejsu uzytkownika.
- Services sa niezalezne od sposobu prezentacji i moga byc uzyte takze w wersji web.
- Repozytorium izoluje format danych od logiki aplikacji.

## 6. Kwestie implementacyjne i organizacja kodu
Struktura projektu:
- src/diet_planner/models.py - klasy domenowe,
- src/diet_planner/repository.py - odczyt danych,
- src/diet_planner/services.py - obliczenia i planowanie,
- src/diet_planner/cli.py - interfejs tekstowy,
- tests/test_services.py - testy jednostkowe,
- data/meals.json - baza przykladowych posilkow.

Automatyzacja uruchamiania:
- skrypt scripts/uruchom.sh: tworzy venv, instaluje zaleznosci i uruchamia aplikacje,
- skrypt scripts/testy.sh: uruchamia testy.

## 7. Organizacja pracy zespolu 4-osobowego
Osoba 1 - analiza i architektura:
- odpowiada za wymagania, slownik pojec i model klas,
- pilnuje spojnosci miedzy raportem i kodem,
- prezentuje decyzje projektowe na konsultacjach.

Osoba 2 - logika biznesowa:
- implementuje obliczenia kalorii i makro,
- implementuje algorytm budowy planu dnia i tygodnia,
- tlumaczy ograniczenia algorytmu i scenariusze brzegowe.

Osoba 3 - interfejs i integracja:
- prowadzi warstwe CLI,
- laczy przeplyw uzytkownika z logika i repozytorium,
- odpowiada za eksport JSON i wygodne uruchamianie skryptami.

Osoba 4 - testy i dokumentacja:
- przygotowuje testy jednostkowe,
- domyka raport i diagram sekwencji,
- prowadzi finalna kontrole jakosci i gotowosci do oddania.

Wspolna zasada zespolu:
- kazda osoba zna cala architekture,
- kazda osoba umie odtworzyc glowny scenariusz w aplikacji,
- kazda osoba ma przygotowana 2-minutowa czesc prezentacji.

### 7.1 Miniharmonogram (kto i kiedy)
Plan bazowy na 4 tygodnie od 15.04.2026.

| Tydzien | Kiedy | Osoba 1 | Osoba 2 | Osoba 3 | Osoba 4 | Efekt tygodnia |
|---|---|---|---|---|---|---|
| 1 | 15.04-21.04 | Wymagania, slownik, szkic UML klas | Szkic logiki kalorii i makro | Szkic CLI i przeplywu menu | Plan testow i szkielet testow | M1: uzgodniony model i uruchamialne menu |
| 2 | 22.04-28.04 | Final UML klas i decyzje projektowe | Implementacja planera tygodniowego | Integracja CLI z services i walidacja wejsc | Testy logiki i scenariuszy brzegowych | M2: dzialajace generowanie planu |
| 3 | 29.04-05.05 | Kontrola spojnosci raport-kod | Stabilizacja algorytmu i poprawki | Lista zakupow, eksport JSON, skrypty | Regresja i rozszerzenie testow | M3: pelny scenariusz end-to-end |
| 4 | 06.05-12.05 | Domkniecie sekcji analitycznych | Finalne poprawki logiki | Finalne poprawki UX CLI | Finalny raport i checklista oddania | M4: wersja gotowa do oddania |

Punkty kontrolne:
- 21.04: review M1,
- 28.04: review M2,
- 05.05: review M3,
- 12.05: proba generalna przed oddaniem.

## 8. Podsumowanie i dyskusja krytyczna
Mocne strony:
- przejrzysty kod i prosty podzial odpowiedzialnosci,
- sensowna logika biznesowa jak na projekt studencki,
- testy i dokumentacja wspierajace obrone projektu.

Ograniczenia:
- brak dokladnych gramatur i porcji,
- brak walidacji medycznej,
- brak interfejsu graficznego.

Kierunki rozwoju:
- dokladniejsze modele skladnikow i porcji,
- uwzglednienie alergii i budzetu,
- webowy panel uzytkownika.

## 9. Wykaz materialow zrodlowych
- dokument zajec Zaawansowane zagadnienia projektowania obiektowego,
- opis wzoru Mifflin-St Jeor,
- dokumentacja Python i pytest.
