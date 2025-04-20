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

- **move**: Moves a file
  ```sh
  # GUI Mode
  python src/main.py --gui move

  # CLI Mode
  python src/main.py move --source <source> --destination <destination>
  ```

- **copy**: Copies a file
  ```sh
  # GUI Mode
  python src/main.py --gui copy

  # CLI Mode
  python src/main.py copy --source <source> --destination <destination>
  ```

- **delete**: Deletes a specified file or folder.
  ```sh
  # GUI Mode
  python src/main.py --gui delete

  # CLI Mode
  python src/main.py delete -p <path>
  ```

- **log**: Displays a log of previous operations.
  ```sh
  # GUI Mode
  python src/main.py --gui log

  # CLI Mode
  python src/main.py log
  ```

- **sort-by-date**: Organizes files based on creation/modification date.
  ```sh
  # GUI Mode
  python src/main.py --gui sort-by-date

  # CLI Mode
  python src/main.py sort-by-date -s <source_directory> -t <target_directory>
  ```

- **encrypt**: Encrypts a file for security.
  ```sh
  # GUI Mode
  python src/main.py --gui encrypt

  # CLI Mode
  python src/main.py encrypt -f <file>
  ```

- **decrypt**: Decrypts an encrypted file.
  ```sh
  # GUI Mode
  python src/main.py --gui decrypt

  # CLI Mode
  python src/main.py decrypt -f <file>
  ```

- **create-directory**: Creates a new directory.
  ```sh
  # GUI Mode
  python src/main.py --gui create-directory

  # CLI Mode
  python src/main.py create-directory -p <path> -n <directory_name>
  ```

- **delete-directory**: Deletes a specified directory.
  ```sh
  # GUI Mode
  python src/main.py --gui delete-directory

  # CLI Mode
  python src/main.py delete-directory -p <path> -n <directory_name>
  ```

- **list-files**: Lists files in a specified directory.
  ```sh
  # GUI Mode
  python src/main.py --gui list-files

  # CLI Mode
  python src/main.py list-files -p <directory>
  ```

- **rename-directory**: Renames a specified directory.
  ```sh
  # GUI Mode
  python src/main.py --gui rename-directory

  # CLI Mode
  python src/main.py rename-directory -p <path> -n <new_name>
  ```

- **deorganize**: Moves files from subdirectories back to the main directory.
  ```sh
  # GUI Mode
  python src/main.py --gui deorganize

  # CLI Mode
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

## Features
- **AI-based File Categorization**: Uses content and metadata analysis to categorize files into predefined categories.
- **Efficient File Organization**: Automatically organizes files into folders based on their categories.
- **Logging**: Logs file operations for tracking and debugging purposes.
- **File Encryption**: Encrypts files for security.
- **File Sorting by Date**: Organizes files based on their creation or modification date.

- **Directory Management**: Create, delete, list, and rename directories.
- **Deorganization**: Moves files from subdirectories back to the main directory.

## How AI Works in This Project

### Overview
This project uses Artificial Intelligence (AI) to automate the categorization and organization of files based on their metadata (e.g., file size, type, creation date). The AI model is trained to recognize patterns in file metadata and predict the appropriate category for each file.

### How It Works
1. **Training the AI Model:**
   - The AI model is trained using labeled data stored in a CSV file (`labeled_data.csv`).
   - A **Random Forest Classifier** is used to learn how file metadata maps to categories (e.g., Images, Documents, Videos).
   - After training, the model is saved as a `.pkl` file (`trained_model.pkl`) for reuse.

2. **Using the Trained Model:**
   - The trained model is loaded in the project using the `FileCategorizer` class in `model.py`.
   - The `predict_category` method takes file metadata as input and predicts the category of the file.

3. **File Categorization:**
   - During file organization, the AI model predicts the category of each file.
   - Files are then moved to corresponding folders (e.g., Images, Documents) based on the predicted category.

### Role of AI in the Project
1. **Automated File Categorization:**
   - AI eliminates the need for manual file sorting by automatically categorizing files into predefined categories.

2. **Improved Accuracy:**
   - The AI model learns from training data, enabling it to make accurate predictions even for new or unseen files.

3. **Scalability:**
   - The AI-based approach can handle large numbers of files efficiently, making it suitable for real-world applications.

4. **Customizability:**
   - The AI model can be retrained with new data to adapt to additional categories or changing requirements.

5. **Integration with File Operations:**
   - The AI model is seamlessly integrated with file operations, such as organizing files, sorting by category, and handling duplicates.

### Example Workflow
1. A user selects a source directory to organize.
2. The AI model predicts the category of each file in the directory based on its metadata.
3. Files are moved to corresponding folders (e.g., Images, Documents) in the target directory.

By leveraging AI, this project provides an intelligent and efficient solution for file management.

## Classification Metrics: Precision, Recall, F1-Score, and Support

When evaluating the performance of classification models (such as the AI model used in this project), several key metrics are used:

- **Precision**: Out of all the instances the model predicted as positive, what proportion were actually positive? Precision focuses on minimizing false positives (false alarms).
  - **Formula**: Precision = TP / (TP + FP), where TP is true positives and FP is false positives.

- **Recall (Sensitivity)**: Out of all the actual positive instances, what proportion did the model correctly identify? Recall focuses on minimizing false negatives (missed opportunities).
  - **Formula**: Recall = TP / (TP + FN), where TP is true positives and FN is false negatives.

- **F1-Score**: The harmonic mean of precision and recall, providing a single metric that balances both. The F1-score is especially useful when precision and recall are in trade-off, such as with imbalanced datasets.
  - **Formula**: F1 = 2 * (precision * recall) / (precision + recall)

- **Support**: The number of actual occurrences of a class in the dataset. It represents the total number of instances belonging to that class.

These metrics help you understand how well your AI model is performing in categorizing files, especially when dealing with multiple categories or imbalanced data.

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
