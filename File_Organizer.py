import os
import shutil


def organize_files(directory):
    """Sort files in a directory into subfolders based on their extension."""
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        return

    moved = 0

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        # Skip directories and hidden files
        if os.path.isdir(filepath) or filename.startswith("."):
            continue

        ext = os.path.splitext(filename)[1].lower()
        folder_name = ext[1:].upper() if ext else "NO_EXTENSION"

        target_dir = os.path.join(directory, folder_name)
        os.makedirs(target_dir, exist_ok=True)

        shutil.move(filepath, os.path.join(target_dir, filename))
        moved += 1
        print(f"  Moved: {filename} -> {folder_name}/")

    print(f"\nDone! {moved} file(s) organized.")


def main():
    print()
    print("#################################")
    print("|     Python File Organizer     |")
    print("#################################")
    print()

    directory = input("Enter the directory path to organize: ").strip()

    if not directory:
        print("No directory provided.")
        return

    confirm = input(f"This will sort files in '{directory}' into subfolders by extension. Continue? (yes/no): ").strip()

    if confirm.lower() == "yes":
        organize_files(directory)
    else:
        print("Cancelled.")


if __name__ == "__main__":
    main()
