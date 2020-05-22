from selenium import webdriver as wd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
from time import sleep
import os
import get_credentials_util


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
driver.get("https://solutions.sciquest.com/apps/Router/MyRequisitionsSearch")

change_to_all_date = "//select[@id='DateRangeErrorContext']"
WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_xpath(change_to_all_date))
driver.find_element_by_xpath(change_to_all_date).click()

select_all_date_option = "//option[contains(.,'All Dates')]"
driver.find_element_by_xpath(select_all_date_option).click()


first_req_css = "body.phoenixBody.withBreadcrumbs:nth-child(2) table.Panel:nth-child(8) td.ForegroundContainer table.SearchResults tbody:nth-child(2) tr:nth-child(1) td.nowrap:nth-child(1) span:nth-child(3) > a:nth-child(1)"
WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_css_selector(first_req_css))
driver.find_element_by_css_selector(first_req_css).click()

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
