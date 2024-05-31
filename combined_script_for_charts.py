# combined_script.py

import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.utils.dataframe import dataframe_to_rows
import subprocess

def create_pivot_table_and_chart(data, excel_file):
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
    data = Reference(ws, min_col=2, min_row=1, max_col=5, max_row=5)
    cats = Reference(ws, min_col=1, min_row=2, max_row=5)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    ws.add_chart(chart, "E15")

    # Save the workbook
    wb.save(excel_file)

def main():
    # Load data
    data = pd.read_csv('sales_data.csv')

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
