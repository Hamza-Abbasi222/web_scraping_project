import camelot
import pandas as pd

def extract_tables_from_pdf(pdf_path):
    """Extract tables from a PDF file and return a list of pandas DataFrames."""
    tables = camelot.read_pdf(pdf_path, pages='all')
    dataframes = [table.df for table in tables]
    return dataframes

def save_tables_to_csv(dataframes, output_path_prefix):
    """Save each DataFrame in the list to a CSV file."""
    for i, df in enumerate(dataframes):
        output_path = f"{output_path_prefix}_table_{i + 1}.csv"
        df.to_csv(output_path, index=False)
        print(f"Saved table {i + 1} to {output_path}")

def main():
    pdf_path = 'sample.pdf'  # Replace with your PDF file path
    output_path_prefix = 'extracted_table'
    
    dataframes = extract_tables_from_pdf(pdf_path)
    save_tables_to_csv(dataframes, output_path_prefix)
    
    print("Extraction and saving of tables is complete.")

if __name__ == '__main__':
    main()
