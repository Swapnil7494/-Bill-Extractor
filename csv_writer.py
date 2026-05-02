import pandas as pd
import os

OUTPUT_DIR = "output"
MASTER_FILE = "all_bills.csv"

COLUMNS = [
    "file_name",
    "consumer_id",
    "name",
    "billing_date",
    "units",
    "amount",
    "due_date"
]


def append_to_csv(data, file_name=None):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    file_path = os.path.join(OUTPUT_DIR, MASTER_FILE)

    # Skip if extraction failed
    if "error" in data:
        return None

    # Add filename to data
    data["file_name"] = file_name

    new_df = pd.DataFrame([data])

    # Ensure all columns exist
    for col in COLUMNS:
        if col not in new_df.columns:
            new_df[col] = None

    new_df = new_df[COLUMNS]

    # Append or create
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)

        # Remove duplicates (including file_name now)
        updated_df = updated_df.drop_duplicates(
            subset=["file_name", "consumer_id", "billing_date"],
            keep="last"
        )
    else:
        updated_df = new_df

    updated_df.to_csv(file_path, index=False)

    return file_path