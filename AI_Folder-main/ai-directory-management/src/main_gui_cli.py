import os
import sys
import logging
import argparse
from ai.model import FileCategorizer
from utils.gui_operations import FileSelector
from utils.file_operations import (
    organize_files_task,summarize_file,display_log,
    sort_files_by_date, encrypt_file, decrypt_file, move_file, copy_file, delete_file, create_directory,
    delete_directory, list_files_in_directory, rename_directory,
    view_file_metadata, preview_file, deorganize_files, batch_rename_files,
)

def main():
    # Initialize logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    parser = argparse.ArgumentParser(description="File management operations using AI.")
    parser.add_argument("--gui", action="store_true", help="Use GUI mode")
    subparsers = parser.add_subparsers(dest="command")

    # Organize files
    parser_organize = subparsers.add_parser("organize", help="Categorizes and moves files into relevant folders.")
    parser_organize.add_argument("-s", "--source-directory", required=False, help="The source directory containing files to organize.")
    parser_organize.add_argument("-t", "--target-directory", required=False, help="The target directory where organized files will be placed.")

   

    # Move file or folder
    parser_move = subparsers.add_parser("move", help="Moves a file or folder to a new location.")
    parser_move.add_argument("--source", required=False, help="The source file or folder to move.")
    parser_move.add_argument("--destination", required=False, help="The destination path.")

    # Copy file or folder
    parser_copy = subparsers.add_parser("copy", help="Copies a file or folder to a new location.")
    parser_copy.add_argument("--source", required=False, help="The source file or folder to copy.")
    parser_copy.add_argument("--destination", required=False, help="The destination path.")

    # Delete file or folder
    parser_delete = subparsers.add_parser("delete", help="Deletes a specified file or folder.")
    parser_delete.add_argument("-p", "--path", required=False, help="The file or folder to delete.")

    # Create directory
    parser_create_directory = subparsers.add_parser("create-directory", help="Creates a new directory.")
    parser_create_directory.add_argument("-p", "--path", required=False, help="The path where the new directory will be created.")
    parser_create_directory.add_argument("-n", "--name", required=False, help="The name of the new directory.")

    # Delete directory
    parser_delete_directory = subparsers.add_parser("delete-directory", help="Deletes a specified directory.")
    parser_delete_directory.add_argument("-p", "--path", required=False, help="The path of the directory to delete.")
    parser_delete_directory.add_argument("-n", "--name", required=False, help="The name of the directory to delete.")

    # List files in directory
    parser_list_files = subparsers.add_parser("list-files", help="Lists files in a specified directory.")
    parser_list_files.add_argument("-p", "--path", required=False, help="The path of the directory to list files in.")

    # Rename directory
    parser_rename_directory = subparsers.add_parser("rename-directory", help="Renames a specified directory.")
    parser_rename_directory.add_argument("-p", "--path", required=False, help="The directory to rename.")
    parser_rename_directory.add_argument("-n", "--new-name", required=False, help="The new name for the directory.")
 
    # Display log
    subparsers.add_parser("log", help="Displays a log of previous operations.")

    # Sort files by date
    parser_sort_by_date = subparsers.add_parser("sort-by-date", help="Organizes files based on creation/modification date.")
    parser_sort_by_date.add_argument("-s", "--source-directory", required=False, help="The source directory containing files to sort.")
    parser_sort_by_date.add_argument("-t", "--target-directory", required=False, help="The target directory where sorted files will be placed.")

    # Encrypt file
    parser_encrypt = subparsers.add_parser("encrypt", help="Encrypts a file for security.")
    parser_encrypt.add_argument("-f", "--file", required=False, help="File to encrypt.")

    # Decrypt file
    parser_decrypt = subparsers.add_parser("decrypt", help="Decrypt a file.")
    parser_decrypt.add_argument("-f", "--file", required=False, help="File to decrypt.")

    # View metadata
    parser_metadata = subparsers.add_parser("view-metadata", help="View metadata of a file.")
    parser_metadata.add_argument("-f", "--file-path", required=False, help="The path to the file.")

    # Preview text file
    parser_preview = subparsers.add_parser("preview", help="Preview the first few lines of a text file.")
    parser_preview.add_argument("-f", "--file-path", required=False, help="The path to the text file.")
    parser_preview.add_argument("--lines", type=int, default=10, help="Number of lines to preview (default: 10).")

    # Deorganize files
    parser_deorganize = subparsers.add_parser("deorganize", help="Moves files from subdirectories back to the main directory.")
    parser_deorganize.add_argument("-s", "--source-directory", required=False, help="The source directory to deorganize.")

 
    args = parser.parse_args()

    if args.gui:
        # Handle GUI mode for all commands
        if args.command == "organize":
            source_dir = FileSelector.select_directory("Select Source Directory")
            if source_dir:
                target_dir = FileSelector.select_directory("Select Target Directory")
                if source_dir and target_dir:
                    model = FileCategorizer()
                    model.load_model()
                    organize_files_task(source_dir, target_dir, model)

        elif args.command == "move":
            source = FileSelector.select_file("Select File to Move")
            if source:
                destination = FileSelector.select_directory("Select Destination Directory")
                if destination:
                    move_file(source, os.path.join(destination, os.path.basename(source)))

        elif args.command == "copy":
            source = FileSelector.select_file("Select File to Copy")
            if source:
                destination = FileSelector.select_directory("Select Destination Directory")
                if destination:
                    copy_file(source, os.path.join(destination, os.path.basename(source)))

        # Handle other commands in GUI mode
        elif args.command == "delete":
            path = FileSelector.select_file("Select File or Folder to Delete")
            if path:
                if FileSelector.show_confirm("Confirm Delete", f"Are you sure you want to delete {os.path.basename(path)}?"):
                    delete_file(path)

        elif args.command == "create-directory":
            path = FileSelector.select_directory("Select Parent Directory")
            if path:
                # Use a simplified input dialog
                name = FileSelector.get_directory_name()
                if name:
                    create_directory(path, name)

        elif args.command == "delete-directory":
            path = FileSelector.select_directory("Select Directory to Delete")
            if path:
                name = os.path.basename(path)
                parent_path = os.path.dirname(path)
                if FileSelector.show_confirm("Confirm Delete", f"Are you sure you want to delete directory '{name}'?"):
                    delete_directory(parent_path, name)

        elif args.command == "list-files":
            path = FileSelector.select_directory("Select Directory to List Files")
            if path:
                files = list_files_in_directory(path)
                if files:
                    print("\nFiles in directory:")
                    for file in files:
                        print(f"  {file}")

        elif args.command == "rename-directory":
            current_path = FileSelector.select_directory("Select Directory to Rename")
            if current_path:
                parent_path = os.path.dirname(current_path)
                current_name = os.path.basename(current_path)
                new_name = FileSelector.get_simple_input("Enter new name:", current_name)
                if new_name and new_name != current_name:
                    rename_directory(parent_path, current_name, new_name)

        elif args.command == "summarize":
            file_path = FileSelector.select_file("Select File to Summarize", 
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("All files", "*.*")])
            if file_path:
                summarize_file(file_path)

       


        elif args.command == "log":
            display_log()

        elif args.command == "sort-by-date":
            source_directory = FileSelector.select_directory("Select Source Directory to Sort")
            if source_directory:
                target_directory = FileSelector.select_directory("Select Target Directory")
                if target_directory:
                    if FileSelector.show_confirm("Confirm Sort", 
                        f"Sort files from '{source_directory}' by date into '{target_directory}'?"):
                        sort_files_by_date(source_directory, target_directory)

        elif args.command == "encrypt":
            file = FileSelector.select_file("Select File to Encrypt")
            if file:
                if FileSelector.show_confirm("Confirm Encrypt", 
                    f"Are you sure you want to encrypt '{os.path.basename(file)}'?"):
                    encrypt_file(file)

        elif args.command == "decrypt":
            file = FileSelector.select_file("Select File to Decrypt")
            if file:
                if FileSelector.show_confirm("Confirm Decrypt", 
                    f"Are you sure you want to decrypt '{os.path.basename(file)}'?"):
                    decrypt_file(file)

 
        elif args.command == "view-metadata":
            file_path = FileSelector.select_file("Select File to View Metadata")
            if file_path:
                metadata = view_file_metadata(file_path)
                if metadata:
                    print("\nFile Metadata:")
                    for key, value in metadata.items():
                        print(f"  {key}: {value}")

        elif args.command == "preview":
            file_path = FileSelector.select_file(
                "Select Text File to Preview", 
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                lines_str = FileSelector.get_input(
                    "Preview Lines",
                    "Enter the number of lines to preview",
                    "10"
                )
                if lines_str:
                    try:
                        lines = int(lines_str)
                        content = preview_file(file_path, lines)
                        if content:
                            print("\nFile Preview:")
                            print(content)
                    except ValueError:
                        logging.error("Please enter a valid number")
                        FileSelector.show_message("Error", "Please enter a valid number", "error")

        elif args.command == "deorganize":
            source_directory = FileSelector.select_directory("Select Directory to Deorganize")
            if source_directory:
                deorganize_files(source_directory)
    
    else:
        # Handle CLI mode (existing code)
        if args.command == "organize":
            if args.source_directory and args.target_directory:
                model = FileCategorizer()
                model.load_model()
                organize_files_task(args.source_directory, args.target_directory, model)
            else:
                logging.error("Source and target directories are required in CLI mode")

        

        elif args.command == "move":
            move_file(args.source, args.destination)

        elif args.command == "copy":
            copy_file(args.source, args.destination)

        elif args.command == "delete":
            if args.path:
                delete_file(args.path)
            else:
                logging.error("Path is required in CLI mode")

        elif args.command == "create-directory":
            if args.path and args.name:
                create_directory(args.path, args.name)
            else:
                logging.error("Path and name are required in CLI mode")

        elif args.command == "delete-directory":
            if args.path and args.name:
                delete_directory(args.path, args.name)
            else:
                logging.error("Path and name are required in CLI mode")

        elif args.command == "list-files":
            if args.path:
                list_files_in_directory(args.path)
            else:
                logging.error("Path is required in CLI mode")

        elif args.command == "rename-directory":
            if args.path and args.old_name and args.new_name:
                rename_directory(args.path, args.old_name, args.new_name)
            else:
                logging.error("Path, old name, and new name are required in CLI mode")

        elif args.command == "summarize":
            if args.file:
                summarize_file(args.file)
            else:
                logging.error("File path is required in CLI mode")

       

        elif args.command == "log":
            display_log()

        elif args.command == "sort-by-date":
            if args.source_directory and args.target_directory:
                sort_files_by_date(args.source_directory, args.target_directory)
            else:
                logging.error("Source and target directories are required in CLI mode")

        elif args.command == "encrypt":
            if args.file:
                encrypt_file(args.file)
            else:
                logging.error("File path is required in CLI mode")

        elif args.command == "decrypt":
            if args.file:
                decrypt_file(args.file)
            else:
                logging.error("File path is required in CLI mode")

        elif args.command == "view-metadata":
            if args.file_path:
                metadata = view_file_metadata(args.file_path)
                if metadata:
                    print("\nFile Metadata:")
                    for key, value in metadata.items():
                        print(f"  {key}: {value}")
            else:
                logging.error("File path is required in CLI mode")

        elif args.command == "preview":
            if args.file_path:
                content = preview_file(args.file_path, args.lines)
                if content:
                    print("\nFile Preview:")
                    print(content)
            else:
                logging.error("File path is required in CLI mode")

        elif args.command == "deorganize":
            if args.source_directory:
                deorganize_files(args.source_directory)
            else:
                logging.error("Source directory is required in CLI mode")
 
        else:
            parser.print_help()

if __name__ == "__main__":
    main()