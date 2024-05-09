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
 
class SearchCoursesTest():
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
            
     def search_courses(self):
          with open("SearchCoursesTestLogs", 'w') as file:
               # Phương thức thực hiện quá trình test chức năng search courses
               # Loop qua các testcase có trong file excel được lưu trong thuộc tính self.df
               for i in range(len(self.df)):
                    # tìm và click vào "My courses" trên thành điều hướng của website
                    self.driver.find_element(By.LINK_TEXT , "My courses").click()
                    time.sleep(3)

                    # Handle trường hợp có phải chọn thòi diểm của các khóa học ["past", "in progress" , "future", ...]
                    if not pd.isna(self.df.iloc[i]["GROUP"]):
                         # Tìm và click chọn vào ô dropdown chứa các tùy chọn về thời điểm của khóa học
                         grouping_dropdown_element = self.driver.find_element(By.XPATH , "//section/div/div/div/div/div/div/button")
                         grouping_dropdown_element.click()
                         time.sleep(2)
                         # Chọn khóa học mong muốn theo testcase 
                         group_value = self.df.iloc[i]["GROUP"]
                         grouping_element = self.driver.find_element(By.XPATH, f'//a[contains(text(), "{group_value}")]')
                         grouping_element.click()
                         time.sleep(2)
                    
                    # Handle chức năng tìm kiếm khóa học 
                    # Chọn và xóa hết dữ liệu có trong Search field 
                    search_course_element = self.driver.find_element(By.NAME, "search")
                    search_course_element.click()
                    search_course_element.clear()
                    # Nhập giá trị cần tìm vào Search field
                    search_course_element.send_keys(self.df.iloc[i]["SEARCH"])
                    time.sleep(2)
                    
                    # Print ra method test hiện tại
                    prevMethod = self.method
                    self.method = self.df.iloc[i]["METHOD_TEST"]
                    if self.method != prevMethod:
                         print(self.method)
                         file.write(f" \n {self.method}\n")
                    
                    
                    # Handle verify the result
                    if self.df.iloc[i]["EXPECT"] == "No courses":
                         time.sleep(2)
                         verify_text = self.driver.find_element(By.XPATH , "//p")
                         # Tìm đoạn văn bản thẻ "No courses" in tag p
                         if verify_text.text == "No courses":
                              # Nếu có thì -> Pass testcase
                              print(f"PASS - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verify_text.text}\n")
                              file.write(f"PASS - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verify_text.text}\n")
                         else:
                              # Nếu ko thì -> Failed testcase
                              print("FAIL -" , self.df.iloc[i]["TC_ID"] , "- EXPECT:" , self.df.iloc[i]["EXPECT"], "- RESULT",self.df.iloc[i]["NOTE"])
                              file.write(f"FAIL - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verify_text.text} - NOTE: {self.df.iloc[i]['NOTE']}\n")
                              
                    elif self.df.iloc[i]["EXPECT"] == "Activity examples":
                         time.sleep(2)
                         verify_text = self.driver.find_element(By.XPATH , "//span[3]/span[2]")
                         # Tìm đoạn văn bản thẻ "Activity examples" là đoạn text tên của môt Courses
                         if verify_text.text == "Activity examples":
                              # Nếu có thì -> Pass testcase
                              print(f"PASS - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verify_text.text}\n")
                              file.write(f"PASS - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verify_text.text}\n")
                         else:
                              # Nếu ko thì -> Failed testcase
                              print("FAIL -" , self.df.iloc[i]["TC_ID"] , "- EXPECT:" , self.df.iloc[i]["EXPECT"], "- RESULT", self.df.iloc[i]["NOTE"])
                              file.write(f"FAIL - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verify_text.text} - NOTE: {self.df.iloc[i]['NOTE']}\n")
                    
                    
                    time.sleep(2)
                    
               
               
     def run_test(self):
          self.driver.get('https://qa.moodledemo.net/')
          
          self.driver.maximize_window()
          
          # Thực hiện precontion: phải login thành công vào hệ thống
          self.log_in()
          
          # self.driver.maximize_window()
          self.search_courses()
          
          # Thực hiên log out sau khi kết thúc một testcase
          self.log_out()
          
        
# RUN TEST
 
test = SearchCoursesTest(USERNAME, PASSWORD, pd.read_excel(sys.argv[1]))

test.run_test()

test.driver.quit()


 #  "cli run test" : "python SearchCoursesTest.py SearchCoursesTC.xlsx"
