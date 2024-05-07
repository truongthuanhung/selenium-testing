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
ASS_NAME = 'Global warming'
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
    def run(self, index):
        grade_input = self.driver.find_element(By.ID, 'id_grade_modgrade_point')
        grade_input.clear()
        grade_input.send_keys(str(self.df.iloc[index,0]))
        self.driver.find_element(By.ID, 'id_submitbutton').click()
        time.sleep(2)
        expected = self.df.iloc[index, 1]
        if (expected == 'OK'):
            try:
                if self.driver.find_element(By.CSS_SELECTOR, '#region-main-box h2'):
                    print(f'Test {index+1} passed!\n')
                    return
            except NoSuchElementException:
                print(f'Test {index+1} failed!\n')
                return
        else:
            try:
                if self.driver.find_element(By.ID, 'fgroup_id_error_grade'):
                    print(f'Test {index+1} passed!\n')
                    return
            except NoSuchElementException:
                print(f'Test {index+1} failed!\n')
                return

    def enter_assignment(self, ass_name):
        course_element = self.driver.find_element(By.XPATH, '//*[@id="module-1013"]/div/div[2]/div[2]/div/div/a')
        course_element.click()
        time.sleep(3)
        self.driver.find_element(By.LINK_TEXT, 'Settings').click()
        time.sleep(3)
        self.driver.find_element(By.ID, 'collapseElement-2').click()
        time.sleep(5)
        
    
    def run_test(self):
        self.log_in()
        for i in range(0, len(self.df)):

            self.enter_course(COURSE_NAME)
            self.enter_assignment(ASS_NAME)
            self.run(i)
            self.driver.get('https://qa.moodledemo.net/my/courses.php')
            time.sleep(8)
        # self.driver.get('https://qa.moodledemo.net/')
        # time.sleep(3)
        self.log_out()
        
        

# Main
test = MoodleTest(USERNAME, PASSWORD, pd.read_excel(sys.argv[1]))

test.run_test()

test.driver.quit()