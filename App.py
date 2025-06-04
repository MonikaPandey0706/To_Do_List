#Intialized a Python File

class Task:
    """
    Represents a single academic task (e.g., assignment, project, study session).
    """
    def __init__(self, task_id, title, description, due_date, priority="Medium", status="Pending"):
        """
        Initializes a new Task object.
        Args:
            task_id (int): Unique identifier for the task.
            title (str): The title of the task.
            description (str): A brief description of the task.
            due_date (str): The due date of the task (YYYY-MM-DD).
            priority (str): "High", "Medium", or "Low". Defaults to "Medium".
            status (str): "Pending" or "Completed". Defaults to "Pending".
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if not title or not description or not due_date:
            raise ValueError("Title, description, and due date are required.")
        if not validate_priority(priority):
            raise ValueError(f"Invalid priority: {priority}. Must be one of {', '.join(ALLOWED_PRIORITIES)}.")
        if not validate_status(status):
            raise ValueError(f"Invalid status: {status}. Must be one of {', '.join(ALLOWED_STATUSES)}.")

        self.id = task_id
        self.title = title.strip()
        self.description = description.strip()
        self.due_date = due_date  # Stored as YYYY-MM-DD string
        self.priority = priority.capitalize() # Standardize capitalization
        self.status = status.capitalize() # Standardize capitalization
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        """Converts the Task object to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at
        }
    

    @staticmethod
    def from_dict(task_dict):
        """Creates a Task object from a dictionary (e.g., loaded from JSON)."""
        return Task(
            task_dict['id'],
            task_dict['title'],
            task_dict['description'],
            task_dict['due_date'],
            task_dict.get('priority', "Medium"), # Handle older entries without priority
            task_dict.get('status', "Pending")   # Handle older entries without status
        )
    

    def get_priority_color(self):
        """Returns the ANSI color code based on priority."""
        if self.priority == "High":
            return COLOR_RED
        elif self.priority == "Medium":
            return COLOR_YELLOW
        elif self.priority == "Low":
            return COLOR_BLUE
        return COLOR_RESET
    

    def get_status_color(self):
        """Returns the ANSI color code based on status."""
        if self.status == "Completed":
            return COLOR_GREEN
        return COLOR_YELLOW # Pending tasks can be yellow
    

    def display(self):
        """Prints the task's details to the console in a formatted way."""
        due_date_obj = datetime.strptime(self.due_date, '%Y-%m-%d')
        today = datetime.now()
        days_left = (due_date_obj - today).days

        status_color = self.get_status_color()
        priority_color = self.get_priority_color()

        due_status_text = ""
        if self.status == "Pending":
            if days_left < 0:
                due_status_text = f" ({COLOR_RED}OVERDUE!{COLOR_RESET})"
            elif days_left == 0:
                due_status_text = f" ({COLOR_RED}Due Today!{COLOR_RESET})"
            elif days_left <= 3:
                due_status_text = f" ({COLOR_YELLOW}{days_left} day(s) left!{COLOR_RESET})"
            else:
                due_status_text = f" ({days_left} days left)"
        else:
            due_status_text = " (Completed)"


        print(f"{COLOR_CYAN}--- Task ID: {self.id} | {self.title}{COLOR_RESET} ---")
        print(f"  Description: {self.description}")
        print(f"  Due Date: {self.due_date}{due_status_text}")
        print(f"  Priority: {priority_color}{self.priority}{COLOR_RESET}")
        print(f"  Status: {status_color}{self.status}{COLOR_RESET}")
        print(f"  Created At: {self.created_at}")
        print("-" * 40)

