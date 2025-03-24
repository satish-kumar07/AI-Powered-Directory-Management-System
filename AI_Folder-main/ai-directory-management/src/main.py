import os
import sys
import logging
import argparse
from ai.model import FileCategorizer
from utils.file_operations import (
    organize_files, find_duplicates, search_files, summarize_file, monitor_directory, display_log,
    sort_files_by_date, encrypt_file, decrypt_file, move_file, copy_file, delete_file, create_directory,
    delete_directory, list_files_in_directory, rename_directory, create_text_file, create_video_file, create_word_file,
    compress_directory, decompress_file, view_file_metadata, preview_file, deorganize_files, batch_rename_files, analyze_disk_usage, compare_directories
)
from utils.undo import undo_last_operation
from utils.gui_operations import FileSelector

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

    # Find duplicates
    parser_find_duplicates = subparsers.add_parser("find-duplicates", help="Detects and lists duplicate files.")
    parser_find_duplicates.add_argument("--directory", required=False, help="The directory to check for duplicate files.")

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

    # Summarize file
    parser_summarize = subparsers.add_parser("summarize", help="Generates an AI-based summary of a text file.")
    parser_summarize.add_argument("file", help="File to summarize.")

    # Monitor directory
    parser_monitor = subparsers.add_parser("monitor", help="Watches the directory and organizes new files in real time.")
    parser_monitor.add_argument("source_directory", help="The source directory to monitor.")
    parser_monitor.add_argument("target_directory", help="The target directory where organized files will be placed.")

    # Undo last operation
    subparsers.add_parser("undo", help="Reverts the last file operation.")

    # Sort files by date
    parser_sort_by_date = subparsers.add_parser("sort-by-date", help="Organizes files based on creation/modification date.")
    parser_sort_by_date.add_argument("source_directory", help="The source directory containing files to sort.")
    parser_sort_by_date.add_argument("target_directory", help="The target directory where sorted files will be placed.")

    # Encrypt file
    parser_encrypt = subparsers.add_parser("encrypt", help="Encrypts a file for security.")
    parser_encrypt.add_argument("file", help="File to encrypt.")

    # Decrypt file
    parser_decrypt = subparsers.add_parser("decrypt", help="Decrypt a file.")
    parser_decrypt.add_argument("file", help="File to decrypt.")

    # Create text file
    parser_create_text_file = subparsers.add_parser("create-text-file", help="Creates a new text file.")
    parser_create_text_file.add_argument("path", help="The path where the text file will be created.")
    parser_create_text_file.add_argument("name", help="The name of the text file (without extension).")
    parser_create_text_file.add_argument("--content", help="Optional content for the text file.", default="")

    # Create video file
    parser_create_video_file = subparsers.add_parser("create-video-file", help="Creates a new video file.")
    parser_create_video_file.add_argument("path", help="The path where the video file will be created.")
    parser_create_video_file.add_argument("name", help="The name of the video file (without extension).")

    # Create Word file
    parser_create_word_file = subparsers.add_parser("create-word-file", help="Creates a new MS Word document.")
    parser_create_word_file.add_argument("path", help="The path where the Word document will be created.")
    parser_create_word_file.add_argument("name", help="The name of the Word document (without extension).")
    parser_create_word_file.add_argument("--content", help="Optional content for the Word document.", default="")

    # Compress directory
    parser_compress = subparsers.add_parser("compress", help="Compress a directory into a zip file.")
    parser_compress.add_argument("path", help="The directory to compress.")
    parser_compress.add_argument("output_name", help="The name of the output zip file (without extension).")

    # Decompress zip file
    parser_decompress = subparsers.add_parser("decompress", help="Decompress a zip file.")
    parser_decompress.add_argument("zip_path", help="The path to the zip file.")
    parser_decompress.add_argument("extract_to", help="The directory to extract the contents to.")

    # View metadata
    parser_metadata = subparsers.add_parser("view-metadata", help="View metadata of a file.")
    parser_metadata.add_argument("file_path", help="The path to the file.")

    # Preview text file
    parser_preview = subparsers.add_parser("preview", help="Preview the first few lines of a text file.")
    parser_preview.add_argument("file_path", help="The path to the text file.")
    parser_preview.add_argument("--lines", type=int, default=10, help="Number of lines to preview (default: 10).")

    # Deorganize files
    parser_deorganize = subparsers.add_parser("deorganize", help="Moves files from subdirectories back to the main directory.")
    parser_deorganize.add_argument("-s", "--source-directory", required=False, help="The source directory to deorganize.")

    # Batch rename
    parser_batch_rename = subparsers.add_parser("batch-rename", help="Rename multiple files based on a pattern.")
    parser_batch_rename.add_argument("directory", help="The directory containing files to rename.")
    parser_batch_rename.add_argument("pattern", help="The pattern to search for in filenames.")
    parser_batch_rename.add_argument("replacement", help="The replacement text.")

    # Analyze disk usage
    parser_disk_usage = subparsers.add_parser("disk-usage", help="Analyze disk usage of directories and files.")
    parser_disk_usage.add_argument("directory", help="The directory to analyze.")

    # Compare directories
    parser_compare = subparsers.add_parser("compare", help="Compare two directories and report differences.")
    parser_compare.add_argument("dir1", help="First directory to compare.")
    parser_compare.add_argument("dir2", help="Second directory to compare.")

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
                    organize_files(source_dir, target_dir, model)

        elif args.command == "find-duplicates":
            directory = FileSelector.select_directory("Select Directory to Check for Duplicates")
            if directory:
                find_duplicates(directory)

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
            file = FileSelector.select_file("Select File to Summarize")
            if file:
                summarize_file(file)

        elif args.command == "monitor":
            source_directory = FileSelector.select_directory("Select Source Directory to Monitor")
            if source_directory:
                target_directory = FileSelector.select_directory("Select Target Directory")
                if target_directory:
                    model = FileCategorizer()
                    model.load_model()
                    monitor_directory(source_directory, target_directory, model)

        elif args.command == "undo":
            undo_last_operation()


        elif args.command == "sort-by-date":
            source_directory = FileSelector.select_directory("Select Source Directory to Sort")
            if source_directory:
                target_directory = FileSelector.select_directory("Select Target Directory")
                if target_directory:
                    sort_files_by_date(source_directory, target_directory)

        elif args.command == "encrypt":
            file = FileSelector.select_file("Select File to Encrypt")
            if file:
                encrypt_file(file)

        elif args.command == "decrypt":
            file = FileSelector.select_file("Select File to Decrypt")
            if file:
                decrypt_file(file)

        elif args.command == "create-text-file":
            path = FileSelector.select_directory("Select Directory")
            if path:
                file_info = FileSelector.get_file_info(
                    title="Create Text File",
                    name_prompt="Enter file name (without extension):",
                    content_prompt="Enter file content (optional):"
                )
                if file_info["name"]:
                    create_text_file(path, file_info["name"], file_info.get("content", ""))

        elif args.command == "create-video-file":
            path = FileSelector.select_directory("Select Directory")
            if path:
                file_info = FileSelector.get_file_info(
                    title="Create Video File",
                    name_prompt="Enter video file name (without extension):"
                )
                if file_info["name"]:
                    create_video_file(path, file_info["name"])

        elif args.command == "create-word-file":
            path = FileSelector.select_directory("Select Directory")
            if path:
                file_info = FileSelector.get_file_info(
                    title="Create Word Document",
                    name_prompt="Enter document name (without extension):",
                    content_prompt="Enter document content (optional):"
                )
                if file_info["name"]:
                    create_word_file(path, file_info["name"], file_info.get("content", ""))

        elif args.command == "compress":
            path = FileSelector.select_directory("Select Directory to Compress")
            if path:
                output_name = input("Enter the name of the output zip file (without extension): ")
                compress_directory(path, output_name)

        elif args.command == "decompress":
            zip_path = FileSelector.select_file("Select Zip File to Decompress")
            if zip_path:
                extract_to = FileSelector.select_directory("Select Directory to Extract Contents")
                if extract_to:
                    decompress_file(zip_path, extract_to)

        elif args.command == "view-metadata":
            file_path = FileSelector.select_file("Select File to View Metadata")
            if file_path:
                metadata = view_file_metadata(file_path)
                if metadata:
                    print(metadata)

        elif args.command == "preview":
            file_path = FileSelector.select_file("Select Text File to Preview")
            if file_path:
                lines = int(input("Enter the number of lines to preview (default: 10): ") or 10)
                content = preview_file(file_path, lines)
                if content:
                    print(content)

        elif args.command == "deorganize":
            source_directory = FileSelector.select_directory("Select Directory to Deorganize")
            if source_directory:
                deorganize_files(source_directory)

        elif args.command == "batch-rename":
            directory = FileSelector.select_directory("Select Directory to Batch Rename Files")
            if directory:
                pattern = input("Enter the pattern to search for in filenames: ")
                replacement = input("Enter the replacement text: ")
                batch_rename_files(directory, pattern, replacement)

        elif args.command == "disk-usage":
            directory = FileSelector.select_directory("Select Directory to Analyze Disk Usage")
            if directory:
                usage_data = analyze_disk_usage(directory)
                if usage_data:
                    print("\nDisk Usage Analysis:")
                    for dir_path, data in usage_data.items():
                        print(f"{dir_path}:")
                        print(f"  Size: {data['size']/1024/1024:.2f} MB")
                        print(f"  Percentage: {data['percentage']:.2f}%")

        elif args.command == "compare":
            dir1 = FileSelector.select_directory("Select First Directory to Compare")
            if dir1:
                dir2 = FileSelector.select_directory("Select Second Directory to Compare")
                if dir2:
                    differences = compare_directories(dir1, dir2)
                    if differences:
                        print("\nDirectory Comparison Results:")
                        print(f"\nFiles only in {dir1}:")
                        for file in differences['only_in_first']:
                            print(f"  {file}")
                        print(f"\nFiles only in {dir2}:")
                        for file in differences['only_in_second']:
                            print(f"  {file}")
                        print("\nFiles with different content:")
                        for file in differences['different_files']:
                            print(f"  {file}")

    else:
        # Handle CLI mode (existing code)
        if args.command == "organize":
            if args.source_directory and args.target_directory:
                model = FileCategorizer()
                model.load_model()
                organize_files(args.source_directory, args.target_directory, model)
            else:
                logging.error("Source and target directories are required in CLI mode")

        elif args.command == "find-duplicates":
            if args.directory:
                find_duplicates(args.directory)
            else:
                logging.error("Directory is required in CLI mode")

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

        elif args.command == "search":
            if args.directory and args.keyword:
                search_files(args.directory, args.keyword)
            else:
                logging.error("Directory and keyword are required in CLI mode")

        elif args.command == "summarize":
            summarize_file(args.file)

        elif args.command == "monitor":
            model = FileCategorizer()
            model.load_model()
            monitor_directory(args.source_directory, args.target_directory, model)

        elif args.command == "undo":
            undo_last_operation()

        elif args.command == "log":
            display_log()

        elif args.command == "sort-by-date":
            sort_files_by_date(args.source_directory, args.target_directory)

        elif args.command == "encrypt":
            encrypt_file(args.file)

        elif args.command == "decrypt":
            decrypt_file(args.file)

        elif args.command == "create-text-file":
            create_text_file(args.path, args.name, args.content)

        elif args.command == "create-video-file":
            create_video_file(args.path, args.name)

        elif args.command == "create-word-file":
            create_word_file(args.path, args.name, args.content)

        elif args.command == "compress":
            compress_directory(args.path, args.output_name)

        elif args.command == "decompress":
            decompress_file(args.zip_path, args.extract_to)

        elif args.command == "view-metadata":
            metadata = view_file_metadata(args.file_path)
            if metadata:
                print(metadata)

        elif args.command == "preview":
            content = preview_file(args.file_path, args.lines)
            if content:
                print(content)

        elif args.command == "deorganize":
            if args.source_directory:
                deorganize_files(args.source_directory)
            else:
                logging.error("Source directory is required in CLI mode")

        elif args.command == "batch-rename":
            batch_rename_files(args.directory, args.pattern, args.replacement)

        elif args.command == "disk-usage":
            usage_data = analyze_disk_usage(args.directory)
            if usage_data:
                print("\nDisk Usage Analysis:")
                for dir_path, data in usage_data.items():
                    print(f"{dir_path}:")
                    print(f"  Size: {data['size']/1024/1024:.2f} MB")
                    print(f"  Percentage: {data['percentage']:.2f}%")

        elif args.command == "compare":
            differences = compare_directories(args.dir1, args.dir2)
            if differences:
                print("\nDirectory Comparison Results:")
                print(f"\nFiles only in {args.dir1}:")
                for file in differences['only_in_first']:
                    print(f"  {file}")
                print(f"\nFiles only in {args.dir2}:")
                for file in differences['only_in_second']:
                    print(f"  {file}")
                print("\nFiles with different content:")
                for file in differences['different_files']:
                    print(f"  {file}")
        else:
            parser.print_help()

if __name__ == "__main__":
    main()