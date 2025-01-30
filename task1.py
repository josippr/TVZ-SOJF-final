# SOJF Seminarski
# Author: Josip Prpić
# Date: 30-01-2025
# Github repo: https://github.com/josippr/TVZ-SOJF-final

# Task: Zadatak 1: Analiza datoteka
# Opis: Studenti trebaju analizirati skup datoteka i generirati popis različitih tipova datoteka prisutnih u direktoriju koristeći file signature analizu.
# Specifikacija zadatka:
#     Napišite skriptu koja iterira kroz direktorij i određuje tip svake datoteke.
#     Implementirajte zadatak u PowerShell ili Python.
#     Koristite hashing algoritme (MD5, SHA256) za svaku datoteku i generirajte izvještaj.
#     Usporedite jednostavnost implementacije u odabranom jeziku s implementacijom u Bashu.


import os
import hashlib
import magic
import argparse
import json

def calculate_hash(file_path, algorithm='md5'):
    hash_func = hashlib.md5() if algorithm == 'md5' else hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        return f'Error: {e}'

def analyze_directory(directory):
    file_types = {}
    file_report = []
    
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        return []
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_type = magic.from_file(file_path, mime=True)
                md5_hash = calculate_hash(file_path, 'md5')
                sha256_hash = calculate_hash(file_path, 'sha256')
                
                if file_type not in file_types:
                    file_types[file_type] = 0
                file_types[file_type] += 1
                
                file_report.append({
                    "file": file,
                    "path": file_path,
                    "type": file_type,
                    "md5": md5_hash,
                    "sha256": sha256_hash
                })
            except Exception as e:
                print(f"Error processing {file}: {e}")
    
    print("File Types Summary:")
    for ftype, count in file_types.items():
        print(f"{ftype}: {count}")
    
    return file_report

def main():
    parser = argparse.ArgumentParser(description='Analyze files in a directory.')
    parser.add_argument('directory', type=str, help='Directory to analyze')
    args = parser.parse_args()
    
    report = analyze_directory(args.directory)
    
    with open('task1_report.json', 'w') as f:
        json.dump(report, f, indent=4)
    
    print("Analysis complete. Report saved as task1_report.json")



if __name__ == "__main__":
  main()