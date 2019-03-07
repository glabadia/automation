from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

WAIT_TIME:  int = 10


def checkNoResultsMessage(driver):
    # = > for no result message not displayed (Note the "")
    noResultsPath = "//div[@class = 'no-result-message '][@style = '']"
    try:
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, noResultsPath)))
        # driver.find_element_by_xpath(noResultsPath)
    except Exception:
        # print(f"Error: {e}")
        return False
    return True
