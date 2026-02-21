import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "training_data.csv")


def log_data(from_node, to_node, hour, base_time, actual_time, delay):

    file_exists = os.path.exists(FILE_PATH)

    with open(FILE_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write header only once
        if not file_exists:
            writer.writerow([
                "from_node",
                "to_node",
                "hour",
                "base_time",
                "actual_time",
                "delay"
            ])

        writer.writerow([
            from_node,
            to_node,
            hour,
            base_time,
            actual_time,
            delay
        ])
