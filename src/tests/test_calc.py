import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService



# Setup Chrome options
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("no-sandbox")
options.add_argument("headless")
options.add_argument("window-size=1400,2100")


# Test function with parameterization
@pytest.mark.parametrize("expression, expected_result", [
    ("3+5", "8"),
    ("4*5", "20"),
    ("10-2", "8"),
    ("6/2", "3"),
])
def test_calculation(expression, expected_result):
    url = "http://localhost:3000/"
    # webdriver_path = 'C:/Users/shlom/Downloads/chromedriver-win64/chromedriver.exe'
    
    se = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=se, options=options)
    driver.get(url)

    try:
        # Locate the input element and clear it
        input_element = driver.find_element(By.CLASS_NAME, "input")
        input_element.clear()
        input_element.send_keys(expression)

        # Locate and click the equals button
        equal_button = driver.find_element(By.ID, "equalbtn")
        equal_button.click()

        # Locate the result element and retrieve its value
        answer_element = driver.find_element(By.CLASS_NAME, "input")
        answer_value = answer_element.get_attribute("value")

        # Check if the actual result matches the expected result
        assert answer_value == expected_result, f"Test failed: {expression} expected {expected_result}, but got {answer_value}."
    finally:
        # Locate and click the AC (clear) button to reset the calculator
        ac_button = driver.find_element(By.CSS_SELECTOR, ".btn.clr")
        ac_button.click()
        driver.quit()
        

# Run the test cases
test_calculation("3+5", "8")
test_calculation("4*5", "20")
test_calculation("10-2", "8")
test_calculation("6/2", "3")
