from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from getImageSize import getImageFileSize
from jpChecker import find_japanese_char as catchJap

SLEEP_TIME: int = 10

errorList = {"yearMakeModel": "unknown", "chassisPrefix": "unknown",
             "transColorFuel": "| --", "equipment": "| --", "yorText": "none", "yorImage": 6385}  # 6385 #2151 for no foto
errorReturnValue = {"jap_char": "japanese characters", "yearMakeModel": "unknown year/make/model", "chassisPrefix": "unknown chassis prefix",
                    "transColorFuel": "no transmission/color/fuel type", "equipment": "no equipment", "yorText": "missing YOR", "yorImage": "no YOR Image"}
errorCounter = {"jap_char": [], "yearMakeModel": [], "chassisPrefix": [],
                "transColorFuel": [], "equipment": [], "yorText": [], "yorImage": []}


def printList(list):
    count = 1
    for item in list:
        print("Element: ", count, ":")
        print(item.text, "class name = ", item.get_attribute("class"))
        print("--------------------------------------------------------------------------------------")
        count += 1


def printDict(dict):
    count = 1
    for item in dict:
        print("Element: ", count, ":")
        print(item)
        print("--------------------------------------------------------------------------------------")
        count += 1


def destructure(vehicles, ibcNums):
    # make a list of dictionaries
    ibcVehicles = []

    for ibcNum in ibcNums:
        ibcNumDict = {}
        ibcNumDict["ibcnum"] = ibcNum.text
        ibcVehicles.append(ibcNumDict)

    for i in range(len(vehicles)):
        print(vehicles[i])
        vehicle = vehicles[i].text.splitlines()
        ibcVehicles[i]["yearMakeModel"] = vehicle[0]
        ibcVehicles[i]["chassisPrefix"] = vehicle[1].split()[-1]
        ibcVehicles[i]["transColorFuel"] = vehicle[2]
        ibcVehicles[i]["equipment"] = vehicle[6]
        ibcVehicles[i]["yor"] = vehicle[9]

    return ibcVehicles

# exec(open(r"C:\Users\glabadia\Desktop\VS\scripts\dataCollectionFiles\init.py").read())


def destruct_info(containerPath):
    ibcNumPath = ".//span[starts-with(@id,'IBCNum')]"
    yearMakeModelPath = ".//span[@class='text-bold pull-left width-55per']"
    chassisPrefixPath = ".//a[@class='text-red pull-left width-70per chassis-amkenya chassis-wd']"
    twoElementPath = ".//span[@class='pull-left width-55per']"
    equipPath = ".//div[@class='pull-left width-55per']/span[1]"
    # transColorFuel = twoElement[0]
    # ccMileage = twoElement[1]
    yorImagePath = ".//span[@class='text-left width-45per yor-in-thumbnail']//img"
    yorTextPath = ".//span[@class='text-left width-45per yor-in-thumbnail']"

    vehicleInfo = {}

    vehicleInfo["ibcnum"] = containerPath.find_element_by_xpath(
        ibcNumPath).text
    vehicleInfo["yearMakeModel"] = containerPath.find_element_by_xpath(
        yearMakeModelPath).text
    vehicleInfo["chassisPrefix"] = containerPath.find_element_by_xpath(
        chassisPrefixPath).text.split()[-1]
    vehicleInfo["transColorFuel"] = containerPath.find_elements_by_xpath(twoElementPath)[
        0].text
    vehicleInfo["equipment"] = containerPath.find_element_by_xpath(
        equipPath).text

    yorTextImage = "None"

    try:
        # yorTextImage = containerPath.find_element_by_xpath(
        #     yorImagePath).get_attribute('src')
        print("destruct image size begin..")
        yorTextImage = getImageFileSize(containerPath.find_element_by_xpath(
            yorImagePath).get_attribute('src'))

    except:
        yorTextImage = containerPath.find_element_by_xpath(yorTextPath).text

    vehicleInfo["yor"] = yorTextImage

    return vehicleInfo


def getAuctionHouse(dc_driver):
    auctionHousePath = "//span[starts-with(@id,'IBCNum')]"
    try:
        auctionHouseContainer = WebDriverWait(dc_driver, SLEEP_TIME).until(
            EC.presence_of_element_located((By.XPATH, auctionHousePath)))
    except Exception as e:
        print(f"Error: {e}")

    # auctionHouseContainer = dc_driver.find_element_by_xpath(auctionHousePath)
    return auctionHouseContainer.text[:-10]


def destruct_info_upd(containerPath):
    ibcNumPath = ".//span[starts-with(@id,'IBCNum')]"
    yearMakeModelPath = ".//span[@class='text-bold pull-left width-55per']"
    chassisPrefixPath = ".//a[@class='text-red pull-left width-70per chassis-amkenya chassis-wd']"
    shuppinPath = ".//span[@id='shuppin']"
    twoElementPath = ".//span[@class='pull-left width-55per']"
    equipPath = ".//div[@class='pull-left width-55per']/span[1]"
    yorImagePath = ".//span[@class='text-left width-45per yor-in-thumbnail']//img"
    yorTextPath = ".//span[@class='text-left width-45per yor-in-thumbnail']"

    vehicleInfo = {}

    vehicleInfo["ibcnum"] = containerPath.find_element_by_xpath(
        ibcNumPath).text
    vehicleInfo["shuppin"] = containerPath.find_element_by_xpath(
        shuppinPath).text
    vehicleInfo["yearMakeModel"] = containerPath.find_element_by_xpath(
        yearMakeModelPath).text
    vehicleInfo["chassisPrefix"] = containerPath.find_element_by_xpath(
        chassisPrefixPath).text.split()[-1]
    vehicleInfo["transColorFuel"] = containerPath.find_elements_by_xpath(twoElementPath)[
        0].text
    vehicleInfo["equipment"] = containerPath.find_element_by_xpath(
        equipPath).text

    yorTextImage = "None"

    try:
        # yorTextImage = getImageFileSize(containerPath.find_element_by_xpath(
        #     yorImagePath).get_attribute('src'))
        yorTextImage = containerPath.find_element_by_xpath(
            yorImagePath).get_attribute('src')
        # print("destruct image path begin..")
        # yorTextImage = getImageFileSize(containerPath.find_element_by_xpath(
        #     yorImagePath).get_attribute('src'))
        vehicleInfo["yorText"] = ""
        vehicleInfo["yorImage"] = yorTextImage

    except:
        yorTextImage = containerPath.find_element_by_xpath(yorTextPath).text
        vehicleInfo["yorText"] = yorTextImage.split()[-1]
        vehicleInfo["yorImage"] = 0

    return vehicleInfo


def errorChecking(vehiclesList):
    ibcnumKey = "ibcnum"
    lookout = {"yearMakeModel": "unknown", "chassisPrefix": "unknown",
               "transColorFuel": "| --", "equipment": "| --", "yor": "none", "yor": 6385}

    vehicleErrors = []
    for vehicle in vehiclesList:
        for key in lookout:
            errors = []
            if type(lookout[key]) is str and type(vehicle[key]) is str:
                if lookout[key].lower() in vehicle[key].lower():
                    errors.append(vehicle[ibcnumKey])
                    errors.append(f"This vehicle has no {key}")
            else:
                if key == "yor" and type(vehicle[key]) is int:
                    if lookout[key] == vehicle[key]:
                        errors.append(vehicle[ibcnumKey])
                        errors.append(f"This vehicle has no {key}")
            if errors:
                vehicleErrors.append(errors)

    return vehicleErrors


def errorCheckUpd(vehiclesList, lookout=errorList, reportLog=errorReturnValue, count=errorCounter):
    ibcnumKey = "ibcnum"
    vehicleErrors = []
    for vehicle in vehiclesList:
        errors = []
        for key in lookout:
            if key == 'yearMakeModel':
                if catchJap(vehicle[key]):
                    errors.append(f"This vehicle has {reportLog['jap_char']}")
                    count[key].append(vehicle[ibcnumKey])
            if key == 'yorImage':
                # if lookout[key] == vehicle[key]:
                if lookout[key] == getImageFileSize(vehicle[key]):
                    count[key].append(vehicle[ibcnumKey])
                    errors.append(f"This vehicle has {reportLog[key]}")
            else:
                if lookout[key].lower() in vehicle[key].lower():
                    count[key].append(vehicle[ibcnumKey])
                    errors.append(f"This vehicle has {reportLog[key]}")

        if errors:
            vehicleErrors.append([vehicle[ibcnumKey]] + errors)
    # vehiclesList[-1]["ibcnum"][:-10]

    return vehicleErrors, count  # , vehiclesList[-1]["ibcnum"][:-10]


def dictErrors(error_list):
    displayOutput = {}

    for key in error_list:  # error_list.items() => returns a tuple, not a key, even if you have a "for key in error_list.items()"
        if len(error_list[key]) == 0:
            displayOutput[errorReturnValue[key]] = "No issues"
        else:
            displayOutput[errorReturnValue[key]] = error_list[key]

    return displayOutput


def printErrors(error_list):
    for key in error_list:
        print(key.title())
        # print(error_list[key])
        value = error_list[key]
        if type(value) is list:
            for content in value:
                print(content)
        else:
            print(value)
        print("-------------------------------------------------------------------------------")


def getAuctionHouseTest(text=""):
    text = "Honda Tokyo-110175756"
    print(text[:-10])


def getTimeStamp():
    from datetime import datetime as dt
    return dt.now().strftime("%A, %d. %B %Y %I:%M%p")


def printToFile(duration, workingDirectory, fileName="testFile", contentList=""):
    import os
    os.chdir(workingDirectory)
    with open(f"{fileName}.txt", "w") as writer:
        writer.write(
            "#############################################################\n")
        writer.write(f"{fileName.upper()} Errors: \n")
        writer.write("\n")
        # writer.write(f"Data Collection lasted for {convert_time(duration):.1f} seconds.\n")
        writer.write(
            f"Data Collection lasted for {convert_time(duration[0])} seconds.\n")
        writer.write(
            f"Error checking lasted for {convert_time(duration[1])} seconds.\n")
        writer.write(f"Finished checking on {getTimeStamp()} \n")
        writer.write(
            "#############################################################\n")
        for content in contentList:
            writer.write(f"{content.title()}:\n")
            value = contentList[content]
            if type(value) is list:
                for entry in value:
                    writer.write(f"{entry[-9:]},\n")
            else:
                writer.write(f"{value[-9:]}\n")
            writer.write(
                "-------------------------------------------------------------\n")


def createDirectory():
    """
    create directory for data collection
        if directory already exists, return false
        else, create directory in strftime('%Y_%b_%d') format
        or create nesting directory : year/Month/day, e.g. 2019/March/5
    """
    import os
    from datetime import datetime as dt

    timeStampList = ["%Y", "%B", "%d"]
    for time in timeStampList:
        current_directory = os.getcwd()
        newFolder = dt.now().strftime(time)
        newDirectory = os.path.join(current_directory, newFolder)
        if not os.path.exists(newDirectory):
            os.makedirs(newDirectory)
        else:
            print(f"Folder '{newDirectory}' already exists!")
        try:
            # Change the current working Directory
            os.chdir(newFolder)
            # print("Directory changed")
        except OSError:
            print("Can't change the Current Working Directory")

    return os.getcwd()


def convert_time(time_sec):
    NUM_SECONDS = 60
    return_val = ""
    raw_time = time_sec // NUM_SECONDS
    remain_time = time_sec % NUM_SECONDS
    if raw_time > 0:
        return_val += f"{int(raw_time)} "
        if raw_time == 1:
            return_val += "minute "
        else:
            return_val += "minutes "
        return f"{return_val}and {remain_time:.1f}"
    return f"{remain_time:.1f}"
