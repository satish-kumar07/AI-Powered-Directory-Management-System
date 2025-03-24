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