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

class StudyManager:
    """
    Manages the collection of academic tasks.
    """
    def __init__(self, data_file=TASKS_FILE):
        self.data_file = data_file
        self.tasks = []
        self._next_id = 1
        self._load_tasks()


    def _load_tasks(self):
        """Loads task data from the JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    tasks_data = json.load(f)
                    self.tasks = [Task.from_dict(d) for d in tasks_data]
                    if self.tasks:
                        self._next_id = max(task.id for task in self.tasks) + 1
                    else:
                        self._next_id = 1
                print(f"{COLOR_GREEN}Loaded {len(self.tasks)} tasks from '{self.data_file}'.{COLOR_RESET}")
            except json.JSONDecodeError:
                print(f"{COLOR_RED}Error reading '{self.data_file}'. File might be corrupted. Starting with empty collection.{COLOR_RESET}")
                self.tasks = []
                self._next_id = 1
            except Exception as e:
                print(f"{COLOR_RED}An unexpected error occurred while loading tasks: {e}{COLOR_RESET}")
                self.tasks = []
                self._next_id = 1
        else:
            print(f"{COLOR_YELLOW}No task data file found at '{self.data_file}'. Starting with empty collection.{COLOR_RESET}")


    def _save_tasks(self):
        """Saves the current task collection to the JSON file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=4, ensure_ascii=False)
            print(f"{COLOR_GREEN}Saved {len(self.tasks)} tasks to '{self.data_file}'.{COLOR_RESET}")
        except Exception as e:
            print(f"{COLOR_RED}Error saving tasks to '{self.data_file}': {e}{COLOR_RESET}")

    def add_task(self):
        """Prompts the user for task details and adds a new task."""
        clear_screen()
        print(f"\n{COLOR_BLUE}--- Add New Task ---{COLOR_RESET}")
        title = get_valid_input("Enter task title: ")
        description = input("Enter task description: ").strip()
        due_date = get_valid_date("Enter due date (YYYY-MM-DD): ")

        print(f"Available Priorities: {', '.join(ALLOWED_PRIORITIES)}")
        priority_str = get_valid_input("Enter priority (High, Medium, Low): ", validate_priority,
                                       f"Invalid priority. Please choose from: {', '.join(ALLOWED_PRIORITIES)}")
        priority = priority_str.capitalize()

        try:
            new_task = Task(self._next_id, title, description, due_date, priority=priority)
            self.tasks.append(new_task)
            self._next_id += 1
            self._save_tasks()
            print(f"\n{COLOR_GREEN}Task added successfully!{COLOR_RESET}")
            new_task.display()
        except ValueError as e:
            print(f"{COLOR_RED}\nError adding task: {e}{COLOR_RESET}")
        input(f"\n{COLOR_BLUE}Press Enter to continue...{COLOR_RESET}")


    def view_tasks(self, filter_status=None, sort_by="due_date"):
        """
        Displays tasks, optionally filtered by status and sorted.
        Args:
            filter_status (str, optional): "Pending" or "Completed" to filter.
            sort_by (str): "due_date", "priority", or "title".
        """

        clear_screen()
        print(f"\n{COLOR_BLUE}--- Your Tasks ---{COLOR_RESET}")
        if not self.tasks:
            print(f"{COLOR_YELLOW}You have no tasks recorded yet.{COLOR_RESET}")
            print("Consider adding some tasks!")
            input(f"\n{COLOR_BLUE}Press Enter to continue...{COLOR_RESET}")
            return


        filtered_tasks = self.tasks
        if filter_status:
            filtered_tasks = [t for t in self.tasks if t.status == filter_status.capitalize()]


        if not filtered_tasks:
            print(f"{COLOR_YELLOW}No {filter_status.lower()} tasks found.{COLOR_RESET}")
            input(f"\n{COLOR_BLUE}Press Enter to continue...{COLOR_RESET}")
            return
        

        # Sorting logic
        if sort_by == "due_date":
            # Sort pending tasks first by due date, then completed tasks
            pending_tasks = sorted([t for t in filtered_tasks if t.status == "Pending"], key=lambda t: datetime.strptime(t.due_date, '%Y-%m-%d'))
            completed_tasks = sorted([t for t in filtered_tasks if t.status == "Completed"], key=lambda t: datetime.strptime(t.due_date, '%Y-%m-%d'))
            sorted_tasks = pending_tasks + completed_tasks
        elif sort_by == "priority":
            priority_order = {"High": 1, "Medium": 2, "Low": 3}
            sorted_tasks = sorted(filtered_tasks, key=lambda t: priority_order.get(t.priority, 99))
        elif sort_by == "title":
            sorted_tasks = sorted(filtered_tasks, key=lambda t: t.title.lower())
        else:
            sorted_tasks = filtered_tasks # Default to unsorted if invalid sort_by

        for task in sorted_tasks:
            task.display()
        print(f"\n{COLOR_BLUE}Total Tasks: {len(filtered_tasks)}{COLOR_RESET}")
        input(f"\n{COLOR_BLUE}Press Enter to continue...{COLOR_RESET}")


    def update_task_status(self):
        """Allows user to change a task's status (e.g., mark as completed)."""
        clear_screen()
        print(f"\n{COLOR_BLUE}--- Update Task Status ---{COLOR_RESET}")
        self.view_tasks(filter_status="Pending") # Show only pending tasks to update

        if not any(t.status == "Pending" for t in self.tasks):
            print(f"{COLOR_YELLOW}No pending tasks to update.{COLOR_RESET}")
            input(f"\n{COLOR_BLUE}Press Enter to continue...{COLOR_RESET}")
            return
        

        task_id_str = get_valid_input("Enter the ID of the task to update status: ",
                                       lambda x: x.isdigit() and int(x) > 0,
                                       "Invalid ID. Please enter a positive number.")
        task_id = int(task_id_str)

        task_to_update = next((task for task in self.tasks if task.id == task_id), None)


        if not task_to_update:
            print(f"{COLOR_RED}Task with ID '{task_id}' not found.{COLOR_RESET}")
            input(f"\n{COLOR_BLUE}Press Enter to continue...{COLOR_RESET}")
            return


        print(f"Current Status for '{task_to_update.title}': {task_to_update.status}")
        print(f"Available Statuses: {', '.join(ALLOWED_STATUSES)}")
        new_status_str = get_valid_input("Enter new status (Pending/Completed): ", validate_status,
                                         f"Invalid status. Choose from: {', '.join(ALLOWED_STATUSES)}")
        new_status = new_status_str.capitalize()

        if task_to_update.status == new_status:
            print(f"{COLOR_YELLOW}Task already has this status.{COLOR_RESET}")
        else:
            task_to_update.status = new_status
            self._save_tasks()
            print(f"{COLOR_GREEN}\nTask '{task_to_update.title}' status updated to '{new_status}'.{COLOR_RESET}")
            task_to_update.display()
        input(f"\n{COLOR_BLUE}Press Enter to continue...{COLOR_RESET}")


    def delete_task(self):
        """Deletes a task from the collection based on its ID."""
        clear_screen()
        print(f"\n{COLOR_BLUE}--- Delete Task ---{COLOR_RESET}")
        if not self.tasks:
            print(f"{COLOR_YELLOW}No tasks to delete. Your task list is empty.{COLOR_RESET}")
            input(f"\n{COLOR_BLUE}Press Enter to continue...{COLOR_RESET}")
            return
        

        self.view_tasks() # Show current tasks to help user pick ID
        task_id_str = get_valid_input("Enter the ID of the task to delete: ",
                                       lambda x: x.isdigit() and int(x) > 0,
                                       "Invalid ID. Please enter a positive number.")
        task_id = int(task_id_str)


        task_to_delete = next((task for task in self.tasks if task.id == task_id), None)

        if not task_to_delete:
            print(f"{COLOR_RED}Task with ID '{task_id}' not found.{COLOR_RESET}")
            input(f"\n{COLOR_BLUE}Press Enter to continue...{COLOR_RESET}")
            return
        

        confirm = get_valid_input(f"Are you sure you want to delete '{task_to_delete.title}' (ID: {task_to_delete.id})? (yes/no): ",
                                  lambda x: x.lower() in ['yes', 'no'],
                                  "Please type 'yes' or 'no'.")

        if confirm.lower() == 'yes':
            self.tasks = [task for task in self.tasks if task.id != task_id]
            self._save_tasks()
            print(f"{COLOR_GREEN}Task '{task_to_delete.title}' (ID: {task_to_delete.id}) deleted successfully.{COLOR_RESET}")
        else:
            print(f"{COLOR_YELLOW}Deletion cancelled.{COLOR_RESET}")
        input(f"\n{COLOR_BLUE}Press Enter to continue...{COLOR_RESET}")
