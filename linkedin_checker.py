import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

def init_driver(headless=False):
    """
    Initialize undetected Chrome with anti-detection options.
    headless=False => browser is visible
    """
    options = uc.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")

    # Anti-detection / privacy options
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--disable-automation")
    options.add_argument("--disable-features=CDP")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-breakpad")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--disable-component-update")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-domain-reliability")
    options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    options.add_argument("--disable-hang-monitor")
    options.add_argument("--disable-ipc-flooding-protection")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-offline-auto-reload")
    options.add_argument("--disable-password-generation")
    options.add_argument("--disable-payments-api")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-renderer-accessibility")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-speech-api")
    options.add_argument("--disable-usbguard")
    options.add_argument("--disable-web-security")
    options.add_argument("--log-level=3")

    driver = uc.Chrome(options=options, version_main=139)
    return driver


def login_linkedin(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    print("---------------------------------")
    print("-------- Driver Statred ---------")
    print("---------------------------------")
    time.sleep(random.uniform(1, 2))
    driver.find_element(By.ID, "username").send_keys(username)
    time.sleep(random.uniform(0.5, 1))
    driver.find_element(By.ID, "password").send_keys(password)
    time.sleep(random.uniform(0.5, 1))
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.search-global-typeahead__input"))
        )
        print("[INFO] Login successful.")
    except TimeoutException:
        print("[ERROR] Could not find the search bar. Check login credentials.")
        driver.quit()
        exit(1)


def human_scroll(driver):
    """
    Scrolls the page in small random increments to simulate human behavior.
    """
    scroll_pause = random.uniform(0.3, 0.7)
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    current_scroll = 0
    while current_scroll < scroll_height:
        increment = random.randint(100, 300)
        current_scroll += increment
        driver.execute_script(f"window.scrollTo(0, {current_scroll});")
        time.sleep(scroll_pause)
        if current_scroll >= scroll_height:
            break
    # Small back-and-forth scroll
    driver.execute_script(f"window.scrollBy(0, {-random.randint(50, 150)});")
    time.sleep(random.uniform(0.2, 0.5))


def check_linkedin_profile(driver, url):
    try:
        driver.get(url)
        time.sleep(random.uniform(1, 2))

        if "linkedin.com/in/" not in driver.current_url.lower():
            return False, ""

        driver.find_element(By.TAG_NAME, "main")
        human_scroll(driver)

        try:
            name_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h1[contains(@class,'inline t-24 v-align-middle break-words')]")
                )
            )
            name = name_element.text.strip()
        except TimeoutException:
            name = ""
            print("[WARNING] Could not find profile name.")

        # Random small pause to simulate human reading
        time.sleep(random.uniform(0.5, 1.5))
        return True, name

    except (NoSuchElementException, TimeoutException):
        return False, ""
