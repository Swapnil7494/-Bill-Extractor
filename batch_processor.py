import os
from extractor.gemini_extractor import extract_from_file
from utils.csv_writer import append_to_csv

# Supported formats
SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".pdf", ".heic"]


def process_folder(folder_path):
    if not os.path.exists(folder_path):
        print("❌ Folder does not exist")
        return

    files = os.listdir(folder_path)

    print(f"📂 Found {len(files)} files")

    processed = 0
    failed = 0

    for file in files:
        file_path = os.path.join(folder_path, file)
        ext = os.path.splitext(file)[1].lower()

        if ext not in SUPPORTED_EXTENSIONS:
            print(f"⏭️ Skipping unsupported file: {file}")
            continue

        print(f"\n🔄 Processing: {file}")

        try:
            result = extract_from_file(file_path)

            if "error" in result:
                print(f"❌ Extraction failed: {file}")
                failed += 1
                continue

            append_to_csv(result)
            print(f"✅ Done: {file}")

            processed += 1

        except Exception as e:
            print(f"❌ Error processing {file}: {e}")
            failed += 1

    print("\n📊 Summary:")
    print(f"Processed: {processed}")
    print(f"Failed: {failed}")