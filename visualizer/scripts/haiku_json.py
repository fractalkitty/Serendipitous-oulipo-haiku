import csv
import json

def convert_haiku_csv_to_json(input_csv_path="../data/haiku.csv", output_json_path="../web/haiku_data.json"):
    haikus = []
    
    with open(input_csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # Get the actual header names from the CSV
        headers = reader.fieldnames
        
        # Find the correct column names regardless of case
        line1_col = next(h for h in headers if h.lower() == 'line1')
        line2_col = next(h for h in headers if h.lower() == 'line2')
        line3_col = next(h for h in headers if h.lower() == 'line3')
        
        for index, row in enumerate(reader, 0):
            # Use the actual column names from the CSV
            haiku_text = f"{row[line1_col]}\n{row[line2_col]}\n{row[line3_col]}"
            
            # Create word list
            words = []
            for line in [row[line1_col], row[line2_col], row[line3_col]]:
                cleaned_words = [word.strip('.,!?;:"\'').lower() for word in line.split()]
                words.extend(cleaned_words)
            
            haiku = {
                "index": index,
                "text": haiku_text,
                "words": words
            }
            haikus.append(haiku)
    
    # Create the final JSON structure
    output_data = {"haikus": haikus}
    
    # Write to JSON file
    with open(output_json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(output_data, jsonfile, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    convert_haiku_csv_to_json()