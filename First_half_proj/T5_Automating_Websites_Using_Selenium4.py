# T5_Automating_Websites_Using_Selenium4.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

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


if __name__ == "__main__":
    extract_specific_elements_with_xpath()