import csv
import os

def get_first_10_rows():
    """
    Reads the chess_games.csv dataset and returns the first 10 rows.
    Uses the csv module's DictReader to return rows as dictionaries mapped to their column names.
    """
    # Get the absolute path to the data file, assuming it's in the same directory as this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'chess_games.csv')
    
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if i >= 10:
                    break
                data.append(row)
    except FileNotFoundError:
        print(f"Dataset file not found at: {file_path}")
            
    return data

if __name__ == '__main__':
    # Test the function by printing the data
    rows = get_first_10_rows()
    for index, row in enumerate(rows):
        print(f"--- Row {index + 1} ---")
        for key, value in row.items():
            print(f"{key}: {value}")
        print()
