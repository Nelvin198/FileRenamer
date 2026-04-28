import os
import re
import sys

# -----------------------------
# Helpers
# -----------------------------

def extract_number(name):
    """
    Extracts the first number found in a filename.
    Examples:
      image_12 -> 12
      image(7) -> 7
      image-99 -> 99
    """
    match = re.search(r"(\d+)", name)
    return match.group(1) if match else None


def ask_yes_no(prompt, default=False):
    suffix = "[Y/n]" if default else "[y/N]"
    reply = input(f"{prompt} {suffix}: ").strip().lower()
    if not reply:
        return default
    return reply.startswith("y")


# -----------------------------
# Core Logic
# -----------------------------

def rename_files(folder, old_name, new_name, recursive, dry_run):
    renamed = skipped = errors = 0
    counter = 1

    walker = os.walk(folder) if recursive else [(folder, [], os.listdir(folder))]

    for root, _, files in walker:
        for file in files:
            old_path = os.path.join(root, file)
            if not os.path.isfile(old_path):
                continue

            name, ext = os.path.splitext(file)

            # ✅ KEEP existing number if found
            num = extract_number(name)
            if num is None:
                num = str(counter)
                counter += 1

            new_file = f"{new_name}_{num}{ext}"
            new_path = os.path.join(root, new_file)

            if file == new_file:
                skipped += 1
                continue

            if os.path.exists(new_path):
                print(f"⚠️  Skipped (exists): {new_path}")
                skipped += 1
                continue

            if dry_run:
                print(f"[PREVIEW] {old_path} → {new_path}")
                renamed += 1
            else:
                try:
                    os.rename(old_path, new_path)
                    print(f"✅ Renamed: {old_path} → {new_path}")
                    renamed += 1
                except Exception as e:
                    print(f"❌ Error: {old_path} ({e})")
                    errors += 1

    return renamed, skipped, errors


# -----------------------------
# CLI
# -----------------------------

def main():
    print("SmartRename v1.1")
    print("Keeps existing numbers, sequential fallback\n")

    folder = input("Folder path (default: .): ").strip() or "."
    old_name = input("Name to replace (e.g. image): ").strip()
    new_name = input("New base name (e.g. media): ").strip()

    if not old_name or not new_name:
        print("❌ Missing input.")
        sys.exit(1)

    if not os.path.isdir(folder):
        print("❌ Folder not found.")
        sys.exit(1)

    recursive = ask_yes_no("Process subfolders?")
    dry_run = ask_yes_no("Preview only?", default=True)

    print("\n──── Preview ────")
    renamed, skipped, errors = rename_files(
        folder, old_name, new_name, recursive, dry_run
    )

    if dry_run and ask_yes_no("\nProceed with renaming?", default=False):
        print("\n──── Renaming ────")
        renamed, skipped, errors = rename_files(
            folder, old_name, new_name, recursive, False
        )

    print("\n──── Summary ────")
    print(f"Renamed : {renamed}")
    print(f"Skipped : {skipped}")
    print(f"Errors  : {errors}")
    print("─────────────────")


if __name__ == "__main__":
    main()
