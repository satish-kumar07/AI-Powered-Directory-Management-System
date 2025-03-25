import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define a class for training the AI model
class ModelTrainer:
    def __init__(self, data_path, model_path):
        self.data_path = data_path
        self.model_path = model_path
        self.model = RandomForestClassifier()

    # Load labeled data for training
    def load_data(self):
        """Load labeled data for training."""
        if not os.path.exists(self.data_path):
            logging.error(f"Data file {self.data_path} does not exist.")
            return None
        data = pd.read_csv(self.data_path)
        return data

    # Preprocess the data for training
    def preprocess_data(self, data):
        """Preprocess the data for training."""
        X = data.drop('category', axis=1)  
        y = data['category'] 
        return train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the AI model
    def train_model(self, X_train, y_train):
        """Train the AI model."""
        self.model.fit(X_train, y_train)
        logging.info("Model training completed.")

    # Evaluate the trained model
    def evaluate_model(self, X_test, y_test):
        """Evaluate the trained model."""
        predictions = self.model.predict(X_test)
        report = classification_report(y_test, predictions)
        logging.info(f"Model evaluation report:\n{report}")

    # Save the trained model to a file
    def save_model(self):
        """Save the trained model to a file."""
        joblib.dump(self.model, self.model_path)
        logging.info(f"Model saved to {self.model_path}")

    # Run the training process
    def run(self):
        """Execute the training process."""
        data = self.load_data()
        if data is not None:
            X_train, X_test, y_train, y_test = self.preprocess_data(data)
            self.train_model(X_train, y_train)
            self.evaluate_model(X_test, y_test)
            self.save_model()

# Entry point for the training process
if __name__ == "__main__":
    # Define paths for the data file and the model file
    data_file = "d:/LANGUAGE/workspace/ai-directory-management/src/ai/labeled_data.csv"
    model_file = "d:/LANGUAGE/workspace/ai-directory-management/src/ai/model.pkl"

    # Create an instance of ModelTrainer and run the training process
    trainer = ModelTrainer(data_file, model_file)
    trainer.run()