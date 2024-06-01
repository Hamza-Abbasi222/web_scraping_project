import camelot
import pandas as pd
import requests
from io import BytesIO
from pathlib import Path

def extract_tables_from_pdf(pdf_path):
    """Extract tables from the PDF file using Camelot."""
    try:
        tables = camelot.read_pdf(str(pdf_path), pages='all')  # Convert Path object to string
        if tables:
            print(f"Successfully extracted {len(tables)} table(s) from the PDF.")
        else:
            print("No tables found in the PDF.")
        return tables
    except Exception as e:
        print(f"Error extracting tables: {e}")
        return []

def save_tables_as_csv(tables, output_csv):
    """Save extracted tables as a single CSV file."""
    if not tables:
        print("No tables to save.")
        return
    
    df_list = [table.df for table in tables]
    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df.to_csv(output_csv, index=False)
    print(f"All extracted tables saved as {output_csv}")

def download_pdf_from_url(url):
    """Download PDF from a URL and return the local path."""
    response = requests.get(url)
    if response.status_code == 200:
        pdf_path = "downloaded_pdf.pdf"
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        return pdf_path
    else:
        print("Failed to download the PDF from the URL.")
        return None

def main():
    user_input = input("Enter the path to the PDF file (local path or URL): ").strip()
    
    if user_input.startswith("http://") or user_input.startswith("https://"):
        pdf_path = download_pdf_from_url(user_input)
    else:
        pdf_path = Path(user_input)
        if not pdf_path.is_file():
            print("The specified local file does not exist.")
            return

    if pdf_path:
        print(f"Attempting to extract tables from {pdf_path}")
        tables = extract_tables_from_pdf(pdf_path)
        
        if tables:
            output_csv = "extracted_table_from_pdf.csv"
            save_tables_as_csv(tables, output_csv)
            
            # Print the combined DataFrame
            combined_df = pd.concat([table.df for table in tables], ignore_index=True)
            print("\nCombined DataFrame:")
            print(combined_df)
        else:
            print("No tables were extracted.")
    else:
        print("No valid PDF path provided.")

if __name__ == "__main__":
    main()
