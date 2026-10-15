import os
import re
import csv

# --- Configuration ---
# Point this to the folder where your .txt deck files are saved
INPUT_DIR = r"C:\Users\abeil\Downloads\decks"
OUTPUT_FILE = r"C:\Users\abeil\Downloads\decks\deck_data.csv"

def standardize_card_name(name):
    """
    Converts to uppercase and removes all non-alphanumeric characters.
    Example: "Sensei's Divining Top" -> "SENSEISDIVININGTOP"
    """
    # .upper() makes it uppercase
    # re.sub(r'[^A-Z0-9]', '', ...) removes anything that is NOT a letter or number
    return re.sub(r'[^A-Z0-9]', '', name.upper())

def process_decklists():
    print("Starting to process decklists...")
    
    # Open the output CSV file
    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
        # Set the delimiter to semicolon
        writer = csv.writer(csv_file, delimiter=';')
        
        # Write the header row
        writer.writerow(['deck_name', 'quantity', 'card_name', 'standardized_name'])
        
        files_processed = 0
        
        # Loop through all files in the input directory
        for filename in os.listdir(INPUT_DIR):
            if filename.endswith(".txt"):
                # Extract the deck name by removing the ".txt" extension
                deck_name = os.path.splitext(filename)[0]
                filepath = os.path.join(INPUT_DIR, filename)
                
                with open(filepath, mode='r', encoding='utf-8') as txt_file:
                    for line in txt_file:
                        line = line.strip() # Remove leading/trailing spaces & newlines
                        
                        # Skip empty lines (like the gap between mainboard and sideboard)
                        if not line:
                            continue
                            
                        # Split the line by the very first space only. 
                        # This separates the number from the rest of the card name.
                        parts = line.split(" ", 1)
                        
                        # Make sure the line correctly split and the first part is a number
                        if len(parts) == 2 and parts[0].isdigit():
                            quantity = parts[0]
                            card_name = parts[1]
                            std_name = standardize_card_name(card_name)
                            
                            # Write the row to the CSV
                            writer.writerow([deck_name, quantity, card_name, std_name])
                            
                files_processed += 1

    print(f"Successfully processed {files_processed} files.")
    print(f"Data saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    # Ensure the directory exists to avoid errors
    if os.path.exists(INPUT_DIR):
        process_decklists()
    else:
        print(f"Error: The directory {INPUT_DIR} does not exist. Please check the path.")