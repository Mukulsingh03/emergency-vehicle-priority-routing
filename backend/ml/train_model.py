import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Correct file path handling
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "training_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "delay_model.pkl")

def train():
    # Load dataset
    df = pd.read_csv(DATA_PATH)

    # Basic validation
    if df.empty:
        raise ValueError("Dataset is empty.")

    # Features
    X = df[["hour", "base_time"]]

    # Target
    y = df["delay"]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Model
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    # Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)

    print(f"MAE: {mae:.4f}")

    # Save model
    joblib.dump(model, MODEL_PATH)
    print("Model saved at:", MODEL_PATH)


if __name__ == "__main__":
    train()
