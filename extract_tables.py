import camelot
import pandas as pd

def extract_tables_from_pdf(pdf_path):
    """Extract tables from the PDF file using Camelot."""
    tables = camelot.read_pdf(pdf_path, gs='C:\\Program Files\\gs\\gs10.03.1\\bin\\gswin64.exe')
    return tables

def save_tables_as_dataframes(tables):
    """Save extracted tables as pandas DataFrames."""
    dfs = []
    for table in tables:
        dfs.append(table.df)
    return dfs

def main():
    pdf_path = "extracted_data.pdf"  # Path to the PDF file
    tables = extract_tables_from_pdf(pdf_path)
    dfs = save_tables_as_dataframes(tables)
    
    # Print or further process the DataFrames
    for i, df in enumerate(dfs):
        print(f"Table {i+1}:")
        print(df)
        print("\n")

if __name__ == "__main__":
    main()
