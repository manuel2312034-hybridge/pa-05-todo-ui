import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class UI:
    def __init__(self):
        self.root = tk.Tk()

    def draw_interface(self):
        #main window
        self.root.title("App tareas")
        self.root.geometry("800x600")
        self.root.minsize(600, 300)

        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Entry for adding tasks
        self.entry_task = tk.Entry(self.root)
        self.entry_task.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        button_add_task = tk.Button(self.root, text="Añadir", command=self.on_add_task_callback)
        button_add_task.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        button_clear_all = tk.Button(self.root, text="Limpiar todo", command=self.clear_all)
        button_clear_all.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Frame for the task lists (Pending, Doing, Done) and separators
        frame_tasks = tk.Frame(self.root)
        frame_tasks.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Configure columns with separators
        frame_tasks.columnconfigure(0, weight=1, uniform='cols')  # Pending
        frame_tasks.columnconfigure(1, weight=0)                  # Separator 1
        frame_tasks.columnconfigure(2, weight=1, uniform='cols')  # Doing
        frame_tasks.columnconfigure(3, weight=0)                  # Separator 2
        frame_tasks.columnconfigure(4, weight=1, uniform='cols')  # Done
        frame_tasks.rowconfigure(0, weight=1)

        # Pending Tasks
        frame_pending = tk.Frame(frame_tasks)
        frame_pending.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        label_pending = tk.Label(frame_pending, text="Pendiente")
        label_pending.pack()

        #Listbox doesnt support embedded buttons so using canvas instead
        self.canvas_pending = tk.Canvas(frame_pending, bg="white", bd=0, highlightthickness=0)
        self.canvas_pending.pack(fill=tk.BOTH, expand=True)

        # Vertical Separator 1 (between Pending and Doing)
        sep1 = ttk.Separator(frame_tasks, orient=tk.VERTICAL)
        sep1.grid(row=0, column=1, sticky="ns", padx=5)

        # Doing Tasks
        frame_doing = tk.Frame(frame_tasks)
        frame_doing.grid(row=0, column=2, sticky="nsew", padx=5)

        label_doing = tk.Label(frame_doing, text="En curso")
        label_doing.pack()

        self.canvas_doing = tk.Canvas(frame_doing, bg="white", bd=0, highlightthickness=0)
        self.canvas_doing.pack(fill=tk.BOTH, expand=True)

        # Vertical Separator 2 (between Doing and Done)
        sep2 = ttk.Separator(frame_tasks, orient=tk.VERTICAL)
        sep2.grid(row=0, column=3, sticky="ns", padx=5)

        # Done Tasks
        frame_done = tk.Frame(frame_tasks)
        frame_done.grid(row=0, column=4, sticky="nsew", padx=(5, 0))

        label_done = tk.Label(frame_done, text="Finalizado")
        label_done.pack()

        self.canvas_done = tk.Canvas(frame_done, bg="white", bd=0, highlightthickness=0)
        self.canvas_done.pack(fill=tk.BOTH, expand=True)

    def on_add_task_callback(self):
        task = self.entry_task.get()
        if task:
            self.add_task_to_listbox(self.canvas_pending, task)
            self.entry_task.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese una tarea")

    def on_move_task(self, task_frame, source_canvas):
        target_canvas = None
        if source_canvas == self.canvas_pending:
            target_canvas = self.canvas_doing
        elif source_canvas == self.canvas_doing:
            target_canvas = self.canvas_done

        task = task_frame.winfo_children()[0].cget("text")
        task_frame.destroy()
        self.add_task_to_listbox(target_canvas, task)
    def add_task_to_listbox(self, canvas, task):
        new_task_frame = tk.Frame(canvas, bg="white")
        new_task_frame.pack(fill=tk.X, pady=2)

        label_task = tk.Label(new_task_frame, text=task, bg="white", anchor="w")
        label_task.pack(side=tk.LEFT, fill=tk.X, expand=True)

        if canvas != self.canvas_done:
            button_move = tk.Button(new_task_frame, text=">", command=lambda: self.on_move_task(new_task_frame, canvas))
            button_move.pack(side=tk.RIGHT, padx=2)

        button_delete = tk.Button(new_task_frame, text="X", command=lambda: self.on_delete_task(new_task_frame))
        button_delete.pack(side=tk.RIGHT, padx=2)

        # Force the task frame to match the canvas width
        canvas.update_idletasks()
        new_task_frame.config(width=canvas.winfo_width())

    def on_delete_task(self, task_frame):
        task_frame.destroy()

    def clear_all(self):
        self.clear_items(self.canvas_pending)
        self.clear_items(self.canvas_done)

    def clear_items(self, canvas):
        children = canvas.winfo_children()
        for child in children:
            child.destroy()
        print('clear all')
    def start(self):
        self.draw_interface()
        self.root.mainloop()

ui = UI()
ui.start()