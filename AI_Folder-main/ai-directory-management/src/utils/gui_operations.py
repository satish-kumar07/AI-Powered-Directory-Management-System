import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class FileSelector:
    _root = None
    
    @classmethod
    def _get_root(cls):
        """Get or create the root window."""
        if cls._root is None:
            cls._root = tk.Tk()
            cls._root.withdraw()
        return cls._root

    @classmethod
    def get_input(cls, title, prompt, default=""):
        """Shows an input dialog with a default value."""
        root = cls._get_root()
        result = simpledialog.askstring(
            title,
            prompt,
            initialvalue=default,
            parent=root
        )
        return result

    @classmethod
    def get_simple_input(cls, prompt, default=""):
        """Shows a simplified input dialog with default value."""
        return cls.get_input("Input", prompt, default)

    @classmethod
    def select_file(cls, title="Select File", filetypes=None):
        """Opens a file selection dialog."""
        root = cls._get_root()
        if filetypes is None:
            filetypes = [("All files", "*.*")]
        return filedialog.askopenfilename(
            title=title,
            filetypes=filetypes,
            parent=root
        )

    @classmethod
    def select_directory(cls, title="Select Directory"):
        """Opens a directory selection dialog."""
        root = cls._get_root()
        return filedialog.askdirectory(
            title=title,
            parent=root
        )

    @classmethod
    def show_message(cls, title, message, type="info"):
        """Shows a message dialog."""
        root = cls._get_root()
        if type == "error":
            messagebox.showerror(title, message, parent=root)
        elif type == "warning":
            messagebox.showwarning(title, message, parent=root)
        else:
            messagebox.showinfo(title, message, parent=root)

    @classmethod
    def show_confirm(cls, title, message):
        """Shows a confirmation dialog."""
        root = cls._get_root()
        return messagebox.askyesno(title, message, parent=root)

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
    def get_directory_name():
        """Prompt the user to input a directory name."""
        import tkinter as tk
        from tkinter.simpledialog import askstring

        root = tk.Tk()
        root.withdraw()  # Hide the main window
        directory_name = askstring("Directory Name", "Enter the name of the new directory:")
        root.destroy()
        return directory_name