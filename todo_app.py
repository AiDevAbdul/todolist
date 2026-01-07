import tkinter as tk

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        self.task_entry = tk.Entry(root, width=50)
        self.task_entry.pack()

        self.add_task_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_task_button.pack()

        self.tasks_listbox = tk.Listbox(root, width=50)
        self.tasks_listbox.pack()

        self.delete_task_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_task_button.pack()

        self.mark_complete_button = tk.Button(root, text="Mark Complete", command=self.mark_complete)
        self.mark_complete_button.pack()

        self.load_tasks()

        self.root.protocol("WM_DELETE_WINDOW", self.save_tasks)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)

    def delete_task(self):
        try:
            selected_task_index = self.tasks_listbox.curselection()[0]
            self.tasks_listbox.delete(selected_task_index)
        except IndexError:
            pass

    def mark_complete(self):
        try:
            selected_task_index = self.tasks_listbox.curselection()[0]
            self.tasks_listbox.itemconfig(selected_task_index, {'bg': 'light green'})
        except IndexError:
            pass

    def save_tasks(self):
        with open("tasks.txt", "w") as f:
            tasks = self.tasks_listbox.get(0, tk.END)
            for task in tasks:
                f.write(task + "\n")
        self.root.destroy()

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as f:
                tasks = f.readlines()
                for task in tasks:
                    self.tasks_listbox.insert(tk.END, task.strip())
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
