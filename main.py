import os
import time
import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Env variables
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
STARTING_URL = os.getenv('STARTING_URL')
TARGET_TIME = os.getenv('TARGET_TIME')

# Login related constants
USERNAME_ID = 'p_lt_ContentWidgets_pageplaceholder_p_lt_zoneContent_CHO_Widget_LoginFormWithFullscreenBackground_XLarge_loginCtrl_BaseLogin_UserName'
PASSWORD_ID = 'p_lt_ContentWidgets_pageplaceholder_p_lt_zoneContent_CHO_Widget_LoginFormWithFullscreenBackground_XLarge_loginCtrl_BaseLogin_Password'
LOGIN_BUTTON_ID = 'p_lt_ContentWidgets_pageplaceholder_p_lt_zoneContent_CHO_Widget_LoginFormWithFullscreenBackground_XLarge_loginCtrl_BaseLogin_LoginButton'

# Navigation related constants
SPORT_BOOKINGS_XPATH = "//a[text()='Sport Bookings']"
TENNIS_XPATH = "//a[text()='TENNIS']"
DATE_SELECTOR_XPATH = "//div[@id='dateSelector-picker']/ul/li[last()]"
COURT_6_HEADER_XPATH = "//th[a/span/text()='Court 6']"
TIMESLOT_XPATH_TEMPLATE = f"//table[@class='courtViewer']/tbody/tr/td[{{}}]//div[contains(@class, 'timeslot') and .//div[@class='time' and contains(text(),  '{TARGET_TIME}')]]"

# Screenshot related constants
SUCCESS_SCREENSHOT_PATH = "screenshot_success.png"
ERROR_SCREENSHOT_PATH = "screenshot_error.png"

# Booking related constants
# TARGET_TIME = datetime.time(hour=8, minute=0, second=0)  # 08:00:00 AM
TARGET_TIME = datetime.time(hour=20, minute=27, second=0)


def wait_for_visibility(driver, by, value, timeout=5):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.visibility_of_element_located((by, value)))


def wait_for_visibility_of_elements(driver, by, value, timeout=5):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.visibility_of_all_elements_located((by, value)))


# Main script
def main():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    load_dotenv()

    try:
        if os.path.exists(ERROR_SCREENSHOT_PATH):
            os.remove(ERROR_SCREENSHOT_PATH)
            print(f"Deleted {ERROR_SCREENSHOT_PATH}")
        else:
            print(f"{ERROR_SCREENSHOT_PATH} does not exist")

        if os.path.exists(SUCCESS_SCREENSHOT_PATH):
            os.remove(SUCCESS_SCREENSHOT_PATH)
            print(f"Deleted {SUCCESS_SCREENSHOT_PATH}")
        else:
            print(f"{SUCCESS_SCREENSHOT_PATH} does not exist")

        driver.get(STARTING_URL)

        username_field = wait_for_visibility(driver, By.ID, USERNAME_ID)
        password_field = wait_for_visibility(driver, By.ID, PASSWORD_ID)

        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)

        login_button = wait_for_visibility(driver, By.ID, LOGIN_BUTTON_ID)
        login_button.click()

        sport_bookings_button = wait_for_visibility(driver, By.XPATH, SPORT_BOOKINGS_XPATH)
        sport_bookings_button.click()

        tennis_button = wait_for_visibility(driver, By.XPATH, TENNIS_XPATH)
        tennis_button.click()

        last_li = wait_for_visibility(driver, By.XPATH, DATE_SELECTOR_XPATH)
        last_li.find_element(By.TAG_NAME, "a").click()

        now = datetime.datetime.now()
        current_time = now.time()

        if current_time > TARGET_TIME:
            target_datetime = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), TARGET_TIME)
        else:
            target_datetime = datetime.datetime.combine(now.date(), TARGET_TIME)

        time_difference = (target_datetime - now).total_seconds()

        print(f"Sleeping for {time_difference} seconds until {target_datetime}")
        time.sleep(time_difference)

        print("Target time reached. Executing actions...")

        court_6_elements = wait_for_visibility_of_elements(driver, By.XPATH,
                                                           f"{COURT_6_HEADER_XPATH}/preceding-sibling::th")
        court_6_index = len(court_6_elements) + 1

        timeslot_xpath = TIMESLOT_XPATH_TEMPLATE.format(court_6_index)

        timeslot_element = wait_for_visibility(driver, By.XPATH, timeslot_xpath)
        timeslot_element.click()

        driver.save_screenshot('screenshot_success.png')

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot('screenshot_error.png')

    finally:
        print('script done')
        # driver.quit()


if __name__ == "__main__":
    main()
