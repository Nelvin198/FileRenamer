import os
import re
import random

def generate_random_id():
    return random.randint(1000, 9999)

def rename_files():
    folder = input("Enter folder path: ").strip()
    old_name = input("Enter name to replace (e.g. media): ").strip()
    new_name = input("Enter new base name (e.g. filename): ").strip()

    if not os.path.isdir(folder):
        print("❌ Folder not found.")
        return

    pattern = re.compile(rf"^{re.escape(old_name)}\((\d+)\)$")

    for file in os.listdir(folder):
        old_path = os.path.join(folder, file)

        if not os.path.isfile(old_path):
            continue

        name, ext = os.path.splitext(file)

        match = pattern.match(name)
        if match:
            item_id = match.group(1)
        else:
            item_id = generate_random_id()

        new_filename = f"{new_name}_{item_id}{ext}"
        new_path = os.path.join(folder, new_filename)

        # Prevent overwriting files
        if os.path.exists(new_path):
            print(f"⚠️ Skipping (already exists): {new_filename}")
            continue

        os.rename(old_path, new_path)
        print(f"✅ Renamed: {file} → {new_filename}")

if __name__ == "__main__":
    rename_files()