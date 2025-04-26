import os
import re
import argparse
import csv
import sys

def clean_filename(filename):
    filename = filename.replace(' ', '_')
    filename = re.sub(r'[^A-Za-z0-9_.-]', '', filename)
    return filename

def process_directory(directory, output_csv, dry_run=False):
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    changes = []

    for filename in os.listdir(directory):
        old_path = os.path.join(directory, filename)
        
        if not os.path.isfile(old_path):
            continue
        
        new_filename = clean_filename(filename)
        new_path = os.path.join(directory, new_filename)

        if filename != new_filename:
            print(f"Renaming: '{filename}' -> '{new_filename}'")
            if not dry_run:
                try:
                    os.rename(old_path, new_path)
                except Exception as e:
                    print(f"Failed to rename '{filename}': {e}")
                    continue
            changes.append((filename, new_filename))

    if changes:
        try:
            with open(output_csv, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['original_filename', 'new_filename'])
                writer.writerows(changes)
            print(f"\nRename log saved to '{output_csv}'")
        except Exception as e:
            print(f"Error writing to CSV: {e}")
    else:
        print("No filenames needed cleaning.")

def main():
    parser = argparse.ArgumentParser(
        description="Filename Cleaner: Cleans filenames in a directory and logs changes."
    )
    parser.add_argument('-d', '--directory', required=True, help="Directory containing files to clean.")
    parser.add_argument('-o', '--output', required=True, help="Output CSV file to save rename log.")
    parser.add_argument('--dry-run', action='store_true', help="Show what would be renamed without making changes.")
    
    args = parser.parse_args()

    process_directory(args.directory, args.output, args.dry_run)

if __name__ == "__main__":
    main()