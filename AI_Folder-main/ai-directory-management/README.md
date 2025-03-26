# AI Directory Management System

## Overview
The AI Directory Management System is designed to efficiently categorize and organize files using artificial intelligence. The system analyzes file content and metadata to predict appropriate categories, streamlining file management tasks.

## Example Directory Structure
Here is an example of how the files will be organized:

### Source Directory
```
source_folder/
├── image1.jpg
├── doc1.pdf
├── video1.mp4
├── script.py
├── image1_copy.jpg (duplicate)
```

### Target Directory
```
target_folder/
├── Images/
│   ├── image1.jpg
├── Documents/
│   ├── doc1.pdf
├── Videos/
│   ├── video1.mp4
├── Code/
│   ├── script.py
├── Duplicates/
│   ├── image1_copy.jpg
├── Others/
```

## Project Structure
```
ai-directory-management
├── src
│   ├── main.py                # Entry point of the application
│   ├── ai
│   │   ├── model.py           # AI model for predicting file categories
│   │   └── train.py           # Functions for training the AI model
│   ├── utils
│   │   ├── file_operations.py  # Utility functions for file operations
│   │   ├── logging_config.py   # Logging configuration
│   │   └── undo.py             # Undo functionality for file operations
│   ├── config
│   │   └── settings.py        # Configuration settings for the application
│   └── tests
│       ├── test_model.py      # Unit tests for the AI model
│       └── test_file_operations.py # Unit tests for file operations
├── requirements.txt            # Project dependencies
├── .gitignore                  # Files and directories to ignore in version control
└── README.md                   # Documentation for the project
```

## Setup Instructions
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd ai-directory-management
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Configure the application settings in `src/config/settings.py` to specify the source and target directories.

## Usage
To run the application, execute one of the following commands:

### GUI Mode
```sh
python src/main.py --gui <command>
```

### CLI Mode
```sh
python src/main.py <command> [arguments]
```

### Available Commands

- **organize**: Categorizes and moves files into relevant folders.
  ```sh
  # GUI Mode
  python src/main.py --gui organize

  # CLI Mode
  python src/main.py organize -s <source_directory> -t <target_directory>
  ```

- **find-duplicates**: Detects and lists duplicate files.
  ```sh
  # GUI Mode
  python src/main.py --gui find-duplicates

  # CLI Mode
  python src/main.py find-duplicates --directory <directory>
  ```

- **move**: Moves a file or folder to a new location.
  ```sh
  python src/main.py move --source <source> --destination <destination>
  ```

- **copy**: Copies a file or folder to a new location.
  ```sh
  python src/main.py copy --source <source> --destination <destination>
  ```

- **delete**: Deletes a specified file or folder.
  ```sh
  python src.main.py delete -p <path>
  ```

- **summarize**: Generates an AI-based summary of a text file.
  ```sh
  python src/main.py summarize -f <file>
  ```

- **monitor**: Watches the directory and organizes new files in real time.
  ```sh
  python src/main.py monitor -s <source_directory> -t <target_directory>
  ```

- **undo**: Reverts the last file operation.
  ```sh
  python src/main.py undo
  ```

- **log**: Displays a log of previous operations.
  ```sh
  python src/main.py log
  ```

- **sort-by-date**: Organizes files based on creation/modification date.
  ```sh
  python src/main.py sort-by-date -s <source_directory> -t <target_directory>
  ```

- **encrypt**: Encrypts a file for security.
  ```sh
  python src/main.py encrypt -f <file>
  ```

- **decrypt**: Decrypts an encrypted file.
  ```sh
  python src/main.py decrypt -f <file>
  ```

- **create-directory**: Creates a new directory.
  ```sh
  python src/main.py create-directory -p <path> -n <directory_name>
  ```

- **delete-directory**: Deletes a specified directory.
  ```sh
  python src/main.py delete-directory -p <path> -n <directory_name>
  ```

- **list-files**: Lists files in a specified directory.
  ```sh
  python src/main.py list-files -p <directory>
  ```

- **rename-directory**: Renames a specified directory.
  ```sh
  python src/main.py rename-directory -p <path> -n <new_name>
  ```

- **deorganize**: Moves files from subdirectories back to the main directory.
  ```sh
  python src/main.py deorganize -s <source_directory>
  ```

- **view-metadata**: Displays metadata of a file.
  ```sh
  # GUI Mode
  python src/main.py --gui view-metadata

  # CLI Mode
  python src/main.py view-metadata -f <file_path>
  ```

- **preview**: Previews the first few lines of a text file.
  ```sh
  # GUI Mode
  python src/main.py --gui preview

  # CLI Mode
  python src/main.py preview -f <file_path> --lines <number_of_lines>
  ```

- **batch-rename**: Renames multiple files in a directory based on a pattern.
  ```sh
  # GUI Mode
  python src/main.py --gui batch-rename

  # CLI Mode
  python src/main.py batch-rename -d <directory> -p <pattern> -r <replacement>
  ```

- **disk-usage**: Analyzes disk usage of directories and files.
  ```sh
  # GUI Mode
  python src/main.py --gui disk-usage

  # CLI Mode
  python src/main.py disk-usage -d <directory>
  ```

- **compare**: Compares two directories and reports differences.
  ```sh
  # GUI Mode
  python src/main.py --gui compare

  # CLI Mode
  python src/main.py compare -d1 <first_directory> -d2 <second_directory>
  ```

## Features
- **AI-based File Categorization**: Uses content and metadata analysis to categorize files into predefined categories.
- **Efficient File Organization**: Automatically organizes files into folders based on their categories.
- **Duplicate Detection**: Identifies and categorizes duplicate files.
- **Logging**: Logs file operations for tracking and debugging purposes.
- **Undo Last Operation**: Reverts the last file operation performed.
- **File Encryption**: Encrypts files for security.
- **File Sorting by Date**: Organizes files based on their creation or modification date.
- **Continuous Monitoring**: Optionally monitor the source directory for changes and automatically organize new files.
- **Directory Management**: Create, delete, list, and rename directories.
- **Deorganization**: Moves files from subdirectories back to the main directory.
- **Compression and Decompression**: Compresses directories into zip files and extracts them.
- **Batch Rename**: Renames multiple files in a directory based on a pattern.
- **Disk Usage Analysis**: Analyzes disk usage of directories and files.
- **Directory Comparison**: Compares two directories and reports differences.

## Techniques Used
The AI Directory Management System uses a combination of techniques to categorize and organize files:

1. **File Metadata Analysis**:
   - The system analyzes file metadata, such as file type and file extension, to predict the appropriate category for each file.
   - This is done using the `predict_category` method in the `FileCategorizer` class, which checks the file type and assigns a category based on predefined rules.

2. **Duplicate Detection**:
   - The system detects duplicate files by calculating the hash of each file's content.
   - This is done using the `calculate_file_hash` method in the `FileCategorizer` class, which uses the `hashlib` library to generate a unique hash for each file.
   - If a file with the same hash already exists, it is categorized as a duplicate.

3. **File Organization**:
   - The system organizes files into folders based on their predicted categories.
   - This is done using the `organize_files` function in the `file_operations.py` module, which moves files to the appropriate target directories based on their categories.

4. **Deorganization**:
   - The system can reverse the organization process by moving files from subdirectories back to the main directory.
   - This is done using the `deorganize_files` function in the `file_operations.py` module.

5. **Batch Rename**:
   - Renames multiple files in a directory based on a pattern.

6. **Disk Usage Analysis**:
   - Analyzes disk usage of directories and files.

8. **Directory Comparison**:
   - Compares two directories and reports differences.

## Import Libraries
The following libraries are used in this project:
- **os**: For interacting with the operating system, such as file and directory operations.
- **sys**: For accessing command-line arguments.
- **joblib**: For loading and saving the AI model.
- **shutil**: For high-level file operations, such as copying and moving files.
- **hashlib**: For calculating file hashes to detect duplicates.
- **logging**: For logging file operations and debugging information.
- **watchdog**: For monitoring the file system for changes.
- **cryptography**: For file encryption.
- **argparse**: For parsing command-line arguments.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.
