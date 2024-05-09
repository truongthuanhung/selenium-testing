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

    def create_event(self, title, duration):
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        time.sleep(3)
        self.driver.find_element(By.XPATH, "//button[contains(.,\'New event\')]").click()
        time.sleep(3)
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(title)
        self.driver.find_element(By.XPATH, "//a[contains(.,\'Show more...\')]").click()
        self.driver.find_element(By.ID, "id_duration_2").click()
        self.driver.find_element(By.ID, "id_timedurationminutes").click()
        self.driver.find_element(By.ID, "id_timedurationminutes").send_keys(duration)
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Save\')]").click()
        time.sleep(5)
    
    def verify_title_error(self, testid):
        self.driver.find_element(By.ID, "id_error_name").click()
        if self.driver.find_element(By.ID, "id_error_name").text == "- Required":
            print(f"Textcase {testid} passed")
        else:
            print(f"Textcase {testid} failed")
        self.driver.find_element(By.XPATH, "//div[5]/div[2]/div/div/div/button/span").click()
    
    def verify_duration_error(self, testid):
        self.driver.find_element(By.ID, "fgroup_id_error_durationgroup").click()
        if self.driver.find_element(By.ID, "fgroup_id_error_durationgroup").text == "The duration in minutes you have entered is invalid. Please enter the duration in minutes greater than 0 or select no duration.":
            print(f"Textcase {testid} passed")
        else:
            print(f"Textcase {testid} failed")
        self.driver.find_element(By.XPATH, "//div[5]/div[2]/div/div/div/button/span").click()
    
    def verify_success(self, testid, title):
        self.driver.find_element(By.XPATH, f"//span[contains(.,\'{title}\')]").click()
        time.sleep(5)
        if self.driver.find_element(By.XPATH, f"//span[contains(.,\'{title}\')]").text == title:
            print(f"Textcase {testid} passed")
        else:
            print(f"Textcase {testid} failed")
        time.sleep(10)
        delete_button = self.driver.find_element(By.XPATH, "//div[2]/div/div/div[3]/button[contains(.,\'Delete\')]")
        actions = ActionChains(self.driver)
        actions.move_to_element(delete_button).perform()
        delete_button.click()
        time.sleep(5)
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Delete event\')]").click()
        time.sleep(3)
    
    def testcase(self, testid, title, duration):
        self.create_event(title, duration)
        if title == "":
            self.verify_title_error(testid)
        elif duration < 1: #vi moodle cat di phan thap phan
            self.verify_duration_error(testid)
        else:
            self.verify_success(testid, title)
        time.sleep(3)
   
    def run_test(self):
        self.log_in()
        self.testcase('TC-052-001', "Học từ vựng", 1)
        self.testcase('TC-052-002', "Học từ vựng", 0)
        self.testcase('TC-052-003', "", 1)
        self.testcase('TC-052-004', "", 0)
        self.log_out()
        
# Main
test = MoodleTest(USERNAME, PASSWORD)
test.run_test()
test.driver.quit()