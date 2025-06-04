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
