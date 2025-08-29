#Main.py
import sys
import os
from datetime import datetime
from Account import USERNAME, PASSWORD
from file_reader import get_all_docx_files, extract_linkedin_links, extract_phone_number
from linkedin_checker import init_driver, login_linkedin, check_linkedin_profile
from output_manager import display_results_terminal, save_results_html, save_results_excel
from logging_config import setup_logger
from utils import timing
import logging

logger = setup_logger()
logging.disable(logging.CRITICAL)

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

    for file_path in files:
        file_name = os.path.basename(file_path)
        folder_name = os.path.basename(os.path.dirname(file_path))
        if file_name in exclude_names or folder_name in exclude_names:
            continue

        phone = extract_phone_number(file_path)
        links = extract_linkedin_links(file_path)
        if not links:
            results.append({
                "file_name": file_name,
                "full_path": file_path,
                "folder_name": folder_name,
                "phone": phone,
                "link": "",
                "name": "",
                "status": False
            })
        else:
            for link in links:
                try:
                    if test_mode:
                        status, name = True, "Mock Name"
                    else:
                        status, name = check_linkedin_profile(driver, link)
                except Exception:
                    status, name = False, ""
                results.append({
                    "file_name": file_name,
                    "full_path": file_path,
                    "folder_name": folder_name,
                    "phone": phone,
                    "link": link,
                    "name": name,
                    "status": status
                })

    if driver:
        driver.quit()

    # Remove duplicates
    unique_results = []
    seen = set()
    for r in results:
        key = (r["file_name"], r["link"])
        if key not in seen:
            seen.add(key)
            unique_results.append(r)

    # Ensure 'status' field exists for all
    for r in unique_results:
        if "status" not in r:
            r["status"] = False

    return unique_results

@timing(logger)
def save_results(results):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    status_dir = os.path.join(base_dir, "Status")
    os.makedirs(status_dir, exist_ok=True)

    save_results_html(results, status_dir)
    save_results_excel(results, status_dir)

def main(folder_path, test_mode=False):
    results = process_files(folder_path, test_mode=test_mode)
    display_results_terminal(results)
    save_results(results)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <folder_path> [--test]")
        sys.exit(1)
    folder_path = sys.argv[1]
    test_mode = "--test" in sys.argv
    main(folder_path, test_mode=test_mode)
