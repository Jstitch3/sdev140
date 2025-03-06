from datetime import datetime
import json
import tkinter as tk
from tkinter import Tk, messagebox
from tkinter import simpledialog
from typing import Any

class Task:
    def __init__(self, description: str, priority: str, due_date: str):
        """
        Initializes a new task object with the provided description, priority, and due date.
        :param description: The task description (string).
        :param priority: The task priority ('low', 'medium', 'high').
        :param due_date: The due date of the task in 'YYYY-MM-DD' format.
        """
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = False

    def mark_completed(self):
        """Marks the task as completed."""
        self.completed = True

    def to_dict(self) -> dict[str, Any]:
        """Converts the task object to a dictionary representation."""
        return {
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed
        }

class TaskManagerApp:
    def __init__(self, root: Tk):
        """Initializes the application."""
        self.root = root
        self.root.title("QuickTask Manager")
        self.root.geometry("600x400")
        self.tasks: list[Task] = []
        self.load_tasks()
        self.create_main_window()

    def create_main_window(self):
        """Creates the main window for the app."""
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        self.title_label = tk.Label(self.main_frame, text="QuickTask Manager", font=("Arial", 24))
        self.title_label.pack()

        self.add_task_icon = tk.PhotoImage(file="images/add.png").subsample(16, '')
        self.delete_task_icon = tk.PhotoImage(file="images/delete.png").subsample(16, '')

        self.task_frame = tk.Frame(self.main_frame)
        self.task_frame.pack(pady=10)

        self.add_button = tk.Button(self.main_frame, text="Add Task", image=self.add_task_icon, compound="left", command=self.add_task)
        self.add_button.pack(pady=10)

        self.view_button = tk.Button(self.main_frame, text="View Tasks", command=self.view_tasks)
        self.view_button.pack(pady=10)

        self.exit_button = tk.Button(self.main_frame, text="Exit", command=self.root.quit)
        self.exit_button.pack(pady=10)

    def add_task(self):
        """Opens a window to add a new task."""
        self.add_task_window = tk.Toplevel(self.root)
        self.add_task_window.title("Add New Task")

        self.description_label = tk.Label(self.add_task_window, text="Task Description:")
        self.description_label.pack()

        self.description_entry = tk.Entry(self.add_task_window, width=40)
        self.description_entry.pack(pady=5)

        self.priority_label = tk.Label(self.add_task_window, text="Priority (low/medium/high):")
        self.priority_label.pack()

        self.priority_entry = tk.Entry(self.add_task_window, width=40)
        self.priority_entry.pack(pady=5)

        self.due_date_label = tk.Label(self.add_task_window, text="Due Date (YYYY-MM-DD):")
        self.due_date_label.pack()

        self.due_date_entry = tk.Entry(self.add_task_window, width=40)
        self.due_date_entry.pack(pady=5)

        self.save_button = tk.Button(self.add_task_window, text="Save", command=self.save_task)
        self.save_button.pack(pady=10)

        self.cancel_button = tk.Button(self.add_task_window, text="Cancel", command=self.add_task_window.destroy)
        self.cancel_button.pack(pady=10)

    def save_task(self):
        """Saves a task to the list and JSON file."""
        description = self.description_entry.get().strip()  # Get and strip any leading/trailing whitespace
        priority = self.priority_entry.get().strip().lower()  # Convert priority to lowercase for uniformity
        due_date = self.due_date_entry.get().strip()

        # Validation for empty fields
        if not description or not priority or not due_date:
            messagebox.showerror("Error", "All fields are required.") # type: ignore
            return

        # Validation for priority value
        if priority not in ["low", "medium", "high"]:
            messagebox.showerror("Error", "Priority must be 'low', 'medium', or 'high'.") # type: ignore
            return

        # Validation for due date format
        try:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")  # Try to convert the due date
            due_date = due_date_obj.strftime('%Y-%m-%d')  # Reformat date to ensure it's in the correct format
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.") # type: ignore
            return

        # If all validations pass, create and save the task
        task = Task(description, priority, due_date)
        self.tasks.append(task)
        self.save_tasks()  # Save updated tasks to the JSON file
        self.add_task_window.destroy()  # Close the add task window
        messagebox.showinfo("Success", "Task added successfully!")  # type: ignore # Show success message

    def view_tasks(self):
        """Displays the tasks in the window with edit, delete, and mark as completed options."""
        for task in self.task_frame.winfo_children():
            task.destroy()

        for i, task in enumerate(self.tasks):
            task_frame = tk.Frame(self.task_frame)
            task_frame.pack(fill="x", pady=5)

            # Task text (description, priority, and due date)
            task_info = f"{task.description} | {task.priority} | {task.due_date} | {'Completed' if task.completed else 'Pending'}"
            task_label = tk.Button(task_frame, text=task_info, anchor="w", width=50, padx=5)
            task_label.pack(side="left")
            
            # Create buttons (edit, delete, and mark as completed) for each task
            edit_button = tk.Button(task_frame, text="Edit", command=lambda i=i: self.edit_task(i))
            edit_button.pack(side='left', pady=5)

            delete_button = tk.Button(task_frame, text="Delete", image=self.delete_task_icon, command=lambda i=i: self.delete_task(i))
            delete_button.pack(side='left', pady=5)

            complete_button = tk.Button(task_frame, text="Mark as Completed" if not task.completed else "Unmark Completed", command=lambda i=i: self.toggle_completion(i))
            complete_button.pack(side='left', pady=5)

    def edit_task(self, index: int):
        """Allows editing of the selected task."""
        task = self.tasks[index]
        new_description = simpledialog.askstring("Edit Task", "Enter new description:", initialvalue=task.description)
        new_priority = simpledialog.askstring("Edit Task", "Enter new priority (low/medium/high):", initialvalue=task.priority)
        new_due_date = simpledialog.askstring("Edit Task", "Enter new due date (YYYY-MM-DD):", initialvalue=task.due_date)

        if new_description and new_priority and new_due_date:
            try:
                due_date_obj = datetime.strptime(new_due_date, "%Y-%m-%d")
                task.description = new_description
                task.priority = new_priority
                task.due_date = due_date_obj.strftime('%Y-%m-%d')
                self.save_tasks()
                self.view_tasks()  # Refresh task list
                messagebox.showinfo("Success", "Task updated successfully!") # type: ignore
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.") # type: ignore
        else:
            messagebox.showerror("Error", "All fields are required.") # type: ignore

    def delete_task(self, index: int):
        """Deletes the selected task from the list and the JSON file."""
        del self.tasks[index]
        self.save_tasks()
        self.view_tasks()  # Refresh task list
        messagebox.showinfo("Success", "Task deleted successfully!") # type: ignore

    def toggle_completion(self, index: int):
        """Marks a task as completed or uncompleted."""
        task = self.tasks[index]
        task.mark_completed()  # Mark the task as completed
        self.save_tasks()  # Save updated task list
        self.view_tasks()  # Refresh the task list to reflect the change

    def load_tasks(self):
        """Loads tasks from the JSON file."""
        try:
            with open("tasks.json", "r") as file:
                task_data = json.load(file)
                for data in task_data:
                    task = Task(data["description"], data["priority"], data['due_date'])
                    task.completed = data["completed"]
                    self.tasks.append(task)
        except FileNotFoundError:
            pass

    def save_tasks(self):
        """Saves tasks to the JSON file."""
        task_data = [task.to_dict() for task in self.tasks]
        with open("tasks.json", "w") as file:
            json.dump(task_data, file)

# Run the app
if __name__ == "__main__":
    root = Tk()
    app = TaskManagerApp(root)
    root.mainloop()
