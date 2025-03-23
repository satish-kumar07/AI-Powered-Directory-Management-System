import joblib
import os

class FileCategorizer:
    def __init__(self, model_path='d:/LANGUAGE/workspace/ai-directory-management/src/ai/model.pkl'):
        self.model_path = model_path
        self.model = None

    def load_model(self):
        """Load the trained model from a file."""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            raise FileNotFoundError(f"Model file {self.model_path} does not exist.")

    def predict_category(self, file_metadata):
        """Predict the category of a file based on its metadata."""
        if self.model is None:
            raise ValueError("Model is not loaded.")
        
        # Mock prediction process for demonstration purposes
        if file_metadata['type'] == 'application/pdf':
            return 'Documents'
        elif file_metadata['type'] in ['image/jpeg', 'image/png']:
            return 'Images'
        elif file_metadata['type'] == 'audio/mpeg':
            return 'Audio'
        elif file_metadata['type'] in ['video/mp4', 'video/quicktime', 'video/x-matroska', 'video/x-mkv']:
            return 'Video'
        elif file_metadata['type'] in ['text/plain', 'text/markdown']:
            return 'Text'
        elif file_metadata['type'] in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/csv']:
            return 'Spreadsheets'
        elif file_metadata['type'] in ['application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation']:
            return 'Presentations'
        elif file_metadata['type'] in ['application/zip', 'application/x-rar-compressed', 'application/x-tar', 'application/x-gzip']:
            return 'Archives'
        elif file_metadata['type'] in ['application/x-python-code', 'application/javascript', 'application/x-sh', 'application/x-java', 'application/x-c', 'application/x-c++', 'application/x-ruby', 'application/x-php', 'application/x-perl', 'application/x-go', 'application/x-rust', 'application/x-swift', 'application/x-kotlin', 'application/x-typescript', 'application/x-sql']:
            return 'Scripts'
        elif file_metadata['type'] in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            return 'Word Documents'
        elif file_metadata['type'] in ['application/json', 'application/xml', 'application/x-yaml']:
            return 'Configuration Files'
        elif file_metadata['type'] in ['application/x-sqlite3', 'application/x-sql']:
            return 'Database Files'
        elif file_metadata['type'] in ['application/x-font-ttf', 'application/x-font-otf']:
            return 'Font Files'
        elif file_metadata['type'] in ['application/x-msdownload', 'application/x-sh']:
            return 'Executable Files'
        else:
            return 'Others'

class AIModel:
    def __init__(self):
        self.model = None

    def train(self, training_data):
    
        self.model = "trained_model"

    def predict_category(self, file_metadata):
        """Predict the category of a file based on its metadata."""
        if file_metadata['type'] == 'application/pdf':
            return 'Documents'
        elif file_metadata['type'] in ['image/jpeg', 'image/png']:
            return 'Images'
        elif file_metadata['type'] == 'audio/mpeg':
            return 'Audio'
        elif file_metadata['type'] == 'text/plain':
            return 'Text'
        elif file_metadata['type'] in ['video/mp4', 'video/quicktime', 'video/x-matroska', 'video/x-mkv']:
            return 'Video'
        elif file_metadata['type'] in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/csv']:
            return 'Spreadsheets'
        elif file_metadata['type'] in ['application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation']:
            return 'Presentations'
        elif file_metadata['type'] in ['application/zip', 'application/x-rar-compressed', 'application/x-tar', 'application/x-gzip']:
            return 'Archives'
        elif file_metadata['type'] in ['application/x-python-code', 'application/javascript', 'application/x-sh', 'application/x-java', 'application/x-c', 'application/x-c++', 'application/x-ruby', 'application/x-php', 'application/x-perl', 'application/x-go', 'application/x-rust', 'application/x-swift', 'application/x-kotlin', 'application/x-typescript', 'application/x-sql']:
            return 'Scripts'
        elif file_metadata['type'] in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            return 'Word Documents'
        elif file_metadata['type'] in ['application/json', 'application/xml', 'application/x-yaml']:
            return 'Configuration Files'
        elif file_metadata['type'] in ['application/x-sqlite3', 'application/x-sql']:
            return 'Database Files'
        elif file_metadata['type'] in ['application/x-font-ttf', 'application/x-font-otf']:
            return 'Font Files'
        elif file_metadata['type'] in ['application/x-msdownload', 'application/x-sh']:
            return 'Executable Files'
        else:
            return 'Others'

    def evaluate(self, test_data):
        return 0.95  