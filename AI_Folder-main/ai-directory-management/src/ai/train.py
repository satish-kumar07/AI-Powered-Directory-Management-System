import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class ModelTrainer:
    def __init__(self, data_path, model_path):
        self.data_path = data_path
        self.model_path = model_path
        self.model = RandomForestClassifier()

    def load_data(self):
        """Load labeled data for training."""
        if not os.path.exists(self.data_path):
            logging.error(f"Data file {self.data_path} does not exist.")
            return None
        data = pd.read_csv(self.data_path)
        return data

    def preprocess_data(self, data):
        """Preprocess the data for training."""
        X = data.drop('category', axis=1)  # Features
        y = data['category']  # Target
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train_model(self, X_train, y_train):
        """Train the AI model."""
        self.model.fit(X_train, y_train)
        logging.info("Model training completed.")

    def evaluate_model(self, X_test, y_test):
        """Evaluate the trained model."""
        predictions = self.model.predict(X_test)
        report = classification_report(y_test, predictions)
        logging.info(f"Model evaluation report:\n{report}")

    def save_model(self):
        """Save the trained model to a file."""
        joblib.dump(self.model, self.model_path)
        logging.info(f"Model saved to {self.model_path}")

    def run(self):
        """Execute the training process."""
        data = self.load_data()
        if data is not None:
            X_train, X_test, y_train, y_test = self.preprocess_data(data)
            self.train_model(X_train, y_train)
            self.evaluate_model(X_test, y_test)
            self.save_model()

# Example usage
if __name__ == "__main__":
    data_file = "d:/LANGUAGE/workspace/ai-directory-management/src/ai/labeled_data.csv"  # Replace with your labeled data file path
    model_file = "d:/LANGUAGE/workspace/ai-directory-management/src/ai/model.pkl"  # Replace with your desired model file path

    trainer = ModelTrainer(data_file, model_file)
    trainer.run()