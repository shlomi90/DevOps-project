import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1200")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Test function with parameterization
@pytest.mark.parametrize("buttons_sequence, expected_result", [
    (["1", "0", "÷", "0", "="], "Infinity"),
    (["1", "0", "÷", "2", "="], "5"),
    (["1", "0", "+", "3", "="], "13"),
])
def test_calculator(buttons_sequence, expected_result):
    url = "http://localhost"
    se = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=se, options=chrome_options)
    driver.get(url)

    try:
        # Click the AC button to clear any previous input
        ac_button = driver.find_element(By.CSS_SELECTOR, ".btn.clr")
        ac_button.click()
        time.sleep(0.5)  

        for button_text in buttons_sequence:
            if button_text == "=":
                button = driver.find_element(By.ID, "equalbtn")
            else:
                button = driver.find_element(By.XPATH, f"//button[text()='{button_text}']")
            button.click()
            time.sleep(0.5)  # Adding a short delay to ensure the button click is processed

        answer_element = driver.find_element(By.CLASS_NAME, "input")
        answer_value = answer_element.get_attribute("value")

        assert answer_value == expected_result, f"Test failed: {buttons_sequence} expected {expected_result}, but got {answer_value}."
    finally:
        ac_button.click()
        # Ensure to quit the driver even if an error occurs
        driver.quit()
