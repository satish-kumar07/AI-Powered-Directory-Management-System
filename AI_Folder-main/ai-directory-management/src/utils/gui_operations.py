import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class FileSelector:
    @staticmethod
    def select_directory(title="Select Directory"):
        """Opens a dialog for directory selection."""
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        directory = filedialog.askdirectory(title=title)
        return directory if directory else None

    @staticmethod
    def select_file(title="Select File", filetypes=None):
        """Opens a dialog for file selection."""
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        if filetypes is None:
            filetypes = [("All files", "*.*")]
        file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
        return file_path if file_path else None

    @staticmethod
    def show_message(title, message, type="info"):
        """Shows a message dialog."""
        root = tk.Tk()
        root.withdraw()
        if type == "error":
            messagebox.showerror(title, message)
        elif type == "warning":
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)

    @staticmethod
    def show_confirm(title, message):
        """Shows a confirmation dialog."""
        root = tk.Tk()
        root.withdraw()
        return messagebox.askyesno(title, message)

    @staticmethod
    def get_input(title, prompt):
        """Shows an input dialog."""
        root = tk.Tk()
        root.title(title)
        
        # Center the window
        window_width = 400
        window_height = 150
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        label = tk.Label(root, text=prompt)
        label.pack(pady=10)
        
        entry = tk.Entry(root, width=40)
        entry.pack(pady=10)
        entry.focus()
        
        result = [None]
        
        def on_ok():
            result[0] = entry.get()
            root.destroy()
        
        def on_cancel():
            root.destroy()
        
        tk.Button(root, text="OK", command=on_ok).pack(side=tk.LEFT, padx=20, pady=10)
        tk.Button(root, text="Cancel", command=on_cancel).pack(side=tk.RIGHT, padx=20, pady=10)
        
        root.mainloop()
        return result[0]

    @staticmethod
    def get_directory_name():
        """Shows a simplified input dialog for directory name."""
        root = tk.Tk()
        root.withdraw()
        name = simpledialog.askstring("Create Directory", "Enter directory name:")
        return name

    @staticmethod
    def get_file_info(title="Create File", name_prompt="File name:", content_prompt=None):
        """Get file name and optional content in a single dialog."""
        root = tk.Tk()
        root.title(title)
        
        # Center window
        window_width = 400
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # File name entry
        tk.Label(root, text=name_prompt).pack(pady=5)
        name_entry = tk.Entry(root, width=40)
        name_entry.pack(pady=5)
        name_entry.focus()

        # Content entry if needed
        content_entry = None
        if content_prompt:
            tk.Label(root, text=content_prompt).pack(pady=5)
            content_entry = tk.Text(root, width=40, height=4)
            content_entry.pack(pady=5)

        result = {"name": None, "content": None}

        def on_submit():
            result["name"] = name_entry.get()
            if content_entry:
                result["content"] = content_entry.get("1.0", tk.END).strip()
            root.destroy()

        def on_cancel():
            root.destroy()

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Create", command=on_submit).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT)

        root.mainloop()
        return result

    @staticmethod
    def get_simple_input(prompt, default=""):
        """Shows a simplified input dialog with default value."""
        root = tk.Tk()
        root.withdraw()
        result = simpledialog.askstring("Input", prompt, initialvalue=default)
        return result