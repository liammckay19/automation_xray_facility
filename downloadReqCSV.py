import glob
import argparse

from selenium import webdriver as wd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
from time import sleep
import os
import get_credentials_util


def create_directories():
    if not os.path.exists("requisition_csv"):
        os.mkdir("requisition_csv")


def isClickable(webelement):
    from selenium.common.exceptions import ElementClickInterceptedException
    try:
        wait = WebDriverWait(driver, 5)
        wait.until(lambda driver: element_to_be_clickable(webelement))
        return True
    except ElementClickInterceptedException as e:
        print(e)
        return False


def wait_until_found(driver, xpath, time_to_wait=100):
    WebDriverWait(driver, time_to_wait).until(lambda driver: driver.find_element_by_xpath(xpath))


def main():
    global driver
    # To prevent download dialog
    create_directories()
    chromeOptions = wd.ChromeOptions()
    prefs = {"download.default_directory" : os.path.join(os.path.abspath(os.curdir),"requisition_csv")+"/"}
    chromeOptions.add_experimental_option("prefs",prefs)
    username, password = get_credentials_util.get_credentials("credentials_myaccess_email.json")

    # try:
    driver = wd.Chrome(executable_path='/usr/local/bin/chromedriver', options=chromeOptions)
    # except:
    #     print(
    #         "\nAlso,You must install chromedriver for Chrome. https://stackoverflow.com/questions/42478591/python-selenium-chrome-webdriver. put it in /usr/local/bin/")

    print("going to BearBuy.")
    driver.get("http://solutions.sciquest.com/apps/Router/SAMLAuth/UCSF")

    action = ActionChains(driver)
    print(action)
    # driver.action.click(el).pause(keyboard).pause(keyboard).pause(keyboard).send_keys('keys').perform

    print("logging in")  # login to UCSF bearbuy
    username_form_xpath = "//input[@id='ad-username']"
    WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_xpath(username_form_xpath))
    username_form = driver.find_element_by_xpath(username_form_xpath).click()
    action.send_keys(username)
    action.perform()
    action.w3c_actions.key_action.source.clear_actions()
    action.w3c_actions.key_inputs.clear()

    pass_form_xpath = "//input[@id='password']"
    pass_form = driver.find_element_by_xpath(pass_form_xpath).click()

    action.send_keys(password)
    action.perform()
    action.w3c_actions.key_action.source.clear_actions()
    action.w3c_actions.key_inputs.clear()

    login_xpath = "//button[@id='form_submit']"

    login_button = driver.find_element_by_id("form_submit").click()

    orders_button_xpath = "//*[@id='PHX_NAV_ProcurementOrders_Img']"
    wait_until_found(driver, orders_button_xpath)  # wait until loaded
    driver.get("https://solutions.sciquest.com/apps/Router/ManageSearchExports")  # go to manage exports

    # download csv from bearbuy export
    first_export_link = '//*[@id="ExportrequestforRequisition"]/span'
    wait_until_found(driver, first_export_link)
    first_export = driver.find_element_by_xpath(first_export_link).click()
    sleep(1)

    csv = list(sorted(glob.glob("/Users/liam_msg/Downloads/template_requisition_search_RequisitionData_ALL*")))[0]
    print(csv)


    driver.quit()


if __name__ == '__main__':
    main()
