import os
import shutil
import logging
import mimetypes
import hashlib
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from cryptography.fernet import Fernet
import stat
from utils.gui_operations import FileSelector
from threading import Thread

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(asctime)s - %(message)s')

def move_file(source_path, target_path, show_dialog=True):
    """Move a file or folder to a new location."""
    try:
        shutil.move(source_path, target_path)
        logging.info(f"Moved {source_path} to {target_path}")
        log_operation('move', {'source': source_path, 'target': target_path})
        if show_dialog:
            FileSelector.show_message("Success", f"Moved {os.path.basename(source_path)} successfully")
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
    except Exception as e:
        logging.error(f"Error moving {source_path} to {target_path}: {e}")
        if show_dialog:
            FileSelector.show_message("Error", f"Error moving file: {str(e)}", "error")

def copy_file(source_path, target_path):
    """Copy a file or folder to a new location."""
    try:
        if os.path.isdir(source_path):
            if not os.path.exists(target_path):
                shutil.copytree(source_path, target_path)
            else:
                for item in os.listdir(source_path):
                    s = os.path.join(source_path, item)
                    d = os.path.join(target_path, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)
        else:
            shutil.copy2(source_path, target_path)
        logging.info(f"Copied {source_path} to {target_path}")
        log_operation('copy', {'source': source_path, 'target': target_path})
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
    except Exception as e:
        logging.error(f"Error copying {source_path} to {target_path}: {e}")

def delete_file(path):
    """Delete a specified file or folder."""
    try:
        if os.path.isdir(path):
           
            for root, dirs, files in os.walk(path):
                for dir in dirs:
                    os.chmod(os.path.join(root, dir), stat.S_IWRITE)
                for file in files:
                    os.chmod(os.path.join(root, file), stat.S_IWRITE)
            shutil.rmtree(path)
        else:
            os.chmod(path, stat.S_IWRITE)
            os.remove(path)
        logging.info(f"Deleted {path}")
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
    except Exception as e:
        logging.error(f"Error deleting {path}: {e}")

def summarize_file(file_path):
    """Generate an AI-based summary of a text file."""
    if not os.path.isfile(file_path):
        logging.error(f"File not found: {file_path}")
        return

    try:
        # Open the file with a fallback encoding and handle decoding errors
        with open(file_path, "r", encoding="utf-8", errors="replace") as file:
            content = file.read()

        # Perform the summarization (replace this with your actual summarization logic)
        summary = f"Summary of {file_path}:\n{content[:200]}..."  # Example: First 200 characters
        logging.info(f"File summarized successfully: {file_path}")
        print(summary)

    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
    except Exception as e:
        logging.error(f"Error summarizing file {file_path}: {e}")

def display_log():
    """Display a log of previous operations."""
    try:
        with open('operations.log', 'r') as log_file:
            log_content = log_file.read()
            print(log_content)
            logging.info("Displayed log content.")
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
    except Exception as e:
        logging.error(f"Error displaying log: {e}")

def categorize_file(file_name, categories):
    """Categorize a file based on its extension."""
    _, ext = os.path.splitext(file_name)
    ext = ext.lower()
    for category, extensions in categories.items():
        if ext in extensions:
            return category
    return "Others"

def organize_files_task(source_directory, target_directory, model, show_message=None):
    """Organize files in the source directory using the provided model."""
    try:
        if not os.path.exists(source_directory):
            logging.error(f"Source directory '{source_directory}' does not exist.")
            if show_message:
                show_message("Error", f"Source directory '{source_directory}' does not exist.")
            return

        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        for file_name in os.listdir(source_directory):
            file_path = os.path.join(source_directory, file_name)
            if os.path.isfile(file_path):
                file_metadata = {
                    'name': file_name,
                    'size': os.path.getsize(file_path),
                    'type': mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
                }
                category = model.predict_category(file_metadata)
                target_folder = os.path.join(target_directory, category)
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                move_file(file_path, os.path.join(target_folder, file_name), show_dialog=False)

        # Log success and show success message
        logging.info(f"Files in '{source_directory}' have been organized successfully into '{target_directory}'.")
        if show_message:
            show_message("Success", f"Files in '{source_directory}' have been organized successfully into '{target_directory}'.")

        # Stop the function after successful completion
        return
    except Exception as e:
        logging.error(f"Error organizing files: {e}")
        if show_message:
            show_message("Error", f"Error organizing files: {e}")

def deorganize_files(source_directory):
    """Moves files from subdirectories back to the main directory."""
    try:
        for root, dirs, files in os.walk(source_directory):
            for file in files:
                # Skip system files like desktop.ini
                if file.lower() == "desktop.ini":
                    logging.info(f"Skipping system file: {file}")
                    continue

                source_path = os.path.join(root, file)
                target_path = os.path.join(source_directory, file)

                # Avoid overwriting existing files
                if os.path.exists(target_path):
                    logging.warning(f"File already exists: {target_path}")
                    continue

                try:
                    os.rename(source_path, target_path)
                    logging.info(f"Moved {source_path} to {target_path}")
                except PermissionError as e:
                    logging.error(f"Permission denied: {e}")
                except Exception as e:
                    logging.error(f"Error moving file {file}: {e}")

    except Exception as e:
        logging.error(f"Error during deorganization: {e}")


def rename_files(directory):
    """Rename files intelligently based on content/type."""
    if not os.path.exists(directory):
        logging.error(f"Directory {directory} does not exist.")
        return

    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type:
                print(f"Current file: {file_path}")
                new_file_name = input(f"Enter new name for {file_name} (leave blank to skip): ").strip()
                if new_file_name:
                    new_file_path = os.path.join(root, new_file_name)
                    try:
                        os.rename(file_path, new_file_path)
                        logging.info(f"Renamed file {file_path} to {new_file_path}")
                    except PermissionError as e:
                        logging.error(f"Permission denied: {e}")
                    except Exception as e:
                        logging.error(f"Error renaming file {file_path} to {new_file_path}: {e}")
                else:
                    logging.info(f"Skipped renaming file {file_path}")
            else:
                logging.warning(f"Could not determine MIME type for file {file_path}")

def log_operation(operation, details):
    """Log an operation to the operations log."""
    log_entry = {
        'operation': operation,
        'details': details
    }
    try:
        with open('operations.log', 'a') as log_file:
            log_file.write(json.dumps(log_entry) + '\n')
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")

class DirectoryEventHandler(FileSystemEventHandler):
    def __init__(self, model, target_directory):
        self.model = model
        self.target_directory = target_directory

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            logging.info(f"New file detected: {file_path}")
            self.organize_file(file_path)

    def organize_file(self, file_path):
        file_name = os.path.basename(file_path)
        file_metadata = {
            'name': file_name,
            'size': os.path.getsize(file_path),
            'type': mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
        }
        category = self.model.predict_category(file_metadata)
        target_folder = os.path.join(self.target_directory, category)
        if not os.path.exists(target_folder):
            try:
                os.makedirs(target_folder)
                logging.info(f"Created directory: {target_folder}")
            except PermissionError as e:
                logging.error(f"Permission denied: {e}")
                return
            except Exception as e:
                logging.error(f"Error creating directory {target_folder}: {e}")
                return
        else:
            logging.info(f"Directory already exists: {target_folder}")
        try:
            move_file(file_path, os.path.join(target_folder, file_name))
        except PermissionError as e:
            logging.error(f"Permission denied: {e}")
        except Exception as e:
            logging.error(f"Error moving file {file_path} to {target_folder}: {e}")


def process_file(file_path, target_directory, model):
    """Process a new file."""
    try:
        file_metadata = {
            'name': os.path.basename(file_path),
            'size': os.path.getsize(file_path),
            'type': mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
        }
        category = model.predict_category(file_metadata)
        target_folder = os.path.join(target_directory, category)

        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            logging.info(f"Created directory: {target_folder}")
        else:
            logging.info(f"Directory already exists: {target_folder}")

        target_path = os.path.join(target_folder, os.path.basename(file_path))
        os.rename(file_path, target_path)
        logging.info(f"Moved {file_path} to {target_path}")

    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
    except Exception as e:
        logging.error(f"Error moving file {file_path}: {e}")

def sort_files_by_date(source_directory, target_directory):
    """Organize files based on creation/modification date."""
    if not os.path.exists(source_directory):
        logging.error(f"Source directory {source_directory} does not exist.")
        return

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    for file_name in os.listdir(source_directory):
        file_path = os.path.join(source_directory, file_name)
        if os.path.isfile(file_path):
            
            mod_time = os.path.getmtime(file_path)
            mod_time_struct = time.localtime(mod_time)
            year = mod_time_struct.tm_year
            month = mod_time_struct.tm_mon
            day = mod_time_struct.tm_mday

            
            target_subdir = os.path.join(target_directory, f"{year}-{month:02d}-{day:02d}")
            if not os.path.exists(target_subdir):
                os.makedirs(target_subdir)

            
            target_path = os.path.join(target_subdir, file_name)
            try:
                shutil.move(file_path, target_path)
                logging.info(f"Moved {file_path} to {target_path}")
            except PermissionError as e:
                logging.error(f"Permission denied: {e}")
            except Exception as e:
                logging.error(f"Error moving {file_path} to {target_path}: {e}")

    logging.info("File sorting by date completed.")

def generate_key():
    """Generate a key for encryption."""
    key = Fernet.generate_key()
    try:
        with open('encryption.key', 'wb') as key_file:
            key_file.write(key)
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
    return key

def load_key():
    """Load the encryption key from a file."""
    try:
        return open('encryption.key', 'rb').read()
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
        return None

def encrypt_file(file_path):
    """Encrypt a file for security."""
    try:
        
        if not os.path.exists('encryption.key'):
            key = generate_key()
        else:
            key = load_key()

        if key is None:
            return

        fernet = Fernet(key)

        with open(file_path, 'rb') as file:
            file_data = file.read()

       
        encrypted_data = fernet.encrypt(file_data)

       
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)

        logging.info(f"Encrypted file: {file_path}")
        log_operation('encrypt', {'file': file_path})
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
    except Exception as e:
        logging.error(f"Error encrypting file {file_path}: {e}")

def decrypt_file(file_path):
    """Decrypt a file."""
    try:
        if not os.path.exists('encryption.key'):
            logging.error("Encryption key not found.")
            return
        key = load_key()
        if key is None:
            return
        fernet = Fernet(key)

        with open(file_path, 'rb') as file:
            encrypted_data = file.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        with open(file_path, 'wb') as file:
            file.write(decrypted_data)

        logging.info(f"Decrypted file: {file_path}")
        log_operation('decrypt', {'file': file_path})
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
    except Exception as e:
        logging.error(f"Error decrypting file {file_path}: {e}")

def create_directory(parent_path, directory_name, show_dialog=True):
    """Create a new directory at the specified path."""
    try:
        # Validate inputs
        if not parent_path or not directory_name:
            raise ValueError("Parent path and directory name are required")

        # Create full path
        new_dir_path = os.path.join(parent_path, directory_name)

        # Check if directory already exists
        if os.path.exists(new_dir_path):
            msg = f"Directory '{directory_name}' already exists"
            logging.warning(msg)
            if show_dialog:
                FileSelector.show_message("Warning", msg, "warning")
            return False

        # Create directory
        os.makedirs(new_dir_path)
        
        # Log success
        logging.info(f"Created directory: {new_dir_path}")
        log_operation('create_directory', {'path': parent_path, 'name': directory_name})
        
        if show_dialog:
            FileSelector.show_message("Success", f"Created directory '{directory_name}'")
        return True

    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
    except Exception as e:
        error_msg = f"Error creating directory: {str(e)}"
        logging.error(error_msg)
        if show_dialog:
            FileSelector.show_message("Error", error_msg, "error")
        return False

def delete_directory(path, name):
    """Delete a specified directory."""
    try:
        full_path = os.path.join(path, name)
        if os.path.exists(full_path) and os.path.isdir(full_path):
            shutil.rmtree(full_path)
            logging.info(f"Deleted directory: {full_path}")
            log_operation('delete_directory', {'path': full_path})
        else:
            logging.warning(f"Directory does not exist: {full_path}")
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
    except Exception as e:
        logging.error(f"Error deleting directory {full_path}: {e}")

def list_files_in_directory(path):
    """List files in a specified directory."""
    try:
        if os.path.exists(path) and os.path.isdir(path):
            files = os.listdir(path)
            logging.info(f"Files in directory {path}: {files}")
            return files
        else:
            logging.warning(f"Directory does not exist: {path}")
            return []
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
    except Exception as e:
        logging.error(f"Error listing files in directory {path}: {e}")
        return []

def rename_directory(parent_path, old_name, new_name):
    """Rename a directory with optimized performance."""
    try:
        old_path = os.path.join(parent_path, old_name)
        new_path = os.path.join(parent_path, new_name)
        
        if not os.path.exists(old_path):
            raise FileNotFoundError(f"Directory '{old_name}' not found")
        if os.path.exists(new_path):
            raise FileExistsError(f"Directory '{new_name}' already exists")

        os.rename(old_path, new_path)
        logging.info(f"Renamed directory from '{old_name}' to '{new_name}'")
        log_operation('rename_directory', {'parent_path': parent_path, 'old_name': old_name, 'new_name': new_name})
        return True

    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
    except Exception as e:
        logging.error(f"Error renaming directory: {str(e)}")
        return False

def view_file_metadata(file_path):
    """View metadata of a file."""
    try:
        if os.path.exists(file_path):
            metadata = {
                "Size": os.path.getsize(file_path),
                "Created": time.ctime(os.path.getmtime(file_path)),
                "Type": mimetypes.guess_type(file_path)[0]
            }
            logging.info(f"Metadata for {file_path}: {metadata}")
            return metadata
        else:
            logging.warning(f"File does not exist: {file_path}")
            return None
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
    except Exception as e:
        logging.error(f"Error retrieving metadata for {file_path}: {e}")
        return None

def preview_file(file_path, lines=10):
    """Preview the first few lines of a text file."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as file:
            content = "".join([next(file) for _ in range(lines)])
        return content
    except StopIteration:
        # Handle case where the file has fewer lines than requested
        return content
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
        raise
    except Exception as e:
        logging.error(f"Error previewing file {file_path}: {e}")
        raise

