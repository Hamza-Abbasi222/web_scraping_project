import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import firebase_admin
from firebase_admin import credentials, firestore
import mysql.connector

# Import functions from the existing modules
from First_half_proj.T1_automation_script import fetch_data, extract_information, generate_reports
from First_half_proj.T2_extract_tables_from_pdf_using_camelot import extract_tables_from_pdf, save_tables_as_csv
from First_half_proj.T4_selenium_automation import selenium_automation
from First_half_proj.T6_scrape_headlines import get_valid_url, get_html_tag_and_class, scrape_headlines, export_headlines_to_csv

# Initialize Firebase (Make sure you have your Firebase credentials file)
def init_firebase():
    cred = credentials.Certificate('path/to/your/firebase/credentials.json')
    firebase_admin.initialize_app(cred)
    return firestore.client()

# Connect to MySQL
def connect_mysql():
    return mysql.connector.connect(
        host="your_host",
        user="your_user",
        password="your_password",
        database="your_database"
    )

# Scrape book details using Beautiful Soup
def scrape_books(url):
    soup = fetch_data(url)
    tag_class_pairs = [('h3', 'title'), ('p', 'price_color')]  # Example pairs, adjust as needed
    data = extract_information(soup, tag_class_pairs)
    return data

# Store data in Firebase
def store_in_firebase(data):
    db = init_firebase()
    for key, values in data.items():
        for value in values:
            db.collection('books').add({key: value})

# Store data in MySQL
def store_in_mysql(data):
    connection = connect_mysql()
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS books (title VARCHAR(255), price VARCHAR(255))")

    for key, values in data.items():
        for value in values:
            cursor.execute("INSERT INTO books (title, price) VALUES (%s, %s)", (value['title'], value['price']))

    connection.commit()
    cursor.close()
    connection.close()

# Main function to run the project tasks
def main():
    # Step 1: Scrape book details from the website
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

    # Step 2: Store the scraped data in a database
    store_in_firebase(book_data)
    store_in_mysql(book_data)

    # Generate reports using Pandas
    df = pd.DataFrame(book_data)
    df.to_csv('books_report.csv', index=False)
    df.to_excel('books_report.xlsx', index=False)
    generate_reports(book_data)

    # Perform Selenium automation (example function call)
    selenium_automation()

    # Extract tables from PDF and save as CSV (example function call)
    pdf_path = 'path/to/your/pdf_file.pdf'
    tables = extract_tables_from_pdf(pdf_path)
    save_tables_as_csv(tables, 'extracted_tables.csv')

    # Export headlines to CSV (example function call)
    export_headlines_to_csv()

if __name__ == "__main__":
    main()
