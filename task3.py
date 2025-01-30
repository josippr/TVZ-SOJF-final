import os
import hashlib
import argparse
import json
import csv

def calculate_hash(file_path, algorithm='md5'):
    hash_func = hashlib.md5() if algorithm == 'md5' else hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        return f'Error: {e}'

def find_duplicates(directory):
    file_hashes = {}
    duplicates = []
    unique_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_hash(file_path, 'sha256')
            
            if file_hash in file_hashes:
                duplicates.append(file_path)
                os.remove(file_path)  # Remove duplicate file
            else:
                file_hashes[file_hash] = file_path
                unique_files.append(file_path)
    
    return unique_files, duplicates

def export_report(report, format_type):
    if format_type == 'json':
        with open('deduplication_report.json', 'w') as f:
            json.dump(report, f, indent=4)
        print("Deduplication complete. Report saved as deduplication_report.json")
    elif format_type == 'csv':
        with open('deduplication_report.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Unique Files Count", "Duplicate Files Count"])
            writer.writerow([report["unique_files_count"], report["duplicate_files_count"]])
            writer.writerow([])
            writer.writerow(["Duplicate Files"])
            writer.writerows([[dup] for dup in report["duplicates"]])
        print("Deduplication complete. Report saved as deduplication_report.csv")
    else:
        print("Invalid export format specified.")

def main():
    parser = argparse.ArgumentParser(description='Identify and remove duplicate files.')
    parser.add_argument('--directory', type=str, required=True, help='Directory to analyze')
    parser.add_argument('--export', type=str, choices=['json', 'csv'], required=True, help='Export format: json or csv')
    args = parser.parse_args()
    
    unique_files, duplicates = find_duplicates(args.directory)
    
    report = {
        "unique_files_count": len(unique_files),
        "duplicate_files_count": len(duplicates),
        "duplicates": duplicates
    }
    
    export_report(report, args.export)

if __name__ == "__main__":
    main()