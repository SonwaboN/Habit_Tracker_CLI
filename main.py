import json
import os
import questionary
from datetime import datetime, timedelta
from habit import Habit
import analytics

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        return [Habit(**h) for h in data]

def save_data(habits):
    with open(DATA_FILE, "w") as f:
        json.dump([h.to_dict() for h in habits], f, indent=4)

def generate_dummy_data():
    """
    Creates 5 predefined habits with 4 weeks of tracking data.
    Reqs: - 5 predefined habits, 4 weeks of data.
    """
    habits = []
    
    # Define habits
    names_daily = ["Drink Water", "Read Book", "Code Python"]
    names_weekly = ["Exercise", "Clean House"]
    
    # Generate 4 weeks of dates (last 28 days)
    end_date = datetime.now()
    dates_daily = [
        (end_date - timedelta(days=i)).isoformat() 
        for i in range(28)
    ]
    # Generate 4 weeks of weekly dates
    dates_weekly = [
        (end_date - timedelta(weeks=i)).isoformat() 
        for i in range(4)
    ]

    # Create Daily Habits with data
    for name in names_daily:
        h = Habit(name, "daily")
        h.completed_dates = dates_daily[:] # Copy the list
        habits.append(h)

    # Create Weekly Habits with data
    for name in names_weekly:
        h = Habit(name, "weekly")
        h.completed_dates = dates_weekly[:] # Copy the list
        habits.append(h)
        
    return habits

def main():
    habits = load_data()
    
    # If no data exists, load the 4-week dummy data
    if not habits:
        habits = generate_dummy_data()
        save_data(habits)
        print("Welcome! Created 5 sample habits with 4 weeks of history.")

    while True:
        choice = questionary.select(
            "What do you want to do?",
            choices=["Create Habit", "Check-off Habit", "Analyze", "Delete Habit", "Exit"]
        ).ask()

        if choice == "Create Habit":
            name = questionary.text("Habit Name:").ask()
            period = questionary.select("Periodicity:", choices=["daily", "weekly"]).ask()
            habits.append(Habit(name, period))
            save_data(habits)
            print(f"Created {name}!")

        elif choice == "Check-off Habit":
            if not habits:
                print("No habits to check off!")
                continue
            habit_name = questionary.select(
                "Which habit?",
                choices=[h.name for h in habits]
            ).ask()
            
            for h in habits:
                if h.name == habit_name:
                    h.check_off()
            save_data(habits)
            print(f"Checked off {habit_name}!")

        elif choice == "Analyze":
            if not habits:
                print("No data to analyze.")
                continue
            
            # Reqs: List all currently tracked habits
            print("\n--- All Habits ---")
            for h in habits:
                print(f"- {h.name} ({h.periodicity})")
            
            print("\n--- Longest Streak Overall ---")
            print(analytics.get_longest_streak_all(habits))
            
            # Reqs: Return longest run streak for a given habit
            selected_habit_name = questionary.select(
                "Check streak for specific habit:",
                choices=[h.name for h in habits]
            ).ask()
            
            selected_habit = next((h for h in habits if h.name == selected_habit_name), None)
            if selected_habit:
                streak = analytics.calculate_streak(selected_habit.completed_dates, selected_habit.periodicity)
                print(f"Current streak for {selected_habit.name}: {streak}")

        elif choice == "Delete Habit":
            # Reqs: Allow user to delete habits
            if not habits:
                print("No habits to delete.")
                continue
            habit_to_delete = questionary.select(
                "Which habit to delete?",
                choices=[h.name for h in habits]
            ).ask()
            
            # Filter out the deleted habit
            habits = [h for h in habits if h.name != habit_to_delete]
            save_data(habits)
            print(f"Deleted {habit_to_delete}.")

        elif choice == "Exit":
            print("Goodbye!")
            break
def test_habit_deletion():
    """
    Test that a habit can be successfully removed from a list of habits.
    """
    habits = [
        Habit("Read", "daily"),
        Habit("Run", "daily")
    ]
    
    # Simulate deletion
    habit_to_delete = "Run"
    habits = [h for h in habits if h.name != habit_to_delete]
    
    assert len(habits) == 1
    assert habits[0].name == "Read"

def test_four_week_fixture_daily_streak():
    """
    Test streak calculation using 4 weeks (28 days) of predefined time-series data.
    """
    today = datetime.now()
    # Generate 28 consecutive days of check-offs
    four_weeks_data = [(today - timedelta(days=i)).isoformat() for i in range(28)]
    
    # Test functional analytics with this fixture
    streak = analytics.calculate_streak(four_weeks_data, "daily")
    
    # The streak should be exactly 28
    assert streak == 28

def test_four_week_fixture_weekly_streak():
    """
    Test streak calculation using 4 weeks of predefined weekly data.
    """
    today = datetime.now()
    # Generate 4 consecutive weeks of check-offs
    four_weeks_data = [(today - timedelta(weeks=i)).isoformat() for i in range(4)]
    
    streak = analytics.calculate_streak(four_weeks_data, "weekly")
    
    # The streak should be exactly 4 weeks
    assert streak == 4
if __name__ == "__main__":
    main()