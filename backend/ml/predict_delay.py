import os
import joblib
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "delay_model.pkl")

model = joblib.load(MODEL_PATH)

def predict_delay(base_time):
    current_hour = 9

    input_data = pd.DataFrame(
        [[current_hour, base_time]],
        columns=["hour", "base_time"]
    )

    predicted_delay = model.predict(input_data)[0]

    return max(predicted_delay, -base_time)
