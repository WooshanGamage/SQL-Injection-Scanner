# SQL Injection Vulnerability Scanner

A Python-based utility designed to enhance web security by automating the detection of SQL injection vulnerabilities in web forms.

## Overview

SQL Injection is one of the most dangerous vulnerabilities in web applications, allowing attackers to manipulate database queries through user input fields. This scanner bridges the gap between complex security tools and practical usage by offering a simple yet powerful solution for identifying SQL injection vulnerabilities.

## Features

- **Automated Scanning**: Detect SQL injection vulnerabilities by injecting test payloads into form fields and analyzing server responses.
- **Easy to Use**: Command-line interface guides users through scanning processes, suitable for both beginners and professionals.
- **Form Extraction**: Uses BeautifulSoup to parse HTML and identify form elements automatically.
- **Error Handling**: Includes robust error detection for common SQL error messages to highlight potential security flaws.

## How It Works

1. **Form Extraction**: The tool parses web forms on the given URL, identifying inputs, actions, and methods (GET/POST).
2. **Payload Injection**: It injects test payloads, such as common SQL injection patterns, into form fields.
3. **Response Analysis**: The scanner checks the server's response for error messages indicative of SQL injection vulnerabilities.

## Limitations
- Only works with publicly accessible URLs.
- May not detect vulnerabilities on forms that require authentication or those with suppressed error messages.
- Currently focuses on basic error-based SQL injection detection.

## Future Enhancements
-Support for authentication and session management.
-Detection of advanced injection techniques like blind and time-based SQL injections.
-Integration of reporting features to generate vulnerability summaries.

##Ethical Considerations
Ensure that you have proper authorization before scanning any web applications. Unauthorized vulnerability scanning is illegal and may result in severe legal consequences.

## Authors
# M.G. Wooshan Rukmal Gamage
**Undergraduate | Computer Science**  
University of Westminster

**LinkedIn**:  [Wooshan Gamage](https://www.linkedin.com/in/wooshan-gamage-5b03b91bb/)  
**GitHub**:  [WooshanGamage](https://github.com/WooshanGamage)  
**Medium**:  [WooshanGamage](https://medium.com/@wooshangamage)

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Requirements

- Python 3.12 or higher
- Libraries:
  - `requests`
  - `BeautifulSoup4`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/WooshanGamage/sql-injection-scanner.git
    ```
2. Navigate to the project directory:
    ```bash
    cd sql-injection-scanner
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the scanner, execute the following command:

```bash
python3 SQL_Injection_Scanner.py
