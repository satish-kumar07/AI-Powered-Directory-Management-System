import os
import logging
import threading
import time  
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES  # Drag-and-Drop support
from plyer import notification  # For desktop notifications
from ai.model import FileCategorizer
from utils.file_operations import (
    display_log,sort_files_by_date, encrypt_file, decrypt_file, move_file, copy_file, delete_file, create_directory,
    delete_directory, list_files_in_directory, rename_directory,view_file_metadata, preview_file, deorganize_files,organize_files_task,
     move_folder, copy_folder
)

class FileManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("File Management Operations")
        master.geometry("1000x800")  # Increased window size
        master.configure(bg='lightblue')  # Set background color

        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # Add a header label
        header_label = tk.Label(master, text="File Management Operations", font=("Arial", 24, "bold"), bg="lightblue")
        header_label.pack(pady=20)
        header_label.configure(font=("Helvetica", 24, "bold"))

        # Create a tabbed interface
        notebook = ttk.Notebook(master)
        notebook.pack(expand=True, fill="both")

        # Create tabs
        file_operations_tab = ttk.Frame(notebook)
        directory_operations_tab = ttk.Frame(notebook)
        advanced_operations_tab = ttk.Frame(notebook)

        notebook.add(file_operations_tab, text="File Operations")
        notebook.add(directory_operations_tab, text="Directory Operations")
        notebook.add(advanced_operations_tab, text="Advanced Operations")

        # Add buttons to File Operations tab
        self.add_buttons(file_operations_tab, [
            ("Organize Files", self.organize_files),
            ("Move File", self.move_file),
            ("Copy File", self.copy_file),
            ("Delete File", self.delete_file),
            ("Deorganize Files", self.deorganize_files),
        ])

        # Add buttons to Directory Operations tab
        self.add_buttons(directory_operations_tab, [
            ("Create Folder", self.create_directory),
            ("Delete Folder", self.delete_directory),
            ("List Files", self.list_files),
            ("Rename Folder", self.rename_directory),
            ("Move Folder", self.move_folder),
            ("Copy Folder", self.copy_folder),
        ])

        # Add buttons to Advanced Operations tab
        self.add_buttons(advanced_operations_tab, [
            ("Display Log", self.display_log),
            ("Sort Files by Date", self.sort_files_by_date),
            ("Encrypt File", self.encrypt_file),
            ("Decrypt File", self.decrypt_file),
            ("View Metadata", self.view_metadata),
            ("Preview File", self.preview_file),
        ])

        # Add Drag-and-Drop Support
        master.drop_target_register(DND_FILES)
        master.dnd_bind('<<Drop>>', self.handle_drop)

        # Add Progress Bar
        self.progress = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

    def add_buttons(self, frame, buttons):
        """Helper method to add buttons to a frame."""
        row, column = 0, 0
        for text, command in buttons:
            button = tk.Button(frame, text=text, command=command, width=20, height=2, bg="white", fg="black", font=("Arial", 10, "bold"))
            button.grid(row=row, column=column, padx=10, pady=10)
            column += 1
            if column > 3:  # Adjust the number of columns per row as needed
                column = 0
                row += 1


    def handle_drop(self, event):
        """Handle files dropped into the application."""
        dropped_files = self.master.tk.splitlist(event.data)
        for file in dropped_files:
            logging.info(f"Dropped file: {file}")
            notification.notify(
                title="File Dropped",
                message=f"File '{os.path.basename(file)}' has been added.",
                timeout=5
            )

    def long_running_task(self):
        """Simulate a long-running task with a progress bar."""
        self.progress["value"] = 0
        for i in range(100):
            self.progress["value"] += 1
            self.master.update_idletasks()
            time.sleep(0.05)  # Simulate work

    def select_directory(self, title="Select Directory"):
        return filedialog.askdirectory(title=title)

    def select_file(self, title="Select File"):
        return filedialog.askopenfilename(title=title)

    def get_input(self, title="Input", prompt="Enter value:", default=None):
        """Prompt the user for input with an optional default value."""
        return simpledialog.askstring(title, prompt, initialvalue=default)

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def organize_files(self):
        """Organize files in a selected directory."""
        source_directory = self.select_directory("Select Directory to Organize")
        if source_directory:
            target_directory = self.select_directory("Select Target Directory for Organized Files")
            if not target_directory:
                self.show_message("Error", "Target directory not selected.")
                return

            if messagebox.askyesno("Confirm Organize", f"Organize files in '{source_directory}'?"):
                try:
                    # Initialize and load the FileCategorizer model
                    model = FileCategorizer()
                    model.load_model()  # Ensure the model is loaded before use

                    # Start the organization task in a separate thread
                    threading.Thread(
                        target=organize_files_task,
                        args=(source_directory, target_directory, model, self.show_message)
                    ).start()
                except FileNotFoundError as e:
                    logging.error(f"Error loading model: {e}")
                    self.show_message("Error", "AI model file not found. Please ensure the model is trained and available.")
                except Exception as e:
                    logging.error(f"Error initializing model: {e}")
                    self.show_message("Error", f"Failed to initialize model: {e}")

    def move_file(self):
        source = self.select_file("Select File to Move")
        if source:
            destination = self.select_directory("Select Destination Directory")
            if destination:
                copy_file(source, os.path.join(destination, os.path.basename(source)))

    def copy_file(self):
        source = self.select_file("Select File to Copy")
        if source:
            destination = self.select_directory("Select Destination Directory")
            if destination:
                copy_file(source, os.path.join(destination, os.path.basename(source)))

    def delete_file(self):
        path = self.select_file("Select File or Folder to Delete")
        if path:
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {os.path.basename(path)}?"):
                delete_file(path)

    def create_directory(self):
        path = self.select_directory("Select Parent Directory")
        if path:
            name = self.get_input("Create Directory", "Enter the name of the new directory:")
            if name:
                create_directory(path, name)

    def delete_directory(self):
        path = self.select_directory("Select Directory to Delete")
        if path:
            name = os.path.basename(path)
            parent_path = os.path.dirname(path)
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete directory '{name}'?"):
                delete_directory(parent_path, name)

    def list_files(self):
        path = self.select_directory("Select Directory to List Files")
        if path:
            files = list_files_in_directory(path)
            if files:
                self.show_message("Files in Directory", "\n".join(files))

    def rename_directory(self):
        current_path = self.select_directory("Select Directory to Rename")
        if current_path:
            parent_path = os.path.dirname(current_path)
            current_name = os.path.basename(current_path)
            new_name = self.get_input("Rename Directory", "Enter new name:", current_name)
            if new_name and new_name != current_name:
                new_path = os.path.join(parent_path, new_name)
                try:
                    # Handle case-sensitive renaming explicitly
                    if os.path.exists(new_path) and new_name.lower() != current_name.lower():
                        self.show_message("Error", f"Directory '{new_name}' already exists in '{parent_path}'.")
                    else:
                        # Temporary rename to handle case-only changes
                        temp_path = os.path.join(parent_path, f"{current_name}_temp")
                        os.rename(current_path, temp_path)
                        os.rename(temp_path, new_path)
                        self.show_message("Success", f"Directory '{current_name}' has been renamed to '{new_name}'.")
                except Exception as e:
                    logging.error(f"Error renaming directory: {e}")
                    self.show_message("Error", f"Failed to rename directory: {e}")

    def display_log(self):
        display_log()

    def sort_files_by_date(self):
        source_directory = self.select_directory("Select Source Directory to Sort")
        if source_directory:
            target_directory = self.select_directory("Select Target Directory")
            if target_directory:
                if messagebox.askyesno("Confirm Sort", f"Sort files from '{source_directory}' by date into '{target_directory}'?"):
                    sort_files_by_date(source_directory, target_directory)

    def encrypt_file(self):
        file = self.select_file("Select File to Encrypt")
        if file:
            if messagebox.askyesno("Confirm Encrypt", f"Are you sure you want to encrypt '{os.path.basename(file)}'?"):
                encrypt_file(file)

    def decrypt_file(self):
        file = self.select_file("Select File to Decrypt")
        if file:
            if messagebox.askyesno("Confirm Decrypt", f"Are you sure you want to decrypt '{os.path.basename(file)}'?"):
                decrypt_file(file)

    def view_metadata(self):
        file_path = self.select_file("Select File to View Metadata")
        if file_path:
            metadata = view_file_metadata(file_path)
            if metadata:
                metadata_str = "\n".join([f"{key}: {value}" for key, value in metadata.items()])
                self.show_message("File Metadata", metadata_str)

    def preview_file(self):
        file_path = self.select_file("Select Text File to Preview")
        if file_path:
            lines_str = self.get_input("Preview Lines", "Enter the number of lines to preview:")
            if lines_str:
                try:
                    lines = int(lines_str)
                    content = preview_file(file_path, lines)
                    if content:
                        self.show_message("File Preview", content)
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid number")
                except Exception as e:
                    logging.error(f"Error previewing file {file_path}: {e}")
                    self.show_message("Error", f"Failed to preview file: {e}")

    def deorganize_files(self):
        source_directory = self.select_directory("Select Directory to Deorganize")
        if source_directory:
            deorganize_files(source_directory)
            # Show success message
            self.show_message("Success", f"Files in '{source_directory}' have been deorganized successfully.")

    def move_folder(self):
        source_folder = self.select_directory("Select Folder to Move")
        if source_folder:
            target_folder = self.select_directory("Select Target Location")
            if target_folder:
                move_folder(source_folder, target_folder)
                self.show_message("Success", f"Moved folder to: {target_folder}")

    def copy_folder(self):
        source_folder = self.select_directory("Select Folder to Copy")
        if source_folder:
            target_folder = self.select_directory("Select Target Location")
            if target_folder:
                copy_folder(source_folder, target_folder)
                self.show_message("Success", f"Copied folder to: {target_folder}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = FileManagerApp(root)
    root.mainloop()