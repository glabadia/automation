from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from time import sleep, time
from utils import errorCheckUpd, printErrors, dictErrors, getAuctionHouse, printToFile, createDirectory, convert_time
from results import expandVehicleInfoIdirect, retrieveInfoTest, retrieveInfoUpd
from errors import checkNoResultsMessage

import asyncio
WAIT_TIME: int = 10
SLEEP_TIME: int = 5


def nextResults(webdriver):
    '''
    #1  Get current page number
    #2  Get Next page number reference
    '''
    getActiveLink = "//ul[@class='pagination margin-top-bottom-none']//li[@class='active']"
    getNextLink = "/following-sibling::li[1]//a"

    infoList = []

    startDC = time()
    isEnd = False
    hasGotAuctionName = False

    auctionHouseName = ""

    while not isEnd:
        print("Incur python to sleep..")
        # Data Collection lasted for 6 minutes and 32.5 seconds.
        # //div[@class="no-result-message "][@style="display: none;"]=> for no result message not displayed
        # //div[@class="no-result-message "][@style=""]=> for no result message not displayed (Note the "")
        sleep(SLEEP_TIME)
        # naa osaka has issues
        checkMessage = checkNoResultsMessage(webdriver)
        print(f"No resuls message: {checkMessage}")
        if checkMessage:
            break

        expandVehicleInfoIdirect(webdriver)

        # init errorchecking..
        # if error exists => break while loop

        if not hasGotAuctionName:
            hasGotAuctionName = True
            auctionHouseName = getAuctionHouse(webdriver)

        activePage = WebDriverWait(webdriver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, getActiveLink)))
        # print(f"Active Page: {activePage.text}")
        nextPage = WebDriverWait(webdriver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, f"{getActiveLink}/{getNextLink}")))

        print(f"Checking [Page {activePage.text}]..")

        start = time()
        retrieved_details = retrieveInfoUpd(webdriver)
        infoList.extend(retrieved_details)
        end = time()
        # print(retrieved_details)

        if nextPage.text == "»":
            isEnd = True
            print("Traverse reached last page..")
            print()
            break
        else:
            print(
                f"Finished checking [{auctionHouseName}, Page {activePage.text}] in {(end-start):.1f} seconds.")
            print()
            print(f"Next is [Page {nextPage.text}]..")
            nextPage.click()
    else:
        print("Traverse has reached the end.")
        print()

    endDC = time()

    timeDC = endDC-startDC
    print(f"Finished collecting data in {timeDC} seconds.")

    print(f"Now, getting to check for errors..")
    print()
    startCheck = time()
    checkErrorList = errorCheckUpd(infoList)

    populate_errors = dictErrors(checkErrorList[1])
    # print(populate_errors)
    print("----------------------------------------------------------")
    printErrors(populate_errors)

    endCheck = time()
    checkDuration = endCheck - startCheck
    print(f"Error checking in {convert_time(checkDuration)} seconds.")

    printToFile((timeDC, checkDuration), createDirectory(),
                auctionHouseName, populate_errors)

    # check if //div[@id='loader'][contains(@style,'display: block;')] wait until display: none
    #   loader style --> display: block; top: 0px; bottom: 0px; left: 0px; right: 0px; position: fixed; background-color: rgba(255, 255, 255, 0.7); overflow: hidden; outline: none 0px; z-index: 999; text-align: center; margin-left: -15px; margin-right: -15px;
