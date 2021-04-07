import glob
import argparse
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver as wd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
from time import sleep
import os
import get_credentials_util
import re


def find_element_regex(PARTIAL_LINK_TEXT,regex):
    # https://stackoverflow.com/questions/34315533/can-i-find-an-element-using-regex-with-python-and-selenium
    pattern = re.compile(regex)

    elements = driver.find_elements(By.PARTIAL_LINK_TEXT, PARTIAL_LINK_TEXT)
    for element in elements:
        match = pattern.match(element.text)
        if match:
            return element

def create_directories():
    if not os.path.exists("bearbuy_requisitions"):
        os.mkdir("bearbuy_requisitions")


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


def check_if_completed(hard_run=False):
    if hard_run:
        print("Downloading requisitions")
        return True
    elif len(glob.glob("bearbuy_requisitions/*")) > 1:
        run_this_script = input('Requisitions detected. Download requisitions? y/n')
        if run_this_script == "y":
            return True
        else:
            return False
    else:
        print("Downloading requisitions")
        return True


def main(args):
    global driver
    create_directories()
    hard_run = args.hard_run
    run_script = check_if_completed(hard_run)

    if run_script:
        username, password = get_credentials_util.get_credentials("credentials_myaccess_email.json")

        try:
            driver = wd.Firefox(executable_path='/usr/local/bin/geckodriver')
        except:
            print(
                "You must install geckodriver for Firefox. https://github.com/mozilla/geckodriver/releases. put it in /usr/local/bin/")

        print("going to BearBuy.")
        driver.get("http://solutions.sciquest.com/apps/Router/SAMLAuth/UCSF")

        action = ActionChains(driver)
        print(action)
        # driver.action.click(el).pause(keyboard).pause(keyboard).pause(keyboard).send_keys('keys').perform

        print("logging in")
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
        wait_until_found(driver, orders_button_xpath)
        driver.get("https://solutions.sciquest.com/apps/Router/RequisitionElasticSearch")

        change_to_all_date = '//*[@id="ESSearchInput_SubmittedDate"]'
        WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_xpath(change_to_all_date))
        driver.find_element_by_xpath(change_to_all_date).click()

        select_all_date_option = '//*[@id="ActiveForm"]/div/div/div[2]/div[1]/div[1]/div[1]/ul/li[1]/div/div/div/div[1]/ul[1]/li[1]/table/tbody/tr/td/div/label/span'
        driver.find_element_by_xpath(select_all_date_option).click()

        apply_button = '//*[@id="BUTTON_APPLY"]'
        driver.find_element_by_xpath(apply_button).click()

        # sort_req_number = '/html/body/div[1]/div[5]/div[2]/div/form/div/div/div/div[2]/div[2]/div/div/table/thead/tr/th[2]/div[2]/a'
        # driver.find_element_by_xpath(sort_req_number).click()
        loading = '/html/body/div[30]/div/div'
        element = WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, loading))
        )

        first_req = '/html/body/div[1]/div[5]/div[2]/div/form/div/div/div[2]/div[2]/div/div/table/tbody/tr[1]/td[2]/a'
        
        reqs = find_element_regex('1',r'^(\d{9})$')
        # driver.find_element_by_xpath(first_req_xpth).click()\

        reqs.click()
        # reqs[0].click()

        sleep(2)
        next_arrow_xpath = "//button[@id='PhxGenId_2']"
        wait_until_found(driver, next_arrow_xpath)
        next_arrow = driver.find_element_by_xpath(next_arrow_xpath)
        numreqs = 0

        print('downloading requisitions...')
        while isClickable(next_arrow):
            sleep(0.5)
            wait_until_found(driver, next_arrow_xpath)
            next_arrow = driver.find_element_by_xpath(next_arrow_xpath)
            if next_arrow:
                if 'disabled' in str(next_arrow.get_attribute('outerHTML')):
                    with open(os.path.join('bearbuy_requisitions', driver.title + ".html"), "w") as f:
                        f.write(driver.page_source)

                    numreqs += 1
                    print('downloaded', driver.title)

                    break

            with open(os.path.join('bearbuy_requisitions', driver.title + ".html"), "w") as f:
                f.write(driver.page_source)
            next_arrow.click()
            numreqs += 1
        print("reqs found =", numreqs)
        driver.quit()


if __name__ == '__main__':
    main()
