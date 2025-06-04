#Intialized a Python File

import json
import os
from datetime import datetime, timedelta

# --- Constants ---
# File to store task data.
TASKS_FILE = 'student_tasks.json'

# Allowed task priorities.
ALLOWED_PRIORITIES = ["High", "Medium", "Low"]

# Allowed task statuses.
ALLOWED_STATUSES = ["Pending", "Completed"]

# ANSI escape codes for text colors (for better readability in console)
# Reset color at the end of each print to avoid bleeding
COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[92m"  # For completed tasks, success messages
COLOR_YELLOW = "\033[93m" # For medium priority, warnings
COLOR_RED = "\033[91m"    # For high priority, overdue tasks, error messages
COLOR_BLUE = "\033[94m"   # For general info, menu
COLOR_CYAN = "\033[96m"   # For task titles

def clear_screen():
    """Clears the console screen for better readability."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_input(prompt, validation_func=None, error_message="Invalid input. Please try again."):
    """
    Prompts the user for input and validates it using an optional validation function.
    Args:
        prompt (str): The message to display to the user.
        validation_func (callable, optional): A function that takes the input
                                              and returns True if valid, False otherwise.
        error_message (str): The message to display if validation fails.
    Returns:
        str: The validated input.
    """
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print(f"{COLOR_YELLOW}Input cannot be empty. Please try again.{COLOR_RESET}")
            continue
        if validation_func:
            if validation_func(user_input):
                return user_input
            else:
                print(f"{COLOR_RED}{error_message}{COLOR_RESET}")
        else:
            return user_input

def get_valid_date(prompt, error_message="Invalid date format. Please use YYYY-MM-DD."):
    """
    Prompts for a date and validates its format.
    """
    while True:
        date_str = get_valid_input(prompt)
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print(f"{COLOR_RED}{error_message}{COLOR_RESET}")


def validate_priority(priority_str):
    """Validates if a string is one of the ALLOWED_PRIORITIES (case-insensitive)."""
    return priority_str.lower() in [p.lower() for p in ALLOWED_PRIORITIES]

def validate_status(status_str):
    """Validates if a string is one of the ALLOWED_STATUSES (case-insensitive)."""
    return status_str.lower() in [s.lower() for s in ALLOWED_STATUSES]


