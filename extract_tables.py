import camelot
import pandas as pd

def extract_tables_from_pdf(pdf_path):
    """Extract tables from the PDF file using Camelot."""
    try:
        tables = camelot.read_pdf(pdf_path)
        if tables:
            print(f"Successfully extracted {len(tables)} table(s) from the PDF.")
        else:
            print("No tables found in the PDF.")
        return tables
    except Exception as e:
        print(f"Error extracting tables: {e}")
        return []

def save_tables_as_dataframes(tables):
    """Save extracted tables as pandas DataFrames."""
    dfs = []
    for i, table in enumerate(tables):
        df = table.df
        dfs.append(df)
        df.to_csv(f'extracted_table_{i+1}.csv', index=False)
        print(f"Table {i+1} saved as extracted_table_{i+1}.csv")
    return dfs

def main():
    pdf_path = "annots.pdf"  # Path to the PDF file
    print(f"Attempting to extract tables from {pdf_path}")
    
    tables = extract_tables_from_pdf(pdf_path)
    
    if tables:
        dfs = save_tables_as_dataframes(tables)
        
        # Print or further process the DataFrames
        for i, df in enumerate(dfs):
            print(f"\nTable {i+1}:")
            print(df)
    else:
        print("No tables were extracted.")

if __name__ == "__main__":
    main()
