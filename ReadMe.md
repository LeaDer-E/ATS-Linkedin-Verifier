
# LinkedIn Resume Checker - [Hebr SA](https://hebrsa.com/)

## Overview

This tool is designed to be run periodically to verify LinkedIn profile links extracted from ATS-style CVs (DOCX files). If a candidate updates or changes their LinkedIn URL, the system detects this change so that their resume can be updated accordingly after the client sends us the new link.

The program extracts LinkedIn URLs from the first 5 lines of DOCX resumes (assumed ATS format), logs into LinkedIn using Selenium, checks each profile’s accessibility and name, then generates output reports in **Excel** and **dark-themed HTML** formats.

---

## Features

- Extract LinkedIn profile links and phone numbers from DOCX resumes.
- Check LinkedIn profile status and extract the profile name.
- Output:
  - **Excel report** with clickable hyperlinks, custom formatting, centered text, yellow-highlighted headers, bold filename column, and adjusted column widths.
  - **HTML report** with dark theme, filter by status (valid/invalid/all), and clean layout.
- Advanced Logger included with easy enable/disable.
- Ability to exclude specific folders or files by adding their names to `EX.txt`.
- Freezing of header row and first column in Excel for better navigation.
- Supports manual control of logging verbosity.

---

## Important Notes & Usage Warnings

- **Designed only for ATS resumes** where client data (including LinkedIn URL) appears within the first 5 lines of DOCX files.
- The terminal output is minimal and not emphasized, as Excel and HTML reports are the primary outputs.
- **Use at your own risk:** LinkedIn may detect automated Selenium login and block or limit access. To minimize detection:
  - Consider using an undetectable ChromeDriver.
  - Modify `linkedin_checker.py` accordingly.
- ChromeDriver **must be installed** and compatible with your Chrome version for Selenium to work.
- The tool was built specifically for [Hebr SA](https://hebrsa.com/)’s resume validation workflow but can be adapted for similar ATS-based DOCX files.

---

## Project Structure

``` bash
	linkedin_verifier/
	│
	├── Account.py # Stores LinkedIn login credentials (username, password)
	├── Main.py # Main script to run the program
	├── file_reader.py # Reads DOCX files, extracts LinkedIn links and phone numbers
	├── linkedin_checker.py # Handles LinkedIn login and profile verification using Selenium
	├── output_manager.py # Manages displaying results and saving them to HTML and Excel
	├── utils.py # Utility functions such as regex patterns and timing decorators
	├── logging_config.py # Configures the logging system
	├── requirements.txt # Required Python packages
	└── README.md # This file with usage instructions
```

---

## Installation & Setup

### Windows

1. Ensure Python 3.9+ is installed.
2. Open **Command Prompt** or **PowerShell**.
3. (Optional) Create virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

4. Install required packages:

```bash
pip install -r requirements.txt
```

Or individually:

```bash
pip install python-docx selenium openpyxl pandas undetected_chromedriver setuptools
```

5. Download **ChromeDriver** matching your Chrome version and place it in your system PATH or project directory.

### Ubuntu

1. Install Python3 and pip:

```bash
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-distutils
```

2. (Optional) Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:

```bash
pip3 install -r requirements.txt
```

Or individually:

```bash
pip3 install python-docx selenium openpyxl pandas undetected_chromedriver setuptools
```

4. Download **ChromeDriver** matching your Chrome version and place it in your system PATH or project directory.

---

## Running the Program

```bash
python main.py <path_to_folder_with_DOCX_files>
```

Example:

```bash
python main.py "./resumes"
```

### Test Mode

Run without accessing LinkedIn (mock results) for testing:

```bash
python main.py <path_to_folder_with_DOCX_files> --test
```

### Additional
- in main.py:
```bash
@timing(logger)
def process_files(folder_path, test_mode=False): 
    files = get_all_docx_files(folder_path)
    logger.info(f"Found {len(files)} DOCX files")

    exclusion_file = os.path.join(os.path.dirname(__file__), "EX.txt")
    exclude_names = set()
    if os.path.exists(exclusion_file):
        with open(exclusion_file, "r", encoding="utf-8") as f:
            exclude_names = set(line.strip() for line in f if line.strip())

    results = []
    driver = None
    if not test_mode:
        driver = init_driver(headless=False) #You Can Change it to "True" to make the browser hidded
        try:
            login_linkedin(driver, USERNAME, PASSWORD)
        except Exception as e:
            if driver:
                driver.quit()
            return []
```
- Take a look at this Line
```bash
        driver = init_driver(headless=False) #You Can Change it to "True" to make the browser hidded
```
---

## Output Files
All outputs are saved in the `/Status/` folder with timestamped filenames.

### Excel Report

- Saved in `/Status/` with timestamp.
- Columns:

| File Name    | Phone         | Full Path               | Link                                                                   | Folder Name | Name       | Result |
| ------------ | ------------- | ----------------------- | ---------------------------------------------------------------------- | ----------- | ---------- | ------ |
| resume1.docx | +966555123456 | C:/Resumes/resume1.docx | [https://linkedin.com/in/johndoe](https://linkedin.com/in/johndoe)     | August2025  | John Doe   | ✔     |
| resume2.docx | +966555654321 | C:/Resumes/resume2.docx | [https://linkedin.com/in/janesmith](https://linkedin.com/in/janesmith) | August2025  | Jane Smith | ✖     |

- Features:
  - Clickable LinkedIn links (blue & underlined).
  - Yellow header row.
  - Bold 'File Name' column.
  - Centered text.
  - Freeze panes: first row & column.
  - Font size 16.
  - Full borders.

### HTML Report

- Dark themed, responsive table.
- Filter dropdown: all, valid, invalid.
- Columns match Excel report.
- Color-coded status icons (✔ valid / ✖ invalid).

---

## Logging (Advanced Logger)

- The program uses an **advanced logging system** for debug and error tracking.
- By default, logging output is suppressed by this line in `main.py`:

  ```python
  logging.disable(logging.CRITICAL)
  ```

- To enable logging (for troubleshooting or detailed information):
  - Comment out or remove the above line.
  - Logs will print to the console at debug/info/warning/error levels.

---

## Excluding Files or Folders from Scanning

- A file named `EX.txt` in the program root.
- List one folder name or file name per line to exclude from scanning.
- The program skips any DOCX file or folder matching these names.

Example `EX.txt`:

```
exclude_folder
do_not_scan_this_file.docx
```

---

## Disclaimer

This tool is provided **as-is** for internal use within [Hebr SA](https://hebrsa.com/) workflows. Using automation on LinkedIn may violate their terms and risks account restrictions. Use responsibly and at your own discretion.

---

## Contact & Support

For direct support or inquiries, contact:

**Eslam Mustafa**  
Email: eslaam.mustafa@gmail.com

---

## License

Use under your own responsibility. Adhere to LinkedIn’s Terms of Service.


---
