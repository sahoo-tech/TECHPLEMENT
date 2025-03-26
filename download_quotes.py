import requests
import csv
import os

def download_quotes():
    # URL of the quotes dataset (you'll need to replace this with the actual URL)
    url = "https://raw.githubusercontent.com/akshaynehate/Quotes-Dataset/master/quotes.csv"
    
    try:
        print("Downloading quotes dataset...")
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Save the CSV file
        with open('quotes.csv', 'w', encoding='utf-8', newline='') as f:
            f.write(response.text)
        
        print("Successfully downloaded quotes.csv")
        
        # Process the CSV to ensure it has the correct format
        with open('quotes.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        # Write back with proper formatting
        with open('quotes.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['quote', 'author', 'category'])
            writer.writeheader()
            for row in rows:
                writer.writerow({
                    'quote': row.get('quote', row.get('text', '')),
                    'author': row.get('author', 'Unknown'),
                    'category': row.get('category', 'General')
                })
        
        print("Successfully processed quotes.csv")
        
    except Exception as e:
        print(f"Error downloading quotes: {str(e)}")
        print("Using default quotes instead.")

if __name__ == "__main__":
    download_quotes() 