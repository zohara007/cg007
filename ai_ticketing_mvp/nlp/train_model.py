# nlp/train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_and_save_model():
    """
    Loads data, trains a ticket classification model, and saves it.
    """
    print("Starting model training...")

    # Define paths
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tickets_dataset.json')
    model_save_path = os.path.join(os.path.dirname(__file__), 'saved_models', 'ticket_classifier.joblib')
    
    # Ensure the directory for saving the model exists
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)

    # 1. Load Data
    try:
        df = pd.read_json(data_path)
        print(f"Data loaded successfully. Shape: {df.shape}")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # 2. Prepare Data
    X = df['description']
    y = df['category']

    # 3. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Data split into {len(X_train)} training and {len(X_test)} testing samples.")

    # 4. Create a Model Pipeline
    # This pipeline first converts text to a matrix of TF-IDF features,
    # then trains a Linear Support Vector Classifier.
    model_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', ngram_range=(1, 2))),
        ('clf', LinearSVC(random_state=42, C=0.5, class_weight='balanced'))
    ])

    # 5. Train the Model
    print("Training the model...")
    model_pipeline.fit(X_train, y_train)
    print("Model training completed.")

    # 6. Evaluate the Model
    y_pred = model_pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # 7. Save the trained model
    joblib.dump(model_pipeline, model_save_path)
    print(f"\nModel saved successfully to: {model_save_path}")

if __name__ == "__main__":
    train_and_save_model()