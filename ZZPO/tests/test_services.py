from datetime import date
from pathlib import Path

import pytest

from diet_planner.models import ActivityLevel, Gender, Goal, UserProfile
from diet_planner.repository import MealRepository
from diet_planner.services import MealPlannerService, NutritionService, ShoppingListService

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "meals.json"


def build_profile(**kwargs: object) -> UserProfile:
    base = {
        "age": 23,
        "height_cm": 178,
        "weight_kg": 76.0,
        "gender": Gender.MALE,
        "activity_level": ActivityLevel.MODERATE,
        "goal": Goal.MAINTAIN,
        "dietary_preferences": set(),
        "daily_meals": 4,
    }
    base.update(kwargs)
    return UserProfile(**base)


def test_daily_calories_reflect_goal_adjustment() -> None:
    nutrition = NutritionService()

    profile_lose = build_profile(goal=Goal.LOSE)
    profile_gain = build_profile(goal=Goal.GAIN)

    calories_lose = nutrition.estimate_daily_calories(profile_lose)
    calories_gain = nutrition.estimate_daily_calories(profile_gain)

    assert calories_lose < calories_gain


def test_create_weekly_plan_has_7_days_and_meals() -> None:
    planner = MealPlannerService(MealRepository(DATA_PATH), rng_seed=1)
    profile = build_profile()

    plan = planner.create_weekly_plan(profile, start_day=date(2026, 4, 13))

    assert len(plan.days) == 7
    assert all(len(day.meals) == profile.daily_meals for day in plan.days)


def test_vegetarian_preference_filters_meals() -> None:
    planner = MealPlannerService(MealRepository(DATA_PATH), rng_seed=1)
    profile = build_profile(dietary_preferences={"vegetarian"})

    plan = planner.create_weekly_plan(profile, start_day=date(2026, 4, 13))

    for day in plan.days:
        for meal in day.meals:
            assert "vegetarian" in meal.tags


def test_shopping_list_contains_aggregated_items() -> None:
    planner = MealPlannerService(MealRepository(DATA_PATH), rng_seed=3)
    shopping = ShoppingListService()

    plan = planner.create_weekly_plan(build_profile(), start_day=date(2026, 4, 13))
    result = shopping.build_for_week(plan)

    assert result
    assert all(count > 0 for count in result.values())


def test_error_when_not_enough_meals_for_preferences() -> None:
    planner = MealPlannerService(MealRepository(DATA_PATH), rng_seed=1)
    profile = build_profile(dietary_preferences={"vegetarian", "high-protein"}, daily_meals=5)

    with pytest.raises(ValueError):
        planner.create_weekly_plan(profile, start_day=date(2026, 4, 13))
