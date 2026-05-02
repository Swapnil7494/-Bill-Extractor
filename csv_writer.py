# =========================================
# 📊 CSV Writer Utility for Bill Extraction
# =========================================

import os
import pandas as pd


# 📁 Output Configuration
OUTPUT_DIR = "output"
MASTER_FILE = "all_bills.csv"


# 📌 Standard CSV Columns
COLUMNS = [
    "file_name",
    "consumer_id",
    "name",
    "billing_date",
    "units",
    "amount",
    "due_date"
]


# =========================================
# ➕ Append Extracted Data to CSV
# =========================================
def append_to_csv(data, file_name=None):
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    file_path = os.path.join(OUTPUT_DIR, MASTER_FILE)

    # 🚫 Skip failed extraction
    if "error" in data:
        return None

    # 📄 Add filename to record
    data["file_name"] = file_name

    # Convert to DataFrame
    new_df = pd.DataFrame([data])

    # 🧩 Ensure all required columns exist
    for col in COLUMNS:
        if col not in new_df.columns:
            new_df[col] = None

    # Reorder columns
    new_df = new_df[COLUMNS]

    # =========================================
    # 📥 Append or Create CSV
    # =========================================
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)

        # Merge new + existing data
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)

        # 🧹 Remove duplicates
        updated_df = updated_df.drop_duplicates(
            subset=["file_name", "consumer_id", "billing_date"],
            keep="last"
        )

    else:
        updated_df = new_df

    # 💾 Save updated CSV
    updated_df.to_csv(file_path, index=False)

    return file_path
