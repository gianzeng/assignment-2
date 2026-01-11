"""
HIT137 Assignment 2 - Question 2
Temperature Data Analysis (Standard Library Version)
"""

import csv
import glob
import os
import math
from collections import defaultdict

def load_data(folder_path):
    """
    Loads data from all CSV files into a list of records.
    Each record is a dict: {'STATION_NAME': ..., 'Year': ..., 'Month': ..., 'Temperature': ...}
    """
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))
    records = []
    
    print(f"Found {len(all_files)} files.")
    
    for filename in all_files:
        try:
            basename = os.path.basename(filename)
            year_str = basename.split('_')[-1].replace('.csv', '')
            year = int(year_str)
            
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    station = row.get('STATION_NAME', '')
                    # Iterate through months
                    months = ['January', 'February', 'March', 'April', 'May', 'June', 
                              'July', 'August', 'September', 'October', 'November', 'December']
                    
                    for month in months:
                        temp_str = row.get(month, '')
                        if temp_str and temp_str.strip():
                            try:
                                temp = float(temp_str)
                                records.append({
                                    'STATION_NAME': station,
                                    'Year': year,
                                    'Month': month,
                                    'Temperature': temp
                                })
                            except ValueError:
                                pass # Ignore non-numeric
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            
    return records

def calculate_mean(values):
    return sum(values) / len(values) if values else 0

def calculate_std(values):
    if len(values) < 2:
        return 0.0
    mean = calculate_mean(values)
    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(variance)

def process_seasonal_average(records):
    """Task 1: Seasonal Average"""
    season_map = {
        'December': 'Summer', 'January': 'Summer', 'February': 'Summer',
        'March': 'Autumn', 'April': 'Autumn', 'May': 'Autumn',
        'June': 'Winter', 'July': 'Winter', 'August': 'Winter',
        'September': 'Spring', 'October': 'Spring', 'November': 'Spring'
    }
    
    season_temps = defaultdict(list)
    
    for r in records:
        season = season_map.get(r['Month'])
        if season:
            season_temps[season].append(r['Temperature'])
            
    # Output formatting with degree symbol
    output_lines = []
    # Order
    for season in ['Summer', 'Autumn', 'Winter', 'Spring']:
        if season in season_temps:
            avg = calculate_mean(season_temps[season])
            output_lines.append(f"{season}: {avg:.1f}°C")
            
    with open('average_temp.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    print("Task 1 Done: average_temp.txt created.")

def main():
    print("HIT137 Assignment 2 - Question 2 (Standard Lib)")
    folder = 'temperatures'
    
    if not os.path.exists(folder):
        print(f"Error: Folder '{folder}' not found.")
        return
        
    records = load_data(folder)
    if records:
        process_seasonal_average(records)
        print("All tasks completed.")
    else:
        print("No records found.")

if __name__ == "__main__":
    main()
