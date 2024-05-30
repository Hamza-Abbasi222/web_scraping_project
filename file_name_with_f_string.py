# main_script.py

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import camelot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

# Functions for each task
def get_valid_url():
    while True:
        url = input("Enter the URL of the website you want to scrape: ").strip()
        if url.startswith(("http://", "https://")):
            return url
        else:
            print("Invalid URL. Please enter a URL starting with 'http://' or 'https://'.")

def scrape_headlines(url, tag, class_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    if class_name:
        headlines = soup.find_all(tag, class_=class_name)
    else:
        headlines = soup.find_all(tag)
    return [headline.get_text(strip=True) for headline in headlines]

def extract_table_from_pdf(pdf_path):
    tables = camelot.read_pdf(pdf_path, pages='all')
    if tables:
        df = tables[0].df
        csv_file = f"table_{os.path.basename(pdf_path)}.csv"
        df.to_csv(csv_file, index=False)
        print(f"Table extracted and saved to '{csv_file}'.")
    else:
        print("No tables found in the PDF.")

def automate_website_interaction(url):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)
    print(f"Page title: {driver.title}")

    try:
        example_button = driver.find_element(By.ID, "exampleButtonId")
        example_button.click()
        time.sleep(2)  # wait for 2 seconds to see the click action
    except:
        print("Button with ID 'exampleButtonId' not found.")
    
    try:
        example_input = driver.find_element(By.NAME, "exampleInputName")
        example_input.send_keys("Sample Text")
        time.sleep(2)  # wait for 2 seconds to see the text input action
    except:
        print("Input with NAME 'exampleInputName' not found.")
    
    try:
        example_link = driver.find_element(By.LINK_TEXT, "Example Link Text")
        example_link.click()
        time.sleep(2)  # wait for 2 seconds to see the link click action
    except:
        print("Link with text 'Example Link Text' not found.")
    
    driver.quit()

def main():
    # Example: Scraping headlines
    website_url = get_valid_url()
    tag, class_name = 'h2', ''  # Assume 'h2' tag without class for simplicity
    headlines = scrape_headlines(website_url, tag, class_name)
    if headlines:
        csv_file = f"headlines_{website_url.replace('http://', '').replace('https://', '').replace('/', '_')}.csv"
        df = pd.DataFrame(headlines, columns=["Headline"])
        df.to_csv(csv_file, index=False)
        print(f"Headlines have been exported to '{csv_file}'.")
    else:
        print("No headlines found.")

    # Example: Extracting table from PDF
    pdf_path = input("Enter the path to the PDF file: ").strip()
    extract_table_from_pdf(pdf_path)

    # Example: Automating website interaction
    url = get_valid_url()
    automate_website_interaction(url)

if __name__ == "__main__":
    main()
