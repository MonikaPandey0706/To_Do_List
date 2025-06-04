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

