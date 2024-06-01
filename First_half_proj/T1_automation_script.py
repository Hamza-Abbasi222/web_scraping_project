# T1_automation_script.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def fetch_data(url):
    """Fetch data from the specified URL and return a BeautifulSoup object."""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def extract_information(soup, tag_class_pairs):
    """Extract information from specified HTML tags with their class names."""
    data = {}
    for tag_class_pair in tag_class_pairs:
        if isinstance(tag_class_pair, tuple) and len(tag_class_pair) == 2:
            tag, class_name = tag_class_pair
            elements = soup.find_all(tag, class_=class_name)
            texts = [element.get_text(strip=True) for element in elements]
            if not texts:  # Check if the array is empty
                print(f"No data found for {tag} with class {class_name}, trying without class.")
                elements = soup.find_all(tag)
                texts = [element.get_text(strip=True) for element in elements]
            if texts:
                data[f"{tag},{class_name}"] = texts
            else:
                print(f"No data found for {tag},{class_name}")
        else:
            print(f"Invalid input format: {tag_class_pair}. Please use ('tag','class') format.")

    # Check the lengths of arrays
    lengths = {key: len(value) for key, value in data.items()}
    print("Lengths of arrays:")
    for key, length in lengths.items():
        print(f"{key}: {length}")

    if len(set(lengths.values())) > 1:
        raise ValueError("Arrays must all be the same length")

    return data

def generate_reports(data):
    """Generate reports in CSV, Excel, and PDF formats from the extracted data."""
    df = pd.DataFrame(data)
    df.to_csv('extracted_data.csv', index=False)
    df.to_excel('extracted_data.xlsx', index=False)
    
    c = canvas.Canvas('extracted_data.pdf', pagesize=letter)
    text = df.to_string(index=False)
    
    width, height = letter
    margin = 50
    y = height - margin
    for line in text.split('\n'):
        if y < margin:
            c.showPage()
            y = height - margin
        c.drawString(margin, y, line)
        y -= 12
    c.save()
    
    print('Reports have been successfully generated: extracted_data.csv, extracted_data.xlsx, and extracted_data.pdf')

def main():
    url = input("Enter the URL to scrape: ").strip()
    
    try:
        soup = fetch_data(url)
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return
    
    tag_class_pairs = []
    while True:
        tag_class_pair = input("Enter the HTML tag and its class to extract (tag,class), or enter 'done' to finish: ").strip()
        if tag_class_pair.lower() == 'done':
            break
        # Check if the input is a tuple
        if ',' in tag_class_pair:
            parts = tag_class_pair.split(',')
            if len(parts) != 2:
                print(f"Invalid input format: {tag_class_pair}. Please use 'tag,class' format.")
                continue
            tag_class_pairs.append((parts[0].strip(), parts[1].strip()))
        else:
            print(f"Invalid input format: {tag_class_pair}. Please use 'tag,class' format.")
    
    if not tag_class_pairs:
        print("No HTML tags provided.")
        return
    
    try:
        data = extract_information(soup, tag_class_pairs)
        generate_reports(data)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
