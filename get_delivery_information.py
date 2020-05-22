from selenium.webdriver.common.by import By
from selenium import webdriver as wd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from time import sleep, time
from pyautogui_utils import find_image_screenshot
import os
import get_credentials_util
import argparse
import email_purchase_order_finder

global driver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#
# cap = DesiredCapabilities().FIREFOX
# cap["marionette"] = False

def main():
    username, password = get_credentials_util.get_credentials("credentials_myaccess_email.json")

    parser = argparse.ArgumentParser()
    parser.add_argument('-reqtsv', '--allRequsitions_path', help='path to allRequisitions.tsv from bearbuy_scrape',
                        required=True)
    args = parser.parse_args()

    automation_dir = "/Users/liam_msg/Documents/automation"

    purchase_orders = set()
    with open(args.allRequsitions_path, 'r') as allRequisitions:
        for i, line in enumerate(allRequisitions.readlines()):
            if i == 0:
                continue
            purchase_orders.add(line.rstrip().split('\t')[-1])
    print(purchase_orders)

    if not os.path.exists(os.path.join(automation_dir,'logistics_shipping')):
        os.mkdir(os.path.join(automation_dir,'logistics_shipping'))

    driver = wd.Firefox(executable_path='/usr/local/bin/geckodriver')

    driver.get("https://scmlogistics.ucsf.edu/Reporting/Viewer.aspx")

    action = ActionChains(driver)
    print(action)
    # driver.action.click(el).pause(keyboard).pause(keyboard).pause(keyboard).send_keys('keys').perform

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

    # new website (logistics helper wtf bureaucracy site)
    #
    home_button_xpath = "//a[contains(text(),'Home')]"
    WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_xpath(home_button_xpath))
    home_button = driver.find_element_by_xpath(home_button_xpath).click()
    # sleep(0.2)
    # home_button = driver.find_element_by_xpath(home_button_xpath).click()
    # sleep(0.2)
    # home_button = driver.find_element_by_xpath(home_button_xpath).click()
    driver.get("https://scmlogistics.ucsf.edu/Reporting/Viewer.aspx?v=bbponum")


    for purchase_order in purchase_orders:
        sleep(1)
        bbpo_textbox_xpath = "//input[@id='ctl00_mstr_rptVwr_ctl08_ctl03_txtValue']"
        WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_xpath(bbpo_textbox_xpath))

        element = WebDriverWait(driver, 10).until(
            element_to_be_clickable((By.XPATH, bbpo_textbox_xpath))
        )
        bbpo_textbox = driver.find_element_by_xpath(bbpo_textbox_xpath)
        bbpo_textbox.clear()
        bbpo_textbox.send_keys(purchase_order)

        view_report_xpath = "//input[@id='ctl00_mstr_rptVwr_ctl08_ctl00']"
        view_report = driver.find_element_by_xpath(view_report_xpath).click()
        sleep(3)


        with open(os.path.join(automation_dir,'logistics_shipping',purchase_order+".html"), "w") as f:
            f.write(driver.page_source)
            print("saved",purchase_order+".html")

    driver.quit()

if __name__ == '__main__':
    main()