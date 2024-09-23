from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

debbuging = bool(os.getenv("DEBUG"))
script_dir = Path(__file__).resolve().parent
driver_path = script_dir.joinpath("driver", "chromedriver")
driver_options = Options()

if debbuging:
    # driver_options.add_argument('start-maximized')
    driver_options.add_experimental_option("detach", True)
else:
    driver_options.add_argument("--headless")


def wait_for_elements (driver, by, element_identifier, timeout = 15):
    try:
        WebDriverWait(driver, timeout).until(ec.visibility_of_element_located((by, element_identifier)))
        print(f"{element_identifier} found and loaded")
    except TimeoutException:
        print(f"Timeout waiting for {element_identifier}")
        return None
    
    return driver.find_element(by, element_identifier)


def login(driver):
    driver.get(os.getenv('URL'))
    accept_cookies_btn = wait_for_elements(driver, By.ID, "onetrust-accept-btn-handler")

    if accept_cookies_btn:
        accept_cookies_btn.click()
        
        password_input = wait_for_elements(driver, By.ID, "loginLoginWrap")
        username_input = wait_for_elements(driver, By.XPATH, '//input[@type="email"][@name="login"]')  
        sign_in_btn = wait_for_elements(driver, By.XPATH, '//button[@type="submit"]')
        
        if (
            username_input 
            and password_input 
            and sign_in_btn
        ):
            username_input.send_keys("morvinian@gmail.com")
            password_input.send_keys("12345678")
            sign_in_btn.click()

        else:
            print("Unable to find username and password fields")
    else:
        print("Accept cookies Btn not found")

def main_config():
    service= Service(driver_path)
    driver = webdriver.Chrome(service = service, options = driver_options)
    
    try:
        login(driver)
    except WebDriverException as e:
        print(f"An error occurred: {e}")
    finally:
        if not debbuging:
            driver.quit()
            
if __name__ == "__main__":
    main_config()