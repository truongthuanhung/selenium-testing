from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import sys
USERNAME = 'teacher'
PASSWORD = 'moodle'
COURSE_NAME = 'Activity examples'
ASS_NAME = 'Online text assignment'
class MoodleTest():
    def __init__(self, username, password, df):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        self.df = df
        
    def log_in(self):
        self.driver.get('https://qa.moodledemo.net/')
        self.driver.maximize_window()
        # click log in button
        log_in_button = self.driver.find_element(By.LINK_TEXT, 'Log in')
        log_in_button.click()
        # get input element
        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')
        # fill in the input and submit
        username_input.send_keys(self.username)
        password_input.send_keys(self.password + Keys.ENTER)
        time.sleep(5)
    
    def log_out(self):
        menu_toggle_element = self.driver.find_element(By.ID, 'user-menu-toggle')
        menu_toggle_element.click()
        log_out_button = self.driver.find_element(By.LINK_TEXT, 'Log out')
        log_out_button.click()
        time.sleep(5)

    def enter_course(self, course_name):
        course_element = self.driver.find_element(By.LINK_TEXT, course_name)
        course_element.click()
        time.sleep(5)
        self.handle_close_modal()
    
    def handle_close_modal(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, '.modal-footer .btn-secondary').click()
            time.sleep(2)
        except NoSuchElementException:
            time.sleep(5)
    def enter_assignment(self, ass_name):
        course_element = self.driver.find_element(By.LINK_TEXT, ass_name)
        course_element.click()
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, "Grade").click()
        time.sleep(10)
        self.driver.find_element(By.CSS_SELECTOR, '.confirmation-buttons .btn').click()

        for i in range(0, len(self.df)):
            grade_input = self.driver.find_element(By.NAME, 'grade')
            grade_input.clear()
            grade_input.send_keys(str(self.df.iloc[i,0]))
            self.driver.find_element(By.NAME, 'savechanges').click()
            time.sleep(5)
            self.driver.find_element(By.CSS_SELECTOR, '.confirmation-buttons .btn').click()
            current_grade = self.driver.find_element(By.CSS_SELECTOR, '.currentgrade a').text
            expected = self.df.iloc[i,1]
            if expected == 'Grade must be greater than or equal to zero.' or expected == 'Grade must be less than or equal to 100.':
                text = self.driver.find_element(By.ID, 'id_error_grade').text
                if (text ==  expected):
                    print(f"Text {i+1} runs successfully")
                else:
                    print(f"Text {i+1} failed: '{float(current_grade)}' does not match expected value '{float(expected)}'")
            else:
                if (float(current_grade) ==  float(expected)):
                    print(f"Text {i+1} runs successfully")
                else:
                    print(f"Text {i+1} failed: '{float(current_grade)}' does not match expected value '{float(expected)}'")
    
    def run_test(self):
        self.log_in()
        self.enter_course(COURSE_NAME)

        self.enter_assignment(ASS_NAME)
        self.driver.get('https://qa.moodledemo.net/')
        time.sleep(3)
        self.log_out()
        
        

# Main
test = MoodleTest(USERNAME, PASSWORD, pd.read_excel(sys.argv[1]))

test.run_test()

test.driver.quit()