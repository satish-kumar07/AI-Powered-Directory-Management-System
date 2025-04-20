import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import logging
from collections import Counter

# Set up logging
logging.basicConfig(level=logging.INFO)

class ModelTrainer:
    def __init__(self, data_path, model_path):
        self.data_path = data_path
        self.model_path = model_path
        self.model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)

    def load_data(self):
        """Load labeled data from CSV."""
        if not os.path.exists(self.data_path):
            logging.error(f"Data file {self.data_path} does not exist.")
            return None
        data = pd.read_csv(self.data_path)
        logging.info(f"Loaded dataset with shape: {data.shape}")
        return data

    def preprocess_data(self, data):
        """Preprocess features and labels, handle class balancing."""
        X = data.drop('category', axis=1)
        y = data['category']

        # Count the number of classes
        class_counts = y.value_counts()
        num_classes = len(class_counts)

        # Calculate minimum required test size to have at least 1 sample per class
        min_test_size = num_classes / len(y) + 0.05  # + a little buffer

        test_size = max(0.3, min_test_size)  # ensure test size isn't too small

        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )
            logging.info("Stratified train/test split successful.")
        except ValueError as e:
            logging.warning(f"Stratified split failed: {e}")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )
            logging.info("Used non-stratified train/test split as fallback.")

        logging.info(f"Train label distribution: {Counter(y_train)}")
        logging.info(f"Test label distribution: {Counter(y_test)}")

        return X_train, X_test, y_train, y_test

    def train_model(self, X_train, y_train):
        """Train the model using Random Forest."""
        self.model.fit(X_train, y_train)
        logging.info("Model training completed.")

    def evaluate_model(self, X_test, y_test):
        """Print classification metrics."""
        predictions = self.model.predict(X_test)
        report = classification_report(y_test, predictions, zero_division=1)
        logging.info(f"Model evaluation report:\n{report}")

    def save_model(self):
        """Save the model to disk."""
        joblib.dump(self.model, self.model_path)
        logging.info(f"Model saved to {self.model_path}")

    def run(self):
        """Complete training process: load, split, train, evaluate, save."""
        data = self.load_data()
        if data is not None:
            X_train, X_test, y_train, y_test = self.preprocess_data(data)
            self.train_model(X_train, y_train)
            self.evaluate_model(X_test, y_test)
            self.save_model()

# ---- Main execution ----
if __name__ == "__main__":
    data_file = "d:/LANGUAGE/workspace/ai-directory-management/src/ai/labeled_data.csv"
    model_file = "d:/LANGUAGE/workspace/ai-directory-management/src/ai/model.pkl"

    trainer = ModelTrainer(data_file, model_file)
    trainer.run()
