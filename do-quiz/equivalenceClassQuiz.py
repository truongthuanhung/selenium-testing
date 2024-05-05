from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import sys
USERNAME = 'student'
PASSWORD = 'moodle'
COURSE_NAME = 'Votes for Women!'
QUIZ_NAME = 'Suffrage quiz'

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
    
    def test_all(self, idx):
        self.test_data_1(idx)
        self.test_data_2(idx)
        self.test_data_3(idx)
        self.test_data_4(idx)
        self.test_data_5(idx)
        self.submit_quiz()
        time.sleep(5)
        text = self.driver.find_element(By.XPATH, '''//td[contains(text(),'out of 10.00')]''').text
        expected = self.df.iloc[idx,5]
        if (text == expected):
            print(f"Text {idx+1} runs successfully")
        else:
            print(f"Text {idx+1} failed: '{text}' does not match expected value '{expected}'")
    def test_data_1(self, idx):
        if self.df.iloc[idx,0] == 'as a superior to man':
             self.driver.find_element(By.XPATH, '''//p[contains(text(),'as a superior to man')]''').click()
        elif (self.df.iloc[idx,0] == 'as an equal to man'):
            self.driver.find_element(By.XPATH, '''//p[contains(text(),'as an equal to man')]''').click()
        else:
            self.driver.find_element(By.XPATH, '''//p[contains(text(),'as a helpmate for man')]''').click()
    
    def test_data_2(self, idx):
        if self.df.iloc[idx,1] == 'Nancy Astor':
             self.driver.find_element(By.XPATH, '''//p[contains(text(),'Nancy Astor')]''').click()
        elif (self.df.iloc[idx,1] == 'Constance Marciewicz'):
            self.driver.find_element(By.XPATH, '''//p[contains(text(),'Constance Marciewicz')]''').click()
        else:
            self.driver.find_elements(By.XPATH, '''//p[contains(text(),'Emmeline Pankhurst')]''')[0].click()

    def test_data_3(self, idx):
        if self.df.iloc[idx,2] == 'Emmeline Pankhurst':
             self.driver.find_elements(By.XPATH, '''//p[contains(text(),'Emmeline Pankhurst')]''')[1].click()
        elif (self.df.iloc[idx,2] == 'Queen Victoria'):
            self.driver.find_element(By.XPATH, '''//p[contains(text(),'Queen Victoria')]''').click()
        else:
            self.driver.find_element(By.XPATH, '''//p[contains(text(),'an Indian Maharaja')]''').click()

    def test_data_4(self, idx):
        if self.df.iloc[idx,3] == 1918:
             self.driver.find_elements(By.XPATH, '''//p[contains(text(),'1918')]''')[0].click()
        elif (self.df.iloc[idx,3] == 1924):
            self.driver.find_element(By.XPATH, '''//p[contains(text(),'1924')]''').click()
        else:
            self.driver.find_elements(By.XPATH, '''//p[contains(text(),'1928')]''')[0].click()

    def test_data_5(self, idx):
        if self.df.iloc[idx,4] == 1918:
             self.driver.find_elements(By.XPATH, '''//p[contains(text(),'1918')]''')[1].click()
        elif (self.df.iloc[idx,4] == 1920):
            self.driver.find_element(By.XPATH, '''//p[contains(text(),'1920')]''').click()
        else:
            self.driver.find_elements(By.XPATH, '''//p[contains(text(),'1928')]''')[1].click()

    def choose_quiz(self, quiz_name):
        quiz_element = self.driver.find_element(By.LINK_TEXT, quiz_name)
        quiz_element.click()
        time.sleep(3)
        self.driver.find_element(By.CLASS_NAME, 'btn-primary').click()
        time.sleep(3)
        self.driver.find_element(By.NAME, 'submitbutton').click()

    def submit_quiz(self):
        self.driver.find_element(By.ID, 'mod_quiz-next-nav').click()
        time.sleep(3)
        self.driver.find_element(By.CLASS_NAME, 'btn-primary').click()
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, '.modal-footer .btn-primary').click()
        time.sleep(3)
   
    def run_test(self, idx):
        #self.log_in()
        self.driver.get('https://qa.moodledemo.net/my/courses.php')
        time.sleep(2)
        self.enter_course(COURSE_NAME)
        self.choose_quiz(QUIZ_NAME)
        self.test_all(idx)
        #self.log_out()
        

# Main
test = MoodleTest(USERNAME, PASSWORD, pd.read_excel(sys.argv[1]))
test.log_in()

for i in range(0, len(test.df)):
    test.run_test(i)
    time.sleep(1)

test.log_out()
test.driver.quit()