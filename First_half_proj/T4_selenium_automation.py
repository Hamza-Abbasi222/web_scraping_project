# T4_selenium_automation.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
