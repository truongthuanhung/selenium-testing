from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
USERNAME = 'student'
PASSWORD = 'moodle'

class MoodleTest():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        
    def log_in(self):
        self.driver.get('https://qa.moodledemo.net/')
        self.driver.maximize_window()
        self.driver.find_element(By.LINK_TEXT, 'Log in').click()
        self.driver.find_element(By.NAME, 'username').send_keys(self.username)
        self.driver.find_element(By.NAME, 'password').send_keys(self.password + Keys.ENTER)
        time.sleep(5)
    
    def log_out(self):
        self.driver.find_element(By.ID, 'user-menu-toggle').click()
        self.driver.find_element(By.LINK_TEXT, 'Log out').click()

    def enter_export_calendar(self):
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        time.sleep(5)
        self.driver.find_element(By.XPATH, "//a[contains(.,\'Import or export calendars\')]").click()
        time.sleep(3)
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Export calendar\')]").click()
        time.sleep(3)
    
    def verify_success(self):
        value = self.driver.find_element(By.ID, "calendarexporturl").get_attribute("value")
        if not value == "https://qa.moodledemo.net/calendar/export_execute.php?userid=4&authtoken=3a825938ad829a496e27567fc51ef1b6839f4c6c&preset_what=all&preset_time=weeknow":
            return False
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Copy URL\')]").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".toast-message").click()
        if not self.driver.find_element(By.CSS_SELECTOR, ".toast-message").text == "Calendar URL copied to clipboard":
            return False
        return True

    def verify_required(self, option):
        if option == "noevents" or option == "noboth":
            self.driver.find_element(By.ID, "fgroup_id_error_events").click()
            if not self.driver.find_element(By.ID, "fgroup_id_error_events").text == "Required":
                return False
        if option == "noperiod" or option == "noboth":
            self.driver.find_element(By.ID, "fgroup_id_error_period").click()
            if not self.driver.find_element(By.ID, "fgroup_id_error_period").text == "Required":
                return False
        return True
            
    def print_result(self, testid, result):
        if result:
            print(f"Textcase {testid} passed")
        else:
            print(f"Textcase {testid} failed")
   
    def testcase1(self, testid):
        self.enter_export_calendar()
        self.driver.find_element(By.ID, "id_events_exportevents_all").click()
        self.driver.find_element(By.ID, "id_period_timeperiod_weeknow").click()
        self.driver.find_element(By.ID, "id_generateurl").click()
        time.sleep(3)
        self.print_result(testid, self.verify_success())
    
    def testcase2(self, testid):
        self.enter_export_calendar()
        self.driver.find_element(By.ID, "id_events_exportevents_all").click()
        self.driver.find_element(By.ID, "id_generateurl").click()
        self.print_result(testid, self.verify_required("noperiod"))
        
    def testcase3(self, testid):
        self.enter_export_calendar()
        self.driver.find_element(By.ID, "id_period_timeperiod_weeknow").click()
        self.driver.find_element(By.ID, "id_generateurl").click()
        self.print_result(testid, self.verify_required("noevents"))
        
    def testcase3(self, testid):
        self.enter_export_calendar()
        self.driver.find_element(By.ID, "id_generateurl").click()
        self.print_result(testid, self.verify_required("noboth"))
   
    def run_test(self):
        self.log_in()
        self.testcase1('TC-062-001')
        self.testcase2('TC-062-002')
        self.testcase2('TC-062-003')
        self.testcase2('TC-062-004')
        self.log_out()
        
# Main
test = MoodleTest(USERNAME, PASSWORD)
test.run_test()
test.driver.quit()