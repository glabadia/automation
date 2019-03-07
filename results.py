from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils import printList, destruct_info, destruct_info_upd, createDirectory
from time import sleep
from search import calibrateSearch
EXPAND_WAIT_TIME: int = 50
WAIT_TIME: int = 25
SLEEP_TIME: int = 10


def expandVehicleInfo(driver):

    expandPath = "//div[@id = 'home']/div[@class = 'search-results hide-in-toggle']/div[@class = 'panel panel-default search-heading']/div[@class = 'panel-heading search-result-heading']/div[@class = 'row header-content']/div[@class = 'col-lg-7 col-md-7 col-xs-7 photo-details-heading']/div[@class = 'col-lg-5 col-md-5 col-xs-5 photo-heading']/div[@class='checkbox-all-vehicle']/div[@class='visible-md visible-lg right-expand-all']"
    # /a[@class='expand-all-view']"
    # sleep for 10 seconds to allow the browser to populate data, and fill the div with desired results.
    sleep(10)

    # Purchase Report ATNZ
    # ATNZ Sales Report
    # ATNZ Sales Performance Report
    expandButton = driver.find_element_by_xpath(expandPath)

    sleep(3)  # Allow for the loader image to fade out in the browser
    expandButton.click()


def expandVehicleInfoIdirect(driver):
    # sleep for 7-15 seconds to allow the browser to populate data, and fill the div with desired results.
    # sleep(20)
    expandPath = "//div[@class='visible-md visible-lg right-expand-all']"
    expandCSS = "i.glyphicon.text-left.expand-icon.glyphicon-plus-sign"
    loaderOnInvisible = "//div[@id='loader'][contains(@style,'display: none;')]"
    print("Waiting to populate data..")

    # i.glyphicon.text-left.expand-icon.glyphicon-plus-sign::before
    # expandButton = driver.find_element_by_xpath(expandPath)
    # sleep(SLEEP_TIME)  # Allow for the loader image to fade out in the browser
    isLoaderPresent = False
    try:
        isLoaderPresent = WebDriverWait(driver, SLEEP_TIME).until(
            EC.presence_of_element_located((By.XPATH, loaderOnInvisible)))
    except Exception as e:
        print(f"Error, {e}")

    if isLoaderPresent:
        print("Loader gone!")
        try:
            # expandButton = WebDriverWait(driver, EXPAND_WAIT_TIME).until(
            #     EC.presence_of_element_located((By.XPATH, expandPath)))

            # if isPlusExist:
            #     print("Expand button still exist!")
            isPlusExist = True
            while isPlusExist:
                expandButton = driver.find_element_by_xpath(expandPath)
                expandButton.click()
                isPlusExist = driver.find_elements_by_css_selector(expandCSS)

        except Exception as e:
            print(f"Error, {e}")
    else:
        print("Sorry. Page is still loading..")
    # try:
    #     expandButton = WebDriverWait(driver, WAIT_TIME).until(
    #         EC.presence_of_element_located((By.XPATH, expandPath)))
    #     sleep(WAIT_TIME)  # Allow for the loader image to fade out in the browser

    #     expandButton.click()
    # except TimeoutException as te:
    #     print(f"Timeout Error {te}")
    #     pass
    # except Exception as e:
    #     print(f"Error: {e}")
    #     pass


def retrieveSearchResultsOnePage(driver):
    #   vehicleListPath = 'div[id=^'vehicle']'
    # vehiclePath = "div[id=^'vehicle']"
    # vehiclePath = "//div[starts-with(@id,'vehicle')]"
    #   the info beside the main picture
    vehiclePath = "//div[@class='data-container']"
    vehicleInfoList = driver.find_elements_by_xpath(vehiclePath)
    # printList(vehicleInfoList)
    return vehicleInfoList


def retrieveInfo(driver):
    allVehicles = []
    vehicleInfoPath = "//div[@class='col-lg-12 search-result-container']"
    containerSelectors = driver.find_elements_by_xpath(vehicleInfoPath)
    for container in containerSelectors:
        allVehicles.append(destruct_info(container))

    return allVehicles


def retrieveInfoUpd(driver):
    """
    Retrieves all info in idirect browser
    A.K.A getting the meat...
    """
    # //div[starts-with(@id,'VehicleDetail')]
    allVehicles = []
    vehicleInfoPath = "//div[@class='col-lg-12 search-result-container']"
    containerSelectors = driver.find_elements_by_xpath(vehicleInfoPath)
    for container in containerSelectors:
        allVehicles.append(destruct_info_upd(container))

    return allVehicles


def retrieveInfoTest(driver):
    """
    Tests the 100th element of the div
    """
    #
    vehicleInfoPath = "//div[starts-with(@id,'VehicleDetail')]"
    containerSelectors = driver.find_elements_by_xpath(vehicleInfoPath)

    return containerSelectors[-1].text


def vehicleDetailInfo(driver, vehiclesList):
    # info
    # //div[@class='col-lg-12 search-result-container']
    # info_onlyleftside
    # //div[@class='search-result-panel auction-detail-panel']
    # info_rightside
    # //div[@class='search-result-panel hide-in-mobile pricing-container-panel']
    # images
    # //div[contains(@class,'search-result-additional-panel additional-detail-panel')]
    vehicleDetailList = ""
    for vehicle in vehiclesList:
        vehicleDetailsPath = "div.data-container"
        vehicleDetailsPane = driver.find_element_by_css_selector(
            vehicleDetailsPath)
        vehicleDetailList = vehicleDetailsPane.text.split('\\n')

    #   span#IBCNum123456789.pull-right
    #   chassisNumPath = "//span[starts-with(@id,'IBCNum')]"
    #   year = "//span[starts-with(@id,'year')]"
    #   makeModelPath = "//span[starts-with(@id,'cInfo')]"
    #   chassisPrefix  = "//span[starts-wth(@id,'chassis')]"
    #   chassisPrefix  = "//span[starts-wth(@id,'chassis')]"

    return vehicleDetailList


def fetchIBCNum(driver):
    ibcNumSelector = "//span[starts-with(@id,'IBCNum')]"
    ibcNumbers = driver.find_elements_by_xpath(ibcNumSelector)
    # yorImagePath = "//span[@class='text-left width-45per yor-in-thumbnail']//img"
    return ibcNumbers


def fetchIBCandYOR(driver):
    ibcNum_and_yor = []
    containerSelectorPath = "//div[@class='col-lg-12 search-result-container']"
    ibcNumSelectorPath = ".//span[starts-with(@id,'IBCNum')]"
    yorImagePath = ".//span[@class='text-left width-45per yor-in-thumbnail']//img"
    yorText = ".//span[@class='text-left width-45per yor-in-thumbnail']"
    containerSelectors = driver.find_elements_by_xpath(containerSelectorPath)

    for container in containerSelectors:
        ibcnum = container.find_element_by_xpath(ibcNumSelectorPath)
        yor = "None"
        try:
            yor = container.find_element_by_xpath(
                yorImagePath).get_attribute('src')
        except:
            yor = container.find_element_by_xpath(yorText).text
            # print(f"There is no YOR for ibcnum {ibcnum.text}")
        print([ibcnum.text, yor])
        ibcNum_and_yor.append([ibcnum.text, yor])

    return ibcNum_and_yor


def vehicleDetailPix():
    # 	vehicleDetailPath = "//div[starts-with(@id,'VehicleDetail)]"
    #		auctionDetail = 'div.search-result-panel auction-detail-panel'
    #	vehicleDetailsList = driver.find_elements_by_xpath(vehicleDetailPath)
    #	for every vehicleDetail => div.search-result-additional-panel additional-detail-panel
        #		auctionsheet = "//div[starts-with(@id,'aucSheetContainer')]"
    #		div.additional-image-container hide-in-mobile
    #		additionalPix = "//div[starts-with(@id,'imageFront')]"
    #		additionalPix = "//div[starts-with(@id,'imageBack-container')]"
    #		additionalPix = "//div[starts-with(@id,'interior-image-desk')]"
    #   //div[@id='VehicleDetail110220143']
    #   //div[starts-with(@id,'VehicleDetail')] --> container
    #   //img[starts-with(@id,'imageBack')]
    #   //img[starts-with(@id,'interior-image-desk')]
    #   //img[starts-with(@id,'auction-sheet-image')]
    return


def yorImages():
    #   Japanese characters
    #   /[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]/
    # yorImagePath = "//span[@class='text-left width-45per yor-in-thumbnail']//img"
    return
