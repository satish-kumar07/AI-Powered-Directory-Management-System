# Configuration settings for the AI-based directory management system

SOURCE_DIRECTORY = "D:\LANGUAGE\workspace\source"  # Replace with the actual source directory path
TARGET_DIRECTORY = "D:\LANGUAGE\workspace\target"  # Replace with the actual target directory path

AI_MODEL_PARAMETERS = {
    "learning_rate": 0.001,
    "batch_size": 32,
    "num_epochs": 10,
    "input_shape": (224, 224, 3),  # Example input shape for image data
}

LOGGING_SETTINGS = {
    "log_file": "ai_directory_management.log",
    "log_level": "INFO",
}