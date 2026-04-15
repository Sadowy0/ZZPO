from __future__ import annotations

from datetime import date
from pathlib import Path

from .models import ActivityLevel, Gender, Goal, UserProfile, WeeklyPlan
from .repository import MealRepository
from .services import MealPlannerService, PlanExporter, ShoppingListService

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT_DIR / "data" / "meals.json"

ACTIVITY_OPTIONS: list[tuple[str, ActivityLevel]] = [
    ("Siedzacy (1.2)", ActivityLevel.SEDENTARY),
    ("Lekka aktywnosc (1.375)", ActivityLevel.LIGHT),
    ("Umiarkowana aktywnosc (1.55)", ActivityLevel.MODERATE),
    ("Wysoka aktywnosc (1.725)", ActivityLevel.HIGH),
]

GOAL_OPTIONS: list[tuple[str, Goal]] = [
    ("Redukcja masy", Goal.LOSE),
    ("Utrzymanie masy", Goal.MAINTAIN),
    ("Budowanie masy", Goal.GAIN),
]

PREFERENCE_OPTIONS: list[tuple[str, str]] = [
    ("Wegetarianska", "vegetarian"),
    ("Wysokobialkowa", "high-protein"),
    ("Szybkie posilki", "quick"),
]


def ask_int(prompt: str, minimum: int, maximum: int) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if minimum <= value <= maximum:
                return value
        except ValueError:
            pass
        print(f"Podaj liczbe calkowita z zakresu {minimum}-{maximum}.")


def ask_float(prompt: str, minimum: float, maximum: float) -> float:
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            value = float(raw)
            if minimum <= value <= maximum:
                return value
        except ValueError:
            pass
        print(f"Podaj liczbe z zakresu {minimum}-{maximum}.")


def ask_gender() -> Gender:
    value = ask_int("Plec [1=mezczyzna, 2=kobieta]: ", 1, 2)
    return Gender.MALE if value == 1 else Gender.FEMALE


def ask_activity() -> ActivityLevel:
    print("Poziom aktywnosci:")
    for index, (label, _) in enumerate(ACTIVITY_OPTIONS, start=1):
        print(f"  {index}. {label}")
    choice = ask_int("Wybierz aktywnosc: ", 1, len(ACTIVITY_OPTIONS))
    return ACTIVITY_OPTIONS[choice - 1][1]


def ask_goal() -> Goal:
    print("Cel:")
    for index, (label, _) in enumerate(GOAL_OPTIONS, start=1):
        print(f"  {index}. {label}")
    choice = ask_int("Wybierz cel: ", 1, len(GOAL_OPTIONS))
    return GOAL_OPTIONS[choice - 1][1]


def ask_preferences() -> set[str]:
    print("Preferencje (numery oddziel przecinkami, Enter = brak):")
    for index, (label, tag) in enumerate(PREFERENCE_OPTIONS, start=1):
        print(f"  {index}. {label} [{tag}]")

    raw = input("Wybierz preferencje: ").strip()
    if not raw:
        return set()

    selected: set[str] = set()
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        try:
            idx = int(token)
            if 1 <= idx <= len(PREFERENCE_OPTIONS):
                selected.add(PREFERENCE_OPTIONS[idx - 1][1])
        except ValueError:
            continue
    return selected


def meal_type_label(meal_type: str) -> str:
    labels = {
        "breakfast": "sniadanie",
        "lunch": "obiad",
        "dinner": "kolacja",
        "snack": "przekaska",
    }
    return labels.get(meal_type, meal_type)


def build_profile() -> UserProfile:
    print("\nTworzenie profilu uzytkownika")
    age = ask_int("Wiek: ", 15, 90)
    height_cm = ask_int("Wzrost [cm]: ", 130, 220)
    weight_kg = ask_float("Masa [kg]: ", 35, 250)
    gender = ask_gender()
    activity_level = ask_activity()
    goal = ask_goal()
    daily_meals = ask_int("Liczba posilkow dziennie (3-6): ", 3, 6)
    dietary_preferences = ask_preferences()

    return UserProfile(
        age=age,
        height_cm=height_cm,
        weight_kg=weight_kg,
        gender=gender,
        activity_level=activity_level,
        goal=goal,
        dietary_preferences=dietary_preferences,
        daily_meals=daily_meals,
    )


class DietPlannerCLI:
    def __init__(self) -> None:
        repository = MealRepository(DATA_PATH)
        self._planner = MealPlannerService(repository)
        self._shopping = ShoppingListService()
        self._current_plan: WeeklyPlan | None = None

    def run(self) -> None:
        while True:
            print("\n=== Planowanie Diety ===")
            print("1. Generuj plan tygodniowy")
            print("2. Pokaz podsumowanie tygodnia")
            print("3. Pokaz szczegoly dnia")
            print("4. Pokaz liste zakupow")
            print("5. Eksportuj plan do JSON")
            print("0. Wyjdz")

            choice = ask_int("Wybierz opcje: ", 0, 5)
            if choice == 1:
                self.generate_plan()
            elif choice == 2:
                self.show_week_summary()
            elif choice == 3:
                self.show_day_details()
            elif choice == 4:
                self.show_shopping_list()
            elif choice == 5:
                self.export_plan()
            else:
                print("Koniec programu.")
                return

    def generate_plan(self) -> None:
        profile = build_profile()
        try:
            self._current_plan = self._planner.create_weekly_plan(profile, start_day=date.today())
            print("Plan tygodniowy wygenerowany.")
            self.show_week_summary()
        except ValueError as error:
            print(f"Nie mozna wygenerowac planu: {error}")

    def show_week_summary(self) -> None:
        if self._current_plan is None:
            print("Najpierw wygeneruj plan.")
            return

        print("\nPodsumowanie tygodnia")
        print(
            f"Cel makro: {self._current_plan.macro_target.calories} kcal, "
            f"B {self._current_plan.macro_target.protein_g} g, "
            f"T {self._current_plan.macro_target.fat_g} g, "
            f"W {self._current_plan.macro_target.carbs_g} g"
        )
        for index, day in enumerate(self._current_plan.days, start=1):
            total = day.total_nutrition
            print(
                f"{index}. {day.day.isoformat()} | cel {day.target_calories} kcal | "
                f"rzeczywiscie {total.calories} kcal"
            )

    def show_day_details(self) -> None:
        if self._current_plan is None:
            print("Najpierw wygeneruj plan.")
            return

        day_number = ask_int("Numer dnia (1-7): ", 1, 7)
        day = self._current_plan.days[day_number - 1]

        print(f"\nSzczegoly dnia {day.day.isoformat()}")
        for meal in day.meals:
            print(
                f"- {meal.name} [{meal_type_label(meal.meal_type)}] | {meal.nutrition.calories} kcal "
                f"(B {meal.nutrition.protein_g}, T {meal.nutrition.fat_g}, W {meal.nutrition.carbs_g})"
            )

        total = day.total_nutrition
        print(
            f"Suma: {total.calories} kcal, "
            f"B {total.protein_g} g, T {total.fat_g} g, W {total.carbs_g} g"
        )

    def show_shopping_list(self) -> None:
        if self._current_plan is None:
            print("Najpierw wygeneruj plan.")
            return

        shopping_list = self._shopping.build_for_week(self._current_plan)
        print("\nLista zakupow")
        for item, count in shopping_list.items():
            print(f"- {item}: {count}")

    def export_plan(self) -> None:
        if self._current_plan is None:
            print("Najpierw wygeneruj plan.")
            return

        file_name = input("Nazwa pliku wyjsciowego [plan_diety.json]: ").strip() or "plan_diety.json"
        output_path = ROOT_DIR / file_name
        PlanExporter.save(self._current_plan, output_path)
        print(f"Plan zapisano do {output_path}")


def main() -> None:
    DietPlannerCLI().run()


if __name__ == "__main__":
    main()
