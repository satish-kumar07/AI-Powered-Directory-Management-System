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

def main():
    # Initialize logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    parser = argparse.ArgumentParser(description="File management operations using AI.")
    subparsers = parser.add_subparsers(dest="command")

    # Organize files
    parser_organize = subparsers.add_parser("organize", help="Categorizes and moves files into relevant folders.")
    parser_organize.add_argument("source_directory", help="The source directory containing files to organize.")
    parser_organize.add_argument("target_directory", help="The target directory where organized files will be placed.")

    # Find duplicates
    parser_find_duplicates = subparsers.add_parser("find-duplicates", help="Detects and lists duplicate files.")
    parser_find_duplicates.add_argument("directory", help="The directory to check for duplicate files.")

    # Move file or folder
    parser_move = subparsers.add_parser("move", help="Moves a file or folder to a new location.")
    parser_move.add_argument("source", help="The source file or folder to move.")
    parser_move.add_argument("destination", help="The destination path.")

    # Copy file or folder
    parser_copy = subparsers.add_parser("copy", help="Copies a file or folder to a new location.")
    parser_copy.add_argument("source", help="The source file or folder to copy.")
    parser_copy.add_argument("destination", help="The destination path.")

    # Delete file or folder
    parser_delete = subparsers.add_parser("delete", help="Deletes a specified file or folder.")
    parser_delete.add_argument("path", help="The file or folder to delete.")

    # Create directory
    parser_create_directory = subparsers.add_parser("create-directory", help="Creates a new directory.")
    parser_create_directory.add_argument("path", help="The path where the new directory will be created.")
    parser_create_directory.add_argument("name", help="The name of the new directory.")

    # Delete directory
    parser_delete_directory = subparsers.add_parser("delete-directory", help="Deletes a specified directory.")
    parser_delete_directory.add_argument("path", help="The path of the directory to delete.")
    parser_delete_directory.add_argument("name", help="The name of the directory to delete.")

    # List files in directory
    parser_list_files = subparsers.add_parser("list-files", help="Lists files in a specified directory.")
    parser_list_files.add_argument("path", help="The path of the directory to list files in.")

    # Rename directory
    parser_rename_directory = subparsers.add_parser("rename-directory", help="Renames a specified directory.")
    parser_rename_directory.add_argument("current_path", help="The current path of the directory.")
    parser_rename_directory.add_argument("current_name", help="The current name of the directory.")
    parser_rename_directory.add_argument("new_name", help="The new name of the directory.")

    # Search files
    parser_search = subparsers.add_parser("search", help="Finds files using AI-powered semantic search.")
    parser_search.add_argument("directory", help="The directory to search in.")
    parser_search.add_argument("keyword", help="Keyword to search for.")

    # Summarize file
    parser_summarize = subparsers.add_parser("summarize", help="Generates an AI-based summary of a text file.")
    parser_summarize.add_argument("file", help="File to summarize.")

    # Monitor directory
    parser_monitor = subparsers.add_parser("monitor", help="Watches the directory and organizes new files in real time.")
    parser_monitor.add_argument("source_directory", help="The source directory to monitor.")
    parser_monitor.add_argument("target_directory", help="The target directory where organized files will be placed.")

    # Undo last operation
    subparsers.add_parser("undo", help="Reverts the last file operation.")

    # Display log
    subparsers.add_parser("log", help="Displays a log of previous operations.")

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
    parser_deorganize.add_argument("source_directory", help="The source directory to deorganize.")

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

    if args.command == "organize":
        model = FileCategorizer()
        model.load_model()
        organize_files(args.source_directory, args.target_directory, model)
    elif args.command == "find-duplicates":
        find_duplicates(args.directory)
    elif args.command == "move":
        move_file(args.source, args.destination)
    elif args.command == "copy":
        copy_file(args.source, args.destination)
    elif args.command == "delete":
        delete_file(args.path)
    elif args.command == "create-directory":
        create_directory(args.path, args.name)
    elif args.command == "delete-directory":
        delete_directory(args.path, args.name)
    elif args.command == "list-files":
        list_files_in_directory(args.path)
    elif args.command == "rename-directory":
        rename_directory(args.current_path, args.current_name, args.new_name)
    elif args.command == "search":
        search_files(args.directory, args.keyword)
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
        deorganize_files(args.source_directory)
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