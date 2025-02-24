from datetime import datetime
import json
import tkinter as tk
from tkinter import Tk, messagebox
from typing import Any

class Task:
    def __init__(self, description: str, priority: str, due_date: str):
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def to_dict(self) -> dict[str, Any]:
        return {
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed
        }

class TaskManagerApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("QuickTask Manager")
        self.root.geometry("600x400")
        self.tasks: list[Task] = []
        self.load_tasks()
        
        self.create_main_window()

    def create_main_window(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        self.title_label = tk.Label(self.main_frame, text="QuickTask Manager", font=("Arial", 24))
        self.title_label.pack()

        self.add_button = tk.Button(self.main_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=10)

        self.view_button = tk.Button(self.main_frame, text="View Tasks", command=self.view_tasks)
        self.view_button.pack(pady=10)

        self.exit_button = tk.Button(self.main_frame, text="Exit", command=self.root.quit)
        self.exit_button.pack(pady=10)

    def add_task(self):
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
        description = self.description_entry.get()
        priority = self.priority_entry.get()
        due_date = self.due_date_entry.get()

        if description and priority and due_date:
            try:
                due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
                task = Task(description, priority, due_date_obj.strftime('%Y-%m-%d'))
                self.tasks.append(task)
                self.save_tasks()
                self.add_task_window.destroy()
                messagebox.showinfo("Success", "Task added successfully!")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    def view_tasks(self):
        self.view_tasks_window = tk.Toplevel(self.root)
        self.view_tasks_window.title("View Tasks")

        self.filter_frame = tk.Frame(self.view_tasks_window)
        self.filter_frame.pack(pady=10)

        self.filter_label = tk.Label(self.filter_frame, text="Filter by Priority:")
        self.filter_label.pack(side=tk.LEFT)

        self.priority_filter = tk.StringVar(value="All")
        self.priority_menu = tk.OptionMenu(self.filter_frame, self.priority_filter, "All", "low", "medium", "high")
        self.priority_menu.pack(side=tk.LEFT, padx=5)

        self.filter_button = tk.Button(self.filter_frame, text="Filter", command=self.update_task_list)
        self.filter_button.pack(side=tk.LEFT, padx=5)

        self.task_listbox = tk.Listbox(self.view_tasks_window, width=80, height=10)
        self.task_listbox.pack(pady=10)

        self.update_task_list()

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)

        priority_filter = self.priority_filter.get()

        for task in self.tasks:
            if priority_filter == "All" or task.priority == priority_filter:
                task_info = f"{task.description} | {task.priority} | {task.due_date} | {'Completed' if task.completed else 'Pending'}"
                self.task_listbox.insert(tk.END, task_info)

    def load_tasks(self):
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
        task_data = [task.to_dict() for task in self.tasks]
        with open("tasks.json", "w") as file:
            json.dump(task_data, file)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
