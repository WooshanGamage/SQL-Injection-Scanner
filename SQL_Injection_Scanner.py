import sys # System-specific functions and variables
import requests as re # HTTP requests library (aliased as 're')
from bs4 import BeautifulSoup as  BS # HTML/XML parsing (aliased as 'BS')
from urllib.parse import urljoin as UJ # Join base and relative URLs (aliased as 'UJ')
import time  # Time-related functions

LinkedIn = "\n My LinkedIn profile - \033[34m https://www.linkedin.com/in/wooshan-gamage-5b03b91bb/ \033[0m"
Github = " My Github profile   - \033[35m https://github.com/WooshanGamage \033[0m\n"  # Purple (35m is the code for purple)
http_session = re.Session()  # Create a new HTTP session
http_session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"  # Set User-Agent header for the session


def extract_forms_from_page(url):  # Define a function to extract forms from a given URL
    parsed_html = BS(http_session.get(url).content, "html.parser")  # Fetch and parse HTML content from the URL
    return parsed_html.find_all("form")  # Return all form elements found in the parsed HTML


def extract_form_details(form):  # Define a function to extract details from a form element
    form_details = {}  # Initialize a dictionary to store form details
    form_action = form.attrs.get("action")  # Get the 'action' attribute of the form
    form_method = form.attrs.get("method", "get").lower()  # Get the 'method' attribute and convert to lowercase
    input_fields = []  # Initialize a list to store input fields

    for input_tag in form.find_all("input"):  # Iterate over all input tags in the form
        input_type = input_tag.attrs.get("type", "text")  # Get the 'type' attribute
        input_name = input_tag.attrs.get("name")  # Get the 'name' attribute
        input_value = input_tag.attrs.get("value", "")  # Get the 'value' attribute
        input_fields.append({
            "type": input_type,
            "name": input_name,
            "value": input_value
        })

    form_details['action'] = form_action  # Add form action to details
    form_details['method'] = form_method  # Add form method to details
    form_details['inputs'] = input_fields  # Add input fields to details
    return form_details  # Return the form details dictionary

def is_response_vulnerable(response): # Define a function to check if the response indicates a vulnerability
    sql_error_messages = { # Define a set of common SQL error messages
        "quoted string not properly terminated",
        "unclosed quotation mark after the character string",
        "you have an error in your SQL syntax",
        "unknown column in 'field list'",
        "unexpected end of SQL command",
        "Warning: mysql_num_rows() expects parameter 1 to be resource",
        "Warning: mysql_fetch_array() expects parameter 1 to be resource",
        "SQL syntax error",
        "unrecognized token",
        "syntax error at or near",
        "division by zero",
        "missing right parenthesis",
        "Incorrect integer value",
        "Invalid SQL statement",
        "Subquery returns more than 1 row",
        "Data truncation: Data too long for column",
        "Conversion failed when converting",
        "ORA-00933: SQL command not properly ended",
        "ORA-00942: table or view does not exist",
        "SQLite3::SQLException: unrecognized token",
        "PostgreSQL error: Fatal error",
        "MySQL server version for the right syntax"
    }
    for error_message in sql_error_messages:  # Iterate over the SQL error messages
        if error_message in response.content.decode().lower():  # Check if the error message is in the response content
            return True  # Return True if a SQL error message is found
    return False  # Return False if no SQL error messages are found

# Function to scan a URL for SQL injection vulnerabilities
def scan_for_sql_injection(url):  # Define a function to scan a URL for SQL injection vulnerabilities
    forms_on_page = extract_forms_from_page(url)  # Extract forms from the page
    print(f"[+] Detected {len(forms_on_page)} forms on {url}.\n")  # Print the number of detected forms

    for form in forms_on_page:  # Iterate over each form on the page
        FORM_details = extract_form_details(form)  # Extract details from the form
        form_action = FORM_details['action']  # Get the form's action URL
        form_action_url = UJ(url, form_action)  # Construct the absolute URL for the form action
        print(f"[+] Form details: {FORM_details}")  # Print the form details

        vulnerable_flag = False  # Initialize the flag to check if vulnerability is found

        for i in "\"'":  # Iterate over both double and single quotes
            form_data = {}  # Initialize a dictionary to store form data
            for input_tag in FORM_details["inputs"]:  # Iterate over each input field in the form
                if input_tag["type"] == "hidden" or input_tag["value"]:  # Handle hidden inputs or inputs with values
                    form_data[input_tag['name']] = input_tag["value"] + i  # Append index to the value
                elif input_tag["type"] != "submit":  # Handle non-submit inputs
                    form_data[input_tag['name']] = f"test{i}"  # Set a test value with index

            if FORM_details["method"] == "post":  # Handle POST request
                response = http_session.post(form_action_url, data=form_data)  # Send POST request with form data
            elif FORM_details["method"] == "get":  # Handle GET request
                response = http_session.get(form_action_url, params=form_data)  # Send GET request with form data

            if is_response_vulnerable(response):  # Check if the response indicates a vulnerability
                vulnerable_flag = True  # Set flag to True if vulnerability detected
                print(f"SQL Injection vulnerability detected in form at {form_action_url}")  # Print vulnerability message
                break  # Exit loop as we've already detected a vulnerability

        if not vulnerable_flag:  # Check if no vulnerability was detected
            print(f"No SQL Injection vulnerability detected in form at {form_action_url}")  # Print message if no vulnerability found

if __name__ == "__main__":
    print('\033[38;5;214m' + r'''
       _____  ____  _         _____       _           _   _                 _____                                 
      / ____|/ __ \| |       |_   _|     (_)         | | (_)               / ____|                                
     | (___ | |  | | |         | |  _ __  _  ___  ___| |_ _  ___  _ __    | (___   ___ __ _ _ __  _ __   ___ _ __ 
      \___ \| |  | | |         | | | '_ \| |/ _ \/ __| __| |/ _ \| '_ \    \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
      ____) | |__| | |____    _| |_| | | | |  __/ (__| |_| | (_) | | | |   ____) | (_| (_| | | | | | | |  __/ |   
     |_____/ \___\_\______|  |_____|_| |_| |\___|\___|\__|_|\___/|_| |_|  |_____/ \___\__,_|_| |_|_| |_|\___|_|   
                                        _/ |                                                                     
                                       |__/                                                                      
    ''' + '\033[0m \n                                                               \033[92m - Wooshan Gamage ( Team Encryptix )\033[0m\n')
    print('''If you want to exit, type "0" in the "Input a URL" tab''') # Print exit instruction

    while True:  # Start an infinite loop for user input
        url_to_scan = input("\n Input a URL : ")  # Prompt user for a URL to scan
        if url_to_scan == "0":  # Check if the user wants to exit
            sys.exit()  # Exit the program
        elif not url_to_scan:  # Check if the URL input is empty
            print("URL can't be empty") # Print an error message for empty URL
            continue  # Restart the loop to prompt for input again
        print()
        scan_for_sql_injection(url_to_scan)  # Scan the provided URL for SQL injection

        time.sleep(1)# Wait for 1 second
        print(LinkedIn) # Print LinkedIn information
        time.sleep(1)  # Wait for 1 second
        print(Github)  # Print GitHub information
        time.sleep(1)  # Wait for 1 second
