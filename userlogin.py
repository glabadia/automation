from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

SLEEP_TIME: int = 10


def userLogin(un, pw, driver):
    """
    automates userLogin
    """
    # UserId, Password, btnlogin
    driver.find_element_by_id("UserId").send_keys(un)
    driver.find_element_by_id("Password").send_keys(pw)
    driver.find_element_by_id("btnlogin").click()


def userLoginIdirect(un, pw, driver):
    """
    automates userLogin
    """
    loginPath = "//div[@id='login_container_web']//a[@class='btn btn-primary'][contains(text(),'Login')]"
    loginButton = WebDriverWait(driver, SLEEP_TIME).until(
        EC.presence_of_element_located((By.XPATH, loginPath)))
    loginButton.click()

    driver.find_element_by_id("username").send_keys(un)
    driver.find_element_by_id("password").send_keys(pw)
    driver.find_element_by_id("login-command").click()
