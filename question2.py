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

def process_temperature_range(records):
    """Task 2: Largest Range (Max - Min) per station"""
    station_temps = defaultdict(list)
    
    for r in records:
        station_temps[r['STATION_NAME']].append(r['Temperature'])
        
    max_range = -1
    target_stations = []
    
    # First pass: find max range
    station_ranges = {}
    
    for station, temps in station_temps.items():
        if not temps: continue
        t_max = max(temps)
        t_min = min(temps)
        rng = t_max - t_min
        station_ranges[station] = (rng, t_max, t_min)
        
        if rng > max_range:
            max_range = rng
            
    # Second pass: collect all with max range
    for station, (rng, t_max, t_min) in station_ranges.items():
        # Float comparison tolerance
        if abs(rng - max_range) < 1e-9:
            target_stations.append((station, rng, t_max, t_min))
            
    output_lines = []
    for station, rng, t_max, t_min in target_stations:
        output_lines.append(f"{station}: Range {rng:.1f}°C (Max: {t_max:.1f}°C, Min: {t_min:.1f}°C)")
        
    with open('largest_temp_range_station.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    print("Task 2 Done: largest_temp_range_station.txt created.")

def process_temperature_stability(records):
    """Task 3: Stability (StdDev)"""
    station_temps = defaultdict(list)
    for r in records:
        station_temps[r['STATION_NAME']].append(r['Temperature'])
        
    station_stds = {}
    for station, temps in station_temps.items():
        if len(temps) > 1:
            station_stds[station] = calculate_std(temps)
            
    if not station_stds:
        print("Not enough data for stability analysis.")
        return

    # Find Min and Max Std
    min_std = min(station_stds.values())
    max_std = max(station_stds.values())
    
    most_stable = [s for s, v in station_stds.items() if abs(v - min_std) < 1e-9]
    most_variable = [s for s, v in station_stds.items() if abs(v - max_std) < 1e-9]
    
    output_lines = []
    
    for s in most_stable:
        output_lines.append(f"Most Stable: {s}: StdDev {min_std:.1f}°C")
        
    for s in most_variable:
        output_lines.append(f"Most Variable: {s}: StdDev {max_std:.1f}°C")
        
    with open('temperature_stability_stations.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    print("Task 3 Done: temperature_stability_stations.txt created.")

def main():
    print("HIT137 Assignment 2 - Question 2 (Standard Lib)")
    folder = 'temperatures'
    
    if not os.path.exists(folder):
        print(f"Error: Folder '{folder}' not found.")
        return
        
    records = load_data(folder)
    if records:
        process_seasonal_average(records)
        process_temperature_range(records)
        process_temperature_stability(records)
        print("All tasks completed.")
    else:
        print("No records found.")

if __name__ == "__main__":
    main()
