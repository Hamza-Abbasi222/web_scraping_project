# combined_script_for_charts

import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.utils.dataframe import dataframe_to_rows
import subprocess

def create_csv():
    # Define the data
    data = {
        'Date': ['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02'],
        'Category': ['Product A', 'Product B', 'Product A', 'Product B'],
        'Value': [100, 200, 150, 250]
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Define the file path
    csv_file_path = 'sales_data.csv'

    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)

    print(f"CSV file created and saved at: {csv_file_path}")

def create_pivot_table_and_chart(data, excel_file):
    # Check if necessary columns exist
    required_columns = {'Date', 'Category', 'Value'}
    if not required_columns.issubset(data.columns):
        print(f"Missing columns in the DataFrame: {required_columns - set(data.columns)}")
        return
    
    # Create a pivot table
    pivot_table = data.pivot_table(index='Date', columns='Category', values='Value', aggfunc='sum')
    
    # Create a bar chart
    wb = Workbook()
    ws = wb.active
    for r in dataframe_to_rows(pivot_table, index=True, header=True):
        ws.append(r)
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Sales by Category"
    chart.y_axis.title = 'Value'
    chart.x_axis.title = 'Date'
    data_ref = Reference(ws, min_col=2, min_row=1, max_col=ws.max_column, max_row=ws.max_row)
    cats = Reference(ws, min_col=1, min_row=2, max_row=ws.max_row)
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats)
    ws.add_chart(chart, "E15")

    # Save the workbook
    wb.save(excel_file)

def main():
    # Create CSV file with data
    create_csv()
    
    # Load data
    data = pd.read_csv('sales_data.csv')
    
    # Print columns for debugging
    print(f"Data columns: {data.columns}")

    # Customize file names using f-strings
    csv_file = 'sales_data.csv'
    excel_file = 'sales_data.xlsx'

    # Create pivot table and export it to an Excel file
    create_pivot_table_and_chart(data, excel_file)

    # Schedule the script to run at any time
    command = f"python combined_script.py"
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    main()
