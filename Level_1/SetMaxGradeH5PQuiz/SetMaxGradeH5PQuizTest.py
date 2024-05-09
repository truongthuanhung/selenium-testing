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
 
class SetMaxGradeH5PQuizTest():
    def __init__(self, username, password, df):
        # Lưu thông tin của account và set up Driver
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        # df là thuộc tính lưu trữ data đọc từ bảng excel
        self.df = df
        # Method là phương pháp test hiện tại
        self.method = None
        
    def log_in(self):
        # Thưc hiện click nut login trên thành header
        log_in_button = self.driver.find_element(By.LINK_TEXT, 'Log in')
        log_in_button.click()
        # Tìm đến field username, nhập dữ liệu vào cụ thể ở đây là "student"
        username_input = self.driver.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(self.username)
        # Tìm đến field password, nhập dữ liệu vào cụ thể ở đây là "moodle"
        password_input = self.driver.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(self.password + Keys.ENTER)
        time.sleep(3)
    
    def log_out(self):
        # Click vào icon account của User để xuất cữa sổ dropdown
        menu_toggle_element = self.driver.find_element(By.ID, 'user-menu-toggle')
        menu_toggle_element.click()
        # Click chọn tuy chọn log out
        log_out_button = self.driver.find_element(By.LINK_TEXT, 'Log out')
        log_out_button.click()
        time.sleep(3)
          
    
    def setGradeH5PQuiz(self):
        with open("SetGradeH5PQuizLogs", 'w') as file:
            for i in range(0, len(self.df)):
                # tìm và click vào "My courses" trên thành điều hướng của website
                self.driver.find_element(By.LINK_TEXT , "My courses").click()
                time.sleep(3)
                
                # Tìm và click chọn vào khóa học Activity examples 
                self.driver.find_element(By.XPATH, "//div/div/div/div/div/a/div").click()
                time.sleep(3)
                
                # Tìm và click chọn vào mục H5P quizz có tên là "Global Warming"
                course_element = self.driver.find_element(By.XPATH, '//*[@id="module-1013"]/div/div[2]/div[2]/div/div/a')
                course_element.click()
                time.sleep(3)
                
                # điều hướng sang tab Settings
                self.driver.find_element(By.LINK_TEXT, 'Settings').click()
                time.sleep(3)
                
                # tìm đến mục Grade của Quiz
                self.driver.find_element(By.ID, 'collapseElement-2').click()
                time.sleep(3)            
                
                # tìm đến field grade và tiến hành bước nhập điểm 
                grade_input = self.driver.find_element(By.ID, 'id_grade_modgrade_point')
                grade_input.clear()    
                grade_input.send_keys(str(self.df.iloc[i]["GRADE"]))
                time.sleep(3)
                
                # tìm và click vào button "Save and đíplay"
                self.driver.find_element(By.ID, "id_submitbutton").click()
                time.sleep(3)
                
                # Print ra method test hiện tại
                prevMethod = self.method
                self.method = self.df.iloc[i]["METHOD_TEST"]
                if self.method != prevMethod:
                        print(self.method)
                        file.write(f" \n {self.method}\n")
                
                # handle việc verify text check và so với Expect trong testcase
                verity_test = ""
                if  self.df.iloc[i]["EXPECT"] == "Invalid grade value. This must be an integer between 1 and 100":
                    # trường hợp grade nhập vào là không hợp lệ
                    verity_test = self.driver.find_element(By.ID, "fgroup_id_error_grade").text   
                elif self.df.iloc[i]["EXPECT"] == "Recalculating grades":
                    # trường hợp grade nhập vào là hợp lệ và update thành công
                    verity_test = self.driver.find_element(By.XPATH, "//div[2]/h2").text
                
                
                if verity_test == self.df.iloc[i]["EXPECT"]:
                    print(f"PASS - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verity_test}\n")
                    file.write(f"PASS - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verity_test}\n")
                else:
                    print("FAIL -" , self.df.iloc[i]["TC_ID"] , "- EXPECT:" , self.df.iloc[i]["EXPECT"], "- RESULT",self.df.iloc[i]["NOTE"])
                    file.write(f"FAIL - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verity_test} - NOTE: {self.df.iloc[i]['NOTE']}\n")
                        
                time.sleep(2)
            
           
    
    def run_test(self):
        
        self.driver.get('https://qa.moodledemo.net/')
        
        self.driver.maximize_window()
        
        self.log_in()
        
        self.setGradeH5PQuiz()
        
        
        self.log_out()
        
        
        
        
        

# Main
test = SetMaxGradeH5PQuizTest(USERNAME, PASSWORD, pd.read_excel(sys.argv[1]))

test.run_test()

test.driver.quit()

# "cli run tetst" : "python SetMaxGradeH5PQuizTest.py SetMaxGradeH5PQuiz.xlsx"