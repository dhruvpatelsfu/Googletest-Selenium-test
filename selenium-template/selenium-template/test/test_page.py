from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from e1utils import construct_headless_chrome_driver, get_landing_page_url

def test_nonsecret_scenario():
    # test with incorrect secret code
    secret_code = "nabracabadra"

    # get page url and start browser
    page_url = get_landing_page_url()
    browser = construct_headless_chrome_driver()

    # open the landing page
    browser.get(page_url)

    # fill out the form with name, food, and wrong secret code
    browser.find_element(By.ID, "preferredname").send_keys("Steve")
    browser.find_element(By.ID, "food").send_keys("Apple")
    browser.find_element(By.ID, "secret").send_keys(secret_code)

    # submit the form
    browser.find_element(By.ID, "submit").click()

    # wait for the response page to load
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, "thankname")))

    # check the thank you message
    name_message = browser.find_element(By.ID, "thankname").text
    assert name_message == "Steve", f"Expected 'Steve', got '{name_message}'"

    # check the food message
    food_message = browser.find_element(By.ID, "foodploy").text
    assert food_message == "Apple", f"Expected 'Apple', got '{food_message}'"

    # verify secret button is not present
    secret_button = browser.find_elements(By.ID, "secretButton")
    assert len(secret_button) == 0, "Secret button should not be present"

    browser.quit()

def test_secret_scenario():
    # test for both secret codes "magic" "abracadabra"
    for secret_code in ["magic", "abracadabra"]:
        # get page url and start browser
        page_url = get_landing_page_url()
        browser = construct_headless_chrome_driver()

        # open the landing page
        browser.get(page_url)

        # fill out the form with name, food, and correct secret code
        browser.find_element(By.ID, "preferredname").send_keys("Steve")
        browser.find_element(By.ID, "food").send_keys("Apple")
        browser.find_element(By.ID, "secret").send_keys(secret_code)

        # submit the form
        browser.find_element(By.ID, "submit").click()

        # wait for the response page to load
        WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, "thankname")))

        # check the thank you message
        name_message = browser.find_element(By.ID, "thankname").text
        assert name_message == "Steve", f"Expected 'Steve', got '{name_message}'"

        # check the food message
        food_message = browser.find_element(By.ID, "foodploy").text
        assert food_message == "Apple", f"Expected 'Apple', got '{food_message}'"

        # check secret button is present
        secret_button = browser.find_element(By.ID, "secretButton")
        assert secret_button.is_displayed(), "Secret button should be present"

        # click the secret button and wait for the secret page to load
        secret_button.click()

        # wait for the secret page to load
        WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, "secret")))

        # check the secret page thank you message
        secret_name_message = browser.find_element(By.ID, "thankname").text
        assert secret_name_message == "Steve", f"Expected 'Steve', got '{secret_name_message}'"

        # check the secret code message
        secret_code_message = browser.find_element(By.ID, "secret").text
        assert secret_code_message == secret_code, f"Expected '{secret_code}', got '{secret_code_message}'"

        browser.quit()
