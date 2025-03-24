import tkinter as tk
from tkinter import filedialog, messagebox

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