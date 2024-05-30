# automate_reports_and_whatsapp.py

import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pywhatkit as kit
import datetime
import time

def create_excel_report(data, excel_file):
    wb = Workbook()
    ws = wb.active
    for r in dataframe_to_rows(data, index=False, header=True):
        ws.append(r)
    wb.save(excel_file)

def send_whatsapp_message(phone_number, message):
    now = datetime.datetime.now()
    send_time = now + datetime.timedelta(minutes=2)  # Schedule to send after 2 minutes
    kit.sendwhatmsg(phone_number, message, send_time.hour, send_time.minute + 1)

def main():
    # Sample data
    data = {
        'Date': ['2023-05-28', '2023-05-29', '2023-05-30'],
        'Category': ['A', 'B', 'C'],
        'Value': [10, 20, 30]
    }
    df = pd.DataFrame(data)
    
    # Customize file names using f-strings
    csv_file = 'sales_data.csv'
    excel_file = 'sales_data_report.xlsx'
    
    # Save the data to a CSV file
    df.to_csv(csv_file, index=False)
    
    # Create and save an Excel report
    create_excel_report(df, excel_file)
    
    # WhatsApp message details
    phone_number = input("Enter the phone number to send WhatsApp message (e.g., '+1234567890'): ")
    message = "Excel report has been created and saved as sales_data_report.xlsx"
    
    # Send a WhatsApp message
    send_whatsapp_message(phone_number, message)

if __name__ == "__main__":
    main()
