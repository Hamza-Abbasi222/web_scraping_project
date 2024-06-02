import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import camelot
from pathlib import Path

# Functions from T1_automation_script.py
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

# Functions from T2_extract_tables_from_pdf_using_camelot.py
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

# Functions from T3_xpath_example.py
def xpath_example():
    """Example of XPath usage."""
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Books</title>
    </head>
    <body>
        <h1>Book List</h1>
        <table>
            <tr>
                <th>Title</th>
                <th>Author</th>
            </tr>
            <tr>
                <td>1984</td>
                <td>George Orwell</td>
            </tr>
            <tr>
                <td>Brave New World</td>
                <td>Aldous Huxley</td>
            </tr>
        </table>
    </body>
    </html>
    '''

    tree = html.fromstring(html_content)

    # XPath queries
    title = tree.xpath('//title/text()')
    h1 = tree.xpath('//h1/text()')
    first_book_title = tree.xpath('//table/tr[2]/td[1]/text()')
    brave_new_world_author = tree.xpath('//table/tr[3]/td[2]/text()')
    all_rows = tree.xpath('//table/tr')

    print("Page Title:", title)
    print("Header (H1):", h1)
    print("First Book Title:", first_book_title)
    print("Author of Brave New World:", brave_new_world_author)

    print("All Rows:")
    for row in all_rows:
        print(row.xpath('.//td/text()'))

# Functions from T4_selenium_automation.py
def selenium_automation():
    """Automate website interactions using Selenium."""
    # Get the website URL from the user
    website_url = input("Enter the URL of the website you want to interact with: ").strip()

    # Set up WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)

    try:
        # Open the webpage
        driver.get(website_url)
        print("Page title:", driver.title)
        
        while True:
            # Ask the user what action they want to perform
            action = input("What action would you like to perform? (click, fill, quit): ").strip().lower()

            if action == "click":
                # Ask for the element locator
                by = input("Enter the type of locator (id, name, class_name, xpath, css_selector): ").strip().lower()
                value = input("Enter the locator value: ").strip()

                # Perform the click action
                try:
                    element = wait.until(EC.presence_of_element_located((getattr(By, by.upper()), value)))
                    element.click()
                    print(f"Clicked the element with {by} = {value}.")
                except Exception as e:
                    print(f"Error: {e}")
            
            elif action == "fill":
                # Ask for the element locator
                by = input("Enter the type of locator (id, name, class_name, xpath, css_selector): ").strip().lower()
                value = input("Enter the locator value: ").strip()

                # Ask for the text to fill
                text = input("Enter the text to fill: ").strip()

                # Perform the fill action
                try:
                    element = wait.until(EC.presence_of_element_located((getattr(By, by.upper()), value)))
                    element.send_keys(text)
                    element.send_keys(Keys.RETURN)
                    print(f"Filled the element with {by} = {value} with text '{text}'.")
                except Exception as e:
                    print(f"Error: {e}")
            
            elif action == "quit":
                print("Quitting...")
                break
            else:
                print("Invalid action. Please enter 'click', 'fill', or 'quit'.")

            # Wait for a few seconds for demonstration purposes
            time.sleep(2)
    
    finally:
        # Close the WebDriver
        driver.quit()

# Functions from T5_Automating_Websites_Using_Selenium4.py
def extract_specific_elements_with_xpath():
    """Extract specific elements from a website using XPath."""
    # Get the website URL from the user
    website_url = input("Enter the URL of the website you want to interact with: ").strip()

    # Set up WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Open the webpage
        driver.get(website_url)
        print("Page title:", driver.title)

        # Ask for the XPath of the elements to extract
        xpath = input("Enter the XPath of the elements you want to extract: ").strip()

        # Extract the elements using the provided XPath
        try:
            elements = driver.find_elements(By.XPATH, xpath)
            if elements:
                print(f"Found {len(elements)} elements:")
                for idx, element in enumerate(elements, start=1):
                    print(f"{idx}: {element.text}")
            else:
                print("No elements found with the provided XPath.")
        except Exception as e:
            print(f"Error extracting elements: {e}")

        # Wait for a few seconds for demonstration purposes
        time.sleep(5)

    finally:
        # Close the WebDriver
        driver.quit()

# Functions from T6_scrape_headlines.py
def export_headlines_to_csv():
    """Extract headlines from a website and export them to a CSV file."""
    # Get the website URL from the user
    website_url = input("Enter the URL of the website you want to scrape headlines from: ").strip()

    # Get the HTML tag and class name for headlines
    tag = input("Enter the HTML tag used for the headlines (e.g., 'h1', 'h2', 'div'): ").strip()
    class_name = input("Enter the class name used for the headlines (leave blank if not applicable): ").strip()

    # Scrape the headlines
    response = requests.get(website_url)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    if class_name:
        headlines = soup.find_all(tag, class_=class_name)
    else:
        headlines = soup.find_all(tag)

    if headlines:
        # Store the headlines in a Pandas DataFrame
        df = pd.DataFrame([headline.get_text(strip=True) for headline in headlines], columns=["Headline"])

        # Export the DataFrame to a CSV file
        df.to_csv("headlines.csv", index=False)
        print("Headlines have been exported to 'headlines.csv'.")
    else:
        print("No headlines found with the provided tag and class.")


if __name__ == "__main__":
    main()