# SOJF Seminarski
# Author: Josip Prpić
# Date: 30-01-2025
# Github repo: https://github.com/josippr/TVZ-SOJF-final

# Task: Zadatak 4: Analiza NTFS volumena
# Opis: Analizirajte NTFS volumen kako biste istražili skrivene podatke (Alternate Data Streams - ADS).
# Specifikacija zadatka:
#     Skripta treba koristiti alate poput fsstat i icat za istraživanje NTFS strukture.
#     Napišite skriptu u Pythonu ili PowerShellu koja:
#         Detektira prisutnost ADS-a.
#         Ekstrahira sadržaj pronađenih ADS-ova.
#         Generira izvještaj s detaljima (npr. veličina, ime datoteke, sadržaj ADS-a).

import os
import subprocess
import argparse
import json

def detect_ads(file_path):
    """Detects Alternate Data Streams (ADS) in a given file."""
    try:
        result = subprocess.run(['fsutil', 'stream', 'list', file_path], capture_output=True, text=True, check=True)
        ads_list = [line.strip() for line in result.stdout.split('\n') if ':' in line and '::$DATA' not in line]
        return ads_list
    except subprocess.CalledProcessError as e:
        return [f"Error detecting ADS: {e}"]

def extract_ads(file_path, ads_name):
    """Extracts the content of an Alternate Data Stream."""
    output_file = f"{file_path.replace(os.sep, '_')}_{ads_name.replace(':', '_')}.ads"
    try:
        with open(output_file, 'wb') as out_file:
            result = subprocess.run(['icat', file_path, ads_name], stdout=out_file, check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        return f"Error extracting ADS: {e}"

def analyze_ntfs_volume(volume):
    ads_report = []
    
    for root, _, files in os.walk(volume):
        for file in files:
            file_path = os.path.join(root, file)
            ads_list = detect_ads(file_path)
            
            if ads_list:
                extracted_ads = []
                for ads in ads_list:
                    extracted_path = extract_ads(file_path, ads)
                    extracted_ads.append({"ads": ads, "extracted_to": extracted_path})
                
                ads_report.append({
                    "file": file,
                    "path": file_path,
                    "ads_streams": extracted_ads
                })
    
    return ads_report

def main():
    parser = argparse.ArgumentParser(description='Analyze NTFS volume for Alternate Data Streams (ADS).')
    parser.add_argument('--volume', type=str, required=True, help='Volume to analyze (e.g., E:)')
    args = parser.parse_args()
    
    report = analyze_ntfs_volume(args.volume + '\\')
    
    with open('task2_report.json', 'w') as f:
        json.dump(report, f, indent=4)
    
    print("Analysis complete. Report saved as task2_report.json")

if __name__ == "__main__":
    main()

