# T7_main_script.py

from T1_automation_script import fetch_data, extract_information, generate_reports
from T2_extract_tables_from_pdf_using_camelot import extract_tables_from_pdf, save_tables_as_csv
from T3_xpath_example import xpath_example
from T4_selenium_automation import selenium_automation
from T5_Automating_Websites_Using_Selenium4 import extract_specific_elements_with_xpath
from T6_scrape_headlines import export_headlines_to_csv

def main():
    print("Select an option:")
    print("1. Fetch Data and Generate Reports")
    print("2. Extract Tables from PDF")
    print("3. XPath Example")
    print("4. Selenium Automation")
    print("5. Extract Specific Elements with XPath")
    print("6. Export Headlines to CSV")
    print("7. Exit")
    
    option = input("Enter your choice: ").strip()
    
    if option == "1":
        url = input("Enter the URL: ").strip()
        tag_class_pairs = [
            ('h1', 'class1'),
            ('p', 'class2')
            # Add more as needed
        ]
        soup = fetch_data(url)
        data = extract_information(soup, tag_class_pairs)
        generate_reports(data)
    elif option == "2":
        pdf_path = input("Enter the path to the PDF file: ").strip()
        tables = extract_tables_from_pdf(pdf_path)
        output_csv = input("Enter the name of the output CSV file: ").strip()
        save_tables_as_csv(tables, output_csv)
    elif option == "3":
        xpath_example()
    elif option == "4":
        selenium_automation()
    elif option == "5":
        extract_specific_elements_with_xpath()
    elif option == "6":
        export_headlines_to_csv()
    elif option == "7":
        print("Exiting...")
    else:
        print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
