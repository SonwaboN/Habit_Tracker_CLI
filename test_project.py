import pytest
from datetime import datetime, timedelta
from habit import Habit
import analytics

def test_habit_creation():
    """
    Test that a habit is initialized with correct default values.
    """
    h = Habit("Run", "daily")
    assert h.name == "Run"
    assert h.periodicity == "daily"
    assert isinstance(h.creation_date, str)  # Should be an ISO format string
    assert h.completed_dates == []

def test_check_off():
    """
    Test that checking off a habit adds the current timestamp.
    """
    h = Habit("Drink Water", "daily")
    h.check_off()
    
    assert len(h.completed_dates) == 1
    # Verify it is a valid ISO string
    assert isinstance(h.completed_dates[0], str)

def test_streak_calculation_daily():
    """
    Test streak calculation for consecutive days.
    """
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    day_before = today - timedelta(days=2)
    
    # Create a list of ISO formatted strings
    dates = [
        today.isoformat(),
        yesterday.isoformat(),
        day_before.isoformat()
    ]
    
    # Pass data to the pure function in analytics module
    streak = analytics.calculate_streak(dates, "daily")
    
    # Should be 3 days in a row
    assert streak == 3

def test_streak_broken_daily():
    """
    Test that a missing day breaks the streak.
    """
    today = datetime.now()
    # Skip yesterday, go straight to 2 days ago
    two_days_ago = today - timedelta(days=2)
    
    dates = [
        today.isoformat(),
        two_days_ago.isoformat()
    ]
    
    streak = analytics.calculate_streak(dates, "daily")
    
    # Streak should be 1 (just today), because the chain was broken
    assert streak == 1

def test_streak_calculation_weekly():
    """
    Test streak calculation for consecutive weeks.
    """
    today = datetime.now()
    last_week = today - timedelta(weeks=1)
    
    dates = [
        today.isoformat(),
        last_week.isoformat()
    ]
    
    streak = analytics.calculate_streak(dates, "weekly")
    assert streak == 2

def test_filter_by_periodicity():
    """
    Test filtering habits by their type.
    """
    habits = [
        Habit("Daily Run", "daily"),
        Habit("Weekly Swim", "weekly"),
        Habit("Daily Read", "daily")
    ]
    
    daily_habits = analytics.get_habits_by_periodicity(habits, "daily")
    weekly_habits = analytics.get_habits_by_periodicity(habits, "weekly")
    
    assert len(daily_habits) == 2
    assert len(weekly_habits) == 1
    assert daily_habits[0].name == "Daily Run"