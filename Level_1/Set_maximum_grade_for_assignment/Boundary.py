from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
USERNAME = 'teacher'
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

    def set_max_grade(self, max_grade):
        self.driver.find_element(By.LINK_TEXT, "My courses").click()
        time.sleep(3)
        self.driver.find_element(By.LINK_TEXT, "Activity examples").click()
        self.driver.find_element(By.LINK_TEXT, "Assignment with marking guide").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Settings").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Grade").click()
        time.sleep(1)
        maxgrade_element = self.driver.find_element(By.ID, "id_grade_modgrade_point")
        actions = ActionChains(self.driver)
        actions.double_click(maxgrade_element).perform()
        maxgrade_element.send_keys(max_grade)
        self.driver.find_element(By.ID, "id_submitbutton").click()
        time.sleep(5)
    
    def verify_error(self, testid):
        self.driver.find_element(By.ID, "fgroup_id_error_grade").click()
        if self.driver.find_element(By.ID, "fgroup_id_error_grade").text == "Invalid grade value. This must be an integer between 1 and 101":
            print(f"Textcase {testid} passed")
        else:
            print(f"Textcase {testid} failed")
    
    def verify_success(self, testid):
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > h2").click()
        if self.driver.find_element(By.XPATH, "//h2[contains(.,\'Recalculating grades\')]").text == "Recalculating grades":
            print(f"Textcase {testid} passed")
        else:
            print(f"Textcase {testid} failed")
    
    def testcase(self, testid, max_grade):
        self.set_max_grade(max_grade)
        if max_grade < 1 or max_grade > 100:
            self.verify_error(testid)
        else:
            self.verify_success(testid)
        time.sleep(3)
   
    def run_test(self):
        self.log_in()
        self.testcase('TC-111-001', 0)
        self.testcase('TC-111-002', 1)
        self.testcase('TC-111-003', 2)
        self.testcase('TC-111-004', 99)
        self.testcase('TC-111-005', 100)
        self.testcase('TC-111-006', 101)
        self.log_out()
        
# Main
test = MoodleTest(USERNAME, PASSWORD)
test.run_test()
test.driver.quit()